#!/usr/bin/env python3
"""Bridge vuln intel freshness into proof-pattern workflow artifacts.

This is a controller for the user's desired loop:
latest vulnerability -> local lab run-card -> proof pattern draft -> live-target prerequisites.
It is deliberately non-executing. It creates the handoff artifacts that gate local
靶機 testing and later live target selection, but it does not run PoCs, scanners,
containers, browsers/noVNC, account actions, or live requests.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_TARGET_ARGS = {"--target", "--url", "--host", "--scope", "--live", "--execute", "--scan", "--exploit"}
LOCAL_FIRST = {"new_local_bootstrap_candidate", "needs_bundle_update", "covered_by_existing_bundle"}


def _emit_error(error: str, detail: str = "") -> int:
    print(json.dumps({"status": "error", "error": error, "detail": detail, "target_touching": False}, indent=2))
    return 30


def _reject_target_like_args(argv: list[str]) -> int | None:
    for arg in argv:
        key = arg.split("=", 1)[0]
        if key in FORBIDDEN_TARGET_ARGS:
            return _emit_error("target_or_execution_argument_rejected", key)
    return None


def _slug(value: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return text[:80] or "unknown_candidate"


def _choose_candidate(delta: dict[str, Any]) -> dict[str, Any]:
    recs = delta.get("top_recommendations") or []
    for wanted in ("new_local_bootstrap_candidate", "needs_bundle_update", "needs_authorized_live_target"):
        for item in recs:
            if item.get("classification") == wanted:
                return item
    items = delta.get("items") or []
    for wanted in ("new_local_bootstrap_candidate", "needs_bundle_update", "needs_authorized_live_target", "covered_by_existing_bundle"):
        for item in items:
            if item.get("classification") == wanted:
                return item
    raise ValueError("no actionable candidate in delta")


def _safe_local_goal(candidate: dict[str, Any]) -> str:
    classes = set(candidate.get("vuln_classes") or [])
    hint = str(candidate.get("safe_proof_hint") or "")
    if "ssrf" in classes:
        return "Build a disposable local-lab callback marker proof only; no metadata/internal scanning and no live callback."
    if "file-read/path-traversal" in classes or "xxe" in classes:
        return "Build a local-lab owned marker-file proof only; do not read system files, secrets, keys, tokens, or third-party data."
    if "deserialization" in classes or "rce/command-execution" in classes:
        return "Build a marker-only local-lab proof with pre/post health and explicit operator gate before any execution."
    if "auth/access-control" in classes:
        return "Build a throwaway local-lab Account A/B role/object matrix using synthetic data only."
    if "xss" in classes:
        return "Build a browser-runtime safe marker proof only; no cookies, tokens, keylogging, or victim interaction."
    return hint or "Review manually and create only a disposable local-lab proof surrogate."


def _live_prereqs(candidate: dict[str, Any]) -> list[str]:
    classes = set(candidate.get("vuln_classes") or [])
    common = [
        "explicit bug-bounty/client/user-owned scope and rules",
        "operator-owned accounts/objects only",
        "redaction check before evidence enters reports",
        "stop before non-owned data, secrets, destructive impact, scanner/fuzzer/DAST, or report submission",
    ]
    if "auth/access-control" in classes:
        return ["two owned accounts or two tenants/workspaces", "positive Account A control and negative Account B control"] + common
    if "ssrf" in classes:
        return ["program explicitly allows callback/OAST or use no-callback surrogate", "no metadata/internal host probing"] + common
    if "xss" in classes:
        return ["safe marker only in owned object/UI", "no cookie/token/credential capture and no victim interaction"] + common
    if "file-read/path-traversal" in classes or "xxe" in classes:
        return ["only read an operator-owned synthetic marker if live proof is explicitly allowed", "never request secrets/system files"] + common
    if "deserialization" in classes or "rce/command-execution" in classes:
        return ["usually local-lab only unless written authorization explicitly permits marker execution", "pre/post health and human checkpoint required"] + common
    return common


def _render_run_card(candidate: dict[str, Any], stamp: str) -> str:
    cid = candidate.get("id", "unknown")
    return f"""# Local Lab Bootstrap Run Card — {cid} — {stamp}

Status: plan-only / operator-gated local lab test / no target touched

Do not run against live targets. Do not run against public IPs/domains. This run-card is for a disposable, intentionally vulnerable, recoverable local 靶機 or fixture only.

## Candidate

- ID: {cid}
- Title: {candidate.get('title','')}
- Classification: {candidate.get('classification','')}
- Classes: {', '.join(candidate.get('vuln_classes') or [])}
- Safe proof goal: {_safe_local_goal(candidate)}

## Required gates before local execution

1. Disposable local target identified and snapshotted or rebuildable.
2. No host/user Docker socket mounted into the victim unless explicitly approved for that lab.
3. Test data is synthetic and lab-owned.
4. Pre-health command and post-health command are defined.
5. Cleanup/recovery command is defined.
6. Any callback, scanner, fuzzer, exploit PoC, or destructive variant needs a separate explicit local-lab approval.

## Proof artifact requirements

- Save only sanitized evidence under `labs/proofs/` or `handoff/`.
- Record expected vs observed behavior.
- Record limits and what was not tested.
- Do not store credentials, cookies, tokens, OTPs, phone numbers, private scope, loot, or real third-party data.

## After successful local proof

Promote only a summarized, sanitized proof pattern into `modules/bundles/` and update the live-bounty bridge. A draft bundle is created separately but must remain unverified until this run-card has evidence.
"""


def _render_draft_bundle(candidate: dict[str, Any], stamp: str) -> str:
    cid = candidate.get("id", "unknown")
    return f"""# Draft proof pattern candidate — {cid}

Status: draft / not verified / do not add to proof library yet
vuln_classes: {', '.join(candidate.get('vuln_classes') or ['unknown/review'])}
source_candidate: {cid}
created: {stamp}
safe_proof_posture: {_safe_local_goal(candidate)}
live_target_policy: prerequisite_mapping_only_until_local_proof_verified

## Why this exists

This draft preserves the proof-pattern idea selected from the latest vulnerability-intel freshness delta. It is not a verified proof-library bundle.

## Minimum promotion requirements

- Disposable local lab or fixture run completed.
- Pre/post health and cleanup recorded.
- Evidence is sanitized and contains no secrets/loot/private data.
- A reviewer can reproduce the bounded proof from local artifacts only.
- Live-target prerequisites and stop-before rules are documented.

## Candidate summary

- Title: {candidate.get('title','')}
- Classification: {candidate.get('classification','')}
- Safe hint: {candidate.get('safe_proof_hint','')}
"""


def _render_live_mapping(candidate: dict[str, Any], stamp: str) -> str:
    prereqs = "\n".join(f"- {item}" for item in _live_prereqs(candidate))
    return f"""# Live Target Prerequisite Map — {candidate.get('id','unknown')} — {stamp}

Status: prerequisite mapping only / no live target touched

This maps a local proof pattern candidate to future live-target prerequisites. It does not authorize testing.

## Required before any live lane

{prereqs}

## Current decision

Keep as `blocked_preserve` for live work until a verified local proof pattern exists and the operator confirms an in-scope program/lane with required owned controls.
"""


def _render_summary(payload: dict[str, Any]) -> str:
    c = payload["selected_candidate"]
    return f"""# Vuln-to-Proof Loop — {payload['stamp']}

Status: latest漏洞 -> local靶機 run-card -> proof pattern draft -> live-target prerequisites

No local lab, scanner, PoC, browser/noVNC, account, or live target was executed.

## Selected candidate

- ID: {c.get('id')}
- Title: {c.get('title','')}
- Classification: {c.get('classification')}
- Classes: {', '.join(c.get('vuln_classes') or [])}

## Stage decisions

- latest vulnerability intake: {payload['stages']['latest_vulnerability_intake']['status']}
- local target test: {payload['stages']['local_target_test']['status']}
- proof pattern library: {payload['stages']['proof_pattern_library']['status']}
- live target selection: {payload['stages']['live_target_selection']['status']}

## Artifacts

- local run-card: `{payload['artifacts']['local_run_card']}`
- proof pattern draft: `{payload['artifacts']['proof_pattern_draft']}`
- live prerequisite map: `{payload['artifacts']['live_target_prereq_map']}`

## Next real action

Operator chooses whether to run the local run-card in a disposable lab. Until then, this is an automated planning/bridging loop, not exploitation/testing execution.
"""


def build_loop(delta_json: Path, out_dir: Path, stamp: str) -> dict[str, Any]:
    delta = json.loads(delta_json.read_text(encoding="utf-8"))
    candidate = _choose_candidate(delta)
    candidate_slug = _slug(str(candidate.get("id") or candidate.get("title") or "candidate"))
    out_dir.mkdir(parents=True, exist_ok=True)
    run_card = out_dir / f"local_run_card_{candidate_slug}_{stamp}.md"
    draft = out_dir / f"proof_pattern_draft_{candidate_slug}_{stamp}.md"
    live_map = out_dir / f"live_target_prereq_map_{candidate_slug}_{stamp}.md"
    run_card.write_text(_render_run_card(candidate, stamp), encoding="utf-8")
    draft.write_text(_render_draft_bundle(candidate, stamp), encoding="utf-8")
    live_map.write_text(_render_live_mapping(candidate, stamp), encoding="utf-8")
    payload = {
        "status": "ok",
        "stamp": stamp,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "target_touching": False,
        "source_delta": delta_json.as_posix(),
        "selected_candidate": candidate,
        "stages": {
            "latest_vulnerability_intake": {"status": "consumed_existing_delta", "source": delta.get("source_vuln_intel", "")},
            "local_target_test": {"status": "run_card_only_operator_gate", "artifact": run_card.as_posix()},
            "proof_pattern_library": {"status": "draft_only_until_local_proof_verified", "artifact": draft.as_posix()},
            "live_target_selection": {"status": "prerequisite_mapping_only_no_live_touch", "artifact": live_map.as_posix()},
        },
        "artifacts": {
            "local_run_card": run_card.as_posix(),
            "proof_pattern_draft": draft.as_posix(),
            "live_target_prereq_map": live_map.as_posix(),
        },
        "safety_note": "planning artifacts only; no local or live execution",
    }
    json_path = out_dir / f"proof_loop_{stamp}.json"
    md_path = out_dir / f"proof_loop_{stamp}.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(_render_summary(payload), encoding="utf-8")
    payload["artifacts"]["summary_json"] = json_path.as_posix()
    payload["artifacts"]["summary_md"] = md_path.as_posix()
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    rejected = _reject_target_like_args(argv)
    if rejected is not None:
        return rejected
    parser = argparse.ArgumentParser(description="Generate non-executing vuln-to-proof loop artifacts")
    parser.add_argument("--delta-json", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "handoff" / "vuln_intel" / "proof_loop")
    parser.add_argument("--stamp", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    args = parser.parse_args(argv)
    payload = build_loop(args.delta_json, args.out_dir, args.stamp)
    print(json.dumps({"status": "ok", "target_touching": False, "artifacts": payload["artifacts"]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
