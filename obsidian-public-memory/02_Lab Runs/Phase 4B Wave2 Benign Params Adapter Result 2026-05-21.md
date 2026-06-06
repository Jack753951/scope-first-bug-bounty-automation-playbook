> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4B Wave2 Benign Params Adapter Result 2026-05-21

Status: completed / local-lab fast lane / candidate-only
Repo truth: `<user-home>`

## What changed

- Added reusable Wave2 benign parameter adapter: `scripts/lab_modules/wave2_benign_params.py`.
- Added tests: `scripts/test_wave2_benign_params.py`.
- Ran fixed GET-only inert canaries through `<lab-vm>` against host-only Juice Shop.

## Run

Run id: `phase4b_wave2_benign_20260521T054852Z`
Artifacts: `<user-home>`

Health:

```text
pre_health=200
post_health=200
requests_sent=5
```

## Observations

- `/rest/products/search?q=PHASE4B_REFLECT_CANARY` -> 200 JSON, no canary reflection.
- `/search?q=PHASE4B_REFLECT_CANARY` -> 200 SPA HTML fallback, no canary reflection.
- `/redirect?to=https%3A%2F%2Fphase4b-canary.invalid%2F` -> 406, no `Location`, no open-redirect candidate.
- `/redirect?to=/` -> 406, no `Location`, no open-redirect candidate.
- `/redirect?to=/#/score-board` -> 406, no `Location`, no open-redirect candidate.

## Assessment

No XSS/reflection candidate found.
No open redirect candidate found.

Useful calibration:

- SPA 200 response is a false-positive trap, not reflection evidence.
- Redirect error-body echo is tracked separately as `canary_echoed_in_error_body`, not as redirect or reflection evidence.

## Next

Best next lab-fast-lane slice: bounded `/ftp/` filename/content-class verifier, because `/ftp/` remains the strongest candidate from the GET-only metadata adapter.
