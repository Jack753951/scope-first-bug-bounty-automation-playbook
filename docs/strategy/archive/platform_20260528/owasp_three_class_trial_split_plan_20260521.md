> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# OWASP three-class pilot split plan

Status: planned / corrective action
Date: 2026-05-21
Reason: operator clarified that the desired final library shape is one vulnerability behavior/class per module.

## Correction

`modules/bundles/owasp_three_class_trial.md` is retained as a pilot/stress-test artifact only. It should not become the final reusable module shape.

Going forward:

- one vulnerability behavior/class = one module/bundle;
- a module may map equivalent categories across OWASP 2017/2021/2025 only when the tested capability is the same behavior;
- shared Python helper code is allowed;
- runnable entrypoint, bundle documentation, tracker state, importer, and candidate-review bridge should remain per vulnerability behavior.

## Split targets

### 1. Access-control metadata module

Proposed bundle:

`modules/bundles/lab_access_control_unauth_route_metadata.md`

Primary mapping:

- 2017 A05 Broken Access Control
- 2021 A01 Broken Access Control
- 2025 migration-track Broken Access Control

Candidate source from pilot:

- `/rest/admin/application-configuration` -> 200 JSON -> `unauthenticated_200_candidate`
- `/api/Users` -> 401 -> auth-gate control
- `/administration` -> SPA fallback control, not finding

Next work:

- extract access-control-only adapter or add class filter to shared runner;
- add access-control-only tests;
- generate access-control-only runnable;
- rerun against lab;
- create importer for access-control candidate seeds only.

### 2. Crypto/transport metadata module

Proposed bundle:

`modules/bundles/lab_crypto_transport_metadata.md`

Primary mapping:

- 2017 A03 Sensitive Data Exposure
- 2021 A02 Cryptographic Failures
- 2025 migration-track Cryptographic Failures

Candidate source from pilot:

- `/`, `/rest/user/whoami`, `/api/SecurityQuestions` -> `crypto_transport_cookie_metadata`

Next work:

- perform fresh OSS/tooling recon focused on testssl.sh/SSLyze/HTTP Observatory alternatives;
- decide wrap/adapt/write-custom for plain HTTP and future HTTPS labs;
- keep metadata-only until TLS wrapper exists.

### 3. Exceptional-condition metadata module

Proposed bundle:

`modules/bundles/lab_exceptional_condition_metadata.md`

Primary mapping:

- 2025 migration-track A10 Mishandling of Exceptional Conditions
- related context: 2021 Security Misconfiguration / Logging / Insecure Design depending on final verified 2025 mapping

Candidate source from pilot:

- `/rest/does-not-exist` -> 500 HTML title `Error: Unexpected path: /rest/does-not-exist` -> `server_error_candidate`

Next work:

- extract exceptional-condition-only adapter;
- add tests for fixed benign malformed paths, no fuzzing by default;
- if destructive error-handling tests are later needed, use disposable lab snapshot/recovery gate first.

## Keep from pilot

Useful lessons to retain:

- generated runner must be lab-executed, not only syntax-tested;
- `curl -L=false` was invalid and now has a regression test;
- status-code-only logic causes false positives;
- SPA fallback controls must be explicit;
- importer should convert only selected signals into `needs_manual_review`, not all 200s or metadata observations.
