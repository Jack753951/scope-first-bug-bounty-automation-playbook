#!/usr/bin/env python3
# TRIAL ONLY — no schema promotion, no drafting, stdin/stdout gap consumer only.
"""Offline candidate review packet gap consumer (P2.20, trial-only).

Reads one candidate review packet JSON document from stdin and emits one
deterministic triage gap/action JSON document to stdout. It performs no file
reads, no file writes, no target interaction, no network calls, no process
launches, and no runtime wiring.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from typing import Any

SOURCE_SCHEMA_VERSION = "candidate_review_packet/0.1-trial"
GAP_SCHEMA_VERSION = "candidate_review_gap_report/0.1-trial"

FORBIDDEN_PACKET_STATUSES = frozenset(
    "".join(parts)
    for parts in (
        ("confirm", "ed"),
        ("verifi", "ed"),
        ("accept", "ed"),
    )
)

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


class GapError:
    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


def _error_payload(errors: list[GapError]) -> dict[str, Any]:
    return {
        "schema_version": GAP_SCHEMA_VERSION,
        "status": "error",
        "source_schema_version": None,
        "summary": {
            "finding_count": 0,
            "blocked_count": 0,
            "not_ready_count": 0,
            "reviewer_decision_required_count": 0,
            "gap_code_counts": {},
        },
        "finding_gaps": [],
        "errors": [error.as_dict() for error in errors],
    }


def _compact_emit(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")


def _review_question_keys(finding: dict[str, Any]) -> set[str]:
    questions = finding.get("review_questions")
    if not isinstance(questions, list):
        return set()
    keys: set[str] = set()
    for question in questions:
        if isinstance(question, dict) and isinstance(question.get("key"), str):
            keys.add(question["key"])
    return keys


def _text_missing(value: Any) -> bool:
    return not isinstance(value, str) or not value.strip()


def _gap_codes_for_finding(finding: dict[str, Any]) -> list[str]:
    codes: list[str] = []
    evidence_count = finding.get("evidence_ref_count")
    if not isinstance(evidence_count, int) or evidence_count <= 0:
        codes.append("MISSING_EVIDENCE")
    if finding.get("confidence") == "low":
        codes.append("LOW_CONFIDENCE")
    if finding.get("severity_hint") == "info":
        codes.append("INFO_SEVERITY_REPORT_BLOCKED")
    if finding.get("manual_verification_required") is True:
        codes.append("MANUAL_VERIFICATION_REQUIRED")
    if finding.get("scanner_output_only") is True:
        codes.append("SCANNER_OUTPUT_ONLY")
    if _text_missing(finding.get("remediation")):
        codes.append("MISSING_REMEDIATION")
    if _text_missing(finding.get("verification_guidance")):
        codes.append("MISSING_VERIFICATION_GUIDANCE")
    if "scope_in_authorized_scope" not in _review_question_keys(finding):
        codes.append("MISSING_SCOPE_REVIEW_QUESTION")
    return sorted(codes, key=lambda code: GAP_CODE_INDEX.get(code, 999))


def _review_state(finding: dict[str, Any], gap_codes: list[str]) -> str:
    blocking_codes = {
        "MISSING_EVIDENCE",
        "LOW_CONFIDENCE",
        "INFO_SEVERITY_REPORT_BLOCKED",
        "MISSING_REMEDIATION",
        "MISSING_VERIFICATION_GUIDANCE",
        "MISSING_SCOPE_REVIEW_QUESTION",
    }
    if finding.get("report_readiness") == "reviewer_decision_required" and not any(
        code in blocking_codes for code in gap_codes
    ):
        return "reviewer_decision_required"
    return "not_ready"


def _target_value(finding: dict[str, Any]) -> str:
    target = finding.get("target")
    if isinstance(target, dict) and isinstance(target.get("value"), str):
        return target["value"]
    return ""


def _finding_gap_entry(finding: dict[str, Any]) -> dict[str, Any]:
    codes = _gap_codes_for_finding(finding)
    target = finding.get("target") if isinstance(finding.get("target"), dict) else {}
    source = finding.get("source") if isinstance(finding.get("source"), dict) else {}
    return {
        "finding_id": finding.get("id") if isinstance(finding.get("id"), str) else "",
        "target_value": target.get("value") if isinstance(target.get("value"), str) else "",
        "module_id": source.get("module_id") if isinstance(source.get("module_id"), str) else "",
        "review_state": _review_state(finding, codes),
        "gap_codes": codes,
    }


def _validate_packet(packet: Any) -> list[GapError]:
    errors: list[GapError] = []
    if not isinstance(packet, dict):
        return [GapError("PACKET_NOT_OBJECT", "packet", "packet must be a JSON object")]
    if packet.get("schema_version") != SOURCE_SCHEMA_VERSION:
        errors.append(
            GapError(
                "PACKET_SCHEMA_UNSUPPORTED",
                "schema_version",
                "packet schema_version must be candidate_review_packet/0.1-trial",
            )
        )
    if packet.get("status") != "ok":
        errors.append(GapError("PACKET_STATUS_NOT_OK", "status", "packet status must be ok"))
    packet_errors = packet.get("errors")
    if packet_errors not in ([], None):
        errors.append(
            GapError("PACKET_ERRORS_PRESENT", "errors", "packet errors must be empty")
        )
    findings = packet.get("findings")
    if not isinstance(findings, list):
        errors.append(GapError("FINDINGS_NOT_LIST", "findings", "findings must be a list"))
        return errors
    for index, finding in enumerate(findings):
        path = f"findings[{index}]"
        if not isinstance(finding, dict):
            errors.append(GapError("FINDING_NOT_OBJECT", path, "finding must be an object"))
            continue
        status = finding.get("status")
        if isinstance(status, str) and status.lower() in FORBIDDEN_PACKET_STATUSES:
            errors.append(
                GapError(
                    "FINDING_STATUS_PROMOTED",
                    f"{path}.status",
                    "finding status is above candidate workflow boundary",
                )
            )
    return errors


def _build_summary(entries: list[dict[str, Any]]) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    for entry in entries:
        counts.update(entry["gap_codes"])
    ordered_counts = {code: counts[code] for code in GAP_CODE_ORDER if counts[code]}
    return {
        "finding_count": len(entries),
        "blocked_count": sum(1 for entry in entries if entry["gap_codes"]),
        "not_ready_count": sum(1 for entry in entries if entry["review_state"] == "not_ready"),
        "reviewer_decision_required_count": sum(
            1 for entry in entries if entry["review_state"] == "reviewer_decision_required"
        ),
        "gap_code_counts": ordered_counts,
    }


def review_packet(packet: Any) -> dict[str, Any]:
    errors = _validate_packet(packet)
    if errors:
        return _error_payload(errors)
    findings = packet.get("findings")
    entries = [_finding_gap_entry(finding) for finding in findings]
    entries.sort(key=lambda entry: (entry["finding_id"], entry["target_value"]))
    return {
        "schema_version": GAP_SCHEMA_VERSION,
        "status": "ok",
        "source_schema_version": SOURCE_SCHEMA_VERSION,
        "summary": _build_summary(entries),
        "finding_gaps": entries,
        "errors": [],
    }


def _live_flag_errors(argv: list[str]) -> list[GapError]:
    errors: list[GapError] = []
    for index, arg in enumerate(argv):
        name = arg.split("=", 1)[0]
        if name in LIVE_TARGET_FLAGS:
            errors.append(
                GapError(
                    "LIVE_TARGET_FLAG_NOT_ALLOWED",
                    f"argv[{index}]",
                    "live target flags are not accepted by the offline gap consumer",
                )
            )
        else:
            errors.append(
                GapError(
                    "ARGUMENT_NOT_ALLOWED",
                    f"argv[{index}]",
                    "this consumer accepts no command-line arguments",
                )
            )
    return errors


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    args = list(sys.argv[1:] if argv is None else argv)
    errors = _live_flag_errors(args)
    if errors:
        payload = _error_payload(errors)
        _compact_emit(payload)
        return 2, payload
    raw = sys.stdin.read()
    try:
        packet = json.loads(raw)
    except json.JSONDecodeError:
        payload = _error_payload(
            [GapError("INPUT_JSON_INVALID", "stdin", "stdin must contain one JSON document")]
        )
        _compact_emit(payload)
        return 1, payload
    payload = review_packet(packet)
    _compact_emit(payload)
    return (0 if payload["status"] == "ok" else 1), payload


if __name__ == "__main__":
    raise SystemExit(main()[0])
