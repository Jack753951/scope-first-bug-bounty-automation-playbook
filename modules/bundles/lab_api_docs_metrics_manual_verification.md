> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_api_docs_metrics_manual_verification

Status: mini-bundle / manual-verification checklist / candidate-only
Date: 2026-05-22
Latest evidence source: `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/`

## Purpose

This mini-bundle turns existing `/api-docs` and `/metrics` exposure observations into a manual verification checklist without adding crawler/fuzzer breadth or promoting findings.

## Inputs

- `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/lab_api_docs_exposure_triage/observations.jsonl`
- `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/lab_metrics_exposure_triage/observations.jsonl`
- Optional rerun artifacts from `phase4b_owasp_cve_continuation_20260521T232928Z/` when present.

## API docs manual checks

- Verify `/api-docs` and `/api-docs/` are reachable without authentication.
- Record only redacted screenshots/snippets showing Swagger/OpenAPI UI markers.
- Identify whether endpoint names, schemas, or example requests materially accelerate attack-surface discovery.
- Do not submit requests from the docs UI unless a separate run card authorizes it.
- Treat docs exposure as no/low/medium impact based on actual unauthenticated detail and chaining potential.

## Metrics manual checks

- Verify `/metrics` is reachable without authentication.
- Record only metric names/classes, not raw full metric dumps if they contain host/user/path/session-like values.
- Look for sensitive labels, internal hostnames, build versions, route names, queue names, error counters, or feature flags.
- Confirm whether metrics are intended for internal-only monitoring.
- Do not scrape repeatedly or stress the endpoint.

## Logging/monitoring evidence checklist

- Does the app expose monitoring data publicly inside the lab network?
- Does the data include security-relevant labels, errors, endpoints, versions, or infrastructure topology?
- Does the app log or alert on suspicious auth/API-docs/metrics access? If not observable from the lab, record as `unknown`, not a finding.
- What remediation is appropriate: authentication, network ACL, metric relabeling/redaction, or docs disablement in production?

## Output semantics

All outcomes remain `candidate-only / needs_manual_review`; no confirmed finding or reportable status without impact proof, redaction, and report-readiness review.
