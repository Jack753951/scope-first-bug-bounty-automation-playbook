> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B Fast-Lane GET-only Adapter Result — 2026-05-21

Status: completed / local-lab only / candidate-only
Run id: `phase4b_fast_lane_20260521T053646Z`
Route/tool: Hermes on Windows control plane -> project SSH bridge -> `<attacker-vm>` -> host-only Juice Shop
Visible model/runtime: current Hermes agent model details are provided by the runtime header when visible; no external coding worker was used for implementation.
Usage artifact path: none; direct Hermes tool execution only.

## Scope

Allowed target:

- `http://<lab-ip>:3000/`
- victim: `<victim-vm>` / OWASP Juice Shop
- attacker: `<attacker-vm>`
- network: VirtualBox host-only

No public target, no bug-bounty target, no credential workflow, no callback/OAST, no brute force, no crawler, no scanner broad run, no destructive action.

## Policy change

Created lab fast-lane policy:

- `handoff/phase4b_lab_fast_lane_policy_20260521.md`

This permits bounded Tier 1/Tier 2 host-only lab probes to run with lighter pre-execution overhead when they preserve request caps, health checks, artifacts, and candidate-only output.

## Adapter added

Added reusable adapter:

- `scripts/lab_modules/phase4b_get_only_metadata_probe.py`

Added tests:

- `scripts/test_phase4b_get_only_metadata_probe.py`

Adapter properties:

- fixed/private lab target only
- GET-only metadata checks
- no HEAD requests, avoiding earlier Juice Shop HEAD/timeout ambiguity
- fixed path list
- request cap default 40, maximum 100
- timeout maximum 5 seconds
- rate limit maximum 2 requests/sec
- pre/post health files
- JSONL candidate-only observations
- temporary raw bodies removed after hashing/snippet extraction
- public targets rejected
- executable script writing requires `--lab-approved`

## Execution artifacts

Local artifact directory:

- `<artifact-output-dir>/phase4b_fast_lane_20260521T053646Z/`

Files:

- `observations.jsonl`
- `summary.txt`
- `health.txt`
- `pre_health.txt`
- `post_health.txt`
- `artifact_manifest.txt`
- per-step `.headers` files

## Health

```text
pre_health=200
post_health=200
requests_sent=8
```

The target remained healthy after the run.

## Observations

The adapter produced 8 candidate-only observations:

- `/` -> 200, title `OWASP Juice Shop`
- `/robots.txt` -> 200, `User-agent: * Disallow: /ftp`
- `/.well-known/security.txt` -> 200, security contact metadata
- `/ftp/` -> 200, title `listing directory /ftp/`, `directory_listing_candidate=true`
- `/api-docs/` -> 200, title `Swagger UI`
- `/rest/products/search?q=phase4b_canary` -> 200 JSON success empty data
- `/search?q=phase4b_canary` -> 200 SPA HTML fallback, useful false-positive control
- `/redirect?to=https://phase4b-canary.invalid/` -> 406, no Location header, negative open-redirect control

Curl printed a timeout warning for `/ftp/` while still capturing a 200 response and 11275 bytes. Because the adapter is candidate-only, this does not promote the observation to a confirmed finding. It does show that the next directory-listing verifier should either use a slightly larger timeout or treat near-complete FTP listing reads as a special content-class case.

## Candidate assessment

Most useful candidates:

1. `/ftp/` directory listing metadata
   - best next lab finding-rehearsal candidate
   - still needs bounded filename/content-class verifier, not bulk download

2. `/api-docs/` Swagger UI metadata
   - useful attack-surface disclosure rehearsal
   - not a vulnerability by itself

Negative/false-positive controls:

- `/search?q=phase4b_canary` confirms SPA fallback; do not treat 200 HTML as reflection evidence.
- `/redirect?to=https://phase4b-canary.invalid/` returned 406 without `Location`; no open redirect candidate for this canary.

## Validation

TDD status before execution:

- `python -m unittest scripts.test_phase4b_get_only_metadata_probe -v` -> OK, 4 tests

The final full repo review is recorded separately after documentation updates.

## Next step

Use the lab fast lane to add a second adapter:

- `scripts/lab_modules/wave2_benign_params.py`

Initial scope should be bounded benign parameter checks only:

- inert reflection canary
- redirect canary variants from a fixed local allowlist
- no executable JavaScript payload
- no crawler / gau / dalfox / kxss
- same health/artifact/candidate-only contract
