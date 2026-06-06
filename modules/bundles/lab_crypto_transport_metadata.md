> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_crypto_transport_metadata

Status: active bundle / local-lab bounded / candidate-only
Date: 2026-05-21
Adapter: `scripts/lab_modules/lab_crypto_transport_metadata.py`
Shared helper: `scripts/lab_modules/single_vuln_module_common.py`
Test: `scripts/test_owasp_single_vuln_modules.py`
Generated runner: `setting/local/lab_crypto_transport_metadata_run.sh`
Latest run: `<artifact-output-dir>/phase4b_single_vuln_three_20260521T081506Z/lab_crypto_transport_metadata/`

## Scope

One vulnerability behavior/class per module:

- Primary: `A02:2021 Cryptographic Failures`
- Mapping: `A03:2017 Sensitive Data Exposure`
- 2025 migration-track mapping: Cryptographic Failures

This module captures bounded HTTP/cookie/transport metadata only. It does not run TLS scanners in the current local-lab wave because the target is plain HTTP. A later wrapper may adopt/wrap `testssl.sh`, `SSLyze`, or Observatory-style checks if a TLS-enabled authorized target exists.

## OSS/tooling reconnaissance

Checked:

- testssl.sh
- SSLyze
- Mozilla HTTP Observatory

Decision: `write-custom`

Reason: mature TLS/HTTP observability tools exist, but the current lab target is plain HTTP. This first module captures bounded transport/cookie metadata and defers TLS wrapper work.

## Safety boundaries

- Local/private lab target only.
- Plan-only by default; generated runnable requires `--lab-approved`.
- Fixed path list.
- Request cap enforced by generated runner.
- Pre/post health recorded.
- Bodies are hashed then deleted; no raw body retention.
- Output semantics are `candidate-only`.
- No confirmed/reportable/submission language.

## Probes

| Path | Purpose | Expected role |
|---|---|---|
| `/` | transport and cookie metadata baseline | metadata/control |
| `/rest/user/whoami` | identity endpoint cookie/header metadata | metadata/control |
| `/api/SecurityQuestions` | security-question metadata context | metadata/control |

## Latest lab result

Run id: `phase4b_single_vuln_three_20260521T081506Z`

Health:

```text
pre_health=200
post_health=200
requests_sent=3
```

Possible manual-review candidates:

```text
None from this bounded run.
```

Controls / metadata observations:

```text
/ -> 200 crypto_transport_cookie_metadata
/rest/user/whoami -> 200 crypto_transport_cookie_metadata
/api/SecurityQuestions -> 200 crypto_metadata_context
```

## Missing evidence before finding language

- HTTPS/TLS scanner result if a TLS-enabled authorized target exists.
- Sensitive data proof, if any, with redaction.
- Cookie flag comparison with authenticated flow if credentials are later explicitly authorized in the lab.
- Manual impact analysis and report-readiness gate.

## Artifacts

- `observations.jsonl`
- `possible_vulnerabilities.md`
- `health.txt`
- `summary.txt`
- `artifact_manifest.txt`

## Validation

```text
python scripts/test_owasp_single_vuln_modules.py
python -m py_compile scripts/lab_modules/single_vuln_module_common.py scripts/lab_modules/lab_crypto_transport_metadata.py
bash -n setting/local/lab_crypto_transport_metadata_run.sh
```
