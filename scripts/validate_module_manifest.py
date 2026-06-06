#!/usr/bin/env python3
"""Validate Hacklab module manifests.

This helper is intentionally standard-library only. It validates the P2-3 module
manifest contract that future runners must use before executing a module. The
validator performs no network activity and treats ambiguity as deny.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9._-]+)?$")
URL_RE = re.compile(r"^https?://[^\s]+$")
TOOL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._+-]{0,127}$")

MODULE_TOP_KEYS = {
    "schema_version",
    "module_id",
    "version",
    "name",
    "description",
    "risk_level",
    "target_types",
    "technique_tags",
    "execution",
    "external_tools",
    "output_contracts",
    "safety_gates",
    "references",
}
EXECUTION_KEYS = {
    "supports_dry_run",
    "requires_network",
    "network_access",
    "target_touching",
    "destructive",
    "intrusive",
    "default_profile",
}
TOOL_KEYS = {"name", "required", "version_constraint"}
OUTPUT_KEYS = {"run_schema", "finding_schema", "evidence_schema", "emits_findings", "emits_evidence"}
SAFETY_KEYS = {
    "require_policy_decision",
    "require_scope_match",
    "manual_verification_required",
    "scanner_output_only",
    "store_redacted_evidence_only",
    "stores_raw_secrets",
    "writes_to_loot",
    "allows_destructive_actions",
    "allows_oast_callbacks",
}

RISK_LEVELS = {"info", "low", "medium", "high"}
TARGET_TYPES = {"url", "domain", "ip", "cidr"}
TECHNIQUE_TAGS = {
    "passive.http_headers",
    "passive.tls_metadata",
    "passive.dns_metadata",
    "passive.content_metadata",
    "active.http_get",
    "active.tcp_connect",
    "active.dns_lookup",
    "active.web_content_check",
}
NETWORK_ACCESS = {"none", "dns", "target-http", "target-tcp"}
SUPPORTED_SCHEMAS = {
    "run_schema": "run/1.0",
    "finding_schema": "finding/1.0",
    "evidence_schema": "evidence/1.0",
}
REQUIRED_TRUE_GATES = {
    "require_policy_decision",
    "require_scope_match",
    "manual_verification_required",
    "scanner_output_only",
    "store_redacted_evidence_only",
}
REQUIRED_FALSE_GATES = {
    "stores_raw_secrets",
    "writes_to_loot",
    "allows_destructive_actions",
    "allows_oast_callbacks",
}


@dataclass
class ValidationResult:
    verdict: str = "deny"
    document_type: str = "module_manifest"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def allow_if_clean(self) -> "ValidationResult":
        self.verdict = "deny" if self.errors else "allow"
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "module_manifest_validation/1.0",
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


def _validate_execution(execution: Any, technique_tags: set[str], errors: list[str]) -> None:
    if not isinstance(execution, dict):
        errors.append("execution must be an object")
        return
    _unknown_keys(execution, EXECUTION_KEYS, "execution", errors)
    _require_keys(execution, EXECUTION_KEYS, "execution", errors)

    if execution.get("supports_dry_run") is not True:
        errors.append("execution.supports_dry_run must be true")
    if not isinstance(execution.get("requires_network"), bool):
        errors.append("execution.requires_network must be boolean")
    network_access = execution.get("network_access")
    if network_access not in NETWORK_ACCESS:
        errors.append("execution.network_access is unsupported")
    if not isinstance(execution.get("target_touching"), bool):
        errors.append("execution.target_touching must be boolean")
    if execution.get("destructive") is not False:
        errors.append("execution.destructive must be false")
    if execution.get("intrusive") is not False:
        errors.append("execution.intrusive must be false")
    if not _is_nonempty_string(execution.get("default_profile"), 120):
        errors.append("execution.default_profile must be a non-empty string")

    if execution.get("requires_network") is False:
        if network_access != "none":
            errors.append("execution.network_access must be none when requires_network is false")
        if execution.get("target_touching") is not False:
            errors.append("execution.target_touching must be false when requires_network is false")
    if network_access in {"target-http", "target-tcp"}:
        if execution.get("requires_network") is not True:
            errors.append("execution.requires_network must be true for target network access")
        if execution.get("target_touching") is not True:
            errors.append("execution.target_touching must be true for target network access")
    if network_access == "dns" and execution.get("requires_network") is not True:
        errors.append("execution.requires_network must be true for dns network access")
    if any(tag.startswith("active.") for tag in technique_tags) and execution.get("requires_network") is not True:
        errors.append("execution.requires_network must be true for active technique_tags")

    expected_postures = {
        "active.http_get": ("target-http", True),
        "active.web_content_check": ("target-http", True),
        "active.tcp_connect": ("target-tcp", True),
        "active.dns_lookup": ("dns", False),
    }
    for tag, (expected_network, expected_touching) in expected_postures.items():
        if tag in technique_tags:
            if network_access != expected_network or execution.get("target_touching") is not expected_touching:
                errors.append(
                    f"execution network posture conflicts with technique_tags {tag}: "
                    f"expected network_access={expected_network} and target_touching={str(expected_touching).lower()}"
                )
    if technique_tags and not any(tag.startswith("active.") for tag in technique_tags):
        if execution.get("target_touching") is not False:
            errors.append("execution network posture conflicts with passive-only technique_tags: target_touching must be false")


def _validate_external_tools(tools: Any, errors: list[str]) -> None:
    if not isinstance(tools, list):
        errors.append("external_tools must be a list")
        return
    names: set[str] = set()
    for idx, item in enumerate(tools):
        where = f"external_tools[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{where} must be an object")
            continue
        _unknown_keys(item, TOOL_KEYS, where, errors)
        _require_keys(item, {"name", "required"}, where, errors)
        name = item.get("name")
        if not isinstance(name, str) or not TOOL_NAME_RE.fullmatch(name):
            errors.append(f"{where}.name is invalid")
        elif name in names:
            errors.append(f"{where}.name is duplicate")
        else:
            names.add(name)
        if not isinstance(item.get("required"), bool):
            errors.append(f"{where}.required must be boolean")
        if "version_constraint" in item and not _is_nonempty_string(item.get("version_constraint"), 80):
            errors.append(f"{where}.version_constraint must be a non-empty string")


def _validate_output_contracts(output: Any, errors: list[str]) -> None:
    if not isinstance(output, dict):
        errors.append("output_contracts must be an object")
        return
    _unknown_keys(output, OUTPUT_KEYS, "output_contracts", errors)
    _require_keys(output, OUTPUT_KEYS, "output_contracts", errors)
    for key, expected in SUPPORTED_SCHEMAS.items():
        if output.get(key) != expected:
            errors.append(f"output_contracts.{key} must be {expected}")
    for key in ("emits_findings", "emits_evidence"):
        if not isinstance(output.get(key), bool):
            errors.append(f"output_contracts.{key} must be boolean")


def _validate_safety_gates(gates: Any, errors: list[str]) -> None:
    if not isinstance(gates, dict):
        errors.append("safety_gates must be an object")
        return
    _unknown_keys(gates, SAFETY_KEYS, "safety_gates", errors)
    _require_keys(gates, SAFETY_KEYS, "safety_gates", errors)
    for key in sorted(REQUIRED_TRUE_GATES):
        if gates.get(key) is not True:
            errors.append(f"safety_gates.{key} must be true")
    for key in sorted(REQUIRED_FALSE_GATES):
        if gates.get(key) is not False:
            errors.append(f"safety_gates.{key} must be false")


def validate_module_manifest(data: Any) -> ValidationResult:
    result = ValidationResult()
    errors = result.errors
    if not isinstance(data, dict):
        errors.append("module manifest must be an object")
        return result.allow_if_clean()

    _unknown_keys(data, MODULE_TOP_KEYS, "module", errors)
    _require_keys(data, MODULE_TOP_KEYS, "module", errors)
    if data.get("schema_version") != "module_manifest/1.0":
        errors.append("schema_version must be module_manifest/1.0")
    if not isinstance(data.get("module_id"), str) or not ID_RE.fullmatch(data.get("module_id", "")):
        errors.append("module_id is invalid")
    if not isinstance(data.get("version"), str) or not VERSION_RE.fullmatch(data.get("version", "")):
        errors.append("version must be semantic version")
    if not _is_nonempty_string(data.get("name"), 120):
        errors.append("name must be a non-empty string")
    if not _is_nonempty_string(data.get("description"), 1000):
        errors.append("description must be a non-empty string")
    if data.get("risk_level") not in RISK_LEVELS:
        errors.append("risk_level is unsupported")

    _validate_unique_enum_list(data.get("target_types"), TARGET_TYPES, "target_types", errors)
    technique_tags = _validate_unique_enum_list(data.get("technique_tags"), TECHNIQUE_TAGS, "technique_tags", errors)
    _validate_execution(data.get("execution"), technique_tags, errors)
    _validate_external_tools(data.get("external_tools"), errors)
    _validate_output_contracts(data.get("output_contracts"), errors)
    _validate_safety_gates(data.get("safety_gates"), errors)

    refs = data.get("references")
    if not isinstance(refs, list):
        errors.append("references must be a list")
    else:
        for idx, ref in enumerate(refs):
            if not isinstance(ref, str) or not URL_RE.fullmatch(ref):
                errors.append(f"references[{idx}] must be an http(s) URL")

    return result.allow_if_clean()


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    parser = argparse.ArgumentParser(description="Validate Hacklab module manifest metadata")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = validate_module_manifest(_load_json(args.manifest))
    except Exception as exc:  # keep CLI default-deny on IO/parse ambiguity
        result = ValidationResult(errors=[f"load failed: {exc}"]).allow_if_clean()

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
