> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersecurity Expert Project Charter

## Mission

Build an authorized cybersecurity research and operations workspace that can support:

- learning and mastery across networking, web, cloud, endpoint, identity, and defensive operations
- repeatable reconnaissance and vulnerability assessment in labs or explicitly authorized scopes
- professional evidence collection, triage, reporting, remediation guidance, and retesting
- defensive engineering such as firewall rules, hardening baselines, monitoring notes, and incident response playbooks
- vulnerability intelligence tracking and safe lab reproduction of selected CVEs
- a structured command, technique, protocol, and report library that improves over time

This project should make you stronger as a cybersecurity practitioner without turning the workspace into an uncontrolled attack kit. The north star is: authorized, repeatable, explainable, defensible.

## Non-Negotiable Rules

1. Only test systems you own, operate, have written permission to assess, or that are intentionally provided as labs, CTFs, bug bounty scopes, or training targets.
2. Every real-world assessment needs scope, dates, target list, allowed techniques, rate limits, emergency contacts, and reporting expectations before scanning starts.
3. Findings must be verified and documented with evidence, impact, reproduction conditions, and remediation. Scanner output alone is not a finding.
4. Do not add stealth, persistence, evasion, credential theft, destructive actions, or malware behavior to this workspace.
5. Keep secrets out of the repository. Use environment variables or local ignored files for API keys, tokens, webhook URLs, and client data.
6. For public vulnerability research, reproduce in a controlled lab first, then follow responsible disclosure rules.

## Collaboration Model

### Human Owner

- Defines goals, legal scope, priorities, and acceptable risk.
- Decides which targets are in scope.
- Reviews reports before external delivery.
- Chooses when learning depth matters more than automation speed.

### Codex

- Maintains repo structure, scripts, tests, templates, and documentation.
- Turns vague goals into scoped tasks and implementation plans.
- Reviews generated scripts for safety, repeatability, and evidence quality.
- Builds defensive tools, report automation, lab workflows, and integration glue.

### Cowork

- Can work on larger implementation chunks, refactors, report generation flows, tests, and long-form documentation cleanup.
- Should receive small, well-scoped tasks with clear files, constraints, and done criteria.
- Should not be asked to run real-world scans unless the scope and authorization are already recorded.

### Hermes

- Can work on vulnerability intelligence, weekly CVE review, source comparison, report polish, executive summaries, and handoff notes.
- Should cite primary sources for current advisories, CVEs, vendor guidance, and exploitation status.
- Should not summarize scanner output as confirmed risk unless manual verification evidence is included.

## Agent Handoff Template

Use this when sending a task to Codex, Cowork, Hermes, or another assistant:

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

Example:

```text
Task: Add JSON schema validation to recon output.
Context: recon_automation.py writes Markdown and JSON reports.
Authorized scope: local code only; no network scanning.
Files to inspect: scripts/recon_automation.py, scripts/README.md
Files allowed to edit: scripts/recon_automation.py, tests/
Do not change: existing command-line flags unless necessary.
Expected output: schema validation helper and focused tests.
Verification: run unit tests and one dry-run with mocked tool output.
Safety constraints: no live target scanning.
```

## Core Workstreams

### 1. Foundations

- Linux, shell, Python, Git, networking, HTTP, TLS, DNS, identity, and logging.
- Build clean notes for protocols, common ports, packet analysis, and operating system behavior.
- Convert scattered notes into reusable reference pages.

### 2. Lab Infrastructure

- Keep Kali and vulnerable lab targets separated from personal systems.
- Maintain lab target inventory: IP, service, purpose, credentials, reset procedure.
- Prefer intentionally vulnerable apps such as Juice Shop, DVWA, WebGoat, Metasploitable, PortSwigger labs, HTB, THM, and CTF boxes.

### 3. Reconnaissance

- Build safe, configurable recon automation.
- Output structured data, command logs, timestamps, tool versions, and Markdown summaries.
- Support rate limits, scope allowlists, and dry-run mode before live execution.

### 4. Vulnerability Assessment

- Integrate scanners as signal sources, not truth sources.
- Normalize findings by severity, affected asset, evidence, confidence, and remediation.
- Track false positives and manual verification steps.

### 5. Manual Verification

- Create checklists for common classes: access control, auth/session, injection, SSRF, file handling, CORS, headers, redirects, JWT, dependency exposure, cloud misconfiguration.
- Keep proof steps minimal, non-destructive, and reportable.
- Capture screenshots, HTTP requests/responses, logs, and affected versions.

### 6. Reporting

- Produce professional reports with executive summary, scope, methodology, findings, risk rating, evidence, remediation, and retest status.
- Maintain finding templates mapped to CWE, OWASP, CVSS, and MITRE ATT&CK when relevant.
- Separate internal notes from client-ready language.

### 7. Defense And Hardening

- Build firewall, host hardening, SSH, web server, cloud, and logging checklists.
- Add scripts that audit configuration and produce remediation guidance.
- Treat defense as equal to offense: every exploit class should have a detection and prevention note.

### 8. Vulnerability Intelligence

- Track CVEs, vendor advisories, CISA KEV, exploit maturity, affected products, mitigations, and lab reproduction status.
- Avoid chasing every headline. Prioritize technologies you actually use or study.
- Add a weekly review ritual: what changed, what matters, what to reproduce, what to ignore.

### 9. Research And Safe Exploit Development

- Study root causes in lab conditions.
- Reproduce known vulnerabilities only on local or authorized targets.
- Document vulnerable version, fixed version, trigger condition, impact, mitigation, and detection.
- Keep PoCs minimal and non-destructive.

### 10. Command And Technique Library

- Store commands by goal, preconditions, expected output, interpretation, and safety notes.
- Prefer reusable checklists over random command dumps.
- Include "when not to use this" notes for risky tools.

## Proposed Repository Shape

```text
hacking/
  PROJECT_CHARTER.md
  AGENTS.md
  CYBERSECURITY_OPERATING_SYSTEM.md
  README.md
  scripts/
    recon/
    vuln-assessment/
    defense/
    report/
  notes/
    protocols/
    web-security/
    network-security/
    cloud-security/
    windows-ad/
    linux/
  reports/
    templates/
    samples/
  defense/
  command-library/
  labs/
    inventory.md
    runbooks/
  intelligence/
    cve-watch.md
    weekly-reviews/
  skills/
```

The current repository already has several of these ideas. Future cleanup should migrate gradually instead of moving everything at once.

## First Milestones

### Milestone 1: Make The Workspace Reliable

- Fix or replace mojibake/encoding-damaged Markdown files.
- Add a clean script index with purpose, inputs, outputs, dependencies, and safety notes.
- Add a target scope file format for authorized assessments.
- Add dry-run support where scripts can show planned actions before running tools.

### Milestone 2: Improve Recon And Reports

- Standardize JSON output across recon and scanner scripts.
- Generate Markdown reports with consistent sections.
- Add tool version capture and command provenance.
- Add tests for parsing and report generation.

### Milestone 3: Build Defensive Counterparts

- Add firewall and hardening audit templates.
- Add security header, TLS, SSH, and Linux baseline checks.
- Create "finding to fix" mappings for common issues.

### Milestone 4: Add Intelligence Workflow

- Create a weekly CVE review template.
- Track affected technology, exploit maturity, mitigation, detection, and reproduction notes.
- Keep live exploit reproduction inside lab notes only.

## Definition Of Done

A new script, checklist, or report workflow is done when:

- it states allowed use and assumptions
- it has clear inputs and outputs
- it refuses or warns on missing scope when appropriate
- it records tool versions and timestamps
- it produces human-readable output and structured output when useful
- it has a basic verification path
- it avoids secrets and unnecessary destructive behavior

## Immediate Next Actions

1. Add shared scope validation and dry-run support to target-touching scripts.
2. Create sample parser outputs so report generation can be tested without live scans.
3. Expand `defense/` with SSH, Linux, web server, TLS, and logging baselines.
4. Convert high-value notes into `notes/protocols/` and `command-library/`.
5. Start weekly reviews from `intelligence/weekly-reviews/TEMPLATE.md`.
