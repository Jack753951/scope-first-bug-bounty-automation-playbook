#!/usr/bin/env python3
"""Offline role-conflict synthesis for attack-path planning packets.

Reads local JSON only. It never browses, scans, sends requests, starts VMs, or
executes attack steps.
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
SCHEMA_PATH = ROOT / "schemas" / "attack_path_role_synthesis.schema.json"
CANDIDATE_SCHEMA_PATH = ROOT / "schemas" / "attack_path_candidate.schema.json"
FORBIDDEN_ARGS = {"--target", "--url", "--host", "--scope", "--live"}
BAD_VERDICTS = {"REQUEST_CHANGES", "BLOCKED", "FAIL"}
DOWNGRADED_DECISIONS = {"park_preserve", "blocked_awaiting_scope", "blocked_awaiting_operator", "needs_local_simulation", "no_selection"}


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


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_schema(path: Path) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def schema_errors(data: Any, schema: dict[str, Any], label: str) -> list[str]:
    errors = []
    for error in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "<root>"
        errors.append(f"{label}:{where}: {error.message}")
    return errors


def semantic_errors(packet: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    decision = packet["decision"]
    selected = decision["selected_candidate_id"]
    selected_blockers = [r for r in packet["role_inputs"] if selected and selected in r.get("candidate_ids", []) and r["verdict"] in BAD_VERDICTS]
    if selected_blockers and decision["decision"] == "select_bounded_lane":
        errors.append(f"{label}: selected candidate {selected} has blocking role verdicts and cannot remain select_bounded_lane")
    if selected_blockers and decision["decision"] in DOWNGRADED_DECISIONS:
        resolved_roles = {role for c in packet.get("conflicts", []) for role in c.get("roles", []) if c.get("candidate_id") == selected and c.get("resolution") in {"downgrade", "park", "block", "needs_operator", "needs_local_simulation"}}
        missing = sorted({r["role"] for r in selected_blockers} - resolved_roles)
        if missing:
            errors.append(f"{label}: downgraded selected candidate {selected} lacks explicit conflict resolution for roles: {', '.join(missing)}")
    return errors


def candidate_selected(packet: dict[str, Any]) -> str:
    return packet.get("decision", {}).get("selected_candidate_id", "")


def cmd_validate(args: argparse.Namespace) -> int:
    schema = load_schema(SCHEMA_PATH)
    errors: list[str] = []
    for path in args.input:
        data = load_json(path)
        errs = schema_errors(data, schema, path)
        if not errs:
            errs.extend(semantic_errors(data, path))
        errors.extend(errs)
    print(json.dumps({"status": "error" if errors else "ok", "target_touching": False, "errors": errors}, indent=2, ensure_ascii=False))
    return 1 if errors else 0


def cmd_synthesize(args: argparse.Namespace) -> int:
    candidate_schema = load_schema(CANDIDATE_SCHEMA_PATH)
    candidate_packet = load_json(args.candidate_packet)
    errors = schema_errors(candidate_packet, candidate_schema, args.candidate_packet)
    role_inputs = [load_json(path) for path in args.role_artifact]
    selected = candidate_selected(candidate_packet)
    if not selected:
        errors.append("candidate packet has no selected candidate")
    conflicts: list[dict[str, Any]] = []
    bad_roles = [r for r in role_inputs if selected in r.get("candidate_ids", []) and r.get("verdict") in BAD_VERDICTS]
    decision = candidate_packet.get("decision", {}).get("decision", "no_selection")
    if bad_roles and decision == "select_bounded_lane":
        conflicts.append({
            "conflict_id": f"{selected}_blocking_role_verdict",
            "type": "role_disagreement",
            "candidate_id": selected,
            "roles": [r["role"] for r in bad_roles],
            "summary": "One or more roles blocked or requested changes for the selected candidate.",
            "resolution": "park",
            "reason": "Blocking role verdicts must preserve the idea without authorizing execution."
        })
        out_decision = "park_preserve"
        reason = "Selected lane downgraded because role review found blockers."
    else:
        out_decision = decision if decision in {"select_bounded_lane", "park_preserve", "blocked_awaiting_scope", "blocked_awaiting_operator", "switch_target", "needs_local_simulation"} else "no_selection"
        reason = candidate_packet.get("decision", {}).get("reason", "role synthesis completed")
    result = {
        "schema_version": "1.0",
        "synthesis_id": f"{candidate_packet.get('packet_id', 'packet')}_role_synthesis",
        "program_slug": candidate_packet.get("program_slug", "unknown"),
        "source_packets": [args.candidate_packet] + args.role_artifact,
        "role_inputs": role_inputs,
        "conflicts": conflicts,
        "decision": {
            "selected_candidate_id": selected,
            "decision": out_decision,
            "reason": reason,
            "required_next_artifact": "handoff/kali_vm_operations_state.json" if out_decision == "select_bounded_lane" else "handoff/live_bounty_learning_seeds.jsonl",
            "needs_kali_readiness_check": out_decision == "select_bounded_lane",
            "learning_seed_if_blocked": "required" if out_decision != "select_bounded_lane" else ""
        },
        "updated_at": date.today().isoformat(),
        "target_touching": False
    }
    schema = load_schema(SCHEMA_PATH)
    errors.extend(schema_errors(result, schema, "synthesis"))
    if not errors:
        errors.extend(semantic_errors(result, "synthesis"))
    if errors:
        print(json.dumps({"status": "error", "target_touching": False, "errors": errors}, indent=2, ensure_ascii=False))
        return 1
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    reject_target_like_args(argv)
    parser = argparse.ArgumentParser(description="Offline attack-path role synthesis")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("--input", action="append", required=True)
    validate.set_defaults(func=cmd_validate)
    synth = sub.add_parser("synthesize")
    synth.add_argument("--candidate-packet", required=True)
    synth.add_argument("--role-artifact", action="append", required=True)
    synth.add_argument("--out")
    synth.set_defaults(func=cmd_synthesize)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
