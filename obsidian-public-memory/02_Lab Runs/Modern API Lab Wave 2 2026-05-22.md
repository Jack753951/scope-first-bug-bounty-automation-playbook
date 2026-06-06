> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Modern API Lab Wave 2 2026-05-22

Status: completed / disposable target extended
Repo handoff: `<user-home>`
Artifacts: `<user-home>`

## Verified bundles

- `verified_lab_flow_modern_api_xss_runtime_proof.md`
  - Chromium runtime DOM proof: `<body data-xss="XSS_RUNTIME_MARKER">`.
- `verified_lab_flow_modern_api_xxe_safe_marker.md`
  - Bounded XXE-style safe marker proof: `XXE_SAFE_MARKER_HERMES_LOCAL_LAB`.
- `verified_lab_flow_modern_api_deserialization_bounded_gadget.md`
  - Bounded unsafe pickle gadget invokes in-process marker recorder: `DESER_SAFE_MARKER_HERMES_LOCAL_LAB`.

## Boundaries

No public target, no credential theft, no external callback, no real secret file read, no shell/reverse shell/persistence.

## Health

Pre-health: 200
Post-health: 200

## Cleanup

Target is currently running on Kali port 18080 unless stopped:

`~/hermes-labs/modern_vuln_api/stop_modern_vuln_api.sh 18080`
