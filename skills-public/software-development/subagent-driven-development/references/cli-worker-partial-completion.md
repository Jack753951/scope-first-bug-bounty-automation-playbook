> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# CLI Worker Partial-Completion Pattern

Use this when implementation is delegated to an external CLI worker (Claude Code, Codex CLI, OpenCode, repo wrapper scripts) and the worker exits on a turn/time/token limit or without a clean final report.

## Durable lesson

A bounded CLI worker can produce useful, mostly-correct workspace changes even when its own run reports failure such as `reached max turns`. Treat that as an incomplete orchestration event, not as proof the implementation failed or succeeded.

## Recovery sequence

1. Freeze the scope: do not broaden the task or start a second full implementation pass.
2. Inspect changed files and generated handoff artifacts before editing.
3. Compare changes against the original bounded task/spec.
4. Run the smallest relevant targeted tests/compile checks first.
5. If only a narrow gap remains, patch it directly or dispatch a narrow fix worker; do not restart the entire worker task.
6. If the wrapper or task-routing command may have used the wrong task file, verify the wrapper actually honors the override mechanism before re-running. If a wrong-task run occurred, restore any touched tracked files, delete or quarantine accidental rolling archives/results that would confuse the audit trail, then write the intended rolling task explicitly and re-run through the normal wrapper.
7. Run local verification yourself after any worker or manual fix:
   - targeted unit tests for touched behavior
   - compile/syntax checks for touched modules
   - project validation/safety command when the repo defines one
   - diff hygiene (`git diff --check` or equivalent)
8. Add a focused review pass for spec/safety/quality if the repo uses multi-agent review.
9. Record the outcome in the repo's durable handoff files, distinguishing:
   - worker command and status
   - partial changes accepted
   - Hermes/manual narrow fixes
   - validation commands and results
   - blocked follow-ups

## Side-effect-sensitive constraints

For repos that can publish, upload, schedule, alter credentials, or touch user runtime data, the recovery review should explicitly forbid broad runtime actions. Allowed actions should be limited to reading files, inspecting diffs, static checks, targeted tests, compile checks, and the repo's safe validate command unless the user separately authorized a gate.

## What not to preserve

Do not encode one run's timeout as a durable claim that the CLI tool is unreliable. Preserve the recovery workflow, not the transient failure.