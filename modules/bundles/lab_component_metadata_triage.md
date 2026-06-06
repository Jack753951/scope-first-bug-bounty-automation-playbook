> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_component_metadata_triage

Status: draft-active bundle / local-learning-lab / candidate-only
Date: 2026-05-22
Adapter: `scripts/lab_modules/lab_component_metadata_triage.py`
Generated runner: `setting/local/lab_component_metadata_triage_run.sh`
Latest artifacts: `<artifact-output-dir>/phase4b_owasp_cve_continuation_20260521T232928Z/lab_component_metadata_triage/`

## Use when

Use this bundle when preview/recon suggests exposed package manifests, client dependency clues, static build metadata, or an app/version endpoint.

## OWASP / CVE mapping

- OWASP A06:2021 Vulnerable and Outdated Components.
- OWASP A08:2021 Software and Data Integrity Failures, limited to dependency provenance clues.
- CVE: version strings are never enough; CVE mapping remains `candidate-only` until package identity, reachable vulnerable code path, advisory source, and impact are manually verified.

## Mature OSS/tooling recon

Decision: wrap/reference mature dependency tools after artifact hygiene.

- Retire.js: client-side dependency/CVE hints.
- npm audit: local package metadata review when a manifest is legitimately available.
- OWASP Dependency-Check: offline CVE correlation.
- osv-scanner: offline advisory correlation.

## What it runs

Fixed GET-only probes:

```text
/package.json
/package-lock.json
/npm-shrinkwrap.json
/yarn.lock
/bower.json
/composer.json
/assets/package.json
/rest/admin/application-version
```

## Controls

- No recursive asset crawling or package download.
- No raw manifest promotion to report evidence without redaction/manual review.
- No CVE claim from a version string alone.

## Missing evidence before finding language

- Confirm exact component name/version from an approved source.
- Correlate advisory/CVE from primary source.
- Confirm reachability/impact in this application.
- Redact evidence and pass report-readiness review.
