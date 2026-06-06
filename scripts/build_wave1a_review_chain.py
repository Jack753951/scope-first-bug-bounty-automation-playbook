#!/usr/bin/env python3
"""Offline Wave 1A candidate-review chain builder.

This helper starts from the committed Wave 1A metadata observation fixture
contract, reuses ``build_wave1a_candidate_review_fixture.py`` to create
``finding/1.0`` candidate fixtures and a ``candidate_review_packet/0.1-trial``,
then runs the existing offline gap, verification-plan, and report-readiness gate
consumers in memory.

Boundary: no target interaction, no network I/O, no subprocess execution, no
file writes by default, no report drafting/submission, and no promotion to
confirmed/verified/reportable states.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "wave1a_review_chain/0.1-trial"
SOURCE_SCHEMA_VERSIONS = [
    "wave1a_candidate_review_bridge/0.1-trial",
    "candidate_review_packet/0.1-trial",
    "candidate_review_gap_report/0.1-trial",
    "candidate_verification_plan/0.1-trial",
    "report_readiness_gate/0.1-trial",
]
LIVE_TARGET_FLAGS = frozenset({"--target", "--url", "--host", "--scope", "--live"})
FORBIDDEN_PROMOTIONS = {"confirmed", "verified", "reportable", "accepted", "ready_for_submission"}


@dataclass(frozen=True)
class ChainError:
    code: str
    path: str
    message: str
    stage: str | None = None

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


def _bridge() -> Any:
    return _load_script_module("build_wave1a_candidate_review_fixture.py", "_wave1a_review_chain_bridge")


def _gap_consumer() -> Any:
    return _load_script_module("review_candidate_packet_gaps.py", "_wave1a_review_chain_gap_consumer")


def _planner() -> Any:
    return _load_script_module("build_candidate_verification_plan.py", "_wave1a_review_chain_verification_planner")


def _gate() -> Any:
    return _load_script_module("build_report_readiness_gate.py", "_wave1a_review_chain_report_readiness_gate")


def _safety() -> dict[str, bool]:
    return {
        "network_io": False,
        "subprocess_execution": False,
        "target_touching": False,
        "output_file_write": False,
        "promotes_findings": False,
        "report_drafting": False,
        "report_submission": False,
    }


def _empty_summary() -> dict[str, int]:
    return {
        "candidate_seed_count": 0,
        "candidate_count": 0,
        "gap_finding_count": 0,
        "verification_plan_count": 0,
        "gate_result_count": 0,
        "blocked_count": 0,
        "needs_manual_review_count": 0,
        "error_count": 0,
    }


def _stage_error(stage: str, payload: Any) -> ChainError:
    stage_errors = []
    if isinstance(payload, dict) and isinstance(payload.get("errors"), list):
        stage_errors = payload["errors"]
    if stage_errors:
        first = stage_errors[0]
        if isinstance(first, dict):
            code = first.get("code") if isinstance(first.get("code"), str) else "UNKNOWN_STAGE_ERROR"
            path = first.get("path") if isinstance(first.get("path"), str) else stage
            message = first.get("message") if isinstance(first.get("message"), str) else "stage failed"
            return ChainError("REVIEW_CHAIN_STAGE_FAILED", path, f"{code}: {message}", stage=stage)
    return ChainError("REVIEW_CHAIN_STAGE_FAILED", stage, "review-chain stage failed closed", stage=stage)


def _error_payload(errors: list[ChainError], artifacts: dict[str, Any] | None = None) -> dict[str, Any]:
    summary = _empty_summary()
    summary["error_count"] = len(errors)
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "error",
        "source_schema_versions": SOURCE_SCHEMA_VERSIONS,
        "summary": summary,
        "artifacts": artifacts or {},
        "errors": [error.as_dict() for error in errors],
        "safety": _safety(),
    }


def _summary(bridge_payload: dict[str, Any], artifacts: dict[str, Any]) -> dict[str, int]:
    packet = artifacts["candidate_review_packet"]
    gap_report = artifacts["candidate_review_gap_report"]
    plan = artifacts["candidate_verification_plan"]
    gate = artifacts["report_readiness_gate"]
    bridge_summary = bridge_payload.get("summary") if isinstance(bridge_payload.get("summary"), dict) else {}
    return {
        "candidate_seed_count": int(bridge_summary.get("candidate_seed_count", 0)),
        "candidate_count": int(packet["summary"].get("candidate_count", 0)),
        "gap_finding_count": int(gap_report["summary"].get("finding_count", 0)),
        "verification_plan_count": int(plan["summary"].get("finding_count", 0)),
        "gate_result_count": int(gate["summary"].get("finding_count", 0)),
        "blocked_count": int(gate["summary"].get("blocked_count", 0)),
        "needs_manual_review_count": int(gate["summary"].get("needs_manual_review_count", 0)),
        "error_count": 0,
    }


def _check_no_promotional_values(payload: Any) -> None:
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
        elif isinstance(value, str) and value.lower() in FORBIDDEN_PROMOTIONS:
            raise ValueError(f"forbidden promotional value: {value}")

    walk(payload)


def build_review_chain(repo_root: str | Path, input_path: str, *, run_id: str = "wave1a-review-chain") -> dict[str, Any]:
    """Return an offline Wave 1A review-chain artifact from a committed fixture path."""
    artifacts: dict[str, Any] = {}

    bridge_payload = _bridge().build_bridge(repo_root, input_path, run_id=run_id)
    artifacts["candidate_review_bridge"] = bridge_payload
    if not isinstance(bridge_payload, dict) or bridge_payload.get("status") != "ok":
        return _error_payload([_stage_error("candidate_review_bridge", bridge_payload)], artifacts)

    packet = bridge_payload.get("candidate_review_packet")
    artifacts["candidate_review_packet"] = packet
    if not isinstance(packet, dict) or packet.get("status") != "ok":
        return _error_payload([_stage_error("candidate_review_packet", packet)], artifacts)

    gap_report = _gap_consumer().review_packet(packet)
    artifacts["candidate_review_gap_report"] = gap_report
    if gap_report.get("status") != "ok":
        return _error_payload([_stage_error("candidate_review_gap_report", gap_report)], artifacts)

    plan = _planner().build_plan(gap_report)
    artifacts["candidate_verification_plan"] = plan
    if plan.get("status") != "ok":
        return _error_payload([_stage_error("candidate_verification_plan", plan)], artifacts)

    gate = _gate().build_gate(plan)
    artifacts["report_readiness_gate"] = gate
    if gate.get("status") != "ok":
        return _error_payload([_stage_error("report_readiness_gate", gate)], artifacts)

    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "ok",
        "source_schema_versions": SOURCE_SCHEMA_VERSIONS,
        "input_path": input_path,
        "summary": _summary(bridge_payload, artifacts),
        "artifacts": artifacts,
        "errors": [],
        "safety": _safety(),
    }
    _check_no_promotional_values(payload)
    return payload


def _live_flag_errors(argv: list[str]) -> list[ChainError]:
    errors: list[ChainError] = []
    for index, arg in enumerate(argv):
        name = arg.split("=", 1)[0]
        if name in LIVE_TARGET_FLAGS:
            errors.append(
                ChainError(
                    "LIVE_TARGET_FLAG_NOT_ALLOWED",
                    f"argv[{index}]",
                    "live target flags are not accepted by the offline Wave 1A review-chain builder",
                )
            )
    return errors


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    live_errors = _live_flag_errors(argv)
    if live_errors:
        print(json.dumps(_error_payload(live_errors), indent=2, sort_keys=True))
        return 2

    parser = argparse.ArgumentParser(description="Build an offline Wave 1A review-chain artifact")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--run-id", default="wave1a-review-chain")
    parser.add_argument("--json", action="store_true", help="Accepted for compatibility; output is always JSON")
    args = parser.parse_args(argv)

    payload = build_review_chain(Path(args.repo_root), args.input, run_id=args.run_id)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("status") == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
