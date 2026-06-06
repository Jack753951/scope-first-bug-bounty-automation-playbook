> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified exploit-flow rerun wave 1 summary

Date: 2026-05-21 UTC
Target: http://<lab-ip>:3000/
Artifact: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/`

## Scope / health / recovery

- Scope: `config/scope.txt` includes `<lab-ip>/16`; target `<lab-ip>` is in scope.
- Pre-health: HTTP 200 on `/`.
- Post-health: HTTP 200 on `/`.
- Recovery: no destructive action or persistent marker write was performed, so snapshot restore was not needed.

## Promoted verified-lab-flow bundles

- `verified_lab_flow_sqli_auth_bypass_admin_users_read.md`
- `verified_lab_flow_unauth_admin_config_read.md`
- `verified_lab_flow_directory_listing_file_read.md`
- `verified_lab_flow_api_docs_metrics_exposure.md`

## Attempted-not-verified / blockers

See `modules/bundles/attempted_not_verified_flows_wave1.md` for rerun inventory and concrete blocker reasons.

Supplement: headers/CORS direct rerun evidence was added at `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/headers_cors_rerun/headers_cors_supplement.md` after the initial wave summary.

## Validation note

Validation commands run after documentation updates: `python -m py_compile` for changed Python (none changed), `bash -n` on generated patched runners, `HACKLAB=$(pwd) ./bin/hermes review`, and `git status --short`.
