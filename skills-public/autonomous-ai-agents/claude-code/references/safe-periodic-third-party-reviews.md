> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Safe periodic third-party reviews with Claude Code

Use this pattern when Hermes is coordinating recurring/offline reviews and the user wants Claude/Cowork used aggressively for strategy, creative, architecture, or quality review while Hermes remains the safety gate.

## Trigger

- Scheduled or repeat project-health/strategy reviews.
- Review should be independent of the main agent but must not mutate production state.
- The project already has a safe packet/snapshot builder or can generate one.

## Pattern

1. Build a safe review packet first.
   - Include project snapshot, recent validation notes, relevant handoff docs, and explicit safety boundaries.
   - Exclude secrets, OAuth/token files, runtime user data, upload credentials, and raw private state.
2. Invoke Claude Code in print mode as the third-party reviewer.
   - Prefer `claude -p` with piped/safe packet text or a narrowly scoped task file.
   - Use read-only or recommendation-only framing when no implementation is desired.
   - Add `--max-turns` and a timeout so scheduled jobs cannot run indefinitely.
3. Write Claude's output to a review artifact, not directly into production config.
   - Example destinations: `handoff/periodic_reviews/YYYY-MM-DD/claude_cowork_strategy_review.md` or equivalent.
4. Hermes synthesizes the review separately.
   - Record agreements, disagreements/tradeoffs, immediate actions, deferrals, and safety notes.
   - Keep the synthesis recommendation-only unless the user explicitly asked for implementation.
5. Only route implementation after the review loop is closed.
   - Use Codex/engineering review or the project's implementation workflow before code/config changes.

## Prompt ingredients

- State that Claude is an independent reviewer, not the actor executing changes.
- Ask for blocking defects plus third-party recommendations on architecture, extensibility, maintainability, safety, testing, roadmap fit, and creative/channel strategy where relevant.
- Explicitly forbid upload/publish, credential/token access, scheduler mutation, privacy-default changes, competitor asset copying, and production config mutation unless the user separately approved it.
- Require output as a markdown report suitable for Hermes synthesis.

## Verification checklist

- Claude Code is installed and authenticated in the execution context (`claude --version`, `claude auth status --text`).
- The review artifact exists and contains substantive findings.
- Hermes synthesis exists and distinguishes accepted actions from suggestions.
- No upload/generation/scheduler/OAuth/token/runtime-data/privacy-default changes occurred during the review.
- Local repo checks such as `git diff --check` and project lock-file absence are verified when relevant.

## Pitfalls

- Do not treat a green wrapper/doctor check as proof Claude Code is authenticated; verify auth or inspect the worker report for `Not logged in`.
- Do not let scheduled reviews read broad repo contents if a safe packet builder exists; feed the packet instead.
- Do not collapse Claude review and Hermes synthesis into one artifact. Keeping them separate preserves independent-review value and makes safety auditing easier.
- Do not let a disabled/internal experiment consume endless phase work without a user go/no-go gate; surface decision artifacts before more implementation.