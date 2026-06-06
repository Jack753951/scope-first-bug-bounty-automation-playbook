> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Attack Chain Methodology — PTES × MITRE ATT&CK

Use this as the spine for any engagement. Each phase has a goal, the standard toolset, and the matching MITRE tactic.

---

## Phase 1 — Pre-Engagement
**Goal**: Define rules of engagement; written authorization; emergency contacts.
- Scope: in-scope IPs / domains, excluded targets, testing window, allowed techniques.
- Communication channels for stop-test signal.
- Data handling: PII redaction, retention policy, secure transport.

## Phase 2 — Intelligence Gathering / Reconnaissance
**MITRE**: TA0043 Reconnaissance, TA0042 Resource Development.
- **Passive**: WHOIS, DNS records, crt.sh, Wayback Machine, Shodan, Censys, GitHub leaks, LinkedIn.
- **Active (only if scope allows)**: subfinder, amass, ffuf for content discovery.
- Tool: bundled `recon_automation.py` for whois + DNS + subdomain + Nmap.

## Phase 3 — Threat Modeling
**Goal**: Map likely attack paths to the asset's value.
- STRIDE per component; rank by impact × likelihood.
- Identify trust boundaries (where data crosses authentication zones).

## Phase 4 — Vulnerability Analysis
**MITRE**: TA0007 Discovery + parts of TA0001 Initial Access (probing).
- Web: Burp Suite scan, nuclei, sqlmap (manual), nikto.
- Network: Nmap NSE scripts, masscan, banner grabbing.
- AD: BloodHound collection.
- Tool: bundled `vuln_scan_integration.py`.

## Phase 5 — Exploitation
**MITRE**: TA0001 Initial Access, TA0002 Execution.
- Choose the lowest-risk exploit that proves the issue (don't chain to RCE if XSS is enough for the report).
- Document each request/response.
- Avoid destructive payloads; avoid DoS unless explicitly in scope.

## Phase 6 — Post-Exploitation
**MITRE**: TA0003 Persistence, TA0004 Privilege Escalation, TA0005 Defense Evasion, TA0006 Credential Access, TA0008 Lateral Movement, TA0009 Collection.
- Privilege escalation: LinPEAS / WinPEAS / GTFOBins / PowerUp.
- Lateral movement: SOCKS via chisel/ligolo-ng; SMB relays; pass-the-X.
- Loot: hashes (NTDS.dit), tokens, configs; never exfiltrate real PII.
- Cleanup: remove created accounts, scheduled tasks, web shells; document all artefacts.

## Phase 7 — Reporting
**Goal**: Make business risk obvious to non-technical readers.
- Use the bundled `assets/pentest_report_outline.md`.
- One executive summary page (no jargon).
- Each finding: Severity + CVSS 3.1 vector + CWE + OWASP + Description + Impact + PoC + Remediation + Reference.
- Attach raw evidence as appendix; the body must read as narrative.

---

## MITRE ATT&CK quick mapping table

| Pentest activity | ATT&CK tactic | Common technique IDs |
|------------------|---------------|----------------------|
| Subdomain enum, OSINT | Reconnaissance | T1595, T1589, T1590 |
| Phishing pretext | Initial Access | T1566 |
| SQLi / RCE on web | Initial Access | T1190 |
| Reverse shell payload | Execution | T1059 (.001 PowerShell, .004 Unix shell) |
| Service install / cron | Persistence | T1543, T1053 |
| GTFOBins SUID | Privilege Escalation | T1548.001 |
| Mimikatz / lsass dump | Credential Access | T1003.001 |
| Kerberoasting | Credential Access | T1558.003 |
| BloodHound collection | Discovery | T1482, T1087 |
| Pass-the-Hash | Lateral Movement | T1550.002 |
| Data staging | Collection | T1074 |
| Exfil over HTTPS | Exfiltration | T1041 |

---

## Reporting clock — typical engagement weights

| Phase | % of total time |
|-------|-----------------|
| Pre-engagement | 5% |
| Recon + threat modeling | 15% |
| Vuln analysis + exploitation + post-ex | 50% |
| **Reporting** | **30%** |

If reporting feels too long, your findings aren't well documented. Reporting is the deliverable.
