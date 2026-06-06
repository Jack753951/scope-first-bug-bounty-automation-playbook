> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B three single-vulnerability module run result

Status: completed / local-lab bounded / candidate-only
Date: 2026-05-21
Run id: `phase4b_single_vuln_three_20260521T081506Z`
Target: `http://<lab-ip>:3000/`
Attacker VM: `<attacker-vm>` / `<lab-ip>`
Victim VM: `<victim-vm>` / `<lab-ip>`

## Purpose

Continue Phase 4B capability-building by converting the earlier three-class pilot into three separate one-vulnerability modules. This is not real bug bounty activation and not finding confirmation. Output remains candidate-only / needs manual review.

## Modules completed

1. `lab_access_control_unauth_route_metadata`
   - Bundle: `modules/bundles/lab_access_control_unauth_route_metadata.md`
   - Adapter: `scripts/lab_modules/lab_access_control_unauth_route_metadata.py`
   - Runner: `setting/local/lab_access_control_unauth_route_metadata_run.sh`
   - Artifact: `<artifact-output-dir>/phase4b_single_vuln_three_20260521T081506Z/lab_access_control_unauth_route_metadata/`

2. `lab_crypto_transport_metadata`
   - Bundle: `modules/bundles/lab_crypto_transport_metadata.md`
   - Adapter: `scripts/lab_modules/lab_crypto_transport_metadata.py`
   - Runner: `setting/local/lab_crypto_transport_metadata_run.sh`
   - Artifact: `<artifact-output-dir>/phase4b_single_vuln_three_20260521T081506Z/lab_crypto_transport_metadata/`

3. `lab_exceptional_condition_metadata`
   - Bundle: `modules/bundles/lab_exceptional_condition_metadata.md`
   - Adapter: `scripts/lab_modules/lab_exceptional_condition_metadata.py`
   - Runner: `setting/local/lab_exceptional_condition_metadata_run.sh`
   - Artifact: `<artifact-output-dir>/phase4b_single_vuln_three_20260521T081506Z/lab_exceptional_condition_metadata/`

Shared helper:

- `scripts/lab_modules/single_vuln_module_common.py`

Focused test:

- `scripts/test_owasp_single_vuln_modules.py`

## OSS/tooling recon decisions

| Module | Tools checked | Decision | Reason |
|---|---|---|---|
| access-control metadata | OWASP ZAP, Autorize, AuthMatrix | write-custom | Avoid credentials/session replay/Burp workflow and broad scan for this fixed unauth route metadata wave. |
| crypto/transport metadata | testssl.sh, SSLyze, Mozilla HTTP Observatory | write-custom | Target is plain HTTP; first module captures bounded HTTP/cookie metadata and defers TLS wrappers. |
| exceptional-condition metadata | OWASP ZAP, ffuf, nuclei templates | write-custom | Broad scanners/fuzzers are overkill; this module uses only fixed benign routes. |

No new external scripts/tools were downloaded for this wave.

## Execution notes

The first Kali execution attempt exposed two operational issues that were corrected before the final run:

- Victim lab was temporarily unreachable; restored/started `<victim-vm>` from the existing VirtualBox snapshot and verified `HTTP/1.1 200 OK` from the attacker VM.
- MSYS path conversion rewrote `/home/kali/...` output paths into `C:/Program Files/Git/...`; final generator calls used `MSYS2_ARG_CONV_EXCL='*'` before copying runners to Kali.
- Generated Python heredoc initially rendered newline escapes incorrectly; shared helper now renders the bash script from a raw f-string.

Final run succeeded and artifacts were pulled back.

## Result summary

### Access-control metadata

Health:

```text
pre_health=200
post_health=200
requests_sent=3
```

Possible manual-review candidate:

```text
/rest/admin/application-configuration -> 200 application/json; signal unauthenticated_200_candidate
```

Controls:

```text
/api/Users -> 401 auth_gate_control
/administration -> 200 spa_fallback_control
```

### Crypto/transport metadata

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

Metadata controls:

```text
/ -> 200 crypto_transport_cookie_metadata
/rest/user/whoami -> 200 crypto_transport_cookie_metadata
/api/SecurityQuestions -> 200 crypto_metadata_context
```

### Exceptional-condition metadata

Health:

```text
pre_health=200
post_health=200
requests_sent=3
```

Possible manual-review candidate:

```text
/rest/does-not-exist -> 500; title `Error: Unexpected path: /rest/does-not-exist`; signal server_error_candidate
```

Controls:

```text
/rest/products/search?q=%25 -> 200 stable_error_handling_control
/rest/products/search?q=%F0%9F%92%A9 -> 200 stable_error_handling_control
```

## Safety boundary

- Local lab only.
- Fixed target and fixed path list.
- No public/bug-bounty target activation.
- No credentials, brute force, callbacks/OAST, crawler, broad scanner, destructive action, loot retention, or report submission.
- Bodies are hashed then deleted.
- Outputs are candidate-only and require manual verification before finding language.

## Validation commands

```text
python scripts/test_owasp_single_vuln_modules.py
python -m py_compile scripts/lab_modules/single_vuln_module_common.py scripts/lab_modules/lab_access_control_unauth_route_metadata.py scripts/lab_modules/lab_crypto_transport_metadata.py scripts/lab_modules/lab_exceptional_condition_metadata.py
bash -n setting/local/lab_access_control_unauth_route_metadata_run.sh
bash -n setting/local/lab_crypto_transport_metadata_run.sh
bash -n setting/local/lab_exceptional_condition_metadata_run.sh
HACKLAB=<private-workspace> USER=Owner ./bin/hermes review
```

## Next recommended step

Add the offline importer/bridge for these single-vulnerability observations so `possible_vulnerabilities.md` and `observations.jsonl` can feed a `needs_manual_review` candidate-review queue without promoting confirmed/reportable statuses.
