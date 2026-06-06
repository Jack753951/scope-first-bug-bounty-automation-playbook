#!/usr/bin/env python3
"""Validate P2-10 module I/O envelope contracts.

This helper is intentionally standard-library only. It validates JSON data for the
future module input/result envelope layer without importing module code, launching
subprocesses, opening network connections, touching targets, or writing findings
or evidence. Ambiguity fails closed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Any

HASH_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9._-]+)?$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
TECHNIQUE_RE = re.compile(r"^(passive|active)\.[a-z0-9_]+$")
TARGET_TYPES = {"url", "domain", "ip", "cidr"}
RISK_LEVELS = {"info", "low", "medium", "high"}
RESULT_STATUSES = {"not_executed", "planned", "skipped", "error"}

INPUT_TOP_KEYS = {"schema_version", "run", "program", "target", "policy", "profile", "module", "constraints", "output"}
RUN_KEYS = {"run_id", "mode", "dry_run", "runner", "created_at_utc"}
PROGRAM_KEYS = {"slug", "scope_file_sha256", "global_scope_file_sha256"}
TARGET_KEYS = {"type", "value"}
POLICY_KEYS = {"decision", "decision_artifact_path", "decision_sha256", "checked_at_utc"}
PROFILE_KEYS = {"profile_id", "profile_sha256"}
MODULE_KEYS = {"module_id", "module_version", "manifest_sha256", "risk_level", "target_types", "technique_tags"}
CONSTRAINT_KEYS = {
    "supports_dry_run",
    "requires_network",
    "network_access",
    "target_touching",
    "destructive",
    "intrusive",
    "emits_findings",
    "emits_evidence",
    "manual_verification_required",
    "scanner_output_only",
    "store_redacted_evidence_only",
    "stores_raw_secrets",
    "writes_to_loot",
    "allows_destructive_actions",
    "allows_oast_callbacks",
}
OUTPUT_KEYS = {"module_output_dir", "findings", "evidence"}
RESULT_KEYS = {"schema_version", "run_id", "module_id", "status", "dry_run", "target_touching", "summary", "findings", "evidence", "errors", "warnings"}


@dataclass
class ValidationResult:
    verdict: str = "deny"
    document_type: str = "module_io"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def allow_if_clean(self) -> "ValidationResult":
        self.verdict = "deny" if self.errors else "allow"
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "module_io_contract_validation/1.0",
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


def _object(value: Any, where: str, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{where} must be an object")
        return None
    return value


def _nonempty_string(value: Any, max_len: int = 500) -> bool:
    return isinstance(value, str) and 1 <= len(value) <= max_len


def _check_const(value: Any, expected: Any, where: str, errors: list[str]) -> None:
    if value != expected:
        errors.append(f"{where} must be {expected!r}")


def _check_hash(value: Any, where: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not HASH_RE.fullmatch(value):
        errors.append(f"{where} must be canonical sha256")


def _check_run_id(value: Any, where: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not RUN_ID_RE.fullmatch(value):
        errors.append(f"{where} is invalid")


def _check_id(value: Any, where: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        errors.append(f"{where} is invalid")


def _check_utc(value: Any, where: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        errors.append(f"{where} must be UTC timestamp")


def _validate_string_array(value: Any, allowed: set[str] | None, pattern: re.Pattern[str] | None, where: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{where} must be a non-empty array")
        return
    seen: set[str] = set()
    for idx, item in enumerate(value):
        item_where = f"{where}[{idx}]"
        if not isinstance(item, str):
            errors.append(f"{item_where} must be a string")
            continue
        if item in seen:
            errors.append(f"{item_where} is duplicate")
        seen.add(item)
        if allowed is not None and item not in allowed:
            errors.append(f"{item_where} is unsupported")
        if pattern is not None and not pattern.fullmatch(item):
            errors.append(f"{item_where} is invalid")


def _validate_policy_path(value: Any, run_id: Any, where: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{where} must be a string")
        return
    if "\\" in value or "://" in value or "//" in value or "/./" in value or value.startswith("./") or value.endswith("/."):
        errors.append(f"{where} must be a local canonical POSIX path under runs/<run_id>/policy/")
        return
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        errors.append(f"{where} must be relative and must not contain traversal segments")
        return
    parts = path.parts
    if len(parts) != 4 or parts[0] != "runs" or parts[2] != "policy" or not parts[3].endswith(".json"):
        errors.append(f"{where} must be under runs/<run_id>/policy/<file>.json")
        return
    if isinstance(run_id, str) and parts[1] != run_id:
        errors.append(f"{where} run_id must match run.run_id")
    if not RUN_ID_RE.fullmatch(parts[1]) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\.json", parts[3]):
        errors.append(f"{where} contains unsupported characters")


def _validate_module_output_path(value: Any, run_id: Any, module_id: Any, where: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{where} must be a string")
        return
    if "\\" in value or "://" in value or "//" in value or "/./" in value or value.startswith("./") or value.endswith("/."):
        errors.append(f"{where} must be a local canonical POSIX path under runs/<run_id>/modules/<module_id>")
        return
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        errors.append(f"{where} must be relative and must not contain traversal segments")
        return
    parts = path.parts
    if len(parts) != 4 or parts[0] != "runs" or parts[2] != "modules":
        errors.append(f"{where} must be under runs/<run_id>/modules/<module_id>")
        return
    if isinstance(run_id, str) and parts[1] != run_id:
        errors.append(f"{where} run_id must match run.run_id")
    if isinstance(module_id, str) and parts[3] != module_id:
        errors.append(f"{where} module_id must match module.module_id")
    if not RUN_ID_RE.fullmatch(parts[1]) or not ID_RE.fullmatch(parts[3]):
        errors.append(f"{where} contains unsupported characters")


def _validate_empty_array(value: Any, where: str, errors: list[str]) -> None:
    if value != []:
        errors.append(f"{where} must be an empty array in P2-10")


def validate_module_input(data: Any) -> ValidationResult:
    result = ValidationResult(document_type="module_input")
    errors = result.errors
    root = _object(data, "document", errors)
    if root is None:
        return result.allow_if_clean()
    _unknown_keys(root, INPUT_TOP_KEYS, "document", errors)
    _require_keys(root, INPUT_TOP_KEYS, "document", errors)
    _check_const(root.get("schema_version"), "module_input/1.0", "schema_version", errors)

    run = _object(root.get("run"), "run", errors)
    run_id = None
    if run is not None:
        _unknown_keys(run, RUN_KEYS, "run", errors)
        _require_keys(run, RUN_KEYS, "run", errors)
        run_id = run.get("run_id")
        _check_run_id(run_id, "run.run_id", errors)
        _check_const(run.get("mode"), "dry-run", "run.mode", errors)
        _check_const(run.get("dry_run"), True, "run.dry_run", errors)
        _check_const(run.get("runner"), "hacklab-module-runner", "run.runner", errors)
        _check_utc(run.get("created_at_utc"), "run.created_at_utc", errors)

    program = _object(root.get("program"), "program", errors)
    if program is not None:
        _unknown_keys(program, PROGRAM_KEYS, "program", errors)
        _require_keys(program, PROGRAM_KEYS, "program", errors)
        _check_id(program.get("slug"), "program.slug", errors)
        _check_hash(program.get("scope_file_sha256"), "program.scope_file_sha256", errors)
        _check_hash(program.get("global_scope_file_sha256"), "program.global_scope_file_sha256", errors)

    target = _object(root.get("target"), "target", errors)
    if target is not None:
        _unknown_keys(target, TARGET_KEYS, "target", errors)
        _require_keys(target, TARGET_KEYS, "target", errors)
        if target.get("type") not in TARGET_TYPES:
            errors.append("target.type is unsupported")
        if not _nonempty_string(target.get("value"), 500):
            errors.append("target.value must be a non-empty string")

    policy = _object(root.get("policy"), "policy", errors)
    if policy is not None:
        _unknown_keys(policy, POLICY_KEYS, "policy", errors)
        _require_keys(policy, POLICY_KEYS, "policy", errors)
        _check_const(policy.get("decision"), "allow", "policy.decision", errors)
        _validate_policy_path(policy.get("decision_artifact_path"), run_id, "policy.decision_artifact_path", errors)
        _check_hash(policy.get("decision_sha256"), "policy.decision_sha256", errors)
        _check_utc(policy.get("checked_at_utc"), "policy.checked_at_utc", errors)

    profile = _object(root.get("profile"), "profile", errors)
    if profile is not None:
        _unknown_keys(profile, PROFILE_KEYS, "profile", errors)
        _require_keys(profile, PROFILE_KEYS, "profile", errors)
        _check_const(profile.get("profile_id"), "audit-baseline", "profile.profile_id", errors)
        _check_hash(profile.get("profile_sha256"), "profile.profile_sha256", errors)

    module = _object(root.get("module"), "module", errors)
    module_id = None
    if module is not None:
        _unknown_keys(module, MODULE_KEYS, "module", errors)
        _require_keys(module, MODULE_KEYS, "module", errors)
        module_id = module.get("module_id")
        _check_id(module_id, "module.module_id", errors)
        if not isinstance(module.get("module_version"), str) or not SEMVER_RE.fullmatch(module.get("module_version", "")):
            errors.append("module.module_version must be semantic version")
        _check_hash(module.get("manifest_sha256"), "module.manifest_sha256", errors)
        if module.get("risk_level") not in RISK_LEVELS:
            errors.append("module.risk_level is unsupported")
        _validate_string_array(module.get("target_types"), TARGET_TYPES, None, "module.target_types", errors)
        _validate_string_array(module.get("technique_tags"), None, TECHNIQUE_RE, "module.technique_tags", errors)

    constraints = _object(root.get("constraints"), "constraints", errors)
    if constraints is not None:
        _unknown_keys(constraints, CONSTRAINT_KEYS, "constraints", errors)
        _require_keys(constraints, CONSTRAINT_KEYS, "constraints", errors)
        true_fields = {"supports_dry_run", "manual_verification_required", "scanner_output_only", "store_redacted_evidence_only"}
        false_fields = CONSTRAINT_KEYS - true_fields - {"network_access"}
        for key in sorted(true_fields):
            _check_const(constraints.get(key), True, f"constraints.{key}", errors)
        _check_const(constraints.get("network_access"), "none", "constraints.network_access", errors)
        for key in sorted(false_fields):
            _check_const(constraints.get(key), False, f"constraints.{key}", errors)

    output = _object(root.get("output"), "output", errors)
    if output is not None:
        _unknown_keys(output, OUTPUT_KEYS, "output", errors)
        _require_keys(output, OUTPUT_KEYS, "output", errors)
        _validate_module_output_path(output.get("module_output_dir"), run_id, module_id, "output.module_output_dir", errors)
        _validate_empty_array(output.get("findings"), "output.findings", errors)
        _validate_empty_array(output.get("evidence"), "output.evidence", errors)

    return result.allow_if_clean()


def validate_module_result(data: Any) -> ValidationResult:
    result = ValidationResult(document_type="module_result")
    errors = result.errors
    root = _object(data, "document", errors)
    if root is None:
        return result.allow_if_clean()
    _unknown_keys(root, RESULT_KEYS, "document", errors)
    _require_keys(root, RESULT_KEYS, "document", errors)
    _check_const(root.get("schema_version"), "module_result/1.0", "schema_version", errors)
    _check_run_id(root.get("run_id"), "run_id", errors)
    _check_id(root.get("module_id"), "module_id", errors)
    if root.get("status") not in RESULT_STATUSES:
        errors.append("status is unsupported for P2-10")
    _check_const(root.get("dry_run"), True, "dry_run", errors)
    _check_const(root.get("target_touching"), False, "target_touching", errors)
    if not _nonempty_string(root.get("summary"), 500):
        errors.append("summary must be a non-empty string")
    else:
        summary = root["summary"].lower()
        if "executed" in summary and "not executed" not in summary:
            errors.append("summary must not imply module execution")
        blocked_terms = ("http response", "raw response", "secret", "token", "cookie", "loot", "callback", "scanner output", "confirmed")
        for term in blocked_terms:
            if term in summary:
                errors.append(f"summary must not contain unsafe term: {term}")
    _validate_empty_array(root.get("findings"), "findings", errors)
    _validate_empty_array(root.get("evidence"), "evidence", errors)
    for key in ("errors", "warnings"):
        value = root.get(key)
        if not isinstance(value, list):
            errors.append(f"{key} must be an array")
        elif len(value) > 20:
            errors.append(f"{key} must contain at most 20 items")
        else:
            for idx, item in enumerate(value):
                if not _nonempty_string(item, 200):
                    errors.append(f"{key}[{idx}] must be a non-empty string")
    return result.allow_if_clean()


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    parser = argparse.ArgumentParser(description="Validate offline-only module_input/1.0 or module_result/1.0 JSON contracts.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", help="Path to a module_input/1.0 JSON document.")
    group.add_argument("--result", help="Path to a module_result/1.0 JSON document.")
    parser.add_argument("--json", action="store_true", help="Print structured JSON output.")
    args = parser.parse_args(argv)

    try:
        if args.input:
            validation = validate_module_input(load_json(args.input))
        else:
            validation = validate_module_result(load_json(args.result))
    except (OSError, json.JSONDecodeError) as exc:
        document_type = "module_input" if args.input else "module_result"
        validation = ValidationResult(document_type=document_type, errors=[f"failed to load JSON: {exc}"]).allow_if_clean()

    payload = validation.as_dict()
    if args.json or validation.verdict != "allow":
        print(json.dumps(payload, indent=2, sort_keys=True))
    return (0 if validation.verdict == "allow" else 1), payload


if __name__ == "__main__":
    code, _payload = main()
    raise SystemExit(code)
