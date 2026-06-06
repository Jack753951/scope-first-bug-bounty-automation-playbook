> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B Three Exposure Bundle Run

Status: completed local-learning-lab run / candidate-only
Date: 2026-05-21
Target: `http://<lab-ip>:3000/`
Scope: `<lab-ip>/16` in `config/scope.txt`
Route/tool: Hermes TDD implementation + local runner execution
Runtime/model visibility: parent Hermes model visible in session metadata; no external coding worker usage artifact for this slice
Artifacts: `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/`

## Selected bundles

The operator asked for three more OWASP/CVE-usable scanner scripts and mature OSS tooling references, then to package them as bundles. I selected three low-impact OWASP/misconfiguration-style local-lab exposure checks rather than exploit/CVE PoCs:

1. `lab_api_docs_exposure_triage`
   - OWASP: A05:2021 Security Misconfiguration; API9:2023 Improper Inventory Management.
   - Adapter: `scripts/lab_modules/lab_api_docs_exposure_triage.py`.
   - Bundle: `modules/bundles/lab_api_docs_exposure_triage.md`.
2. `lab_metrics_exposure_triage`
   - OWASP: A05:2021 Security Misconfiguration; contextual A09 telemetry exposure.
   - Adapter: `scripts/lab_modules/lab_metrics_exposure_triage.py`.
   - Bundle: `modules/bundles/lab_metrics_exposure_triage.md`.
3. `lab_source_map_disclosure_triage`
   - OWASP: A05:2021 Security Misconfiguration; A06 client dependency clues if source maps support dependency/version triage.
   - Adapter: `scripts/lab_modules/lab_source_map_disclosure_triage.py`.
   - Bundle: `modules/bundles/lab_source_map_disclosure_triage.md`.

Shared helper:

- `scripts/lab_modules/web_exposure_common.py`.

Focused tests:

- `scripts/test_phase4b_three_exposure_bundles.py`.

## Mature OSS/tooling recon

Checked/referenced mature OSS projects via GitHub metadata/API and recorded them in plans/bundles:

- OWASP ZAP `zaproxy/zaproxy`, Apache-2.0, ~15k stars.
- nuclei `projectdiscovery/nuclei`, MIT, ~28k stars.
- ffuf `ffuf/ffuf`, MIT, ~16k stars.
- dirsearch `maurosoria/dirsearch`, license not identified by GitHub API result, ~14k stars.
- Prometheus/promtool `prometheus/prometheus`, Apache-2.0, ~64k stars.
- Retire.js `RetireJS/retire.js`, Apache-2.0, ~4k stars.
- SecretFinder `m4ll0k/SecretFinder`, GPL-3.0, ~2.4k stars.
- trufflehog `trufflesecurity/trufflehog`, AGPL-3.0, ~26k stars.
- LinkFinder `GerbenJavado/LinkFinder`, license to verify before vendoring.

Decision: wrap/reference mature tools, but start with fixed GET-only local-lab probes. Do not vendor or run broad templates yet.

## Runtime results

### API docs exposure

Artifacts: `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/lab_api_docs_exposure_triage/`

Candidate-only leads:

```text
/api-docs  status=200  keywords=['swagger', 'swagger-ui']
/api-docs/ status=200  keywords=['swagger', 'swagger-ui']
```

Controls:

- `/swagger`, `/swagger/`, `/swagger-ui`, `/swagger-ui/`, `/swagger.json`, `/openapi.json` were generic SPA/root fallback controls.
- `/api/swagger.json` returned 500 and remains a control/error-handling observation.

### Metrics exposure

Artifacts: `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/lab_metrics_exposure_triage/`

Candidate-only lead:

```text
/metrics status=200 content_type=text/plain; version=0.0.4; charset=utf-8 bytes=25971
keywords=['# help', '# type', 'process_', 'nodejs_', 'http_']
```

Controls:

- `/prometheus`, `/stats/prometheus`, `/actuator/prometheus`, and `/actuator/metrics` were generic SPA/root fallback controls.

### Source-map disclosure

Artifacts: `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/lab_source_map_disclosure_triage/`

Candidate-only leads:

```text
None from this bounded local-lab run.
```

Controls:

- Common and inferred `.js.map` paths returned HTTP 200 but matched the application-root body hash, so they were classified as generic SPA/root fallback controls.

## Safety boundary

- All outputs remain `candidate-only / needs_manual_review`.
- No credential attempts, brute force, callbacks, exploit PoCs, raw secret retention, report submission, or confirmed-finding promotion.
- Raw response bodies are not committed; artifacts record statuses, content types, hashes, and bounded details.
- Public targets fail closed in tests.

## Validation

```text
python -m unittest scripts.test_phase4b_three_exposure_bundles -v
# RED first failed because adapters did not exist; GREEN passed after implementation.
```

Additional final validation recorded separately in `handoff/latest_check.md` after `hermes review`.

## Follow-up candidates

- Manually review `/api-docs` and `/metrics` with redacted screenshots before any report language.
- Consider a future offline-only importer that normalizes API docs and metrics candidates into the candidate-review bridge after these bundles see more lab runs.
- For source-map/CVE work, only add Retire.js/trufflehog/SecretFinder after explicit redaction/loot-hygiene gates.
