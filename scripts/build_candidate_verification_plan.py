#!/usr/bin/env python3
# TRIAL ONLY — no schema promotion, no drafting, stdin/stdout checklist consumer only.
"""Offline candidate verification checklist consumer (P2.21, trial-only).

Reads one candidate review gap report JSON document from stdin and emits one
deterministic human-checklist JSON document to stdout. It performs no file
reads, no file writes, no target interaction, no network calls, no process
launches, and no runtime wiring.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from typing import Any

SOURCE_SCHEMA_VERSION = "candidate_review_gap_report/0.1-trial"
PLAN_SCHEMA_VERSION = "candidate_verification_plan/0.1-trial"

LIVE_TARGET_FLAGS = frozenset({"--target", "--url", "--host", "--scope", "--live"})

GAP_CODE_ORDER = (
    "MISSING_EVIDENCE",
    "LOW_CONFIDENCE",
    "INFO_SEVERITY_REPORT_BLOCKED",
    "MANUAL_VERIFICATION_REQUIRED",
    "SCANNER_OUTPUT_ONLY",
    "MISSING_REMEDIATION",
    "MISSING_VERIFICATION_GUIDANCE",
    "MISSING_SCOPE_REVIEW_QUESTION",
)
GAP_CODE_INDEX = {code: index for index, code in enumerate(GAP_CODE_ORDER)}

STATE_MAP = {
    "not_ready": "blocked",
    "reviewer_decision_required": "needs_manual_review",
}

CHECKS = {
    "MISSING_EVIDENCE": {
        "code": "CHECK_MISSING_EVIDENCE",
        "action_kind": "collect_redacted_evidence",
        "prompt": "Collect or reference redacted evidence through an authorized manual step before escalation.",
    },
    "LOW_CONFIDENCE": {
        "code": "CHECK_LOW_CONFIDENCE",
        "action_kind": "corroborate_observation",
        "prompt": "Corroborate the observation manually or mark the candidate as insufficiently supported.",
    },
    "INFO_SEVERITY_REPORT_BLOCKED": {
        "code": "CHECK_INFO_SEVERITY_RATIONALE",
        "action_kind": "severity_rationale",
        "prompt": "Document why this informational item matters, or keep it out of downstream escalation.",
    },
    "MANUAL_VERIFICATION_REQUIRED": {
        "code": "CHECK_MANUAL_VERIFICATION_NOTES",
        "action_kind": "manual_verification_notes",
        "prompt": "Record human verification notes from an authorized review before any downstream action.",
    },
    "SCANNER_OUTPUT_ONLY": {
        "code": "CHECK_NON_SCANNER_CORROBORATION",
        "action_kind": "non_scanner_corroboration",
        "prompt": "Add non-scanner corroboration or explain why the scanner-only signal is insufficient.",
    },
    "MISSING_REMEDIATION": {
        "code": "CHECK_HUMAN_REMEDIATION_GUIDANCE",
        "action_kind": "human_remediation_guidance",
        "prompt": "Add human-authored remediation guidance without generating submission prose.",
    },
    "MISSING_VERIFICATION_GUIDANCE": {
        "code": "CHECK_SAFE_MANUAL_CHECKLIST",
        "action_kind": "safe_manual_checklist",
        "prompt": "Add a safe manual checklist that stays within authorization and avoids noisy testing.",
    },
    "MISSING_SCOPE_REVIEW_QUESTION": {
        "code": "CHECK_SCOPE_REVIEW_QUESTION",
        "action_kind": "scope_review_question",
        "prompt": "Add an explicit authorized-scope review question before any next action.",
    },
}

REVIEWER_DECISION_CHECK = {
    "code": "CHECK_REVIEWER_DECISION",
    "source_gap_code": None,
    "action_kind": "human_review_decision",
    "prompt": "Record an explicit human review decision before any downstream action.",
}


class PlanError:
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
        "check_item_count": 0,
        "source_gap_code_counts": {},
    }


def _error_payload(errors: list[PlanError]) -> dict[str, Any]:
    return {
        "schema_version": PLAN_SCHEMA_VERSION,
        "status": "error",
        "source_schema_version": None,
        "summary": _empty_summary(),
        "verification_plans": [],
        "errors": [error.as_dict() for error in errors],
    }


def _compact_emit(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")


def _check_item_for_gap(code: str) -> dict[str, Any]:
    spec = CHECKS[code]
    return {
        "code": spec["code"],
        "source_gap_code": code,
        "action_kind": spec["action_kind"],
        "prompt": spec["prompt"],
    }


def _validate_gap_report(report: Any) -> list[PlanError]:
    errors: list[PlanError] = []
    if not isinstance(report, dict):
        return [PlanError("GAP_REPORT_NOT_OBJECT", "report", "gap report must be a JSON object")]
    if report.get("schema_version") != SOURCE_SCHEMA_VERSION:
        errors.append(
            PlanError(
                "GAP_REPORT_SCHEMA_UNSUPPORTED",
                "schema_version",
                "gap report schema_version must be candidate_review_gap_report/0.1-trial",
            )
        )
    if report.get("status") != "ok":
        errors.append(PlanError("GAP_REPORT_STATUS_NOT_OK", "status", "gap report status must be ok"))
    source_errors = report.get("errors")
    if source_errors not in ([], None):
        errors.append(PlanError("GAP_REPORT_ERRORS_PRESENT", "errors", "gap report errors must be empty"))

    summary = report.get("summary")
    if not isinstance(summary, dict):
        errors.append(PlanError("SUMMARY_NOT_OBJECT", "summary", "summary must be an object"))
        summary_counts: dict[str, Any] = {}
    else:
        summary_counts = summary.get("gap_code_counts")
        if not isinstance(summary_counts, dict):
            errors.append(
                PlanError(
                    "GAP_CODE_COUNTS_NOT_OBJECT",
                    "summary.gap_code_counts",
                    "summary.gap_code_counts must be an object",
                )
            )
            summary_counts = {}

    finding_gaps = report.get("finding_gaps")
    if not isinstance(finding_gaps, list):
        errors.append(PlanError("FINDING_GAPS_NOT_LIST", "finding_gaps", "finding_gaps must be a list"))
        return errors

    recomputed: Counter[str] = Counter()
    for index, entry in enumerate(finding_gaps):
        path = f"finding_gaps[{index}]"
        if not isinstance(entry, dict):
            errors.append(PlanError("FINDING_GAP_NOT_OBJECT", path, "finding gap entry must be an object"))
            continue
        for field in ("finding_id", "target_value", "module_id"):
            if not isinstance(entry.get(field), str):
                errors.append(PlanError("FINDING_GAP_FIELD_INVALID", f"{path}.{field}", f"{field} must be a string"))
        review_state = entry.get("review_state")
        if review_state not in STATE_MAP:
            errors.append(
                PlanError(
                    "REVIEW_STATE_UNSUPPORTED",
                    f"{path}.review_state",
                    "review_state must be not_ready or reviewer_decision_required",
                )
            )
        gap_codes = entry.get("gap_codes")
        if not isinstance(gap_codes, list):
            errors.append(PlanError("GAP_CODES_NOT_LIST", f"{path}.gap_codes", "gap_codes must be a list"))
            continue
        if review_state == "not_ready" and not gap_codes:
            errors.append(
                PlanError(
                    "BLOCKED_PLAN_WITHOUT_GAPS",
                    f"{path}.gap_codes",
                    "blocked plans must have at least one source gap code",
                )
            )
        seen_gap_codes: set[str] = set()
        for code_index, code in enumerate(gap_codes):
            if code not in GAP_CODE_INDEX:
                errors.append(
                    PlanError(
                        "GAP_CODE_UNSUPPORTED",
                        f"{path}.gap_codes[{code_index}]",
                        "gap code is not part of the P2.20 trial vocabulary",
                    )
                )
                continue
            if code in seen_gap_codes:
                errors.append(
                    PlanError(
                        "GAP_CODE_DUPLICATE",
                        f"{path}.gap_codes[{code_index}]",
                        "gap codes must not repeat within one finding gap entry",
                    )
                )
                continue
            seen_gap_codes.add(code)
            recomputed[code] += 1

    for key, value in summary_counts.items():
        if key not in GAP_CODE_INDEX:
            errors.append(
                PlanError(
                    "GAP_CODE_COUNT_UNSUPPORTED",
                    f"summary.gap_code_counts.{key}",
                    "summary gap code count uses an unknown code",
                )
            )
        if type(value) is not int or value < 0:
            errors.append(
                PlanError(
                    "GAP_CODE_COUNT_INVALID",
                    f"summary.gap_code_counts.{key}",
                    "summary gap code counts must be non-negative integers",
                )
            )

    if isinstance(summary_counts, dict) and all(
        type(value) is int and value >= 0 and key in GAP_CODE_INDEX
        for key, value in summary_counts.items()
    ):
        ordered_recomputed = {code: recomputed[code] for code in GAP_CODE_ORDER if recomputed[code]}
        if summary_counts != ordered_recomputed:
            errors.append(
                PlanError(
                    "GAP_CODE_COUNTS_MISMATCH",
                    "summary.gap_code_counts",
                    "summary gap code counts must match finding_gaps[].gap_codes",
                )
            )

    return errors


def _plan_entry(entry: dict[str, Any]) -> dict[str, Any]:
    sorted_gap_codes = sorted(entry["gap_codes"], key=lambda code: GAP_CODE_INDEX[code])
    check_items = [_check_item_for_gap(code) for code in sorted_gap_codes]
    plan_state = STATE_MAP[entry["review_state"]]
    if plan_state == "needs_manual_review" and not check_items:
        check_items.append(dict(REVIEWER_DECISION_CHECK))
    return {
        "finding_id": entry["finding_id"],
        "target_value": entry["target_value"],
        "module_id": entry["module_id"],
        "plan_state": plan_state,
        "check_items": check_items,
    }


def _build_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    check_item_count = 0
    for entry in entries:
        check_item_count += len(entry["check_items"])
        for item in entry["check_items"]:
            source = item.get("source_gap_code")
            if isinstance(source, str):
                counts[source] += 1
    return {
        "finding_count": len(entries),
        "blocked_count": sum(1 for entry in entries if entry["plan_state"] == "blocked"),
        "needs_manual_review_count": sum(
            1 for entry in entries if entry["plan_state"] == "needs_manual_review"
        ),
        "check_item_count": check_item_count,
        "source_gap_code_counts": {code: counts[code] for code in GAP_CODE_ORDER if counts[code]},
    }


def build_plan(report: Any) -> dict[str, Any]:
    errors = _validate_gap_report(report)
    if errors:
        return _error_payload(errors)
    entries = [_plan_entry(entry) for entry in report["finding_gaps"]]
    entries.sort(key=lambda entry: (entry["finding_id"], entry["target_value"], entry["module_id"]))
    return {
        "schema_version": PLAN_SCHEMA_VERSION,
        "status": "ok",
        "source_schema_version": SOURCE_SCHEMA_VERSION,
        "summary": _build_summary(entries),
        "verification_plans": entries,
        "errors": [],
    }


def _argv_errors(argv: list[str]) -> list[PlanError]:
    errors: list[PlanError] = []
    for index, arg in enumerate(argv):
        name = arg.split("=", 1)[0]
        if name in LIVE_TARGET_FLAGS:
            errors.append(
                PlanError(
                    "LIVE_TARGET_FLAG_NOT_ALLOWED",
                    f"argv[{index}]",
                    "live target flags are not accepted by the offline checklist consumer",
                )
            )
        else:
            errors.append(
                PlanError(
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
        report = json.loads(raw)
    except json.JSONDecodeError:
        payload = _error_payload(
            [PlanError("INPUT_JSON_INVALID", "stdin", "stdin must contain one JSON document")]
        )
        _compact_emit(payload)
        return 2, payload
    payload = build_plan(report)
    _compact_emit(payload)
    return (0 if payload["status"] == "ok" else 2), payload


if __name__ == "__main__":
    raise SystemExit(main()[0])
