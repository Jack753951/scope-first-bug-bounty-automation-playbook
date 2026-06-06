> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_exceptional_condition_metadata

Status: active bundle / local-lab bounded / candidate-only
Date: 2026-05-21
Adapter: `scripts/lab_modules/lab_exceptional_condition_metadata.py`
Shared helper: `scripts/lab_modules/single_vuln_module_common.py`
Test: `scripts/test_owasp_single_vuln_modules.py`
Generated runner: `setting/local/lab_exceptional_condition_metadata_run.sh`
Latest run: `<artifact-output-dir>/phase4b_single_vuln_three_20260521T081506Z/lab_exceptional_condition_metadata/`

## Scope

One vulnerability behavior/class per module:

- Primary: `A10:2025 Mishandling of Exceptional Conditions`
- Related 2021 context: Security Misconfiguration / Logging and Monitoring / Insecure Design depending on final taxonomy treatment.

This module checks fixed benign malformed/unknown-route error-handling metadata. It does not fuzz, crawl, run nuclei/ffuf, or attempt destructive service disruption.

## OSS/tooling reconnaissance

Checked:

- OWASP ZAP
- ffuf
- nuclei templates

Decision: `write-custom`

Reason: broad scanners/fuzzers exist, but this module uses only fixed benign routes with no crawler/fuzzer behavior and no destructive payloads.

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
| `/rest/products/search?q=%25` | benign malformed percent query control | non-finding/control |
| `/rest/products/search?q=%F0%9F%92%A9` | benign unicode query control | non-finding/control |
| `/rest/does-not-exist` | unknown REST route error behavior | possible manual-review candidate |

## Latest lab result

Run id: `phase4b_single_vuln_three_20260521T081506Z`

Health:

```text
pre_health=200
post_health=200
requests_sent=3
```

Possible manual-review candidate:

```text
/rest/does-not-exist
status 500
title Error: Unexpected path: /rest/does-not-exist
signal server_error_candidate
```

Controls / non-findings:

```text
/rest/products/search?q=%25 -> 200 stable_error_handling_control
/rest/products/search?q=%F0%9F%92%A9 -> 200 stable_error_handling_control
```

## Missing evidence before finding language

- Stable reproduction.
- Sensitive stack/framework detail check.
- Impact analysis beyond cosmetic 500 response.
- Redacted evidence packet and report-readiness gate.

## Artifacts

- `observations.jsonl`
- `possible_vulnerabilities.md`
- `health.txt`
- `summary.txt`
- `artifact_manifest.txt`

## Validation

```text
python scripts/test_owasp_single_vuln_modules.py
python -m py_compile scripts/lab_modules/single_vuln_module_common.py scripts/lab_modules/lab_exceptional_condition_metadata.py
bash -n setting/local/lab_exceptional_condition_metadata_run.sh
```
