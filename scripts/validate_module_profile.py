#!/usr/bin/env python3
"""Validate Hacklab module profile contracts.

Profiles are repo-local JSON data that constrain which validated module manifests
may be selected by the dry-run runner. This validator is standard-library only,
performs no network activity, and treats ambiguity as deny.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _load_script_module(name: str):
    module_path = Path(__file__).resolve().with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(spec.name, module)
    spec.loader.exec_module(module)
    return module


profile_issues = _load_script_module("profile_issues")

PROFILE_SCHEMA_VERSION = "module_profile/1.0"
PROFILE_MALFORMED_JSON = profile_issues.PROFILE_MALFORMED_JSON
PROFILE_READ_ERROR = profile_issues.PROFILE_READ_ERROR
PROFILE_SCHEMA_INVALID = profile_issues.PROFILE_SCHEMA_INVALID
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
PROFILE_TOP_KEYS = {
    "schema_version",
    "profile_id",
    "name",
    "description",
    "mode_allowlist",
    "risk_level_allowlist",
    "target_type_allowlist",
    "technique_tag_allowlist",
    "execution_constraints",
    "output_constraints",
    "required_safety_gates_true",
    "required_safety_gates_false",
}
EXECUTION_CONSTRAINT_KEYS = {
    "supports_dry_run",
    "requires_network",
    "network_access",
    "target_touching",
    "destructive",
    "intrusive",
}
OUTPUT_CONSTRAINT_KEYS = {"emits_findings_allowed", "emits_evidence_allowed"}
MODES = {"dry-run"}


def _load_manifest_validator():
    return _load_script_module("validate_module_manifest")


validate_module_manifest = _load_manifest_validator()
RISK_LEVELS = validate_module_manifest.RISK_LEVELS
TARGET_TYPES = validate_module_manifest.TARGET_TYPES
TECHNIQUE_TAGS = validate_module_manifest.TECHNIQUE_TAGS
NETWORK_ACCESS = validate_module_manifest.NETWORK_ACCESS
SAFETY_KEYS = validate_module_manifest.SAFETY_KEYS
REQUIRED_TRUE_GATES = validate_module_manifest.REQUIRED_TRUE_GATES
REQUIRED_FALSE_GATES = validate_module_manifest.REQUIRED_FALSE_GATES


@dataclass
class ValidationResult:
    verdict: str = "deny"
    document_type: str = "module_profile"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error_codes: list[str] = field(default_factory=list)
    warning_codes: list[str] = field(default_factory=list)

    def allow_if_clean(self) -> "ValidationResult":
        self.verdict = "deny" if self.errors else "allow"
        if self.errors and not self.error_codes:
            self.error_codes = [PROFILE_SCHEMA_INVALID]
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "module_profile_validation/1.0",
            "document_type": self.document_type,
            "verdict": self.verdict,
            "errors": self.errors,
            "warnings": self.warnings,
            "error_codes": sorted(set(self.error_codes)),
            "warning_codes": sorted(set(self.warning_codes)),
        }


def _unknown_keys(data: dict[str, Any], allowed: set[str], where: str, errors: list[str]) -> None:
    for key in sorted(set(data) - allowed):
        errors.append(f"{where}.{key} is not allowed")


def _require_keys(data: dict[str, Any], required: set[str], where: str, errors: list[str]) -> None:
    for key in sorted(required - set(data)):
        errors.append(f"{where}.{key} is required")


def _is_nonempty_string(value: Any, max_len: int = 1000) -> bool:
    return isinstance(value, str) and 1 <= len(value) <= max_len


def _validate_unique_enum_list(value: Any, allowed: set[str], where: str, errors: list[str]) -> set[str]:
    seen: set[str] = set()
    if not isinstance(value, list) or not value:
        errors.append(f"{where} must be a non-empty list")
        return seen
    for idx, item in enumerate(value):
        if not isinstance(item, str) or item not in allowed:
            errors.append(f"{where}[{idx}] is unsupported")
            continue
        if item in seen:
            errors.append(f"{where}[{idx}] is duplicate")
        seen.add(item)
    return seen


def _validate_bool_constraints(value: Any, required: dict[str, bool], where: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{where} must be an object")
        return
    _unknown_keys(value, set(required), where, errors)
    _require_keys(value, set(required), where, errors)
    for key, expected in sorted(required.items()):
        if value.get(key) is not expected:
            errors.append(f"{where}.{key} must be {str(expected).lower()}")


def validate_module_profile(data: Any) -> ValidationResult:
    result = ValidationResult()
    errors = result.errors
    if not isinstance(data, dict):
        errors.append("module profile must be an object")
        return result.allow_if_clean()

    _unknown_keys(data, PROFILE_TOP_KEYS, "profile", errors)
    _require_keys(data, PROFILE_TOP_KEYS, "profile", errors)

    if data.get("schema_version") != PROFILE_SCHEMA_VERSION:
        errors.append(f"profile.schema_version must be {PROFILE_SCHEMA_VERSION}")
    if not isinstance(data.get("profile_id"), str) or not ID_RE.fullmatch(data.get("profile_id", "")):
        errors.append("profile.profile_id is invalid")
    for key in ("name", "description"):
        if not _is_nonempty_string(data.get(key), 1000):
            errors.append(f"profile.{key} must be a non-empty string")

    _validate_unique_enum_list(data.get("mode_allowlist"), MODES, "profile.mode_allowlist", errors)
    _validate_unique_enum_list(data.get("risk_level_allowlist"), RISK_LEVELS, "profile.risk_level_allowlist", errors)
    _validate_unique_enum_list(data.get("target_type_allowlist"), TARGET_TYPES, "profile.target_type_allowlist", errors)
    _validate_unique_enum_list(data.get("technique_tag_allowlist"), TECHNIQUE_TAGS, "profile.technique_tag_allowlist", errors)

    execution = data.get("execution_constraints")
    if not isinstance(execution, dict):
        errors.append("profile.execution_constraints must be an object")
    else:
        _unknown_keys(execution, EXECUTION_CONSTRAINT_KEYS, "profile.execution_constraints", errors)
        _require_keys(execution, EXECUTION_CONSTRAINT_KEYS, "profile.execution_constraints", errors)
        if execution.get("supports_dry_run") is not True:
            errors.append("profile.execution_constraints.supports_dry_run must be true")
        if execution.get("requires_network") is not False:
            errors.append("profile.execution_constraints.requires_network must be false")
        if execution.get("network_access") not in NETWORK_ACCESS:
            errors.append("profile.execution_constraints.network_access is unsupported")
        elif execution.get("network_access") != "none":
            errors.append("profile.execution_constraints.network_access must be none")
        if execution.get("target_touching") is not False:
            errors.append("profile.execution_constraints.target_touching must be false")
        if execution.get("destructive") is not False:
            errors.append("profile.execution_constraints.destructive must be false")
        if execution.get("intrusive") is not False:
            errors.append("profile.execution_constraints.intrusive must be false")

    _validate_bool_constraints(
        data.get("output_constraints"),
        {"emits_findings_allowed": False, "emits_evidence_allowed": False},
        "profile.output_constraints",
        errors,
    )
    true_gates = _validate_unique_enum_list(
        data.get("required_safety_gates_true"), SAFETY_KEYS, "profile.required_safety_gates_true", errors
    )
    false_gates = _validate_unique_enum_list(
        data.get("required_safety_gates_false"), SAFETY_KEYS, "profile.required_safety_gates_false", errors
    )
    for key in sorted(REQUIRED_TRUE_GATES - true_gates):
        errors.append(f"profile.required_safety_gates_true must include {key}")
    for key in sorted(REQUIRED_FALSE_GATES - false_gates):
        errors.append(f"profile.required_safety_gates_false must include {key}")
    for key in sorted(true_gates & false_gates):
        errors.append(f"profile safety gate {key} cannot be required true and false")

    return result.allow_if_clean()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a module_profile/1.0 JSON profile.")
    parser.add_argument("profile", type=Path, help="Path to module profile JSON")
    parser.add_argument("--json", action="store_true", help="Print structured JSON")
    args = parser.parse_args(argv)

    try:
        data = json.loads(args.profile.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result = ValidationResult(errors=[f"profile is not valid JSON: {exc}"], error_codes=[PROFILE_MALFORMED_JSON]).allow_if_clean()
    except OSError as exc:
        result = ValidationResult(errors=[f"profile could not be read: {exc}"], error_codes=[PROFILE_READ_ERROR]).allow_if_clean()
    else:
        result = validate_module_profile(data)

    if args.json:
        print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
    elif result.verdict == "allow":
        print("module profile validation allow")
    else:
        print("module profile validation deny")
        for error in result.errors:
            print(f"- {error}")
    return 0 if result.verdict == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
