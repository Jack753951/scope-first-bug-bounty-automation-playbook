> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Modern API Lab Wave 1 2026-05-22

Status: completed / new disposable target
Repo handoff: `<user-home>`
Target source: `<user-home>`
Artifacts: `<user-home>`

## Why added

Juice Shop did not cleanly prove IDOR object ownership, upload retrieval, or isolated SSRF callback. Kali also lacks Docker/Compose right now, so a small disposable Python stdlib target was faster and more controllable.

## Verified bundles

- `verified_lab_flow_modern_api_idor_object_ownership.md`
  - Alice reads Bob profile and invoice markers by changing object IDs.
- `verified_lab_flow_modern_api_upload_retrieval.md`
  - Alice uploads harmless marker, retrieves it by returned upload ID.
- `verified_lab_flow_modern_api_ssrf_isolated_callback.md`
  - `/fetch?url=http://127.0.0.1:18080/callback?...` produces callback_count=1.

## Health

Pre-health: 200
Post-health: 200

## Cleanup

Target is running on Kali port 18080 unless stopped:

`~/hermes-labs/modern_vuln_api/stop_modern_vuln_api.sh 18080`
