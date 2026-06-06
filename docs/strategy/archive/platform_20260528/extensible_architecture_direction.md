> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Extensible Cybersecurity Lab Architecture Direction

Date: 2026-05-15
Owner: Hermes / Operator
Status: Architectural direction for future implementation

## Goal

This project should evolve into an update-friendly, systematic, and extensible authorized bug bounty / cybersecurity lab platform — not just a multi-agent handoff demo.

The long-term architecture should support:

- clear authorization and scope gates
- program-specific rules and testing windows
- modular vulnerability scripts / checks
- reproducible validation and audit logs
- triage-only scanner output until manually verified
- evidence/report workflows
- agent-assisted post-scan analysis: scripts produce structured evidence, Claude/Cowork reviews triage/impact/report quality, Codex fixes automation, and Hermes verifies scope/safety/handoff
- safe multi-agent implementation and independent review

## Architectural Principles

0. **Learn from mature OSS without inheriting unsafe defaults**
   - Before adding new contracts, schemas, runner boundaries, result/report workflows, or tool integrations, run the design-only OSS Recon Gate in `docs/policy/oss_recon_gate.md`.
   - Prefer adopting durable concepts such as versioned metadata, severity/confidence separation, provenance, lifecycle states, plugin manifests, and structured outputs.
   - Do not copy target-touching execution defaults, unscoped template execution, or scanner-confirmed vulnerability semantics.

1. **Core safety first**
   - `safe_target` and program scope/rule validation remain central.
   - No module may bypass global scope, program scope, technique gates, or dry-run/live-mode checks.

2. **Modular checks, not monolithic scripts**
   - Vulnerability-specific logic should eventually live in modules/plugins rather than growing `recon.sh` forever.
   - Modules declare metadata: name, category, required technique tags, supported target types, risk level, external tools, and dry-run behavior.

3. **Policy/data separated from execution**
   - Program scope/rules live under `programs/<slug>/scope.json`.
   - Module metadata lives beside modules.
   - Runtime engine reads policy and metadata, then decides what is allowed.

4. **Default-deny plugin loading**
   - Unknown module schema, unsupported technique, missing dry-run implementation, or disallowed program rule means the module does not run.
   - Modules must be opt-in by allowlist/profile, not auto-run just because a file exists.

5. **Composable pipelines**
   - Recon, vulnerability checks, triage, verification, and reporting should be separable stages.
   - Each stage consumes structured input and emits structured output.

6. **Update-friendly contracts**
   - Use versioned schemas for program scope, module manifests, findings, and reports.
   - Avoid hidden behavior encoded only in shell conditionals.
   - Prefer clear JSON/Markdown artifacts and stable CLI contracts.

7. **Evidence and auditability**
   - Every allow/deny decision should produce an audit reason.
   - Findings remain triage candidates until manually verified.
   - Reports should distinguish automated observations from confirmed vulnerabilities.

8. **Agent workflow is part of architecture**
   - Codex implements minimal patches.
   - Claude/Cowork independently reviews non-trivial or high-impact changes.
   - Hermes verifies and records handoff state before moving phases.

## Proposed Future Module Layout

Longer-term target structure:

```text
scripts/
  core/
    scope.py
    policy.py
    runner.py
    evidence.py
    finding.py
    report.py

modules/
  _schema/
    module.schema.json
    finding.schema.json
    evidence.schema.json
  checks/
    web/
      headers/
        module.yaml
        check.py
        README.md
        tests/
      cors/
        module.yaml
        check.py
        README.md
        tests/
      jwt/
        module.yaml
        check.py
        README.md
        tests/
      open_redirect/
        module.yaml
        check.py
        README.md
        tests/
      xss_reflection/
        module.yaml
        check.py
        README.md
        tests/
  profiles/
    audit-baseline.yaml
    web-passive.yaml
    lab-active.yaml
```

Detailed module-system notes are tracked in `handoff/module_system_architecture_notes.md`.

Example `module.json` concept:

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
  "forbidden_if": ["automation_permitted=false"],
  "outputs": "finding.schema.json"
}
```

## Near-Term Impact On Phase 1

Phase 1 should avoid overfitting `scope.json` only to today's `recon.sh`.
It should establish concepts that future modules can reuse:

- technique tags
- target types
- allowed/disallowed techniques
- rate caps
- testing windows
- audit events
- program authorization references
- versioned JSON schema

## Near-Term Impact On Codex Tasks

When Codex implements Phase 1, ask it to keep changes modular:

1. Prefer standalone validation/helper functions over inline ad-hoc logic.
2. Keep schema files separate from shell execution logic.
3. Avoid making `recon.sh` the permanent home for every future vulnerability check.
4. Put reusable policy validation in clearly named functions/files where possible.
5. Add tests/dry-run evidence that can be reused when module support starts.

## Non-Goals For Immediate Phase 1

Do not implement full plugin execution yet unless explicitly requested.
Phase 1 should only prepare the foundation:

- program scope schema
- loader/default-deny validation
- integration gates
- dry-run tests
- documentation

The vulnerability module/plugin framework should be a later phase after Phase 1 scope/rule gates are stable.
