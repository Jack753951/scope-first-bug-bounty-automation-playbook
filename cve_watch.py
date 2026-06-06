#!/usr/bin/env python3
"""
cve_watch.py — daily CVE briefing for a fixed watchlist of web-server / proxy tech.

Queries the NVD API 2.0 for CVEs *published* (or modified) in the last N hours
that mention any of the watch keywords. Outputs:
  - a human-readable Markdown brief sorted by CVSS severity, and
  - a JSON dump for downstream tooling.

Designed to run as a daily Windows Task Scheduler / cron job, OR to be driven
by a Claude scheduled task that calls it via the workspace bash.

Watch keywords default to the high-yield bug-bounty targets:
    nginx, apache, tomcat, openssl, haproxy, envoy, traefik

Usage
-----
  python cve_watch.py                                      # last 24h, default keywords
  python cve_watch.py --hours 48 --keywords nginx,tomcat
  python cve_watch.py --min-cvss 7.0 --out-md intelligence/cve_briefs/cve_brief.md --out-json intelligence/cve_briefs/cve_brief.json

Notes
-----
- NVD's public endpoint is rate-limited (~5 req / 30s without an API key).
  The script paces itself; pass --api-key for higher throughput.
- The script uses pubStartDate / pubEndDate by default. Pass --modified to
  switch to lastModStartDate / lastModEndDate (catches updated CVSS scores).
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

DEFAULT_KEYWORDS = ["nginx", "apache", "tomcat", "openssl", "haproxy", "envoy", "traefik"]
NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def iso(dt):
    # NVD requires ISO 8601 with milliseconds, no offset suffix issues
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000")


def fetch(keyword, start, end, modified, api_key):
    params = {"keywordSearch": keyword, "resultsPerPage": 200}
    if modified:
        params["lastModStartDate"] = iso(start)
        params["lastModEndDate"] = iso(end)
    else:
        params["pubStartDate"] = iso(start)
        params["pubEndDate"] = iso(end)
    url = NVD_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "cve-watch/1.0"})
    if api_key:
        req.add_header("apiKey", api_key)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def cvss_of(item):
    metrics = (item.get("cve") or {}).get("metrics") or {}
    # Prefer v4, then v3.1, then v3.0, then v2
    for key in ("cvssMetricV40", "cvssMetricV31", "cvssMetricV30"):
        arr = metrics.get(key) or []
        if arr:
            d = arr[0].get("cvssData") or {}
            return d.get("baseScore"), d.get("baseSeverity"), key.replace("cvssMetric", "v").lower()
    arr = metrics.get("cvssMetricV2") or []
    if arr:
        d = arr[0].get("cvssData") or {}
        return d.get("baseScore"), arr[0].get("baseSeverity"), "v2"
    return None, None, None


def description(item):
    descs = (item.get("cve") or {}).get("descriptions") or []
    for d in descs:
        if d.get("lang") == "en":
            return d.get("value", "").strip()
    return ""


def refs(item):
    out = []
    for r in (item.get("cve") or {}).get("references") or []:
        u = r.get("url")
        if u:
            out.append(u)
    return out[:5]


def collect(keywords, hours, modified, api_key):
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    found = {}
    for kw in keywords:
        sys.stderr.write(f"[*] NVD: keyword={kw}  window={hours}h\n")
        try:
            data = fetch(kw, start, end, modified, api_key)
        except Exception as e:
            sys.stderr.write(f"    error: {type(e).__name__}: {e}\n")
            time.sleep(7)
            continue
        items = data.get("vulnerabilities", []) or []
        sys.stderr.write(f"    {len(items)} result(s)\n")
        for v in items:
            cid = (v.get("cve") or {}).get("id")
            if not cid:
                continue
            score, sev, ver = cvss_of(v)
            entry = found.get(cid) or {
                "id": cid,
                "published": (v.get("cve") or {}).get("published"),
                "modified": (v.get("cve") or {}).get("lastModified"),
                "cvss": score,
                "severity": sev,
                "cvss_version": ver,
                "description": description(v),
                "references": refs(v),
                "keywords": [],
            }
            if kw not in entry["keywords"]:
                entry["keywords"].append(kw)
            found[cid] = entry
        # be polite to the public endpoint
        time.sleep(0 if api_key else 7)
    return list(found.values())


def render_markdown(entries, hours, min_cvss):
    entries = [e for e in entries if (e.get("cvss") or 0) >= min_cvss]
    entries.sort(key=lambda e: (-(e.get("cvss") or 0), e["id"]))
    now = datetime.now(timezone.utc).isoformat(timespec="minutes")
    lines = [
        f"# CVE briefing — {now}",
        "",
        f"_Window: last **{hours} h** • Minimum CVSS: **{min_cvss}** • Source: NVD API 2.0_",
        "",
    ]
    if not entries:
        lines.append("_No CVEs matched the watchlist in this window._")
        return "\n".join(lines)

    for e in entries:
        score = e.get("cvss") or "—"
        sev = e.get("severity") or "—"
        kws = ", ".join(e.get("keywords") or [])
        lines += [
            f"## {e['id']} — CVSS {score} ({sev})",
            f"- **Keywords matched:** {kws}",
            f"- **Published:** {e.get('published') or '—'}  ·  **Modified:** {e.get('modified') or '—'}",
            "",
            (e.get("description") or "").strip(),
            "",
            "**References:**",
        ]
        for r in e.get("references") or []:
            lines.append(f"- {r}")
        lines.append("")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Daily CVE briefing from NVD for a watchlist.")
    p.add_argument("--keywords", default=",".join(DEFAULT_KEYWORDS),
                   help=f"Comma-separated keywords (default: {','.join(DEFAULT_KEYWORDS)})")
    p.add_argument("--hours", type=int, default=24,
                   help="Look-back window in hours (default: 24)")
    p.add_argument("--modified", action="store_true",
                   help="Use lastModified window instead of published (catches re-scored CVEs)")
    p.add_argument("--min-cvss", type=float, default=0.0,
                   help="Filter out CVEs below this CVSS base score (default: 0)")
    p.add_argument("--out-md", default="intelligence/cve_briefs/cve_brief.md", help="Markdown output path")
    p.add_argument("--out-json", default="intelligence/cve_briefs/cve_brief.json", help="JSON output path")
    p.add_argument("--api-key", help="NVD API key (optional, raises rate limit)")
    args = p.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    entries = collect(keywords, args.hours, args.modified, args.api_key)

    from pathlib import Path

    Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)

    with open(args.out_json, "w") as f:
        json.dump(entries, f, indent=2)
    md = render_markdown(entries, args.hours, args.min_cvss)
    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write(md)

    sys.stderr.write(f"[+] {len(entries)} CVE(s) collected -> {args.out_md} / {args.out_json}\n")


if __name__ == "__main__":
    main()
