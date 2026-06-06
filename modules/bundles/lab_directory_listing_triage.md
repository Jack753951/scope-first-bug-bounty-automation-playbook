> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_directory_listing_triage

Status: active / local-lab bounded bundle
Date: 2026-05-21
Source: `<artifact-output-dir>/phase4b_fast_lane_20260521T053646Z/`, `handoff/phase4b_fast_lane_get_only_result_20260521.md`

## Use when

Use this bundle when preview or recon results show a directory-listing candidate such as:

```text
GET /ftp/ -> 200
title ~= listing directory /ftp/
content-type ~= text/html
```

Current lab trigger:

```text
http://<lab-ip>:3000/ftp/
```

## Do not use when

- target is public/client/bug-bounty and no explicit scope/rules/run approval exists;
- the goal is bulk download;
- the script would collect secrets, credentials, tokens, PII, proprietary files, or loot;
- recursive crawling is required;
- the operator has not approved target-touching execution for the target class.

## Inputs

- target base URL;
- candidate path, default `/ftp/`;
- prior preview/recon artifact path;
- request cap and timeout;
- output directory.

## Scripts

Current:

1. `scripts/lab_modules/phase4b_get_only_metadata_probe.py`
   - Confirms `/ftp/` appears as a metadata candidate.

2. `scripts/lab_modules/ftp_filename_content_class_verifier.py`
   - Lists filenames from `/ftp/` HTML.
   - Performs one bounded GET of the listing page only; no listed-file downloads.
   - Records filename, href, normalized path, extension, and content class.
   - Does not bulk download.
   - Does not retain raw bodies.

Optional later:

3. evidence packet/report helper
   - Converts reviewed candidate into lab report rehearsal input.

## Caps

For local lab fast lane:

- request cap: default <= 40, hard max <= 100;
- timeout: <= 5 seconds;
- rate: <= 2 req/sec;
- pre/post health required;
- no recursion;
- no external domains;
- no redirects followed unless explicitly documented.

## Outputs

Expected output:

```text
observations.jsonl
summary.txt
health.txt
artifact_manifest.txt
```

Observation vocabulary:

```text
candidate
needs_manual_review
no_candidate
blocked
```

## Review

Reviewer checks:

- Is this truly directory listing metadata, not a SPA false positive?
- Are filenames classified without retaining sensitive file contents?
- Did the run avoid bulk download and recursion?
- Did pre/post health remain stable?
- Is there a clear manual verification TODO before report wording?

## Report contribution

This bundle may contribute to a lab-only report rehearsal after review:

- finding class: directory listing / information disclosure / security misconfiguration;
- evidence: URL, status, title, filename classes, content-type/size metadata;
- impact: constrained to exposed listed files/classes, not assumed secrets;
- remediation: disable directory listing, restrict static file exposure, validate intended public files;
- retest: `/ftp/` should no longer list directory contents or should only expose intended files.

## Promotion rule

This bundle was promoted from draft to active after:

1. `ftp_filename_content_class_verifier.py` exists;
2. tests cover public-target rejection, request caps, no bulk download, and filename classification;
3. one local-lab run succeeded with health stable at `<artifact-output-dir>/phase4b_ftp_filename_20260521T064526Z/`;
4. result is summarized in handoff and linked from `scripts/SCRIPT_INVENTORY.md`.

## Bridge deferral

This wave leaves behind a reusable runner/module bundle, but candidate-review bridge generation is deferred. The output contains filename classes only and still requires manual review before evidence/report language. Do not convert the listed filenames into finding fixtures until a separate bridge/importer slice defines exactly which content classes become candidate seeds and confirms no file contents are retained.
