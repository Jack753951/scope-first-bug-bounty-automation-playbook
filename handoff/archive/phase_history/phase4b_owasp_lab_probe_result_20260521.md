> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B OWASP Local-Lab Probe Result — 2026-05-21

Status: completed / local-lab only / candidate-only
Run id: `phase4b_owasp_lab_probe_20260521T051717Z`
Route/tool: Hermes on Windows control plane -> PowerShell SSH/SCP wrappers -> `<attacker-vm>` -> host-only `<victim-vm>` Juice Shop
Visible model/runtime: Hermes current session; no Claude Code/Codex worker usage artifact for this lab probe

## Authorization and scope

Authorized class: local lab / intentionally vulnerable app.

Target touched:

- `http://<lab-ip>:3000/`
- Victim: `<victim-vm>`, host-only network
- Attacker/tool runner: `<attacker-vm>`, host-only network

No public target, bug bounty program, client asset, callback/OAST endpoint, brute-force flow, credentialed flow, exploit chain, persistence, stealth, malware, proxy/pivot, or report-submission path was used.

## Run controls

- Fixed target only.
- Fixed request list only.
- Request cap configured: 40.
- Requests sent: 16.
- Timeout: 5 seconds per request.
- Redirect-follow disabled with `--max-redirs 0`.
- Evidence posture: JSONL observations, headers/body hashes, content length, titles, short redacted snippets only.
- Output semantics: observation-only / candidate-only; no confirmed finding promotion.

## Health

Source artifact: `<artifact-output-dir>/phase4b_owasp_lab_probe_20260521T051717Z/health.txt`

```text
pre_health=200
post_health=200
requests_sent=16
```

Health remained OK after the run.

## Local artifacts

Pulled to Windows:

- `<artifact-output-dir>/phase4b_owasp_lab_probe_20260521T051717Z/observations.jsonl`
- `<artifact-output-dir>/phase4b_owasp_lab_probe_20260521T051717Z/summary.txt`
- `<artifact-output-dir>/phase4b_owasp_lab_probe_20260521T051717Z/health.txt`

Remote Kali source:

- `/home/kali/codex-output/phase4b_owasp_lab_probe_20260521T051717Z/`

## Summary observations

Source artifact: `<artifact-output-dir>/phase4b_owasp_lab_probe_20260521T051717Z/summary.txt`

Observed fixed paths:

- `GET /` -> `200`, `text/html`, title `OWASP Juice Shop`
- `GET /robots.txt` -> `200`, `text/plain`, 28 bytes
- `GET /.well-known/security.txt` -> `200`, `text/plain`, 475 bytes
- `GET /ftp/` -> body/title indicated `listing directory /ftp/`, but the transfer hit the 5s timeout near completion; keep as candidate metadata, not a confirmed report finding by automation.
- `GET /api-docs/` -> `200`, `text/html`, title `Swagger UI`
- `GET /rest/products/search?q=phase4b_canary` -> `200`, `application/json`, 30 bytes
- `GET /search?q=phase4b_canary` -> `200`, `text/html`, title `OWASP Juice Shop`; likely SPA fallback / route behavior, not a reflected-XSS finding.
- `GET /redirect?to=https://phase4b-canary.invalid/` -> `406`, title `Error: Unrecognized target URL for redirect: https://phase4b-canary.invalid/`; no redirect `Location` header observed.

## Output-side review notes

- Several `HEAD` requests and one `/ftp/` GET produced `curl` timeout suffixes even though headers/status/body metadata were partially captured. Treat these as harness/HTTP-method behavior signals, not vulnerability findings.
- For future adapter quality, prefer GET-only metadata probes with byte range / max-time / max-filesize handling instead of relying on HEAD against Juice Shop/Express routes.
- `/search?q=phase4b_canary` returning the normal Juice Shop HTML reinforces the SPA fallback false-positive trap.
- `/redirect?to=https://phase4b-canary.invalid/` returning 406 is a useful negative control for open-redirect candidate handling.
- `/api-docs/` and `/ftp/` remain useful local-lab metadata candidates for report-flow rehearsal, but still require manual content-class/impact wording before any report-ready state.

## Wrapper hardening found during run

`scripts/kali-pull.ps1` initially failed because Windows OpenSSH read a BOM-broken user SSH config. Hermes patched `scripts/kali-pull.ps1` to mirror `scripts/kali-run.ps1` and pass a project-local empty SSH config via `-F`, then verified the wrapper pull succeeded.

## Decision

`LOCAL_LAB_PROBE_ACCEPTED_AS_CANDIDATE_ONLY_EVIDENCE`

The target was used meaningfully within the local-lab authorization boundary. The next safe step can be a stronger GET-only local-lab adapter/run-card that turns this into a reusable Phase 4B module invocation path, still with health checks, request caps, redaction, and candidate-only output.
