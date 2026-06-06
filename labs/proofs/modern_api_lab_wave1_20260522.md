> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API Lab Wave 1

Status: completed / new disposable target added and tested
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> local target `http://127.0.0.1:18080`
Target source: `labs/modern_vuln_api/modern_vuln_api.py`
Runner: `labs/modern_vuln_api/modern_api_wave1_test.sh`
Artifacts: `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/`

## Why this target was added

Juice Shop covered SQLi/auth bypass, exposed files, API docs/metrics, upload acceptance, and valuable candidates. It did not cleanly cover:

- own-object vs other-object IDOR proof;
- upload retrieval proof;
- isolated SSRF callback proof.

This disposable Python stdlib target was added instead of waiting on Docker, because Kali currently has no Docker/Podman/Compose installed.

## Environment precheck

```text
Kali route: <attacker-vm>
Docker/Podman/Compose: not present
Disk /: 52G free
Scope: 127.0.0.1 and localhost are present in config/scope.txt
```

## Results

### IDOR / object ownership

Bundle:

`modules/bundles/verified_lab_flow_modern_api_idor_object_ownership.md`

Evidence:

```text
alice GET /api/users/1 -> 200 marker=PROFILE_MARKER_ALICE
alice GET /api/users/2 -> 200 marker=PROFILE_MARKER_BOB
alice GET /api/invoices/1001 -> 200 marker=ALICE_PRIVATE_INVOICE_MARKER
alice GET /api/invoices/2001 -> 200 marker=BOB_PRIVATE_INVOICE_MARKER
```

### Upload retrieval

Bundle:

`modules/bundles/verified_lab_flow_modern_api_upload_retrieval.md`

Evidence:

```text
upload -> 201 upload_id=f9ca155bd3f0 retrieve=200 marker_found=yes
```

### SSRF isolated callback

Bundle:

`modules/bundles/verified_lab_flow_modern_api_ssrf_isolated_callback.md`

Evidence:

```text
fetch callback -> 200 callback_log=200 callback_count=1
```

## Health

```text
pre_health: 200
post_health: 200
```

## Runtime / cleanup

The target is currently disposable and can be stopped on Kali with:

```bash
~/hermes-labs/modern_vuln_api/stop_modern_vuln_api.sh 18080
```

## Next target additions

- XXE parser lab.
- Deserialization lab.
- XSS runtime lab with reliable browser proof.
- Optional Docker-backed crAPI/WebGoat/Vulhub once Docker/Compose is installed.
