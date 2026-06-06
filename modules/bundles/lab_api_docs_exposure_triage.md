> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_api_docs_exposure_triage

Status: draft-active bundle / local-learning-lab / candidate-only
Date: 2026-05-21
Adapter: `scripts/lab_modules/lab_api_docs_exposure_triage.py`
Generated runner: `setting/local/lab_api_docs_exposure_triage_run.sh`
Latest artifacts: `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/lab_api_docs_exposure_triage/`

## Use when

Use this bundle when preview/recon suggests Swagger/OpenAPI/API documentation exposure or when a lab target needs a bounded API docs baseline.

## OWASP / CVE mapping

- OWASP A05:2021 Security Misconfiguration
- OWASP API9:2023 Improper Inventory Management
- 2025 migration track: misconfiguration / exposed documentation leads
- CVE: none claimed by default; API docs exposure is context/impact dependent.

## Mature OSS/tooling recon

Decision: wrap/reference mature tools, but start with fixed low-impact paths.

- OWASP ZAP (`zaproxy/zaproxy`, Apache-2.0): OpenAPI import and passive API review.
- nuclei (`projectdiscovery/nuclei`, MIT): allowlisted exposure templates after scope gate.
- ffuf (`ffuf/ffuf`, MIT): bounded API docs path discovery.
- dirsearch (`maurosoria/dirsearch`, license not identified by GitHub API result): reference-only alternative path discovery.

## What it runs

Fixed GET-only probes:

```text
/api-docs
/api-docs/
/swagger
/swagger/
/swagger-ui
/swagger-ui/
/swagger.json
/openapi.json
/api/swagger.json
```

## Inputs

```bash
MSYS2_ARG_CONV_EXCL='*' python scripts/lab_modules/lab_api_docs_exposure_triage.py \
  --target http://<lab-ip>:3000/ \
  --lab-approved \
  --out-script setting/local/lab_api_docs_exposure_triage_run.sh \
  --output-dir /tmp/lab_api_docs_exposure_triage
bash setting/local/lab_api_docs_exposure_triage_run.sh
```

## Outputs

```text
observations.jsonl
http_probe_results.jsonl
possible_vulnerabilities.md
summary.txt
tool_stdout.txt
tool_stderr.txt
artifact_manifest.txt
```

## Candidate / control logic

Candidate:

- HTTP 200/redirect with API docs keywords such as `swagger`, `openapi`, `swagger-ui`, `paths`, or `components`.
- Body hash differs from `/` root, to avoid SPA/router fallback false positives.

Controls:

- 404/401/403/timeout.
- HTTP 200 with same body hash as `/` root.
- Status-code-only signal without API-doc keywords.

## Latest local-lab result

Candidate-only leads:

```text
/api-docs  status=200  keywords=['swagger', 'swagger-ui']
/api-docs/ status=200  keywords=['swagger', 'swagger-ui']
```

Controls:

- `/swagger`, `/swagger/`, `/swagger-ui`, `/swagger-ui/`, `/swagger.json`, `/openapi.json` were generic SPA/root fallback controls.
- `/api/swagger.json` returned 500 and remains a control/error-handling observation.

## Missing evidence before finding language

- Manually verify the docs are reachable without auth and contain useful endpoint/schema details.
- Redact screenshots/output.
- Explain impact: inventory leakage, unauthenticated schema discovery, attack-surface acceleration, or no meaningful impact.
- Do not call this confirmed/reportable without report-readiness review.
