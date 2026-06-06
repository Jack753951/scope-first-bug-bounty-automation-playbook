#!/usr/bin/env python3
"""Build an offline operator approval packet for candidate bug-bounty scope.

This helper reads normalized passive policy JSON plus the operator-owned global
scope allowlist and emits a packet that separates already-whitelisted assets
from entries that require operator approval. It never edits config/scope.txt,
creates programs/<slug>/scope.json, opens sockets, authenticates, scans, or
promotes a lane beyond passive/operator-gate review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.scope import (  # noqa: E402
    ScopeEntry,
    load_global_scope,
    normalize_target,
    parse_global_scope_line,
    target_matches_any,
)

SCHEMA_VERSION = "scope_approval_packet/0.1"
BOUNDARY = (
    "Offline approval packet only. This file does not authorize live target "
    "testing, edit config/scope.txt, create/broaden programs/<slug>/scope.json, "
    "or approve account/API-token/OAuth/webhook/payment/KYC actions."
)

ASSET_RE = re.compile(
    r"(?P<asset>(?:https?://)?(?:\*\.)?(?:[A-Za-z0-9_-]+\.)+[A-Za-z]{2,}"
    r"(?:/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]*)?|"
    r"github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)",
    re.I,
)

SOURCE_ONLY_RE = re.compile(r"github\.com/|\b(executable|source code|desktop client|cli|plugin|gateway|mesh)\b", re.I)
HIGH_RISK_RE = re.compile(
    r"customer data plane|out of scope|denial of service|automated scanning|bruteforce|"
    r"social engineering|phishing|spam|ssrf|oast|callback|takeover|kuma\.io",
    re.I,
)


def _load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _asset_value(row: Any) -> str:
    if isinstance(row, dict):
        return str(row.get("asset") or row.get("value") or "").strip()
    if isinstance(row, str):
        return row.strip()
    return ""


def _unique_dicts(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        value = str(row.get(key) or "")
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(row)
    return out


def _extract_rule_assets(rules: list[str]) -> list[str]:
    assets: list[str] = []
    for rule in rules:
        for match in ASSET_RE.finditer(str(rule)):
            assets.append(match.group("asset").rstrip(".)],;"))
    seen: set[str] = set()
    out: list[str] = []
    for asset in assets:
        if asset not in seen:
            seen.add(asset)
            out.append(asset)
    return out


def _normalize_asset_for_scope(asset: str) -> dict[str, Any]:
    raw = asset.strip().rstrip(".)],;")
    if not raw:
        return {"asset": asset, "kind": "invalid", "errors": ["empty asset"]}
    lowered = raw.lower()
    if lowered.startswith("github.com/"):
        return {"asset": raw, "kind": "source_repository", "scope_entry": raw, "host": "github.com"}
    if lowered.startswith("http://") or lowered.startswith("https://"):
        parsed = urlsplit(lowered)
        if parsed.hostname is None:
            return {"asset": raw, "kind": "invalid", "errors": ["URL asset has no host"]}
        host = parsed.hostname.lower()
        if host.startswith("*."):
            return {"asset": raw, "kind": "wildcard", "scope_entry": host, "host": host}
        return {"asset": raw, "kind": "domain", "scope_entry": host, "host": host, "source_url_path": parsed.path or "/"}
    if lowered.startswith("*."):
        return {"asset": raw, "kind": "wildcard", "scope_entry": lowered, "host": lowered}
    parsed_target = normalize_target(lowered)
    if parsed_target.target is None:
        return {"asset": raw, "kind": "invalid", "errors": list(parsed_target.errors)}
    target = parsed_target.target
    return {"asset": raw, "kind": target.target_type, "scope_entry": target.normalized, "host": target.host}


def _global_match(scope_entry: str, global_entries: list[ScopeEntry]) -> tuple[bool, str | None]:
    candidate_entry = parse_global_scope_line(scope_entry, "candidate")
    if candidate_entry is not None and any(
        entry.entry_type == candidate_entry.entry_type and entry.value == candidate_entry.value
        for entry in global_entries
    ):
        return True, scope_entry

    # For host-like candidates, also accept coverage by an existing global wildcard.
    target_result = normalize_target(scope_entry[2:] if scope_entry.startswith("*.") else scope_entry)
    if target_result.target is None:
        return False, None
    for entry in global_entries:
        if target_matches_any(target_result.target, [entry]):
            return True, entry.value
    return False, None


def build_scope_approval_packet(policy: dict[str, Any], *, global_scope_path: str | Path) -> dict[str, Any]:
    global_scope = load_global_scope(global_scope_path)
    global_entries = global_scope.entries
    out_rules = [str(x) for x in policy.get("out_of_scope_rules") or policy.get("out_of_scope_or_high_risk") or []]
    out_rule_assets = set(_extract_rule_assets(out_rules))

    already: list[dict[str, Any]] = []
    needs: list[dict[str, Any]] = []
    wildcard_narrowing: list[dict[str, Any]] = []
    source_only: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []

    rows = policy.get("in_scope_assets") or []
    for row in rows:
        asset = _asset_value(row)
        if not asset:
            continue
        norm = _normalize_asset_for_scope(asset)
        norm["scope_hint"] = row.get("scope_hint") if isinstance(row, dict) else "policy_context"
        norm["source_line"] = row.get("source_line") if isinstance(row, dict) else ""
        source_blob = " ".join([asset, str(norm.get("source_line") or ""), str(norm.get("scope_hint") or "")])

        if norm["kind"] == "invalid":
            invalid.append(norm)
            continue
        if asset in out_rule_assets or norm.get("scope_entry") in out_rule_assets or HIGH_RISK_RE.search(source_blob):
            norm["reason"] = "asset appears in out-of-scope/high-risk policy context"
            blocked.append(norm)
            continue
        if norm["kind"] == "source_repository" or SOURCE_ONLY_RE.search(source_blob):
            norm["reason"] = "source/local review candidate; not a live web scope entry by itself"
            source_only.append(norm)
            continue

        scope_entry = str(norm.get("scope_entry") or "")
        is_global, matched_by = _global_match(scope_entry, global_entries)
        if is_global:
            norm["matched_global_scope"] = matched_by
            already.append(norm)
        elif scope_entry.startswith("*."):
            norm["reason"] = "wildcard policy asset requires exact-host narrowing before config/scope.txt approval"
            wildcard_narrowing.append(norm)
        else:
            norm["reason"] = "candidate appears in passive policy intake but is not in config/scope.txt"
            needs.append(norm)

    program_slug = policy.get("program_slug") or str(policy.get("program") or "unknown").lower().replace(" ", "_")
    suggested_entries = [str(row["scope_entry"]) for row in needs]
    packet = {
        "schema_version": SCHEMA_VERSION,
        "program_slug": program_slug,
        "program": policy.get("program", program_slug),
        "platform": policy.get("platform", "unknown"),
        "source_url": policy.get("source_url", "unknown"),
        "observed_at": policy.get("observed_at") or date.today().isoformat(),
        "boundary": BOUNDARY,
        "global_scope_path": str(global_scope_path),
        "global_scope_errors": global_scope.errors,
        "global_scope_warnings": global_scope.warnings,
        "already_in_global_scope": _unique_dicts(already, "scope_entry"),
        "needs_operator_scope_approval": _unique_dicts(needs, "scope_entry"),
        "wildcard_requires_exact_host_narrowing": _unique_dicts(wildcard_narrowing, "scope_entry"),
        "source_or_local_only": _unique_dicts(source_only, "scope_entry"),
        "blocked_or_out_of_scope": _unique_dicts(blocked, "scope_entry"),
        "invalid_or_unsupported": _unique_dicts(invalid, "asset"),
        "suggested_config_scope_entries": suggested_entries,
        "operator_gates": [
            "operator approval before editing config/scope.txt",
            "operator approval before creating or broadening programs/<slug>/scope.json",
            "operator approval before any live target first-contact beyond passive policy/public-doc reading",
            "separate approval for account signup/login/OTP/CAPTCHA/password/phone/payment/KYC",
            "separate approval for API-token/OAuth app/webhook/integration creation or handling",
        ],
        "recommended_next_step": _recommended_next_step(needs, wildcard_narrowing, source_only),
    }
    return packet


def _recommended_next_step(needs: list[dict[str, Any]], wildcards: list[dict[str, Any]], source_only: list[dict[str, Any]]) -> str:
    if needs:
        return "Ask operator to approve or reject the exact suggested config/scope.txt entries; do not touch live assets before approval."
    if wildcards:
        return "Narrow wildcard policy assets to exact owned hosts before asking for config/scope.txt approval."
    if source_only:
        return "Proceed only with local/source review candidates; no live target scope approval is implied."
    return "No approvable live scope entries found; keep candidate passive or park."


def render_markdown(packet: dict[str, Any]) -> str:
    lines = [
        f"# Scope Approval Packet — {packet['program_slug']}",
        "",
        f"Generated by `scripts/build_scope_approval_packet.py` for `{packet['program_slug']}`.",
        "",
        f"Boundary: {packet['boundary']}",
        "",
        "## Source",
        "",
        f"- Program: {packet.get('program')}",
        f"- Platform: {packet.get('platform')}",
        f"- Source URL: {packet.get('source_url')}",
        f"- Observed at: {packet.get('observed_at')}",
        f"- Global scope file: `{packet.get('global_scope_path')}`",
        "",
    ]
    if packet.get("global_scope_errors") or packet.get("global_scope_warnings"):
        lines += ["## Global scope parser notes", ""]
        for err in packet.get("global_scope_errors", []):
            lines.append(f"- ERROR: {err}")
        for warn in packet.get("global_scope_warnings", []):
            lines.append(f"- WARN: {warn}")
        lines.append("")

    def section(title: str, key: str, detail: str) -> None:
        rows = packet.get(key) or []
        lines.extend([f"## {title} ({len(rows)})", "", detail, ""])
        if not rows:
            lines.extend(["_None._", ""])
            return
        for row in rows:
            entry = row.get("scope_entry") or row.get("asset")
            reason = row.get("reason") or row.get("matched_global_scope") or row.get("scope_hint") or ""
            lines.append(f"- `{entry}` — {reason}")
        lines.append("")

    section(
        "Already in config/scope.txt",
        "already_in_global_scope",
        "These are already covered by the global allowlist, but still require program scope/lane boundary before live action.",
    )
    section(
        "Needs operator scope approval",
        "needs_operator_scope_approval",
        "Exact entries that appear candidate-eligible from passive policy text but are not in config/scope.txt.",
    )
    section(
        "Wildcard requires exact-host narrowing",
        "wildcard_requires_exact_host_narrowing",
        "Do not approve broad wildcards blindly; choose exact hosts or a tighter operator-approved boundary first.",
    )
    section(
        "Source/local only",
        "source_or_local_only",
        "Use for local/source review. These are not live web target approvals by themselves.",
    )
    section(
        "Blocked or out of scope",
        "blocked_or_out_of_scope",
        "Policy/high-risk context says do not pursue these without a new explicit operator decision and program-rule check.",
    )
    section("Invalid or unsupported", "invalid_or_unsupported", "Parser could not turn these into safe scope entries.")

    lines += ["## Suggested config/scope.txt additions", ""]
    entries = packet.get("suggested_config_scope_entries") or []
    if entries:
        lines.append("Copy-paste only after explicit operator approval:")
        lines.append("")
        lines.append("```text")
        for entry in entries:
            lines.append(entry)
        lines.append("```")
    else:
        lines.append("_None._")
    lines += ["", "## Operator gates", ""]
    for gate in packet.get("operator_gates", []):
        lines.append(f"- {gate}")
    lines += ["", "## Recommended next step", "", packet.get("recommended_next_step", ""), ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build offline operator scope approval packet from normalized policy JSON.")
    parser.add_argument("--policy", required=True, help="Normalized policy JSON path")
    parser.add_argument("--global-scope", default="config/scope.txt", help="Global scope allowlist path")
    parser.add_argument("--output", required=True, help="Markdown output packet path")
    parser.add_argument("--json-output", help="Optional JSON output packet path")
    args = parser.parse_args(argv)

    policy = _load_json(args.policy)
    packet = build_scope_approval_packet(policy, global_scope_path=args.global_scope)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_markdown(packet), encoding="utf-8")
    if args.json_output:
        json_path = Path(args.json_output)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path.as_posix()}")
    if args.json_output:
        print(f"wrote {Path(args.json_output).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
