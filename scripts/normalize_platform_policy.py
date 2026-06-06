#!/usr/bin/env python3
"""Normalize passive bounty-platform policy text into candidate-only facts.

This helper is intentionally offline: it reads already-captured visible text from
Kali/noVNC/CDP or a public-policy copy and emits a compact JSON normalization. It
never opens URLs, scans targets, authenticates, or authorizes live testing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "platform_policy_normalization/0.1"

GATE_PATTERNS = {
    "captcha": re.compile(r"\bcaptcha\b", re.I),
    "otp": re.compile(r"\botp\b|one[- ]?time password", re.I),
    "2fa": re.compile(r"\b2fa\b|mfa|multi[- ]factor", re.I),
    "verification code": re.compile(r"verification code|email verification|verify your email", re.I),
    "phone": re.compile(r"\bphone\b|sms", re.I),
    "payment": re.compile(r"payment|credit card|billing", re.I),
    "kyc": re.compile(r"\bkyc\b|identity verification", re.I),
    "api token": re.compile(r"api token|personal access token|secret key", re.I),
}

CANDIDATE_CLASS_PATTERNS = {
    "org_role_invite_authz": re.compile(r"organization|workspace|team|member|invite|role|rbac|audit", re.I),
    "oauth_oidc": re.compile(r"oauth|oidc|saml|sso|scim|redirect_uri|client_id", re.I),
    "api_token_or_webhook_boundary": re.compile(r"api token|webhook|integration|secret key", re.I),
    "api_direct_object_authz": re.compile(r"api|graphql|openapi|swagger|direct url|idor|bola", re.I),
    "source_or_plugin_review": re.compile(r"github\.com|source code|plugin|sdk|cli|gateway", re.I),
}

STOP_BEFORE_DEFAULT = [
    "config/scope.txt change or programs/<slug>/scope.json creation/broadening",
    "account signup/login/OTP/CAPTCHA/password/phone/payment/KYC",
    "api token, OAuth app, webhook, integration, or scarce-resource creation",
    "customer or non-owned data access",
    "scanner_fuzzer_dast_or_large_scale_discovery",
    "SSRF/OAST/callback/exploit attempts",
    "any live target testing beyond passive policy/public-doc reading",
]

OUT_OF_SCOPE_HINTS = [
    "out of scope",
    "denial of service",
    "automated scanning",
    "social engineering",
    "phishing",
    "spam",
    "physical",
    "brute force",
]

ASSET_RE = re.compile(
    r"(?P<asset>(?:https?://)?(?:\*\.)?(?:[A-Za-z0-9_-]+\.)+[A-Za-z]{2,}(?:/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]*)?|github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)",
    re.I,
)


def _clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip(" \t-•|;,")


def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"https?://", "", value)
    value = re.sub(r"[^a-z0-9]+", "_", value).strip("_")
    return value or "unknown"


def _context(lines: list[str], idx: int, radius: int = 1) -> str:
    start = max(0, idx - radius)
    end = min(len(lines), idx + radius + 1)
    return " | ".join(lines[start:end])[:600]


def _extract_assets(lines: list[str]) -> list[dict[str, str]]:
    assets: dict[str, dict[str, str]] = {}
    in_scope_zone = False
    out_scope_zone = False
    for idx, raw in enumerate(lines):
        line = _clean_line(raw)
        low = line.lower()
        if not line:
            continue
        if "out of scope" in low:
            out_scope_zone = True
            in_scope_zone = False
        elif "in scope" in low or "eligible" in low:
            in_scope_zone = True
            out_scope_zone = False
        for match in ASSET_RE.finditer(line):
            asset = match.group("asset").rstrip(".)]")
            if asset.lower().startswith("http://") or asset.lower().startswith("https://") or "." in asset or asset.lower().startswith("github.com/"):
                if asset not in assets:
                    assets[asset] = {
                        "asset": asset,
                        "source_line": line[:300],
                        "scope_hint": "out_of_scope_context" if out_scope_zone else ("in_scope_context" if in_scope_zone else "policy_context"),
                        "evidence_context": _context(lines, idx),
                    }
    return list(assets.values())


def _extract_out_of_scope(lines: list[str]) -> list[str]:
    rules: list[str] = []
    in_out_section = False
    for raw in lines:
        line = _clean_line(raw)
        if not line:
            continue
        low = line.lower()
        if "out of scope" in low:
            in_out_section = True
            rules.append(line)
            continue
        if in_out_section and ("in scope" in low or "bounty" in low) and "out of scope" not in low:
            in_out_section = False
        if in_out_section or any(h in low for h in OUT_OF_SCOPE_HINTS[1:]):
            if len(line) <= 260 and line not in rules:
                rules.append(line)
    return rules[:30]


def _extract_bounty_notes(lines: list[str]) -> list[str]:
    notes: list[str] = []
    for raw in lines:
        line = _clean_line(raw)
        low = line.lower()
        if any(term in low for term in ["bounty", "reward", "severity", "critical", "high", "medium", "low", "response", "sla", "gold standard"]):
            if line and line not in notes:
                notes.append(line[:260])
    return notes[:30]


def _find_matches(patterns: dict[str, re.Pattern[str]], text: str) -> list[str]:
    return [name for name, pattern in patterns.items() if pattern.search(text)]


def _extract_assets_from_items(items: list[Any], scope_hint: str) -> list[dict[str, str]]:
    assets: dict[str, dict[str, str]] = {}
    for item in items:
        line = _clean_line(str(item))
        for match in ASSET_RE.finditer(line):
            asset = match.group("asset").rstrip(".)]")
            assets[asset] = {
                "asset": asset,
                "source_line": line[:300],
                "scope_hint": scope_hint,
                "evidence_context": line[:600],
            }
    return list(assets.values())


def _normalize_structured_policy(
    payload: dict[str, Any],
    *,
    program: str,
    platform: str,
    source_url: str | None,
    observed_at: str | None,
) -> dict[str, Any]:
    in_scope_signals = list(payload.get("high_value_in_scope_signals") or [])
    out_rules = [str(x) for x in payload.get("out_of_scope_or_high_risk") or []]
    notable = [str(x) for x in payload.get("notable_policy_focus") or []]
    lane_split = payload.get("candidate_lane_split") or []
    lane_text = "\n".join(str(x.get("why", "")) + " " + str(x.get("id", "")) for x in lane_split if isinstance(x, dict))
    text_for_match = "\n".join(in_scope_signals + out_rules + notable + [lane_text])
    return {
        "schema_version": SCHEMA_VERSION,
        "program_slug": _slugify(program or payload.get("program_slug", "unknown")),
        "program": program or payload.get("program_slug", "unknown"),
        "platform": platform.lower() if platform else "unknown",
        "source_url": source_url or payload.get("url") or "unknown",
        "observed_at": observed_at or payload.get("observed_at") or date.today().isoformat(),
        "source_kind": "passive_policy_intake_json",
        "safety_boundary": "Candidate-only passive normalization. No live target testing, scope authorization, or report-ready claim is created by this file.",
        "in_scope_assets": _extract_assets_from_items(in_scope_signals, "in_scope_context"),
        "out_of_scope_rules": out_rules[:30],
        "bounty_risk_notes": (in_scope_signals + notable)[:30],
        "auth_gates": _find_matches(GATE_PATTERNS, text_for_match),
        "candidate_classes": _find_matches(CANDIDATE_CLASS_PATTERNS, text_for_match),
        "lane_split": lane_split,
        "stop_before": STOP_BEFORE_DEFAULT,
        "raw_text_stats": {"line_count": len(in_scope_signals) + len(out_rules) + len(notable), "char_count": len(text_for_match)},
    }


def normalize_policy_text(
    text: str,
    *,
    program: str,
    platform: str = "unknown",
    source_url: str | None = None,
    observed_at: str | None = None,
) -> dict[str, Any]:
    try:
        structured = json.loads(text)
    except json.JSONDecodeError:
        structured = None
    if isinstance(structured, dict) and (
        "high_value_in_scope_signals" in structured or "out_of_scope_or_high_risk" in structured or "candidate_lane_split" in structured
    ):
        return _normalize_structured_policy(structured, program=program, platform=platform, source_url=source_url, observed_at=observed_at)

    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [_clean_line(line) for line in normalized_text.split("\n") if _clean_line(line)]
    text_for_match = "\n".join(lines)
    program_slug = _slugify(program)
    candidate_classes = _find_matches(CANDIDATE_CLASS_PATTERNS, text_for_match)
    auth_gates = _find_matches(GATE_PATTERNS, text_for_match)

    return {
        "schema_version": SCHEMA_VERSION,
        "program_slug": program_slug,
        "program": program,
        "platform": platform.lower() if platform else "unknown",
        "source_url": source_url or "unknown",
        "observed_at": observed_at or date.today().isoformat(),
        "source_kind": "passive_visible_text",
        "safety_boundary": "Candidate-only passive normalization. No live target testing, scope authorization, or report-ready claim is created by this file.",
        "in_scope_assets": _extract_assets(lines),
        "out_of_scope_rules": _extract_out_of_scope(lines),
        "bounty_risk_notes": _extract_bounty_notes(lines),
        "auth_gates": auth_gates,
        "candidate_classes": candidate_classes,
        "stop_before": STOP_BEFORE_DEFAULT,
        "raw_text_stats": {"line_count": len(lines), "char_count": len(text_for_match)},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Normalize passive bounty-platform policy visible text into candidate-only JSON.")
    parser.add_argument("--input", required=True, help="Text file captured from cdp-visible-text or platform policy copy")
    parser.add_argument("--output", help="Output JSON path; stdout when omitted")
    parser.add_argument("--program", required=True, help="Program/company slug or display name")
    parser.add_argument("--platform", default="unknown", help="Platform hint, e.g. <bug-bounty-platform>/intigriti/bugcrowd")
    parser.add_argument("--source-url", default="unknown", help="Passive source URL for provenance")
    parser.add_argument("--observed-at", help="ISO date override")
    args = parser.parse_args(argv)

    text = Path(args.input).read_text(encoding="utf-8")
    payload = normalize_policy_text(text, program=args.program, platform=args.platform, source_url=args.source_url, observed_at=args.observed_at)
    output = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
