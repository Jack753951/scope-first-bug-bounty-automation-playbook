#!/usr/bin/env python3
"""Normalize public disclosed-report text into offline, sanitized records.

This helper is deliberately file-input only. It never fetches URLs, logs in,
uses cookies, scans targets, or authorizes live testing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PRIVATE_SOURCE_RE = re.compile(r"sign in|login|captcha|cloudflare|private program|please authenticate", re.I)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
SECRET_RE = re.compile(r"\b(?:h1_api_token|api[_-]?token|secret|bearer)[A-Za-z0-9_:\-]{8,}\b", re.I)
OTP_RE = re.compile(r"\b(?:otp|code)[:\s-]*\d{4,8}\b", re.I)
ROUTE_RE = re.compile(r"(?<![A-Za-z0-9])/[A-Za-z0-9_./{}:*-]+")

CLASS_RULES = [
    ("idor", re.compile(r"\bidor\b|\bbola\b|object ownership|owned object", re.I)),
    ("authorization_bypass", re.compile(r"auth(?:orization|z)|access-control|role|permission|tenant boundary", re.I)),
    ("ssrf", re.compile(r"\bssrf\b|server-side request forgery|callback", re.I)),
    ("upload_parser", re.compile(r"upload|parser|file traversal|path traversal", re.I)),
    ("oauth_oidc", re.compile(r"oauth|oidc|saml|scim|sso", re.I)),
]

PRIMITIVE_RULES = [
    ("org_role_invite_authz", re.compile(r"organization|workspace|team|invite|role", re.I)),
    ("ssrf_callback_marker", re.compile(r"\bssrf\b|callback|collaborator|oast", re.I)),
    ("api_object_boundary", re.compile(r"\bapi\b|object|tenant|idor|bola", re.I)),
    ("webhook_boundary", re.compile(r"webhook", re.I)),
    ("oauth_or_sso_boundary", re.compile(r"oauth|oidc|saml|scim|sso", re.I)),
]

SURFACE_RULES = {
    "organization": re.compile(r"organization|org\b", re.I),
    "workspace": re.compile(r"workspace", re.I),
    "team": re.compile(r"team", re.I),
    "invitation": re.compile(r"invite|invitation", re.I),
    "role": re.compile(r"role|permission", re.I),
    "api": re.compile(r"\bapi\b|graphql|openapi|swagger", re.I),
    "webhook": re.compile(r"webhook", re.I),
    "api_key": re.compile(r"api token|api key|token", re.I),
    "sso": re.compile(r"sso|saml|scim|oauth|oidc", re.I),
    "audit_log": re.compile(r"audit", re.I),
}

DEFAULT_BLOCKED_ACTIONS = [
    "live_target_contact_without_scope_and_lane_gate",
    "customer_or_non_owned_data_access",
    "secret_cookie_token_or_otp_capture",
    "high_volume_scanning_or_fuzzing",
    "report_submission_or_finding_promotion",
]


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def sanitize_text(text: str) -> str:
    text = EMAIL_RE.sub("[redacted_email]", text)
    text = SECRET_RE.sub("[redacted_secret]", text)
    text = OTP_RE.sub("[redacted_otp]", text)
    return text


def _summary(text: str, limit: int = 1200) -> str:
    compact = re.sub(r"\s+", " ", sanitize_text(text)).strip()
    return compact[:limit]


def _matches(rules: list[tuple[str, re.Pattern[str]]], text: str) -> list[str]:
    return [name for name, pattern in rules if pattern.search(text)]


def _proof_shapes(text: str) -> list[str]:
    shapes: list[str] = []
    if re.search(r"account\s+a|account\s+b|two owned|owned test accounts", text, re.I):
        shapes.append("owned_account_a_b")
    if re.search(r"owned object|workspace object|tenant", text, re.I):
        shapes.append("owned_object")
    if re.search(r"callback|collaborator|oast", text, re.I):
        shapes.append("operator_controlled_callback_marker")
    if re.search(r"screenshot|minimal str|steps to reproduce|\bstr\b", text, re.I):
        shapes.append("clear_str")
    return _unique(shapes)


def _impact_shapes(text: str) -> list[str]:
    impacts: list[str] = []
    if re.search(r"tenant boundary|cross-tenant|organization", text, re.I):
        impacts.append("tenant_boundary")
    if re.search(r"role|permission|low-privilege", text, re.I):
        impacts.append("privilege_boundary")
    if re.search(r"invite|member", text, re.I):
        impacts.append("membership_or_invitation")
    if re.search(r"ssrf|callback", text, re.I):
        impacts.append("network_callback_observation")
    return _unique(impacts)


def _quality_signals(text: str) -> list[str]:
    signals: list[str] = []
    if re.search(r"minimal str|steps to reproduce|\bstr\b", text, re.I):
        signals.append("clear_str")
    if re.search(r"screenshot", text, re.I):
        signals.append("screenshots")
    if re.search(r"impact", text, re.I):
        signals.append("business_impact")
    if re.search(r"remediation|fix", text, re.I):
        signals.append("remediation_pattern")
    if re.search(r"severity", text, re.I):
        signals.append("severity_signal")
    return _unique(signals)


def _safety_tags(text: str, private_source: bool) -> list[str]:
    tags = ["passive_public_source_only", "target-touching required"]
    if private_source:
        tags.append("login_or_captcha_or_private_source")
    if re.search(r"customer|non-owned|private data", text, re.I):
        tags.append("customer_data_risk")
    if re.search(r"callback|ssrf|oast|collaborator", text, re.I):
        tags.append("callback_risk")
    return _unique(tags)


def normalize_report_text(text: str, *, source: str, url: str, title: str = "") -> dict[str, Any]:
    private_source = bool(PRIVATE_SOURCE_RE.search(text) or PRIVATE_SOURCE_RE.search(url))
    if private_source:
        return {
            "schema_version": "disclosed_report/0.1",
            "source": source,
            "url": url,
            "title": title or url,
            "source_visibility": "needs_operator_or_browser_review",
            "status": "needs_operator_or_browser_review",
            "target_touching": False,
            "summary": "[private_or_login_gated_content_not_ingested]",
            "vulnerability_classes": [],
            "primitives": [],
            "proof_shapes": [],
            "impact_shapes": [],
            "product_surface_keywords": [],
            "route_patterns": [],
            "report_quality_signals": [],
            "safety_tags": _safety_tags(text, private_source=True),
            "blocked_actions": _unique(DEFAULT_BLOCKED_ACTIONS + ["do_not_ingest_private_logged_in_content"]),
        }

    sanitized = sanitize_text(text)
    surfaces = [name for name, pattern in SURFACE_RULES.items() if pattern.search(sanitized)]
    return {
        "schema_version": "disclosed_report/0.1",
        "source": source,
        "url": url,
        "title": title or url,
        "source_visibility": "public",
        "status": "ok",
        "target_touching": False,
        "summary": _summary(sanitized),
        "vulnerability_classes": _matches(CLASS_RULES, sanitized),
        "primitives": _matches(PRIMITIVE_RULES, sanitized),
        "proof_shapes": _proof_shapes(sanitized),
        "impact_shapes": _impact_shapes(sanitized),
        "product_surface_keywords": _unique(surfaces),
        "route_patterns": _unique([route.rstrip(".,);]") for route in ROUTE_RE.findall(sanitized)])[:20],
        "report_quality_signals": _quality_signals(sanitized),
        "safety_tags": _safety_tags(sanitized, private_source=False),
        "blocked_actions": DEFAULT_BLOCKED_ACTIONS,
    }


def _load_input_rows(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    payload = json.loads(text)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and "records" in payload:
        return payload["records"]
    if isinstance(payload, dict):
        return [payload]
    raise ValueError(f"Unsupported disclosed-report input shape: {path}")


def ingest_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    records = [
        normalize_report_text(
            str(row.get("text") or row.get("body") or row.get("summary") or ""),
            source=str(row.get("source") or "unknown"),
            url=str(row.get("url") or "unknown"),
            title=str(row.get("title") or row.get("url") or "untitled"),
        )
        for row in rows
    ]
    return {
        "schema_version": "disclosed_report_batch/0.1",
        "target_touching": False,
        "boundary": "Offline passive disclosed-report normalization only; no live target contact is authorized.",
        "record_count": len(records),
        "records": records,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Normalize offline public disclosed-report text into sanitized JSON records.")
    parser.add_argument("--input", required=True, help="Input JSON or JSONL rows with source/url/title/text")
    parser.add_argument("--output", required=True, help="Output normalized JSON batch")
    args = parser.parse_args(argv)

    rows = _load_input_rows(Path(args.input))
    payload = ingest_rows(rows)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path} records={payload['record_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
