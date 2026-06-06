> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# owasp_three_class_trial

Status: active trial bundle / local-lab bounded
Date: 2026-05-21
Adapter: `scripts/lab_modules/owasp_three_class_probe.py`
Test: `scripts/test_owasp_three_class_probe.py`
Latest run: `<artifact-output-dir>/phase4b_owasp_three_class_20260521T073537Z/`

## Use when

Use this bundle to test three low-risk OWASP classes in one bounded local-lab trial:

1. `A01:2021 Broken Access Control` / 2017+2025 access-control mapping
2. `A02:2021 Cryptographic Failures` / 2017 sensitive-data + 2025 crypto mapping
3. `A10:2025 Mishandling of Exceptional Conditions` migration-track error-handling class

This is a trial bundle, not a broad scanner. It is suitable only when the target is the authorized host-only lab target and the operator wants to quickly check whether the three-class workflow itself has problems.

## Do not use when

- Target is public, client, or real bug-bounty scope.
- Credentials, brute force, session replay, or account takeover are required.
- TLS scanner coverage is required; use a future testssl/SSLyze wrapper for that.
- Error-handling fuzzing/crawling is desired; this bundle only sends fixed benign requests.
- Findings would be auto-promoted to confirmed/reportable.

## OSS/tooling reconnaissance decision

Before writing this adapter, OSS/tooling recon checked:

- Broken Access Control: OWASP ZAP, Autorize, AuthMatrix.
- Cryptographic Failures: testssl.sh, SSLyze, Mozilla HTTP Observatory.
- Exceptional Conditions: OWASP ZAP, ffuf, nuclei templates.

Decision for all three in this first trial: `write-custom`.

Reason: mature tools exist, but either are not installed in the current host context, expect Burp/session/TLS/broad-scanning workflows, or are too broad for this candidate-only fixed-path lab wave. The custom adapter remains small, fixed-path, candidate-only, and import-friendly.

## Inputs

- `--target`: authorized local/private lab URL, default tested target `http://<lab-ip>:3000/`.
- `--lab-approved`: required before writing a runnable script.
- `--out-script`: generated bash runner path.
- `--output-dir`: remote artifact directory.
- `--request-cap`: default 16, tested with 10 target probes plus pre/post health.

## Scripts

```text
scripts/lab_modules/owasp_three_class_probe.py
setting/local/owasp_three_class_probe_run.sh
```

## Caps and boundaries

- Plan-only by default.
- Rejects public targets fail-closed.
- Fixed paths only.
- No crawler/scanner/fuzzer.
- No credentials or brute force.
- No callbacks/OAST.
- No raw body retention; bodies are hashed then deleted.
- Candidate-only JSONL observations.
- No confirmed/verified/reportable/accepted status.

## Latest lab result

Latest artifact directory:

```text
<artifact-output-dir>/phase4b_owasp_three_class_20260521T073537Z/
```

Health:

```text
pre_health=200
post_health=200
requests_sent=10
```

Signals observed:

- A01 Broken Access Control:
  - `/rest/admin/application-configuration` returned 200 JSON and is `unauthenticated_200_candidate`.
  - `/api/Users` returned 401 and is an auth-gate observation.
  - `/rest/user/whoami` returned 200 JSON and is `unauth_identity_metadata`.
  - `/administration` returned the SPA title and is `spa_fallback_control`, not an access-control finding.
- A02 Cryptographic Failures:
  - `/`, `/rest/user/whoami`, `/api/SecurityQuestions` recorded transport/cookie metadata only.
  - Current target is plain HTTP; TLS-tool wrapper is deferred.
- A10:2025 Mishandling of Exceptional Conditions:
  - benign search variants returned 200 JSON.
  - `/rest/does-not-exist` returned 500 with title `Error: Unexpected path: /rest/does-not-exist`, retained as `server_error_candidate`.

## Review notes

The first run showed a false-positive risk: SPA routes returning 200 must not be treated as unauthenticated access by status alone. The adapter was patched to label `/administration` as `spa_fallback_control` and `/rest/user/whoami` as `unauth_identity_metadata`.

## Importer/bridge status

Deferred for this first trial. Next useful step is a small offline importer that converts only:

- `unauthenticated_200_candidate`
- `server_error_candidate`

into `needs_manual_review` candidate seeds, while keeping `spa_fallback_control` and metadata-only observations as non-finding context.
