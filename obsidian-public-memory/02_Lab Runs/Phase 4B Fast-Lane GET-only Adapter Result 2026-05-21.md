> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4B Fast-Lane GET-only Adapter Result 2026-05-21

Status: completed / local-lab only / candidate-only
Repo truth: `<user-home>`

## What changed

- Created lab fast-lane policy for host-only Juice Shop Tier 1/Tier 2 checks.
- Added reusable GET-only adapter: `scripts/lab_modules/phase4b_get_only_metadata_probe.py`.
- Added tests: `scripts/test_phase4b_get_only_metadata_probe.py`.
- Ran adapter through `<lab-vm>` against `<lab-vm>` Juice Shop.

## Run

Run id: `phase4b_fast_lane_20260521T053646Z`
Artifacts: `<user-home>`

Health:

```text
pre_health=200
post_health=200
requests_sent=8
```

## Observations

- `/ftp/` -> 200, title `listing directory /ftp/`, candidate for directory-listing finding rehearsal.
- `/api-docs/` -> 200, title `Swagger UI`, candidate for exposed API-docs metadata rehearsal.
- `/search?q=phase4b_canary` -> 200 SPA fallback; false-positive control.
- `/redirect?to=https://phase4b-canary.invalid/` -> 406, no redirect for this canary.

## Next

Build `scripts/lab_modules/wave2_benign_params.py` using the same fast-lane contract:

- fixed local target
- inert parameter canaries
- no executable payloads
- no crawler/scanner
- JSONL candidate-only output
