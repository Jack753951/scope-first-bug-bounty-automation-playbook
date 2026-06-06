> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# LAB ONLY — Phase 4A.1 `/ftp/` Directory Listing Report Rehearsal

Date: 2026-05-21
Target: `http://<lab-ip>:3000`
Environment: local host-only OWASP Juice Shop victim lab
Report status: LAB ONLY / TRAINING / NOT FOR REAL BUG BOUNTY SUBMISSION
Finding status: candidate / lab-report-draft-ready / not confirmed real-world finding
Evidence root: `scans/phase4a_content_class_verification_20260521_104314/`
Primary source artifacts:

- `scans/phase4a_content_class_verification_20260521_104314/content_class_verification.json`
- `scans/phase4a_content_class_verification_20260521_104314/lab_report_rehearsal.md`
- `handoff/phase4a_1_content_class_verification_result_20260521.md`

> LAB-ONLY WARNING: This report is a controlled workflow rehearsal against an intentionally vulnerable local Juice Shop instance on a host-only network. It is not a real bug bounty submission, does not establish real-world impact, and must not be reused against public/client targets without explicit authorization, program rules, and fresh validation.

## Executive Summary

A bounded Phase 4A.1 content-class verification run confirmed that the local Juice Shop lab exposes a real directory listing at `/ftp/`. The route is not a single-page-app fallback: it returns HTTP 200, `text/html`, and page title `listing directory /ftp/`. The listing exposes filename metadata including backup-like, encrypted-looking, dependency-manifest-like, and incident-support-looking names.

This is suitable as a lab-only report rehearsal for a metadata exposure candidate. It is not ready for real bug bounty submission because the target is an intentionally vulnerable local lab and the test intentionally did not download or inspect file bodies. Therefore, the supported impact is limited to directory-listing metadata exposure and potentially sensitive-looking filenames.

## Finding Summary

| Field | Value |
|---|---|
| Candidate ID | CAND-001 |
| Title | Unauthenticated local-lab `/ftp/` directory listing exposes sensitive-looking filename metadata |
| Status | Lab-report-draft-ready candidate |
| Real bug bounty readiness | Not ready |
| Severity | Not assigned; likely informational/low unless file contents or program impact are proven |
| Confidence | Medium for directory listing existence; Low for real-world impact |
| Affected asset | `http://<lab-ip>:3000/ftp/` local lab route |
| Evidence type | Metadata-only, redacted/minimized |

## Scope and Rules of Engagement

In scope for this rehearsal:

- Local host-only target only: `http://<lab-ip>:3000`
- Fixed GET-only content-class verification against a short candidate path list
- Metadata, hashes, derived classifications, filename previews, and short redacted snippets only

Out of scope and not performed:

- Public or real bug bounty targets
- Recursive crawling
- File downloads or file-body inspection
- Credential attacks, brute force, session guessing, or authentication bypass attempts
- SQL dumps, loot collection, or sensitive content collection
- Exploit payloads, callbacks/OAST, reverse shells, listeners, persistence, or destructive testing
- Automatic confirmed finding promotion or real submission drafting

## Methodology

The verification run used a fixed candidate path list and a request cap of 7, including pre- and post-health checks:

1. `GET /` — pre-health baseline
2. `GET /robots.txt`
3. `GET /.well-known/security.txt`
4. `GET /ftp/`
5. `GET /rest/products/search`
6. `GET /api-docs/`
7. `GET /` — post-health baseline

The run stored only minimized evidence:

- status code
- content type
- content length
- body SHA-256
- page title when present
- derived body class
- filename previews for directory listings
- short redacted snippets for public text routes

No listed file was downloaded.

## Health and Safety Result

The lab remained stable during the run.

| Check | Result |
|---|---|
| Pre-health HTTP status | 200 |
| Post-health HTTP status | 200 |
| Pre-health body SHA-256 | `9893b61734b4a11bb9b81c6feb2c97d0cc6aaa59190f8ec885a6e86c25661cef` |
| Post-health body SHA-256 | `9893b61734b4a11bb9b81c6feb2c97d0cc6aaa59190f8ec885a6e86c25661cef` |
| Health conclusion | No obvious degradation; root hash stable |

## Technical Details

### `/robots.txt` discovery hint

`/robots.txt` returned HTTP 200 and contained:

```text
User-agent: *
Disallow: /ftp
```

This supports the discovery narrative because the application itself advertises `/ftp`. However, `robots.txt` is not access control and is not a vulnerability by itself.

### `/ftp/` directory-listing response evidence

`/ftp/` returned:

| Field | Observed value |
|---|---|
| HTTP status | 200 |
| Content-Type | `text/html; charset=utf-8` |
| Content-Length header | `11334` |
| Page title | `listing directory /ftp/` |
| Derived body class | `directory_listing_candidate` |
| Listing names observed | 12 |
| Body SHA-256 | `3144a22b1b6e773279d292ff98a8094f37eb2f790dff557170ce0f984fdccc6b` |

Sensitive-looking filename metadata observed in the listing preview:

```text
announcement_encrypted.md
coupons_2013.md.bak
encrypt.pyc
incident-support.kdbx
package-lock.json.bak
package.json.bak
suspicious_errors.yml
```

This evidence supports the claim that the local-lab route exposes unauthenticated directory-listing metadata and sensitive-looking filenames. Here, “public” means reachable without authentication inside the host-only lab; it does not mean publicly internet-exposed. It does not prove that the file contents are sensitive because file bodies were intentionally not retrieved.

### False-positive exclusion

The route is unlikely to be an SPA fallback false positive because:

- `/ftp/` returned title `listing directory /ftp/`, not `OWASP Juice Shop`.
- `/ftp/` content length differed from the root SPA baseline.
- The parser extracted listing names from the `/ftp/` HTML.
- The derived body class was `directory_listing_candidate`.

## Impact Discussion

Directory listings can expose internal filenames, backup artifacts, dependency manifests, encrypted archives, incident-support material, and operational hints. In a real environment, this can help an attacker prioritize follow-up requests or infer internal project structure.

For this lab rehearsal, the impact is intentionally constrained:

- Confirmed: unauthenticated directory-listing metadata is visible on the local lab route.
- Confirmed: the filename list includes backup-like and sensitive-looking names.
- Not confirmed: actual sensitive file contents.
- Not confirmed: credential exposure, source-code exposure, password database compromise, or real-world business impact.
- Not claimed: severity suitable for a real bug bounty report.

Most real bug bounty programs may treat metadata-only filename exposure as informational unless file contents, sensitive business context, or program-specific impact are proven. This report therefore keeps the item as a candidate and uses it to rehearse evidence quality, wording discipline, remediation, and retest planning.

## Reproduction Steps

These steps are for the local authorized lab only.

1. Confirm the local lab target is reachable:

```text
GET http://<lab-ip>:3000/
Expected: HTTP 200
```

2. Check the advertised path in `robots.txt`:

```text
GET http://<lab-ip>:3000/robots.txt
Expected body contains: Disallow: /ftp
```

3. Request the directory route:

```text
GET http://<lab-ip>:3000/ftp/
Expected: HTTP 200
Expected title/body marker: listing directory /ftp/
```

4. Review only listing metadata. Do not recursively crawl or download listed files unless separately authorized.

Expected result:

- `/ftp/` displays a directory listing.
- The listing includes backup-like and sensitive-looking filenames.

## Evidence Handling Notes

Evidence was minimized to reduce sensitive-data risk:

- The report includes filenames only, not file contents.
- No credential, token, cookie, or file-body evidence is included.
- Short public snippets are used only for `robots.txt`.
- Raw route bodies were not added to this report.

## Root Cause

The application serves a publicly accessible directory listing for `/ftp/`. Files or metadata that appear backup-like, encrypted-looking, or operationally sensitive are placed under a web-accessible directory, and `robots.txt` advertises the path instead of preventing access.

## Remediation

### Short-Term Mitigation

- Disable directory listing for `/ftp/` or the equivalent public directory.
- Remove unintended backup files, dependency manifests, password-manager-database-like artifacts if present and confirmed, encrypted archives, and incident/support artifacts from web-accessible directories.
- Return a controlled response such as `403`, `404`, or an intended static page for unauthenticated directory requests.

### Long-Term Fix

- Serve only explicitly allowlisted static assets from public web roots.
- Move operational, support, backup, dependency, and archive artifacts outside the document root.
- Add build/deployment checks that fail if backup-like or sensitive-looking filenames are published.
- Treat `robots.txt` as crawler guidance only, never as access control.
- Add regression tests for unauthenticated directory-listing exposure.

## Retest Plan

1. Request `/ftp/` unauthenticated.
   - Expected: no directory listing; `403`, `404`, or an intended controlled page.
2. If separately authorized and still in scope, request representative backup/manifest/archive filenames if they are still known to be present.
   - Expected: inaccessible to unauthenticated users or removed from the web root.
3. Re-check `robots.txt`.
   - Expected: it no longer advertises hidden or sensitive directories.
4. Confirm application health remains normal.
   - Expected: root page still returns HTTP 200 and intended content.

## Report Readiness Gate

| Gate | Status | Notes |
|---|---|---|
| Authorized scope | Pass for local lab only | Host-only Juice Shop lab |
| Route existence | Pass | `/ftp/` returns HTTP 200 |
| False-positive exclusion | Pass | Not SPA fallback; directory-listing marker observed |
| Sensitive content proof | Not performed | No file bodies downloaded |
| Impact proof | Partial | Metadata exposure only |
| Remediation | Drafted | Directory listing / document-root controls |
| Retest criteria | Drafted | 403/404/no listing; artifacts unavailable |
| Real bounty submission | Fail / blocked | Lab-only target; no real program authorization or file-content impact |

Final lab-only verdict:

```text
LAB_REPORT_DRAFT_READY_FOR_CAND_001_METADATA_EXPOSURE
NOT_READY_FOR_REAL_BUG_BOUNTY_SUBMISSION
```

## References

- CWE-548: Exposure of Information Through Directory Listing
- CWE-200: Exposure of Sensitive Information to an Unauthorized Actor
- OWASP Web Security Testing Guide: Information Gathering and Configuration Management testing concepts
- OWASP Juice Shop: intentionally vulnerable training application

## Appendix: Non-Findings from This Verification

These were observed but are not findings in this report:

- `/.well-known/security.txt`: expected public security/contact metadata.
- `/rest/products/search`: real JSON endpoint, but no sensitive-data or auth-bypass claim from this bounded check.
- `/api-docs/`: Swagger UI candidate only; no vulnerability claim without a separate bounded documentation exposure review.
