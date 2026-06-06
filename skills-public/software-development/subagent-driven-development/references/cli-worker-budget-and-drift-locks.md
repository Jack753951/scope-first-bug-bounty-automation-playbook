> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# CLI Worker Budgeting and Symmetric Drift-Locks

Use this note when an external implementation worker such as Claude Code, Codex CLI, OpenCode, or a repo wrapper is doing a fixture/test/handoff-heavy slice with independent review artifacts.

## Context/turn budget discipline

- Keep the repo or skill default conservative. Do not raise global defaults just because one rich slice hit a max-turn or timeout boundary.
- For one rich offline slice, prefer a temporary per-run override (for example a max-turn or max-steps env var) and record the exact command/status in the handoff artifact.
- If the same class of slice repeatedly needs more budget, first split the work into smaller rungs: direction review, fixture/schema implementation, tests, handoff update, independent review, and closeout.
- Treat `error_max_turns`, timeout, or missing final prose as a partial-completion state, not an implementation failure. Inspect changed files, run targeted tests, then dispatch or perform a narrow follow-up review/fix.
- Record visible model/runtime details when available. If a wrapper does not expose an exact model, state that limitation rather than inventing one.

## Symmetric drift-lock pattern

When two artifacts must stay vocabulary-compatible (for example a fixture's allowed statuses/gap codes and a reviewer catalog/report schema):

1. Pick one canonical source of truth or intentionally assert exact set equality between peers.
2. Test both directions, not just "new catalog values appear in old tests". A future addition to the old fixture must fail if the catalog is not updated too.
3. Prefer static parsing for constants from adjacent runtime files when importing them would create directories, load credentials, start schedulers, or touch production/runtime state.
4. For Python constants, a small stdlib `ast` parser can extract literal assignments such as `ALLOWED_STATUSES = {...}` without executing the module.
5. Add a negative or equality assertion that fails loudly on unknown, missing, or extra vocabulary entries.
6. Keep the drift-lock test local/offline; it should not activate scanners, network calls, schedulers, upload/publish paths, OAuth, or secrets.

## Review signal

Independent reviewers should treat one-way vocabulary checks as incomplete if the task claims to lock two artifacts together. A valid pass requires either a declared single source of truth or explicit bidirectional/equality coverage.
