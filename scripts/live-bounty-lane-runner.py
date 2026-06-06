#!/usr/bin/env python3
"""Local-only live-bounty lane runner.

This runner does not touch targets. It reads the machine lane queue, validates the
selected lane state, and emits the next checkpoint/action as JSON so Hermes can
resume work systematically without turning every lane into prose-only state.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
LANE_SCHEMA_PATH = ROOT / "schemas" / "live_bounty_lane_state.schema.json"

READY_STATUSES = {"ready", "ready_autonomous", "ready_local_preview", "ready_local_orchestration"}
OPERATOR_BLOCKED_STATUSES = {"blocked_operator_action"}
SCOPE_BLOCKED_STATUSES = {"blocked_awaiting_scope", "blocked_scope_or_policy", "blocked_policy_ambiguity"}
CLOSED_OR_PARKED_STATUSES = {"no_finding", "surface_only", "parked"}

EXIT_READY = 0
EXIT_OPERATOR_BLOCKED = 10
EXIT_SCOPE_BLOCKED = 20
EXIT_INVALID = 30

TARGET_TOUCHING_OPTIONS = {"--target", "--url", "--host", "--scope", "--live"}


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def resolve_path(path_value: str) -> Path:
    # Windows-host Hermes runs through MSYS/Git-Bash. CLI path arguments are
    # usually converted by the shell, but paths embedded inside JSON are not.
    # Support the common MSYS absolute forms so temp-fixture queues and repo
    # paths validate the same way from bash and Python.
    if os.name == "nt" and path_value.startswith("/c/"):
        return Path("C:/" + path_value[3:])
    if os.name == "nt" and path_value.startswith("/tmp/"):
        return Path(os.environ.get("TEMP", "C:/tmp")) / path_value[len("/tmp/"):]
    path = Path(path_value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def load_lane_schema() -> dict:
    schema = load_json(LANE_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return schema


def validate_doc(doc: Any, schema: dict, label: str) -> list[str]:
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for error in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "<root>"
        errors.append(f"{label}:{where}: {error.message}")
    return errors


def validate_queue(queue: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(queue, dict):
        return ["queue:<root>: must be object"]
    if queue.get("schema_version") != "1.0":
        errors.append("queue:schema_version must be 1.0")
    lanes = queue.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        errors.append("queue:lanes must be a non-empty list")
        return errors
    seen_priorities: set[int] = set()
    for idx, lane in enumerate(lanes):
        if not isinstance(lane, dict):
            errors.append(f"queue:lanes/{idx}: must be object")
            continue
        for field in ["program_slug", "lane_id", "state_file", "priority", "status"]:
            if field not in lane:
                errors.append(f"queue:lanes/{idx}: missing {field}")
        priority = lane.get("priority")
        if priority is not None:
            if not isinstance(priority, int):
                errors.append(f"queue:lanes/{idx}/priority: must be integer")
            elif priority in seen_priorities:
                errors.append(f"queue:lanes/{idx}/priority: duplicate priority {priority}")
            else:
                seen_priorities.add(priority)
        state_file = lane.get("state_file")
        if isinstance(state_file, str):
            candidate = resolve_path(state_file)
            if not candidate.exists():
                errors.append(f"queue:lanes/{idx}/state_file does not exist: {state_file}")
        elif "state_file" in lane:
            errors.append(f"queue:lanes/{idx}/state_file: must be string")
    return errors


def select_lane(queue: dict) -> dict:
    lanes = queue["lanes"]
    return sorted(lanes, key=lambda lane: lane["priority"])[0]


def decide(state: dict) -> tuple[str, int, list[str]]:
    status = state.get("status")
    state_name = state.get("state", "")
    if status in READY_STATUSES or "READY_AUTONOMOUS" in state_name:
        return "autonomous_local_action_available", EXIT_READY, []
    if status in OPERATOR_BLOCKED_STATUSES:
        return "blocked_operator_action", EXIT_OPERATOR_BLOCKED, []
    if status in SCOPE_BLOCKED_STATUSES:
        return "blocked_scope_or_policy", EXIT_SCOPE_BLOCKED, []
    if status in CLOSED_OR_PARKED_STATUSES:
        return "lane_closed_or_parked", EXIT_READY, []
    return "invalid_queue_or_state", EXIT_INVALID, [f"unsupported lane status for runner: {status}"]


def build_result(*, decision: str, exit_code: int, errors: list[str], queue_path: str | None = None,
                 queue_entry: dict | None = None, state: dict | None = None) -> dict:
    result: dict[str, Any] = {
        "schema_version": "1.0",
        "runner": "live-bounty-lane-runner",
        "runner_mode": "local_orchestration_only",
        "target_touching": False,
        "decision": decision,
        "exit_code": exit_code,
        "errors": errors,
        "queue_path": queue_path,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    if queue_entry is not None:
        result["queue_entry"] = queue_entry
    if state is not None:
        result.update({
            "program_slug": state.get("program_slug"),
            "lane_id": state.get("lane_id"),
            "lane_title": state.get("lane_title"),
            "autonomy_level": state.get("autonomy_level"),
            "state": state.get("state"),
            "status": state.get("status"),
            "next_autonomous_action": state.get("next_autonomous_action"),
            "next_operator_action": state.get("next_operator_action"),
            "operator_gates": state.get("operator_gates", []),
            "stop_conditions": state.get("stop_conditions", []),
            "allowed_actions": state.get("lane_boundary", {}).get("allowed_actions", []),
            "blocked_actions": state.get("lane_boundary", {}).get("blocked_actions", []),
            "dry_run_gate": state.get("authorization", {}).get("dry_run_gate"),
            "out_of_scope_control": state.get("authorization", {}).get("out_of_scope_control"),
            "artifacts": state.get("artifacts", {}),
            "next_preview_seed": state.get("learning", {}).get("next_preview_seed"),
        })
    return result


def emit(result: dict, status_out: str | None) -> None:
    text = json.dumps(result, indent=2, ensure_ascii=False)
    print(text)
    if status_out:
        out = Path(status_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")


def has_target_touching_args(argv: list[str]) -> bool:
    return any(arg in TARGET_TOUCHING_OPTIONS or any(arg.startswith(opt + "=") for opt in TARGET_TOUCHING_OPTIONS) for arg in argv)


def option_value(argv: list[str], option: str) -> str | None:
    for idx, arg in enumerate(argv):
        if arg == option and idx + 1 < len(argv) and not argv[idx + 1].startswith("--"):
            return argv[idx + 1]
        prefix = option + "="
        if arg.startswith(prefix):
            return arg[len(prefix):]
    return None


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Local-only live-bounty lane queue runner")
    parser.add_argument("--queue", required=True, help="Path to handoff/live_bounty_lane_queue.json")
    parser.add_argument("--status-out", help="Optional path to write runner status JSON")
    # Accepted only so the runner can return structured fail-closed JSON instead
    # of argparse text if a future caller accidentally passes target-like flags.
    parser.add_argument("--target")
    parser.add_argument("--url")
    parser.add_argument("--host")
    parser.add_argument("--scope")
    parser.add_argument("--live", action="store_true")
    if has_target_touching_args(argv):
        queue_path = option_value(argv, "--queue")
        status_out = option_value(argv, "--status-out")
        result = build_result(
            decision="invalid_queue_or_state",
            exit_code=EXIT_INVALID,
            errors=["target-touching arguments are not supported by this local-only runner"],
            queue_path=queue_path,
        )
        emit(result, status_out)
        return EXIT_INVALID

    args = parser.parse_args(argv)

    try:
        queue = load_json(args.queue)
        errors = validate_queue(queue)
        if errors:
            result = build_result(
                decision="invalid_queue_or_state",
                exit_code=EXIT_INVALID,
                errors=errors,
                queue_path=args.queue,
            )
            emit(result, args.status_out)
            return EXIT_INVALID

        queue_entry = select_lane(queue)
        state_path = resolve_path(queue_entry["state_file"])
        state = load_json(state_path)
        errors = validate_doc(state, load_lane_schema(), "state")
        for field in ["program_slug", "lane_id", "status"]:
            if queue_entry.get(field) != state.get(field):
                errors.append(f"queue/state mismatch for {field}: queue={queue_entry.get(field)!r} state={state.get(field)!r}")
        if errors:
            result = build_result(
                decision="invalid_queue_or_state",
                exit_code=EXIT_INVALID,
                errors=errors,
                queue_path=args.queue,
                queue_entry=queue_entry,
            )
            emit(result, args.status_out)
            return EXIT_INVALID

        decision, exit_code, decision_errors = decide(state)
        result = build_result(
            decision=decision,
            exit_code=exit_code,
            errors=decision_errors,
            queue_path=args.queue,
            queue_entry=queue_entry,
            state=state,
        )
        emit(result, args.status_out)
        return exit_code
    except Exception as exc:  # fail closed with structured output
        result = build_result(
            decision="invalid_queue_or_state",
            exit_code=EXIT_INVALID,
            errors=[f"runner exception: {type(exc).__name__}: {exc}"],
            queue_path=args.queue,
        )
        emit(result, args.status_out)
        return EXIT_INVALID


if __name__ == "__main__":
    raise SystemExit(main())
