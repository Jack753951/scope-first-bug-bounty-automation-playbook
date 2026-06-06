> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Extensible Cybersecurity Lab Architecture

Use when a cybersecurity workspace should evolve into a reusable authorized testing / bug bounty platform rather than a collection of one-off scripts.

## Goal

Design for maintainability, updateability, and safe extension:

- clear authorization and scope gates
- program-specific rules and testing windows
- modular vulnerability checks/scripts
- reproducible validation and audit logs
- triage-only scanner output until manually verified
- structured evidence/report workflows
- multi-agent implementation with independent review

## Core Principles

1. **Safety gate is central**
   - No script or module bypasses global scope, program scope, technique gates, dry-run/live-mode checks, or audit logging.

2. **Policy/data separate from execution**
   - Global authorization: `config/scope.txt`.
   - Program rules: `programs/<slug>/scope.json`.
   - Future module metadata: `modules/**/module.json`.
   - Execution engines read policy/metadata and default-deny on ambiguity.

3. **Versioned contracts**
   - Use schema versions for program scope, module manifests, finding records, and report artifacts.
   - Prefer explicit JSON/Markdown artifacts over hidden shell-condition behavior.

4. **Modular vulnerability checks**
   - Checks declare name, category, technique tags, target types, risk, dry-run support, network requirements, external tools, and output schema.
   - Modules are opt-in via profile/allowlist; never auto-run just because a file exists.

5. **Composable pipeline stages**
   - Recon -> vulnerability checks -> triage -> manual verification -> report drafting -> retest.
   - Each stage consumes structured input and emits structured output.

6. **Auditability**
   - Every allow/deny decision includes a reason.
   - Automated findings remain candidates until evidence, impact, remediation, and retest notes are added.

## Possible Future Layout

```text
programs/
  <program-slug>/
    scope.json
    authorization.txt
    README.md

modules/
  _schema/
    module.schema.json
    finding.schema.json
  checks/
    web/
      headers_security/
        module.json
        run.sh or run.py
        README.md
        tests/
      exposed_git/
        module.json
        run.sh or run.py
    cves/
      cve_YYYY_NNNN/
        module.json
        run.sh or run.py
        references.md
  profiles/
    safe-baseline.json
    web-passive.json
    lab-active.json
```

## Example Module Manifest Concept

```json
{
  "schema_version": "1.0",
  "name": "headers_security",
  "category": "web-passive",
  "techniques": ["http_probe", "vulnerability_scan_passive"],
  "target_types": ["url", "domain"],
  "risk": "low",
  "dry_run_supported": true,
  "requires_network": true,
  "external_tools": ["curl"],
  "outputs": "finding.schema.json"
}
```

## Near-Term Phase Guidance

- Phase 1 program-scope work should establish reusable concepts: technique tags, target types, allowed/disallowed techniques, rate caps, testing windows, audit events, authorization references, and versioned JSON schema.
- Do not implement a full plugin executor until scope/rule gates are stable.
- Ask implementation agents to avoid growing `recon.sh` into a permanent monolith; prefer reusable helpers and separate schema files where possible.
