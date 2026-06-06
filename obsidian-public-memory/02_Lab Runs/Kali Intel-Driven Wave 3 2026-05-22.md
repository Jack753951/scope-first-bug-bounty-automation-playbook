> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Kali Intel-Driven Wave 3 2026-05-22

Status: completed against current Juice Shop target
Repo handoff: `<user-home>`
Artifact root: `<user-home>`

## User directive

Downloads/new local targets are allowed when useful. This wave first reused the current authorized Juice Shop target because it still produced useful bundles.

## Results

- `valuable_candidate_kev_path_traversal_file_read_variants.md`: verified exposed `/ftp` file reads; traversal variants were blocked or root fallback.
- `valuable_candidate_upload_retrieval_and_validation.md`: authenticated marker PDF/TXT uploads returned HTTP 204; retrieval/RCE/arbitrary write not proven.
- `valuable_candidate_browser_xss_runtime_probe.md`: Kali Chromium workflow retained; current evidence is candidate-only, not runtime proof.
- `valuable_candidate_auth_access_boundary_expansion.md`: SQLi-derived admin token plus unauth/auth endpoint differential for future IDOR testing.

## Health

Pre-health: 200
Post-health: 200

## New target candidates

- IDOR/API lab target
- Upload retrieval/execution lab target
- SSRF lab with isolated callback service
- XXE/deserialization lab with parser/serialized-object surfaces
