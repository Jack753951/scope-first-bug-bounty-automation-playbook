> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Gate closeout and next-direction-review handoff pattern

Use this when a cybersecurity workspace finishes a cluster of offline/synthetic hardening slices and needs to move the project forward without prematurely implementing the next boundary.

## Trigger

- A review lane or gate has accumulated several completed micro-slices (tests, docs, dry-run hardening, fixture clarifications).
- The active queue says the next decision is whether to move into a new platform/runtime boundary.
- The next lane would touch a contract, runner, recon bridge, execution boundary, evidence/finding/report lifecycle, or lab/live activation.

## Pattern

1. Read the active navigation layer and governing policies first:
   - `handoff/active_strategy_queue.md`
   - `handoff/accepted_changes.md`
   - review tier / multi-party review / OSS gate docs
   - most recent direction + implementation-review artifacts
2. Write a concise gate closeout artifact, not another implementation patch.
   - Record what is complete.
   - Name deferred recommendations and their re-open triggers.
   - Decide whether the gate is `PASS`, `PASS_WITH_CONDITIONS`, `DEFER`, or `BLOCK`.
   - State the safety boundary: handoff/planning only, no target interaction, no runtime change.
3. Prepare the next direction-review prompt when the next step crosses a platform boundary.
   - Make it design-only/read-only.
   - Require OSS Recon Gate for T3+ surfaces.
   - Ask for `APPROVE`, `APPROVE_WITH_CHANGES`, `DEFER`, or `BLOCK`.
   - Forbid implementation inside the review.
4. Update the rolling task pointer and create a named task artifact.
   - Example: `handoff/claude_code_task.md` plus `handoff/claude_code_task_pN.md`.
5. Update navigation and acceptance history.
   - `handoff/active_strategy_queue.md`: next lane, current artifact, boundary.
   - `handoff/accepted_changes.md`: append/prepend concise closeout/prep record per project convention.
6. Validate and publish as a handoff-only change.
   - `git diff --check`
   - project review wrapper such as `USER=${USER:-Owner} HACKLAB=<user-home> ./bin/hermes review`
   - added-line secret scan when touching handoff/task prompts
   - commit/push/comment on existing PR if the workspace is already using PR review.

## Safety assertions for the closeout artifact

Explicitly say what did not change:

- no target-touching automation
- no scanner/module execution
- no `config/scope.txt` or real program-scope changes
- no runtime edits unless the completed gate truly included reviewed runtime hardening
- no schemas, modules, report/submission adapters, scheduler, credentials/OAuth, deployment, billing, or production settings
- no bridge implementation until the next direction review approves it

## Direction prompt requirements for bridge-style next lanes

For a recon-to-runner, evidence/finding, importer/exporter, or report boundary, ask the reviewer to answer:

- tier and milestone boundary, including whether T3 proximity escalates to T4
- whether to bridge now or defer
- smallest safe implementation shape and maximum file list if proceeding
- exact runtime files that may or may not be edited
- OSS Recon Gate comparison with 2-5 relevant projects/formats
- required focused tests and negative safety assertions
- deferred items and fresh-review triggers

## Pitfalls

- Do not let a closeout artifact quietly authorize implementation. It should close one gate and prepare the next review.
- Do not run the worker implementation command until the prompt is bounded and the current handoff state is clean.
- Do not keep adding micro-hardening just because there are non-blocking recommendations; name re-open triggers and move to the next mainline decision.
- Do not describe lab/live activation as the default next step unless the operator explicitly approves and the required T4/T5 review path is satisfied.
