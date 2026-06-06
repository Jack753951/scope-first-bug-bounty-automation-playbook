> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# CISA KEV OWASP CVE Lab Mapping 2026-05-22

Status: intelligence/backlog source added
Repo handoff: `<user-home>`

## What changed

CISA KEV is now an explicit source for selecting local lab vulnerability patterns, alongside OWASP and CVE/advisory research.

Fetched official source:

`https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`

Local artifacts:

- `<user-home>`
- `<user-home>`
- `<user-home>`

Catalog count at fetch time: 1601.

## Rule

Product-specific CVEs are not automatically applicable to Juice Shop or the local victim. Use them as pattern inspiration unless the target actually has the affected product/version/component.

## Lab-test buckets

- Injection / SQLi / command/template injection -> OWASP A03
- XSS -> browser-backed runtime proof
- Path traversal / file read -> `/ftp` and traversal/file exposure bundles
- File upload / file write -> marker upload, retrieval, extension/content-type validation
- Authentication / access control -> SQLi auth bypass, unauth/auth boundary reads/state changes
- Exposed config/info disclosure -> admin config, API docs, metrics
- SSRF -> blocked until isolated callback lab exists
- XXE -> blocked until XML parser/input surface exists
- Deserialization -> blocked until serialized-object input exists
- RCE -> only if matching vulnerable component or execution sink exists

## Execution routing

Windows Hermes remains intelligence/control plane. Any target-touching KEV-inspired validation must run from `<lab-vm>` and pull artifacts back.
