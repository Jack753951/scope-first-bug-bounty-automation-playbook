#!/usr/bin/env python3
"""Dry-run-only module runner skeleton for Hacklab modules.

This P2-8 runner intentionally does not execute module code, scanners, probes,
child processes, callbacks, or network activity. It only validates module
manifests, a data-driven repo-local module profile, and a policy allow artifact,
then emits a planned run/1.0 manifest preview plus stable profile error codes
suitable for later review.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import importlib.util
import json
import re
import shutil
import sys

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


def _load_script_module(name: str):
    module_path = Path(__file__).resolve().with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


profile_issues = _load_script_module("profile_issues")

RUNNER_NAME = "hacklab-module-runner"
RUNNER_PRODUCER_NAME = "module_runner"
RUNNER_VERSION = "0.1.0"
RUN_SCHEMA_VERSION = "run/1.0"
POLICY_BOUNDARY_SCHEMA_VERSION = "policy_boundary/1.0"
POLICY_DECISION_SCHEMA_VERSION = "policy_decision/1.0"
SUPPORTED_MODE = "dry-run"
TARGET_TYPES = {"url", "domain", "ip", "cidr"}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


IssueDetail = profile_issues.IssueDetail
PROFILE_ID_INVALID = profile_issues.PROFILE_ID_INVALID
PROFILE_NOT_FOUND = profile_issues.PROFILE_NOT_FOUND
PROFILE_PATH_INVALID = profile_issues.PROFILE_PATH_INVALID
PROFILE_READ_ERROR = profile_issues.PROFILE_READ_ERROR
PROFILE_MALFORMED_JSON = profile_issues.PROFILE_MALFORMED_JSON
PROFILE_SCHEMA_INVALID = profile_issues.PROFILE_SCHEMA_INVALID
PROFILE_ID_MISMATCH = profile_issues.PROFILE_ID_MISMATCH
PROFILE_MEMBERSHIP_MISMATCH = profile_issues.PROFILE_MEMBERSHIP_MISMATCH
PROFILE_CONSTRAINT_MODE = profile_issues.PROFILE_CONSTRAINT_MODE
PROFILE_CONSTRAINT_RISK = profile_issues.PROFILE_CONSTRAINT_RISK
PROFILE_CONSTRAINT_TARGET_TYPE = profile_issues.PROFILE_CONSTRAINT_TARGET_TYPE
PROFILE_CONSTRAINT_TECHNIQUE_TAG = profile_issues.PROFILE_CONSTRAINT_TECHNIQUE_TAG
PROFILE_CONSTRAINT_EXECUTION = profile_issues.PROFILE_CONSTRAINT_EXECUTION
PROFILE_CONSTRAINT_OUTPUT = profile_issues.PROFILE_CONSTRAINT_OUTPUT
PROFILE_CONSTRAINT_SAFETY_GATE = profile_issues.PROFILE_CONSTRAINT_SAFETY_GATE
PROFILE_EMPTY_SELECTION = profile_issues.PROFILE_EMPTY_SELECTION


def _codes(details: list[IssueDetail]) -> list[str]:
    return profile_issues.issue_codes(details)


@dataclass
class RunnerResult:
    verdict: str = "deny"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error_details: list[IssueDetail] = field(default_factory=list)
    warning_details: list[IssueDetail] = field(default_factory=list)
    plan: dict[str, Any] | None = None
    module_input_previews: list[dict[str, Any]] = field(default_factory=list)
    module_result_previews: list[dict[str, Any]] = field(default_factory=list)
    preview_manifest: dict[str, Any] | None = None

    @property
    def error_codes(self) -> list[str]:
        return _codes(self.error_details)

    @property
    def warning_codes(self) -> list[str]:
        return _codes(self.warning_details)

    def allow_if_clean(self) -> "RunnerResult":
        self.verdict = "deny" if self.errors else "allow"
        return self

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": "module_runner_plan/1.0",
            "verdict": self.verdict,
            "errors": self.errors,
            "warnings": self.warnings,
            "error_codes": self.error_codes,
            "warning_codes": self.warning_codes,
            "error_details": [issue.as_dict() for issue in self.error_details],
            "warning_details": [issue.as_dict() for issue in self.warning_details],
        }
        if self.plan is not None:
            payload["plan"] = self.plan
        if self.module_input_previews:
            payload["module_input_previews"] = self.module_input_previews
        if self.module_result_previews:
            payload["module_result_previews"] = self.module_result_previews
        if self.preview_manifest is not None:
            payload["preview_manifest"] = self.preview_manifest
        return payload


@dataclass
class ModuleDiscoveryResult:
    verdict: str = "deny"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error_details: list[IssueDetail] = field(default_factory=list)
    warning_details: list[IssueDetail] = field(default_factory=list)
    manifest_paths: list[Path] = field(default_factory=list)
    modules: list[dict[str, Any]] = field(default_factory=list)

    @property
    def error_codes(self) -> list[str]:
        return _codes(self.error_details)

    @property
    def warning_codes(self) -> list[str]:
        return _codes(self.warning_details)

    def allow_if_clean(self) -> "ModuleDiscoveryResult":
        self.verdict = "deny" if self.errors else "allow"
        if self.errors:
            self.manifest_paths = []
            self.modules = []
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "module_discovery/1.0",
            "verdict": self.verdict,
            "errors": self.errors,
            "warnings": self.warnings,
            "error_codes": self.error_codes,
            "warning_codes": self.warning_codes,
            "error_details": [issue.as_dict() for issue in self.error_details],
            "warning_details": [issue.as_dict() for issue in self.warning_details],
            "manifest_paths": [str(path) for path in self.manifest_paths],
            "modules": self.modules,
        }


validate_module_manifest = _load_script_module("validate_module_manifest")
validate_module_profile = _load_script_module("validate_module_profile")
validate_run_manifest = _load_script_module("validate_run_manifest")
validate_module_io_contract = _load_script_module("validate_module_io_contract")
validate_module_io_bundle = _load_script_module("validate_module_io_bundle")


def _add_issue(
    errors: list[str],
    details: list[IssueDetail] | None,
    code: str,
    message: str,
    *,
    component: str = "module_profile",
    path: Path | str | None = None,
    field: str | None = None,
    profile_id: str | None = None,
    module_id: str | None = None,
) -> None:
    profile_issues.add_issue(
        errors,
        details,
        code,
        message,
        component=component,
        path=path,
        field=field,
        profile_id=profile_id,
        module_id=module_id,
    )


def _add_warning(
    warnings: list[str],
    details: list[IssueDetail] | None,
    code: str,
    message: str,
    *,
    component: str = "module_profile",
    path: Path | str | None = None,
    field: str | None = None,
    profile_id: str | None = None,
    module_id: str | None = None,
) -> None:
    profile_issues.add_warning(
        warnings,
        details,
        code,
        message,
        component=component,
        path=path,
        field=field,
        profile_id=profile_id,
        module_id=module_id,
    )


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: str | Path) -> str:
    return sha256(Path(path).read_bytes()).hexdigest()


def _load_json_file(
    path: Path,
    label: str,
    errors: list[str],
    error_details: list[IssueDetail] | None = None,
    *,
    component: str | None = None,
    profile_id: str | None = None,
) -> Any | None:
    issue_component = component or label.replace(" ", "_")
    if not path.exists():
        message = f"{label} not found: {path}"
        code = PROFILE_NOT_FOUND if label == "module profile" else PROFILE_READ_ERROR
        _add_issue(errors, error_details, code, message, component=issue_component, path=path, profile_id=profile_id)
        return None
    if not path.is_file():
        message = f"{label} is not a file: {path}"
        code = PROFILE_PATH_INVALID if label == "module profile" else PROFILE_READ_ERROR
        _add_issue(errors, error_details, code, message, component=issue_component, path=path, profile_id=profile_id)
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        message = f"{label} is not valid JSON: {exc}"
        code = PROFILE_MALFORMED_JSON if label == "module profile" else PROFILE_READ_ERROR
        _add_issue(errors, error_details, code, message, component=issue_component, path=path, profile_id=profile_id)
        return None
    except OSError as exc:
        message = f"{label} could not be read: {exc}"
        _add_issue(errors, error_details, PROFILE_READ_ERROR, message, component=issue_component, path=path, profile_id=profile_id)
        return None


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _module_checks_root(repo_root: Path) -> Path:
    return repo_root.resolve() / "modules" / "checks"


def _module_profiles_root(repo_root: Path) -> Path:
    return repo_root.resolve() / "modules" / "profiles"



def load_module_profile(
    repo_root: str | Path,
    profile: str,
    errors: list[str],
    error_details: list[IssueDetail] | None = None,
) -> tuple[Path | None, dict[str, Any] | None]:
    """Load and validate one repo-local module profile by ID.

    Profile IDs resolve only to modules/profiles/<profile>.json under the
    supplied repository root. Missing, malformed, path-escaping, or unsafe
    profile files append errors and return None.
    """
    repo = Path(repo_root).resolve()
    profiles_root = _module_profiles_root(repo)
    if not isinstance(profile, str) or not validate_module_profile.ID_RE.fullmatch(profile):
        _add_issue(errors, error_details, PROFILE_ID_INVALID, "module profile id is invalid", component="module_profile_loader", profile_id=str(profile))
        return None, None
    profile_path = (profiles_root / f"{profile}.json").resolve()
    if not _is_relative_to(profile_path, profiles_root):
        message = f"module profile path must stay under modules/profiles: {profile_path}"
        _add_issue(errors, error_details, PROFILE_PATH_INVALID, message, component="module_profile_loader", path=profile_path, profile_id=profile)
        return None, None
    data = _load_json_file(profile_path, "module profile", errors, error_details, component="module_profile_loader", profile_id=profile)
    if data is None:
        return None, None
    validation = validate_module_profile.validate_module_profile(data)
    if validation.verdict != "allow":
        for error in validation.errors:
            message = f"module profile {profile_path}: {error}"
            _add_issue(errors, error_details, PROFILE_SCHEMA_INVALID, message, component="module_profile_validator", path=profile_path, profile_id=profile)
        return profile_path, None
    if data.get("profile_id") != profile:
        message = f"module profile {profile_path}: profile_id must match requested profile {profile}"
        _add_issue(errors, error_details, PROFILE_ID_MISMATCH, message, component="module_profile_loader", path=profile_path, field="profile.profile_id", profile_id=profile)
        return profile_path, None
    return profile_path, data


def _profile_allows_manifest(
    manifest: dict[str, Any],
    profile_data: dict[str, Any],
    *,
    target_type: str | None,
    mode: str,
    manifest_path: Path,
    errors: list[str],
    skip_non_member: bool,
    error_details: list[IssueDetail] | None = None,
    warnings: list[str] | None = None,
    warning_details: list[IssueDetail] | None = None,
) -> bool:
    profile_id = profile_data["profile_id"]
    module_id = manifest.get("module_id")
    execution = manifest.get("execution", {})
    default_profile = execution.get("default_profile")
    if default_profile != profile_id:
        message = f"module manifest {manifest_path}: default_profile must match selected profile {profile_id}"
        if skip_non_member:
            if warnings is not None:
                _add_warning(warnings, warning_details, PROFILE_MEMBERSHIP_MISMATCH, message, component="module_profile_selector", path=manifest_path, field="execution.default_profile", profile_id=profile_id, module_id=module_id)
            return False
        _add_issue(errors, error_details, PROFILE_MEMBERSHIP_MISMATCH, message, component="module_profile_selector", path=manifest_path, field="execution.default_profile", profile_id=profile_id, module_id=module_id)
        return False

    if mode not in profile_data.get("mode_allowlist", []):
        message = f"module manifest {manifest_path}: mode {mode} is not allowed by profile {profile_id}"
        _add_issue(errors, error_details, PROFILE_CONSTRAINT_MODE, message, component="module_profile_selector", path=manifest_path, field="mode", profile_id=profile_id, module_id=module_id)
    risk_level = manifest.get("risk_level")
    if risk_level not in profile_data.get("risk_level_allowlist", []):
        message = f"module manifest {manifest_path}: risk_level {risk_level} is not allowed by profile {profile_id}"
        _add_issue(errors, error_details, PROFILE_CONSTRAINT_RISK, message, component="module_profile_selector", path=manifest_path, field="risk_level", profile_id=profile_id, module_id=module_id)
    if target_type is not None and target_type not in profile_data.get("target_type_allowlist", []):
        message = f"module manifest {manifest_path}: target_type {target_type} is not allowed by profile {profile_id}"
        _add_issue(errors, error_details, PROFILE_CONSTRAINT_TARGET_TYPE, message, component="module_profile_selector", path=manifest_path, field="target_type", profile_id=profile_id, module_id=module_id)
    if target_type is not None and target_type not in manifest.get("target_types", []):
        message = f"module manifest {manifest_path}: target type {target_type} is not supported"
        if skip_non_member:
            if warnings is not None:
                _add_warning(warnings, warning_details, PROFILE_CONSTRAINT_TARGET_TYPE, message, component="module_profile_selector", path=manifest_path, field="target_types", profile_id=profile_id, module_id=module_id)
            return False
        _add_issue(errors, error_details, PROFILE_CONSTRAINT_TARGET_TYPE, message, component="module_profile_selector", path=manifest_path, field="target_types", profile_id=profile_id, module_id=module_id)

    allowed_targets = set(profile_data.get("target_type_allowlist", []))
    for item in manifest.get("target_types", []):
        if item not in allowed_targets:
            message = f"module manifest {manifest_path}: target_type {item} is not allowed by profile {profile_id}"
            _add_issue(errors, error_details, PROFILE_CONSTRAINT_TARGET_TYPE, message, component="module_profile_selector", path=manifest_path, field="target_types", profile_id=profile_id, module_id=module_id)
    allowed_tags = set(profile_data.get("technique_tag_allowlist", []))
    for tag in manifest.get("technique_tags", []):
        if tag not in allowed_tags:
            message = f"module manifest {manifest_path}: technique_tag {tag} is not allowed by profile {profile_id}"
            _add_issue(errors, error_details, PROFILE_CONSTRAINT_TECHNIQUE_TAG, message, component="module_profile_selector", path=manifest_path, field="technique_tags", profile_id=profile_id, module_id=module_id)

    constraints = profile_data.get("execution_constraints", {})
    for key in ("supports_dry_run", "requires_network", "network_access", "target_touching", "destructive", "intrusive"):
        if execution.get(key) != constraints.get(key):
            message = f"module manifest {manifest_path}: execution.{key} violates profile {profile_id}"
            _add_issue(errors, error_details, PROFILE_CONSTRAINT_EXECUTION, message, component="module_profile_selector", path=manifest_path, field=f"execution.{key}", profile_id=profile_id, module_id=module_id)

    output = manifest.get("output_contracts", {})
    output_constraints = profile_data.get("output_constraints", {})
    if output.get("emits_findings") is True and output_constraints.get("emits_findings_allowed") is not True:
        message = f"module manifest {manifest_path}: emits_findings is not allowed by profile {profile_id}"
        _add_issue(errors, error_details, PROFILE_CONSTRAINT_OUTPUT, message, component="module_profile_selector", path=manifest_path, field="output_contracts.emits_findings", profile_id=profile_id, module_id=module_id)
    if output.get("emits_evidence") is True and output_constraints.get("emits_evidence_allowed") is not True:
        message = f"module manifest {manifest_path}: emits_evidence is not allowed by profile {profile_id}"
        _add_issue(errors, error_details, PROFILE_CONSTRAINT_OUTPUT, message, component="module_profile_selector", path=manifest_path, field="output_contracts.emits_evidence", profile_id=profile_id, module_id=module_id)

    gates = manifest.get("safety_gates", {})
    for gate in profile_data.get("required_safety_gates_true", []):
        if gates.get(gate) is not True:
            message = f"module manifest {manifest_path}: safety_gates.{gate} must be true for profile {profile_id}"
            _add_issue(errors, error_details, PROFILE_CONSTRAINT_SAFETY_GATE, message, component="module_profile_selector", path=manifest_path, field=f"safety_gates.{gate}", profile_id=profile_id, module_id=module_id)
    for gate in profile_data.get("required_safety_gates_false", []):
        if gates.get(gate) is not False:
            message = f"module manifest {manifest_path}: safety_gates.{gate} must be false for profile {profile_id}"
            _add_issue(errors, error_details, PROFILE_CONSTRAINT_SAFETY_GATE, message, component="module_profile_selector", path=manifest_path, field=f"safety_gates.{gate}", profile_id=profile_id, module_id=module_id)

    return True

def _candidate_manifest_paths(repo_root: Path, manifest_paths: list[str | Path] | None, errors: list[str]) -> list[Path]:
    checks_root = _module_checks_root(repo_root)
    if manifest_paths is None:
        if not checks_root.exists():
            errors.append(f"modules/checks root not found: {checks_root}")
            return []
        return sorted(path.resolve() for path in checks_root.rglob("module.json") if path.is_file())
    return sorted(Path(path).resolve() for path in manifest_paths)


def discover_profile_manifests(
    *,
    repo_root: str | Path,
    profile: str = "audit-baseline",
    target_type: str | None = None,
    mode: str = SUPPORTED_MODE,
    manifest_paths: list[str | Path] | None = None,
) -> ModuleDiscoveryResult:
    """Discover repo-local module manifests and select dry-run-safe profile members.

    This helper reads JSON manifests and profile data only. It does not import
    module code, launch subprocesses, open sockets, touch targets, or emit
    findings/evidence.
    """
    result = ModuleDiscoveryResult()
    errors = result.errors
    repo = Path(repo_root).resolve()
    checks_root = _module_checks_root(repo)

    profile_path, profile_data = load_module_profile(repo, profile, errors, result.error_details)
    if mode != SUPPORTED_MODE:
        errors.append("module discovery supports dry-run mode only")
    if target_type is not None and target_type not in TARGET_TYPES:
        errors.append("target_type is unsupported")

    candidates = _candidate_manifest_paths(repo, manifest_paths, errors)
    seen_module_ids: set[str] = set()
    selected: list[tuple[Path, dict[str, Any]]] = []

    for manifest_path in candidates:
        if not _is_relative_to(manifest_path, checks_root):
            errors.append(f"module manifest path must stay under modules/checks: {manifest_path}")
            continue
        if manifest_path.name != "module.json":
            errors.append(f"module manifest path must be named module.json: {manifest_path}")
            continue

        manifest = _load_json_file(manifest_path, "module manifest", errors)
        if manifest is None:
            continue
        validation = validate_module_manifest.validate_module_manifest(manifest)
        if validation.verdict != "allow":
            for error in validation.errors:
                errors.append(f"module manifest {manifest_path}: {error}")
            continue

        module_id = manifest["module_id"]
        if module_id in seen_module_ids:
            errors.append(f"module manifest {manifest_path}: duplicate module_id {module_id}")
            continue
        seen_module_ids.add(module_id)

        if profile_data is None:
            continue
        if not _profile_allows_manifest(
            manifest,
            profile_data,
            target_type=target_type,
            mode=mode,
            manifest_path=manifest_path,
            errors=errors,
            skip_non_member=True,
            error_details=result.error_details,
            warnings=result.warnings,
            warning_details=result.warning_details,
        ):
            continue
        selected.append((manifest_path, manifest))

    if not candidates and not errors:
        errors.append("no module manifests discovered under modules/checks")
    if not selected and not errors:
        _add_issue(
            errors,
            result.error_details,
            PROFILE_EMPTY_SELECTION,
            f"no module manifests selected for profile {profile}",
            component="module_profile_selector",
            profile_id=profile,
        )

    if errors:
        return result.allow_if_clean()

    result.manifest_paths = [path for path, _manifest in selected]
    result.modules = [
        {
            "module_id": manifest["module_id"],
            "path": str(path),
            "profile": manifest["execution"]["default_profile"],
            "profile_sha256": sha256_file(profile_path) if profile_path is not None else "",
            "requires_network": manifest["execution"]["requires_network"],
            "network_access": manifest["execution"]["network_access"],
            "target_touching": manifest["execution"]["target_touching"],
        }
        for path, manifest in selected
    ]
    return result.allow_if_clean()


def _validate_policy_artifact(
    policy_artifact: Any,
    *,
    target_value: str,
    target_type: str,
    mode: str,
    errors: list[str],
) -> dict[str, Any] | None:
    if not isinstance(policy_artifact, dict):
        errors.append("policy artifact must be a JSON object")
        return None
    if policy_artifact.get("schema_version") != POLICY_BOUNDARY_SCHEMA_VERSION:
        errors.append(f"policy artifact schema_version must be {POLICY_BOUNDARY_SCHEMA_VERSION}")

    boundary = policy_artifact.get("boundary")
    if not isinstance(boundary, dict):
        errors.append("policy artifact boundary must be an object")
    else:
        if boundary.get("status") != "allow":
            errors.append("policy artifact boundary.status must be allow")
        if boundary.get("audit_event") != "PROGRAM_POLICY_ALLOW":
            errors.append("policy artifact boundary.audit_event must be PROGRAM_POLICY_ALLOW")
        for key in ("errors", "contract_errors", "boundary_errors", "deny_reason_codes"):
            value = boundary.get(key, [])
            if value:
                errors.append(f"policy artifact boundary.{key} must be empty for allow")

    helper = policy_artifact.get("helper")
    if not isinstance(helper, dict):
        errors.append("policy artifact helper must be an object")
    else:
        if helper.get("timed_out") is not False:
            errors.append("policy artifact helper.timed_out must be false for allow")
        if helper.get("returncode") != 0:
            errors.append("policy artifact helper.returncode must be 0 for allow")

    request = policy_artifact.get("request")
    if not isinstance(request, dict):
        errors.append("policy artifact request must be an object")
    else:
        if request.get("target") != target_value:
            errors.append("policy artifact request.target must match requested target")
        if request.get("mode") != mode:
            errors.append("policy artifact request.mode must match requested mode")

    decision = policy_artifact.get("decision")
    if not isinstance(decision, dict):
        errors.append("policy artifact decision must be an object")
        return None
    if decision.get("schema_version") != POLICY_DECISION_SCHEMA_VERSION:
        errors.append(f"policy decision schema_version must be {POLICY_DECISION_SCHEMA_VERSION}")
    if decision.get("verdict") != "allow":
        errors.append("policy decision verdict must be allow")
    if decision.get("audit_event") != "PROGRAM_POLICY_ALLOW":
        errors.append("policy decision audit_event must be PROGRAM_POLICY_ALLOW")
    if decision.get("target") != target_value:
        errors.append("policy decision target must match requested target")
    if decision.get("target_type") != target_type:
        errors.append("policy decision target_type must match requested target_type")
    if decision.get("mode") != mode:
        errors.append("policy decision mode must match requested mode")
    for key in ("errors", "deny_reason_codes"):
        value = decision.get(key, [])
        if value:
            errors.append(f"policy decision {key} must be empty for allow")
    for key in ("warnings", "reasons"):
        value = decision.get(key, [])
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            errors.append(f"policy decision {key} must be a list of strings")
    for key in ("program_slug", "target_type", "program_file_sha256", "global_scope_sha256", "decided_at_utc"):
        if not isinstance(decision.get(key), str) or not decision.get(key):
            errors.append(f"policy decision {key} must be a non-empty string")
    for key in ("program_file_sha256", "global_scope_sha256"):
        if isinstance(decision.get(key), str) and not HASH_RE.fullmatch(decision[key]):
            errors.append(f"policy decision {key} must be canonical sha256")
    if isinstance(decision.get("decided_at_utc"), str) and not UTC_RE.fullmatch(decision["decided_at_utc"]):
        errors.append("policy decision decided_at_utc must be UTC timestamp")
    return decision


def _repo_local_policy_artifact_path(
    policy_path: Path,
    *,
    run_id: str,
    repo_root: str | Path,
    errors: list[str],
) -> str:
    """Classify an explicit policy artifact path and return its repo-relative path.

    The runner accepts only explicit policy artifacts. It never auto-discovers,
    copies, or normalizes recon outputs into run directories. Allowed shapes are:
    - runs/<run_id>/policy/<file>
    - scans/<scan-dir>/evidence/policy/policy_boundary_*.json
    """
    repo_input = Path(repo_root)
    if repo_input.exists() and repo_input.is_symlink():
        errors.append("policy artifact repository root must not be a symlink")
        return f"runs/{run_id}/policy/decision.json"

    repo = repo_input.resolve(strict=False)
    raw_path = Path(policy_path)
    lexical_path = raw_path if raw_path.is_absolute() else (repo / raw_path)
    if any(part == ".." for part in lexical_path.parts):
        errors.append("policy artifact path must not contain traversal segments")
    resolved_path = lexical_path.resolve(strict=False)

    if not _is_relative_to(resolved_path, repo):
        errors.append("policy artifact path must stay under the selected repository root")
        return f"runs/{run_id}/policy/decision.json"
    if raw_path.exists() and raw_path.is_symlink():
        errors.append("policy artifact file must not be a symlink")
    if _lexical_parent_is_symlink(lexical_path, repo) or _existing_parent_is_symlink(resolved_path, repo):
        errors.append("policy artifact path must not traverse symlinked parent directories")
    if resolved_path.exists() and not resolved_path.is_file():
        errors.append("policy artifact path must be a regular file")

    try:
        rel_parts = resolved_path.relative_to(repo).parts
    except ValueError:
        errors.append("policy artifact path must stay under the selected repository root")
        return f"runs/{run_id}/policy/decision.json"

    if len(rel_parts) == 4 and rel_parts[0] == "runs" and rel_parts[2] == "policy":
        if rel_parts[1] != run_id:
            errors.append("policy artifact runs path must match run_id")
        return "/".join(rel_parts)

    if rel_parts and rel_parts[0] == "runs":
        errors.append("policy artifact path must be under runs/<run_id>/policy/<file> and match run_id")
        return f"runs/{run_id}/policy/decision.json"

    if len(rel_parts) == 5 and rel_parts[0] == "scans" and rel_parts[2:4] == ("evidence", "policy"):
        scan_dir = rel_parts[1]
        filename = rel_parts[4]
        if not scan_dir or scan_dir in {".", ".."} or "/" in scan_dir or "\\" in scan_dir:
            errors.append("policy artifact scans path must include one safe scan directory segment")
        if not re.fullmatch(r"policy_boundary_[A-Za-z0-9_.-]+\.json", filename):
            errors.append("recon evidence policy artifact filename must match policy_boundary_*.json")
        return "/".join(rel_parts)

    if rel_parts and rel_parts[0] == "scans":
        errors.append("recon evidence policy artifact path must be scans/<scan-dir>/evidence/policy/policy_boundary_*.json")
    else:
        errors.append("policy artifact path must be under runs/<run_id>/policy/<file> or scans/<scan-dir>/evidence/policy/policy_boundary_*.json")
    return f"runs/{run_id}/policy/decision.json"


def _load_and_validate_manifests(
    manifest_paths: list[Path],
    *,
    target_type: str,
    mode: str,
    profile_data: dict[str, Any] | None,
    errors: list[str],
    error_details: list[IssueDetail] | None = None,
) -> list[tuple[Path, dict[str, Any]]]:
    manifests: list[tuple[Path, dict[str, Any]]] = []
    seen_module_ids: set[str] = set()
    if not manifest_paths:
        errors.append("at least one module manifest is required")
        return manifests
    for manifest_path in manifest_paths:
        manifest = _load_json_file(manifest_path, "module manifest", errors)
        if manifest is None:
            continue
        validation = validate_module_manifest.validate_module_manifest(manifest)
        if validation.verdict != "allow":
            for error in validation.errors:
                errors.append(f"module manifest {manifest_path}: {error}")
            continue
        module_id = manifest.get("module_id")
        if module_id in seen_module_ids:
            errors.append(f"module manifest {manifest_path}: duplicate module_id {module_id}")
        else:
            seen_module_ids.add(module_id)
        if profile_data is None:
            continue
        _profile_allows_manifest(
            manifest,
            profile_data,
            target_type=target_type,
            mode=mode,
            manifest_path=manifest_path,
            errors=errors,
            skip_non_member=False,
            error_details=error_details,
        )
        manifests.append((manifest_path, manifest))
    return manifests


def build_module_io_previews(
    *,
    plan: dict[str, Any],
    manifests: list[tuple[Path, dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Build P2-10 preview-only module I/O envelopes from already-validated data.

    This helper constructs JSON data only. It must not import module code, spawn
    subprocesses, open network connections, touch targets, or create findings,
    evidence, reports, callbacks, or loot.
    """

    errors: list[str] = []
    input_previews: list[dict[str, Any]] = []
    result_previews: list[dict[str, Any]] = []

    for manifest_path, manifest in manifests:
        module_id = manifest["module_id"]
        module_input = {
            "schema_version": "module_input/1.0",
            "run": {
                "run_id": plan["run_id"],
                "mode": plan["policy"]["mode"],
                "dry_run": plan["execution"]["dry_run"],
                "runner": plan["execution"]["runner"],
                "created_at_utc": plan["created_at_utc"],
            },
            "program": deepcopy(plan["program"]),
            "target": deepcopy(plan["target"]),
            "policy": {
                "decision": plan["policy"]["decision"],
                "decision_artifact_path": plan["policy"]["decision_artifact_path"],
                "decision_sha256": plan["policy"]["decision_sha256"],
                "checked_at_utc": plan["policy"]["checked_at_utc"],
            },
            "profile": {
                "profile_id": plan["execution"]["profile_id"],
                "profile_sha256": plan["execution"]["profile_sha256"],
            },
            "module": {
                "module_id": module_id,
                "module_version": manifest["version"],
                "manifest_sha256": sha256_file(manifest_path),
                "risk_level": manifest["risk_level"],
                "target_types": list(manifest["target_types"]),
                "technique_tags": list(manifest["technique_tags"]),
            },
            "constraints": {
                "supports_dry_run": manifest["execution"]["supports_dry_run"],
                "requires_network": manifest["execution"]["requires_network"],
                "network_access": manifest["execution"]["network_access"],
                "target_touching": manifest["execution"]["target_touching"],
                "destructive": manifest["execution"]["destructive"],
                "intrusive": manifest["execution"]["intrusive"],
                "emits_findings": manifest["output_contracts"]["emits_findings"],
                "emits_evidence": manifest["output_contracts"]["emits_evidence"],
                "manual_verification_required": manifest["safety_gates"]["manual_verification_required"],
                "scanner_output_only": manifest["safety_gates"]["scanner_output_only"],
                "store_redacted_evidence_only": manifest["safety_gates"]["store_redacted_evidence_only"],
                "stores_raw_secrets": manifest["safety_gates"]["stores_raw_secrets"],
                "writes_to_loot": manifest["safety_gates"]["writes_to_loot"],
                "allows_destructive_actions": manifest["safety_gates"]["allows_destructive_actions"],
                "allows_oast_callbacks": manifest["safety_gates"]["allows_oast_callbacks"],
            },
            "output": {
                "module_output_dir": f"runs/{plan['run_id']}/modules/{module_id}",
                "findings": [],
                "evidence": [],
            },
        }
        module_result = {
            "schema_version": "module_result/1.0",
            "run_id": plan["run_id"],
            "module_id": module_id,
            "status": "not_executed",
            "dry_run": True,
            "target_touching": False,
            "summary": "Dry-run contract preview only; module code was not executed.",
            "findings": [],
            "evidence": [],
            "errors": [],
            "warnings": [],
        }

        input_validation = validate_module_io_contract.validate_module_input(module_input)
        if input_validation.verdict != "allow":
            errors.extend(f"module input preview {module_id}: {error}" for error in input_validation.errors)
        result_validation = validate_module_io_contract.validate_module_result(module_result)
        if result_validation.verdict != "allow":
            errors.extend(f"module result preview {module_id}: {error}" for error in result_validation.errors)
        input_previews.append(module_input)
        result_previews.append(module_result)

    return input_previews, result_previews, errors


def _is_safe_persist_run_id(run_id: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,127}", run_id)) and ".." not in run_id


def _json_bytes(payload: dict[str, Any] | list[dict[str, Any]]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _artifact_record(name: str, relative_path: str, payload: dict[str, Any] | list[dict[str, Any]]) -> tuple[dict[str, Any], bytes]:
    data = _json_bytes(payload)
    return {
        "name": name,
        "relative_path": relative_path,
        "sha256": sha256(data).hexdigest(),
        "size_bytes": len(data),
        "content_type": "application/json",
    }, data


def _existing_parent_is_symlink(path: Path, stop_at: Path) -> bool:
    current = path
    stop_at = stop_at.resolve()
    candidates: list[Path] = []
    while True:
        candidates.append(current)
        if current == stop_at or current.parent == current:
            break
        current = current.parent
    for candidate in candidates:
        if candidate.exists() and candidate.is_symlink():
            return True
    return False


def _lexical_parent_is_symlink(path: Path, stop_at: Path) -> bool:
    """Check the original, unresolved parent chain for symlink segments."""
    current = path
    stop_at = stop_at.resolve()
    candidates: list[Path] = []
    while True:
        candidates.append(current)
        try:
            if current.resolve(strict=False) == stop_at:
                break
        except OSError:
            pass
        if current.parent == current:
            break
        current = current.parent
    for candidate in candidates:
        if candidate.exists() and candidate.is_symlink():
            return True
    return False


def _remove_empty_dir(path: Path) -> None:
    try:
        path.rmdir()
    except OSError:
        pass


def persist_preview_bundle(
    *,
    repo_root: str | Path,
    run_id: str,
    plan: dict[str, Any],
    input_previews: list[dict[str, Any]],
    result_previews: list[dict[str, Any]],
    bundle_validation: Any,
) -> dict[str, Any]:
    """Persist an already-validated dry-run preview bundle under runs/<run_id>/preview.

    This helper writes data-only JSON artifacts after all runner gates have passed.
    It must not import modules, spawn processes, open network clients, touch targets,
    or emit findings/evidence beyond the empty previews already validated upstream.
    """
    if not _is_safe_persist_run_id(run_id):
        raise ValueError("preview persistence run_id must be a single safe path segment")
    if bundle_validation.verdict != "allow":
        raise ValueError("preview bundle persistence requires allow bundle validation")

    repo_input = Path(repo_root)
    if repo_input.exists() and repo_input.is_symlink():
        raise ValueError("preview persistence refuses a symlinked repository root")
    repo = repo_input.resolve()
    runs_path = repo / "runs"
    preview_path = runs_path / run_id / "preview"
    if _lexical_parent_is_symlink(preview_path, repo):
        raise ValueError("preview persistence refuses symlinked parent paths")
    runs_root = runs_path.resolve(strict=False)
    run_dir = runs_root / run_id
    preview_dir = run_dir / "preview"
    tmp_dir = run_dir / ".preview.tmp"

    if not _is_relative_to(runs_root, repo):
        raise ValueError("runs root must be inside the repository root")
    if not _is_relative_to(preview_dir.resolve(strict=False), runs_root):
        raise ValueError("preview directory must stay under runs/<run_id>")
    if _existing_parent_is_symlink(preview_dir, repo):
        raise ValueError("preview persistence refuses symlinked parent paths")
    if preview_dir.exists() or tmp_dir.exists():
        raise ValueError("preview bundle directory already exists")

    bundle_payload = bundle_validation.as_dict()
    artifact_payloads: list[tuple[str, dict[str, Any] | list[dict[str, Any]]]] = [
        ("run.json", plan),
        ("module_inputs.json", input_previews),
        ("module_results.json", result_previews),
        ("bundle_consistency.json", bundle_payload),
    ]
    artifact_records: list[dict[str, Any]] = []
    serialized: list[tuple[str, bytes]] = []
    for filename, payload in artifact_payloads:
        relative_path = f"runs/{run_id}/preview/{filename}"
        record, data = _artifact_record(filename, relative_path, payload)
        artifact_records.append(record)
        serialized.append((filename, data))

    manifest = {
        "schema_version": "preview_manifest/1.0",
        "run_id": run_id,
        "created_at_utc": utc_now(),
        "producer": {
            "name": RUNNER_PRODUCER_NAME,
            "version": RUNNER_VERSION,
        },
        "preview_mode": {
            "persist_preview_bundle": True,
            "include_module_io_preview": True,
            "dry_run": True,
        },
        "bundle_consistency": {
            "status": "ok",
            "verdict": bundle_payload["verdict"],
            "relative_path": f"runs/{run_id}/preview/bundle_consistency.json",
            "sha256": artifact_records[-1]["sha256"],
        },
        "artifacts": artifact_records,
    }
    manifest_data = _json_bytes(manifest)

    try:
        run_dir.mkdir(parents=True, exist_ok=True)
        tmp_dir.mkdir()
        for filename, data in serialized:
            (tmp_dir / filename).write_bytes(data)
        (tmp_dir / "preview_manifest.json").write_bytes(manifest_data)
        tmp_dir.rename(preview_dir)
    except Exception:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        _remove_empty_dir(run_dir)
        raise

    return manifest


def build_dry_run_plan(
    *,
    manifest_paths: list[str | Path],
    policy_artifact_path: str | Path,
    run_id: str,
    target_type: str,
    target_value: str,
    mode: str = SUPPORTED_MODE,
    profile: str = "audit-baseline",
    profile_root: str | Path = ".",
    include_module_io_preview: bool = False,
    persist_preview_bundle_root: str | Path | None = None,
) -> RunnerResult:
    result = RunnerResult()
    errors = result.errors

    if mode != SUPPORTED_MODE:
        errors.append("module runner skeleton supports dry-run mode only")
    if target_type not in TARGET_TYPES:
        errors.append("target_type is unsupported")
    if not isinstance(target_value, str) or not target_value:
        errors.append("target_value must be a non-empty string")
    if persist_preview_bundle_root is not None and not include_module_io_preview:
        errors.append("preview bundle persistence requires --include-module-io-preview")

    profile_path, profile_data = load_module_profile(profile_root, profile, errors, result.error_details)

    policy_path = Path(policy_artifact_path)
    if not policy_path.is_absolute():
        policy_path = Path(profile_root) / policy_path
    policy_run_path = _repo_local_policy_artifact_path(
        policy_path,
        run_id=run_id,
        repo_root=profile_root,
        errors=errors,
    )
    policy_artifact = _load_json_file(policy_path, "policy artifact", errors)
    decision = None

    if policy_artifact is not None:
        decision = _validate_policy_artifact(
            policy_artifact,
            target_value=target_value,
            target_type=target_type,
            mode=mode,
            errors=errors,
        )

    manifests = _load_and_validate_manifests(
        [Path(path) for path in manifest_paths],
        target_type=target_type,
        mode=mode,
        profile_data=profile_data,
        errors=errors,
        error_details=result.error_details,
    )

    if errors:
        return result.allow_if_clean()
    assert decision is not None

    created_at = utc_now()
    plan = {
        "schema_version": RUN_SCHEMA_VERSION,
        "run_id": run_id,
        "created_at_utc": created_at,
        "completed_at_utc": None,
        "status": "planned",
        "program": {
            "slug": decision["program_slug"],
            "scope_file_sha256": decision["program_file_sha256"],
            "global_scope_file_sha256": decision["global_scope_sha256"],
        },
        "target": {
            "type": target_type,
            "value": target_value,
        },
        "policy": {
            "mode": mode,
            "decision": "allow",
            "decision_artifact_path": policy_run_path,
            "decision_sha256": sha256_file(policy_path),
            "checked_at_utc": decision["decided_at_utc"],
        },
        "execution": {
            "runner": RUNNER_NAME,
            "profile": profile,
            "profile_id": profile,
            "profile_sha256": sha256_file(profile_path) if profile_path is not None else "",
            "dry_run": True,
            "target_touching": False,
        },
        "modules": [
            {
                "module_id": manifest["module_id"],
                "manifest_sha256": sha256_file(manifest_path),
                "status": "planned",
            }
            for manifest_path, manifest in manifests
        ],
        "artifacts": {
            "findings": [],
            "evidence": [],
        },
        "review": {
            "manual_verification_required": True,
            "scanner_output_only": True,
            "agent_review_status": "not_started",
        },
    }

    run_validation = validate_run_manifest.validate_run(plan)
    if run_validation.verdict != "allow":
        errors.extend(f"run plan: {error}" for error in run_validation.errors)
        return result.allow_if_clean()

    if include_module_io_preview:
        input_previews, result_previews, preview_errors = build_module_io_previews(plan=plan, manifests=manifests)
        if preview_errors:
            errors.extend(preview_errors)
            return result.allow_if_clean()
        bundle_validation = validate_module_io_bundle.build_bundle_consistency_report(
            plan,
            input_previews,
            result_previews,
        )
        if bundle_validation.verdict != "allow":
            for code, message in zip(bundle_validation.error_codes, bundle_validation.errors):
                _add_issue(
                    errors,
                    result.error_details,
                    code,
                    f"module I/O bundle: {message}",
                    component="module_io_bundle",
                )
            return result.allow_if_clean()
        result.module_input_previews = input_previews
        result.module_result_previews = result_previews
        if persist_preview_bundle_root is not None:
            try:
                result.preview_manifest = persist_preview_bundle(
                    repo_root=persist_preview_bundle_root,
                    run_id=run_id,
                    plan=plan,
                    input_previews=input_previews,
                    result_previews=result_previews,
                    bundle_validation=bundle_validation,
                )
            except Exception as exc:
                errors.append(f"preview bundle persistence failed: {exc}")
                result.preview_manifest = None
                return result.allow_if_clean()

    result.plan = plan
    return result.allow_if_clean()


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    parser = argparse.ArgumentParser(
        description="Build a dry-run-only module run manifest preview without executing modules.",
    )
    parser.add_argument("--manifest", action="append", help="Path to a module_manifest/1.0 JSON file. Repeatable. Optional when --discover-root is used.")
    parser.add_argument("--discover-root", type=Path, help="Repository root for offline modules/checks/**/module.json discovery.")
    parser.add_argument("--policy-artifact", required=True, help="Path to a policy_boundary/1.0 allow artifact.")
    parser.add_argument("--run-id", required=True, help="Run ID for the planned run manifest.")
    parser.add_argument("--target-type", required=True, choices=sorted(TARGET_TYPES), help="Normalized target type.")
    parser.add_argument("--target", required=True, help="Target value that must match the policy artifact.")
    parser.add_argument("--mode", default=SUPPORTED_MODE, choices=[SUPPORTED_MODE], help="Only dry-run is supported in P2-4/P2-6.")
    parser.add_argument("--profile", default="audit-baseline", help="Runner profile ID loaded from modules/profiles/<profile>.json.")
    parser.add_argument("--profile-root", type=Path, help="Repository root for profile loading in explicit --manifest mode. Defaults to --discover-root or current directory.")
    parser.add_argument("--include-module-io-preview", action="store_true", help="Include P2-10 module_input/1.0 and module_result/1.0 preview-only envelopes; still does not execute modules.")
    parser.add_argument("--persist-preview-bundle", action="store_true", help="Persist the validated dry-run preview bundle under <repo>/runs/<run-id>/preview after all gates pass. Requires --include-module-io-preview and an explicit repo root.")
    parser.add_argument("--output", help="Optional path to write the plan JSON payload.")
    parser.add_argument("--json", action="store_true", help="Print structured JSON output.")
    args = parser.parse_args(argv)

    if args.persist_preview_bundle and not args.include_module_io_preview:
        result = RunnerResult(errors=["--persist-preview-bundle requires --include-module-io-preview"]).allow_if_clean()
        payload = result.as_dict()
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if args.json or not args.output:
            print(json.dumps(payload, indent=2, sort_keys=True))
        return 1, payload
    if args.persist_preview_bundle and not (args.discover_root or args.profile_root):
        result = RunnerResult(errors=["--persist-preview-bundle requires an explicit repo root via --discover-root or --profile-root"]).allow_if_clean()
        payload = result.as_dict()
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if args.json or not args.output:
            print(json.dumps(payload, indent=2, sort_keys=True))
        return 1, payload

    if args.discover_root and args.manifest:
        result = RunnerResult(errors=["cannot combine --discover-root with explicit --manifest paths"]).allow_if_clean()
        payload = result.as_dict()
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if args.json or not args.output:
            print(json.dumps(payload, indent=2, sort_keys=True))
        return 1, payload

    manifest_paths = [Path(path) for path in (args.manifest or [])]
    if args.discover_root:
        discovery = discover_profile_manifests(
            repo_root=args.discover_root,
            profile=args.profile,
            target_type=args.target_type,
            mode=args.mode,
        )
        if discovery.verdict != "allow":
            result = RunnerResult(
                errors=discovery.errors,
                warnings=discovery.warnings,
                error_details=discovery.error_details,
                warning_details=discovery.warning_details,
            ).allow_if_clean()
            payload = result.as_dict()
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            if args.json or not args.output:
                print(json.dumps(payload, indent=2, sort_keys=True))
            return 1, payload
        manifest_paths.extend(discovery.manifest_paths)

    if not manifest_paths:
        result = RunnerResult(errors=["at least one --manifest or --discover-root is required"]).allow_if_clean()
        payload = result.as_dict()
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if args.json or not args.output:
            print(json.dumps(payload, indent=2, sort_keys=True))
        return 1, payload

    result = build_dry_run_plan(
        manifest_paths=manifest_paths,
        policy_artifact_path=Path(args.policy_artifact),
        run_id=args.run_id,
        target_type=args.target_type,
        target_value=args.target,
        mode=args.mode,
        profile=args.profile,
        profile_root=args.profile_root or args.discover_root or Path.cwd(),
        include_module_io_preview=args.include_module_io_preview,
        persist_preview_bundle_root=(args.discover_root or args.profile_root) if args.persist_preview_bundle else None,
    )
    payload = result.as_dict()

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json or not args.output:
        print(json.dumps(payload, indent=2, sort_keys=True))

    return (0 if result.verdict == "allow" else 1), payload


if __name__ == "__main__":
    code, _payload = main()
    raise SystemExit(code)
