#!/usr/bin/env python3
# TRIAL ONLY — schema promotion deferred to P2.20+ after two real consumers exist.
"""Offline candidate review packet builder (P2.19, trial-only).

Reads allowlisted committed ``finding/1.0`` fixtures, validates each finding
through ``scripts.validate_finding_evidence.validate_data``, and emits a single
deterministic trial review-packet JSON document to stdout.

The builder is offline/local only. It performs no live scans, network calls,
target interaction, subprocess execution, filesystem writes, or runtime
wiring. Promotion to a versioned schema under ``modules/_schema/`` is deferred
until two distinct downstream consumers exercise the trial vocabulary
unchanged.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

SCHEMA_VERSION = "candidate_review_packet/0.1-trial"
FORBIDDEN_STATUSES = frozenset({"confirmed", "verified", "accepted"})

_ALLOWED_SECURITY_HEADERS_PREFIX = ("tests", "fixtures", "security_headers_baseline")
_ALLOWED_REVIEW_PACKET_PREFIX = ("tests", "fixtures", "candidate_review_packet")
_ALLOWED_LEAF = "expected_findings.json"


def _load_validator() -> Any:
    here = Path(__file__).resolve().parent
    target = here / "validate_finding_evidence.py"
    module_name = "_p2_19_finding_evidence_validator"
    existing = sys.modules.get(module_name)
    if existing is not None and hasattr(existing, "validate_data"):
        return existing.validate_data
    spec = importlib.util.spec_from_file_location(module_name, target)
    if spec is None or spec.loader is None:
        raise RuntimeError("validate_finding_evidence module could not be located")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    if not hasattr(module, "validate_data"):
        raise RuntimeError("validate_finding_evidence is missing validate_data")
    return module.validate_data


_validate_data = _load_validator()


@dataclass(frozen=True)
class PacketError:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {"code": self.code, "path": self.path, "message": self.message}


def _is_abs_or_drive_path(value: str) -> bool:
    if value.startswith("/"):
        return True
    if PureWindowsPath(value).drive:
        return True
    return False


def _matches_allowlist(parts: tuple[str, ...]) -> bool:
    if not parts or parts[-1] != _ALLOWED_LEAF:
        return False
    if (
        len(parts) == 5
        and parts[: len(_ALLOWED_SECURITY_HEADERS_PREFIX)] == _ALLOWED_SECURITY_HEADERS_PREFIX
    ):
        return True
    if (
        len(parts) >= 5
        and parts[: len(_ALLOWED_REVIEW_PACKET_PREFIX)] == _ALLOWED_REVIEW_PACKET_PREFIX
    ):
        return True
    return False


def _classify_input_path(
    rel_path: str, repo_root_resolved: Path
) -> tuple[str | None, str, Path | None]:
    if not isinstance(rel_path, str) or not rel_path:
        return ("INPUT_PATH_NOT_ALLOWED", "input path must be a non-empty string", None)
    if "\x00" in rel_path:
        return ("INPUT_PATH_UNSUPPORTED_CHARS", "input path must not contain NUL", None)
    if _is_abs_or_drive_path(rel_path):
        return (
            "INPUT_PATH_MUST_BE_RELATIVE",
            "input path must be repo-relative",
            None,
        )
    if "\\" in rel_path:
        return (
            "INPUT_PATH_UNSUPPORTED_CHARS",
            "input path must use forward slashes only",
            None,
        )
    if "://" in rel_path:
        return (
            "INPUT_PATH_UNSUPPORTED_CHARS",
            "input path must not contain URL scheme",
            None,
        )

    pure = PurePosixPath(rel_path)
    parts = pure.parts
    if any(part in ("", ".", "..") for part in parts):
        return (
            "INPUT_PATH_TRAVERSAL",
            "input path must not contain traversal segments",
            None,
        )

    if not _matches_allowlist(parts):
        return (
            "INPUT_PATH_NOT_ALLOWED",
            "input path is not in the committed allowlist",
            None,
        )

    candidate = repo_root_resolved
    for part in parts:
        candidate = candidate / part
        try:
            if candidate.exists() and candidate.is_symlink():
                return (
                    "INPUT_PATH_SYMLINK_REFUSED",
                    "symlinks are not allowed in input path components",
                    None,
                )
        except OSError:
            return (
                "INPUT_PATH_SYMLINK_REFUSED",
                "input path could not be inspected for symlinks",
                None,
            )

    try:
        resolved = candidate.resolve(strict=False)
    except OSError:
        return (
            "INPUT_PATH_OUTSIDE_REPO",
            "input path could not be resolved under repo root",
            None,
        )
    try:
        resolved.relative_to(repo_root_resolved)
    except ValueError:
        return (
            "INPUT_PATH_OUTSIDE_REPO",
            "input path must resolve under repo root",
            None,
        )
    if not candidate.exists():
        return (
            "INPUT_PATH_OUTSIDE_REPO",
            "input file is not present under repo root",
            None,
        )
    if not candidate.is_file():
        return (
            "INPUT_PATH_OUTSIDE_REPO",
            "input path must point to a regular file",
            None,
        )
    return (None, "", candidate)


def _build_review_questions(finding: dict[str, Any]) -> list[dict[str, str]]:
    target = finding.get("target") if isinstance(finding.get("target"), dict) else {}
    source = finding.get("source") if isinstance(finding.get("source"), dict) else {}
    classifications = (
        finding.get("classifications")
        if isinstance(finding.get("classifications"), dict)
        else {}
    )
    evidence = finding.get("evidence") if isinstance(finding.get("evidence"), list) else []

    target_value = target.get("value", "") if isinstance(target, dict) else ""
    target_type = target.get("type", "") if isinstance(target, dict) else ""
    module_id = source.get("module_id", "") if isinstance(source, dict) else ""
    policy_hash = (
        source.get("policy_decision_sha256", "") if isinstance(source, dict) else ""
    )
    severity = finding.get("severity_hint", "")
    confidence = finding.get("confidence", "")
    status = finding.get("status", "")
    evidence_count = len(evidence)
    cwes = classifications.get("cwe") if isinstance(classifications, dict) else None
    if not isinstance(cwes, list):
        cwes = []

    questions: list[dict[str, str]] = [
        {
            "key": "scope_in_authorized_scope",
            "text": (
                f"Confirm target.value '{target_value}' (type={target_type}) "
                "is within the program's authorized scope at the run window."
            ),
        },
        {
            "key": "policy_decision_freshness",
            "text": (
                f"Confirm source.policy_decision_sha256 '{policy_hash}' "
                f"is still the current allow artifact for module_id '{module_id}'."
            ),
        },
        {
            "key": "manual_verification_executed",
            "text": (
                "Confirm an authorized response has been manually inspected per "
                "verification_guidance before drafting."
            ),
        },
        {
            "key": "severity_calibration",
            "text": (
                f"Compare severity_hint='{severity}' against the program's severity rubric "
                "(program-specific, not platform-defined)."
            ),
        },
        {
            "key": "status_guardrail",
            "text": (
                f"This packet does NOT promote status from '{status}'. "
                "Promotion to confirmed/verified is a separate human step."
            ),
        },
    ]

    if evidence_count == 0:
        questions.append(
            {
                "key": "evidence_sufficiency",
                "text": (
                    "No evidence refs are attached. Capture a manual evidence file "
                    "before drafting, or leave as candidate-only."
                ),
            }
        )
    else:
        questions.append(
            {
                "key": "evidence_sufficiency",
                "text": (
                    f"Confirm the {evidence_count} attached evidence refs are redacted "
                    "and sufficient for the report kind."
                ),
            }
        )

    if cwes:
        cwe_repr = ", ".join(sorted(str(c) for c in cwes))
        questions.append(
            {
                "key": "cwe_classification_check",
                "text": (
                    f"Confirm CWE classifications {cwe_repr} accurately describe the observed condition."
                ),
            }
        )

    if confidence == "low":
        questions.append(
            {
                "key": "confidence_floor",
                "text": (
                    "Confidence is low; either raise it with additional verification "
                    "or keep this finding off the draft."
                ),
            }
        )

    questions.sort(key=lambda question: question["key"])
    return questions


def _report_readiness(finding: dict[str, Any]) -> str:
    evidence = finding.get("evidence") if isinstance(finding.get("evidence"), list) else []
    if not evidence:
        return "not_ready"
    if finding.get("confidence") == "low":
        return "not_ready"
    if finding.get("severity_hint") == "info":
        return "not_ready"
    return "reviewer_decision_required"


def _project_finding(finding: dict[str, Any]) -> dict[str, Any]:
    target = finding.get("target") if isinstance(finding.get("target"), dict) else {}
    source = finding.get("source") if isinstance(finding.get("source"), dict) else {}
    triage = finding.get("triage") if isinstance(finding.get("triage"), dict) else {}
    classifications = (
        finding.get("classifications")
        if isinstance(finding.get("classifications"), dict)
        else {}
    )
    evidence = finding.get("evidence") if isinstance(finding.get("evidence"), list) else []
    references = finding.get("references") if isinstance(finding.get("references"), list) else []
    cwes = classifications.get("cwe")
    owasp = classifications.get("owasp")
    return {
        "id": finding.get("id"),
        "status": finding.get("status"),
        "title": finding.get("title"),
        "summary": finding.get("summary"),
        "severity_hint": finding.get("severity_hint"),
        "confidence": finding.get("confidence"),
        "target": {
            "type": target.get("type") if isinstance(target, dict) else None,
            "value": target.get("value") if isinstance(target, dict) else None,
        },
        "source": {
            "module_id": source.get("module_id") if isinstance(source, dict) else None,
            "run_id": source.get("run_id") if isinstance(source, dict) else None,
            "policy_decision_sha256": (
                source.get("policy_decision_sha256") if isinstance(source, dict) else None
            ),
        },
        "evidence_ref_count": len(evidence),
        "classifications": {
            "cwe": list(cwes) if isinstance(cwes, list) else [],
            "owasp": list(owasp) if isinstance(owasp, list) else [],
            "cvss_vector": classifications.get("cvss_vector")
            if isinstance(classifications, dict)
            else None,
        },
        "references": list(references),
        "remediation": finding.get("remediation"),
        "verification_guidance": finding.get("verification_guidance"),
        "manual_verification_required": triage.get("manual_verification_required") is True
        if isinstance(triage, dict)
        else False,
        "scanner_output_only": triage.get("scanner_output_only") is True
        if isinstance(triage, dict)
        else False,
        "review_questions": _build_review_questions(finding),
        "report_readiness": _report_readiness(finding),
    }


def _build_summary(findings: list[dict[str, Any]], input_count: int) -> dict[str, Any]:
    targets = sorted(
        {
            entry["target"]["value"]
            for entry in findings
            if isinstance(entry.get("target"), dict)
            and isinstance(entry["target"].get("value"), str)
        }
    )
    modules = sorted(
        {
            entry["source"]["module_id"]
            for entry in findings
            if isinstance(entry.get("source"), dict)
            and isinstance(entry["source"].get("module_id"), str)
        }
    )
    return {
        "candidate_count": len(findings),
        "input_count": input_count,
        "modules": modules,
        "targets": targets,
    }


def _finding_sort_key(packet_finding: dict[str, Any]) -> tuple[str, str]:
    target = packet_finding.get("target") if isinstance(packet_finding.get("target"), dict) else {}
    return (
        str(packet_finding.get("id") or ""),
        str(target.get("value") or "") if isinstance(target, dict) else "",
    )


def build_packet(repo_root: str | Path, inputs: list[str]) -> dict[str, Any]:
    errors: list[PacketError] = []
    findings: list[dict[str, Any]] = []

    try:
        repo_root_resolved = Path(repo_root).resolve(strict=False)
    except OSError:
        errors.append(
            PacketError("REPO_ROOT_INVALID", "repo_root", "--repo-root could not be resolved")
        )
        return _packet_payload(errors, findings, 0)
    if not repo_root_resolved.exists() or not repo_root_resolved.is_dir():
        errors.append(
            PacketError(
                "REPO_ROOT_INVALID",
                "repo_root",
                "--repo-root does not exist or is not a directory",
            )
        )
        return _packet_payload(errors, findings, 0)

    seen: set[str] = set()
    deduped_inputs: list[str] = []
    for raw in inputs:
        if raw in seen:
            continue
        seen.add(raw)
        deduped_inputs.append(raw)

    for index, rel_path in enumerate(deduped_inputs):
        path_label = f"inputs[{index}]"
        code, message, candidate = _classify_input_path(rel_path, repo_root_resolved)
        if code is not None or candidate is None:
            errors.append(PacketError(code or "INPUT_PATH_NOT_ALLOWED", path_label, message))
            continue

        try:
            raw_text = candidate.read_text(encoding="utf-8")
        except OSError:
            errors.append(
                PacketError("INPUT_READ_FAILED", path_label, "input file could not be read")
            )
            continue
        try:
            data = json.loads(raw_text)
        except (UnicodeDecodeError, json.JSONDecodeError):
            errors.append(
                PacketError("INPUT_LOAD_FAILED", path_label, "input file is not valid JSON")
            )
            continue
        if not isinstance(data, list):
            errors.append(
                PacketError(
                    "INPUT_NOT_LIST",
                    path_label,
                    "input file must contain a JSON array of findings",
                )
            )
            continue

        for find_idx, finding in enumerate(data):
            finding_path = f"{path_label}.findings[{find_idx}]"
            if not isinstance(finding, dict):
                errors.append(
                    PacketError(
                        "FINDING_NOT_OBJECT", finding_path, "finding must be a JSON object"
                    )
                )
                continue
            status = finding.get("status")
            if isinstance(status, str) and status.lower() in FORBIDDEN_STATUSES:
                errors.append(
                    PacketError(
                        "FORBIDDEN_STATUS",
                        finding_path,
                        f"finding status '{status}' is not allowed in the candidate review packet",
                    )
                )
                continue
            result = _validate_data(finding, "finding")
            if getattr(result, "verdict", "deny") != "allow":
                detail = "; ".join(getattr(result, "errors", []) or [])
                errors.append(
                    PacketError(
                        "FINDING_VALIDATION_FAILED",
                        finding_path,
                        f"finding validation failed: {detail}"
                        if detail
                        else "finding validation failed",
                    )
                )
                continue
            findings.append(_project_finding(finding))

    findings.sort(key=_finding_sort_key)
    return _packet_payload(errors, findings, len(deduped_inputs))


def _packet_payload(
    errors: list[PacketError],
    findings: list[dict[str, Any]],
    input_count: int,
) -> dict[str, Any]:
    status = "ok" if not errors else "error"
    return {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "errors": [error.as_dict() for error in errors],
        "summary": _build_summary(findings, input_count),
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    parser = argparse.ArgumentParser(
        description=(
            "Build the trial offline candidate review packet (P2.19). Standard-library "
            "only; reads allowlisted committed expected_findings.json fixtures and emits "
            "one deterministic trial review-packet JSON document to stdout."
        )
    )
    parser.add_argument(
        "--repo-root",
        required=True,
        help="Repository root used to resolve every --input path.",
    )
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        help=(
            "Repo-relative path to a committed expected_findings.json fixture. "
            "Repeatable; at least one occurrence is required."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Accepted for compatibility; output is always JSON.",
    )
    args = parser.parse_args(argv)
    packet = build_packet(args.repo_root, args.input)
    sys.stdout.write(json.dumps(packet, sort_keys=True, separators=(",", ":")) + "\n")
    return (0 if packet.get("status") == "ok" else 1), packet


if __name__ == "__main__":
    code, _payload = main()
    raise SystemExit(code)
