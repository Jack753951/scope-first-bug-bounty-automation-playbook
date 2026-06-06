> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Post-Scan Agent Review

## Purpose

Scripts generate structured candidate findings. Agents and humans review whether they are real, impactful, in-scope, and reportable.

## Review dimensions

- Scope/run integrity
- Evidence quality
- False positive likelihood
- Manual verification steps
- Business/security impact
- Remediation clarity
- Retest plan
- Report readiness

## Routing

- Hermes verifies scope/audit integrity
- Claude/Cowork reviews impact, report quality, and false positives
- Codex fixes automation defects
