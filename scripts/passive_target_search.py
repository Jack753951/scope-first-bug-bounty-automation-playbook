#!/usr/bin/env python3
"""Build passive bug-bounty target-search queries and triage templates.

This helper does not send network requests, open browsers, scan targets, or touch
live systems. It only prints search URLs/queries and a compact scoring skeleton
so Hermes can drive Kali/noVNC browser work until a real gate appears.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from urllib.parse import quote_plus


SURFACE_TERMS = [
    "api",
    "developer",
    "docs",
    "graphql",
    "swagger",
    "openapi",
    "webhook",
    "integration",
    "saml",
    "scim",
    "sso",
    "workspace",
    "organization",
    "tenant",
    "invite",
    "roles",
    "billing",
    "export",
    "import",
]

GATE_TERMS = [
    "captcha",
    "otp",
    "2fa",
    "phone",
    "payment",
    "kyc",
    "claim your spot",
    "verification code",
]


@dataclass(frozen=True)
class SearchItem:
    kind: str
    label: str
    query: str
    url: str


def google_url(query: str) -> str:
    return "https://www.google.com/search?q=" + quote_plus(query)


def github_url(query: str, search_type: str = "code") -> str:
    return f"https://github.com/search?q={quote_plus(query)}&type={quote_plus(search_type)}"


def h1_url(query: str) -> str:
    return "https://<bug-bounty-platform>.com/directory/programs?query=" + quote_plus(query)


def intigriti_url(query: str) -> str:
    return "https://app.intigriti.com/programs?search=" + quote_plus(query)


def bugcrowd_url(query: str) -> str:
    return "https://bugcrowd.com/programs?search=" + quote_plus(query)


def hacktivity_url(query: str) -> str:
    return "https://<bug-bounty-platform>.com/hacktivity?querystring=" + quote_plus(query)


def build_queries(company: str, domain: str | None, platform: str | None) -> list[SearchItem]:
    c = company.strip()
    d = (domain or "").strip()
    items: list[SearchItem] = []

    for name, func in [
        ("hackerone_directory", h1_url),
        ("intigriti_programs", intigriti_url),
        ("bugcrowd_programs", bugcrowd_url),
    ]:
        items.append(SearchItem("platform", name, c, func(c)))

    items.extend(
        [
            SearchItem("disclosure", "bug_bounty_program", f'"{c}" "bug bounty"', google_url(f'"{c}" "bug bounty"')),
            SearchItem("disclosure", "responsible_disclosure", f'"{c}" "responsible disclosure"', google_url(f'"{c}" "responsible disclosure"')),
            SearchItem("reports", "hackerone_hacktivity", c, hacktivity_url(c)),
            SearchItem("reports", "writeups", f'"{c}" "bug bounty" "writeup"', google_url(f'"{c}" "bug bounty" "writeup"')),
            SearchItem("github", "company_code", f'"{c}" (api OR graphql OR webhook OR tenant OR workspace)', github_url(f'"{c}" api graphql webhook tenant workspace')),
        ]
    )

    if d:
        for term in SURFACE_TERMS:
            q = f'site:{d} "{term}"'
            items.append(SearchItem("surface", f"domain_{term}", q, google_url(q)))
        items.extend(
            [
                SearchItem("github", "domain_code", f'"{d}" (api OR graphql OR redirect_uri OR client_id)', github_url(f'"{d}" api graphql redirect_uri client_id')),
                SearchItem("surface", "javascript", f"site:{d} ext:js", google_url(f"site:{d} ext:js")),
                SearchItem("surface", "docs_subdomain", f"site:docs.{d} OR site:developer.{d} OR site:api.{d}", google_url(f"site:docs.{d} OR site:developer.{d} OR site:api.{d}")),
            ]
        )

    if platform:
        p = platform.lower()
        items.append(SearchItem("platform_hint", f"platform_{p}", f"{c} {platform}", google_url(f'"{c}" "{platform}"')))

    return items


def triage_template(company: str, domain: str | None, platform: str | None) -> dict:
    return {
        "program": company,
        "platform": platform or "unknown",
        "domain": domain or "unknown",
        "source": "passive_target_search.py",
        "gate_stop_if_seen": GATE_TERMS,
        "score": {
            "freshness_0_3": None,
            "self_signup_0_2": None,
            "free_plan_0_2": None,
            "low_priv_control_0_3": None,
            "owned_object_0_3": None,
            "scope_clarity_0_2": None,
            "operator_cost_low_0_3": None,
            "access_control_surface_0_3": None,
            "api_or_direct_url_surface_0_2": None,
            "total_0_23": None,
        },
        "interesting_surfaces": [],
        "likely_bundles": [],
        "operator_gates_seen": [],
        "decision": "UNSCORED",
        "decision_options": ["EXECUTE_LATER", "PASSIVE_ONLY", "PARK", "KILL"],
        "notes": "Passive/public enrichment only. Stop at OTP/CAPTCHA/login-secret/phone/payment/KYC/scarce-claim/live-test gates.",
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Generate passive target-search queries and a first-bounty triage template. No network access.")
    ap.add_argument("--company", required=True, help="Company/program/product name")
    ap.add_argument("--domain", help="Root domain, e.g. example.com")
    ap.add_argument("--platform", help="Bounty platform hint, e.g. <bug-bounty-platform>/Intigriti/Bugcrowd")
    ap.add_argument("--format", choices=["json", "markdown"], default="json")
    ns = ap.parse_args(argv)

    items = build_queries(ns.company, ns.domain, ns.platform)
    payload = {"schema_version": "1.0", "queries": [asdict(i) for i in items], "triage_template": triage_template(ns.company, ns.domain, ns.platform)}

    if ns.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"# Passive target search: {ns.company}\n")
        for i in items:
            print(f"- [{i.kind}] {i.label}: {i.query}\n  {i.url}")
        print("\n## Triage template\n")
        print("```json")
        print(json.dumps(payload["triage_template"], ensure_ascii=False, indent=2))
        print("```")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
