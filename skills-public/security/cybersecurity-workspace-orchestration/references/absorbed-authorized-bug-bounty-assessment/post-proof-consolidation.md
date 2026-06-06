> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Post-Proof Consolidation Reference

Use this after any new proof, bundle, live-target surface map, report packet, bridge artifact, or authorization-gate/tooling fix in an authorized assessment project.

## Why it exists

Do not rely only on periodic cron reviews to notice new evidence or bundles. The session that created the artifact has the freshest context and should immediately decide how it affects future work. The goal is not more documentation; it is making the artifact discoverable and decision-useful for the next worker.

## Classify first

Choose one status/class before editing indexes:

```text
local_lab_verified_proof
local_lab_candidate
attempted_not_verified
live_surface_map
live_candidate
report_packet
tooling_gate_fix
bridge_or_decision_aid
reference_only
```

Use conservative live-target labels:

```text
surface_only
needs_second_account
blocked_state_change
blocked_sensitive_flow
blocked_operator_action
gate_fail_closed_needs_fix
gate_fixed_dry_run_verified
candidate
report_ready
not_report_ready
```

Never promote a `surface_only`, `candidate`, or `needs_second_account` observation just because it is well documented.

## Authority files to update

Update only what future agents will actually read:

- `handoff/accepted_changes.md` — append-only summary with boundary and validation.
- `handoff/current_navigation.md` — only if next safe action, gate status, or main route changed.
- `handoff/active_strategy_queue.md` — only if priority/order/blockers changed.
- Project Obsidian note — compact repo-truth path and synthesis.
- Proof library index — for local reusable proof patterns.
- Live-bounty bridge — for live prerequisites, blocked states, no-finding value, Account A/B prerequisites.
- Script/tool inventory and focused tests — for automation/gate fixes.

## Required reusable-proof metadata

A reusable proof/bundle should answer:

```text
Use when:
Do not use when:
Minimum evidence:
Positive control:
Negative control:
Required accounts / roles:
State-changing risk:
Safe local runner:
Artifact root:
Live bounty prerequisites:
Blocked live states:
Report-readiness threshold:
```

If it cannot answer these, keep it `reference_only`, `candidate`, or `attempted_not_verified`.

## Validation

Run the narrowest tests that prove the new claim, plus project hygiene:

```text
focused tests for changed scripts/tools
git diff --check
project local review command, if available
```

For authorization gates, prove both sides:

```text
exact in-scope dry-run passes
clearly out-of-scope dry-run fails
overrides remain dry-run-only or otherwise blocked
```

A fixed dry-run gate can be labeled `gate_fixed_dry_run_verified`, but that is not authorization for live scanner-like automation.

## Wrap-up shape

Use the user's preferred project wrap-up:

```text
Benefit:
Changes:
Validation:
Next safe action:
```

## Hard boundaries

The consolidation pass must not:

- touch live targets;
- add scope or authorize automation;
- run scans/fuzzers/callbacks;
- submit reports;
- store cookies, tokens, OTPs, phone numbers, emails, addresses, secrets, or raw loot;
- auto-promote candidate/no-finding evidence to reportable.

## Script pattern

A project may implement this as a dry-run checklist script, e.g.:

```bash
scripts/post-proof-consolidation.sh \
  --type live_surface_map \
  --artifact handoff/<artifact>.md \
  --dry-run
```

The script should print required updates and validation gates, not silently edit status-critical files unless a human/operator explicitly approves that behavior.
