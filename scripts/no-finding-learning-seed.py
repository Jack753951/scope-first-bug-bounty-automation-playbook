#!/usr/bin/env python3
"""Create and validate local no-finding learning seed artifacts.

This is not an evidence promotion path. It only turns no-finding/surface/blocked
outcomes into compact future-selection hints.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "no_finding_learning_seed.schema.json"
EVIDENCE_SCHEMA_PATH = ROOT / "schemas" / "live_bounty_evidence.schema.json"
FORBIDDEN_ARGS = {"--target", "--url", "--host", "--scope", "--live"}
ALLOWED_EVIDENCE = {"no_finding", "surface_only", "blocked", "blocked_operator_action", "blocked_awaiting_scope", "not_report_ready"}
OUTCOME_MAP = {"blocked": "blocked_operator_action"}


def reject_target_like_args(argv: list[str]) -> None:
    seen = []
    for arg in argv:
        if arg in FORBIDDEN_ARGS:
            seen.append(arg)
        elif any(arg.startswith(flag + "=") for flag in FORBIDDEN_ARGS):
            seen.append(arg.split("=", 1)[0])
    seen = sorted(set(seen))
    if seen:
        print(json.dumps({"status": "error", "target_touching": False, "exit_code": 30, "errors": [f"forbidden target-like argument: {arg}" for arg in seen]}, indent=2))
        raise SystemExit(30)


def load_schema(path: Path) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def schema_errors(data: Any, schema_path: Path, label: str) -> list[str]:
    schema = load_schema(schema_path)
    errors = []
    for error in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "<root>"
        errors.append(f"{label}:{where}: {error.message}")
    return errors


def semantic_errors(seed: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    if seed.get("target_touching") is not False:
        errors.append(f"{label}: target_touching must remain false")
    if not seed.get("negative_findings"):
        errors.append(f"{label}: negative_findings must explain what was checked")
    if seed.get("outcome") in {"surface_only", "no_finding"} and not seed.get("target_selection_updates"):
        errors.append(f"{label}: no_finding/surface_only seeds require target_selection_updates")
    return errors


def cmd_validate(args: argparse.Namespace) -> int:
    data = load_json(args.input)
    errors = schema_errors(data, SCHEMA_PATH, args.input)
    if not errors:
        errors.extend(semantic_errors(data, args.input))
    print(json.dumps({"status": "error" if errors else "ok", "target_touching": False, "errors": errors}, indent=2, ensure_ascii=False))
    return 1 if errors else 0


def cmd_summarize(args: argparse.Namespace) -> int:
    data = load_json(args.input)
    errors = schema_errors(data, SCHEMA_PATH, args.input)
    if not errors:
        errors.extend(semantic_errors(data, args.input))
    if errors:
        print(json.dumps({"status": "error", "target_touching": False, "errors": errors}, indent=2, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "ok", "target_touching": False, "outcome": data["outcome"], "missing_prerequisites": data["missing_prerequisites"], "target_selection_updates": data["target_selection_updates"], "next_attack_path_seeds": data["next_attack_path_seeds"]}, indent=2, ensure_ascii=False))
    return 0


def cmd_from_evidence(args: argparse.Namespace) -> int:
    evidence = load_json(args.evidence)
    errors = schema_errors(evidence, EVIDENCE_SCHEMA_PATH, args.evidence)
    status = evidence.get("status")
    if status not in ALLOWED_EVIDENCE:
        errors.append(f"{args.evidence}: status {status!r} is not allowed for no-finding learning seed")
    if errors:
        print(json.dumps({"status": "error", "target_touching": False, "errors": errors}, indent=2, ensure_ascii=False))
        return 1
    outcome = OUTCOME_MAP.get(status, status)
    missing = evidence.get("blocked_states") or [evidence.get("next_learning_seed", "operator/control prerequisite unclear")]
    observations = evidence.get("observations", [])
    observed = "; ".join(o.get("label", "observation") for o in observations[:3]) or "local evidence packet reviewed"
    seed = {
        "schema_version": "1.0",
        "seed_id": f"{evidence['program_slug']}_{evidence['lane_id']}_learning_seed",
        "program_slug": evidence["program_slug"],
        "lane_id": evidence["lane_id"],
        "source_evidence": args.evidence,
        "outcome": outcome,
        "negative_findings": [{"hypothesis": evidence.get("next_learning_seed", "lane did not produce reportable evidence"), "evidence": observed, "confidence": "medium", "do_not_retry_without": missing}],
        "missing_prerequisites": missing,
        "target_selection_updates": ["prefer targets/lanes where the missing prerequisite is available before repeating this path"],
        "next_attack_path_seeds": [{"title": "Retry only after missing controls exist", "rationale": evidence.get("next_learning_seed", "previous lane lacked reportable signal"), "required_prerequisites": missing, "preferred_roles": ["adversarial-planner", "boundary-engineer", "evidence-critic"], "route": "same_target_after_operator_gate" if status.startswith("blocked") else "new_target"}],
        "updated_at": date.today().isoformat(),
        "target_touching": False
    }
    errors = schema_errors(seed, SCHEMA_PATH, "seed") + semantic_errors(seed, "seed")
    if errors:
        print(json.dumps({"status": "error", "target_touching": False, "errors": errors}, indent=2, ensure_ascii=False))
        return 1
    if args.out:
        Path(args.out).write_text(json.dumps(seed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(seed, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    reject_target_like_args(argv)
    parser = argparse.ArgumentParser(description="Offline no-finding learning seed helper")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("--input", required=True)
    validate.set_defaults(func=cmd_validate)
    summarize = sub.add_parser("summarize")
    summarize.add_argument("--input", required=True)
    summarize.set_defaults(func=cmd_summarize)
    from_ev = sub.add_parser("from-evidence")
    from_ev.add_argument("--evidence", required=True)
    from_ev.add_argument("--out")
    from_ev.set_defaults(func=cmd_from_evidence)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
