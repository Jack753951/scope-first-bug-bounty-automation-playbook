> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersecurity Operating System

這是專案的能力地圖。目標不是把工具堆滿，而是建立一套可以長期訓練、實戰、回顧與交付的系統。

## 1. Foundations

- Linux、Windows、shell、Python、Git、資料格式、logging。
- Networking：OSI、TCP/IP、routing、subnetting、DNS、HTTP、TLS、SMTP、SMB、Kerberos、LDAP、RDP、SSH、VPN。
- Web：browser security、cookies、CORS、auth/session、OAuth/OIDC、API、GraphQL、file upload、deserialization。
- Cloud：IAM、networking、storage exposure、metadata services、logging、Kubernetes basics。
- Identity：AD、Kerberos、NTLM、ADCS、Azure / Entra ID basics。

## 2. Reconnaissance

Purpose: understand the target without exceeding scope.

- Scope validation and allowlists.
- Passive recon, DNS, WHOIS, certificate transparency, technology fingerprinting.
- Service discovery and version collection.
- Change tracking: new ports, new hosts, new technologies, exposed admin panels.
- Output: structured JSON, Markdown summary, evidence log, tool versions.

## 3. Vulnerability Assessment

Purpose: turn signals into verified risk.

- Use scanners as signal sources: nuclei, nikto, whatweb, nmap scripts, dependency scanners.
- Normalize by asset, weakness, evidence, confidence, severity, remediation.
- Track false positives.
- Keep proof minimal and non-destructive.
- Never ship raw scanner output as a finding.

## 4. Manual Web Testing

Core classes:

- Access control and IDOR
- Authentication and session management
- Injection: SQLi, command injection, SSTI, LDAP injection
- XSS and content injection
- SSRF and request smuggling research in labs
- File upload, LFI, path traversal
- CORS, redirects, headers, cookies
- JWT, OAuth, SAML, OIDC logic issues
- API and GraphQL authorization

Each class should eventually have:

- test checklist
- minimal proof pattern
- evidence guidance
- remediation notes
- detection / logging hints

## 5. Network, AD, And Internal Testing

- Network mapping and service enumeration.
- SMB, LDAP, Kerberos, RDP, WinRM, SSH basics.
- Active Directory attack paths in labs: BloodHound, Kerberoasting concepts, AS-REP roasting concepts, ACL issues, ADCS misconfigurations.
- Defensive pair: segmentation, least privilege, audit policy, LAPS / Windows LAPS, hardening, event IDs, detection notes.

## 6. Defense And Hardening

- Firewall policy: default deny, least exposure, egress control, admin access restrictions.
- Host hardening: SSH, sudo, service inventory, patching, file permissions.
- Web hardening: TLS, security headers, cookie flags, upload restrictions, rate limits.
- WAF / IDS / IPS: useful as guardrails, not substitutes for fixes.
- Monitoring: auditd, Sysmon, web logs, auth logs, DNS logs, cloud logs.
- Incident response: triage, containment, evidence preservation, eradication, recovery, lessons learned.

## 7. Vulnerability Intelligence

- Track CISA KEV, NVD, vendor advisories, GitHub security advisories, project release notes, and exploit maturity.
- Prioritize by exposure, affected technology, exploitability, asset criticality, and available mitigation.
- Maintain weekly reviews in `intelligence/weekly-reviews/`.
- Reproduce only in local labs or authorized environments.

## 8. Vulnerability Research

- Code review for common bug classes.
- Fuzzing in labs and local projects.
- Patch diffing and root-cause analysis.
- Minimal, non-destructive proof of concept.
- Responsible disclosure notes: timeline, vendor contact, affected/fixed versions, mitigation, detection.

## 9. Reporting

Professional reports should include:

- Executive summary
- Scope and rules of engagement
- Methodology
- Findings with severity, CVSS vector, CWE, OWASP, evidence, impact, remediation, retest steps
- Risk themes and remediation roadmap
- Appendix for tools, timestamps, limitations, and evidence handling

Internal notes can be messy while investigating. Client-ready reports must be precise, restrained, and verified.

## 10. Command And Technique Library

Store commands by task, not by tool. Each entry should include:

- Goal
- Preconditions
- Command
- Expected output
- How to interpret results
- Safety notes
- When not to use it

This turns random one-liners into reusable professional knowledge.
