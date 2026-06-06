> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec Policy/Docs Closeout Pattern

Use this when a safety-gated cybersec repo finishes an offline calibration/policy slice and needs to move to the next lane without accidentally promoting runtime behavior.

## Trigger

- A fixture/catalog/policy/docs-only slice has been accepted.
- A direction review recommends a narrow docs-only follow-up.
- The repo has many rolling handoff files and untracked artifacts, so navigation state can drift.

## Pattern

1. Close the previous mini-thread first.
   - Create a named checkpoint under `handoff/`, e.g. `p3_12_closeout_current_thread_pause_<date>.md`.
   - State tier, authority, reviewers consulted, safety boundary, OSS Recon Gate status, and next default lane.
   - Explicitly say what remains deferred and what is not approved.

2. Update navigation and acceptance layers.
   - `handoff/active_strategy_queue.md`: current lane, next candidates, deferred lanes.
   - `handoff/accepted_changes.md`: append concise accepted-change entry.
   - `notes/daily/<date>.md`: short session log and boundary.

3. For the next policy/docs lane, run a direction review before editing.
   - Write a named direction prompt.
   - Ask Cowork to classify tier and boundary.
   - If it returns T1 docs-only / Hermes direct authority, local Hermes edits are acceptable.

4. Keep future fields non-contractual.
   - Policy may list future field candidates, but must say they are not schema, not manifest contract, not implemented, not validated, and not consumed by any runner.
   - Any promotion to schema/manifest/profile/runner is T3+ and needs OSS Recon Gate.

5. Validate even for docs-only changes.
   - Run `git diff --check`.
   - Run `HACKLAB=$(pwd) ./bin/hermes review`.
   - Record that Python/shell checks passed even if only Markdown changed.

6. Handle unrelated transient artifacts conservatively.
   - If an untracked temp test directory exists, identify it as non-slice noise.
   - If deletion is denied, do not retry; record it in the final summary.

## Pitfalls

- Do not let a docs-only risk-tier appendix become an implicit manifest contract.
- Do not skip the active strategy queue update; otherwise the next session may reopen a closed lane.
- Do not treat `dry-run` or generic automation permission as live authorization.
- Do not convert non-blocking direction-review recommendations into hidden blockers.
