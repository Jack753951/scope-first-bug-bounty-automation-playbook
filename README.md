> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Bounty Lane

Scope-first, safety-gated bug bounty automation workspace for agentic recon, lab proofs, evidence workflows, and report readiness.

This repository is a broad public-clean export of an internal agent-assisted bug-bounty automation workspace.
It keeps the project structure, scripts, schemas, templates, policies, lab modules, tests, reusable Hermes skills, and sanitized notes where possible.

Export policy used for this edition:

- Source tracked files inspected: 1276
- Meaningful non-runtime tracked candidates: 1136
- Public text files exported after redaction: 1107
- Skipped mainly binary/raw evidence files: 29

Redacted or removed:

- personal host paths and usernames;
- exact target/program names and domains;
- account aliases and credential-like material;
- VM names and host-only lab IPs;
- exact advisory IDs tied to private run history;
- raw logs, scans, loot, screenshots, browser state, and local runtime caches.

Nothing here authorizes live testing. Fill placeholders such as `<program-slug>`, `<in-scope-host>`, `<lab-ip>`, and `<authorized-scope-file>` only inside your own authorized environment.

## Entry points

- `SAFETY.md`, `INDEX.md`, `HERMES_PROJECT_CONTEXT.md` — sanitized project contracts.
- `orchestration/` and `hermes/` files — agent loop/policy material where retained.
- `scripts/` — validators, offline pipelines, local-lab modules, tests.
- `schemas/`, `fixtures/`, `templates/` — machine-readable contracts and sample data.
- `modules/` — reusable bundle/check/profile structure, redacted.
- `docs/`, `public_exports/`, `notes/` — sanitized methodology and project notes.

## Verify before reusing

```bash
python scripts/public_safety_scan.py .
python -m compileall scripts
```
