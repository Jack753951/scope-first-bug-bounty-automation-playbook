#!/usr/bin/env python3
"""Validate Hacklab candidate finding and evidence metadata.

This helper is intentionally standard-library only. It is a semantic guard for the
P2-1 schema contract, not a full JSON Schema engine.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

HASH_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
URL_RE = re.compile(r"^https?://[^\s]+$")
SAFE_STORAGE_RE = re.compile(r"^runs/[A-Za-z0-9][A-Za-z0-9._:-]{2,127}/evidence/[A-Za-z0-9][A-Za-z0-9._/-]{0,255}$")
SENSITIVE_METADATA_KEY_RE = re.compile(
    r"(authorization|cookie|set-cookie|token|secret|password|passwd|api[_-]?key|credential|raw|body|request|response|header|bearer)",
    re.IGNORECASE,
)
SENSITIVE_METADATA_VALUE_RE = re.compile(
    r"(authorization\s*:|bearer\s+|set-cookie\s*:|cookie\s*:|password\s*=|passwd\s*=|api[_-]?key\s*=|token\s*=|secret\s*=|session\s*=)",
    re.IGNORECASE,
)

FINDING_TOP_KEYS = {
    "schema_version",
    "id",
    "status",
    "title",
    "summary",
    "target",
    "source",
    "severity_hint",
    "confidence",
    "triage",
    "evidence",
    "references",
    "classifications",
    "remediation",
    "verification_guidance",
}
EVIDENCE_TOP_KEYS = {
    "schema_version",
    "id",
    "finding_id",
    "kind",
    "captured_at_utc",
    "source",
    "target",
    "storage",
    "summary",
    "metadata",
}
TARGET_KEYS = {"type", "value"}
FINDING_SOURCE_KEYS = {"module_id", "run_id", "policy_decision_sha256"}
EVIDENCE_SOURCE_KEYS = {"tool", "module_id", "run_id"}
TRIAGE_KEYS = {"scanner_output_only", "manual_verification_required"}
EVIDENCE_REF_KEYS = {"id", "kind", "sha256", "redacted"}
STORAGE_KEYS = {"path", "sha256", "redacted"}
CLASSIFICATION_KEYS = {"cwe", "owasp", "cvss_vector"}

FINDING_STATUSES = {"candidate", "needs_verification", "no_observation", "not_applicable", "error"}
FORBIDDEN_STATUSES = {"confirmed", "verified", "accepted"}
SEVERITIES = {"info", "low", "medium", "high", "critical"}
CONFIDENCE = {"low", "medium", "high"}
TARGET_TYPES = {"url", "domain", "ip", "cidr"}
EVIDENCE_KINDS = {"http_exchange", "screenshot", "log_excerpt", "tool_output", "metadata"}


@dataclass
class ValidationResult:
    verdict: str = "deny"
    document_type: str = "bundle"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def allow_if_clean(self) -> "ValidationResult":
        self.verdict = "deny" if self.errors else "allow"
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "finding_evidence_validation/1.0",
            "document_type": self.document_type,
            "verdict": self.verdict,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def _unknown_keys(data: dict[str, Any], allowed: set[str], where: str, errors: list[str]) -> None:
    for key in sorted(set(data) - allowed):
        errors.append(f"{where}.{key} is not allowed")


def _require_keys(data: dict[str, Any], required: set[str], where: str, errors: list[str]) -> None:
    for key in sorted(required - set(data)):
        errors.append(f"{where}.{key} is required")


def _is_nonempty_string(value: Any, max_len: int = 2000) -> bool:
    return isinstance(value, str) and 1 <= len(value) <= max_len


def _validate_target(target: Any, where: str, errors: list[str]) -> None:
    if not isinstance(target, dict):
        errors.append(f"{where} must be an object")
        return
    _unknown_keys(target, TARGET_KEYS, where, errors)
    _require_keys(target, TARGET_KEYS, where, errors)
    if target.get("type") not in TARGET_TYPES:
        errors.append(f"{where}.type is unsupported")
    if not _is_nonempty_string(target.get("value"), 500):
        errors.append(f"{where}.value must be a non-empty string")


def _validate_storage_path(path_value: Any, run_id: Any, errors: list[str]) -> None:
    if not isinstance(path_value, str):
        errors.append("storage.path must be a string")
        return
    if "\\" in path_value or "://" in path_value:
        errors.append("storage.path must be a local POSIX path under runs/<run_id>/evidence/")
        return
    path = PurePosixPath(path_value)
    if path.is_absolute():
        errors.append("storage.path must be relative")
        return
    parts = path.parts
    if any(part in {"", ".", ".."} for part in parts):
        errors.append("storage.path must not contain traversal segments")
        return
    if len(parts) < 4 or parts[0] != "runs" or parts[2] != "evidence":
        errors.append("storage.path must be under runs/<run_id>/evidence/")
        return
    if isinstance(run_id, str) and parts[1] != run_id:
        errors.append("storage.path run_id must match source.run_id")
        return
    if not SAFE_STORAGE_RE.fullmatch(path_value):
        errors.append("storage.path contains unsupported characters")


def _validate_metadata(metadata: Any, errors: list[str], where: str = "metadata", depth: int = 0) -> None:
    if not isinstance(metadata, dict):
        errors.append("metadata must be an object")
        return
    if len(metadata) > 20:
        errors.append("metadata has too many fields")
    for key, value in metadata.items():
        if not isinstance(key, str) or not key:
            errors.append(f"{where} keys must be non-empty strings")
            continue
        if SENSITIVE_METADATA_KEY_RE.search(key):
            errors.append(f"{where}.{key} key looks sensitive; keep raw/sensitive data in redacted evidence files only")
        if isinstance(value, (dict, list)):
            errors.append(f"{where}.{key} must be a flat repository-safe scalar, not nested raw data")
        elif not isinstance(value, (str, int, float, bool)) and value is not None:
            errors.append(f"{where}.{key} has unsupported value type")
        elif isinstance(value, str):
            if len(value) > 500:
                errors.append(f"{where}.{key} value is too long for repository-safe metadata")
            if SENSITIVE_METADATA_VALUE_RE.search(value):
                errors.append(f"{where}.{key} value looks sensitive; keep raw/sensitive data in redacted evidence files only")


def _validate_finding(data: dict[str, Any]) -> ValidationResult:
    result = ValidationResult(document_type="finding")
    errors = result.errors
    _unknown_keys(data, FINDING_TOP_KEYS, "finding", errors)
    _require_keys(data, FINDING_TOP_KEYS, "finding", errors)

    if data.get("schema_version") != "finding/1.0":
        errors.append("schema_version must be finding/1.0")
    if not isinstance(data.get("id"), str) or not ID_RE.fullmatch(data.get("id", "")):
        errors.append("id must be a stable lowercase finding id")
    status = data.get("status")
    if status in FORBIDDEN_STATUSES:
        errors.append("confirmed/verified finding status is not allowed for automated output")
    elif status not in FINDING_STATUSES:
        errors.append("status is unsupported")
    if not _is_nonempty_string(data.get("title"), 200):
        errors.append("title must be a non-empty string")
    if not _is_nonempty_string(data.get("summary"), 2000):
        errors.append("summary must be a non-empty string")
    _validate_target(data.get("target"), "target", errors)

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        _unknown_keys(source, FINDING_SOURCE_KEYS, "source", errors)
        _require_keys(source, FINDING_SOURCE_KEYS, "source", errors)
        if not isinstance(source.get("module_id"), str) or not ID_RE.fullmatch(source.get("module_id", "")):
            errors.append("source.module_id is invalid")
        if not isinstance(source.get("run_id"), str) or not RUN_ID_RE.fullmatch(source.get("run_id", "")):
            errors.append("source.run_id is invalid")
        if not isinstance(source.get("policy_decision_sha256"), str) or not HASH_RE.fullmatch(source.get("policy_decision_sha256", "")):
            errors.append("source.policy_decision_sha256 must be canonical sha256")

    if data.get("severity_hint") not in SEVERITIES:
        errors.append("severity_hint is unsupported")
    if data.get("confidence") not in CONFIDENCE:
        errors.append("confidence is unsupported")

    triage = data.get("triage")
    if not isinstance(triage, dict):
        errors.append("triage must be an object")
    else:
        _unknown_keys(triage, TRIAGE_KEYS, "triage", errors)
        _require_keys(triage, TRIAGE_KEYS, "triage", errors)
        if triage.get("manual_verification_required") is not True:
            errors.append("triage.manual_verification_required must be true")
        if triage.get("scanner_output_only") is not True:
            errors.append("triage.scanner_output_only must be true")

    evidence = data.get("evidence")
    if not isinstance(evidence, list):
        errors.append("evidence must be a list")
    else:
        for idx, item in enumerate(evidence):
            where = f"evidence[{idx}]"
            if not isinstance(item, dict):
                errors.append(f"{where} must be an object")
                continue
            _unknown_keys(item, EVIDENCE_REF_KEYS, where, errors)
            _require_keys(item, EVIDENCE_REF_KEYS, where, errors)
            if not isinstance(item.get("id"), str) or not ID_RE.fullmatch(item.get("id", "")):
                errors.append(f"{where}.id is invalid")
            if item.get("kind") not in EVIDENCE_KINDS:
                errors.append(f"{where}.kind is unsupported")
            if not isinstance(item.get("sha256"), str) or not HASH_RE.fullmatch(item.get("sha256", "")):
                errors.append(f"{where}.sha256 must be canonical sha256")
            if item.get("redacted") is not True:
                errors.append(f"{where}.redacted must be true")

    refs = data.get("references")
    if not isinstance(refs, list):
        errors.append("references must be a list")
    else:
        for idx, ref in enumerate(refs):
            if not isinstance(ref, str) or not URL_RE.fullmatch(ref):
                errors.append(f"references[{idx}] must be an http(s) URL")

    classifications = data.get("classifications")
    if not isinstance(classifications, dict):
        errors.append("classifications must be an object")
    else:
        _unknown_keys(classifications, CLASSIFICATION_KEYS, "classifications", errors)
        cwes = classifications.get("cwe", [])
        if cwes is not None:
            if not isinstance(cwes, list) or any(not isinstance(c, str) or not re.fullmatch(r"CWE-[0-9]+", c) for c in cwes):
                errors.append("classifications.cwe entries must be CWE-numeric strings")
        owasp = classifications.get("owasp", [])
        if owasp is not None:
            if not isinstance(owasp, list) or any(not _is_nonempty_string(o, 120) for o in owasp):
                errors.append("classifications.owasp entries must be non-empty strings")
        cvss = classifications.get("cvss_vector")
        if cvss is not None and not _is_nonempty_string(cvss, 160):
            errors.append("classifications.cvss_vector must be a string")

    if not _is_nonempty_string(data.get("remediation"), 2000):
        errors.append("remediation must be a non-empty string")
    if not _is_nonempty_string(data.get("verification_guidance"), 2000):
        errors.append("verification_guidance must be a non-empty string")
    return result.allow_if_clean()


def _validate_evidence(data: dict[str, Any]) -> ValidationResult:
    result = ValidationResult(document_type="evidence")
    errors = result.errors
    _unknown_keys(data, EVIDENCE_TOP_KEYS, "evidence", errors)
    _require_keys(data, EVIDENCE_TOP_KEYS, "evidence", errors)

    if data.get("schema_version") != "evidence/1.0":
        errors.append("schema_version must be evidence/1.0")
    if not isinstance(data.get("id"), str) or not ID_RE.fullmatch(data.get("id", "")):
        errors.append("id is invalid")
    if not isinstance(data.get("finding_id"), str) or not ID_RE.fullmatch(data.get("finding_id", "")):
        errors.append("finding_id is invalid")
    if data.get("kind") not in EVIDENCE_KINDS:
        errors.append("kind is unsupported")
    if not isinstance(data.get("captured_at_utc"), str) or not UTC_RE.fullmatch(data.get("captured_at_utc", "")):
        errors.append("captured_at_utc must be UTC timestamp")

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        _unknown_keys(source, EVIDENCE_SOURCE_KEYS, "source", errors)
        _require_keys(source, EVIDENCE_SOURCE_KEYS, "source", errors)
        if not _is_nonempty_string(source.get("tool"), 120):
            errors.append("source.tool must be a non-empty string")
        if not isinstance(source.get("module_id"), str) or not ID_RE.fullmatch(source.get("module_id", "")):
            errors.append("source.module_id is invalid")
        if not isinstance(source.get("run_id"), str) or not RUN_ID_RE.fullmatch(source.get("run_id", "")):
            errors.append("source.run_id is invalid")

    _validate_target(data.get("target"), "target", errors)

    storage = data.get("storage")
    if not isinstance(storage, dict):
        errors.append("storage must be an object")
    else:
        _unknown_keys(storage, STORAGE_KEYS, "storage", errors)
        _require_keys(storage, STORAGE_KEYS, "storage", errors)
        _validate_storage_path(storage.get("path"), source.get("run_id") if isinstance(source, dict) else None, errors)
        if not isinstance(storage.get("sha256"), str) or not HASH_RE.fullmatch(storage.get("sha256", "")):
            errors.append("storage.sha256 must be canonical sha256")
        if storage.get("redacted") is not True:
            errors.append("storage.redacted must be true")

    if not _is_nonempty_string(data.get("summary"), 1000):
        errors.append("summary must be a non-empty string")
    _validate_metadata(data.get("metadata"), errors)
    return result.allow_if_clean()


def validate_data(data: Any, document_type: str) -> ValidationResult:
    if not isinstance(data, dict):
        return ValidationResult(document_type=document_type, errors=["document must be an object"]).allow_if_clean()
    if document_type == "finding":
        return _validate_finding(data)
    if document_type == "evidence":
        return _validate_evidence(data)
    return ValidationResult(document_type=document_type, errors=["document_type must be finding or evidence"]).allow_if_clean()


def validate_bundle(finding: Any, evidence_items: list[Any]) -> ValidationResult:
    result = ValidationResult(document_type="bundle")
    finding_result = validate_data(finding, "finding")
    result.errors.extend(f"finding: {error}" for error in finding_result.errors)
    evidence_by_id: dict[str, dict[str, Any]] = {}
    for idx, evidence in enumerate(evidence_items):
        evidence_result = validate_data(evidence, "evidence")
        result.errors.extend(f"evidence[{idx}]: {error}" for error in evidence_result.errors)
        if isinstance(evidence, dict) and isinstance(evidence.get("id"), str):
            evidence_by_id[evidence["id"]] = evidence

    if isinstance(finding, dict):
        finding_id = finding.get("id")
        for ref in finding.get("evidence", []) if isinstance(finding.get("evidence"), list) else []:
            if not isinstance(ref, dict):
                continue
            ev_id = ref.get("id")
            evidence = evidence_by_id.get(ev_id)
            if evidence is None:
                result.errors.append(f"evidence id {ev_id!r} referenced by finding is missing")
                continue
            if evidence.get("finding_id") != finding_id:
                result.errors.append(f"evidence id {ev_id!r} finding_id mismatch")
            storage = evidence.get("storage") if isinstance(evidence.get("storage"), dict) else {}
            if ref.get("sha256") != storage.get("sha256"):
                result.errors.append(f"evidence id {ev_id!r} sha256 mismatch")
            if ref.get("kind") != evidence.get("kind"):
                result.errors.append(f"evidence id {ev_id!r} kind mismatch")
            if ref.get("redacted") is not True or storage.get("redacted") is not True:
                result.errors.append(f"evidence id {ev_id!r} must be redacted")
    return result.allow_if_clean()


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    parser = argparse.ArgumentParser(description="Validate Hacklab finding/evidence metadata")
    parser.add_argument("--finding", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        finding = _load_json(args.finding)
        evidence = [_load_json(path) for path in args.evidence]
        result = validate_bundle(finding, evidence)
    except Exception as exc:  # keep CLI default-deny on IO/parse ambiguity
        result = ValidationResult(document_type="bundle", errors=[f"load failed: {exc}"]).allow_if_clean()

    payload = result.as_dict()
    if argv is None:
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(f"verdict: {payload['verdict']}")
            for error in payload["errors"]:
                print(f"ERROR: {error}")
            for warning in payload["warnings"]:
                print(f"WARNING: {warning}")
    return (0 if result.verdict == "allow" else 1), payload


if __name__ == "__main__":
    code, _payload = main()
    raise SystemExit(code)
