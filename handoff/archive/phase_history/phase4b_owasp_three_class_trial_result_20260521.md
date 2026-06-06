> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B OWASP three-class bounded lab trial

Status: completed / local-lab bounded / candidate-only
Date: 2026-05-21
Run id: `phase4b_owasp_three_class_20260521T073537Z`
Bundle: `modules/bundles/owasp_three_class_trial.md`
Adapter: `scripts/lab_modules/owasp_three_class_probe.py`
Test: `scripts/test_owasp_three_class_probe.py`
Generated runner: `setting/local/owasp_three_class_probe_run.sh`
Artifacts: `<artifact-output-dir>/phase4b_owasp_three_class_20260521T073537Z/`

## Operator request

Try three OWASP vulnerability classes first to see if the single-vulnerability/module workflow has problems.

## Classes selected

1. `A01:2021 Broken Access Control`
   - Maps to 2017 Broken Access Control and 2025 Broken Access Control.
   - Lane: active bounded metadata.
2. `A02:2021 Cryptographic Failures`
   - Maps to 2017 Sensitive Data Exposure and 2025 Cryptographic Failures.
   - Lane: metadata only.
3. `A10:2025 Mishandling of Exceptional Conditions`
   - 2025 migration-track error-handling class.
   - Lane: benign malformed input metadata.

## OSS/tooling reconnaissance

Before writing the adapter, checked mature OSS/tooling:

| Class | Tools/projects checked | Decision | Reason |
|---|---|---|---|
| Broken Access Control | OWASP ZAP, Autorize, AuthMatrix | `write-custom` | Mature tools exist, but ZAP is broad/not installed and Autorize/AuthMatrix expect Burp/session/credential workflows. First wave only needs fixed unauthenticated route metadata. |
| Cryptographic Failures | testssl.sh, SSLyze, Mozilla HTTP Observatory | `write-custom` | Mature TLS/HTTP observability tools exist, but current Juice Shop lab is plain HTTP and tools are not installed in the host context. First wave records transport/cookie metadata only. |
| Exceptional Conditions | OWASP ZAP, ffuf, nuclei templates | `write-custom` | Broad fuzzing/scanning tools exist, but this wave requires only three fixed benign error-handling probes, no crawler/fuzzer behavior. |

Local tool probe also found `zap.sh`, `zaproxy`, `testssl.sh`, `sslyze`, `nuclei`, and `ffuf` not available in the host PATH for this run.

## TDD evidence

RED:

```text
python scripts/test_owasp_three_class_probe.py
```

Initial failure: `scripts/lab_modules/owasp_three_class_probe.py` missing.

GREEN/fix:

```text
python scripts/test_owasp_three_class_probe.py
```

Result: `3 tests OK`.

Regression during lab run:

- First generated runner used invalid `curl -L=false` and failed on Kali.
- Patched adapter to remove invalid curl option and create empty header/body temp files if curl fails.
- Added test assertion that generated runner does not contain `-L=false`.

Second improvement:

- Initial signal logic treated `/administration` 200 as `unauthenticated_200_candidate`.
- Patched adapter to label `/administration` as `spa_fallback_control` and `/rest/user/whoami` as `unauth_identity_metadata`.
- Added test assertions for both signals.

## Execution

Route/tool:

```text
Hermes local terminal -> ssh/scp -> scripts/kali-run.ps1 -> <attacker-vm> -> <victim-vm> Juice Shop
```

Target:

```text
http://<lab-ip>:3000/
```

Health:

```text
pre_health=200
post_health=200
requests_sent=10
```

## Observation summary

A01 Broken Access Control:

- `/rest/admin/application-configuration` -> 200 JSON, `unauthenticated_200_candidate`.
- `/api/Users` -> 401, auth gate observed.
- `/rest/user/whoami` -> 200 JSON, `unauth_identity_metadata`.
- `/administration` -> 200 HTML title `OWASP Juice Shop`, `spa_fallback_control`.

A02 Cryptographic Failures:

- `/`, `/rest/user/whoami`, `/api/SecurityQuestions` recorded HTTP/cookie/transport metadata only.
- No TLS scanner result because target is plain HTTP and TLS wrappers are deferred.

A10:2025 Mishandling of Exceptional Conditions:

- `/rest/products/search?q=%25` -> 200 JSON.
- `/rest/products/search?q=%F0%9F%92%A9` -> 200 JSON.
- `/rest/does-not-exist` -> 500 HTML title `Error: Unexpected path: /rest/does-not-exist`, `server_error_candidate`.

## Candidate-only conclusion

Potential manual-review seeds:

- `A01 /rest/admin/application-configuration` as unauthenticated config/API metadata candidate.
- `A10 /rest/does-not-exist` as exceptional-condition/error-handling metadata candidate.

Non-findings / controls:

- `/administration` is SPA fallback control, not access-control evidence.
- `/api/Users` showed 401 auth gate.
- Crypto wave is metadata-only and not a finding.

## Safety boundary

- Authorized host-only local lab only.
- No public targets.
- No credentials/brute force.
- No exploit chain.
- No crawler/scanner/fuzzer.
- No callback/OAST.
- No raw body retention; body hashes only.
- No destructive behavior in this trial.
- No finding/report promotion.

## Deferred next step

Add an offline importer/bridge for `owasp_three_class_observation/0.1` that converts only `unauthenticated_200_candidate` and `server_error_candidate` into `needs_manual_review` candidate seeds while keeping SPA fallback and metadata-only observations as context.
