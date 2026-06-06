> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# source_reviewed_wrapper_wave1_patterns

Status: valuable-candidate / source-reviewed wrapper workflow / local lab verified subflows
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> Kali `<attacker-vm>` -> local disposable target `http://127.0.0.1:18080`
Artifacts: `<artifact-output-dir>/source_reviewed_wrapper_wave1_20260522T024602Z/`
Runner: `labs/modern_vuln_api/source_reviewed_wrapper_wave1.sh`

## Purpose

Convert acquired external sources into safe reusable lab wrappers without blindly executing raw exploit scripts.

## Sources used as patterns

- Exploit-DB acquisition metadata for path traversal, arbitrary upload, and auth/access classes.
- PayloadsAllTheThings XXE/XSS payload styles, adapted to safe local markers.
- Arjun-style parameter discovery, bounded to known local endpoints and a short candidate list.
- Dalfox/XSStrike-style browser runtime marker proof.
- jwt_tool-style token sanity concept retained for future JWT target.

## Evidence

Summary:

```text
pre_health: 200
xss runtime marker=yes
xxe marker=yes status=200
upload status=201 retrieve=200 marker=yes
post_health: 200
```

Observed access-control object tampering:

```text
/api/users/1 -> PROFILE_MARKER_ALICE
/api/users/2 -> PROFILE_MARKER_BOB
/api/invoices/1001 -> PRIVATE_INVOICE_MARKER
/api/invoices/2001 -> PRIVATE_INVOICE_MARKER
```

Parameter discovery observed `/fetch?url=...` as behavior-changing:

```text
/fetch base_status=400
/fetch?url=HERMES_PARAM_MARKER status=502
```

## Classification

This bundle is valuable-candidate as a reusable source-to-wrapper methodology. Individual subflows are already covered by verified bundles:

- `verified_lab_flow_modern_api_xss_runtime_proof.md`
- `verified_lab_flow_modern_api_xxe_safe_marker.md`
- `verified_lab_flow_modern_api_upload_retrieval.md`
- `verified_lab_flow_modern_api_idor_object_ownership.md`

## Boundaries

- No raw third-party exploit execution.
- No public targets.
- No external callbacks.
- No credential theft.
- No shell/reverse shell/persistence.
