> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B Wave2 Benign Params Adapter Result — 2026-05-21

Status: completed / local-lab fast lane / candidate-only
Run id: `phase4b_wave2_benign_20260521T054852Z`
Route/tool: Hermes on Windows control plane -> project SSH bridge -> `<attacker-vm>` -> host-only Juice Shop
Visible model/runtime: current Hermes session model details are provided by the runtime header when visible; no external coding worker was used.
Usage artifact path: none; direct Hermes tool execution only.

## Scope

Allowed target:

- `http://<lab-ip>:3000/`
- victim: `<victim-vm>` / OWASP Juice Shop
- attacker: `<attacker-vm>`
- network: VirtualBox host-only

No public target, bug-bounty target, credential flow, callback/OAST, crawler, broad scanner, brute force, destructive action, or finding promotion.

## Adapter added

Added reusable Wave2 adapter:

- `scripts/lab_modules/wave2_benign_params.py`

Added tests:

- `scripts/test_wave2_benign_params.py`

Adapter properties:

- fixed/private lab target only
- GET-only benign parameter probes
- inert text canary only: `PHASE4B_REFLECT_CANARY`
- inert redirect canaries only, including `https://phase4b-canary.invalid/`
- `--max-redirs 0`; redirect chains are not followed
- no executable JavaScript payloads
- no `gau`, `kxss`, `dalfox`, `sqlmap`, crawler, scanner, callbacks, or brute force
- pre/post health required
- JSONL candidate-only observations
- raw bodies temporary only
- writing an executable script requires `--lab-approved`
- public targets rejected

## Execution artifacts

Local artifact directory:

- `<artifact-output-dir>/phase4b_wave2_benign_20260521T054852Z/`

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
requests_sent=5
```

The target remained healthy after the run.

## Observations

The adapter produced 5 candidate-only observations:

1. `/rest/products/search?q=PHASE4B_REFLECT_CANARY`
   - status: 200
   - content type: `application/json; charset=utf-8`
   - response: empty success data
   - `canary_in_body=false`
   - assessment: no reflection candidate for this inert canary

2. `/search?q=PHASE4B_REFLECT_CANARY`
   - status: 200
   - content type: `text/html; charset=UTF-8`
   - title: `OWASP Juice Shop`
   - `canary_in_body=false`
   - assessment: SPA fallback false-positive control, not reflection evidence

3. `/redirect?to=https%3A%2F%2Fphase4b-canary.invalid%2F`
   - status: 406
   - no `Location` header
   - `external_redirect_candidate=false`
   - `canary_echoed_in_error_body=true`
   - assessment: target rejects this external redirect canary; no open-redirect candidate

4. `/redirect?to=/`
   - status: 406
   - no `Location` header
   - `external_redirect_candidate=false`
   - assessment: no relative-root redirect candidate for this canary

5. `/redirect?to=/#/score-board`
   - status: 406
   - no `Location` header
   - `external_redirect_candidate=false`
   - assessment: no relative-fragment redirect candidate for this canary

## Candidate assessment

No XSS/reflection candidate was found in this Wave2 inert-canary run.

No open redirect candidate was found in this Wave2 inert-canary run.

Useful calibration outcomes:

- The search SPA route is confirmed as a false-positive trap: 200 HTML does not imply reflection.
- The product search API returns success/empty data without reflecting the inert canary.
- Juice Shop's redirect endpoint rejects these three fixed canaries with 406 and no `Location` header.
- Error-body echo is tracked separately as `canary_echoed_in_error_body` and does not count as reflection or redirect evidence.

## Validation

Focused TDD before execution:

- `python -m unittest scripts.test_wave2_benign_params -v` -> OK, 4 tests

Final repo validation is recorded separately after documentation updates.

## Next step

Recommended next lab-fast-lane slice:

- bounded `/ftp/` filename/content-class verifier

Rationale:

- Current strongest candidate remains `/ftp/` directory listing metadata from the GET-only adapter.
- The verifier should list filenames and classify content type/size only.
- It should avoid bulk downloads, secrets collection, credential material, and confirmed-finding wording.
