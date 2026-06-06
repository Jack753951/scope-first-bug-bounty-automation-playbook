> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# API-key-aware Claude Code routing

Use this reference when the user wants model/token usage balanced without consuming an API key reserved for another production path.

## Durable lesson

Claude Code CLI may be authenticated through Claude Pro/Max OAuth rather than `ANTHROPIC_API_KEY`. In that setup, implementation-heavy build work can be routed through Claude Code while keeping the Anthropic API key available for the user-designated application workload, such as YouTube script generation.

## Recommended sequence

1. Verify Claude Code auth mode without exposing secrets:
   - `claude --version`
   - `claude auth status --text`
2. If it reports a Pro/Max/OAuth login, prefer Claude Code print mode for bounded build work:
   - refactors
   - test scaffolds
   - renderer/layout polish
   - local fixtures
   - handoff/documentation updates paired with code
3. Keep Hermes as orchestrator and verifier:
   - write a bounded task file such as `handoff/claude_code_task.md`
   - run Claude Code via the project wrapper or direct `claude -p "$(cat task.md)" ... < /dev/null`
   - inspect actual file changes
   - rerun local tests, compile checks, validate scripts, diff checks, and lock-file checks
4. Use Codex/GPT mainly for:
   - independent engineering risk review
   - OpenAI-specific reasoning
   - narrow fixes
   - fallback implementation when Claude Code is unavailable, unauthenticated, or repeatedly max-turns
5. Record project-specific routing rules in project context/handoff files so future sessions preserve the intended split.

## Pitfalls

- Do not equate "use Claude more" with "switch Hermes global/scheduled model to Anthropic API" when the user explicitly wants the API key preserved.
- Do not trust Claude Code self-reports; verify files and commands locally.
- Do not keep rerunning a monolithic Claude Code task after `Error: Reached max turns`; inspect partial changes and continue with a narrower task.
- Do not print tokens, `.env`, API keys, or auth files while checking auth mode.
- Do not expect Hermes `insights` to fully reflect Claude Code Pro/OAuth work. Record the implementation worker route in project handoff/accepted-changes files when usage balance matters.

## Cybersecurity / gated-workspace routing

For repos with explicit authorization or safety gates, Claude Code is a build worker, not the security gate:

- Good Claude Code tasks: offline/local implementation phases, refactors, schema/validator work, fixture/test scaffolding, docs paired with code, and read-only implementation/security review packets.
- Keep Hermes responsible for: scope/authorization decisions, target-touching approval, final diff inspection, local validation, and acceptance notes.
- Include explicit forbidden changes in Claude Code prompts: no live scans, no target interaction, no new network clients, no `config/scope.txt` edits, no credentials/loot/secrets, no scheduler/deploy/billing changes unless the user explicitly approves.
- Prefer phase-sized prompts such as `schema + tests`, `validator + fixtures`, `docs`, then `integration`, rather than one broad "finish the phase" prompt.
- After Claude Code returns, run independent verification before reporting success: `git status`, focused diff review, relevant tests/compilation, project review wrapper if present, and sensitive-file checks.

## Example routing statement for project docs

`ANTHROPIC_API_KEY` is reserved primarily for application script generation. For programming/build work, prefer bounded Claude Code CLI tasks when Claude Code is authenticated via Pro/OAuth; reserve Codex/GPT for focused independent risk review, narrow fixes, OpenAI-specific reasoning, or fallback implementation. Hermes remains responsible for local verification.
