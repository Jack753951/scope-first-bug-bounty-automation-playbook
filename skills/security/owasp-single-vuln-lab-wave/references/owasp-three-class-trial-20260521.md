> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# OWASP three-class local-lab trial — 2026-05-21

Use this as a concrete example when applying `owasp-single-vuln-lab-wave` to multiple classes in a pilot batch while still preserving one-class semantics in the output.

## Classes covered

- `A01:2021 Broken Access Control` mapped to 2017/2025 access-control rows.
- `A02:2021 Cryptographic Failures` mapped to 2017 Sensitive Data Exposure and 2025 crypto rows.
- `A10:2025 Mishandling of Exceptional Conditions` migration-track error-handling row.

## OSS/tooling recon decisions

Before writing a new adapter, mature OSS/tooling was checked:

- Access control: OWASP ZAP, Autorize, AuthMatrix.
- Crypto metadata: testssl.sh, SSLyze, Mozilla HTTP Observatory.
- Exceptional conditions: OWASP ZAP, ffuf, nuclei templates.

Decision for this pilot: `write-custom`, because available tools were too broad, session/credential-heavy, TLS-specific, or not aligned with fixed-path candidate-only local-lab probing. Future waves should still repeat OSS recon; do not assume custom is always correct.

## Adapter and artifacts

- Adapter: `scripts/lab_modules/owasp_three_class_probe.py`
- Tests: `scripts/test_owasp_three_class_probe.py`
- Runner: `setting/local/owasp_three_class_probe_run.sh`
- Bundle: `modules/bundles/owasp_three_class_trial.md`
- Result note: `handoff/phase4b_owasp_three_class_trial_result_20260521.md`
- Latest artifacts: `<artifact-output-dir>/phase4b_owasp_three_class_20260521T073537Z/`

## Durable workflow lessons

1. Always test generated runnable scripts, not only the generator. A generated Kali runner initially used invalid `curl -L=false`; add tests to prevent invalid generated shell flags.
2. Keep false-positive controls explicit. A SPA route returning `200` (`/administration`) was first over-labeled as an unauthenticated access candidate; it was corrected to `spa_fallback_control`.
3. Status code alone is not enough for access-control signals. Use path semantics, title/content-type, auth-gate controls (`401`), and SPA fallback controls.
4. For crypto waves on plain HTTP lab targets, treat results as metadata-only unless a dedicated TLS wrapper (e.g. testssl/SSLyze) is added through a separate OSS/tooling decision.
5. For exceptional-condition waves, fixed benign malformed/unknown routes can produce useful `server_error_candidate` observations without fuzzing.
6. Keep output candidate-only: no raw body retention, no confirmed/report-ready status, and no automatic finding promotion.

## Candidate bridge guidance

A future importer/bridge should convert only reviewed high-signal observations into `needs_manual_review` seeds, e.g.:

- `unauthenticated_200_candidate`
- `server_error_candidate`

Keep these as context/non-findings:

- `spa_fallback_control`
- `crypto_transport_cookie_metadata`
- `401` auth-gate observations
- metadata-only body hashes/titles/content-types
