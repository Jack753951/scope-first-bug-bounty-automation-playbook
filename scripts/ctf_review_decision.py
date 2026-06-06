#!/usr/bin/env python3
"""Offline CTF review-decision helper.

P2.17 pure review decision over a JSON input file or stdin. Standard-library
only. No network, no sockets, no subprocess, no file writes beyond the
explicit ``--output`` path.

The script consumes a structured solver result, classifies it as
``hint`` / ``candidate`` / ``verified`` / ``needs_second_review``, and emits a
deterministic JSON decision document.

Output fields (sorted keys, sorted triggers):

* ``schema_hint`` -- non-binding, unversioned hint string for callers.
* ``status``      -- one of ``hint`` / ``candidate`` / ``verified`` / ``needs_second_review``.
* ``confidence``  -- one of ``low`` / ``medium`` / ``high`` (default ``low``).
* ``triggers``    -- sorted list of second-review trigger codes.
* ``reasons``     -- sorted list of short human-readable reason strings.
* ``input_hash``  -- SHA-256 of the canonical JSON form of the input.

The helper is intentionally conservative:

* Ambiguity defaults to ``needs_second_review`` with ``confidence`` capped
  at ``low``.
* High confidence is never inferred; callers must explicitly pass
  ``claimed_confidence: "high"`` AND have a non-empty ``verifier`` block.
* Any input fields that look like network targets, scope overrides, or
  status assertions are recorded as ignored. They never grant verification
  and never trigger network action.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_HINT = "ctf_review_decision/0.1-unversioned"

STATUS_HINT = "hint"
STATUS_CANDIDATE = "candidate"
STATUS_VERIFIED = "verified"
STATUS_NEEDS_SECOND_REVIEW = "needs_second_review"

ALLOWED_STATUSES = (
    STATUS_HINT,
    STATUS_CANDIDATE,
    STATUS_VERIFIED,
    STATUS_NEEDS_SECOND_REVIEW,
)

CONFIDENCE_LOW = "low"
CONFIDENCE_MEDIUM = "medium"
CONFIDENCE_HIGH = "high"
ALLOWED_CONFIDENCES = (CONFIDENCE_LOW, CONFIDENCE_MEDIUM, CONFIDENCE_HIGH)

TRIGGER_ABNORMAL_FORMAT = "abnormal_format"
TRIGGER_MULTIPLE_CANDIDATES = "multiple_candidates"
TRIGGER_SOLVER_TIMEOUT = "solver_timeout"
TRIGGER_EXTERNAL_SOURCE_ONLY = "external_source_only"
TRIGGER_UI_OR_CHECKER_ONLY = "ui_or_checker_only"

ALLOWED_TRIGGERS = (
    TRIGGER_ABNORMAL_FORMAT,
    TRIGGER_EXTERNAL_SOURCE_ONLY,
    TRIGGER_MULTIPLE_CANDIDATES,
    TRIGGER_SOLVER_TIMEOUT,
    TRIGGER_UI_OR_CHECKER_ONLY,
)

UI_OR_CHECKER_SOURCE_TAGS = frozenset({"ui", "ui_checker", "checker"})
EXTERNAL_SOURCE_TAGS = frozenset({"external_writeup", "external_source"})
ACCEPTABLE_VERIFIER_KINDS = frozenset(
    {
        "deterministic_replay",
        "checksum_match",
        "oracle_replay",
        "source_transform_inversion",
        "parser_validation",
    }
)

# Fields that look like network/scope/status overrides. They are recorded as
# ignored and never acted upon. They never grant verification.
OVERRIDE_FIELD_NAMES = frozenset(
    {
        "target_url",
        "target_host",
        "target_ip",
        "scope_override",
        "live_target",
        "force_verified",
        "status",
        "asserted_status",
        "override_status",
    }
)


class DecisionInputError(ValueError):
    pass


def _canonical_bytes(payload: Any) -> bytes:
    return json.dumps(
        payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")


def _hash_input(payload: Any) -> str:
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return False


def _coerce_str_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _format_matches(candidate: Any, pattern: Any) -> bool | None:
    if not isinstance(pattern, str) or pattern == "":
        return None
    if not isinstance(candidate, str):
        return False
    try:
        compiled = re.compile(pattern)
    except re.error:
        return None
    return compiled.search(candidate) is not None


def _detect_triggers(payload: dict, reasons: list[str]) -> list[str]:
    triggers: set[str] = set()

    candidate_flag = payload.get("candidate_flag")
    expected_regex = payload.get("expected_format_regex")
    fmt = _format_matches(candidate_flag, expected_regex)
    if fmt is False:
        triggers.add(TRIGGER_ABNORMAL_FORMAT)
        reasons.append("candidate_flag did not match expected_format_regex")
    if _coerce_bool(payload.get("abnormal_format")):
        triggers.add(TRIGGER_ABNORMAL_FORMAT)
        reasons.append("input asserted abnormal_format")

    candidate_count = payload.get("candidate_count")
    candidates_list = payload.get("multiple_candidates")
    if isinstance(candidate_count, int) and candidate_count > 1:
        triggers.add(TRIGGER_MULTIPLE_CANDIDATES)
        reasons.append("candidate_count > 1")
    if isinstance(candidates_list, list) and len(candidates_list) > 1:
        triggers.add(TRIGGER_MULTIPLE_CANDIDATES)
        reasons.append("multiple_candidates list has more than one entry")

    if _coerce_bool(payload.get("solver_timed_out")):
        triggers.add(TRIGGER_SOLVER_TIMEOUT)
        reasons.append("solver_timed_out flag asserted")

    sources = _coerce_str_list(payload.get("candidate_sources"))
    source_set = frozenset(sources)
    if source_set and source_set.issubset(EXTERNAL_SOURCE_TAGS):
        triggers.add(TRIGGER_EXTERNAL_SOURCE_ONLY)
        reasons.append("candidate_sources contained only external writeup tags")
    if _coerce_bool(payload.get("external_source_only")):
        triggers.add(TRIGGER_EXTERNAL_SOURCE_ONLY)
        reasons.append("input asserted external_source_only")

    if source_set and source_set.issubset(UI_OR_CHECKER_SOURCE_TAGS):
        triggers.add(TRIGGER_UI_OR_CHECKER_ONLY)
        reasons.append("candidate_sources contained only UI/checker tags")
    if _coerce_bool(payload.get("checker_only_success")):
        triggers.add(TRIGGER_UI_OR_CHECKER_ONLY)
        reasons.append("checker_only_success flag asserted")

    return sorted(triggers)


def _decide_status(payload: dict, triggers: list[str], reasons: list[str]) -> str:
    if triggers:
        return STATUS_NEEDS_SECOND_REVIEW
    verifier = payload.get("verifier")
    if isinstance(verifier, dict):
        kind = verifier.get("kind")
        if isinstance(kind, str) and kind in ACCEPTABLE_VERIFIER_KINDS:
            reasons.append(f"verifier kind {kind} accepted (no triggers fired)")
            return STATUS_VERIFIED
    if isinstance(payload.get("candidate_flag"), str) and payload["candidate_flag"]:
        return STATUS_CANDIDATE
    return STATUS_HINT


def _decide_confidence(payload: dict, status: str, reasons: list[str]) -> str:
    claimed = payload.get("claimed_confidence")
    base = CONFIDENCE_LOW
    if isinstance(claimed, str) and claimed in ALLOWED_CONFIDENCES:
        base = claimed
    else:
        reasons.append("claimed_confidence missing or invalid; defaulting to low")

    if status == STATUS_NEEDS_SECOND_REVIEW:
        if base != CONFIDENCE_LOW:
            reasons.append("confidence capped at low because status is needs_second_review")
        return CONFIDENCE_LOW

    if base == CONFIDENCE_HIGH and status != STATUS_VERIFIED:
        reasons.append(
            "high confidence not inferred without verified status; downgraded to medium"
        )
        return CONFIDENCE_MEDIUM

    return base


def _collect_ignored(payload: dict, reasons: list[str]) -> list[str]:
    ignored = sorted(
        name for name in OVERRIDE_FIELD_NAMES if name in payload
    )
    if ignored:
        reasons.append(
            "ignored override fields (no-op, no network action): " + ", ".join(ignored)
        )
    return ignored


def decide(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise DecisionInputError("input JSON must be an object")

    reasons: list[str] = []
    ignored = _collect_ignored(payload, reasons)
    triggers = _detect_triggers(payload, reasons)
    status = _decide_status(payload, triggers, reasons)
    confidence = _decide_confidence(payload, status, reasons)

    decision = {
        "schema_hint": SCHEMA_HINT,
        "status": status,
        "confidence": confidence,
        "triggers": triggers,
        "reasons": sorted(set(reasons)),
        "ignored_fields": ignored,
        "input_hash": _hash_input(payload),
    }
    return decision


def _render(decision: dict) -> str:
    return json.dumps(decision, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def _load_input(source: str) -> dict:
    if source == "-":
        text = sys.stdin.read()
    else:
        text = Path(source).read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise DecisionInputError(f"input is not valid JSON: {exc.msg}") from exc
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ctf_review_decision",
        description=(
            "Pure offline CTF review-decision helper. Reads a JSON result and "
            "emits a deterministic decision document. No network, no subprocess."
        ),
    )
    parser.add_argument(
        "--input",
        default="-",
        help='Path to the input JSON file, or "-" for stdin (default: stdin).',
    )
    parser.add_argument(
        "--output",
        default="-",
        help='Path to the output JSON file, or "-" for stdout (default: stdout).',
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        payload = _load_input(args.input)
        decision = decide(payload)
    except DecisionInputError as exc:
        sys.stderr.write(json.dumps({"status": "error", "error": str(exc)}, sort_keys=True) + "\n")
        return 2

    rendered = _render(decision)
    if args.output == "-":
        sys.stdout.write(rendered)
    else:
        Path(args.output).write_text(rendered, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
