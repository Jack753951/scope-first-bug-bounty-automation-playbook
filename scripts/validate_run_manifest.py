#!/usr/bin/env python3
"""Validate Hacklab run manifests and run/finding/evidence bundles.

This helper is intentionally standard-library only. It validates the P2-2 run
execution ledger contract and cross-checks P2-1 finding/evidence metadata when
provided. It performs no network activity and treats ambiguity as deny.
"""

from __future__ import annotations

import argparse
import importlib.util
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
RUN_PATH_RE = re.compile(r"^runs/[A-Za-z0-9][A-Za-z0-9._:-]{2,127}/(policy|findings|evidence)/[A-Za-z0-9][A-Za-z0-9._/-]{0,255}$")
RECON_POLICY_PATH_RE = re.compile(r"^scans/[A-Za-z0-9][A-Za-z0-9._-]{2,255}/evidence/policy/policy_boundary_[A-Za-z0-9_.-]+\.json$")

RUN_TOP_KEYS = {
    "schema_version",
    "run_id",
    "created_at_utc",
    "completed_at_utc",
    "status",
    "program",
    "target",
    "policy",
    "execution",
    "modules",
    "artifacts",
    "review",
}
PROGRAM_KEYS = {"slug", "scope_file_sha256", "global_scope_file_sha256"}
TARGET_KEYS = {"type", "value"}
POLICY_KEYS = {"mode", "decision", "decision_artifact_path", "decision_sha256", "checked_at_utc"}
EXECUTION_KEYS = {"runner", "profile", "profile_id", "profile_sha256", "dry_run", "target_touching"}
MODULE_KEYS = {"module_id", "manifest_sha256", "status"}
ARTIFACT_KEYS = {"findings", "evidence"}
FINDING_ARTIFACT_KEYS = {"id", "path", "sha256"}
EVIDENCE_ARTIFACT_KEYS = {"id", "path", "sha256", "redacted"}
REVIEW_KEYS = {"manual_verification_required", "scanner_output_only", "agent_review_status"}

RUN_STATUSES = {"planned", "running", "completed", "error", "aborted"}
POLICY_MODES = {"dry-run", "planned", "live"}
MODULE_STATUSES = {"planned", "skipped", "completed", "error"}
AGENT_REVIEW_STATUSES = {"not_started", "in_review", "needs_human", "accepted", "rejected"}
TARGET_TYPES = {"url", "domain", "ip", "cidr"}


@dataclass
class ValidationResult:
    verdict: str = "deny"
    document_type: str = "run"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def allow_if_clean(self) -> "ValidationResult":
        self.verdict = "deny" if self.errors else "allow"
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "run_manifest_validation/1.0",
            "document_type": self.document_type,
            "verdict": self.verdict,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def _load_finding_validator():
    module_path = Path(__file__).with_name("validate_finding_evidence.py")
    spec = importlib.util.spec_from_file_location("validate_finding_evidence", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load validate_finding_evidence.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(spec.name, module)
    spec.loader.exec_module(module)
    return module


def _unknown_keys(data: dict[str, Any], allowed: set[str], where: str, errors: list[str]) -> None:
    for key in sorted(set(data) - allowed):
        errors.append(f"{where}.{key} is not allowed")


def _require_keys(data: dict[str, Any], required: set[str], where: str, errors: list[str]) -> None:
    for key in sorted(required - set(data)):
        errors.append(f"{where}.{key} is required")


def _is_nonempty_string(value: Any, max_len: int = 500) -> bool:
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


def _validate_run_path(path_value: Any, run_id: Any, expected_section: str, where: str, errors: list[str]) -> None:
    if not isinstance(path_value, str):
        errors.append(f"{where}.path must be a string")
        return
    if "\\" in path_value or "://" in path_value:
        errors.append(f"{where}.path must be a local POSIX path under runs/<run_id>/{expected_section}/")
        return
    path = PurePosixPath(path_value)
    if path.is_absolute():
        errors.append(f"{where}.path must be relative")
        return
    parts = path.parts
    if any(part in {"", ".", ".."} for part in parts):
        errors.append(f"{where}.path must not contain traversal segments")
        return
    if len(parts) < 4 or parts[0] != "runs" or parts[2] != expected_section:
        errors.append(f"{where}.path must be under runs/<run_id>/{expected_section}/")
        return
    if isinstance(run_id, str) and parts[1] != run_id:
        errors.append(f"{where}.path run_id must match run_id")
        return
    if not RUN_PATH_RE.fullmatch(path_value):
        errors.append(f"{where}.path contains unsupported characters")


def _validate_policy_decision_path(path_value: Any, run_id: Any, errors: list[str]) -> None:
    where = "policy.decision_artifact_path"
    if not isinstance(path_value, str):
        errors.append(f"{where}.path must be a string")
        return
    if "\\" in path_value or "://" in path_value:
        errors.append(f"{where}.path must be a local POSIX path under runs/<run_id>/policy/ or scans/<scan-dir>/evidence/policy/")
        return
    path = PurePosixPath(path_value)
    if path.is_absolute():
        errors.append(f"{where}.path must be relative")
        return
    parts = path.parts
    if any(part in {"", ".", ".."} for part in parts):
        errors.append(f"{where}.path must not contain traversal segments")
        return
    if len(parts) >= 4 and parts[0] == "runs" and parts[2] == "policy":
        if isinstance(run_id, str) and parts[1] != run_id:
            errors.append(f"{where}.path run_id must match run_id")
            return
        if not RUN_PATH_RE.fullmatch(path_value):
            errors.append(f"{where}.path contains unsupported characters")
        return
    if len(parts) == 5 and parts[0] == "scans" and parts[2:4] == ("evidence", "policy"):
        if not RECON_POLICY_PATH_RE.fullmatch(path_value):
            errors.append(f"{where}.path must match scans/<scan-dir>/evidence/policy/policy_boundary_*.json")
        return
    errors.append(f"{where}.path must be under runs/<run_id>/policy/ or scans/<scan-dir>/evidence/policy/")


def _validate_program(program: Any, errors: list[str]) -> None:
    if not isinstance(program, dict):
        errors.append("program must be an object")
        return
    _unknown_keys(program, PROGRAM_KEYS, "program", errors)
    _require_keys(program, PROGRAM_KEYS, "program", errors)
    if not isinstance(program.get("slug"), str) or not ID_RE.fullmatch(program.get("slug", "")):
        errors.append("program.slug is invalid")
    for key in ("scope_file_sha256", "global_scope_file_sha256"):
        if not isinstance(program.get(key), str) or not HASH_RE.fullmatch(program.get(key, "")):
            errors.append(f"program.{key} must be canonical sha256")


def _validate_policy(policy: Any, run_id: Any, errors: list[str]) -> None:
    if not isinstance(policy, dict):
        errors.append("policy must be an object")
        return
    _unknown_keys(policy, POLICY_KEYS, "policy", errors)
    _require_keys(policy, POLICY_KEYS, "policy", errors)
    if policy.get("mode") not in POLICY_MODES:
        errors.append("policy.mode is unsupported")
    if policy.get("decision") != "allow":
        errors.append("policy.decision must be allow for an execution ledger")
    _validate_policy_decision_path(policy.get("decision_artifact_path"), run_id, errors)
    if not isinstance(policy.get("decision_sha256"), str) or not HASH_RE.fullmatch(policy.get("decision_sha256", "")):
        errors.append("policy.decision_sha256 must be canonical sha256")
    if not isinstance(policy.get("checked_at_utc"), str) or not UTC_RE.fullmatch(policy.get("checked_at_utc", "")):
        errors.append("policy.checked_at_utc must be UTC timestamp")


def _validate_execution(execution: Any, policy: Any, errors: list[str]) -> None:
    if not isinstance(execution, dict):
        errors.append("execution must be an object")
        return
    _unknown_keys(execution, EXECUTION_KEYS, "execution", errors)
    _require_keys(execution, EXECUTION_KEYS, "execution", errors)
    if not _is_nonempty_string(execution.get("runner"), 120):
        errors.append("execution.runner must be a non-empty string")
    if not _is_nonempty_string(execution.get("profile"), 120):
        errors.append("execution.profile must be a non-empty string")
    if not _is_nonempty_string(execution.get("profile_id"), 120):
        errors.append("execution.profile_id must be a non-empty string")
    if execution.get("profile_id") != execution.get("profile"):
        errors.append("execution.profile_id must match execution.profile")
    if not isinstance(execution.get("profile_sha256"), str) or not HASH_RE.fullmatch(execution.get("profile_sha256", "")):
        errors.append("execution.profile_sha256 must be canonical sha256")
    if not isinstance(execution.get("dry_run"), bool):
        errors.append("execution.dry_run must be boolean")
    if not isinstance(execution.get("target_touching"), bool):
        errors.append("execution.target_touching must be boolean")
    if isinstance(policy, dict) and policy.get("mode") == "dry-run" and execution.get("target_touching") is not False:
        errors.append("execution.target_touching must be false when policy.mode is dry-run")
    if execution.get("dry_run") is True and execution.get("target_touching") is not False:
        errors.append("execution.target_touching must be false when execution.dry_run is true")


def _validate_modules(modules: Any, errors: list[str]) -> set[str]:
    module_ids: set[str] = set()
    if not isinstance(modules, list) or not modules:
        errors.append("modules must be a non-empty list")
        return module_ids
    for idx, item in enumerate(modules):
        where = f"modules[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{where} must be an object")
            continue
        _unknown_keys(item, MODULE_KEYS, where, errors)
        _require_keys(item, MODULE_KEYS, where, errors)
        module_id = item.get("module_id")
        if not isinstance(module_id, str) or not ID_RE.fullmatch(module_id):
            errors.append(f"{where}.module_id is invalid")
        elif module_id in module_ids:
            errors.append(f"{where}.module_id is duplicate")
        else:
            module_ids.add(module_id)
        if not isinstance(item.get("manifest_sha256"), str) or not HASH_RE.fullmatch(item.get("manifest_sha256", "")):
            errors.append(f"{where}.manifest_sha256 must be canonical sha256")
        if item.get("status") not in MODULE_STATUSES:
            errors.append(f"{where}.status is unsupported")
    return module_ids


def _validate_artifact_ref(item: Any, keys: set[str], run_id: Any, section: str, where: str, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append(f"{where} must be an object")
        return
    _unknown_keys(item, keys, where, errors)
    _require_keys(item, keys, where, errors)
    if not isinstance(item.get("id"), str) or not ID_RE.fullmatch(item.get("id", "")):
        errors.append(f"{where}.id is invalid")
    _validate_run_path(item.get("path"), run_id, section, where, errors)
    if not isinstance(item.get("sha256"), str) or not HASH_RE.fullmatch(item.get("sha256", "")):
        errors.append(f"{where}.sha256 must be canonical sha256")
    if section == "evidence" and item.get("redacted") is not True:
        errors.append(f"{where}.redacted must be true")


def _validate_artifacts(artifacts: Any, run_id: Any, errors: list[str]) -> None:
    if not isinstance(artifacts, dict):
        errors.append("artifacts must be an object")
        return
    _unknown_keys(artifacts, ARTIFACT_KEYS, "artifacts", errors)
    _require_keys(artifacts, ARTIFACT_KEYS, "artifacts", errors)
    for key, section, ref_keys in (
        ("findings", "findings", FINDING_ARTIFACT_KEYS),
        ("evidence", "evidence", EVIDENCE_ARTIFACT_KEYS),
    ):
        values = artifacts.get(key)
        if not isinstance(values, list):
            errors.append(f"artifacts.{key} must be a list")
            continue
        seen_ids: set[str] = set()
        for idx, item in enumerate(values):
            where = f"artifacts.{key}[{idx}]"
            _validate_artifact_ref(item, ref_keys, run_id, section, where, errors)
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                if item["id"] in seen_ids:
                    errors.append(f"{where}.id is duplicate")
                else:
                    seen_ids.add(item["id"])


def _validate_review(review: Any, errors: list[str]) -> None:
    if not isinstance(review, dict):
        errors.append("review must be an object")
        return
    _unknown_keys(review, REVIEW_KEYS, "review", errors)
    _require_keys(review, REVIEW_KEYS, "review", errors)
    if review.get("manual_verification_required") is not True:
        errors.append("review.manual_verification_required must be true")
    if review.get("scanner_output_only") is not True:
        errors.append("review.scanner_output_only must be true")
    if review.get("agent_review_status") not in AGENT_REVIEW_STATUSES:
        errors.append("review.agent_review_status is unsupported")


def validate_run(data: Any) -> ValidationResult:
    result = ValidationResult(document_type="run")
    errors = result.errors
    if not isinstance(data, dict):
        errors.append("run must be an object")
        return result.allow_if_clean()

    _unknown_keys(data, RUN_TOP_KEYS, "run", errors)
    _require_keys(data, RUN_TOP_KEYS, "run", errors)
    if data.get("schema_version") != "run/1.0":
        errors.append("schema_version must be run/1.0")
    run_id = data.get("run_id")
    if not isinstance(run_id, str) or not RUN_ID_RE.fullmatch(run_id):
        errors.append("run_id is invalid")
    if not isinstance(data.get("created_at_utc"), str) or not UTC_RE.fullmatch(data.get("created_at_utc", "")):
        errors.append("created_at_utc must be UTC timestamp")
    completed = data.get("completed_at_utc")
    if completed is not None and (not isinstance(completed, str) or not UTC_RE.fullmatch(completed)):
        errors.append("completed_at_utc must be UTC timestamp or null")
    if data.get("status") not in RUN_STATUSES:
        errors.append("status is unsupported")

    _validate_program(data.get("program"), errors)
    _validate_target(data.get("target"), "target", errors)
    _validate_policy(data.get("policy"), run_id, errors)
    _validate_execution(data.get("execution"), data.get("policy"), errors)
    _validate_modules(data.get("modules"), errors)
    _validate_artifacts(data.get("artifacts"), run_id, errors)
    _validate_review(data.get("review"), errors)
    return result.allow_if_clean()


def _artifact_map(run: dict[str, Any], kind: str) -> dict[str, dict[str, Any]]:
    artifacts = run.get("artifacts") if isinstance(run.get("artifacts"), dict) else {}
    values = artifacts.get(kind) if isinstance(artifacts, dict) else []
    if not isinstance(values, list):
        return {}
    return {item["id"]: item for item in values if isinstance(item, dict) and isinstance(item.get("id"), str)}


def validate_run_bundle(run: Any, findings: list[Any], evidence_items: list[Any]) -> ValidationResult:
    result = ValidationResult(document_type="run_bundle")
    run_result = validate_run(run)
    result.errors.extend(f"run: {error}" for error in run_result.errors)

    finding_validator = _load_finding_validator()
    finding_artifacts = _artifact_map(run, "findings") if isinstance(run, dict) else {}
    evidence_artifacts = _artifact_map(run, "evidence") if isinstance(run, dict) else {}
    module_ids = {
        item.get("module_id")
        for item in run.get("modules", [])
        if isinstance(run, dict) and isinstance(item, dict) and isinstance(item.get("module_id"), str)
    } if isinstance(run, dict) else set()

    run_id = run.get("run_id") if isinstance(run, dict) else None
    target = run.get("target") if isinstance(run, dict) else None
    policy_sha = run.get("policy", {}).get("decision_sha256") if isinstance(run, dict) and isinstance(run.get("policy"), dict) else None

    for idx, finding in enumerate(findings):
        validation = finding_validator.validate_data(finding, "finding")
        result.errors.extend(f"finding[{idx}]: {error}" for error in validation.errors)
        if not isinstance(finding, dict):
            continue
        finding_id = finding.get("id")
        source = finding.get("source") if isinstance(finding.get("source"), dict) else {}
        if source.get("run_id") != run_id:
            result.errors.append(f"finding[{idx}].source.run_id must match run.run_id")
        if source.get("policy_decision_sha256") != policy_sha:
            result.errors.append(f"finding[{idx}].source.policy_decision_sha256 must match run.policy.decision_sha256")
        if source.get("module_id") not in module_ids:
            result.errors.append(f"finding[{idx}].source.module_id is not declared in run.modules")
        if finding.get("target") != target:
            result.errors.append(f"finding[{idx}].target must match run.target")
        artifact = finding_artifacts.get(finding_id)
        if artifact is None:
            result.errors.append(f"finding id {finding_id!r} is not declared in run artifacts")
        single_bundle_validation = finding_validator.validate_bundle(finding, evidence_items)
        result.errors.extend(f"finding[{idx}]_evidence_bundle: {error}" for error in single_bundle_validation.errors)

    for idx, evidence in enumerate(evidence_items):
        validation = finding_validator.validate_data(evidence, "evidence")
        result.errors.extend(f"evidence[{idx}]: {error}" for error in validation.errors)
        if not isinstance(evidence, dict):
            continue
        evidence_id = evidence.get("id")
        source = evidence.get("source") if isinstance(evidence.get("source"), dict) else {}
        if source.get("run_id") != run_id:
            result.errors.append(f"evidence[{idx}].source.run_id must match run.run_id")
        if source.get("module_id") not in module_ids:
            result.errors.append(f"evidence[{idx}].source.module_id is not declared in run.modules")
        if evidence.get("target") != target:
            result.errors.append(f"evidence[{idx}].target must match run.target")
        artifact = evidence_artifacts.get(evidence_id)
        if artifact is None:
            result.errors.append(f"evidence id {evidence_id!r} is not declared in run artifacts")
            continue
        storage = evidence.get("storage") if isinstance(evidence.get("storage"), dict) else {}
        if artifact.get("sha256") != storage.get("sha256"):
            result.errors.append(f"evidence id {evidence_id!r} sha256 must match run artifact declaration")
        if artifact.get("redacted") is not True or storage.get("redacted") is not True:
            result.errors.append(f"evidence id {evidence_id!r} must be redacted")

    return result.allow_if_clean()


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    parser = argparse.ArgumentParser(description="Validate Hacklab run manifest metadata")
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--finding", type=Path, action="append", default=[])
    parser.add_argument("--evidence", type=Path, action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        run = _load_json(args.run)
        findings = [_load_json(path) for path in args.finding]
        evidence = [_load_json(path) for path in args.evidence]
        if findings or evidence:
            result = validate_run_bundle(run, findings, evidence)
        else:
            result = validate_run(run)
    except Exception as exc:  # keep CLI default-deny on IO/parse ambiguity
        result = ValidationResult(document_type="run", errors=[f"load failed: {exc}"]).allow_if_clean()

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
