> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersecurity workspace: safe Claude Code worker routing

Use this reference when a Hermes-controlled cybersecurity repo wants to preserve `ANTHROPIC_API_KEY` capacity while still using Claude-family coding ability.

## Routing pattern

- Keep Hermes/GPT as the central orchestrator and verifier.
- Route bounded implementation/build/test work to Claude Code CLI when `claude auth status --text` shows Pro/Max/OAuth login.
- Reserve Anthropic API-provider usage for high-value design/review, user-designated projects, or explicitly approved exceptions.
- Keep Codex/GPT available for surgical fallback and deterministic repairs.
- If another project depends on `ANTHROPIC_API_KEY`, make API-backed Claude the rare path, not the review default.

Recommended future-only worker mix for this class of workspace:

- Normal week: Hermes/GPT 50-60%, Claude Code Pro/OAuth 30-40%, Codex/GPT fallback 5-15%, API-backed Claude/Cowork 0-3% preferred with 5% ceiling unless explicitly approved.
- Code-heavy week: Hermes/GPT 35-45%, Claude Code Pro/OAuth 45-55%, Codex/GPT fallback 5-15%, API-backed Claude/Cowork 0-3% preferred with 5% ceiling unless explicitly approved.
- Review-heavy week: Hermes/GPT 45-55%, Claude Code Pro/OAuth 20-35%, Codex/GPT 5-15%, API-backed Claude/Cowork 0-10% only when the safety/architecture/report value justifies spending scarce API key capacity.

Preference order when conserving Anthropic API key capacity:

1. Claude Code Pro/OAuth for implementation-heavy coding and bounded read-only review.
2. Hermes/GPT or Codex/GPT for orchestration, quick fixes, deterministic patches, and fallback.
3. API-backed Claude/Cowork only for high-value T3+ direction/safety/architecture/report review when the above routes are not adequate, or when the user explicitly approves API use.

## Safety contract for cybersec repos

A Claude Code implementation prompt should explicitly forbid:

- live scans, exploit attempts, fuzzing, callbacks, brute force, HTTP/socket clients, or target-touching automation
- edits to `config/scope.txt`, `loot/`, credentials, `.env`, tokens, private keys, scheduler, deployment, billing, OAuth/auth settings
- scanner/module runtime wiring unless that is the explicitly reviewed milestone
- promotion of templates to schemas/registries without a separate review gate

The prompt should state:

- implementation worker: Claude Code Pro/OAuth
- verifier: Hermes
- fallback: Codex/GPT only for surgical fixes if needed
- boundary: offline/local only, if applicable
- expected validation commands

## Verification pattern

Do not accept Claude Code self-reporting as completion. After the worker exits:

1. Inspect `git status` and expected files.
2. Read or skim critical new files.
3. Run focused tests and static checks locally.
4. Run the repo review command when available.
5. Update handoff/accepted changes with the worker route and verification result.

If Claude Code returns `error_max_turns`, treat it as partial progress, not failure/no-op:

- inspect what landed
- run targeted tests
- add missing tests or small fixes locally if faster, especially in safety-sensitive repos where verifier-side tests are part of acceptance
- rerun Claude Code only with a narrower follow-up task
- record the worker exit (`terminal_reason`, `subtype`, run log path) separately from the final verified project result

A successful routing pilot pattern is: Claude Code produces the main offline/local implementation, Hermes notices missing tests or handoff details after max-turn exit, Hermes adds focused tests/fixtures, then Hermes runs py_compile, focused tests, full relevant unittest discovery, diff checks, and repo review before acceptance.

For CTF workflow-calibration work, keep trial artifacts under `tests/fixtures/`, use non-binding templates first, and add only weak read-only linters before schema/runtime promotion. See `references/cybersec-ctf-offline-metadata-trial.md` for the P2.17/P2.18 pattern.

## Usage visibility

Claude Code plan/account remaining usage usually requires interactive Claude Code `/usage` or account UI. Print mode slash-command probes may not show plan limits. However `claude -p ... --output-format json` returns per-run `usage`, `modelUsage`, `total_cost_usd`, `subtype`, and `terminal_reason`; record those run-level facts when tracking project worker mix.
