#!/usr/bin/env python3
"""Validate and summarize live-bounty lane state.

This is an orchestration/status helper, not a target-touching runner. It turns
markdown handoff state into machine-checkable JSON so future automation can
resume at lane-level checkpoints instead of asking for every minor step.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
LANE_SCHEMA_PATH = ROOT / "schemas" / "live_bounty_lane_state.schema.json"
EVIDENCE_SCHEMA_PATH = ROOT / "schemas" / "live_bounty_evidence.schema.json"


def load_json_arg(path_or_dash: str) -> Any:
    if path_or_dash == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path_or_dash).read_text(encoding="utf-8"))


def load_schema(path: Path) -> dict:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def validate_doc(doc: Any, schema: dict, label: str) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "<root>"
        errors.append(f"{label}:{where}: {error.message}")
    return errors


def validate_queue(queue: dict) -> list[str]:
    errors: list[str] = []
    if queue.get("schema_version") != "1.0":
        errors.append("queue:schema_version must be 1.0")
    lanes = queue.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        errors.append("queue:lanes must be a non-empty list")
        return errors
    for idx, lane in enumerate(lanes):
        if not isinstance(lane, dict):
            errors.append(f"queue:lanes/{idx}: must be object")
            continue
        for field in ["program_slug", "lane_id", "state_file", "priority", "status"]:
            if field not in lane:
                errors.append(f"queue:lanes/{idx}: missing {field}")
        if "priority" in lane and not isinstance(lane["priority"], int):
            errors.append(f"queue:lanes/{idx}/priority: must be integer")
        state_file = lane.get("state_file")
        if isinstance(state_file, str):
            candidate = Path(state_file)
            if not candidate.is_absolute():
                candidate = ROOT / candidate
            if not candidate.exists():
                errors.append(f"queue:lanes/{idx}/state_file does not exist: {state_file}")
    return errors


def summarize_lane(state: dict, evidence: dict | None = None) -> dict:
    return {
        "program_slug": state["program_slug"],
        "lane_id": state["lane_id"],
        "autonomy_level": state["autonomy_level"],
        "state": state["state"],
        "status": state["status"],
        "next_autonomous_action": state["next_autonomous_action"],
        "next_operator_action": state["next_operator_action"],
        "operator_gates": state.get("operator_gates", []),
        "dry_run_gate": state.get("authorization", {}).get("dry_run_gate"),
        "out_of_scope_control": state.get("authorization", {}).get("out_of_scope_control"),
        "evidence_status": evidence.get("status") if evidence else None,
    }


def cmd_validate(args: argparse.Namespace) -> int:
    lane_schema = load_schema(LANE_SCHEMA_PATH)
    evidence_schema = load_schema(EVIDENCE_SCHEMA_PATH)

    if args.state_json:
        state = load_json_arg(args.state_json)
    elif args.state:
        state = load_json_arg(args.state)
    else:
        raise SystemExit("validate requires --state or --state-json")

    evidence = load_json_arg(args.evidence) if args.evidence else None
    queue = load_json_arg(args.queue) if args.queue else None

    errors = validate_doc(state, lane_schema, "state")
    if evidence is not None:
        errors.extend(validate_doc(evidence, evidence_schema, "evidence"))
    if queue is not None:
        errors.extend(validate_queue(queue))

    result = {
        "status": "error" if errors else "ok",
        "errors": errors,
        "lane": summarize_lane(state, evidence) if not errors else None,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if errors else 0


def cmd_queue(args: argparse.Namespace) -> int:
    queue = load_json_arg(args.queue)
    errors = validate_queue(queue)
    result = {"status": "error" if errors else "ok", "errors": errors, "queue": queue if not errors else None}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if errors else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Live bounty lane status helper")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate lane/evidence/queue JSON and print summary")
    validate.add_argument("--state", help="Path to lane state JSON")
    validate.add_argument("--state-json", help="Lane state JSON path or '-' for stdin")
    validate.add_argument("--evidence", help="Optional evidence JSON path")
    validate.add_argument("--queue", help="Optional queue JSON path")
    validate.set_defaults(func=cmd_validate)

    queue = sub.add_parser("queue", help="Validate and print lane queue")
    queue.add_argument("--queue", required=True)
    queue.set_defaults(func=cmd_queue)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
