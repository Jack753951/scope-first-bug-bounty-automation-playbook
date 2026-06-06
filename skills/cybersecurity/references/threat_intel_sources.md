> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Threat Intelligence & CVE Monitoring Reference

Read when the user asks "what's new in security," "how do I keep up with CVEs," or wants help triaging an advisory.

Goal: a practitioner should know about a high-impact bug affecting their stack within hours of disclosure, not weeks.

---

## 1. Authoritative feeds (start here)

| Source | What it gives you | Format |
|--------|-------------------|--------|
| **NVD** (nvd.nist.gov) | Master CVE database with CVSS, CPE, references | JSON, REST API, RSS |
| **CISA Known Exploited Vulnerabilities (KEV)** | Vulnerabilities under active exploitation in the wild — read this first | JSON feed, weekly updates |
| **CISA Alerts** (cisa.gov/news-events) | US-CERT advisories on major incidents | RSS, email |
| **MITRE CVE List** | CVE assignment metadata (parent of NVD) | JSON, GitHub repo |
| **GitHub Security Advisories (GHSA)** | OSS-specific, well-formatted, fast | RSS per ecosystem |
| **OSV** (osv.dev) | Aggregated open-source vulnerabilities, queryable by package + version | JSON API |
| **Exploit-DB** (exploit-db.com) | Public PoC code, mapped to CVE | RSS, web |

**Practical setup**: subscribe to CISA KEV + GHSA for your stack's ecosystem (npm, PyPI, Maven, etc.) + NVD high/critical RSS. That's 80% of signal for 20% of noise.

---

## 2. Vendor advisories (subscribe to whichever you run)

| Vendor | Channel |
|--------|---------|
| Microsoft | MSRC blog + Patch Tuesday summary (every 2nd Tuesday) |
| Cisco | Cisco Security Advisories RSS |
| Juniper | Juniper SIRT |
| Red Hat / RHEL | Red Hat Security Data API |
| Debian | DSA mailing list |
| Ubuntu | Ubuntu Security Notices RSS |
| Apple | Apple Security Releases page (no good RSS — scrape) |
| Google Chrome | Chrome releases blog |
| Mozilla | Mozilla Security Advisories |
| Atlassian | Atlassian Trust Center |
| AWS | AWS Security Bulletins |
| GCP | Google Cloud Security Bulletins |
| Azure | Microsoft Security Response Center |

**Set up a folder structure in your RSS reader (Feedly / Inoreader / FreshRSS) by criticality**: KEV / Vendor / Research / Background.

---

## 3. Research blogs worth following

- **Google Project Zero** — top-tier kernel / browser research.
- **PortSwigger Research** — best-in-class web research; "Top 10 Web Hacking Techniques" annual list.
- **Trail of Bits Blog** — security engineering, Web3, static analysis.
- **NCC Group Research** — pentest-flavored, occasional whitepapers.
- **GitHub Security Lab** — finding real CVEs at scale via CodeQL.
- **Microsoft Security Blog** — defensive perspective, threat actor reports.
- **Mandiant / Google TIC** — APT campaign reports.
- **SpecterOps** — Active Directory, BloodHound, red team.
- **Krebs on Security** — incident reporting, investigative.
- **The Record / The Hacker News / BleepingComputer** — daily news pulse.

---

## 4. CVE prioritisation — what actually matters

A CVE feed without prioritisation is noise. Use this order:

1. **In CISA KEV?** → drop everything, patch within the deadline KEV gives.
2. **Affects software you run + RCE/auth bypass?** → patch in 24–72 h.
3. **Public PoC exists?** → escalate priority by one tier.
4. **CVSS ≥ 9.0 + remote + unauth?** → patch within a week regardless.
5. **CVSS 7.0–8.9 + auth required?** → next regular patch window.
6. **Local-only, requires admin already?** → next regular patch.

CVSS alone is a bad sole metric. Use **EPSS** (epss.cyentia.com) for "probability of exploitation in the next 30 days" — combines well with CVSS.

---

## 5. Mapping a CVE to your stack — fast workflow

Given a fresh advisory, answer in this order:

1. **Affected software + version range?** → exact CPE strings on NVD.
2. **Do I run an affected version?** → check SBOM (CycloneDX/SPDX), or `dpkg -l | grep`, `pip freeze`, etc.
3. **Is the vulnerable code path actually reachable in my deployment?** → read the advisory carefully; many CVEs only trigger with specific config.
4. **Is there a workaround?** → vendor advisory often lists one.
5. **What's my patch SLA?** → see §4.
6. **Detection rule available?** → check Sigma HQ, vendor's GitHub, social media for proof-of-concept signatures.

---

## 6. Threat intel beyond CVEs — TTP-level

CVEs cover bugs. Threat intel covers *how attackers chain things*.

- **MITRE ATT&CK** (attack.mitre.org) — tactics, techniques, procedures library.
- **MITRE D3FEND** — defensive counterpart, mapping each technique to countermeasures.
- **Pyramid of Pain** (David Bianco) — heuristic for which IOCs are worth chasing.
- **MISP** (misp-project.org) — open-source threat-intel sharing platform.
- **AlienVault OTX** — community threat-intel feed.

---

## 7. Practical "stay current" routine (15 min/day)

1. Skim CISA KEV updates — anything new?
2. Skim GHSA for your ecosystems (npm/PyPI/etc) — anything affecting your direct deps?
3. Read top 1–2 stories on The Hacker News / BleepingComputer.
4. Once a week: read PortSwigger Research / Project Zero / SpecterOps if anything new is posted.
5. Once a month: refresh your SBOM and rerun OSV-Scanner / Snyk / Trivy against it.

---

## 8. Building your own monitoring (automation idea)

Quick wins worth scripting yourself:

```python
# pseudocode — extend recon_automation.py with this pattern

import requests, json, datetime

def fetch_kev():
    r = requests.get("https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json")
    return r.json()["vulnerabilities"]

def fetch_nvd_recent(days=1):
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(days=days)
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?pubStartDate={start:%Y-%m-%dT%H:%M:%S}.000&pubEndDate={end:%Y-%m-%dT%H:%M:%S}.000"
    return requests.get(url).json()["vulnerabilities"]

# Filter by your stack's vendor list, CVSS >= 7, then post to Slack webhook
```

If the user wants this as a real script, propose extending the existing `recon_automation.py` toolkit.

---

## 9. Red flags / sources to be careful with

- Random Telegram channels selling "0days" → mostly scams, sometimes illegal.
- Reddit /r/netsec — fine for news pulse, but verify before acting.
- Twitter/X security infosec community — fast, but also chaotic; verify with primary source before patching off a single tweet.
- "Vulnerability X is unpatched and has a public exploit" claims — check the CVE date, vendor advisory, and at least one independent confirmation before you push out an emergency change at 2 a.m.
