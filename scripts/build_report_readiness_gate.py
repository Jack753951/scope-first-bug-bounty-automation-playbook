#!/usr/bin/env python3
# TRIAL ONLY — no schema promotion, no drafting, stdin/stdout gate consumer only.
"""Offline report readiness gate consumer (P2.22, trial-only).

Reads one ``candidate_verification_plan/0.1-trial`` JSON document from stdin
and emits one deterministic ``report_readiness_gate/0.1-trial`` JSON document
to stdout for human review.

This consumer is a readiness/gating classifier only. It does not draft any
report text, does not confirm any item, and never promotes any item above
``blocked`` / ``needs_manual_review``. It performs no file reads, no file
writes, no target interaction, no network calls, no process launches, and no
runtime wiring.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from typing import Any

SOURCE_SCHEMA_VERSION = "candidate_verification_plan/0.1-trial"
GATE_SCHEMA_VERSION = "report_readiness_gate/0.1-trial"

LIVE_TARGET_FLAGS = frozenset({"--target", "--url", "--host", "--scope", "--live"})

ALLOWED_PLAN_STATES = frozenset({"blocked", "needs_manual_review"})

GATE_ACTION_ORDER = (
    "GATE_COLLECT_EVIDENCE",
    "GATE_COMPLETE_MANUAL_CHECKS",
    "GATE_ADD_SCOPE_REVIEW",
    "GATE_ADD_REMEDIATION_GUIDANCE",
    "GATE_ADD_VERIFICATION_GUIDANCE",
    "GATE_ADD_HUMAN_REVIEW_DECISION",
    "GATE_KEEP_OUT_OF_REPORT",
)
GATE_ACTION_INDEX = {action: index for index, action in enumerate(GATE_ACTION_ORDER)}

BLOCK_REASON_ORDER = (
    "BLOCK_MISSING_EVIDENCE",
    "BLOCK_LOW_CONFIDENCE",
    "BLOCK_INFO_SEVERITY",
    "BLOCK_MANUAL_VERIFICATION_REQUIRED",
    "BLOCK_SCANNER_OUTPUT_ONLY",
    "BLOCK_MISSING_REMEDIATION",
    "BLOCK_MISSING_VERIFICATION_GUIDANCE",
    "BLOCK_MISSING_SCOPE_REVIEW_QUESTION",
)
BLOCK_REASON_INDEX = {reason: index for index, reason in enumerate(BLOCK_REASON_ORDER)}

CHECK_TO_ACTION = {
    "CHECK_MISSING_EVIDENCE": "GATE_COLLECT_EVIDENCE",
    "CHECK_LOW_CONFIDENCE": "GATE_COMPLETE_MANUAL_CHECKS",
    "CHECK_INFO_SEVERITY_RATIONALE": "GATE_KEEP_OUT_OF_REPORT",
    "CHECK_MANUAL_VERIFICATION_NOTES": "GATE_COMPLETE_MANUAL_CHECKS",
    "CHECK_NON_SCANNER_CORROBORATION": "GATE_COMPLETE_MANUAL_CHECKS",
    "CHECK_HUMAN_REMEDIATION_GUIDANCE": "GATE_ADD_REMEDIATION_GUIDANCE",
    "CHECK_SAFE_MANUAL_CHECKLIST": "GATE_ADD_VERIFICATION_GUIDANCE",
    "CHECK_SCOPE_REVIEW_QUESTION": "GATE_ADD_SCOPE_REVIEW",
    "CHECK_REVIEWER_DECISION": "GATE_ADD_HUMAN_REVIEW_DECISION",
}

CHECK_TO_BLOCK_REASON = {
    "CHECK_MISSING_EVIDENCE": "BLOCK_MISSING_EVIDENCE",
    "CHECK_LOW_CONFIDENCE": "BLOCK_LOW_CONFIDENCE",
    "CHECK_INFO_SEVERITY_RATIONALE": "BLOCK_INFO_SEVERITY",
    "CHECK_MANUAL_VERIFICATION_NOTES": "BLOCK_MANUAL_VERIFICATION_REQUIRED",
    "CHECK_NON_SCANNER_CORROBORATION": "BLOCK_SCANNER_OUTPUT_ONLY",
    "CHECK_HUMAN_REMEDIATION_GUIDANCE": "BLOCK_MISSING_REMEDIATION",
    "CHECK_SAFE_MANUAL_CHECKLIST": "BLOCK_MISSING_VERIFICATION_GUIDANCE",
    "CHECK_SCOPE_REVIEW_QUESTION": "BLOCK_MISSING_SCOPE_REVIEW_QUESTION",
}


class GateError:
    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


def _empty_summary() -> dict[str, Any]:
    return {
        "finding_count": 0,
        "blocked_count": 0,
        "needs_manual_review_count": 0,
        "gate_action_counts": {},
    }


def _error_payload(errors: list[GateError]) -> dict[str, Any]:
    return {
        "schema_version": GATE_SCHEMA_VERSION,
        "status": "error",
        "source_schema_version": None,
        "summary": _empty_summary(),
        "gate_results": [],
        "errors": [error.as_dict() for error in errors],
    }


def _compact_emit(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")


def _validate_plan(plan: Any) -> list[GateError]:
    errors: list[GateError] = []
    if not isinstance(plan, dict):
        return [GateError("PLAN_NOT_OBJECT", "plan", "verification plan must be a JSON object")]
    if plan.get("schema_version") != SOURCE_SCHEMA_VERSION:
        errors.append(
            GateError(
                "PLAN_SCHEMA_UNSUPPORTED",
                "schema_version",
                "plan schema_version must be candidate_verification_plan/0.1-trial",
            )
        )
    if plan.get("status") != "ok":
        errors.append(GateError("PLAN_STATUS_NOT_OK", "status", "plan status must be ok"))
    source_errors = plan.get("errors")
    if source_errors not in ([], None):
        errors.append(
            GateError("PLAN_ERRORS_PRESENT", "errors", "plan errors must be empty")
        )

    summary = plan.get("summary")
    if not isinstance(summary, dict):
        errors.append(GateError("SUMMARY_NOT_OBJECT", "summary", "summary must be an object"))
        summary = {}

    verification_plans = plan.get("verification_plans")
    if not isinstance(verification_plans, list):
        errors.append(
            GateError(
                "VERIFICATION_PLANS_NOT_LIST",
                "verification_plans",
                "verification_plans must be a list",
            )
        )
        return errors

    recomputed_blocked = 0
    recomputed_manual = 0
    for index, entry in enumerate(verification_plans):
        path = f"verification_plans[{index}]"
        if not isinstance(entry, dict):
            errors.append(
                GateError(
                    "VERIFICATION_PLAN_NOT_OBJECT",
                    path,
                    "verification plan entry must be an object",
                )
            )
            continue
        for field in ("finding_id", "target_value", "module_id"):
            if not isinstance(entry.get(field), str):
                errors.append(
                    GateError(
                        "VERIFICATION_PLAN_FIELD_INVALID",
                        f"{path}.{field}",
                        f"{field} must be a string",
                    )
                )
        plan_state = entry.get("plan_state")
        if plan_state not in ALLOWED_PLAN_STATES:
            errors.append(
                GateError(
                    "PLAN_STATE_UNSUPPORTED",
                    f"{path}.plan_state",
                    "plan_state must be blocked or needs_manual_review",
                )
            )
        else:
            if plan_state == "blocked":
                recomputed_blocked += 1
            else:
                recomputed_manual += 1
        check_items = entry.get("check_items")
        if not isinstance(check_items, list):
            errors.append(
                GateError(
                    "CHECK_ITEMS_NOT_LIST",
                    f"{path}.check_items",
                    "check_items must be a list",
                )
            )
            continue
        seen_check_codes: set[str] = set()
        for code_index, item in enumerate(check_items):
            item_path = f"{path}.check_items[{code_index}]"
            if not isinstance(item, dict):
                errors.append(
                    GateError(
                        "CHECK_ITEM_NOT_OBJECT",
                        item_path,
                        "check item must be an object",
                    )
                )
                continue
            code = item.get("code")
            if code not in CHECK_TO_ACTION:
                errors.append(
                    GateError(
                        "CHECK_ITEM_CODE_UNSUPPORTED",
                        f"{item_path}.code",
                        "check item code is not part of the P2.21 trial vocabulary",
                    )
                )
                continue
            if code in seen_check_codes:
                errors.append(
                    GateError(
                        "CHECK_ITEM_CODE_DUPLICATE",
                        f"{item_path}.code",
                        "check item codes must not repeat within one verification plan",
                    )
                )
                continue
            seen_check_codes.add(code)

    if isinstance(summary, dict):
        for key in ("finding_count", "blocked_count", "needs_manual_review_count"):
            value = summary.get(key)
            if type(value) is not int or value < 0:
                errors.append(
                    GateError(
                        "SUMMARY_COUNT_INVALID",
                        f"summary.{key}",
                        "summary counts must be non-negative integers",
                    )
                )

        if (
            type(summary.get("finding_count")) is int
            and type(summary.get("blocked_count")) is int
            and type(summary.get("needs_manual_review_count")) is int
        ):
            if summary["finding_count"] != len(verification_plans):
                errors.append(
                    GateError(
                        "SUMMARY_FINDING_COUNT_MISMATCH",
                        "summary.finding_count",
                        "summary finding_count must match verification_plans length",
                    )
                )
            if summary["blocked_count"] != recomputed_blocked:
                errors.append(
                    GateError(
                        "SUMMARY_BLOCKED_COUNT_MISMATCH",
                        "summary.blocked_count",
                        "summary blocked_count must match verification_plans plan_state values",
                    )
                )
            if summary["needs_manual_review_count"] != recomputed_manual:
                errors.append(
                    GateError(
                        "SUMMARY_NEEDS_MANUAL_REVIEW_COUNT_MISMATCH",
                        "summary.needs_manual_review_count",
                        "summary needs_manual_review_count must match verification_plans plan_state values",
                    )
                )

    return errors


def _gate_actions_for(check_codes: list[str]) -> list[str]:
    seen: set[str] = set()
    for code in check_codes:
        action = CHECK_TO_ACTION[code]
        seen.add(action)
    return sorted(seen, key=lambda action: GATE_ACTION_INDEX[action])


def _block_reasons_for(check_codes: list[str]) -> list[str]:
    seen: set[str] = set()
    for code in check_codes:
        reason = CHECK_TO_BLOCK_REASON.get(code)
        if reason is not None:
            seen.add(reason)
    return sorted(seen, key=lambda reason: BLOCK_REASON_INDEX[reason])


def _gate_result(entry: dict[str, Any]) -> dict[str, Any]:
    check_codes = [item["code"] for item in entry["check_items"]]
    plan_state = entry["plan_state"]
    actions = _gate_actions_for(check_codes)
    if plan_state == "blocked":
        block_reasons = _block_reasons_for(check_codes)
        gate_state = "blocked"
    else:
        block_reasons = []
        gate_state = "needs_manual_review"
    return {
        "finding_id": entry["finding_id"],
        "target_value": entry["target_value"],
        "module_id": entry["module_id"],
        "gate_state": gate_state,
        "gate_actions": actions,
        "block_reasons": block_reasons,
    }


def _build_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    blocked = 0
    manual = 0
    for result in results:
        counts.update(result["gate_actions"])
        if result["gate_state"] == "blocked":
            blocked += 1
        elif result["gate_state"] == "needs_manual_review":
            manual += 1
    return {
        "finding_count": len(results),
        "blocked_count": blocked,
        "needs_manual_review_count": manual,
        "gate_action_counts": {
            action: counts[action] for action in GATE_ACTION_ORDER if counts[action]
        },
    }


def build_gate(plan: Any) -> dict[str, Any]:
    errors = _validate_plan(plan)
    if errors:
        return _error_payload(errors)
    results = [_gate_result(entry) for entry in plan["verification_plans"]]
    results.sort(key=lambda result: (result["finding_id"], result["target_value"], result["module_id"]))
    return {
        "schema_version": GATE_SCHEMA_VERSION,
        "status": "ok",
        "source_schema_version": SOURCE_SCHEMA_VERSION,
        "summary": _build_summary(results),
        "gate_results": results,
        "errors": [],
    }


def _argv_errors(argv: list[str]) -> list[GateError]:
    errors: list[GateError] = []
    for index, arg in enumerate(argv):
        name = arg.split("=", 1)[0]
        if name in LIVE_TARGET_FLAGS:
            errors.append(
                GateError(
                    "LIVE_TARGET_FLAG_NOT_ALLOWED",
                    f"argv[{index}]",
                    "live target flags are not allowed by the offline gate consumer",
                )
            )
        else:
            errors.append(
                GateError(
                    "ARGUMENT_NOT_ALLOWED",
                    f"argv[{index}]",
                    "this consumer accepts no command-line arguments",
                )
            )
    return errors


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    args = list(sys.argv[1:] if argv is None else argv)
    errors = _argv_errors(args)
    if errors:
        payload = _error_payload(errors)
        _compact_emit(payload)
        return 2, payload
    raw = sys.stdin.read()
    try:
        plan = json.loads(raw)
    except json.JSONDecodeError:
        payload = _error_payload(
            [GateError("INPUT_JSON_INVALID", "stdin", "stdin must contain one JSON document")]
        )
        _compact_emit(payload)
        return 2, payload
    payload = build_gate(plan)
    _compact_emit(payload)
    return (0 if payload["status"] == "ok" else 2), payload


if __name__ == "__main__":
    raise SystemExit(main()[0])
