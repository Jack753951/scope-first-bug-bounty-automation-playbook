#!/usr/bin/env python3
"""Offline bridge from Wave 1A candidate seeds to candidate-review packets.

This helper consumes the reviewed/committed Wave 1A JSONL fixture contract via
``import_wave1a_metadata_observations.py``, converts only manual-review candidate
seeds into ``finding/1.0`` candidate fixtures, validates those fixtures, and
projects them through the existing trial candidate-review packet vocabulary.

It is an offline bridge only: no target interaction, no network I/O, no
subprocess execution, no file writes by default, no report drafting/submission,
and no promotion to confirmed/verified/reportable states.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "wave1a_candidate_review_bridge/0.1-trial"
FORBIDDEN_PROMOTIONS = {"confirmed", "verified", "reportable", "accepted"}
LIVE_TARGET_FLAGS = frozenset({"--target", "--url", "--host", "--scope", "--live"})


@dataclass(frozen=True)
class BridgeError:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


def _load_script_module(filename: str, module_name: str) -> Any:
    target = Path(__file__).resolve().parent / filename
    existing = sys.modules.get(module_name)
    if existing is not None:
        return existing
    spec = importlib.util.spec_from_file_location(module_name, target)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{filename} could not be located")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def _importer() -> Any:
    return _load_script_module("import_wave1a_metadata_observations.py", "_wave1a_bridge_importer")


def _packet_builder() -> Any:
    return _load_script_module("build_candidate_review_packet.py", "_wave1a_bridge_candidate_packet_builder")


def _safety(*, output_file_write: bool = False) -> dict[str, bool]:
    return {
        "network_io": False,
        "subprocess_execution": False,
        "target_touching": False,
        "output_file_write": output_file_write,
        "promotes_findings": False,
        "report_drafting": False,
        "report_submission": False,
    }


def _empty_summary() -> dict[str, int]:
    return {
        "candidate_seed_count": 0,
        "finding_fixture_count": 0,
        "candidate_review_packet_count": 0,
        "error_count": 0,
    }


def _error_payload(errors: list[BridgeError], *, input_path: str | None = None) -> dict[str, Any]:
    summary = _empty_summary()
    summary["error_count"] = len(errors)
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "error",
        "input_path": input_path,
        "summary": summary,
        "source_schema_versions": [
            "wave1a_metadata_observations/0.1-trial",
            "finding/1.0",
            "candidate_review_packet/0.1-trial",
        ],
        "finding_fixture": [],
        "candidate_review_packet": {},
        "errors": [error.as_dict() for error in errors],
        "safety": _safety(),
    }


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def _short_seed_id(seed: dict[str, Any]) -> str:
    basis = json.dumps(seed, sort_keys=True, separators=(",", ":"))
    return _sha256_text(basis)[:16]


def _title_for(seed: dict[str, Any]) -> str:
    relationship = seed.get("relationship")
    if relationship == "directory_listing_candidate":
        return "Wave 1A local-lab candidate: directory listing metadata lead"
    if relationship == "api_docs_candidate":
        return "Wave 1A local-lab candidate: API documentation metadata lead"
    return "Wave 1A local-lab candidate: metadata lead"


def _summary_for(seed: dict[str, Any]) -> str:
    target = seed.get("target") if isinstance(seed.get("target"), dict) else {}
    url = target.get("url") if isinstance(target.get("url"), str) else "unknown-url"
    relationship = seed.get("relationship")
    if relationship == "directory_listing_candidate":
        return (
            f"Offline Wave 1A metadata observation for {url} suggests a possible directory-listing lead. "
            "This is scanner-output-only and requires authorized manual verification before any finding/report claim."
        )
    if relationship == "api_docs_candidate":
        return (
            f"Offline Wave 1A metadata observation for {url} suggests a possible exposed API documentation lead. "
            "This is scanner-output-only and requires authorized manual verification before any finding/report claim."
        )
    return (
        f"Offline Wave 1A metadata observation for {url} produced a low-risk manual-review lead. "
        "This is scanner-output-only and not a finding."
    )


def _classifications_for(seed: dict[str, Any]) -> dict[str, Any]:
    relationship = seed.get("relationship")
    if relationship == "directory_listing_candidate":
        return {
            "cwe": ["CWE-548"],
            "owasp": ["OWASP Top 10 2021 A05 Security Misconfiguration"],
        }
    if relationship == "api_docs_candidate":
        return {
            "cwe": ["CWE-200"],
            "owasp": ["OWASP Top 10 2021 A05 Security Misconfiguration"],
        }
    return {"cwe": [], "owasp": []}


def _remediation_for(seed: dict[str, Any]) -> str:
    relationship = seed.get("relationship")
    if relationship == "directory_listing_candidate":
        return (
            "If manual review confirms unintended directory listing, disable directory indexes, restrict access, "
            "and remove sensitive artifacts from the exposed path."
        )
    if relationship == "api_docs_candidate":
        return (
            "If manual review confirms unintended API documentation exposure, restrict documentation access, "
            "remove sensitive examples, and align visibility with the program's intended deployment policy."
        )
    return "If manual review confirms unintended exposure, restrict access and document the intended visibility policy."


def _verification_guidance_for(seed: dict[str, Any]) -> str:
    target = seed.get("target") if isinstance(seed.get("target"), dict) else {}
    url = target.get("url") if isinstance(target.get("url"), str) else "the candidate URL"
    return (
        f"Manual-review only: confirm {url} is in authorized local-lab or program scope, capture a redacted "
        "metadata-only evidence file, confirm impact with the applicable rules, and keep this out of reports unless "
        "a human reviewer promotes it after verification."
    )


def _finding_from_seed(seed: dict[str, Any]) -> dict[str, Any]:
    target = seed.get("target") if isinstance(seed.get("target"), dict) else {}
    url = target.get("url") if isinstance(target.get("url"), str) else "http://invalid.local/"
    module_id = seed.get("module_id") if isinstance(seed.get("module_id"), str) else "level1.metadata"
    run_id = seed.get("run_id") if isinstance(seed.get("run_id"), str) else "wave1a-bridge"
    relationship = seed.get("relationship") if isinstance(seed.get("relationship"), str) else "metadata_candidate"
    seed_hash = _short_seed_id(seed)
    policy_hash = _sha256_text(f"wave1a-candidate-review-bridge:{module_id}:{relationship}:{url}")
    return {
        "schema_version": "finding/1.0",
        "id": f"wave1a.{relationship}.{seed_hash}",
        "status": "candidate",
        "title": _title_for(seed),
        "summary": _summary_for(seed),
        "target": {"type": "url", "value": url},
        "source": {
            "module_id": module_id,
            "run_id": run_id,
            "policy_decision_sha256": policy_hash,
        },
        "severity_hint": "low" if relationship == "directory_listing_candidate" else "info",
        "confidence": "low",
        "triage": {
            "scanner_output_only": True,
            "manual_verification_required": True,
        },
        "evidence": [],
        "references": ["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
        "classifications": _classifications_for(seed),
        "remediation": _remediation_for(seed),
        "verification_guidance": _verification_guidance_for(seed),
    }


def _check_no_promotional_status(payload: dict[str, Any]) -> None:
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "status" and isinstance(child, str) and child.lower() in FORBIDDEN_PROMOTIONS:
                    raise ValueError(f"forbidden promotional status: {child}")
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload)


def _validate_findings(findings: list[dict[str, Any]]) -> list[BridgeError]:
    builder = _packet_builder()
    errors: list[BridgeError] = []
    for index, finding in enumerate(findings):
        result = builder._validate_data(finding, "finding")
        if getattr(result, "verdict", "deny") != "allow":
            detail = "; ".join(getattr(result, "errors", []) or [])
            errors.append(
                BridgeError(
                    "GENERATED_FINDING_VALIDATION_FAILED",
                    f"finding_fixture[{index}]",
                    detail or "generated finding failed validation",
                )
            )
    return errors


def _build_packet_from_findings(findings: list[dict[str, Any]]) -> dict[str, Any]:
    builder = _packet_builder()
    projected = [builder._project_finding(finding) for finding in findings]
    projected.sort(key=builder._finding_sort_key)
    return builder._packet_payload([], projected, 1)


def build_bridge(repo_root: str | Path, input_path: str, *, run_id: str = "wave1a-bridge") -> dict[str, Any]:
    imported = _importer().import_observations(Path(repo_root), input_path, run_id=run_id)
    if imported.get("status") != "ok":
        return _error_payload(
            [
                BridgeError(
                    "IMPORTER_STAGE_FAILED",
                    "importer",
                    "Wave 1A observation import failed; candidate-review bridge failed closed",
                )
            ],
            input_path=input_path,
        )

    seeds = imported.get("candidate_seeds") if isinstance(imported.get("candidate_seeds"), list) else []
    findings = [_finding_from_seed(seed) for seed in seeds if isinstance(seed, dict)]
    findings.sort(key=lambda finding: (finding["target"]["value"], finding["id"]))
    validation_errors = _validate_findings(findings)
    if validation_errors:
        return _error_payload(validation_errors, input_path=input_path)

    packet = _build_packet_from_findings(findings)
    if packet.get("status") != "ok":
        return _error_payload(
            [BridgeError("CANDIDATE_PACKET_STAGE_FAILED", "candidate_review_packet", "candidate packet projection failed closed")],
            input_path=input_path,
        )

    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "ok",
        "input_path": input_path,
        "summary": {
            "candidate_seed_count": len(seeds),
            "finding_fixture_count": len(findings),
            "candidate_review_packet_count": packet.get("summary", {}).get("candidate_count", 0),
            "error_count": 0,
        },
        "source_schema_versions": [
            imported.get("schema_version"),
            "finding/1.0",
            packet.get("schema_version"),
        ],
        "finding_fixture": findings,
        "candidate_review_packet": packet,
        "errors": [],
        "safety": _safety(),
    }
    _check_no_promotional_status(payload)
    return payload


def _live_flag_errors(argv: list[str]) -> list[BridgeError]:
    errors: list[BridgeError] = []
    for index, arg in enumerate(argv):
        name = arg.split("=", 1)[0]
        if name in LIVE_TARGET_FLAGS:
            errors.append(
                BridgeError(
                    "LIVE_TARGET_FLAG_NOT_ALLOWED",
                    f"argv[{index}]",
                    "live target flags are not accepted by the offline Wave 1A candidate-review bridge",
                )
            )
    return errors


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    live_errors = _live_flag_errors(argv)
    if live_errors:
        print(json.dumps(_error_payload(live_errors), indent=2, sort_keys=True))
        return 2

    parser = argparse.ArgumentParser(description="Build an offline Wave 1A candidate-review bridge artifact")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--run-id", default="wave1a-bridge")
    parser.add_argument("--json", action="store_true", help="Accepted for compatibility; output is always JSON")
    args = parser.parse_args(argv)

    payload = build_bridge(Path(args.repo_root), args.input, run_id=args.run_id)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("status") == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
