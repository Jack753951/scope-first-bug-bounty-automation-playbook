#!/usr/bin/env python3
"""Offline validator for program scope files.

This is a P1-2 helper only. It loads and validates JSON policy files for future
program scope integration, but it does not run scans or make runtime decisions
for recon.sh.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python 3.8 fallback path.
    ZoneInfo = None  # type: ignore[assignment]


SCHEMA_VERSION = "1.0"
SAFE_ALWAYS_PLATFORMS = {"lab", "ctf", "self-hosted"}
IDN_HANDLING = {"punycode_only", "reject_idn"}
PROGRAM_PLATFORMS = {
    "<bug-bounty-platform>",
    "bugcrowd",
    "intigriti",
    "yeswehack",
    "client",
    "lab",
    "ctf",
    "self-hosted",
    "other",
}
TECHNIQUES = {
    "subdomain_enumeration",
    "http_probe",
    "tls_fingerprint",
    "fixed_path_metadata",
    "port_scan",
    "service_fingerprint",
    "directory_bruteforce",
    "small_wordlist_discovery",
    "vulnerability_scan_passive",
    "nuclei_non_intrusive",
    "vulnerability_scan_active",
    "intrusive_fuzz",
    "owned_object_fuzz",
    "owned_object_authz_check",
    "api_token_min_scope_owned_account",
    "ssrf_marker_callback",
    "oast_marker_callback",
    "exploit_chain_marker_only",
    "exploit_chain_bounded_owned_impact",
    "dos",
    "credential_brute_force",
    "social_engineering",
    "physical",
    "malware",
    "callback_payloads",
}
NON_AUTHORIZABLE_TECHNIQUES = {
    "dos",
    "credential_brute_force",
    "social_engineering",
    "physical",
    "malware",
    "callback_payloads",
}
AUTOMATION_PROFILES = {
    "A1_PASSIVE_PUBLIC",
    "A2_LOW_SPEED_ACTIVE_RECON",
    "A3_BOUNDED_PROOF_ACTIONS",
    "A4_CONTROLLED_HIGH_RISK_PROOF",
}
CONTROLLED_A3_TECHNIQUES = {
    "ssrf_marker_callback",
    "oast_marker_callback",
    "exploit_chain_marker_only",
    "exploit_chain_bounded_owned_impact",
}
TOP_LEVEL_KEYS = {
    "schema_version",
    "program",
    "scope",
    "techniques",
    "rate_limits",
    "testing_windows",
    "expiration",
    "cleanup",
}
REQUIRED_TOP_LEVEL = {
    "schema_version",
    "program",
    "scope",
    "techniques",
    "rate_limits",
    "testing_windows",
    "expiration",
}
PROGRAM_KEYS = {
    "slug",
    "name",
    "platform",
    "url",
    "authorization_reference",
    "policy_version",
    "policy_acknowledged_at",
    "operator_contact",
    "program_contact",
}
REQUIRED_PROGRAM_KEYS = {
    "slug",
    "name",
    "platform",
    "url",
    "authorization_reference",
    "policy_version",
    "policy_acknowledged_at",
}
SCOPE_KEYS = {"in_scope", "out_of_scope", "idn_handling"}
TECHNIQUE_KEYS = {
    "allowed",
    "forbidden",
    "automation_permitted",
    "automation_profile",
    "controlled_capabilities",
    "a4_capabilities",  # legacy alias for controlled_capabilities
    "automation_notes",
}
RATE_LIMIT_KEYS = {
    "max_concurrency",
    "max_requests_per_second",
    "request_delay_ms",
    "nuclei_rate_limit",
    "nuclei_concurrency",
    "naabu_rate",
    "httpx_threads",
    "subfinder_threads",
    "max_requests_per_host_per_run",
    "max_state_changes_per_run",
    "max_chain_steps",
}
CAPABILITY_KEYS = {
    "name",
    "status",
    "max_requests_per_run",
    "max_steps",
    "callback_receiver",
    "allowed_impact",
    "blocked_escalations",
    "stop_before",
    "cleanup_required",
    "notes",
}
CLEANUP_KEYS = {"revoke_api_tokens", "delete_synthetic_objects", "record_cleanup_status", "notes"}
TESTING_WINDOW_KEYS = {"always", "timezone", "allowed", "blackouts"}
EXPIRATION_KEYS = {"valid_from", "valid_until"}
SCOPE_ENTRY_KEYS = {"type", "value", "include_apex", "notes", "reason"}
SCOPE_ENTRY_TYPES = {"domain", "wildcard", "cidr", "ip", "url_prefix"}
WINDOW_KEYS = {"days", "start", "end"}
BLACKOUT_KEYS = {"from", "to", "reason"}
DAY_NAMES = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
TIME_RE = re.compile(r"^([01][0-9]|2[0-3]):[0-5][0-9]$")


@dataclass
class ValidationResult:
    path: str
    program_slug: str | None = None
    verdict: str = "deny"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def finalize(self) -> "ValidationResult":
        self.verdict = "allow" if not self.errors else "deny"
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "program_slug": self.program_slug,
            "verdict": self.verdict,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def _type_name(value: Any) -> str:
    return type(value).__name__


def _error(result: ValidationResult, path: str, message: str) -> None:
    result.errors.append(f"{path}: {message}")


def _warn(result: ValidationResult, path: str, message: str) -> None:
    result.warnings.append(f"{path}: {message}")


def _ensure_object(
    result: ValidationResult,
    value: Any,
    path: str,
    allowed_keys: set[str] | None = None,
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        _error(result, path, f"expected object, got {_type_name(value)}")
        return None
    if allowed_keys is not None:
        unknown = sorted(set(value) - allowed_keys)
        if unknown:
            _error(result, path, f"unknown keys: {', '.join(unknown)}")
    return value


def _require_keys(
    result: ValidationResult,
    obj: dict[str, Any],
    required: set[str],
    path: str,
) -> None:
    missing = sorted(required - set(obj))
    if missing:
        _error(result, path, f"missing required keys: {', '.join(missing)}")


def _ensure_string(result: ValidationResult, value: Any, path: str) -> str | None:
    if not isinstance(value, str):
        _error(result, path, f"expected string, got {_type_name(value)}")
        return None
    if not value:
        _error(result, path, "must not be empty")
        return None
    return value


def _ensure_bool(result: ValidationResult, value: Any, path: str) -> bool | None:
    if not isinstance(value, bool):
        _error(result, path, f"expected boolean, got {_type_name(value)}")
        return None
    return value


def _ensure_list(result: ValidationResult, value: Any, path: str) -> list[Any] | None:
    if not isinstance(value, list):
        _error(result, path, f"expected array, got {_type_name(value)}")
        return None
    return value


def _parse_datetime(result: ValidationResult, value: Any, path: str) -> datetime | None:
    text = _ensure_string(result, value, path)
    if text is None:
        return None
    if not text.endswith("Z"):
        _error(result, path, "must be an ISO-8601 UTC timestamp ending in Z")
        return None
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00")
    except ValueError:
        _error(result, path, "must be a valid ISO-8601 UTC timestamp")
        return None
    if parsed.tzinfo is None:
        _error(result, path, "must include UTC timezone")
        return None
    return parsed.astimezone(timezone.utc)


def _ascii_lower(value: str) -> bool:
    return value.isascii() and value == value.lower()


def _validate_domain_name(value: str) -> str | None:
    if not _ascii_lower(value):
        return "must be lowercase ASCII/punycode only"
    if len(value) > 253:
        return "must be 253 characters or shorter"
    if value.endswith("."):
        return "must not use a trailing dot"
    labels = value.split(".")
    if len(labels) < 2:
        return "must contain at least two labels"
    for label in labels:
        if not label:
            return "must not contain empty labels"
        if len(label) > 63:
            return "labels must be 63 characters or shorter"
        if label.startswith("-") or label.endswith("-"):
            return "labels must not start or end with hyphen"
        if not re.fullmatch(r"[a-z0-9-]+", label):
            return "labels may contain only lowercase letters, digits, and hyphen"
    return None


def _parse_time(result: ValidationResult, value: Any, path: str) -> int | None:
    text = _ensure_string(result, value, path)
    if text is None:
        return None
    if not TIME_RE.fullmatch(text):
        _error(result, path, "must use HH:MM 24-hour time")
        return None
    hour, minute = text.split(":", 1)
    return int(hour) * 60 + int(minute)


def _expected_slug_from_path(path: Path) -> str | None:
    parts = path.parts
    if len(parts) < 3:
        return None
    if parts[-1] != "scope.json":
        return None
    if parts[-3] == "programs" and parts[-2] not in {"_examples", "_schema"}:
        return parts[-2]
    return None


def _validate_program(result: ValidationResult, data: dict[str, Any], file_path: Path) -> None:
    program = _ensure_object(result, data.get("program"), "program", PROGRAM_KEYS)
    if program is None:
        return
    _require_keys(result, program, REQUIRED_PROGRAM_KEYS, "program")

    slug = _ensure_string(result, program.get("slug"), "program.slug")
    if slug is not None:
        result.program_slug = slug
        if not SLUG_RE.fullmatch(slug):
            _error(result, "program.slug", "must match ^[a-z0-9][a-z0-9_-]{0,63}$")
        expected = _expected_slug_from_path(file_path)
        if expected is not None and slug != expected:
            _error(
                result,
                "program.slug",
                f"must match path slug '{expected}' for programs/<slug>/scope.json",
            )

    for key in ("name", "authorization_reference", "policy_version"):
        _ensure_string(result, program.get(key), f"program.{key}")

    platform = _ensure_string(result, program.get("platform"), "program.platform")
    if platform is not None and platform not in PROGRAM_PLATFORMS:
        _error(result, "program.platform", f"unsupported platform '{platform}'")

    url = _ensure_string(result, program.get("url"), "program.url")
    if url is not None:
        parsed = urlsplit(url)
        if parsed.scheme not in {"http", "https", "file"} or not parsed.netloc and parsed.scheme != "file":
            _error(result, "program.url", "must be an http(s) or file URL")
        if not url.isascii():
            _error(result, "program.url", "must be ASCII only")

    _parse_datetime(result, program.get("policy_acknowledged_at"), "program.policy_acknowledged_at")
    for key in ("operator_contact", "program_contact"):
        if key in program and not isinstance(program[key], str):
            _error(result, f"program.{key}", f"expected string, got {_type_name(program[key])}")


def _validate_scope_entry(result: ValidationResult, entry: Any, path: str) -> None:
    obj = _ensure_object(result, entry, path, SCOPE_ENTRY_KEYS)
    if obj is None:
        return
    _require_keys(result, obj, {"type", "value"}, path)
    entry_type = _ensure_string(result, obj.get("type"), f"{path}.type")
    value = _ensure_string(result, obj.get("value"), f"{path}.value")
    if entry_type is None or value is None:
        return
    if entry_type not in SCOPE_ENTRY_TYPES:
        _error(result, f"{path}.type", f"unsupported scope entry type '{entry_type}'")
        return
    if not value.isascii():
        _error(result, f"{path}.value", "raw Unicode/IDN entries are not allowed")
        return
    if "include_apex" in obj and not isinstance(obj["include_apex"], bool):
        _error(result, f"{path}.include_apex", "expected boolean")
    for key in ("notes", "reason"):
        if key in obj and not isinstance(obj[key], str):
            _error(result, f"{path}.{key}", f"expected string, got {_type_name(obj[key])}")

    if entry_type == "domain":
        reason = _validate_domain_name(value)
        if reason:
            _error(result, f"{path}.value", reason)
    elif entry_type == "wildcard":
        if not value.startswith("*."):
            _error(result, f"{path}.value", "wildcard entries must start with '*.'")
        else:
            reason = _validate_domain_name(value[2:])
            if reason:
                _error(result, f"{path}.value", reason)
    elif entry_type == "cidr":
        try:
            ipaddress.IPv4Network(value, strict=False)
        except ValueError:
            _error(result, f"{path}.value", "must be a valid IPv4 CIDR")
    elif entry_type == "ip":
        try:
            ipaddress.IPv4Address(value)
        except ValueError:
            _error(result, f"{path}.value", "must be a valid IPv4 address")
    elif entry_type == "url_prefix":
        parsed = urlsplit(value)
        if parsed.scheme not in {"http", "https"}:
            _error(result, f"{path}.value", "url_prefix must use http or https")
        if parsed.username or parsed.password:
            _error(result, f"{path}.value", "url_prefix must not contain userinfo")
        if parsed.hostname is None:
            _error(result, f"{path}.value", "url_prefix must contain a host")
        else:
            host = parsed.hostname
            reason = _validate_domain_name(host)
            if reason:
                _error(result, f"{path}.value", f"host {reason}")
        try:
            port = parsed.port
        except ValueError:
            _error(result, f"{path}.value", "url_prefix port must be 1-65535")
        else:
            if port is not None and not 1 <= port <= 65535:
                _error(result, f"{path}.value", "url_prefix port must be 1-65535")
        if not parsed.path.startswith("/") or parsed.path == "":
            _error(result, f"{path}.value", "url_prefix must include a path prefix")
        if parsed.query or parsed.fragment:
            _error(result, f"{path}.value", "url_prefix must not include query or fragment")


def _validate_scope(result: ValidationResult, data: dict[str, Any]) -> None:
    scope = _ensure_object(result, data.get("scope"), "scope", SCOPE_KEYS)
    if scope is None:
        return
    _require_keys(result, scope, SCOPE_KEYS, "scope")

    idn = _ensure_string(result, scope.get("idn_handling"), "scope.idn_handling")
    if idn is not None and idn not in IDN_HANDLING:
        _error(result, "scope.idn_handling", f"unsupported IDN handling '{idn}'")

    for key in ("in_scope", "out_of_scope"):
        entries = _ensure_list(result, scope.get(key), f"scope.{key}")
        if entries is None:
            continue
        if key == "in_scope" and not entries:
            _error(result, "scope.in_scope", "must contain at least one entry")
        for index, entry in enumerate(entries):
            _validate_scope_entry(result, entry, f"scope.{key}[{index}]")


def _validate_techniques(result: ValidationResult, data: dict[str, Any]) -> None:
    techniques = _ensure_object(result, data.get("techniques"), "techniques", TECHNIQUE_KEYS)
    if techniques is None:
        return
    _require_keys(result, techniques, {"allowed", "forbidden", "automation_permitted"}, "techniques")

    allowed_values: set[str] = set()
    forbidden_values: set[str] = set()
    for key, target in (("allowed", allowed_values), ("forbidden", forbidden_values)):
        values = _ensure_list(result, techniques.get(key), f"techniques.{key}")
        if values is None:
            continue
        if key == "allowed" and not values:
            _error(result, "techniques.allowed", "must not be empty")
        seen: set[str] = set()
        for index, item in enumerate(values):
            text = _ensure_string(result, item, f"techniques.{key}[{index}]")
            if text is None:
                continue
            if text not in TECHNIQUES:
                _error(result, f"techniques.{key}[{index}]", f"unknown technique '{text}'")
                continue
            if text in seen:
                _error(result, f"techniques.{key}", f"duplicate technique '{text}'")
            seen.add(text)
            target.add(text)

    overlap = sorted(allowed_values & forbidden_values)
    if overlap:
        _error(
            result,
            "techniques",
            f"techniques cannot be both allowed and forbidden: {', '.join(overlap)}",
        )
    blocked = sorted(allowed_values & NON_AUTHORIZABLE_TECHNIQUES)
    if blocked:
        _error(
            result,
            "techniques.allowed",
            f"non-authorizable techniques cannot be allowed: {', '.join(blocked)}",
        )

    _ensure_bool(
        result,
        techniques.get("automation_permitted"),
        "techniques.automation_permitted",
    )
    automation_profile = techniques.get("automation_profile")
    if automation_profile is not None:
        text = _ensure_string(result, automation_profile, "techniques.automation_profile")
        if text is not None and text not in AUTOMATION_PROFILES:
            _error(result, "techniques.automation_profile", f"unsupported automation profile '{text}'")
        if text is not None and allowed_values & ({"owned_object_fuzz", "owned_object_authz_check", "api_token_min_scope_owned_account"} | CONTROLLED_A3_TECHNIQUES) and text not in {"A3_BOUNDED_PROOF_ACTIONS", "A4_CONTROLLED_HIGH_RISK_PROOF"}:
            _error(result, "techniques.automation_profile", "A3 techniques require A3_BOUNDED_PROOF_ACTIONS")
        if text == "A4_CONTROLLED_HIGH_RISK_PROOF":
            _warn(result, "techniques.automation_profile", "A4_CONTROLLED_HIGH_RISK_PROOF is deprecated; use A3_BOUNDED_PROOF_ACTIONS")
    elif allowed_values & (CONTROLLED_A3_TECHNIQUES | {"owned_object_fuzz", "owned_object_authz_check", "api_token_min_scope_owned_account"}):
        _error(result, "techniques.automation_profile", "required when A3 techniques are allowed")

    if allowed_values & CONTROLLED_A3_TECHNIQUES:
        capability_key = "controlled_capabilities" if "controlled_capabilities" in techniques else "a4_capabilities"
        if capability_key == "a4_capabilities":
            _warn(result, "techniques.a4_capabilities", "deprecated; use controlled_capabilities")
        capabilities = _ensure_list(result, techniques.get(capability_key), f"techniques.{capability_key}")
        if not capabilities:
            _error(result, f"techniques.{capability_key}", "required when controlled A3 techniques are allowed")
        elif capabilities is not None:
            capability_names = _validate_controlled_a3_capabilities(result, capabilities, f"techniques.{capability_key}")
            missing = sorted((allowed_values & CONTROLLED_A3_TECHNIQUES) - capability_names)
            if missing:
                _error(
                    result,
                    f"techniques.{capability_key}",
                    "missing capability records for allowed controlled A3 techniques: " + ", ".join(missing),
                )
    else:
        for capability_key in ("controlled_capabilities", "a4_capabilities"):
            if capability_key in techniques:
                capabilities = _ensure_list(result, techniques.get(capability_key), f"techniques.{capability_key}")
                if capabilities is not None:
                    _validate_controlled_a3_capabilities(result, capabilities, f"techniques.{capability_key}")

    if "automation_notes" in techniques and not isinstance(techniques["automation_notes"], str):
        _error(
            result,
            "techniques.automation_notes",
            f"expected string, got {_type_name(techniques['automation_notes'])}",
        )


def _validate_string_list(result: ValidationResult, value: Any, path: str, *, required: bool = False) -> list[str]:
    values = _ensure_list(result, value, path)
    output: list[str] = []
    if values is None:
        return output
    if required and not values:
        _error(result, path, "must not be empty")
    seen: set[str] = set()
    for index, item in enumerate(values):
        text = _ensure_string(result, item, f"{path}[{index}]")
        if text is None:
            continue
        if text in seen:
            _error(result, path, f"duplicate value '{text}'")
        seen.add(text)
        output.append(text)
    return output


def _validate_controlled_a3_capabilities(result: ValidationResult, capabilities: list[Any], base_path: str) -> set[str]:
    names: set[str] = set()
    for index, capability in enumerate(capabilities):
        path = f"{base_path}[{index}]"
        obj = _ensure_object(result, capability, path, CAPABILITY_KEYS)
        if obj is None:
            continue
        _require_keys(result, obj, {"name", "status", "stop_before", "cleanup_required"}, path)
        name = _ensure_string(result, obj.get("name"), f"{path}.name")
        if name is not None:
            if name not in CONTROLLED_A3_TECHNIQUES:
                _error(result, f"{path}.name", f"unsupported controlled A3 capability '{name}'")
            if name in names:
                _error(result, base_path, f"duplicate capability '{name}'")
            names.add(name)
        status = _ensure_string(result, obj.get("status"), f"{path}.status")
        if status is not None and status not in {"operator_approved", "not_approved"}:
            _error(result, f"{path}.status", "must be operator_approved or not_approved")
        if status == "operator_approved" and obj.get("cleanup_required") is not True:
            _error(result, f"{path}.cleanup_required", "operator_approved controlled A3 capabilities require cleanup_required=true")
        for cap_key in ("max_requests_per_run", "max_steps"):
            if cap_key in obj:
                value = obj[cap_key]
                if isinstance(value, bool) or not isinstance(value, int):
                    _error(result, f"{path}.{cap_key}", f"expected integer, got {_type_name(value)}")
                elif value <= 0:
                    _error(result, f"{path}.{cap_key}", "must be a positive integer")
        if "callback_receiver" in obj and not isinstance(obj["callback_receiver"], str):
            _error(result, f"{path}.callback_receiver", f"expected string, got {_type_name(obj['callback_receiver'])}")
        if status == "operator_approved" and name in {"ssrf_marker_callback", "oast_marker_callback"}:
            receiver = obj.get("callback_receiver")
            if not isinstance(receiver, str) or "operator" not in receiver.lower():
                _error(result, f"{path}.callback_receiver", "SSRF/OAST capabilities require an operator-controlled callback receiver")
            if not isinstance(obj.get("max_requests_per_run"), int) or isinstance(obj.get("max_requests_per_run"), bool):
                _error(result, f"{path}.max_requests_per_run", "SSRF/OAST capabilities require max_requests_per_run")
        if status == "operator_approved" and name and name.startswith("exploit_chain"):
            if not isinstance(obj.get("max_requests_per_run"), int) or isinstance(obj.get("max_requests_per_run"), bool):
                _error(result, f"{path}.max_requests_per_run", "exploit-chain capabilities require max_requests_per_run")
            if not isinstance(obj.get("max_steps"), int) or isinstance(obj.get("max_steps"), bool):
                _error(result, f"{path}.max_steps", "exploit-chain capabilities require max_steps")
        if "allowed_impact" in obj and obj["allowed_impact"] not in {"marker_only", "owned_data_only", "owned_state_change_recoverable"}:
            _error(result, f"{path}.allowed_impact", "must be marker_only, owned_data_only, or owned_state_change_recoverable")
        if "blocked_escalations" in obj:
            _validate_string_list(result, obj["blocked_escalations"], f"{path}.blocked_escalations", required=True)
        stop_before = _validate_string_list(result, obj.get("stop_before"), f"{path}.stop_before", required=True)
        if status == "operator_approved" and name in CONTROLLED_A3_TECHNIQUES:
            required_stops = {"non_owned_data", "secret_capture", "credential_extraction", "persistence", "final_submission", "uncontrolled_internal_enumeration"}
            if name in {"ssrf_marker_callback", "oast_marker_callback"}:
                required_stops.add("cloud_metadata_credential_access")
            if name and name.startswith("exploit_chain"):
                required_stops.add("destructive_impact_outside_owned_state")
            missing_stops = sorted(required_stops - set(stop_before))
            if missing_stops:
                _error(result, f"{path}.stop_before", "missing required stops: " + ", ".join(missing_stops))
        cleanup_required = obj.get("cleanup_required")
        if cleanup_required is not None and not isinstance(cleanup_required, bool):
            _error(result, f"{path}.cleanup_required", f"expected boolean, got {_type_name(cleanup_required)}")
        if "notes" in obj and not isinstance(obj["notes"], str):
            _error(result, f"{path}.notes", f"expected string, got {_type_name(obj['notes'])}")
    return names


def _validate_rate_limits(result: ValidationResult, data: dict[str, Any]) -> None:
    rate_limits = _ensure_object(result, data.get("rate_limits"), "rate_limits", RATE_LIMIT_KEYS)
    if rate_limits is None:
        return
    if not rate_limits:
        _error(result, "rate_limits", "must contain at least one safe cap")
    for key, value in rate_limits.items():
        if isinstance(value, bool) or not isinstance(value, int):
            _error(result, f"rate_limits.{key}", f"expected integer, got {_type_name(value)}")
            continue
        if value <= 0:
            _error(result, f"rate_limits.{key}", "must be a positive integer")


def _validate_cleanup(result: ValidationResult, data: dict[str, Any]) -> None:
    if "cleanup" not in data:
        return
    cleanup = _ensure_object(result, data.get("cleanup"), "cleanup", CLEANUP_KEYS)
    if cleanup is None:
        return
    for key in ("revoke_api_tokens", "delete_synthetic_objects", "record_cleanup_status"):
        if key in cleanup and not isinstance(cleanup[key], bool):
            _error(result, f"cleanup.{key}", f"expected boolean, got {_type_name(cleanup[key])}")
    if "notes" in cleanup and not isinstance(cleanup["notes"], str):
        _error(result, "cleanup.notes", f"expected string, got {_type_name(cleanup['notes'])}")


def _validate_window(result: ValidationResult, window: Any, path: str) -> None:
    obj = _ensure_object(result, window, path, WINDOW_KEYS)
    if obj is None:
        return
    _require_keys(result, obj, WINDOW_KEYS, path)
    days = _ensure_list(result, obj.get("days"), f"{path}.days")
    if days is not None:
        if not days:
            _error(result, f"{path}.days", "must not be empty")
        seen: set[str] = set()
        for index, day in enumerate(days):
            text = _ensure_string(result, day, f"{path}.days[{index}]")
            if text is None:
                continue
            if text not in DAY_NAMES:
                _error(result, f"{path}.days[{index}]", f"unsupported day '{text}'")
            if text in seen:
                _error(result, f"{path}.days", f"duplicate day '{text}'")
            seen.add(text)
    start = _parse_time(result, obj.get("start"), f"{path}.start")
    end = _parse_time(result, obj.get("end"), f"{path}.end")
    if start is not None and end is not None and start >= end:
        _error(result, path, "window end must be after start; split overnight windows")


def _validate_blackout(result: ValidationResult, blackout: Any, path: str) -> None:
    obj = _ensure_object(result, blackout, path, BLACKOUT_KEYS)
    if obj is None:
        return
    _require_keys(result, obj, BLACKOUT_KEYS, path)
    start = _parse_datetime(result, obj.get("from"), f"{path}.from")
    end = _parse_datetime(result, obj.get("to"), f"{path}.to")
    if start is not None and end is not None and start >= end:
        _error(result, path, "blackout to must be after from")
    _ensure_string(result, obj.get("reason"), f"{path}.reason")


def _validate_testing_windows(result: ValidationResult, data: dict[str, Any]) -> None:
    testing_windows = _ensure_object(
        result,
        data.get("testing_windows"),
        "testing_windows",
        TESTING_WINDOW_KEYS,
    )
    if testing_windows is None:
        return
    _require_keys(result, testing_windows, {"always"}, "testing_windows")
    always = _ensure_bool(result, testing_windows.get("always"), "testing_windows.always")
    platform = data.get("program", {}).get("platform") if isinstance(data.get("program"), dict) else None
    if always is True and platform not in SAFE_ALWAYS_PLATFORMS:
        _error(
            result,
            "testing_windows.always",
            "always=true is allowed only for lab, ctf, or self-hosted programs",
        )
    if always is False:
        timezone_name = _ensure_string(
            result,
            testing_windows.get("timezone"),
            "testing_windows.timezone",
        )
        if timezone_name is not None:
            if not timezone_name.isascii() or not re.fullmatch(
                r"[A-Za-z0-9_+.-]+(?:/[A-Za-z0-9_+.-]+)*",
                timezone_name,
            ):
                _error(result, "testing_windows.timezone", "must look like an IANA timezone name")
            elif ZoneInfo is not None:
                try:
                    ZoneInfo(timezone_name)
                except Exception:
                    # Some Windows/Python distributions do not bundle the IANA
                    # database. P1-2 validates shape offline and leaves runtime
                    # timezone evaluation to the later integration layer.
                    pass
        allowed = _ensure_list(result, testing_windows.get("allowed"), "testing_windows.allowed")
        if allowed is not None:
            if not allowed:
                _error(result, "testing_windows.allowed", "must not be empty when always=false")
            for index, window in enumerate(allowed):
                _validate_window(result, window, f"testing_windows.allowed[{index}]")
    elif "allowed" in testing_windows:
        allowed = _ensure_list(result, testing_windows.get("allowed"), "testing_windows.allowed")
        if allowed is not None:
            for index, window in enumerate(allowed):
                _validate_window(result, window, f"testing_windows.allowed[{index}]")

    if "blackouts" in testing_windows:
        blackouts = _ensure_list(result, testing_windows["blackouts"], "testing_windows.blackouts")
        if blackouts is not None:
            for index, blackout in enumerate(blackouts):
                _validate_blackout(result, blackout, f"testing_windows.blackouts[{index}]")


def _validate_expiration(
    result: ValidationResult,
    data: dict[str, Any],
    ignore_time: bool,
    now: datetime | None,
) -> None:
    expiration = _ensure_object(result, data.get("expiration"), "expiration", EXPIRATION_KEYS)
    if expiration is None:
        return
    _require_keys(result, expiration, EXPIRATION_KEYS, "expiration")
    valid_from = _parse_datetime(result, expiration.get("valid_from"), "expiration.valid_from")
    valid_until = _parse_datetime(result, expiration.get("valid_until"), "expiration.valid_until")
    if valid_from is None or valid_until is None:
        return
    if valid_until <= valid_from:
        _error(result, "expiration", "valid_until must be after valid_from")
        return
    if valid_until - valid_from > timedelta_days(365):
        _warn(result, "expiration", "validity window is longer than 365 days")
    if not ignore_time:
        current = now or datetime.now(timezone.utc)
        if current < valid_from:
            _error(result, "expiration", "program scope is not yet active")
        if current > valid_until:
            _error(result, "expiration", "program scope is expired")


def timedelta_days(days: int):
    # Kept as a function to avoid exposing datetime.timedelta in public imports.
    from datetime import timedelta

    return timedelta(days=days)


def validate_data(
    data: Any,
    source_path: str | Path,
    *,
    ignore_time: bool = False,
    now: datetime | None = None,
) -> ValidationResult:
    file_path = Path(source_path)
    result = ValidationResult(path=str(source_path))
    root = _ensure_object(result, data, "$", TOP_LEVEL_KEYS)
    if root is None:
        return result.finalize()
    _require_keys(result, root, REQUIRED_TOP_LEVEL, "$")

    schema_version = root.get("schema_version")
    if schema_version != SCHEMA_VERSION:
        _error(result, "schema_version", f"must equal {SCHEMA_VERSION!r}")

    _validate_program(result, root, file_path)
    _validate_scope(result, root)
    _validate_techniques(result, root)
    _validate_rate_limits(result, root)
    _validate_cleanup(result, root)
    _validate_testing_windows(result, root)
    _validate_expiration(result, root, ignore_time=ignore_time, now=now)
    return result.finalize()


def validate_file(
    source_path: str | Path,
    *,
    ignore_time: bool = False,
    now: datetime | None = None,
) -> ValidationResult:
    path = Path(source_path)
    result = ValidationResult(path=str(source_path))
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        _error(result, "$", "file not found")
        return result.finalize()
    except PermissionError:
        _error(result, "$", "permission denied")
        return result.finalize()
    except UnicodeDecodeError as exc:
        _error(result, "$", f"file is not valid UTF-8: {exc}")
        return result.finalize()
    except json.JSONDecodeError as exc:
        _error(result, "$", f"invalid JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}")
        return result.finalize()
    return validate_data(data, path, ignore_time=ignore_time, now=now)


def _print_text(result: ValidationResult) -> None:
    print(f"verdict: {result.verdict}")
    print(f"program_slug: {result.program_slug or 'unknown'}")
    if result.errors:
        print("errors:")
        for item in result.errors:
            print(f"  - {item}")
    else:
        print("errors: []")
    if result.warnings:
        print("warnings:")
        for item in result.warnings:
            print(f"  - {item}")
    else:
        print("warnings: []")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Offline default-deny validator for programs/<slug>/scope.json files.",
    )
    parser.add_argument("scope_file", help="Path to a program scope JSON file.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")
    parser.add_argument(
        "--ignore-time",
        action="store_true",
        help="Validate timestamps but skip current-time active/expired checks.",
    )
    args = parser.parse_args(argv)

    result = validate_file(args.scope_file, ignore_time=args.ignore_time)
    if args.json:
        print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
    else:
        _print_text(result)
    return 0 if result.verdict == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
