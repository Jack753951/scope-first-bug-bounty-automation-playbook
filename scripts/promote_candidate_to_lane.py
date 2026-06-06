#!/usr/bin/env python3
"""Promote a pending-intake candidate into offline lane/run-card drafts.

Default behavior is proposal-only: write `lane_state.draft.json` and a compact
run card under an output directory. This script does not edit config/scope.txt,
create programs/<slug>/scope.json, register queue entries, contact targets, or
authorize live testing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

BOUNDARY = (
    "Draft only. No live action authorized; operator must approve exact scope, "
    "program scope file creation/broadening, and any account/login/surface-mapping gate."
)


def _load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9_-]+", "_", value.lower()).strip("_") or "candidate"


def _today_compact(today: str) -> str:
    return today.replace("-", "")


def _unique(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def find_candidate(pending: dict[str, Any], slug: str) -> dict[str, Any]:
    for candidate in pending.get("candidates") or []:
        if candidate.get("slug") == slug or candidate.get("candidate_id") == slug:
            return candidate
    raise KeyError(f"candidate not found: {slug}")


def build_lane_state(candidate: dict[str, Any], *, today: str) -> dict[str, Any]:
    slug = _slugify(str(candidate.get("slug") or candidate.get("candidate_id") or candidate.get("program") or "candidate"))
    program = str(candidate.get("program") or slug)
    assets = [str(x) for x in candidate.get("candidate_assets") or []]
    blocked = _unique(
        [str(x) for x in candidate.get("blocked_before") or []]
        + [
            "adding_or_broadening_config_scope_without_operator_approval",
            "testing_live_assets",
            "scanner_fuzzer_dast_or_large_scale_discovery",
            "account_signup_login_OTP_CAPTCHA_password_phone_payment_KYC_without_operator_gate",
            "api_token_oauth_webhook_integration_creation_or_storage",
            "customer_or_non_owned_data_access",
            "report_submission_without_operator_final_approval",
        ]
    )
    return {
        "schema_version": "1.0",
        "program_slug": slug,
        "lane_id": f"{slug}_candidate_passive_intake",
        "lane_title": f"{program} passive candidate promotion draft",
        "autonomy_level": "A0",
        "operator_decision": "PASSIVE_ONLY",
        "machine_state": "POLICY_INTAKE",
        "state": "POLICY_INTAKE",
        "status": "blocked_awaiting_scope",
        "authorization": {
            "program_url": str(candidate.get("url") or "https://example.invalid"),
            "scope_file": "not_created_operator_gate",
            "global_scope_entries": [],
            "dry_run_gate": "not_run",
            "out_of_scope_control": "not_applicable",
        },
        "lane_boundary": {
            "allowed_actions": [
                "passive_program_policy_and_scope_review",
                "public_docs_reading",
                "candidate_packet_drafting",
                "scope_approval_packet_drafting",
            ],
            "blocked_actions": blocked,
            "identity_strategy": "No account/auth flow is approved by this draft. Stop before signup/login/OTP/CAPTCHA/password/phone/payment/KYC unless separately approved.",
        },
        "operator_gates": [
            "operator exact-scope approval before config/scope.txt or programs/<slug>/scope.json changes",
            "operator approval before live target first-contact",
            "operator approval before account signup/login/surface mapping",
            "separate approval for API-token/OAuth app/webhook/integration/payment/KYC/final submit",
        ],
        "stop_conditions": [
            "scope_or_policy_ambiguity",
            "auth_or_secret_gate_appears",
            "live_target_contact_would_be_needed",
            "candidate_requires_A3_controlled_technique",
        ],
        "next_autonomous_action": "Build or review the exact-scope approval packet; do not contact live assets.",
        "next_operator_action": "Approve/reject exact scope entries and lane boundary before promotion to live work.",
        "artifacts": {
            "dry_run_packet": "not_run",
            "evidence_dir": f"programs/{slug}/notes/",
            "candidate_source": "handoff/pending_intake.json",
        },
        "learning": {
            "preview_references": ["handoff/pending_intake.json"],
            "next_preview_seed": f"Candidate assets: {', '.join(assets[:6])}" if assets else "Candidate has no extracted assets yet.",
        },
        "updated_at": today,
    }


def render_run_card(candidate: dict[str, Any], lane_state: dict[str, Any], *, today: str) -> str:
    score = candidate.get("score", {}).get("total_0_23") if isinstance(candidate.get("score"), dict) else "n/a"
    assets = [str(x) for x in candidate.get("candidate_assets") or []]
    bundles = [str(x) for x in candidate.get("bundle_fit") or []]
    blocked = [str(x) for x in candidate.get("blocked_before") or []]
    lines = [
        f"# {lane_state['program_slug']} Candidate Promotion Draft — {today}",
        "",
        f"Boundary: {BOUNDARY}",
        "",
        "## Candidate",
        "",
        f"- Program: {candidate.get('program', lane_state['program_slug'])}",
        f"- Platform: {candidate.get('platform', 'unknown')}",
        f"- Source URL: {candidate.get('url', 'unknown')}",
        f"- Score: {score}/23",
        f"- Status: {candidate.get('status', 'candidate')}",
        "",
        "## Candidate assets",
        "",
    ]
    lines.extend([f"- `{asset}`" for asset in assets] or ["_None extracted._"])
    lines += ["", "## Bundle fit", ""]
    lines.extend([f"- {bundle}" for bundle in bundles] or ["- no practiced bundle identified"])
    lines += [
        "",
        "## Precondition gate",
        "",
        "Program: " + str(candidate.get("program", lane_state["program_slug"])),
        "Scope: not yet workspace-approved by this draft",
        "Bundle: " + (", ".join(bundles) if bundles else "none"),
        "Hypothesis: candidate only; no proof claim yet",
        "Report title if true: not selected until exact scope + owned controls exist",
        "",
        "Positive control: not available yet",
        "Negative control: not available yet",
        "Owned object/resource: not available yet",
        "Expected matrix: not built yet",
        "",
        "Allowed actions: passive policy/docs reading; approval packet drafting",
        "Blocked actions: live target contact, signup/login, scanners/fuzzers/DAST, API-token/OAuth/webhook/integration, customer data, report submit",
        "Operator cost: scope approval first; account/login costs unknown",
        "Kill criteria: no exact scope approval, no owned controls, no practiced bundle, high operator friction",
        "Evidence required: scope reference, role/control matrix, redacted screenshots/request snippets only after later approval",
        "Time box: 30 minutes for approval packet; 30-60 minutes for later surface mapping if approved",
        "Decision: PARK until operator exact-scope approval",
        "",
        "## Blocked before",
        "",
    ]
    lines.extend([f"- {item}" for item in blocked] or ["- exact scope approval and live boundary approval"])
    lines += ["", "No live action authorized by this draft.", ""]
    return "\n".join(lines)


def build_lane_draft(pending: dict[str, Any], *, slug: str, today: str | None = None) -> dict[str, Any]:
    today = today or date.today().isoformat()
    candidate = find_candidate(pending, slug)
    lane_state = build_lane_state(candidate, today=today)
    return {
        "boundary": BOUNDARY,
        "candidate": candidate,
        "lane_state": lane_state,
        "run_card_markdown": render_run_card(candidate, lane_state, today=today),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write offline lane/run-card drafts from a pending-intake candidate.")
    parser.add_argument("--pending", default="handoff/pending_intake.json", help="Pending intake JSON path")
    parser.add_argument("--slug", required=True, help="Candidate slug to promote into draft artifacts")
    parser.add_argument("--output-dir", default="programs", help="Directory under which <slug>/ draft artifacts are written")
    parser.add_argument("--date", help="ISO date override")
    args = parser.parse_args(argv)

    pending = _load_json(args.pending)
    today = args.date or date.today().isoformat()
    draft = build_lane_draft(pending, slug=args.slug, today=today)
    slug = draft["lane_state"]["program_slug"]
    out_dir = Path(args.output_dir) / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    lane_path = out_dir / "lane_state.draft.json"
    card_path = out_dir / f"run_card_{_today_compact(today)}.md"
    lane_path.write_text(json.dumps(draft["lane_state"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    card_path.write_text(draft["run_card_markdown"], encoding="utf-8")
    print(f"wrote {lane_path.as_posix()}")
    print(f"wrote {card_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
