> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# attempted_not_verified_flows_wave1

Status: attempted-not-verified / blocked-deferred records
Date: 2026-05-21 UTC
Target: http://<lab-ip>:3000/
Run artifact: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/`

## Previously implemented bundles rerun inventory

Feasible reruns in this wave:

- Directory listing / `/ftp/`: initial hardcoded `/home/kali` runner failed on Windows Git-Bash; patched local rerun partially executed; manual verification succeeded and was promoted to `verified_lab_flow_directory_listing_file_read`.
- Benign reflection/redirect: patched rerun completed; no open redirect candidate for fixed canaries; XSS execution could not be proven without browser execution.
- Access-control unauth route metadata: patched rerun completed; manual verification promoted `/rest/admin/application-configuration` to `verified_lab_flow_unauth_admin_config_read`.
- Crypto transport metadata: patched rerun completed as metadata/hardening only; not an exploit-flow success.
- Exceptional-condition metadata: patched rerun completed; `/rest/does-not-exist` and XSS marker search generated HTTP 500/SQL error evidence, but not a verified exploit impact beyond error disclosure/robustness.
- ffuf sensitive path discovery: initial Windows-host wave incorrectly saw `ffuf` as unavailable. Corrected Kali-side rerun succeeded via `<attacker-vm>`; see `handoff/kali_verified_flow_wave2_20260522.md` and `<artifact-output-dir>/kali_verified_flow_wave2_20260522T001525Z/tools/ffuf_bounded.json`. It confirmed API docs, metrics, `/ftp/`, readable `/ftp/legal.md`, readable `/ftp/acquisitions.md`, `/api/Users` 401 control, and SPA/root-fallback controls.
- nikto server misconfig: initial Windows-host wave incorrectly saw `nikto` as unavailable. Corrected Kali-side rerun succeeded; output is hardening metadata only (`ACAO: *`, `x-recruiting`, `robots.txt`, missing HSTS/CSP/Permissions-Policy/Referrer-Policy), not a verified exploit-flow.
- nmap fingerprint: initial Windows-host wave incorrectly saw `nmap` as unavailable. Corrected Kali-side rerun succeeded and confirmed port `3000/tcp open` with Juice Shop HTTP fingerprint; service fingerprinting only, not an exploit-flow success.
- Headers/CORS baseline: rerun supplement completed with direct `curl` header and inert-Origin checks under `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/headers_cors_rerun/headers_cors_supplement.md`; remains hardening metadata, not a verified exploit-flow success.
- SQLi acquisition triage/sqlmap: initial Windows-host wave saw `sqlmap` as unavailable, which was a route error. Corrected Kali-side sqlmap was available and invoked with a bounded request, but that invocation did not produce useful confirmation; manual Kali HTTP SQLi auth-bypass succeeded and remains the authoritative verified evidence.
- Service baseline targets: rerun completed; most service paths were generic root-fallback controls; one Traefik-style candidate remains candidate-only and unverified.
- API docs exposure: rerun and manual verification succeeded; promoted as part of `verified_lab_flow_api_docs_metrics_exposure`.
- Metrics exposure: rerun and manual verification succeeded; promoted as part of `verified_lab_flow_api_docs_metrics_exposure`.
- Source-map disclosure: rerun completed; source-map paths were generic root-fallback controls; no verified source-map disclosure.
- Auth surface: rerun completed as metadata only; no brute force or credential guessing attempted.
- Component metadata: rerun completed as candidate metadata only; no CVE/reachable vulnerable component claim.
- Integrity metadata: rerun completed as candidate metadata only; no tampering or integrity exploit attempted.
- API-docs/metrics manual verification: upgraded to verified lab flow with concrete docs/UI and Prometheus evidence.

## Three new verified-flow attempts beyond old bundles

1. SQLi authentication bypass and authenticated `/api/Users` data read: verified success; see `verified_lab_flow_sqli_auth_bypass_admin_users_read.md`.
2. JWT `alg:none`/tamper probe: attempted-not-verified. `/rest/user/whoami` returned HTTP 200 `{"user":{}}` for valid, tampered, and no-token cases, so this endpoint is not a valid JWT acceptance oracle. No verified JWT weakness claimed.
3. Coupon/business-logic probe: attempted-not-verified. `POST /rest/basket/1/coupon` with inert marker `VF1_LAB_MARKER_20260521` returned HTTP 401 `No Authorization header was found`; authenticated coupon abuse was not pursued in this wave.

Additional new attempt:

- XSS execution marker via `/rest/products/search?q=<img src=x onerror=alert('VF1')>`: attempted-not-verified. HTTP 500 SQL error occurred; without a browser/runtime execution signal, no XSS execution is claimed. This result is retained as exceptional-condition/SQL error evidence only.

## Cleanup / recovery

No destructive action, upload, marker write, or persistent data change was performed. Post-wave health remained HTTP 200.
