> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A Content-Class Verification to Lab-Only Report Rehearsal

Use this pattern after a bounded content-discovery/path-enumeration rehearsal has produced candidate-only observations and an output-side review has approved a short manual follow-up list.

## Trigger

- Local/intentionally vulnerable lab only.
- Prior output-side review says a small set of paths is worth manual content-class verification.
- Goal is lab-only report rehearsal, not real bug-bounty submission.

## Safe execution shape

1. Fix the target and candidate path list up front.
2. Use GET-only or HEAD-only requests depending on the review's allowed step.
3. Keep a hard request cap including pre/post health checks.
4. Do not recurse, crawl, brute force, authenticate, exploit, callback, or bulk-download.
5. Store only metadata, hashes, derived classifications, filename previews, and short redacted snippets.
6. Run pre/post health and compare status plus a stable root/body hash where practical.

## Classification rules

- Directory listing candidate: title/body markers plus extracted listing names; not SPA fallback.
- Robots.txt: discovery narrative only; never access control and not a finding by itself.
- Security.txt: expected public contact/security metadata; not a finding.
- JSON API metadata: endpoint existence only; no auth-bypass or sensitive-data claim without separate proof.
- API docs/Swagger: docs route candidate only; exposure claim needs separate bounded docs review.
- Repeated same-size 200 HTML paths: likely SPA fallback; exclude from findings until content-class differs from root/canary.

## Report-readiness transition

If the route is verified as a real directory listing and health is stable, it can become `LAB_REPORT_DRAFT_READY` as metadata exposure only. It is still not real bounty submission-ready when:

- the target is intentionally vulnerable/local lab;
- file bodies were not inspected;
- impact is inferred from metadata/filenames only;
- no program-specific rules or real authorization package exists.

Use cautious wording:

> Public directory listing at `/path/` exposes metadata and sensitive-looking filenames. The path may be advertised by `robots.txt`. Current evidence supports a lab-only metadata exposure candidate, not a confirmed sensitive-data leak.

Remediation:

- Disable directory listing.
- Remove unintended backup/sensitive artifacts from the web root.
- Serve only allowlisted static assets.
- Do not rely on robots.txt as access control.

Retest:

- Directory no longer lists contents.
- Sensitive/backup artifacts are unavailable unauthenticated.
- robots.txt no longer advertises hidden sensitive paths.

## Pitfalls

- Do not inspect or download `*.bak`, `*.kdbx`, `secret`, `token`, `password`, backup, incident, dependency-lock, or encrypted-looking files during first-pass calibration unless the operator explicitly approves exactly one narrow non-sensitive sample.
- Do not call metadata-only directory listing a confirmed sensitive-data leak.
- Do not reuse local-lab conclusions as real program bounty findings.
- Do not skip output-side review when the candidate involves API docs, JSON endpoints, HEAD 500 anomalies, or sensitive-looking filenames.

## Session reference

This pattern was distilled from a Juice Shop local lab run where `/ftp/` was verified with a fixed GET-only list, request cap 7, stable pre/post root hash, no downloads, and a lab-only report draft readiness verdict for metadata exposure.