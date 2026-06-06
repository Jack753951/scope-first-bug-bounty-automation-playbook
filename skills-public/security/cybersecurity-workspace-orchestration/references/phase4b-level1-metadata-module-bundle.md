> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4B Level 1 Metadata Module Bundle

Use this reference when turning a bounded local-lab web reconnaissance rehearsal into reusable Level 1 module manifests or a future guarded lab adapter.

## Trigger

- The workspace is moving from Phase 4A lab calibration into Phase 4B modularization.
- A local/intentionally vulnerable web app such as OWASP Juice Shop is already authorized and reachable in an isolated/host-only lab.
- The goal is to productize safe metadata observations, not to run exploit payloads or promote findings.

## Safe Wave 1A shape

A first reusable metadata wave can include only bounded, low-risk observations:

1. Pre-health check against the base URL.
2. Header metadata collection.
3. CORS metadata probes against a small fixed endpoint list and a fixed origin list.
4. Known-path metadata checks such as:
   - `/robots.txt`
   - `/.well-known/security.txt`
   - `/ftp/`
   - `/api-docs/`
   - `/rest/products/search`
5. Tiny fixed-wordlist ffuf/gobuster comparison when explicitly lab-approved.
6. A local info-only nuclei template, if used, with no exploit payloads.
7. Post-health check.

Keep the first pass metadata-only:

- no SQLi/XSS/LFI/SSRF/RCE payload scans
- no brute force or credentialed testing
- no recursive crawling
- no `/ftp/` file downloads
- no callbacks/OAST
- no public or bug-bounty targets
- no confirmed finding promotion

## Output interpretation

Treat outputs as observations/candidates only.

- `/ftp/` returning `200` plus an actual directory-listing title/body class can be a strong metadata-exposure candidate, but still needs report-gate wording and verification.
- `/api-docs/` returning Swagger UI is an API documentation exposure candidate, not automatically a vulnerability.
- REST endpoints returning JSON are API metadata observations unless sensitive data, auth bypass, or impact is verified.
- `Access-Control-Allow-Origin: *` without `Access-Control-Allow-Credentials` is usually non-finding/hardening metadata, not a CORS vulnerability.
- Missing hardening headers such as CSP, HSTS, Referrer-Policy, Permissions-Policy, COOP, and COEP are hardening metadata unless the report flow explicitly supports low-severity config observations.

## SPA fallback traps

Single-page apps often return `200 text/html` with the same content length for non-existent routes. Do not treat these as exposed resources:

- `/administration` style routes may be SPA fallbacks rather than real admin panels.
- `/api` or `/rest` returning generic errors is not automatically a crash/DoS finding.
- gobuster/ffuf can be noisy unless status, length, title, and content-class filters are applied.

Future adapters should record route/content class, title, content type, length, stable hash prefix, and fallback-baseline comparison before escalating.

## Module manifest productization

When the rehearsal works, first create data-only Level 1 manifests under `modules/checks/level1/<module_id>/module.json`. For the first batch, useful class-level manifests are:

- `directory_listing_metadata`
- `robots_securitytxt_metadata`
- `api_docs_metadata`
- `dependency_manifest_metadata`
- `cors_metadata`

Required posture for these first manifests:

- `requires_network=false`
- `network_access=none`
- `target_touching=false`
- `emits_findings=false`
- `emits_evidence=false`
- `manual_verification_required=true`
- `scanner_output_only=true`

Validate each manifest with the repo semantic validator and run the project review wrapper. Do not add live executor wiring in the same slice.

## Future guarded adapter requirements

The next implementation slice may build a bounded local-lab adapter, but only with explicit gates:

- `--lab-approved` or equivalent explicit lab-mode gate
- local/private-lab target restriction
- fixed known-path and CORS origin lists
- request cap and timeouts
- pre/post health checks
- JSONL observation output
- metadata/redacted snippets only
- no file download, recursive crawl, exploit payload, callback, or finding promotion
- structured audit/run card artifacts

Keep any public/real bug-bounty use blocked until separate T4/T5 review, program scope/rules, rate limits, evidence redaction, and operator approval exist.
