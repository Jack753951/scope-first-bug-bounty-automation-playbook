> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Hermes project wrapper routing for Claude Code build-first workflows

Use this reference when a Hermes-managed project has local PowerShell/Bash wrappers for worker orchestration and the user wants API-provider token usage rebalanced toward Claude Code Pro/OAuth.

## Target pattern

A practical target mix is not enforced by model config alone. Implement it in routing defaults:

- GPT/Codex/Hermes API-provider work: about 45-60% for orchestration, local verification, focused risk review, and fallback.
- Claude Code CLI via Pro/OAuth: about 30-45% for implementation-heavy build/refactor/test tasks.
- Anthropic API key: about 5-15%, reserved for the user-designated production path such as YouTube script generation.

Because Claude Code Pro/OAuth may not appear fully in `hermes insights`, track both API-token reports and handoff/worker logs.

## Wrapper changes that worked

For a project wrapper like `run_hermes_worker.ps1`:

1. Add explicit Claude Code budget/tool parameters rather than hard-coding low limits:
   - `ClaudeMaxTurns = 25` for contained implementation phases.
   - `ClaudeAllowedTools = "Read,Edit,Write,Bash,Grep,Glob"` when the worker is expected to run validation.
2. Make dry-run output show the exact `claude -p` command shape so routing is auditable.
3. Keep Codex/GPT worker support as an explicit fallback path.

For a project pipeline like `run_hermes_pipeline.ps1`:

1. Make `-Mode full` prefer Claude Code for build/implementation when that is the project's current routing policy.
2. Add an explicit override such as `-ImplementationWorker codex` for Codex/GPT fallback or focused engineering review.
3. Record routing fields in the generated run report, for example:
   - `ClaudeCodeDefault`
   - `ImplementationWorker`
   - `ClaudeMaxTurns`
   - `DryRun`
4. Keep Hermes or Codex/GPT preflight/review separate from Claude Code implementation so final verification is independent.

## Verification checklist

Run dry-runs before real phase work:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_hermes_worker.ps1' -Worker claude-code -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File './run_hermes_pipeline.ps1' -Mode full -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File './run_hermes_pipeline.ps1' -Mode full -ImplementationWorker codex -DryRun
```

Then run local safety checks appropriate to the project, commonly:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate
git diff --check
test ! -e .agent.lock
```

## Handoff records to create

Create or update a concise project file such as `handoff/ai_usage_routing_status.md` with:

- target mix and rationale;
- API key reservation rule;
- Claude Code build-first rule;
- Codex/GPT fallback/review rule;
- note that `hermes insights` may not include all Claude Code Pro/OAuth usage;
- unchanged safety boundaries.

Update the general accepted-changes or decision log so future agents know the wrapper behavior was intentional.

## Pitfalls

- Do not solve token balancing by moving generic scheduled jobs onto the Anthropic API provider when the user explicitly reserved that key for script/content generation.
- Do not hide the fallback path; users need a copy-pasteable override when Claude Code is unauthenticated or max-turns.
- If one pipeline invokes the same `claude_code_task.md` for both strategy and implementation phases, note it as a follow-up: ideally split task files by role to avoid ambiguity.
- Claude Code self-report is not final verification. Hermes must re-run the dry-runs, validate scripts, diff checks, and lock-file checks itself.
