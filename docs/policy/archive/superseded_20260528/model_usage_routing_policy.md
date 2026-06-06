> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Model Usage Routing Policy

Date: 2026-05-18
Status: Active project routing policy
Scope: cybersec lab / hacking workspace

## Purpose

Preserve the user's `ANTHROPIC_API_KEY` capacity for other projects while still benefiting from Claude-quality coding and review. The project should route suitable coding/build work to Claude Code CLI authenticated through Claude Pro/OAuth, not to Hermes' Anthropic API provider.

## Default routing

| Work type | Primary route | Secondary / fallback | Notes |
|---|---|---|---|
| Hermes orchestration, scope gates, task decomposition, final verification | Hermes on gpt-5.5 / openai-codex | none | Hermes remains the security gate and acceptance authority. |
| Offline implementation-heavy coding | Claude Code CLI Pro/OAuth | Codex/GPT | Use for medium-sized feature slices, refactors, schema/tests, docs+tests. |
| Quick deterministic patches | Codex/GPT | Hermes direct patch | Prefer Codex/GPT for small edits where Claude Code startup/turn cost is unnecessary. |
| Architecture / safety / source-pattern review | Claude Code read-only review or Hermes/GPT where adequate | Claude/Cowork API only for high-value cases | Preserve `ANTHROPIC_API_KEY`; use API-backed Claude sparingly. |
| Kali / target-touching / CTF active service interaction | Hermes + Kali tools | Codex/GPT for local scripts | Must respect scope/safety gates. Claude Code should not independently perform target interaction. |
| Report impact/remediation/quality review | Claude Code read-only review or Hermes synthesis | Claude/Cowork API for high-value final review only | Prefer non-API routes unless report quality/safety risk justifies API use. |

## Claude Code implementation boundaries

Claude Code may be used for:

- offline/local feature implementation
- refactor with tests
- schema/template/validator creation
- fixture-based test harnesses
- read-only code/security review
- documentation updates tied to implementation

Claude Code must not independently perform:

- live scans, exploitation, fuzzing, brute force, callbacks, or target-touching automation
- changes to `config/scope.txt` unless the operator explicitly requests it
- access to `loot/`, secrets, credentials, tokens, `.env`, private keys, or proprietary wordlists
- deployment, publishing, scheduler mutation, billing, OAuth/token changes, or production-side operations
- destructive cleanup or silent overwrites of accepted history

## Required Claude Code prompt footer

Every Claude Code implementation prompt in this repo should include a boundary footer similar to:

```text
Safety and scope boundaries:
- Offline/local workspace changes only.
- Do not run live scans, exploit attempts, fuzzers, callbacks, or target-touching automation.
- Do not modify config/scope.txt, loot/, credentials, .env, tokens, private keys, scheduler/deployment/billing/OAuth settings.
- If a task appears to require target interaction or secrets, stop and write a blocking note instead.
- Update handoff artifacts with concrete findings and validation results.
```

## Verification contract

Claude Code self-report is not sufficient. Hermes must verify before accepting:

1. `git status --short` and targeted diff review
2. `git diff --check` for touched files
3. relevant tests / dry-runs
4. `./bin/hermes review` when repo workflow files or scripts changed
5. unauthorized target rejection tests when scope/recon logic changes
6. `handoff/accepted_changes.md` updated with worker route and verification result

## Target future mix

Track two metrics separately:

1. Hermes insights mix: only what Hermes records internally.
2. Project worker mix: task-route mix including Claude Code MAX/OAuth, which may not appear in Hermes insights.

Suggested steady-state project worker mix:

- Hermes/gpt-5.5 orchestration + verification: 45-60% of agent work
- Claude Code MAX/OAuth implementation/review: 25-40%
- Codex/GPT implementation/fallback: 10-25%
- Claude/Cowork API/key-backed review: 0-3% preferred, 5% ceiling without explicit user approval; reserved for high-value design/safety/report review only

For code-heavy weeks, Claude Code can temporarily rise to 40-55% of implementation work, while Hermes remains the verifier.

## Capacity note

The operator has Claude Max and GPT Pro, so Claude Code MAX/OAuth and GPT/Codex-backed workflows have relatively generous plan capacity. Prefer using those plan-backed routes for day-to-day project work. The scarcity constraint applies mainly to `ANTHROPIC_API_KEY`, which other projects depend on.

## API key conservation rule

`ANTHROPIC_API_KEY` is a scarce cross-project resource. Default to not using API-backed Claude for routine coding or routine review.

Use this preference order:

```text
1. Claude Code MAX/OAuth for implementation-heavy coding/review
2. Hermes/gpt-5.5 or Codex/GPT for orchestration, quick fixes, and fallback
3. Anthropic API-backed Claude/Cowork only when the review is high-value and not adequately covered by Claude Code/Hermes/GPT
```

API-backed Claude is allowed, but should be rare and justified in the handoff. If a task would push API-backed Claude beyond the 0-3% future target or the 5% ceiling, ask the operator first unless there is an explicit prior approval.

## Operational pattern for upcoming P2.17+

1. Hermes frames task and safety boundary.
2. Claude Code read-only review, Hermes/GPT review, or Claude/Cowork API review handles direction when architecture/safety impact is high or when focused dissent would improve quality; prefer non-API routes first and reserve API-backed Claude for high-value cases.
3. Claude Code implements the offline/local slice by default using `hermes claude-impl` / `handoff/claude_code_task.md`; the wrapper must emit `handoff/claude_code_result.md` and `handoff/claude_code_impl_run_<timestamp>.json` so usage/cost/turns are visible.
4. Hermes verifies locally.
5. Codex/GPT performs surgical fixes or fallback only if Claude Code is blocked, overkill for a tiny patch, or leaves a narrow verified gap.
6. Hermes records worker route in `handoff/accepted_changes.md`.
