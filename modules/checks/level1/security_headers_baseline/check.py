#!/usr/bin/env python3
"""Offline fixture-only security header baseline check."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MODULE_ID = "level1.security_headers_baseline"
FIXTURE_VERSION = "security_headers_baseline_input/1"
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
HEADER_NAME_RE = re.compile(r"^[A-Za-z0-9!#$%&'*+\-.^_`|~]{1,80}$")
HSTS_MAX_AGE_RE = re.compile(r"^max-age=([0-9]+)$")
HSTS_MIN_MAX_AGE = 15552000
REFERRER_POLICY_ALLOWLIST = {
    "no-referrer",
    "no-referrer-when-downgrade",
    "origin",
    "origin-when-cross-origin",
    "same-origin",
    "strict-origin",
    "strict-origin-when-cross-origin",
}
REFERENCES = [
    "https://owasp.org/www-project-secure-headers/",
    "https://owasp.org/www-project-application-security-verification-standard/",
]
CLASSIFICATIONS = {
    "cwe": ["CWE-693"],
    "owasp": ["OWASP Secure Headers Project", "OWASP ASVS V14.4"],
}


class SecurityHeadersBaselineError(Exception):
    """Base exception for typed CLI failures."""


class FixtureShapeError(SecurityHeadersBaselineError):
    """Raised when the offline input fixture does not match the closed shape."""


class ParameterError(SecurityHeadersBaselineError):
    """Raised when caller-supplied provenance arguments are invalid."""


RULES = {
    "security_headers_baseline.csp.missing": {
        "header_name": "Content-Security-Policy",
        "severity_hint": "medium",
        "title": "Content-Security-Policy header is missing",
        "summary": "Rule security_headers_baseline.csp.missing observed that the fixture lacks the Content-Security-Policy header. This is a candidate observation only and requires manual verification.",
        "remediation": "Add the Content-Security-Policy header using the application-approved baseline. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the Content-Security-Policy behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
    "security_headers_baseline.csp.unsafe_inline": {
        "header_name": "Content-Security-Policy",
        "severity_hint": "medium",
        "title": "Content-Security-Policy header includes a weak directive",
        "summary": "Rule security_headers_baseline.csp.unsafe_inline observed that the Content-Security-Policy header includes a directive that weakens script protections. This is a candidate observation only and requires manual verification.",
        "remediation": "Tighten the Content-Security-Policy policy to remove the weak directive where application design permits. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the Content-Security-Policy behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
    "security_headers_baseline.x_frame_options.missing": {
        "header_name": "X-Frame-Options",
        "severity_hint": "low",
        "title": "X-Frame-Options header is missing",
        "summary": "Rule security_headers_baseline.x_frame_options.missing observed that the fixture lacks the X-Frame-Options header. This is a candidate observation only and requires manual verification.",
        "remediation": "Add the X-Frame-Options header using the application-approved baseline. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the X-Frame-Options behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
    "security_headers_baseline.x_frame_options.invalid_value": {
        "header_name": "X-Frame-Options",
        "severity_hint": "low",
        "title": "X-Frame-Options header does not meet the baseline",
        "summary": "Rule security_headers_baseline.x_frame_options.invalid_value observed that the X-Frame-Options header is present but does not match the approved baseline. This is a candidate observation only and requires manual verification.",
        "remediation": "Update the X-Frame-Options header to match the application-approved baseline. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the X-Frame-Options behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
    "security_headers_baseline.x_content_type_options.missing": {
        "header_name": "X-Content-Type-Options",
        "severity_hint": "low",
        "title": "X-Content-Type-Options header is missing",
        "summary": "Rule security_headers_baseline.x_content_type_options.missing observed that the fixture lacks the X-Content-Type-Options header. This is a candidate observation only and requires manual verification.",
        "remediation": "Add the X-Content-Type-Options header using the application-approved baseline. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the X-Content-Type-Options behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
    "security_headers_baseline.x_content_type_options.invalid_value": {
        "header_name": "X-Content-Type-Options",
        "severity_hint": "low",
        "title": "X-Content-Type-Options header does not meet the baseline",
        "summary": "Rule security_headers_baseline.x_content_type_options.invalid_value observed that the X-Content-Type-Options header is present but does not match the approved baseline. This is a candidate observation only and requires manual verification.",
        "remediation": "Update the X-Content-Type-Options header to match the application-approved baseline. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the X-Content-Type-Options behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
    "security_headers_baseline.hsts.missing": {
        "header_name": "Strict-Transport-Security",
        "severity_hint": "medium",
        "title": "Strict-Transport-Security header is missing",
        "summary": "Rule security_headers_baseline.hsts.missing observed that the fixture lacks the Strict-Transport-Security header. This is a candidate observation only and requires manual verification.",
        "remediation": "Add the Strict-Transport-Security header using the application-approved baseline. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the Strict-Transport-Security behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
    "security_headers_baseline.hsts.max_age_too_low": {
        "header_name": "Strict-Transport-Security",
        "severity_hint": "medium",
        "title": "Strict-Transport-Security header does not meet the baseline",
        "summary": "Rule security_headers_baseline.hsts.max_age_too_low observed that the Strict-Transport-Security header does not meet the approved duration baseline. This is a candidate observation only and requires manual verification.",
        "remediation": "Update the Strict-Transport-Security header to match the application-approved duration baseline. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the Strict-Transport-Security behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
    "security_headers_baseline.hsts.include_subdomains_missing": {
        "header_name": "Strict-Transport-Security",
        "severity_hint": "medium",
        "title": "Strict-Transport-Security header does not meet the baseline",
        "summary": "Rule security_headers_baseline.hsts.include_subdomains_missing observed that the Strict-Transport-Security header does not apply the approved subdomain baseline. This is a candidate observation only and requires manual verification.",
        "remediation": "Update the Strict-Transport-Security header to match the application-approved subdomain baseline. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the Strict-Transport-Security behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
    "security_headers_baseline.referrer_policy.missing": {
        "header_name": "Referrer-Policy",
        "severity_hint": "low",
        "title": "Referrer-Policy header is missing",
        "summary": "Rule security_headers_baseline.referrer_policy.missing observed that the fixture lacks the Referrer-Policy header. This is a candidate observation only and requires manual verification.",
        "remediation": "Add the Referrer-Policy header using the application-approved baseline. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the Referrer-Policy behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
    "security_headers_baseline.referrer_policy.invalid_value": {
        "header_name": "Referrer-Policy",
        "severity_hint": "low",
        "title": "Referrer-Policy header does not meet the baseline",
        "summary": "Rule security_headers_baseline.referrer_policy.invalid_value observed that the Referrer-Policy header is present but does not match the approved baseline. This is a candidate observation only and requires manual verification.",
        "remediation": "Update the Referrer-Policy header to match the application-approved baseline. Review compatibility and deployment scope before promoting this candidate to a report finding.",
        "verification_guidance": "Manually inspect an authorized response and confirm the Referrer-Policy behavior against OWASP Secure Headers Project and ASVS V14.4 before reporting.",
    },
}


def _reject_unknown_keys(data: dict[str, Any], allowed: set[str], where: str) -> None:
    for key in sorted(set(data) - allowed):
        raise FixtureShapeError(f"{where}.{key} is not allowed")


def _require_keys(data: dict[str, Any], required: set[str], where: str) -> None:
    for key in sorted(required - set(data)):
        raise FixtureShapeError(f"{where}.{key} is required")


def _validate_fixture(fixture: Any) -> dict[str, Any]:
    if not isinstance(fixture, dict):
        raise FixtureShapeError("fixture must be an object")
    _reject_unknown_keys(fixture, {"fixture_version", "target", "status_code", "headers"}, "fixture")
    _require_keys(fixture, {"fixture_version", "target", "status_code", "headers"}, "fixture")

    if fixture.get("fixture_version") != FIXTURE_VERSION:
        raise FixtureShapeError(f"fixture.fixture_version must be {FIXTURE_VERSION}")

    target = fixture.get("target")
    if not isinstance(target, dict):
        raise FixtureShapeError("fixture.target must be an object")
    _reject_unknown_keys(target, {"type", "value"}, "fixture.target")
    _require_keys(target, {"type", "value"}, "fixture.target")
    if target.get("type") not in {"url", "domain"}:
        raise FixtureShapeError("fixture.target.type must be url or domain")
    if not isinstance(target.get("value"), str) or not 1 <= len(target.get("value", "")) <= 500:
        raise FixtureShapeError("fixture.target.value must be a string with length 1..500")

    status_code = fixture.get("status_code")
    if isinstance(status_code, bool) or not isinstance(status_code, int) or not 100 <= status_code <= 599:
        raise FixtureShapeError("fixture.status_code must be an integer in 100..599")

    headers = fixture.get("headers")
    if not isinstance(headers, list):
        raise FixtureShapeError("fixture.headers must be a list")
    for idx, item in enumerate(headers):
        where = f"fixture.headers[{idx}]"
        if not isinstance(item, dict):
            raise FixtureShapeError(f"{where} must be an object")
        _reject_unknown_keys(item, {"name", "value"}, where)
        _require_keys(item, {"name", "value"}, where)
        name = item.get("name")
        value = item.get("value")
        if not isinstance(name, str) or HEADER_NAME_RE.fullmatch(name) is None:
            raise FixtureShapeError(f"{where}.name is not a safe header field name")
        if not isinstance(value, str) or len(value) > 4096:
            raise FixtureShapeError(f"{where}.value must be a string with length <=4096")
    return fixture


def _validate_parameters(run_id: Any, policy_decision_sha256: Any) -> None:
    if not isinstance(run_id, str) or RUN_ID_RE.fullmatch(run_id) is None:
        raise ParameterError("run_id must match ^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")
    if not isinstance(policy_decision_sha256, str) or SHA256_RE.fullmatch(policy_decision_sha256) is None:
        raise ParameterError("policy_decision_sha256 must be 64 lowercase hex")


def _headers_by_name(fixture: dict[str, Any]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for item in fixture["headers"]:
        grouped.setdefault(item["name"].lower(), []).append(item["value"])
    return grouped


def _make_finding(rule_id: str, target: dict[str, str], run_id: str, policy_decision_sha256: str) -> dict[str, Any]:
    rule = RULES[rule_id]
    return {
        "schema_version": "finding/1.0",
        "id": rule_id,
        "status": "candidate",
        "title": rule["title"],
        "summary": rule["summary"],
        "target": {
            "type": target["type"],
            "value": target["value"],
        },
        "source": {
            "module_id": MODULE_ID,
            "run_id": run_id,
            "policy_decision_sha256": policy_decision_sha256,
        },
        "severity_hint": rule["severity_hint"],
        "confidence": "high",
        "triage": {
            "scanner_output_only": True,
            "manual_verification_required": True,
        },
        "evidence": [],
        "references": list(REFERENCES),
        "classifications": {
            "cwe": list(CLASSIFICATIONS["cwe"]),
            "owasp": list(CLASSIFICATIONS["owasp"]),
        },
        "remediation": rule["remediation"],
        "verification_guidance": rule["verification_guidance"],
    }


def _has_hsts_min_max_age(values: list[str]) -> bool:
    for value in values:
        for directive in (part.strip() for part in value.split(";")):
            match = HSTS_MAX_AGE_RE.fullmatch(directive)
            if match and int(match.group(1)) >= HSTS_MIN_MAX_AGE:
                return True
    return False


def _has_hsts_include_subdomains(values: list[str]) -> bool:
    for value in values:
        if any(part.strip() == "includeSubDomains" for part in value.split(";")):
            return True
    return False


def _rule_ids_for_headers(headers: dict[str, list[str]]) -> list[str]:
    rule_ids: list[str] = []

    csp = headers.get("content-security-policy", [])
    if not csp:
        rule_ids.append("security_headers_baseline.csp.missing")
    elif any("unsafe-inline" in value for value in csp):
        rule_ids.append("security_headers_baseline.csp.unsafe_inline")

    xfo = headers.get("x-frame-options", [])
    if not xfo:
        rule_ids.append("security_headers_baseline.x_frame_options.missing")
    elif not any(value.strip() in {"DENY", "SAMEORIGIN"} for value in xfo):
        rule_ids.append("security_headers_baseline.x_frame_options.invalid_value")

    xcto = headers.get("x-content-type-options", [])
    if not xcto:
        rule_ids.append("security_headers_baseline.x_content_type_options.missing")
    elif not any(value.strip() == "nosniff" for value in xcto):
        rule_ids.append("security_headers_baseline.x_content_type_options.invalid_value")

    hsts = headers.get("strict-transport-security", [])
    if not hsts:
        rule_ids.append("security_headers_baseline.hsts.missing")
    else:
        if not _has_hsts_min_max_age(hsts):
            rule_ids.append("security_headers_baseline.hsts.max_age_too_low")
        if not _has_hsts_include_subdomains(hsts):
            rule_ids.append("security_headers_baseline.hsts.include_subdomains_missing")

    referrer = headers.get("referrer-policy", [])
    if not referrer:
        rule_ids.append("security_headers_baseline.referrer_policy.missing")
    elif not any(value.strip() in REFERRER_POLICY_ALLOWLIST for value in referrer):
        rule_ids.append("security_headers_baseline.referrer_policy.invalid_value")

    return rule_ids


def evaluate(fixture: dict, *, run_id: str, policy_decision_sha256: str) -> list[dict]:
    """Evaluate a closed offline fixture and return candidate finding dicts."""
    _validate_parameters(run_id, policy_decision_sha256)
    valid_fixture = _validate_fixture(fixture)
    headers = _headers_by_name(valid_fixture)
    return [
        _make_finding(rule_id, valid_fixture["target"], run_id, policy_decision_sha256)
        for rule_id in _rule_ids_for_headers(headers)
    ]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate an offline security headers fixture")
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--policy-decision-sha256", required=True)
    args = parser.parse_args(argv)

    try:
        findings = evaluate(
            _load_json(args.fixture),
            run_id=args.run_id,
            policy_decision_sha256=args.policy_decision_sha256,
        )
    except SecurityHeadersBaselineError as exc:
        print(f"{exc.__class__.__name__}: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"FixtureLoadError: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(findings, ensure_ascii=False, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
