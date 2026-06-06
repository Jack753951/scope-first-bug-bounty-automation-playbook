> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Worker Prompt Templates — Claude Max + GPT Pro/Codex

Purpose: use Claude/Cowork/Codex where they increase capability, without reintroducing review-tier ceremony. Workers are quality amplifiers; Hermes remains coordinator and hard-stop gate.

## Global safety preamble

```text
You are working in the Cybersec Lab repository.
Follow .hermes.md and docs/policy/*.md hard stops.
Do not run live-target scans, exploits, brute force, callbacks, fuzzing, DAST, OAST, tunnels, or target-touching automation unless the task explicitly says the operator approved that exact boundary.
Do not modify config/scope.txt, credentials, OAuth/session files, loot/, scheduler/deployment settings, or publish/report outputs unless explicitly requested by the operator.
Do not store or print secrets, tokens, cookies, hashes, OTPs, phone numbers, verification links, loot, customer data, or client-sensitive data.
Scanner/module output is triage-only until verified.
Favor capability growth: small runnable scripts, focused tests, compact handoff, useful preserved hypotheses.
```

## Claude Code / Cowork — tactical, architecture, safety, evidence review

Use when long-context reasoning, attacker-path breadth, architecture fit, or evidence criticism will improve the result.

```text
Read .hermes.md plus current navigation/queue/artifact index and the relevant task files.

Task:
Review <DESIGN_OR_DIFF_OR_PHASE> for capability growth and concrete hard-stop blockers.
Do not classify into review tiers. Do not require multi-agent ceremony. Separate real blockers from advisory improvements.
Use OSS/source comparison only if it materially improves the design; do not run scanners or contact targets.

Constraints:
- Offline/read-only review unless explicitly asked to edit.
- Do not run target-touching commands.
- Do not modify secrets, scope, credentials, scheduler/deployment, or report-submission artifacts.

Output format:
Reviewer route/tool:
Context read:
Concrete blockers:
Advisory improvements:
Preserved useful hypotheses / dissent:
Architecture/capability fit:
Safety/authorization assessment:
Validation or evidence gaps:
Suggested next action:
```

Suggested command:

```bash
claude -p "<PROMPT>" --allowedTools "Read" --max-turns 5
```

## Codex — narrow implementation or deterministic review

Use for concrete diffs, scripts, tests, schemas, fixtures, validation helpers, deterministic review, and focused fixes.

```text
Read .hermes.md and the task-specific handoff file.

Task:
Implement or review <NARROW_TASK> only.
Proceed unless a concrete hard-stop blocker appears. If a blocker appears, name it precisely instead of invoking generic caution.

Scope:
- Allowed files/areas: <ALLOWLIST>
- Forbidden unless explicitly requested: config/scope.txt, credentials, OAuth/session files, loot/, logs containing secrets, deployment/scheduler settings, report submission artifacts.
- Do not run live-target scans, exploits, fuzzing, callbacks, brute force, DAST/OAST, tunnels, or target-touching automation.

Validation:
- Run syntax/compile checks for touched Python/Bash/JSON/YAML files.
- Run focused unit/dry-run tests for changed behavior.
- If scope/safety logic changes, prove unauthorized targets fail closed using safe local/offline tests.
- Summarize files changed, validation, hard stops preserved, and follow-ups.
```

Suggested command:

```bash
codex exec --sandbox workspace-write "<PROMPT>"
```

## Hermes final arbitration checklist

After worker completion or direct Hermes edits, verify:

- Hard stops were not crossed.
- Git diff matches task scope.
- No secrets or sensitive artifacts were introduced.
- No active target interaction occurred unless explicitly authorized.
- Focused syntax/tests/review wrapper passed where relevant.
- `.agent.lock` is clear.
- Handoff/current navigation/Obsidian are updated only when durable route changed.
- Reviewer objections are treated as blockers only when they identify concrete authorization, safety, validation, or data/capability-loss issues.

## Program-policy runtime integration reminder

For runtime integrations, still keep these hard safety properties:

```text
- safe_target remains first gate
- program policy is second deny gate
- fresh decision per target/stage
- no cached allow decisions
- dry-run policy mode cannot authorize live target-touching execution
```

Implement with focused tests and Hermes verification. Independent review is useful but not mandatory unless a concrete hard-stop boundary is near.
