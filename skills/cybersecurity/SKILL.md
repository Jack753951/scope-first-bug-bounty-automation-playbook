> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

---
name: cybersecurity
version: "2.1"
last-updated: "2026-05-12"
description: "Use for authorized cybersecurity work: pentesting, vulnerability research, bug bounty, CVE/threat intelligence, defensive architecture, firewall/WAF/IDS hardening, incident response, automation scripting, lab work, and professional reporting."
---

# Cybersecurity Skill

Operating manual for offensive security, defense, vulnerability research, threat intelligence, incident response, automation, and reporting.

## Always Apply

1. Legality is a precondition. Active scanning or exploitation requires an owned asset, written authorization, explicit bug bounty scope, or a legal lab such as HTB, THM, VulnHub, PortSwigger Academy, DVWA, Juice Shop, WebGoat, or Metasploitable.
2. If authorization is unclear, ask for scope before giving active payloads, scan commands, or exploit steps.
3. Do not create stealth, persistence, malware, credential theft, destructive actions, evasion, or unauthorized access workflows.
4. Scanner output is triage only. Confirm findings manually before reporting.
5. Keep secrets, credentials, tokens, client data, and sensitive evidence out of the repository.
6. For current CVEs, advisories, exploitation status, vendor guidance, or "latest" questions, use fresh primary sources before answering.
7. Pair offense with defense. Every technique should eventually have a prevention, detection, or remediation note.

## Authorization Triage

Proceed when the target is clearly one of:

- local lab or intentionally vulnerable app
- CTF / training platform
- asset owned or operated by the user
- bug bounty program with the target in scope
- client engagement with written authorization and rules of engagement

Pause and ask for scope when:

- the target is a public production system and ownership is unclear
- the user asks for brute force, exploitation, credential attacks, or high-volume scanning
- the user gives a company, domain, IP, or account without explaining authorization

Refuse and redirect when the request involves:

- accessing someone else's account, messages, device, or data
- bypassing monitoring, DRM, licensing, or access controls outside authorized testing
- deleting logs, hiding activity, persistence, stealth, malware, ransomware, or credential theft
- attacking a real third-party service without program scope or written permission

## Modes

### Mode A: Authorized Offensive Engagement

Use for pentests, CTFs, labs, bug bounty, recon, vulnerability assessment, manual verification, and report preparation.

Read as needed:

- `references/attack_chain_methodology.md`
- `references/owasp_top10_quickref.md`
- `references/ad_pentest_quickref.md`
- `references/bug_bounty_workflow.md`
- workspace `command-library/README.md`

Companion scripts:

- `scripts/recon_automation.py`
- `scripts/vuln_scan_integration.py`

### Mode B: Defense And Hardening

Use for firewall, WAF, IDS/IPS, fail2ban, SSH, web server hardening, logging, segmentation, and cloud/kubernetes hardening.

Read as needed:

- `references/defense_hardening.md`
- `references/cloud_security.md`
- workspace `defense/firewall-baseline.md`

### Mode C: Vulnerability Research

Use for fuzzing, source review, patch diffing, safe proof of concept, root-cause analysis, and responsible disclosure.

Read:

- `references/vulnerability_research.md`

Keep reproduction in local or authorized labs.

### Mode D: Threat Intelligence

Use for CVEs, vendor advisories, CISA KEV, exploit maturity, patch priority, and weekly review.

Read:

- `references/threat_intel_sources.md`
- workspace `intelligence/cve-watch.md`
- workspace `intelligence/weekly-reviews/TEMPLATE.md`

Use current primary sources for anything time-sensitive.

### Mode E: Education And Career

Use for study plans, certifications, lab progression, and learning paths.

Read:

- `references/learning_paths.md`
- workspace `CYBERSECURITY_OPERATING_SYSTEM.md`

### Mode F: Incident Response

Use for live or recent compromise, suspicious files, ransomware, web shells, stolen credentials, cloud account abuse, or forensic triage.

Read:

- `references/incident_response.md`
- `assets/ir_playbook_template.md`

Preserve evidence before cleanup when possible. Separate containment, eradication, recovery, and lessons learned.

## Reporting Standards

Each confirmed finding should include:

- title
- severity
- CVSS 3.1 vector and score
- affected asset
- summary
- business impact
- technical details
- evidence
- reproduction conditions
- root cause
- remediation
- retest steps
- CWE
- OWASP category when relevant
- references
- confidence

Use:

- `assets/pentest_report_outline.md`
- `assets/finding_template.md`
- workspace `reports/templates/finding.md`

## Automation Standards

New security scripts should:

- state allowed use and assumptions
- support clear inputs and outputs
- warn or refuse when scope is missing for target-touching actions
- support dry-run where practical
- record timestamps, tool versions, and command provenance
- produce Markdown for humans and JSON for automation when useful
- avoid secrets and destructive behavior
- include a local verification path

Prefer extending existing workspace scripts before creating new ones.

## Agent Collaboration

Use workspace `AGENTS.md` for Codex, Cowork, and Hermes task boundaries.

Default ownership:

- Codex: repo structure, scripts, tests, safety review, implementation hygiene
- Cowork: larger implementation chunks, refactors, documentation cleanup, test expansion
- Hermes: current intelligence, source comparison, weekly reviews, executive summaries, report polish

## Handoff Template

```text
Task:
Context:
Authorized scope:
Files to inspect:
Files allowed to edit:
Do not change:
Expected output:
Verification:
Safety constraints:
```

## Output Style

- Be precise about what is proven and what is only suspected.
- Prefer minimal, non-destructive proof.
- Cite primary sources for CVEs and advisories.
- Separate short-term mitigation from long-term remediation.
- Include detection or logging guidance when useful.
- Avoid dumping raw scanner logs into final reports.
