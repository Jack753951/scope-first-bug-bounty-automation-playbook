> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_integrity_metadata_triage

Status: draft-active bundle / local-learning-lab / candidate-only
Date: 2026-05-22
Adapter: `scripts/lab_modules/lab_integrity_metadata_triage.py`
Generated runner: `setting/local/lab_integrity_metadata_triage_run.sh`
Latest artifacts: `<artifact-output-dir>/phase4b_owasp_cve_continuation_20260521T232928Z/lab_integrity_metadata_triage/`

## Use when

Use this bundle when testing software/data integrity metadata, security policy discoverability, service-worker/client-cache clues, or security.txt/robots metadata.

## OWASP / CVE mapping

- OWASP A08:2021 Software and Data Integrity Failures.
- OWASP A05:2021 Security Misconfiguration.
- CVE: none claimed by default; policy/integrity gaps require manual impact analysis.

## Mature OSS/tooling recon

Decision: reference browser/security-header and supply-chain tools; start with fixed metadata probes.

- OWASP ZAP: passive header/integrity-policy review.
- Mozilla Observatory: reference scoring model only; do not submit internal/local lab targets to public SaaS.
- Retire.js: dependency integrity/CVE hints after artifact hygiene.
- SRI hash checkers: manual Subresource Integrity review.

## What it runs

Fixed GET-only probes:

```text
/.well-known/security.txt
/security.txt
/robots.txt
/manifest.json
/ngsw.json
/service-worker.js
/sw.js
/integrity.json
/.well-known/change-password
```

## Controls

- Metadata only; no client-cache poisoning, package tampering, update-channel manipulation, or destructive integrity tests.
- Missing metadata is a hardening clue, not a finding by itself.
- Root SPA fallback is a control.

## Missing evidence before finding language

- Manual verification of missing/weak integrity control in actual loaded resources or update flow.
- Clear exploitability/impact chain.
- Redacted evidence packet and report-readiness review.
