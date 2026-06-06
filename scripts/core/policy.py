"""Offline program policy decision engine.

The decision helper answers whether a target, technique, and mode are allowed
by the intersection of a validated program scope and the global scope file. It
does not execute reconnaissance, probes, scanners, or modules.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python 3.8 fallback.
    ZoneInfo = None  # type: ignore[assignment]

from scripts import validate_program_scope
from scripts.core.scope import (
    NormalizedTarget,
    entries_from_program_scope,
    load_global_scope,
    normalize_target,
    target_matches_any,
)


MODES = {"dry-run", "planned", "live"}
SCHEMA_VERSION = "policy_decision/1.0"
CONTROLLED_A3_TECHNIQUES = {
    "ssrf_marker_callback",
    "oast_marker_callback",
    "exploit_chain_marker_only",
    "exploit_chain_bounded_owned_impact",
}
A3_TECHNIQUES = {
    "owned_object_fuzz",
    "owned_object_authz_check",
    "api_token_min_scope_owned_account",
    *CONTROLLED_A3_TECHNIQUES,
}
A3_PROFILE = "A3_BOUNDED_PROOF_ACTIONS"
LEGACY_A4_PROFILE = "A4_CONTROLLED_HIGH_RISK_PROOF"
A3_PROFILES = {A3_PROFILE, LEGACY_A4_PROFILE}


@dataclass
class PolicyDecision:
    schema_version: str = SCHEMA_VERSION
    verdict: str = "deny"
    program_slug: str = "unknown"
    target: str = ""
    normalized_target: str = ""
    target_type: str = "unknown"
    technique: str = ""
    mode: str = "dry-run"
    reasons: list[str] = field(default_factory=list)
    deny_reason_codes: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    audit_event: str = "PROGRAM_POLICY_DENY"
    program_file_sha256: str | None = None
    global_scope_sha256: str | None = None
    decided_at_utc: str = ""

    def deny(self, code: str, message: str) -> None:
        if code not in self.deny_reason_codes:
            self.deny_reason_codes.append(code)
        self.errors.append(message)

    def reason(self, message: str) -> None:
        if message not in self.reasons:
            self.reasons.append(message)

    def finalize(self) -> "PolicyDecision":
        self.verdict = "allow" if not self.errors and not self.deny_reason_codes else "deny"
        self.audit_event = "PROGRAM_POLICY_ALLOW" if self.verdict == "allow" else "PROGRAM_POLICY_DENY"
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "verdict": self.verdict,
            "program_slug": self.program_slug,
            "target": self.target,
            "normalized_target": self.normalized_target,
            "target_type": self.target_type,
            "technique": self.technique,
            "mode": self.mode,
            "reasons": self.reasons,
            "deny_reason_codes": self.deny_reason_codes,
            "errors": self.errors,
            "warnings": self.warnings,
            "audit_event": self.audit_event,
            "program_file_sha256": self.program_file_sha256,
            "global_scope_sha256": self.global_scope_sha256,
            "decided_at_utc": self.decided_at_utc,
        }


def decide_program_policy(
    *,
    program_path: str | Path,
    global_scope_path: str | Path,
    target: str,
    technique: str,
    mode: str = "dry-run",
    ignore_time: bool = False,
    now: datetime | None = None,
) -> PolicyDecision:
    decision = PolicyDecision(
        target=target,
        technique=technique,
        mode=mode,
        decided_at_utc=_format_utc(now),
    )

    _record_file_sha256(decision, "program_file_sha256", program_path, "PROGRAM_RELOAD_FAILED", "program scope file")
    _record_file_sha256(decision, "global_scope_sha256", global_scope_path, "GLOBAL_SCOPE_ERROR", "global scope file")

    if mode not in MODES:
        decision.deny("UNSUPPORTED_MODE", f"unsupported mode '{mode}'")
        return decision.finalize()
    if decision.deny_reason_codes:
        return decision.finalize()

    program_result = validate_program_scope.validate_file(program_path, ignore_time=ignore_time, now=now)
    if program_result.program_slug:
        decision.program_slug = program_result.program_slug
    decision.warnings.extend(program_result.warnings)
    if program_result.verdict != "allow":
        decision.deny("VALIDATOR_DENY", "program scope validator verdict is deny")
        for error in program_result.errors:
            decision.errors.append(f"validator: {error}")
        return decision.finalize()
    decision.reason("program scope validator allowed")

    data = _load_program_json(program_path, decision)
    if data is None:
        return decision.finalize()

    target_result = normalize_target(target)
    if target_result.target is None:
        code = "IPV6_UNSUPPORTED" if any("IPv6" in error for error in target_result.errors) else "INVALID_TARGET"
        for error in target_result.errors:
            decision.deny(code, error)
        return decision.finalize()
    normalized = target_result.target
    decision.normalized_target = normalized.normalized
    decision.target_type = normalized.target_type
    decision.reason(f"target normalized as {normalized.target_type}")

    _check_program_scope(decision, data, normalized)
    _check_global_scope(decision, global_scope_path, normalized)
    _check_technique(decision, data, technique, mode)
    _check_testing_window(decision, data, mode, now)
    return decision.finalize()


def _load_program_json(path: str | Path, decision: PolicyDecision) -> dict[str, Any] | None:
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        decision.deny("PROGRAM_RELOAD_FAILED", f"failed to reload validated program scope: {exc}")
        return None
    if not isinstance(data, dict):
        decision.deny("PROGRAM_RELOAD_FAILED", "program scope root is not an object")
        return None
    return data


def _check_program_scope(
    decision: PolicyDecision,
    data: dict[str, Any],
    target: NormalizedTarget,
) -> None:
    scope = data.get("scope", {})
    if not isinstance(scope, dict):
        decision.deny("PROGRAM_SCOPE_PARSE_ERROR", "program scope block is not an object")
        return
    out_scope = entries_from_program_scope(scope.get("out_of_scope", []), "scope.out_of_scope")
    in_scope = entries_from_program_scope(scope.get("in_scope", []), "scope.in_scope")
    for error in out_scope.errors:
        decision.deny("PROGRAM_SCOPE_PARSE_ERROR", error)
    for error in in_scope.errors:
        decision.deny("PROGRAM_SCOPE_PARSE_ERROR", error)
    decision.warnings.extend(out_scope.warnings)
    decision.warnings.extend(in_scope.warnings)
    if out_scope.errors or in_scope.errors:
        return
    if target_matches_any(target, out_scope.entries):
        decision.deny("PROGRAM_OUT_OF_SCOPE", "target matches program out_of_scope")
        return
    if not target_matches_any(target, in_scope.entries):
        decision.deny("NOT_IN_PROGRAM_SCOPE", "target does not match program in_scope")
        return
    decision.reason("program in-scope matched")


def _check_global_scope(
    decision: PolicyDecision,
    global_scope_path: str | Path,
    target: NormalizedTarget,
) -> None:
    global_scope = load_global_scope(global_scope_path)
    decision.warnings.extend(global_scope.warnings)
    if global_scope.errors:
        for error in global_scope.errors:
            decision.deny("GLOBAL_SCOPE_ERROR", error)
        return
    if not target_matches_any(target, global_scope.entries):
        decision.deny("NOT_IN_GLOBAL_SCOPE", "target does not match global scope")
        return
    decision.reason("global scope matched")


def _check_technique(
    decision: PolicyDecision,
    data: dict[str, Any],
    technique: str,
    mode: str,
) -> None:
    techniques = data.get("techniques", {})
    if not isinstance(techniques, dict):
        decision.deny("PROGRAM_SCOPE_PARSE_ERROR", "program techniques block is not an object")
        return
    allowed = set(techniques.get("allowed", []))
    forbidden = set(techniques.get("forbidden", []))
    if technique in forbidden:
        decision.deny("FORBIDDEN_TECHNIQUE", f"technique '{technique}' is forbidden by program policy")
    elif technique not in allowed:
        decision.deny("TECHNIQUE_NOT_ALLOWED", f"technique '{technique}' is not allowed by program policy")
    else:
        decision.reason("technique allowed")
    automation_permitted = techniques.get("automation_permitted")
    if mode in {"planned", "live"} and automation_permitted is not True:
        decision.deny("AUTOMATION_DISABLED", f"mode '{mode}' requires techniques.automation_permitted=true")
    elif mode in {"planned", "live"}:
        decision.reason("automation permitted for mode")
    else:
        decision.reason("dry-run mode does not require automation")

    automation_profile = techniques.get("automation_profile")
    if technique in A3_TECHNIQUES and mode in {"planned", "live"}:
        if automation_profile not in A3_PROFILES:
            decision.deny(
                "A3_PROFILE_REQUIRED",
                f"technique '{technique}' requires A3_BOUNDED_PROOF_ACTIONS",
            )
        else:
            if automation_profile == LEGACY_A4_PROFILE:
                decision.warnings.append("A4_CONTROLLED_HIGH_RISK_PROOF is deprecated; treating as A3_BOUNDED_PROOF_ACTIONS")
            decision.reason(f"A3 technique permitted by {automation_profile}")
    if technique in CONTROLLED_A3_TECHNIQUES and mode in {"planned", "live"}:
        if "a4_capabilities" in techniques and "controlled_capabilities" not in techniques:
            decision.warnings.append("techniques.a4_capabilities is deprecated; use controlled_capabilities")
        capability = _find_controlled_a3_capability(techniques, technique)
        if capability is None:
            decision.deny("A3_CAPABILITY_MISSING", f"technique '{technique}' requires a matching A3 controlled capability record")
        elif capability.get("status") != "operator_approved":
            decision.deny("A3_CAPABILITY_NOT_APPROVED", f"technique '{technique}' capability is not operator_approved")
        else:
            _check_controlled_a3_capability(decision, technique, capability)


def _find_controlled_a3_capability(techniques: dict[str, Any], technique: str) -> dict[str, Any] | None:
    capabilities = techniques.get("controlled_capabilities", techniques.get("a4_capabilities"))
    if not isinstance(capabilities, list):
        return None
    for capability in capabilities:
        if isinstance(capability, dict) and capability.get("name") == technique:
            return capability
    return None


def _check_controlled_a3_capability(decision: PolicyDecision, technique: str, capability: dict[str, Any]) -> None:
    max_requests = capability.get("max_requests_per_run")
    if not isinstance(max_requests, int) or isinstance(max_requests, bool) or max_requests <= 0:
        decision.deny("A3_REQUEST_CAP_REQUIRED", f"technique '{technique}' requires positive max_requests_per_run")
        return
    if technique.startswith("exploit_chain"):
        max_steps = capability.get("max_steps")
        if not isinstance(max_steps, int) or isinstance(max_steps, bool) or max_steps <= 0:
            decision.deny("A3_STEP_CAP_REQUIRED", f"technique '{technique}' requires positive max_steps")
            return
    if technique in {"ssrf_marker_callback", "oast_marker_callback"}:
        receiver = capability.get("callback_receiver")
        if not isinstance(receiver, str) or "operator" not in receiver.lower():
            decision.deny("A3_CALLBACK_RECEIVER_REQUIRED", f"technique '{technique}' requires an operator-controlled callback receiver")
            return
    stop_before = capability.get("stop_before")
    if not isinstance(stop_before, list) or not all(isinstance(item, str) for item in stop_before):
        decision.deny("A3_STOP_BEFORE_INVALID", f"technique '{technique}' has invalid stop_before list")
        return
    required_stops = {"non_owned_data", "secret_capture", "credential_extraction", "persistence", "final_submission", "uncontrolled_internal_enumeration"}
    if technique in {"ssrf_marker_callback", "oast_marker_callback"}:
        required_stops.add("cloud_metadata_credential_access")
    if technique.startswith("exploit_chain"):
        required_stops.add("destructive_impact_outside_owned_state")
    missing_stops = sorted(required_stops - set(stop_before))
    if missing_stops:
        decision.deny("A3_STOP_BEFORE_INCOMPLETE", "A3 controlled capability missing stop-before controls: " + ", ".join(missing_stops))
        return
    cleanup_required = capability.get("cleanup_required")
    if cleanup_required is not True:
        decision.deny("A3_CLEANUP_REQUIRED", f"technique '{technique}' requires cleanup_required=true")
        return
    if technique == "exploit_chain_bounded_owned_impact":
        allowed_impact = capability.get("allowed_impact")
        if allowed_impact not in {"owned_data_only", "owned_state_change_recoverable"}:
            decision.deny(
                "A3_IMPACT_BOUNDARY_REQUIRED",
                "bounded exploit chains must specify owned_data_only or owned_state_change_recoverable impact",
            )
            return
    decision.reason(f"A3 controlled capability '{technique}' operator-approved with stop-before controls")


def _check_testing_window(
    decision: PolicyDecision,
    data: dict[str, Any],
    mode: str,
    now: datetime | None,
) -> None:
    if mode == "dry-run":
        decision.reason("dry-run mode does not require testing window")
        return
    windows = data.get("testing_windows", {})
    if not isinstance(windows, dict):
        decision.deny("TESTING_WINDOW_ERROR", "program testing_windows block is not an object")
        return
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    current = current.astimezone(timezone.utc)

    for blackout in windows.get("blackouts", []) or []:
        start = _parse_utc(blackout.get("from"))
        end = _parse_utc(blackout.get("to"))
        if start is not None and end is not None and start <= current < end:
            decision.deny("BLACKOUT", "mode is denied during program testing blackout")
            return

    if windows.get("always") is True:
        decision.reason("testing window always allowed")
        return
    timezone_name = windows.get("timezone")
    if not isinstance(timezone_name, str):
        decision.deny("TESTING_WINDOW_ERROR", "testing window timezone is missing")
        return
    if ZoneInfo is None:
        decision.deny("TESTING_WINDOW_ERROR", "testing window timezone cannot be evaluated on this Python runtime")
        return
    try:
        local_now = current.astimezone(ZoneInfo(timezone_name))
    except Exception:
        decision.deny("TESTING_WINDOW_ERROR", f"testing window timezone cannot be evaluated: {timezone_name}")
        return

    day = local_now.strftime("%a")
    minute = local_now.hour * 60 + local_now.minute
    for window in windows.get("allowed", []) or []:
        days = window.get("days", [])
        start = _parse_hhmm(window.get("start"))
        end = _parse_hhmm(window.get("end"))
        if day in days and start is not None and end is not None and start <= minute < end:
            decision.reason("testing window matched")
            return
    decision.deny("OUTSIDE_TESTING_WINDOW", "mode is outside the program testing window")


def _parse_utc(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        return datetime.fromisoformat(value[:-1] + "+00:00").astimezone(timezone.utc)
    except ValueError:
        return None


def _record_file_sha256(
    decision: PolicyDecision,
    field_name: str,
    path: str | Path,
    code: str,
    label: str,
) -> None:
    source_path = Path(path)
    try:
        digest = sha256(source_path.read_bytes()).hexdigest()
    except OSError as exc:
        setattr(decision, field_name, None)
        decision.deny(code, f"{label} cannot be read for provenance: {source_path}: {exc}")
        return
    setattr(decision, field_name, digest)


def _format_utc(now: datetime | None) -> str:
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    current = current.astimezone(timezone.utc).replace(microsecond=0)
    return current.isoformat().replace("+00:00", "Z")


def _parse_hhmm(value: Any) -> int | None:
    if not isinstance(value, str):
        return None
    try:
        hour, minute = value.split(":", 1)
        return int(hour) * 60 + int(minute)
    except (ValueError, TypeError):
        return None
