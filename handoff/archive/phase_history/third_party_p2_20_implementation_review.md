> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Third-Party Review — P2.20 Candidate Review Packet Gap Consumer

Date: 2026-05-18
Route: Hermes `delegate_task` independent implementation/safety review + follow-up review
Scope: read-only review of `scripts/review_candidate_packet_gaps.py`, `scripts/test_candidate_packet_gaps.py`, `scripts/README.md`, and P2.20 handoff files.

## Initial Verdict

REQUEST_CHANGES

## Initial Blocker

The initial review found one blocker: the consumer rejected live-target flags and dash-prefixed unknown args, but accepted ordinary positional arguments such as `unexpected-positional` and still returned an `ok` gap report. This violated the P2.20 direction review requirement that the consumer accepts no command-line arguments and that all unknown args fail closed with structured JSON errors.

## Hermes Fix

Hermes added a focused regression test:

- `test_rejects_positional_argument_with_json_error`

Hermes then changed `_live_flag_errors(argv)` so every CLI argument is rejected:

- live target flags return `LIVE_TARGET_FLAG_NOT_ALLOWED`
- all other args, including positional args, return `ARGUMENT_NOT_ALLOWED`

The RED test failed before the fix and passed after the fix.

## Follow-Up Verdict

PASS

Follow-up third-party read-only review confirmed:

- focused tests pass (`11 OK`)
- positional args fail closed with structured JSON error output
- unknown args fail closed with structured JSON error output
- live-target flags still fail closed with `LIVE_TARGET_FLAG_NOT_ALLOWED`
- no stderr output is required for these error paths
- no new blockers were found

## Safety Boundary Confirmed

P2.20 remains a trial-only, offline, stdin-to-stdout gap/action consumer. It does not promote schemas, draft bug bounty reports, confirm vulnerabilities, touch live targets, read scope/config/credentials/loot/evidence files, write output files, import network/subprocess/runtime primitives, or wire into runner/recon/CI/scheduler/platform adapters.
