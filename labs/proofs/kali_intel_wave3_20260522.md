> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Kali Intel-Driven Wave 3

Status: completed against current authorized Juice Shop lab; no new vulnerable target installed yet
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> victim `http://<lab-ip>:3000`
Artifact root: `<artifact-output-dir>/kali_intel_wave3_20260522T005554Z/`

## User directive applied

The operator authorized continuing testing and, when useful, downloading or modifying local vulnerable target environments. This wave first tested the existing Juice Shop target against the new external-intelligence queue. It did not install a new target yet because several useful verified/valuable bundles could still be extracted from the current target.

## Sources driving this wave

- CISA KEV / NVD path traversal and file-read patterns
- Exploit-DB/GitHub upload and XSS workflow patterns
- HTB/training-lab style access-control and browser-runtime verification patterns
- Existing OWASP/CVE tracker

## Health and route

```text
pre_health: 200
post_health: 200
Kali tools observed: ffuf, nikto, nmap, sqlmap, chromium
```

## Results retained

### 1. Path traversal / file-read variants

Bundle:

`modules/bundles/valuable_candidate_kev_path_traversal_file_read_variants.md`

Outcome:

- Verified selected `/ftp` exposed-file reads.
- Traversal variants to `package.json`, `server.js`, and `/etc/passwd` were blocked or SPA/root fallback.
- Kept as valuable because it records traversal false-positive controls and exposed-file proof.

### 2. Upload retrieval and validation

Bundle:

`modules/bundles/valuable_candidate_upload_retrieval_and_validation.md`

Outcome:

- `vf3_marker.pdf` upload: HTTP 204
- `vf3_marker.txt` upload: HTTP 204
- Common retrieval paths did not expose the marker.
- Kept as valuable-candidate / partial verified state-change, not RCE or arbitrary file write.

### 3. Browser-backed XSS runtime probe

Bundle:

`modules/bundles/valuable_candidate_browser_xss_runtime_probe.md`

Outcome:

- Kali Chromium ran three payload families.
- Current marker detection is candidate-only; not enough to prove JavaScript execution.
- Kept because it records the browser-backed workflow and the stricter proof requirement.

### 4. Auth/access boundary expansion

Bundle:

`modules/bundles/valuable_candidate_auth_access_boundary_expansion.md`

Outcome:

- SQLi-derived admin token reconfirmed.
- Differential endpoints recorded:
  - `/api/Users` unauth=401 auth=200
  - `/rest/basket/1` unauth=401 auth=200
  - `/api/BasketItems` unauth=401 auth=200
  - `/rest/admin/application-configuration` unauth=200 auth=200
- Kept as valuable because it identifies next IDOR/object-ownership workflow.

## New-target decision

Do not install a new target yet from this wave alone. Recommended next target additions if the operator wants broader modern coverage:

1. IDOR/API lab target for object-ownership proof.
2. Upload lab target where retrieval/execution/storage path can be verified safely.
3. SSRF lab target plus isolated callback service.
4. XXE/deserialization lab target with explicit parser/serialized-object surfaces.

## Boundaries

- No public target.
- No malware/webshell/persistence.
- No real credential theft.
- No external callback/OAST.
- No confirmed claim where runtime proof was missing.
