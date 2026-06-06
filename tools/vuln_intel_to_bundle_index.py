#!/usr/bin/env python3
"""Compare vulnerability-intel candidates with local proof-bundle coverage.

Metadata-only by design: this tool reads local JSON/Markdown bundle metadata and
never touches targets, scanners, browsers, noVNC, recon, accounts, or networks.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VULN_INTEL_DIR = ROOT / "handoff" / "vuln_intel"
DEFAULT_BUNDLE_DIR = ROOT / "modules" / "bundles"
FORBIDDEN_TARGET_ARGS = {"--target", "--url", "--host", "--scope", "--live"}
ACTIONABLE = {"new_local_bootstrap_candidate", "needs_bundle_update", "needs_authorized_live_target"}

try:
    from bundle_index import build_index
except ImportError:  # pragma: no cover - fallback for unusual invocation paths
    sys.path.insert(0, str(ROOT / "tools"))
    from bundle_index import build_index


def _emit_error(error: str, detail: str = "") -> int:
    print(json.dumps({
        "status": "error",
        "error": error,
        "detail": detail,
        "target_touching": False,
    }, indent=2))
    return 30


def _reject_target_like_args(argv: list[str]) -> int | None:
    for arg in argv:
        key = arg.split("=", 1)[0]
        if key in FORBIDDEN_TARGET_ARGS:
            return _emit_error("target_like_argument_rejected", key)
    return None


def _latest_vuln_intel_file(vuln_intel_dir: Path) -> Path:
    files = sorted(vuln_intel_dir.glob("vuln_intel_candidates_*.json"))
    if not files:
        raise FileNotFoundError(f"no vuln_intel_candidates_*.json found under {vuln_intel_dir}")
    return files[-1]


def _norm(value: str) -> str:
    return value.strip().lower()


def _candidate_classes(candidate: dict[str, Any]) -> list[str]:
    raw = candidate.get("vuln_classes") or []
    if isinstance(raw, str):
        raw = [raw]
    return [_norm(str(item)) for item in raw if str(item).strip()]


def _candidate_id(candidate: dict[str, Any]) -> str:
    return str(candidate.get("id") or candidate.get("cve") or candidate.get("ghsa_id") or candidate.get("title") or "unknown")


def _match_bundles(candidate: dict[str, Any], bundles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cid = _candidate_id(candidate).upper()
    classes = set(_candidate_classes(candidate))
    product = _norm(str(candidate.get("product") or ""))
    title_summary = _norm(" ".join(str(candidate.get(key, "")) for key in ("title", "summary", "product", "vendor_project")))
    matches: list[dict[str, Any]] = []
    for bundle in bundles:
        bundle_classes = {_norm(str(item)) for item in bundle.get("vuln_classes", [])}
        ref_match = cid and (cid in {str(x).upper() for x in bundle.get("cve_refs", [])} or cid in {str(x).upper() for x in bundle.get("ghsa_refs", [])})
        class_match = bool(classes & bundle_classes)
        product_terms = [_norm(str(x)) for x in bundle.get("product_refs", []) + bundle.get("coverage_terms", [])]
        product_match = bool(product and any(product in term or term in product for term in product_terms if term))
        term_match = any(term and len(term) >= 4 and term in title_summary for term in product_terms)
        if ref_match or class_match or product_match or term_match:
            matches.append({
                "path": bundle.get("path", ""),
                "title": bundle.get("title", ""),
                "maturity": bundle.get("maturity", "unknown"),
                "vuln_classes": bundle.get("vuln_classes", []),
                "match_reason": "reference" if ref_match else "class" if class_match else "product_or_term",
            })
    maturity_order = {"verified": 0, "candidate": 1, "triage": 2, "attempted_not_verified": 3, "unknown": 4}
    return sorted(matches, key=lambda item: (maturity_order.get(str(item.get("maturity")), 9), item.get("title", "")))


def _classify(candidate: dict[str, Any], matched: list[dict[str, Any]]) -> str:
    routing = str(candidate.get("routing") or "").strip().lower()
    classes = set(_candidate_classes(candidate))
    if routing == "needs_authorized_live_target":
        return "needs_authorized_live_target"
    if routing == "reference_only_review" or not classes or classes == {"unknown/review"}:
        return "reference_only"
    if any(item.get("maturity") == "verified" for item in matched):
        return "covered_by_existing_bundle"
    if any(item.get("maturity") in {"candidate", "triage", "attempted_not_verified"} for item in matched):
        return "needs_bundle_update"
    if routing in {"local_bootstrap_review", "local_or_live_review_high_impact"}:
        return "new_local_bootstrap_candidate"
    return "reject_low_signal"


def _recommendation_score(item: dict[str, Any]) -> tuple[int, str]:
    order = {
        "new_local_bootstrap_candidate": 0,
        "needs_bundle_update": 1,
        "needs_authorized_live_target": 2,
    }
    return (order.get(item["classification"], 99), item["id"])


def _render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Bundle Freshness Delta — {payload['stamp']}",
        "",
        "Status: metadata-only bundle freshness delta / no target touched",
        "",
        "No scanners, PoCs, browser/noVNC, recon, account actions, or live targets were executed.",
        "This report only compares local vulnerability-intel candidates with local proof-bundle metadata.",
        "",
        f"Source vuln intel: `{payload['source_vuln_intel']}`",
        f"Bundle count: {payload['bundle_count']}",
        f"Candidate count: {len(payload['items'])}",
        "",
        "## Top recommendations",
    ]
    if payload["top_recommendations"]:
        for rec in payload["top_recommendations"]:
            lines.append(f"- {rec['id']} — {rec['classification']} — {rec.get('title','')}")
    else:
        lines.append("- None")
    lines.extend(["", "## Candidate classifications"])
    for item in payload["items"]:
        matched = ", ".join(match["title"] for match in item.get("matched_bundles", [])[:3]) or "none"
        lines.append(f"- {item['id']} — {item['classification']} — matched bundles: {matched}")
    lines.append("")
    return "\n".join(lines)


def build_delta(vuln_intel_file: Path, bundle_dir: Path, stamp: str) -> dict[str, Any]:
    candidates = json.loads(vuln_intel_file.read_text(encoding="utf-8"))
    if not isinstance(candidates, list):
        raise ValueError("vuln intel JSON must be a list")
    bundles = build_index(bundle_dir)
    items: list[dict[str, Any]] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        matched = _match_bundles(candidate, bundles)
        classification = _classify(candidate, matched)
        item = {
            "id": _candidate_id(candidate),
            "source": candidate.get("source", ""),
            "published": candidate.get("published", ""),
            "vendor_project": candidate.get("vendor_project", ""),
            "product": candidate.get("product", ""),
            "title": candidate.get("title", ""),
            "routing": candidate.get("routing", ""),
            "vuln_classes": candidate.get("vuln_classes", []),
            "classification": classification,
            "safe_proof_hint": candidate.get("safe_proof_hint", ""),
            "matched_bundles": matched[:5],
        }
        items.append(item)
    recommendations = sorted([item for item in items if item["classification"] in ACTIONABLE], key=_recommendation_score)[:3]
    return {
        "status": "ok",
        "stamp": stamp,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "target_touching": False,
        "source_vuln_intel": vuln_intel_file.as_posix(),
        "bundle_dir": bundle_dir.as_posix(),
        "bundle_count": len(bundles),
        "items": items,
        "top_recommendations": recommendations,
        "safety_note": "metadata-only; no scanners, PoCs, browser/noVNC, recon, account actions, or live targets executed",
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    rejected = _reject_target_like_args(argv)
    if rejected is not None:
        return rejected
    parser = argparse.ArgumentParser(description="Build metadata-only vuln-intel to proof-bundle freshness delta")
    parser.add_argument("--vuln-intel-dir", type=Path, default=DEFAULT_VULN_INTEL_DIR)
    parser.add_argument("--vuln-intel-file", type=Path, default=None)
    parser.add_argument("--bundle-dir", type=Path, default=DEFAULT_BUNDLE_DIR)
    parser.add_argument("--out-prefix", type=Path, default=None)
    parser.add_argument("--stamp", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    args = parser.parse_args(argv)

    vuln_file = args.vuln_intel_file or _latest_vuln_intel_file(args.vuln_intel_dir)
    out_prefix = args.out_prefix or (ROOT / "handoff" / "vuln_intel" / f"bundle_freshness_delta_{args.stamp}")
    payload = build_delta(vuln_file, args.bundle_dir, args.stamp)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = out_prefix.with_suffix(".json")
    md_path = out_prefix.with_suffix(".md")
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(_render_markdown(payload), encoding="utf-8")
    print(json.dumps({"status": "ok", "target_touching": False, "json": json_path.as_posix(), "md": md_path.as_posix()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
