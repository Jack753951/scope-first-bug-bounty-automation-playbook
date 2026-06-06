#!/usr/bin/env python3
"""Subprocess boundary for offline program policy decisions.

This wrapper intentionally does not run reconnaissance, scanners, probes, or
target-touching automation. It invokes the existing policy decision helper,
validates the versioned JSON contract, writes one evidence artifact, and prints
flat shell-readable key/value output for future recon.sh integration.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from hashlib import sha256
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BOUNDARY_SCHEMA_VERSION = "policy_boundary/1.0"
DECISION_SCHEMA_VERSION = "policy_decision/1.0"
DEFAULT_TIMEOUT_SECONDS = 10.0
DEFAULT_HELPER = Path(__file__).resolve().with_name("program_policy_check.py")
MODES = {"dry-run", "planned", "live"}
VERDICTS = {"allow", "deny"}
TECHNIQUES = {
    "subdomain_enumeration",
    "http_probe",
    "port_scan",
    "service_fingerprint",
    "directory_bruteforce",
    "vulnerability_scan_passive",
    "vulnerability_scan_active",
    "intrusive_fuzz",
    "dos",
    "credential_brute_force",
    "social_engineering",
    "physical",
    "malware",
    "callback_payloads",
}
STRING_FIELDS = {
    "program_slug",
    "target",
    "normalized_target",
    "target_type",
    "technique",
    "mode",
    "audit_event",
    "decided_at_utc",
}
LIST_FIELDS = {"reasons", "errors", "warnings", "deny_reason_codes"}
EXPECTED_DECISION_FIELDS = {
    "schema_version",
    "verdict",
    "program_slug",
    "target",
    "normalized_target",
    "target_type",
    "technique",
    "mode",
    "audit_event",
    "reasons",
    "errors",
    "warnings",
    "deny_reason_codes",
    "program_file_sha256",
    "global_scope_sha256",
    "decided_at_utc",
}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


@dataclass
class BoundaryResult:
    status: str
    exit_code: int
    audit_event: str = "PROGRAM_POLICY_BOUNDARY_ERROR"
    deny_reason_codes: list[str] = field(default_factory=list)
    message: str = ""
    artifact_path: str = ""
    decision: dict[str, Any] | None = None
    helper_returncode: int | None = None
    helper_timed_out: bool = False
    contract_errors: list[str] = field(default_factory=list)
    boundary_errors: list[str] = field(default_factory=list)
    helper_stdout_excerpt: str = ""
    helper_stderr_excerpt: str = ""


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_filename_part(value: str, fallback: str = "target") -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())[:80].strip(".-")
    return safe or fallback


def _artifact_path(artifact_dir: Path, target: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_target = _safe_filename_part(target)
    return artifact_dir / f"policy_boundary_{timestamp}_{os.getpid()}_{time.time_ns()}_{safe_target}.json"


def _excerpt(value: str | bytes | None, limit: int = 1000) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    value = value.replace("\x00", "")
    if len(value) > limit:
        return value[:limit] + "...[truncated]"
    return value


def _sha256_file(path: str) -> str:
    return sha256(Path(path).read_bytes()).hexdigest()


def _target_type_for_forced_deny(target: str) -> str:
    if "/" in target and re.fullmatch(r"[0-9]{1,3}(?:\.[0-9]{1,3}){3}/[0-9]{1,2}", target):
        return "cidr"
    if target.startswith(("http://", "https://")):
        return "url"
    if re.fullmatch(r"[0-9]{1,3}(?:\.[0-9]{1,3}){3}", target):
        return "ip"
    return "domain"


def _validate_decision_contract(payload: Any, helper_returncode: int | None) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["helper JSON root must be an object"]

    observed_fields = set(payload)
    missing_fields = sorted(EXPECTED_DECISION_FIELDS - observed_fields)
    unknown_fields = sorted(observed_fields - EXPECTED_DECISION_FIELDS)
    if missing_fields:
        errors.append(f"decision contract missing fields: {', '.join(missing_fields)}")
    if unknown_fields:
        errors.append(f"decision contract unknown fields: {', '.join(unknown_fields)}")

    if payload.get("schema_version") != DECISION_SCHEMA_VERSION:
        errors.append(f"schema_version must equal {DECISION_SCHEMA_VERSION}")

    verdict = payload.get("verdict")
    if verdict not in VERDICTS:
        errors.append("verdict must be allow or deny")

    for field_name in STRING_FIELDS:
        if not isinstance(payload.get(field_name), str):
            errors.append(f"{field_name} must be a string")

    if payload.get("mode") not in MODES:
        errors.append("mode must be dry-run, planned, or live")
    if payload.get("technique") not in TECHNIQUES:
        errors.append("technique must be a schema enum value")

    for field_name in LIST_FIELDS:
        value = payload.get(field_name)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            errors.append(f"{field_name} must be a list of strings")

    for field_name in ("program_file_sha256", "global_scope_sha256"):
        value = payload.get(field_name)
        if not isinstance(value, str) or not HASH_RE.fullmatch(value):
            errors.append(f"{field_name} must be a lowercase SHA-256 hex string")

    decided_at = payload.get("decided_at_utc")
    if not isinstance(decided_at, str) or not UTC_RE.fullmatch(decided_at):
        errors.append("decided_at_utc must be an ISO-8601 UTC timestamp ending in Z")

    audit_event = payload.get("audit_event")
    if verdict == "allow" and audit_event != "PROGRAM_POLICY_ALLOW":
        errors.append("allow verdict must use PROGRAM_POLICY_ALLOW audit_event")
    if verdict == "deny" and audit_event != "PROGRAM_POLICY_DENY":
        errors.append("deny verdict must use PROGRAM_POLICY_DENY audit_event")

    if verdict == "allow" and helper_returncode != 0:
        errors.append("helper exit code contradicts allow verdict")
    if verdict == "deny" and helper_returncode == 0:
        errors.append("helper exit code contradicts deny verdict")

    return errors


def _build_helper_command(args: argparse.Namespace, helper_path: Path) -> list[str]:
    command = [
        sys.executable,
        "-I",
        str(helper_path),
        "--program",
        args.program,
        "--global-scope",
        args.global_scope,
        "--target",
        args.target,
        "--technique",
        args.technique,
        "--mode",
        args.mode,
        "--json",
    ]
    if args.ignore_time:
        command.append("--ignore-time")
    return command


def _write_artifact(artifact_dir: Path, target: str, artifact: dict[str, Any]) -> Path:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    final_path = _artifact_path(artifact_dir, target)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{final_path.name}.",
        suffix=".tmp",
        dir=str(artifact_dir),
        text=True,
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(artifact, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(tmp_name, final_path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    return final_path


def _artifact_payload(args: argparse.Namespace, result: BoundaryResult, helper_path: Path) -> dict[str, Any]:
    return {
        "schema_version": BOUNDARY_SCHEMA_VERSION,
        "artifact_created_at_utc": _utc_now(),
        "boundary": {
            "status": result.status,
            "message": result.message,
            "audit_event": result.audit_event,
            "deny_reason_codes": result.deny_reason_codes,
            "errors": result.boundary_errors,
            "contract_errors": result.contract_errors,
        },
        "request": {
            "stage": getattr(args, "stage", ""),
            "program": args.program,
            "global_scope": args.global_scope,
            "target": args.target,
            "technique": args.technique,
            "mode": args.mode,
            "ignore_time": bool(args.ignore_time),
        },
        "helper": {
            "path": str(helper_path),
            "returncode": result.helper_returncode,
            "timed_out": result.helper_timed_out,
            "stdout_excerpt": result.helper_stdout_excerpt,
            "stderr_excerpt": result.helper_stderr_excerpt,
        },
        "decision": result.decision,
    }



def _forced_deny_decision(args: argparse.Namespace) -> dict[str, Any]:
    program_slug = ""
    try:
        with open(args.program, "r", encoding="utf-8") as handle:
            program_slug = str(json.load(handle).get("program", {}).get("slug", ""))
    except Exception:
        program_slug = Path(args.program).parent.name
    return {
        "schema_version": DECISION_SCHEMA_VERSION,
        "verdict": "deny",
        "program_slug": program_slug,
        "target": args.target,
        "normalized_target": args.target,
        "target_type": _target_type_for_forced_deny(args.target),
        "technique": args.technique,
        "mode": args.mode,
        "audit_event": "PROGRAM_POLICY_DENY",
        "reasons": [],
        "errors": [args.force_deny_message or args.force_deny_code],
        "warnings": [],
        "deny_reason_codes": [args.force_deny_code],
        "program_file_sha256": _sha256_file(args.program),
        "global_scope_sha256": _sha256_file(args.global_scope),
        "decided_at_utc": _utc_now(),
    }

def evaluate_boundary(args: argparse.Namespace, helper_path: Path = DEFAULT_HELPER) -> BoundaryResult:
    helper_path = Path(helper_path)
    result = BoundaryResult(status="error", exit_code=2, message="policy boundary error")
    if getattr(args, "force_deny_code", ""):
        try:
            decision = _forced_deny_decision(args)
        except Exception as exc:
            result.message = "forced policy deny artifact preparation failed"
            result.boundary_errors.append(str(exc))
            return result
        result.decision = decision
        result.contract_errors = _validate_decision_contract(decision, 1)
        if result.contract_errors:
            result.message = "forced policy deny contract failed validation"
            return result
        result.status = "deny"
        result.exit_code = 1
        result.audit_event = decision["audit_event"]
        result.deny_reason_codes = list(decision["deny_reason_codes"])
        result.message = args.force_deny_message or "policy decision denied"
        result.helper_returncode = None
        return result

    command = _build_helper_command(args, helper_path)
    try:
        completed = subprocess.run(
            command,
            shell=False,
            timeout=args.timeout_seconds,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        result.helper_timed_out = True
        result.message = "policy helper timed out"
        result.boundary_errors.append(f"helper timed out after {args.timeout_seconds:g} seconds")
        result.helper_stdout_excerpt = _excerpt(exc.stdout)
        result.helper_stderr_excerpt = _excerpt(exc.stderr)
        return result
    except OSError as exc:
        result.message = "policy helper could not be started"
        result.boundary_errors.append(str(exc))
        return result

    result.helper_returncode = completed.returncode
    result.helper_stdout_excerpt = _excerpt(completed.stdout)
    result.helper_stderr_excerpt = _excerpt(completed.stderr)
    try:
        decision = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        result.message = "policy helper stdout was not valid JSON"
        result.boundary_errors.append(f"invalid helper JSON: {exc.msg} at line {exc.lineno}, column {exc.colno}")
        return result

    result.decision = decision
    result.contract_errors = _validate_decision_contract(decision, completed.returncode)
    if result.contract_errors:
        result.message = "policy helper decision contract failed validation"
        return result

    verdict = decision["verdict"]
    result.audit_event = decision["audit_event"]
    result.deny_reason_codes = list(decision["deny_reason_codes"])
    if verdict == "allow":
        result.status = "allow"
        result.exit_code = 0
        result.message = "policy decision allowed"
    else:
        result.status = "deny"
        result.exit_code = 1
        result.message = "policy decision denied"
    return result


def write_boundary_artifact(args: argparse.Namespace, result: BoundaryResult, helper_path: Path = DEFAULT_HELPER) -> None:
    artifact = _artifact_payload(args, result, Path(helper_path))
    artifact_path = _write_artifact(Path(args.artifact_dir), args.target, artifact)
    result.artifact_path = str(artifact_path).replace(os.sep, "/")


def _print_key_values(result: BoundaryResult) -> None:
    decision = result.decision if isinstance(result.decision, dict) else {}
    lines = {
        "POLICY_BOUNDARY_STATUS": result.status,
        "POLICY_BOUNDARY_AUDIT_EVENT": result.audit_event,
        "POLICY_BOUNDARY_ARTIFACT": result.artifact_path,
        "POLICY_BOUNDARY_DENY_REASON_CODES": ",".join(result.deny_reason_codes),
        "POLICY_BOUNDARY_MESSAGE": result.message,
        "POLICY_BOUNDARY_PROGRAM_HASH": str(decision.get("program_file_sha256") or ""),
        "POLICY_BOUNDARY_GLOBAL_HASH": str(decision.get("global_scope_sha256") or ""),
        "POLICY_BOUNDARY_DECIDED_AT_UTC": str(decision.get("decided_at_utc") or ""),
    }
    for key, value in lines.items():
        print(f"{key}={shlex.quote(value)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Offline policy boundary wrapper for program policy decisions.",
    )
    parser.add_argument("--stage", default="", help="Recon stage/context name for evidence metadata.")
    parser.add_argument("--program", required=True, help="Path to program scope JSON.")
    parser.add_argument("--global-scope", required=True, help="Path to global scope allowlist.")
    parser.add_argument("--target", required=True, help="Target to evaluate.")
    parser.add_argument("--technique", required=True, choices=sorted(TECHNIQUES), help="Technique tag to evaluate.")
    parser.add_argument("--mode", required=True, choices=sorted(MODES), help="Decision mode.")
    parser.add_argument("--artifact-dir", required=True, help="Directory for boundary evidence artifacts.")
    parser.add_argument("--force-deny-code", default="", help="Internal use: write a local fail-closed deny artifact without invoking helper.")
    parser.add_argument("--force-deny-message", default="", help="Internal use: message for --force-deny-code.")
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Policy helper timeout. Default: {DEFAULT_TIMEOUT_SECONDS:g}",
    )
    parser.add_argument(
        "--ignore-time",
        action="store_true",
        help="Forwarded to the helper for stable offline tests/examples only.",
    )
    return parser


def main(argv: list[str] | None = None, helper_path: Path = DEFAULT_HELPER) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.timeout_seconds <= 0:
        parser.error("--timeout-seconds must be greater than 0")

    result = evaluate_boundary(args, helper_path=helper_path)
    try:
        write_boundary_artifact(args, result, helper_path=helper_path)
    except OSError as exc:
        result.status = "error"
        result.exit_code = 2
        result.audit_event = "PROGRAM_POLICY_BOUNDARY_ERROR"
        result.deny_reason_codes = []
        result.message = "policy boundary artifact write failed"
        result.boundary_errors.append(str(exc))
    _print_key_values(result)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
