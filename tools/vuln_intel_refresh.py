#!/usr/bin/env python3
"""One-shot vulnerability intelligence refresh for Cybersec Lab Phase 5A.

This script is intentionally intake-only:
- fetches public advisory metadata from allowlisted sources;
- writes compact candidate artifacts;
- classifies routing for local/bootstrap/live-scope planning;
- does not scan, exploit, bootstrap containers, or touch any target.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "handoff" / "vuln_intel"
USER_AGENT = "CybersecLabPhase5AIntake/0.1 (+local research; no target touch)"

CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
NVD_RECENT_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate={start}&pubEndDate={end}"
GITHUB_ADVISORIES_URL = "https://api.github.com/advisories?per_page={limit}&sort=published&direction=desc"

CLASS_PATTERNS: list[tuple[str, str]] = [
    (r"\b(ssrf|server-side request forgery)\b", "ssrf"),
    (r"\b(xxe|xml external entity)\b", "xxe"),
    (r"\b(path traversal|directory traversal|file read|arbitrary file)\b", "file-read/path-traversal"),
    (r"\b(deseriali[sz]ation|pickle|unserialize)\b", "deserialization"),
    (r"\b(command injection|remote code execution|rce|code execution)\b", "rce/command-execution"),
    (r"\b(sql injection|sqli)\b", "sqli"),
    (r"\b(cross-site scripting|xss)\b", "xss"),
    (r"\b(authentication bypass|authorization bypass|access control|idor|privilege escalation)\b", "auth/access-control"),
    (r"\b(open redirect|redirect)\b", "redirect"),
    (r"\b(upload|zip slip|archive extraction)\b", "upload/archive"),
]

LOCAL_HINTS = [
    "apache", "tomcat", "nginx", "wordpress", "joomla", "drupal", "jenkins",
    "gitlab", "grafana", "prometheus", "elasticsearch", "kibana", "spring",
    "struts", "webgoat", "juice", "docker", "container", "api", "flask",
]

LIVE_HEAVY_HINTS = [
    "cloud", "saas", "tenant", "oauth", "saml", "account", "billing", "workspace",
    "managed", "hosted", "identity provider", "idp", "email", "mobile app",
]

HIGH_RISK_CLASSES = {"rce/command-execution", "deserialization", "ssrf", "file-read/path-traversal", "xxe"}


def fetch_json(url: str, timeout: int = 25) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def compact_text(value: Any, limit: int = 420) -> str:
    text = " ".join(str(value or "").replace("\n", " ").split())
    return text[:limit] + ("…" if len(text) > limit else "")


def classify_vuln(text: str) -> tuple[str, list[str]]:
    labels: list[str] = []
    for pattern, label in CLASS_PATTERNS:
        if re.search(pattern, text, re.I):
            labels.append(label)
    if not labels:
        labels.append("unknown/review")
    risk = "high" if any(label in HIGH_RISK_CLASSES for label in labels) else "medium"
    if labels == ["unknown/review"]:
        risk = "unknown"
    return risk, labels


def route_candidate(text: str, labels: list[str], source: str) -> str:
    low = text.lower()
    local_score = sum(1 for hint in LOCAL_HINTS if hint in low)
    live_score = sum(1 for hint in LIVE_HEAVY_HINTS if hint in low)

    if live_score > local_score and any(label in {"auth/access-control", "ssrf", "xss", "redirect"} for label in labels):
        return "needs_authorized_live_target"
    if local_score > 0:
        return "local_bootstrap_review"
    if source == "CISA KEV" and any(label in HIGH_RISK_CLASSES for label in labels):
        return "local_or_live_review_high_impact"
    return "reference_only_review"


def safe_proof_hint(labels: list[str], route: str) -> str:
    if "auth/access-control" in labels:
        return "Use throwaway accounts, role/account matrix, positive + negative controls, and no real data retention."
    if "xss" in labels:
        return "Use browser/runtime safe marker only; no cookie theft, keylogging, or victim interaction."
    if "ssrf" in labels:
        return "Use callback/OAST only if explicitly allowed; prefer DNS-only marker; no metadata/internal scanning."
    if "file-read/path-traversal" in labels or "xxe" in labels:
        return "Use lab-owned marker or authorized synthetic file only; no secret/system file collection."
    if "rce/command-execution" in labels or "deserialization" in labels:
        return "Requires explicit authorization; use marker-only bounded action, pre/post health, and human confirmation gate."
    if "sqli" in labels:
        return "Use bounded boolean/time-free controls or synthetic data only; no dumping or broad extraction."
    return "Review manually; do not touch targets until scope and safe proof plan are explicit."


def normalize_cisa(limit: int) -> list[dict[str, Any]]:
    data = fetch_json(CISA_KEV_URL)
    vulns = data.get("vulnerabilities", [])[-limit:]
    out = []
    for item in reversed(vulns):
        text = " ".join(str(item.get(k, "")) for k in ["cveID", "vendorProject", "product", "vulnerabilityName", "shortDescription", "requiredAction"])
        risk, labels = classify_vuln(text)
        route = route_candidate(text, labels, "CISA KEV")
        out.append({
            "source": "CISA KEV",
            "id": item.get("cveID", "unknown"),
            "published": item.get("dateAdded", ""),
            "vendor_project": item.get("vendorProject", ""),
            "product": item.get("product", ""),
            "title": item.get("vulnerabilityName", ""),
            "summary": compact_text(item.get("shortDescription", "")),
            "vuln_classes": labels,
            "risk": risk,
            "routing": route,
            "safe_proof_hint": safe_proof_hint(labels, route),
            "references": item.get("notes", ""),
        })
    return out


def normalize_nvd(days: int, limit: int) -> list[dict[str, Any]]:
    end = dt.datetime.now(dt.timezone.utc)
    start = end - dt.timedelta(days=days)
    url = NVD_RECENT_URL.format(
        start=start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        end=end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    )
    data = fetch_json(url)
    vulns = data.get("vulnerabilities", [])[:limit]
    out = []
    for wrapper in vulns:
        cve = wrapper.get("cve", {})
        descriptions = cve.get("descriptions", [])
        desc = next((d.get("value", "") for d in descriptions if d.get("lang") == "en"), descriptions[0].get("value", "") if descriptions else "")
        metrics = cve.get("metrics", {})
        cvss = None
        for key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
            if key in metrics and metrics[key]:
                cvss = metrics[key][0].get("cvssData", {}).get("baseScore")
                break
        text = " ".join([cve.get("id", ""), desc])
        risk, labels = classify_vuln(text)
        route = route_candidate(text, labels, "NVD")
        raw_refs = cve.get("references", [])
        if isinstance(raw_refs, dict):
            raw_refs = raw_refs.get("referenceData", [])
        refs = [r.get("url") for r in raw_refs[:5] if isinstance(r, dict) and r.get("url")]
        out.append({
            "source": "NVD recent",
            "id": cve.get("id", "unknown"),
            "published": cve.get("published", ""),
            "vendor_project": "",
            "product": "",
            "title": compact_text(desc, 110),
            "summary": compact_text(desc),
            "cvss": cvss,
            "vuln_classes": labels,
            "risk": risk,
            "routing": route,
            "safe_proof_hint": safe_proof_hint(labels, route),
            "references": refs,
        })
    return out


def normalize_github(limit: int) -> list[dict[str, Any]]:
    data = fetch_json(GITHUB_ADVISORIES_URL.format(limit=limit))
    out = []
    for item in data[:limit]:
        cves = item.get("cves") or []
        ident = cves[0] if cves else item.get("ghsa_id", "unknown")
        text = " ".join([ident, item.get("summary", ""), item.get("description", ""), item.get("ecosystem", ""), item.get("package", {}).get("name", "")])
        risk, labels = classify_vuln(text)
        route = route_candidate(text, labels, "GitHub Advisory")
        out.append({
            "source": "GitHub Advisory",
            "id": ident,
            "published": item.get("published_at", ""),
            "vendor_project": item.get("ecosystem", ""),
            "product": item.get("package", {}).get("name", ""),
            "title": item.get("summary", ""),
            "summary": compact_text(item.get("description", item.get("summary", ""))),
            "severity": item.get("severity", ""),
            "vuln_classes": labels,
            "risk": risk,
            "routing": route,
            "safe_proof_hint": safe_proof_hint(labels, route),
            "references": item.get("html_url", ""),
        })
    return out


def sort_key(item: dict[str, Any]) -> tuple[int, str]:
    route_weight = {
        "local_bootstrap_review": 0,
        "local_or_live_review_high_impact": 1,
        "needs_authorized_live_target": 2,
        "reference_only_review": 3,
    }.get(item.get("routing", ""), 4)
    return (route_weight, str(item.get("published", "")))


def write_outputs(candidates: list[dict[str, Any]], outdir: Path, stamp: str) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    json_path = outdir / f"vuln_intel_candidates_{stamp}.json"
    md_path = outdir / f"vuln_intel_candidates_{stamp}.md"
    csv_path = outdir / f"vuln_intel_candidates_{stamp}.csv"

    json_path.write_text(json.dumps(candidates, indent=2, ensure_ascii=False), encoding="utf-8")

    fields = ["source", "id", "published", "vendor_project", "product", "title", "vuln_classes", "risk", "routing", "safe_proof_hint"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for item in candidates:
            row = {k: item.get(k, "") for k in fields}
            row["vuln_classes"] = ",".join(item.get("vuln_classes", []))
            writer.writerow(row)

    lines = [
        f"# Vulnerability Intelligence Candidates — {stamp}",
        "",
        "Status: one-shot intake / no target touched",
        "Source: CISA KEV, NVD recent, GitHub Security Advisories when reachable",
        "Boundary: metadata-only; no scanning, exploit execution, target bootstrap, live-target probing, or report submission.",
        "",
        "## Routing meanings",
        "",
        "- `local_bootstrap_review`: likely worth reviewing for a faithful local target or fixture.",
        "- `local_or_live_review_high_impact`: high-impact class; review for local reproduction first, otherwise ask operator for legal scope.",
        "- `needs_authorized_live_target`: do not drop; ask operator for legal target/scope/rules if chosen.",
        "- `reference_only_review`: keep as reference unless it maps to current scope or a clear local target.",
        "",
        "## Top candidates",
        "",
        "| # | Source | ID | Product | Classes | Routing | Safe proof hint |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for idx, item in enumerate(candidates[:20], start=1):
        lines.append(
            "| {idx} | {source} | {id} | {product} | {classes} | {routing} | {hint} |".format(
                idx=idx,
                source=str(item.get("source", "")).replace("|", "\\|"),
                id=str(item.get("id", "")).replace("|", "\\|"),
                product=compact_text(" / ".join([str(item.get("vendor_project", "")), str(item.get("product", ""))]).strip(" / "), 80).replace("|", "\\|"),
                classes=",".join(item.get("vuln_classes", [])).replace("|", "\\|"),
                routing=str(item.get("routing", "")).replace("|", "\\|"),
                hint=compact_text(item.get("safe_proof_hint", ""), 130).replace("|", "\\|"),
            )
        )
    lines.extend([
        "",
        "## Next operator decision",
        "",
        "Pick at most one candidate. If routing is `needs_authorized_live_target`, provide the Phase 5A scope package before any target-touching work. If routing is local, create a bounded local bootstrap plan first.",
        "",
        f"JSON: `{json_path.as_posix()}`",
        f"CSV: `{csv_path.as_posix()}`",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {md_path}")
    print(f"wrote {json_path}")
    print(f"wrote {csv_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 5A one-shot vulnerability intelligence intake")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--stamp", default=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    parser.add_argument("--limit", type=int, default=10, help="per-source item limit")
    parser.add_argument("--nvd-days", type=int, default=7)
    parser.add_argument("--source", choices=["all", "cisa", "nvd", "github"], default="all")
    args = parser.parse_args()

    candidates: list[dict[str, Any]] = []
    errors: list[str] = []
    loaders = []
    if args.source in {"all", "cisa"}:
        loaders.append(("CISA KEV", lambda: normalize_cisa(args.limit)))
    if args.source in {"all", "nvd"}:
        loaders.append(("NVD", lambda: normalize_nvd(args.nvd_days, args.limit)))
    if args.source in {"all", "github"}:
        loaders.append(("GitHub Advisory", lambda: normalize_github(args.limit)))

    for name, loader in loaders:
        try:
            candidates.extend(loader())
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, IndexError) as exc:
            errors.append(f"{name}: {exc}")

    if not candidates:
        for err in errors:
            print(f"ERROR {err}", file=sys.stderr)
        return 2

    candidates.sort(key=sort_key)
    if errors:
        for err in errors:
            print(f"WARN {err}", file=sys.stderr)
    write_outputs(candidates, args.outdir, args.stamp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
