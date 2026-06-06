> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B Wave 1A Result — OWASP Metadata Script Combination

Date: 2026-05-21
Run ID: `phase4b_wave1a_20260521T030959Z`
Route/tool: Hermes -> Windows PowerShell Kali bridge -> `<attacker-vm>` shell script bundle.
Target: `http://<lab-ip>:3000/`
Scope: local intentionally vulnerable OWASP Juice Shop host-only lab only.

## Runtime boundary

Executed only low-risk metadata/content-discovery checks:

- pre/post health via `curl -I /`
- header metadata observation
- bounded CORS header observation on `/` and `/rest/products/search`
- known-path metadata for `/robots.txt`, `/.well-known/security.txt`, `/ftp/`, `/api-docs/`, `/rest/products/search`
- tiny `ffuf` wordlist with 9 entries
- tiny `gobuster` wordlist with 9 entries
- custom local `nuclei` info template against `/`

Not executed:

- SQLi probes
- XSS payload scans
- LFI/file-read payloads
- SSRF/OAST/callbacks
- brute force / hydra
- masscan / metasploit
- recursive crawl/download
- `/ftp/` file downloads
- credentialed testing
- real bug bounty / public targets

## Artifacts

Remote Kali output:

```text
/home/kali/phase4b-owasp/phase4b_wave1a_20260521T030959Z
```

Pulled local output:

```text
<artifact-output-dir>/phase4b_wave1a_20260521T030959Z/
```

Important files:

```text
artifact_manifest.txt
pre_health.txt
post_health.txt
headers_observation.json
cors_observations.jsonl
known_path_metadata.jsonl
ffuf.json
gobuster.stderr
nuclei.jsonl
run_context.txt
```

## Health result

Pre-health:

```text
HTTP/1.1 200 OK
```

Post-health:

```text
HTTP/1.1 200 OK
```

Attacker route context:

```text
<lab-ip>/24 dev eth0 proto kernel scope link src <lab-ip> metric 100
```

Conclusion: Wave 1A did not break the lab target. Availability remained stable.

## Observations

### Header metadata

Observed root headers:

- `X-Content-Type-Options: nosniff` present.
- `X-Frame-Options: SAMEORIGIN` present.
- `Strict-Transport-Security` absent.
- `Content-Security-Policy` absent.
- `Referrer-Policy` absent.
- `Permissions-Policy` absent.
- `Cross-Origin-Opener-Policy` absent.
- `Cross-Origin-Embedder-Policy` absent.

Review: metadata/hardening observation only. Missing headers in a local lab are not automatically reportable vulnerabilities.

### CORS metadata

Checked paths:

- `/`
- `/rest/products/search`

Origins:

- `https://evil.example`
- `null`
- `http://<lab-ip>:3000`

Observed:

- `Access-Control-Allow-Origin: *`
- no `Access-Control-Allow-Credentials: true`
- no candidate issue flagged by the Wave 1A rule.

Review: CORS wildcard without credentials is not a confirmed vulnerability. Archive as metadata/non-finding.

### Known path metadata

| Path | Status | Content class | Candidate? |
|---|---:|---|---|
| `/robots.txt` | 200 | text/plain, 28 bytes | observation only |
| `/.well-known/security.txt` | 200 | text/plain, 475 bytes | expected public metadata |
| `/ftp/` | 200 | HTML title `listing directory /ftp/` | candidate already covered by Phase 4A report |
| `/api-docs/` | 200 | Swagger UI | candidate for documentation exposure triage, not finding yet |
| `/rest/products/search` | 200 | JSON API response | observation only |

Notes:

- `/ftp/` again appears as a real directory-listing response.
- `/api-docs/` is a possible future metadata candidate but requires separate review before report language.
- `/rest/products/search` is expected app API metadata unless later evidence shows sensitive data or auth bypass.

### ffuf tiny discovery

`ffuf` found the fixed wordlist paths and highlighted common false-positive traps:

- `/ftp` -> 200, real directory-listing candidate.
- `/assets` -> 301 to `/assets/`.
- `/rest` and `/api` -> 500 HTML responses; do not treat as confirmed crash/DoS.
- `/administration` -> 200 length equal to SPA root; likely SPA route/fallback, not proof of exposed admin panel.
- `/robots.txt` -> 200.
- `/security.txt` -> 200.
- `/api-docs` -> 301 to `/api-docs/`.
- `/.well-known/security.txt` -> 200.

Review: useful for route discovery, but must be paired with content-class verification before report claims.

### gobuster tiny discovery

`gobuster` stopped because the app returns root-like HTTP 200 for random non-existing URLs:

```text
the server returns a status code that matches the provided options for non existing urls ... => 200 (Length: 9903)
```

Review: this is valuable false-positive evidence. For Juice Shop/SPAs, gobuster must be configured with length/status exclusion or replaced with content-class-aware checks.

### nuclei custom info template

Custom local info template matched root HTTP 200 only.

Review: validates that a custom info-only nuclei template can run safely, but this specific template adds little beyond curl/header metadata. It is useful mostly as a future adapter test.

## Candidate decisions

| Candidate | Decision | Reason |
|---|---|---|
| `/ftp/` directory listing metadata | already accepted as lab-report rehearsal candidate | confirmed real directory-listing response, previous report exists |
| `/api-docs/` Swagger UI | hold for separate triage | documentation route present, but not necessarily vulnerability |
| Missing security headers | archive as hardening metadata | not enough for vulnerability claim |
| CORS wildcard | non-finding for now | no credentials allowed |
| `/administration` 200 | false-positive trap | likely SPA fallback/root length |
| `/rest`/`/api` 500 | do not promote | needs careful manual route review; no DoS/crash claim |

## Modularization outcome

This Wave 1A combination was effective enough to modularize into Level 1 metadata manifests. Created:

```text
modules/checks/level1/directory_listing_metadata/module.json
modules/checks/level1/robots_securitytxt_metadata/module.json
modules/checks/level1/api_docs_metadata/module.json
modules/checks/level1/dependency_manifest_metadata/module.json
modules/checks/level1/cors_metadata/module.json
```

Each is offline/dry-run manifest only for now:

- `requires_network=false`
- `target_touching=false`
- `emits_findings=false`
- `emits_evidence=false`
- `manual_verification_required=true`
- `scanner_output_only=true`

Runtime adapters remain a separate reviewed step.

## What to do next

Recommended next stage:

```text
Phase 4B.1B — turn Wave 1A into a reusable bounded local-lab adapter
```

Scope:

- create `scripts/lab_modules/wave1a_metadata.py`
- add `--lab-approved` gate
- reject non-local/non-scope targets
- fixed known-path list
- fixed CORS origins
- request cap
- pre/post health
- JSONL output
- no file downloads, no recursive crawl, no exploit payloads
- tests for unauthorized target rejection and output shape

This is a useful modularization step before moving to Wave 2 XSS/open-redirect candidates.

## Decision

`WAVE_1A_PASS_AND_MODULARIZE_LEVEL1_METADATA`

No confirmed real-world vulnerabilities. Outputs are lab observations/candidates only.
