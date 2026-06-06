> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4B OWASP Local-Lab Probe Result 2026-05-21

Status: completed / local-lab only / candidate-only
Repo truth: `<user-home>`

## What happened

Hermes used the established Windows -> Kali bridge to run a bounded local-lab probe from `<lab-vm>` to the host-only Juice Shop victim at `http://<lab-ip>:3000/`.

Run id: `phase4b_owasp_lab_probe_20260521T051717Z`

Artifacts:

- `kali-output/phase4b_owasp_lab_probe_20260521T051717Z/observations.jsonl`
- `kali-output/phase4b_owasp_lab_probe_20260521T051717Z/summary.txt`
- `kali-output/phase4b_owasp_lab_probe_20260521T051717Z/health.txt`

## Boundary

- local lab only
- fixed target only
- 16 requests
- pre-health 200 / post-health 200
- no public targets
- no brute force
- no callbacks/OAST
- no exploit chains
- no credentialed flows
- no report/finding promotion

## Useful observations

- `/robots.txt` and `/.well-known/security.txt` are safe metadata candidates.
- `/ftp/` remains a good local-lab report-flow candidate, but body transfer timeout means future adapter should use GET-only bounded byte/body controls.
- `/api-docs/` exposes Swagger UI in the lab and is useful for module/report rehearsal.
- `/search?q=phase4b_canary` returned normal Juice Shop HTML, reinforcing SPA fallback false-positive handling.
- `/redirect?to=https://phase4b-canary.invalid/` returned 406 with no redirect header, useful negative control for open-redirect candidate handling.

## Engineering lesson

`kali-pull.ps1` needed the same `-F empty_ssh_config` hardening as `kali-run.ps1` to avoid a BOM-broken Windows SSH config. This was patched and verified.

## Next

Create a reusable GET-only bounded local-lab adapter/run-card from this result so Phase 4B modules can be invoked repeatedly with health checks, request caps, redaction, and candidate-only output.
