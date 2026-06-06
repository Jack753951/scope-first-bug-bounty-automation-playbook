> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4B OWASP CVE Continuation 2026-05-22

Status: local-lab continuation complete / candidate-only / needs_manual_review
Repo handoff: `<user-home>`
Artifacts: `<user-home>`
Target: `http://<lab-ip>:3000/` only

## What changed

Completed the delayed Phase 4B OWASP/CVE continuation as script/tool -> bundle -> module learning work.

New practical bundles:

- `lab_auth_surface_no_bruteforce` — A07 auth-surface metadata; explicitly no brute force/credential attempts.
- `lab_component_metadata_triage` — A06 vulnerable/outdated component metadata and Retire.js/npm/OSV follow-up clues; no CVE claim from versions alone.
- `lab_integrity_metadata_triage` — A08 security/integrity metadata; no tampering/destructive integrity tests.
- `lab_api_docs_metrics_manual_verification` — manual checklist for `/api-docs`, `/metrics`, and A09 logging/monitoring evidence questions.

## Candidate-only observations

- `/rest/admin/application-configuration`: auth-surface metadata candidate.
- `/rest/admin/application-version`: component/version metadata candidate; manual advisory/impact correlation required.
- `/.well-known/security.txt`, `/security.txt`, `/robots.txt`: security/integrity metadata candidates.
- `/api/Users`: 401 access-control observed.
- Package-manifest and service-worker/static paths were mostly root/SPA fallback controls.

## Controls preserved

No public targets, no credentials, no brute force, no callbacks/OAST, no exploit payloads, no recursion/crawling, no destructive action, no raw secret/loot retention, no confirmed/reportable finding promotion.

## Validation

Focused tests passed; generated runners passed `bash -n`; runners executed successfully; post-run health returned HTTP 200.
