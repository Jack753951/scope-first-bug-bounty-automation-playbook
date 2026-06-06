> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec offline contract validation notes

Use this reference when reviewing schema/validator phases in the cybersec lab or similar safety-gated repos.

## Pattern that worked

1. Keep the phase boundary narrow: schema + read-only validator + fixtures + tests only.
2. Require direction review before implementation for new contracts or archive/ledger boundaries.
3. Make validators standard-library-only and read-only. Static tests should forbid network/process modules such as `socket`, `urllib`, `http`, `subprocess`, `threading`, and `multiprocessing` unless the phase explicitly authorizes them.
4. Add committed golden fixtures under `tests/fixtures/<contract>/<version>/` and assert they pass.
5. Add read-only filesystem snapshot tests so validation leaves file contents and mtimes unchanged.
6. For ledger/index contracts, bind entries by exact relative path + SHA-256 + byte size + strict observed schema version. Do not walk or revalidate inner artifacts in the ledger validator if layering says a lower-level validator owns them.
7. Run focused tests first, then combined contract tests, then full discovery, then JSON parse, `git diff --check`, and Hermes review.
8. Obtain independent implementation/safety review for T3+ contract/platform boundaries and record no-blocker verdict in handoff.
9. If the independent reviewer returns `REQUEST_CHANGES`, fix the blocker, rerun focused/full validation, then ask for a follow-up read-only review of the exact blocker fix. Record both the initial verdict and the follow-up `PASS`/remaining issues in handoff instead of silently overwriting the review history.
10. For calibration side-quests such as CTF scaffolding, explicitly ask the reviewer whether the work still advances the main authorized bug-bounty automation roadmap. If it does not, close the calibration artifact as trial-only/non-runtime and redirect the next phase back to bug-bounty triage, verification, review packets, reporting, or platform integration.

## Transient validation behavior

Full test discovery can occasionally timeout on unrelated long-running dry-run recon tests while focused contract tests and Hermes static review are clean. Do not immediately treat that as a new regression from the contract work. Re-run the specific timed-out test(s), then re-run full discovery once. Record both the initial timeout and the final clean run if the retry passes.

## Compact independent-review packet workaround

If an interactive Claude/Cowork implementation review hits `max turns`, build a compact review packet containing only the direction review, schema, validator, tests, fixtures, and handoff summary. Invoke the reviewer with no tools / one-turn JSON-only output, then parse and save the JSON review artifact. This preserves independent review while avoiding tool-loop exhaustion.
