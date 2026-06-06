> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A.1 Content-Class Verification Result — 2026-05-21

Route/tool: Hermes local bounded verification script via Python stdlib `urllib`.
Model/runtime: main Hermes agent `gpt-5.5 / openai-codex`; no external model used for the HTTP verification itself.
Target: `http://<lab-ip>:3000`
Scope: local intentionally vulnerable OWASP Juice Shop host-only lab only.
Artifact root: `scans/phase4a_content_class_verification_20260521_104314/`

## Boundary

- Fixed GET-only candidate list: `/robots.txt`, `/.well-known/security.txt`, `/ftp/`, `/rest/products/search`, `/api-docs/`.
- Request cap: 7 including pre/post health.
- No recursion, no file downloads, no credentials, no exploit payloads, no callbacks/listeners, no brute force.
- Stored only metadata, hashes, derived classifications, filename previews, and short redacted snippets.

## Result

Verdict: `LAB_REPORT_DRAFT_READY_FOR_CAND_001_METADATA_EXPOSURE`, still `NOT_READY_FOR_REAL_BUG_BOUNTY_SUBMISSION`.

Health stayed stable:

- Pre-health: HTTP 200, root body SHA-256 `9893b61734b4a11bb9b81c6feb2c97d0cc6aaa59190f8ec885a6e86c25661cef`.
- Post-health: HTTP 200, same root body SHA-256.

CAND-001 `/ftp/` was verified as a real directory-listing candidate, not SPA fallback:

- Status: HTTP 200.
- Content-Type: `text/html; charset=utf-8`.
- Title: `listing directory /ftp/`.
- Body class: `directory_listing_candidate`.
- Listing names observed: 12.
- Sensitive-looking filename preview: `announcement_encrypted.md`, `coupons_2013.md.bak`, `encrypt.pyc`, `incident-support.kdbx`, `package-lock.json.bak`, `package.json.bak`, `suspicious_errors.yml`.

Supporting observations:

- `/robots.txt` returns `Disallow: /ftp`; this supports the discovery narrative but is not access control and is not a finding by itself.
- `/.well-known/security.txt` is expected public security/contact metadata; not a finding.
- `/rest/products/search` is a real JSON API endpoint, but no sensitive-data or auth-bypass claim is supported by this bounded check.
- `/api-docs/` returns `Swagger UI`; documentation route candidate only, no exposure claim without a separate bounded docs review.

## Lab-report rehearsal wording

Public directory listing at `/ftp/` exposes metadata and sensitive-looking filenames. `robots.txt` advertises the path. Current evidence supports a lab-only metadata exposure candidate. It does not prove real-world impact or file-content sensitivity because this run intentionally did not download or inspect listed file bodies.

Suggested remediation:

- Disable directory listing.
- Remove unintended backup/sensitive artifacts from the web root.
- Serve only allowlisted static assets.
- Do not rely on `robots.txt` as access control.

Suggested retest:

- `/ftp/` no longer lists directory contents.
- Sensitive/backup artifacts are unavailable to unauthenticated users.
- `robots.txt` no longer advertises hidden sensitive paths.

## Remaining gates

- Keep this as local-lab-only evidence.
- Do not submit as real bug bounty.
- If a future step needs file-body proof, require explicit operator approval for exactly one narrow, non-sensitive sample review; no recursion or loot collection.
