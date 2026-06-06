> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_modern_api_upload_retrieval

Status: verified-impact / authorized local lab / disposable target
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> local disposable target `http://127.0.0.1:18080`
Target implementation: `labs/modern_vuln_api/modern_vuln_api.py`
Artifacts: `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/`
Sources mapped: OWASP A05/A08, CWE-434 unrestricted file upload pattern, Exploit-DB/GitHub upload workflow inspiration

## Why this target was added

Juice Shop accepted marker upload but did not expose a retrieval path. This disposable target provides a safe, explicit upload -> retrieve workflow to validate upload evidence handling without using webshells or execution payloads.

## Verified flow

1. Login as Alice and obtain a bearer token.
2. Upload a harmless text marker to `/upload`:

```text
POST /upload
Authorization: Bearer <alice lab token>
Content-Type: text/plain
X-Filename: vf_modern_marker.txt
body: MODERN_UPLOAD_MARKER_<timestamp>

-> HTTP 201
upload_id=f9ca155bd3f0
```

3. Retrieve by returned upload ID:

```text
GET /uploads/f9ca155bd3f0
-> HTTP 200
marker_found=yes
```

## Impact

Level 3 lab impact: authenticated upload and public retrieval of user-controlled file content. This is not RCE and not a webshell; it is upload storage/retrieval proof.

## Evidence

- `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/upload_response.json`
- `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/upload_retrieved.txt`
- `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/observations.jsonl`

## Boundaries

- No executable upload.
- No webshell.
- No persistence beyond disposable lab temp file.
- No public target.

## Cleanup / recovery

Stop target with:

```bash
~/hermes-labs/modern_vuln_api/stop_modern_vuln_api.sh 18080
```

The upload storage lives under the Kali temp directory and is disposable.
