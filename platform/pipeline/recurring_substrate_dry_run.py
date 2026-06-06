#!/usr/bin/env python3
"""Build operator-inbox candidates from offline/passive recurring inputs.

This is intentionally dry-run/no-target only. It does not perform network
requests, read program secrets, or authorize live recurring automation.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except Exception:  # pragma: no cover - project tests install jsonschema
    Draft202012Validator = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA = ROOT / "schemas" / "operator_inbox_candidate.schema.json"
BLOCKED_ACTIONS = [
    "live_target_contact",
    "active_scanning",
    "fuzzing",
    "callbacks_oast_tunnels",
    "live_proof_attempts",
    "credential_or_token_handling",
    "report_submission",
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9_.-]+", "_", value.lower()).strip("_.-")
    return slug or "candidate"


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def make_error(errors: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "status": "error",
        "mode": "dry_run_no_target",
        "target_touching": False,
        "candidate_count": 0,
        "errors": errors,
        "candidates": [],
    }


def decision_to_machine_state(decision: str) -> str:
    if decision == "KILL":
        return "NO_FINDING_CLOSEOUT"
    if decision == "PARK":
        return "PARKED"
    return "CANDIDATE_REVIEW"


def normalize_decision(value: str | None) -> str:
    if value in {"PASSIVE_ONLY", "PARK", "KILL"}:
        return value
    # Dry-run/no-target substrate must not promote passive input to EXECUTE.
    # Treat EXECUTE or unknown upstream recommendations as candidate review only.
    return "PASSIVE_ONLY"


def candidate_from_item(item: dict[str, Any]) -> dict[str, Any]:
    source_id = str(item.get("id") or item.get("source_id") or item.get("title") or "candidate")
    decision = normalize_decision(item.get("recommended_decision"))
    return {
        "candidate_id": slugify(source_id),
        "title": str(item.get("title") or source_id),
        "summary": str(item.get("summary") or "Offline/passive recurring substrate candidate awaiting review."),
        "source_kind": "offline_passive_intel",
        "source_id": source_id,
        "affected_technology": str(item.get("affected_technology") or "unknown"),
        "operator_decision": decision,
        "machine_state": decision_to_machine_state(decision),
        "recommended_next_step": "Review in operator inbox; require program policy/scope gate before any live or target-touching action.",
        "references": list(item.get("references") or ([item["source_url"]] if item.get("source_url") else [])),
        "safety": {
            "target_touching": False,
            "live_activation_allowed": False,
            "requires_policy_scope_gate": True,
            "blocked_actions": BLOCKED_ACTIONS,
        },
    }


def build_batch(source: dict[str, Any]) -> dict[str, Any]:
    items = source.get("items")
    if not isinstance(items, list):
        return make_error(["input:items must be a list"])
    candidates = [candidate_from_item(item) for item in items if isinstance(item, dict)]
    return {
        "schema_version": "1.0",
        "status": "ok",
        "mode": "dry_run_no_target",
        "target_touching": False,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def validate_batch(batch: dict[str, Any], schema_path: Path) -> list[str]:
    if Draft202012Validator is None:
        return []
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = []
    for err in sorted(validator.iter_errors(batch), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in err.path) or "<root>"
        errors.append(f"{where}: {err.message}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dry-run recurring substrate candidate builder")
    parser.add_argument("--input", required=True, help="Offline/passive intel JSON input")
    parser.add_argument("--out", required=True, help="Output candidate batch JSON")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="Candidate schema path")
    parser.add_argument("--live", action="store_true", help="Rejected: live mode is not implemented in this dry-run harness")
    args = parser.parse_args(argv)

    out_path = Path(args.out)
    if args.live:
        result = make_error(["--live is not supported by recurring_substrate_dry_run.py; use policy-gated scheduler only after explicit approval"])
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 2

    try:
        result = build_batch(load_json(args.input))
        if result["status"] == "ok":
            validation_errors = validate_batch(result, Path(args.schema))
            if validation_errors:
                result = make_error(validation_errors)
    except Exception as exc:
        result = make_error([f"input error: {exc}"])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    out_path.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
