> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live-bounty machine lane state substrate

Use this pattern when a live-bounty workflow is becoming too markdown-dependent and needs resumable, machine-checkable lane state without increasing approval burden or touching targets.

## Goal

Convert authorized live-bounty lanes into local-only orchestration artifacts that answer:

```text
what lane is next?
why is it blocked or runnable?
what exact operator gate remains?
what can Hermes do autonomously after the gate?
which evidence is safe to promote?
```

This is an automation/systematization substrate, not a new target-touching runner and not a new approval-heavy safety workflow.

## Core artifacts

Recommended project-local files:

```text
schemas/live_bounty_lane_state.schema.json
schemas/live_bounty_evidence.schema.json
handoff/live_bounty_lane_queue.json
programs/<program_slug>/lane_state*.json
handoff/live_bounty_evidence/<program_slug>/<lane_id>/*.json
scripts/live-bounty-lane-status.py
scripts/evidence-redaction-check.py
tests/test_live_bounty_state_and_redaction.sh
```

The exact filenames can vary, but keep these concepts separate:

- lane state: current state, gates, allowed/blocked actions, stop conditions, next autonomous action, next operator action;
- evidence summary: request budget, observations, controls, redactions, limitations, candidate/no-finding/report-ready status vocabulary;
- queue: ordered list of lanes with state-file pointers;
- status CLI: validates/summarizes queue, lane state, and evidence;
- redaction checker: fails closed before evidence promotion and does not leak raw sensitive matches in its own output.

## Lane state fields to require

```text
schema_version
program_slug
lane_id
lane_title
autonomy_level
state
status
authorization.scope_file
authorization.dry_run_gate
authorization.out_of_scope_control
lane_boundary.allowed_actions
lane_boundary.blocked_actions
operator_gates
stop_conditions
next_autonomous_action
next_operator_action
artifacts.dry_run_packet
learning.next_preview_seed
updated_at
```

Use explicit blocked/runnable states such as:

```text
A2_PENDING_OPERATOR_AUTH
blocked_operator_action
blocked_awaiting_scope
candidate
needs_manual_review
no_finding
report_ready
```

Do not allow unreviewed promotional terms such as `verified`, `confirmed`, or `reportable` in machine evidence unless a report-readiness gate has explicitly produced them.

## Queue coherence requirements

A queue entry must not be treated as valid merely because it is syntactically well-formed. Validate:

```text
program_slug exists
lane_id exists
state_file exists
priority is an integer
status exists
state_file program_slug/lane_id/status match the queue entry when practical
```

Regression-test the negative case: a queue entry pointing to a missing `state_file` must fail closed.

## Redaction-output hygiene

The redaction checker must not re-leak the sensitive data it detects. Findings should include kind/file/line plus a redacted excerpt, not the raw matched line.

Check for common live-bounty evidence hazards:

```text
Authorization headers
Set-Cookie headers
Bearer tokens
JWT-shaped values
api_key / secret / token assignments
email addresses
phone-like values
OTP-like lines
```

Also regression-test useful non-secrets such as ISO dates (`YYYY-MM-DD`) so normal status artifacts do not false-positive as phone numbers.

## TDD + review loop

1. Write a focused RED test for schema validation, queue validation, status output, and redaction behavior.
2. Watch the test fail for the expected reason.
3. Implement the smallest local-only substrate.
4. Run focused validation.
5. Send the slice to an independent reviewer when it affects orchestration, evidence promotion, or live-bounty state.
6. Convert any `REQUEST_CHANGES` blocker into a regression test before patching.
7. Rerun focused tests and obtain a second review if the first review found blockers.
8. Update authority files: accepted changes, current navigation, active strategy queue, and project notes/Obsidian.

## Boundary

This pattern does not authorize:

```text
target requests
account signup/login
scanner/fuzzer/DAST execution
exploit attempts
credential handling
cross-tenant tests
report submission
```

It only makes the next safe state and gate machine-readable so Hermes can resume efficiently after a real operator or scope gate is satisfied.
