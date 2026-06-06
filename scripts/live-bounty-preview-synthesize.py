#!/usr/bin/env python3
"""Validate and synthesize live-bounty attack-path candidate packets.

This helper is offline-only. It reads local JSON planning packets and produces a
Hermes decision table. It never browses, scans, sends requests, creates accounts,
or executes attack steps.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "attack_path_candidate.schema.json"
SELECTED_EXECUTABLE_DECISION = "select_bounded_lane"


class PacketError(Exception):
    pass


def load_json(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_schema() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def validate_schema(packet: Any, label: str, schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for error in sorted(validator.iter_errors(packet), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "<root>"
        errors.append(f"{label}:{where}: {error.message}")
    return errors


def _nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(_nonempty(item) for item in value)
    if isinstance(value, dict):
        return any(_nonempty(item) for item in value.values())
    return value is not None


def validate_selected_candidate(packet: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    selected_id = packet["decision"]["selected_candidate_id"]
    decision = packet["decision"]["decision"]
    candidates = {candidate["candidate_id"]: candidate for candidate in packet["candidates"]}
    if selected_id not in candidates:
        errors.append(f"{label}:decision/selected_candidate_id does not match any candidate: {selected_id}")
        return errors

    selected = candidates[selected_id]
    if decision == SELECTED_EXECUTABLE_DECISION:
        if selected.get("execution_status") != "bounded_executable":
            errors.append(f"{label}:{selected_id}: selected executable lane must have execution_status=bounded_executable")
        for field in ["proof_boundary", "proof_surrogate", "stop_before"]:
            if not _nonempty(selected.get(field)):
                errors.append(f"{label}:{selected_id}: selected executable lane missing non-empty {field}")
        stop_before = selected.get("stop_before", {})
        for stop_key, value in stop_before.items():
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}:{selected_id}: stop_before/{stop_key} must be explicit")
        proof_surrogate = selected.get("proof_surrogate", {})
        for proof_key in ["method", "why_it_proves_impact_without_harm", "positive_control", "negative_control"]:
            if not isinstance(proof_surrogate.get(proof_key), str) or not proof_surrogate[proof_key].strip():
                errors.append(f"{label}:{selected_id}: proof_surrogate/{proof_key} must be explicit")
    else:
        if selected.get("execution_status") == "bounded_executable":
            errors.append(f"{label}:{selected_id}: bounded_executable candidate should use decision=select_bounded_lane or change execution_status")
    return errors


def synthesize_packet(packet: dict[str, Any], source: str) -> dict[str, Any]:
    selected_id = packet["decision"]["selected_candidate_id"]
    rows = []
    for candidate in packet["candidates"]:
        boundary = candidate["proof_boundary"]
        surrogate = candidate["proof_surrogate"]
        stop_before = candidate["stop_before"]
        rows.append(
            {
                "source": source,
                "program_slug": packet["program_slug"],
                "packet_id": packet["packet_id"],
                "candidate_id": candidate["candidate_id"],
                "selected": candidate["candidate_id"] == selected_id,
                "execution_status": candidate["execution_status"],
                "title": candidate["title"],
                "impact_hypothesis": candidate["impact_hypothesis"],
                "impact_potential": candidate["impact_potential"],
                "surrogate_feasibility": candidate["surrogate_feasibility"],
                "authorization_readiness": candidate["authorization_readiness"],
                "composite_rank": candidate["impact_potential"] + candidate["surrogate_feasibility"] + candidate["authorization_readiness"],
                "request_budget": boundary["request_budget"],
                "proof_surrogate": surrogate["method"],
                "stop_before_keys": sorted(stop_before.keys()),
                "evidence_requirements": candidate["evidence_requirements"],
            }
        )
    rows.sort(
        key=lambda row: (
            row["selected"],
            row["execution_status"] == "bounded_executable",
            row["impact_potential"],
            row["surrogate_feasibility"],
            row["authorization_readiness"],
            row["candidate_id"],
        ),
        reverse=True,
    )
    return {
        "source": source,
        "program_slug": packet["program_slug"],
        "packet_id": packet["packet_id"],
        "decision": packet["decision"],
        "rows": rows,
    }


def cmd_validate(args: argparse.Namespace) -> int:
    schema = load_schema()
    errors: list[str] = []
    for packet_path in args.packets:
        packet = load_json(packet_path)
        errors.extend(validate_schema(packet, packet_path, schema))
        if not errors:
            errors.extend(validate_selected_candidate(packet, packet_path))
    print(json.dumps({"status": "error" if errors else "ok", "errors": errors}, indent=2, ensure_ascii=False))
    return 1 if errors else 0


def cmd_synthesize(args: argparse.Namespace) -> int:
    schema = load_schema()
    errors: list[str] = []
    summaries: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []

    for packet_path in args.packets:
        packet = load_json(packet_path)
        packet_errors = validate_schema(packet, packet_path, schema)
        if not packet_errors:
            packet_errors.extend(validate_selected_candidate(packet, packet_path))
        errors.extend(packet_errors)
        if packet_errors:
            continue
        summary = synthesize_packet(packet, packet_path)
        summaries.append(summary)
        selected_rows.extend(row for row in summary["rows"] if row["selected"])

    executable_selected = [row for row in selected_rows if row["execution_status"] == "bounded_executable"]
    if len(executable_selected) > 1:
        errors.append("synthesis: more than one bounded executable live lane is selected across packets")

    result = {
        "status": "error" if errors else "ok",
        "target_touching": False,
        "runner_mode": "offline_attack_path_synthesis_only",
        "errors": errors,
        "selected_rows": [] if errors else selected_rows,
        "packets": [] if errors else summaries,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if errors else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline live-bounty attack-path preview synthesizer")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate attack-path candidate packet JSON")
    validate.add_argument("packets", nargs="+", help="Packet JSON files")
    validate.set_defaults(func=cmd_validate)

    synthesize = sub.add_parser("synthesize", help="Synthesize one or more packet JSON files")
    synthesize.add_argument("packets", nargs="+", help="Packet JSON files")
    synthesize.set_defaults(func=cmd_synthesize)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
