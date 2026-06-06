> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> Account B passive owned-surface map (2026-05-26)

## Why this reference exists

This captures a reusable live-bounty pattern for SaaS first-contact work after the operator completes an identity/phone/auth gate locally: continue only low-speed owned/passive UI mapping, preserve useful proof hypotheses, then close as `surface_only` unless a fresh owned A/B proof boundary is explicitly approved.

## Pattern

1. Treat operator-completed signup/auth as a gate transition, not as permission for stronger testing.
2. Use browser/noVNC observation only; do not inspect or copy cookies, tokens, OTPs, passwords, phone numbers, or verification links.
3. During onboarding, prefer the lowest-risk path that reaches an owned dashboard:
   - profile/team survey choices are acceptable if non-secret and non-external;
   - skip/set-up-later external integrations;
   - stop before OAuth/mailbox/channel connection, invite send, workflow/rule activation, API token creation, or outbound communication.
4. If onboarding creates default owned objects, record them as owned/passive surface labels, not as vulnerability evidence.
5. Capture the hard gates that remain: channels/OAuth/mailbox, invites/roles, workflows/rules/Topics, API tokens/calls, messages/comments/discussions, report submission.
6. Promote the lane as `surface_only` / `not_report_ready` unless there is an explicit approved proof boundary with owned accounts/objects and allowed state changes.

## Evidence shape used

- `programs/<program>/lane_state.json`: keep schema-valid; use existing enum states/statuses such as `A2_SURFACE_MAP_COMPLETE` / `surface_only` rather than inventing descriptive states that break validation.
- `handoff/live_bounty_evidence/<program>/<lane>/evidence_surface_map_<date>.json`: structured redacted evidence with observations, positive evidence, negative controls, redactions, candidate signals, blocked states, and next learning seed.
- `handoff/<program>_account_b_passive_surface_map_<date>.md`: human summary.
- Navigation sync: update current navigation, active queue, artifact index, accepted changes, and project Obsidian bridge when the lane state changes.

## Validation pattern

Run, when available:

```bash
python scripts/live-bounty-lane-status.py validate --state programs/<program>/lane_state.json --evidence handoff/live_bounty_evidence/<program>/<lane>/evidence_surface_map_<date>.json --queue handoff/live_bounty_lane_queue.json
python scripts/evidence-redaction-check.py --json <summary.md> <evidence.json>
git diff --check -- <changed files>
bash ./bin/hermes review
```

## Pitfalls caught

- Do not leave lane state as a descriptive custom enum (for example `account_b_authenticated_surface_only_channel_gate`); schema validation will fail. Put nuance in `next_autonomous_action`, `operator_gates`, `learning.next_preview_seed`, or the evidence JSON.
- Do not treat default onboarding-created owned labels as a proof; they are surface map evidence only.
- Do not let setup-guide tasks tempt action: connect channel, invite team, automate workflows/rules, and Topics are gates until explicitly approved.
- Local screenshots may contain account initials, browser URLs, workspace labels, trial banners, or object IDs; keep them in ignored local storage unless separately redacted.
