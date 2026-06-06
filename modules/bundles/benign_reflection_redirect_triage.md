> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# benign_reflection_redirect_triage

Status: active / local-lab bounded bundle
Date: 2026-05-21
Source: `scripts/lab_modules/wave2_benign_params.py`, `<artifact-output-dir>/phase4b_wave2_benign_rerun_20260521T070726Z/`

## Use when

Use this bundle when preview or recon results suggest a query-reflection or redirect endpoint candidate, but the current phase should avoid executable XSS payloads, broad parameter fuzzing, redirect following, scanners, or external callbacks.

Typical triggers:

```text
GET /search?q=<value> -> 200
GET /rest/products/search?q=<value> -> 200
GET /redirect?to=<value> -> 3xx/4xx candidate behavior
```

Current lab trigger:

```text
http://<lab-ip>:3000/
```

## Do not use when

- target is public/client/bug-bounty and no explicit scope/rules/run approval exists;
- the goal is browser-executed XSS payloading;
- the goal is broad parameter discovery, crawler expansion, or scanner execution;
- redirects must be followed to external domains;
- callbacks/OAST, credentialed flows, brute force, or destructive behavior would be needed;
- the operator expects confirmed vulnerability or report-ready output directly from the adapter.

## Inputs

- target base URL;
- prior preview/recon artifact or route hint showing search/redirect behavior;
- request cap, timeout, rate;
- output directory.

## Scripts

1. `scripts/lab_modules/wave2_benign_params.py`
   - Uses fixed GET-only inert canaries.
   - Checks API search reflection, SPA search fallback, external redirect canary, and relative redirect canaries.
   - Uses `--max-redirs 0` and does not follow redirects.
   - Does not run `open_redirect.sh`, `xss_finder.sh`, scanners, crawlers, or executable payloads.

Optional later:

2. offline importer/bridge
   - Converts reviewed observations into `needs_manual_review` candidate seeds only when a canary is reflected or a redirect candidate is observed.

## Caps

For local lab fast lane:

- planned active probes: 5 plus pre/post health;
- request cap: default 40, hard max 100;
- timeout: <= 5 seconds;
- rate: <= 2 req/sec;
- fixed URLs only;
- no redirect following;
- no external callback/OAST;
- raw bodies temporary only, redacted snippets in JSONL.

## Outputs

Expected output:

```text
observations.jsonl
summary.txt
health.txt
artifact_manifest.txt
per-step .headers files
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

- Did pre/post health remain stable?
- Did any reflection canary appear in a response body outside expected false-positive/error contexts?
- Did any redirect response include a `Location` header pointing outside the target host?
- Was SPA fallback treated as a false-positive control rather than reflection evidence?
- Did the run avoid executable payloads, redirect following, scanner/crawler behavior, callbacks, and finding promotion?

## Current local-lab result

Latest rerun artifacts:

```text
<artifact-output-dir>/phase4b_wave2_benign_rerun_20260521T070726Z/
```

Summary:

```text
pre_health=200
post_health=200
requests_sent=5
observations=5
```

Candidate assessment from the rerun:

- `/rest/products/search?q=PHASE4B_REFLECT_CANARY` returned 200 JSON but did not reflect the canary.
- `/search?q=PHASE4B_REFLECT_CANARY` returned 200 HTML with `OWASP Juice Shop` title and did not reflect the canary; treat as SPA fallback control.
- `/redirect?to=https://phase4b-canary.invalid/`, `/redirect?to=/`, and `/redirect?to=/#/score-board` returned 406 with no `Location` header; no open-redirect candidate for these fixed canaries.

## Report contribution

This bundle may contribute to a lab-only report rehearsal only after separate manual review finds a real candidate. Current rerun is a calibration/no-candidate result, useful for proving false-positive handling and safe parameter-triage workflow.

## Promotion rule

This bundle is active because:

1. `wave2_benign_params.py` exists and is tested;
2. tests cover inert canaries, public-target rejection, unsafe-limit rejection, no scanner/payload/promotion terms, and approval before writing scripts;
3. local-lab rerun succeeded with stable health at `<artifact-output-dir>/phase4b_wave2_benign_rerun_20260521T070726Z/`;
4. result is summarized in handoff and linked from `scripts/SCRIPT_INVENTORY.md`.

## Bridge deferral

Candidate-review bridge generation is deferred. Do not convert these observations into finding fixtures unless a future importer/bridge defines exact seed rules and keeps all output `needs_manual_review`, not confirmed/reportable.