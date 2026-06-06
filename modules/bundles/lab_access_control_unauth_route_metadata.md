> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_access_control_unauth_route_metadata

Status: active bundle / local-lab bounded / candidate-only
Date: 2026-05-21
Adapter: `scripts/lab_modules/lab_access_control_unauth_route_metadata.py`
Shared helper: `scripts/lab_modules/single_vuln_module_common.py`
Test: `scripts/test_owasp_single_vuln_modules.py`
Generated runner: `setting/local/lab_access_control_unauth_route_metadata_run.sh`
Latest run: `<artifact-output-dir>/phase4b_single_vuln_three_20260521T081506Z/lab_access_control_unauth_route_metadata/`

## Scope

One vulnerability behavior/class per module:

- Primary: `A01:2021 Broken Access Control`
- Mapping: `A05:2017 Broken Access Control`
- 2025 migration-track mapping: Broken Access Control

This module checks fixed unauthenticated route metadata only. It does not use credentials, session replay, role matrices, brute force, crawler behavior, or broad scanning.

## OSS/tooling reconnaissance

Checked:

- OWASP ZAP
- Autorize
- AuthMatrix

Decision: `write-custom`

Reason: mature tools exist, but this wave intentionally avoids credentials/session replay/Burp workflows and broad scanning. Fixed unauthenticated route metadata is safer and more auditable for the local lab capability-building phase.

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
| `/rest/admin/application-configuration` | unauthenticated admin/application configuration metadata | possible manual-review candidate |
| `/api/Users` | auth-gate control for user API | non-finding/control |
| `/administration` | SPA fallback false-positive control | non-finding/control |

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
/rest/admin/application-configuration
status 200
signal unauthenticated_200_candidate
content-type application/json; charset=utf-8
```

Controls / non-findings:

```text
/api/Users -> 401 auth_gate_control
/administration -> 200 spa_fallback_control
```

## Missing evidence before finding language

- Confirm endpoint intended public/private status.
- Compare unauthenticated, low-privileged, and high-privileged responses if credentials are later explicitly authorized in the lab.
- Review redacted fields for sensitivity.
- Prepare a redacted evidence packet.
- Pass report-readiness gate.

## Artifacts

- `observations.jsonl`
- `possible_vulnerabilities.md`
- `health.txt`
- `summary.txt`
- `artifact_manifest.txt`

## Validation

```text
python scripts/test_owasp_single_vuln_modules.py
python -m py_compile scripts/lab_modules/single_vuln_module_common.py scripts/lab_modules/lab_access_control_unauth_route_metadata.py
bash -n setting/local/lab_access_control_unauth_route_metadata_run.sh
```
