#!/usr/bin/env python3
"""Build scored pending-intake candidates from passive policy/doc/report inputs.

Inputs are offline JSON artifacts. This helper never fetches URLs, scans targets,
authenticates, changes scope files, or promotes a candidate beyond passive intake.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

GENERATED_MARKER = "build_target_candidates.py"
DEFAULT_BOUNDARY = (
    "Pre-lane intake. Candidates listed here have no active live lane yet. "
    "No target testing is authorized by this file; operator must approve exact "
    "scope facts and any config/scope.txt or programs/<slug>/scope.json changes."
)

BUNDLE_BY_CLASS = {
    "org_role_invite_authz": "auth-role-separation",
    "oauth_oidc": "oauth-oidc-boundary",
    "api_token_or_webhook_boundary": "api-token-or-webhook-boundary",
    "api_direct_object_authz": "idor-bola-api-object-boundary",
    "source_or_plugin_review": "source-plugin-local-review",
}

KEYWORDS = {
    "self_signup": re.compile(r"sign up|signup|register|free trial|create account", re.I),
    "free_plan": re.compile(r"free|trial|sandbox|developer", re.I),
    "owned_object": re.compile(r"organization|workspace|team|member|invite|role|webhook|api token|audit|billing", re.I),
    "access_control": re.compile(r"idor|bola|authorization|access-control|role|invite|oauth|saml|scim|tenant", re.I),
    "api_surface": re.compile(r"api|graphql|openapi|swagger|webhook|token|direct url", re.I),
    "freshness": re.compile(r"updated|launched|new|recent|2026|2025|changelog|release", re.I),
}


def _load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_json_list(paths: list[str] | None) -> list[Any]:
    items: list[Any] = []
    for path in paths or []:
        payload = _load_json(path)
        if isinstance(payload, list):
            items.extend(payload)
        else:
            items.append(payload)
    return items


def _textify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out


def _score(policy: dict[str, Any], evidence_text: str) -> dict[str, int]:
    in_scope_assets = policy.get("in_scope_assets") or []
    candidate_classes = policy.get("candidate_classes") or []
    auth_gates = policy.get("auth_gates") or []
    text = evidence_text + "\n" + _textify(policy)
    scores = {
        "freshness_0_3": 2 if KEYWORDS["freshness"].search(text) else 1,
        "self_signup_0_2": 2 if KEYWORDS["self_signup"].search(text) else (1 if not auth_gates else 0),
        "free_plan_0_2": 2 if KEYWORDS["free_plan"].search(text) else 1,
        "low_priv_control_0_3": 2 if candidate_classes else 1,
        "owned_object_0_3": 3 if KEYWORDS["owned_object"].search(text) else (2 if candidate_classes else 1),
        "scope_clarity_0_2": 2 if in_scope_assets else 1,
        "operator_cost_low_0_3": max(0, 3 - min(len(auth_gates), 3)),
        "access_control_surface_0_3": 3 if KEYWORDS["access_control"].search(text) else (2 if candidate_classes else 1),
        "api_or_direct_url_surface_0_2": 2 if KEYWORDS["api_surface"].search(text) or in_scope_assets else 1,
    }
    scores["total_0_23"] = sum(scores.values())
    return scores


def _candidate_assets(policy: dict[str, Any]) -> list[str]:
    assets = []
    for row in policy.get("in_scope_assets") or []:
        if isinstance(row, dict):
            assets.append(row.get("asset", ""))
        elif isinstance(row, str):
            assets.append(row)
    return _unique(assets)[:20]


def _signals(policy: dict[str, Any], public_docs: list[Any], disclosed_reports: list[Any]) -> list[str]:
    signals: list[str] = []
    if policy.get("in_scope_assets"):
        signals.append(f"Passive policy normalization found {len(policy.get('in_scope_assets') or [])} candidate scope asset entries.")
    if policy.get("candidate_classes"):
        signals.append("Candidate-only classes: " + ", ".join(policy.get("candidate_classes") or []))
    if policy.get("auth_gates"):
        signals.append("Observed human/operator gates: " + ", ".join(policy.get("auth_gates") or []))
    if public_docs:
        signals.append(f"Public-doc enrichment inputs: {len(public_docs)} item(s).")
    if disclosed_reports:
        signals.append(f"Disclosed-report enrichment inputs: {len(disclosed_reports)} item(s).")
    if policy.get("bounty_risk_notes"):
        signals.extend(str(n)[:220] for n in policy.get("bounty_risk_notes", [])[:4])
    return _unique(signals)[:12]


def _bundle_fit(policy: dict[str, Any], evidence_text: str) -> list[str]:
    bundles = [BUNDLE_BY_CLASS[c] for c in policy.get("candidate_classes", []) if c in BUNDLE_BY_CLASS]
    if re.search(r"invite|role|organization|workspace|team", evidence_text, re.I):
        bundles.append("auth-role-separation")
    if re.search(r"webhook|api token|secret", evidence_text, re.I):
        bundles.append("api-token-or-webhook-boundary")
    if re.search(r"idor|bola|object|tenant", evidence_text, re.I):
        bundles.append("idor-bola-api-object-boundary")
    return _unique(bundles)[:10]


def build_candidate(policy: dict[str, Any], public_docs: list[Any], disclosed_reports: list[Any]) -> dict[str, Any]:
    evidence_text = "\n".join([_textify(x) for x in public_docs + disclosed_reports])
    slug = policy.get("program_slug") or str(policy.get("program") or "unknown").lower().replace(" ", "_")
    bundles = _bundle_fit(policy, evidence_text + "\n" + _textify(policy))
    return {
        "slug": slug,
        "platform": policy.get("platform", "unknown"),
        "program": policy.get("program", slug),
        "source": "passive platform policy normalization + optional public docs/disclosed reports",
        "source_tool": GENERATED_MARKER,
        "url": policy.get("source_url", "unknown"),
        "observed_at": policy.get("observed_at") or date.today().isoformat(),
        "status": "candidate_passive_intake",
        "score": _score(policy, evidence_text),
        "signals": _signals(policy, public_docs, disclosed_reports),
        "candidate_assets": _candidate_assets(policy),
        "candidate_classes": policy.get("candidate_classes", []),
        "bundle_fit": bundles,
        "blocked_before": _unique(list(policy.get("stop_before") or []) + [
            "any live target testing beyond passive policy/public-doc reading",
            "operator approval for exact live scope entries",
        ]),
        "recommended_decision": "passive_triage_then_operator_gate",
        "recommended_next_step": "Review candidate assets/classes, then ask operator before any live scope addition or target contact.",
    }


def build_pending_intake_payload(
    *,
    policies: list[dict[str, Any]],
    public_docs: list[Any] | None = None,
    disclosed_reports: list[Any] | None = None,
    existing: dict[str, Any] | None = None,
    replace_generated: bool = False,
) -> dict[str, Any]:
    public_docs = public_docs or []
    disclosed_reports = disclosed_reports or []
    new_candidates = [build_candidate(policy, public_docs, disclosed_reports) for policy in policies]
    new_slugs = {candidate.get("slug") for candidate in new_candidates}
    candidates = []
    if existing:
        for candidate in existing.get("candidates") or []:
            if replace_generated and candidate.get("source_tool") == GENERATED_MARKER:
                continue
            if candidate.get("slug") in new_slugs:
                continue
            candidates.append(candidate)
    candidates.extend(new_candidates)
    return {
        "schema_version": "1.0",
        "updated_at": date.today().isoformat(),
        "boundary": existing.get("boundary", DEFAULT_BOUNDARY) if existing else DEFAULT_BOUNDARY,
        "candidates": candidates,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build scored passive pending-intake candidates from offline policy/doc/report JSON.")
    parser.add_argument("--policy", action="append", required=True, help="Normalized policy JSON path; repeatable")
    parser.add_argument("--public-docs", action="append", help="JSON file or list containing public-doc snippets")
    parser.add_argument("--disclosed-reports", action="append", help="JSON file or list containing disclosed-report snippets")
    parser.add_argument("--existing", help="Existing pending_intake.json to merge")
    parser.add_argument("--output", required=True, help="Output pending intake JSON path")
    parser.add_argument("--replace-generated", action="store_true", help="Drop previous build_target_candidates.py entries before adding new ones")
    args = parser.parse_args(argv)

    policies = _load_json_list(args.policy)
    public_docs = _load_json_list(args.public_docs)
    disclosed_reports = _load_json_list(args.disclosed_reports)
    existing = _load_json(args.existing) if args.existing else None
    payload = build_pending_intake_payload(
        policies=policies,
        public_docs=public_docs,
        disclosed_reports=disclosed_reports,
        existing=existing,
        replace_generated=args.replace_generated,
    )
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path} candidates={len(payload['candidates'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
