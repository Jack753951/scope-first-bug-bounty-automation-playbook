> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent: Memory, Obsidian, GitHub Support Layer

Use this reference when orchestrating `youtubestrict/youtube_agent` work with Claude Code, Hermes, Codex/GPT, Obsidian, and GitHub.

## Durable support layers

- Repo handoff files are the engineering source of truth for implementation results, validation, safety boundaries, and accepted changes.
- Obsidian stores longer-lived strategy, channel direction, content rules, experiment history, and decision context.
- GitHub supports branch/PR/CI/review workflow, but does not replace Hermes local verification or the repo handoff contract.
- Hermes memory should keep only compact routing reminders; detailed session outcomes belong in repo handoff and, when strategic, Obsidian.

## Workflow pattern

1. Before coding, inspect current handoff/context files and the working tree. The repo often has many active tracked/untracked artifacts; avoid broad cleanup or formatting unrelated to the current rung.
2. Split work into small bounded rungs suitable for Claude Code print-mode implementation.
3. Route implementation-heavy build/refactor/test-scaffold work to Claude Code CLI when Pro/OAuth is available.
4. If Claude Code hits max-turns, inspect actual workspace changes before judging failure; useful partials often land.
5. Hermes reruns local validation, visual QA where applicable, and safety gates before recording acceptance.
6. Use Codex/GPT for focused engineering risk review, OpenAI-specific reasoning, narrow fixes, or fallback implementation.
7. Update repo handoff for material decisions/results; update Obsidian for strategic decisions/content rules; use GitHub PR/CI/review when the work should leave the local handoff stage.

## Safety boundary reminder

Unless the user explicitly approves it, do not upload/publish videos, change scheduler behavior, edit OAuth/token/client-secret files, change default privacy, activate disabled channels, or delete runtime user data.