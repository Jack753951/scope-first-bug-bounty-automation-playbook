#!/usr/bin/env python3
# TRIAL ONLY — no schema promotion, no drafting, offline fixture-chain only.
"""Offline candidate workflow fixture builder (P2.23, trial-only).

Builds one deterministic, fixture-only end-to-end candidate review workflow
artifact by chaining the P2.19 through P2.22 trial helpers in memory:

finding fixtures -> candidate review packet -> gap report -> verification plan
-> report-readiness gate.

This script is an offline workflow demonstrator only. It reads allowlisted
committed finding fixtures through the existing P2.19 builder and emits one JSON
document to stdout. It performs no live scans, no target interaction, no network
calls, no process launches, no runtime wiring, no schema promotion, no report
drafting, and no output-file writes.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

WORKFLOW_SCHEMA_VERSION = "candidate_workflow_fixture/0.1-trial"
SOURCE_SCHEMA_VERSIONS = [
    "candidate_review_packet/0.1-trial",
    "candidate_review_gap_report/0.1-trial",
    "candidate_verification_plan/0.1-trial",
    "report_readiness_gate/0.1-trial",
]

LIVE_TARGET_FLAGS = frozenset({"--target", "--url", "--host", "--scope", "--live"})
_ALLOWED_FLAGS = frozenset({"--repo-root", "--input", "--json"})


class WorkflowError:
    def __init__(self, code: str, path: str, message: str, stage: str | None = None) -> None:
        self.code = code
        self.path = path
        self.message = message
        self.stage = stage

    def as_dict(self) -> dict[str, str]:
        data = {"code": self.code, "path": self.path, "message": self.message}
        if self.stage is not None:
            data["stage"] = self.stage
        return data


def _load_script_module(filename: str, module_name: str) -> Any:
    target = Path(__file__).resolve().parent / filename
    existing = sys.modules.get(module_name)
    if existing is not None:
        return existing
    spec = importlib.util.spec_from_file_location(module_name, target)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{filename} could not be located")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def _builder() -> Any:
    return _load_script_module("build_candidate_review_packet.py", "_p2_23_candidate_packet_builder")


def _gap_consumer() -> Any:
    return _load_script_module("review_candidate_packet_gaps.py", "_p2_23_gap_consumer")


def _planner() -> Any:
    return _load_script_module("build_candidate_verification_plan.py", "_p2_23_verification_planner")


def _gate() -> Any:
    return _load_script_module("build_report_readiness_gate.py", "_p2_23_report_readiness_gate")


def _empty_summary(input_count: int = 0) -> dict[str, int]:
    return {
        "input_count": input_count,
        "candidate_count": 0,
        "gap_finding_count": 0,
        "verification_plan_count": 0,
        "gate_result_count": 0,
        "blocked_count": 0,
        "needs_manual_review_count": 0,
    }


def _error_payload(errors: list[WorkflowError], artifacts: dict[str, Any] | None = None, input_count: int = 0) -> dict[str, Any]:
    return {
        "schema_version": WORKFLOW_SCHEMA_VERSION,
        "status": "error",
        "source_schema_versions": SOURCE_SCHEMA_VERSIONS,
        "summary": _empty_summary(input_count),
        "artifacts": artifacts or {},
        "errors": [error.as_dict() for error in errors],
    }


def _compact_emit(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")


def _stage_error(stage: str, payload: Any) -> WorkflowError:
    stage_errors = []
    if isinstance(payload, dict) and isinstance(payload.get("errors"), list):
        stage_errors = payload["errors"]
    if stage_errors:
        first = stage_errors[0]
        if isinstance(first, dict):
            code = first.get("code") if isinstance(first.get("code"), str) else "UNKNOWN_STAGE_ERROR"
            path = first.get("path") if isinstance(first.get("path"), str) else stage
            message = first.get("message") if isinstance(first.get("message"), str) else "stage failed"
            return WorkflowError("WORKFLOW_STAGE_FAILED", path, f"{code}: {message}", stage=stage)
    return WorkflowError("WORKFLOW_STAGE_FAILED", stage, "workflow stage failed closed", stage=stage)


def _summary(artifacts: dict[str, Any], input_count: int) -> dict[str, int]:
    packet = artifacts["candidate_review_packet"]
    gap_report = artifacts["candidate_review_gap_report"]
    plan = artifacts["candidate_verification_plan"]
    gate = artifacts["report_readiness_gate"]
    return {
        "input_count": input_count,
        "candidate_count": packet["summary"]["candidate_count"],
        "gap_finding_count": gap_report["summary"]["finding_count"],
        "verification_plan_count": plan["summary"]["finding_count"],
        "gate_result_count": gate["summary"]["finding_count"],
        "blocked_count": gate["summary"]["blocked_count"],
        "needs_manual_review_count": gate["summary"]["needs_manual_review_count"],
    }


def build_workflow_fixture(repo_root: str | Path, inputs: list[str]) -> dict[str, Any]:
    """Return one deterministic P2.23 offline workflow fixture document."""
    input_count = len(inputs)
    artifacts: dict[str, Any] = {}

    packet = _builder().build_packet(repo_root, inputs)
    artifacts["candidate_review_packet"] = packet
    if packet.get("status") != "ok":
        return _error_payload([_stage_error("candidate_review_packet", packet)], artifacts, input_count)

    gap_report = _gap_consumer().review_packet(packet)
    artifacts["candidate_review_gap_report"] = gap_report
    if gap_report.get("status") != "ok":
        return _error_payload([_stage_error("candidate_review_gap_report", gap_report)], artifacts, input_count)

    plan = _planner().build_plan(gap_report)
    artifacts["candidate_verification_plan"] = plan
    if plan.get("status") != "ok":
        return _error_payload([_stage_error("candidate_verification_plan", plan)], artifacts, input_count)

    gate = _gate().build_gate(plan)
    artifacts["report_readiness_gate"] = gate
    if gate.get("status") != "ok":
        return _error_payload([_stage_error("report_readiness_gate", gate)], artifacts, input_count)

    return {
        "schema_version": WORKFLOW_SCHEMA_VERSION,
        "status": "ok",
        "source_schema_versions": SOURCE_SCHEMA_VERSIONS,
        "summary": _summary(artifacts, input_count),
        "artifacts": artifacts,
        "errors": [],
    }


def _parse_args(argv: list[str]) -> tuple[list[WorkflowError], str | None, list[str]]:
    errors: list[WorkflowError] = []
    repo_root: str | None = None
    inputs: list[str] = []
    index = 0
    while index < len(argv):
        arg = argv[index]
        name = arg.split("=", 1)[0]
        if name in LIVE_TARGET_FLAGS:
            errors.append(
                WorkflowError(
                    "LIVE_TARGET_FLAG_NOT_ALLOWED",
                    f"argv[{index}]",
                    "live target flags are not accepted by the offline workflow fixture builder",
                )
            )
            index += 1
            continue
        if arg == "--json":
            index += 1
            continue
        if arg in ("--repo-root", "--input"):
            if index + 1 >= len(argv) or argv[index + 1].startswith("--"):
                errors.append(
                    WorkflowError(
                        "ARGUMENT_VALUE_MISSING",
                        f"argv[{index}]",
                        f"{arg} requires a following value",
                    )
                )
                index += 1
                continue
            value = argv[index + 1]
            if arg == "--repo-root":
                repo_root = value
            else:
                inputs.append(value)
            index += 2
            continue
        if arg.startswith("--"):
            errors.append(
                WorkflowError(
                    "ARGUMENT_NOT_ALLOWED",
                    f"argv[{index}]",
                    "this fixture builder accepts only --repo-root, --input, and --json",
                )
            )
        else:
            errors.append(
                WorkflowError(
                    "ARGUMENT_NOT_ALLOWED",
                    f"argv[{index}]",
                    "positional arguments are not accepted by the offline workflow fixture builder",
                )
            )
        index += 1

    if repo_root is None:
        errors.append(
            WorkflowError("REQUIRED_ARGUMENT_MISSING", "argv", "--repo-root is required")
        )
    if not inputs:
        errors.append(
            WorkflowError("REQUIRED_ARGUMENT_MISSING", "argv", "at least one --input is required")
        )
    return errors, repo_root, inputs


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    args = list(sys.argv[1:] if argv is None else argv)
    errors, repo_root, inputs = _parse_args(args)
    if errors:
        payload = _error_payload(errors)
        _compact_emit(payload)
        return 2, payload
    payload = build_workflow_fixture(repo_root or "", inputs)
    _compact_emit(payload)
    return (0 if payload["status"] == "ok" else 1), payload


if __name__ == "__main__":
    raise SystemExit(main()[0])
