> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Subscription-aware worker routing for cybersec workspaces

Use this when the operator has both Claude Code MAX/OAuth and GPT Pro/Codex available and wants to maximize value without wasting quota. In current handoffs and summaries for this user's workspace, use the label `Claude Code MAX/OAuth`; avoid `Pro/OAuth` except when quoting immutable historical logs.

## Core split

- Hermes: coordinator, authorization/scope gate, task router, local verifier, handoff/Obsidian recorder.
- Claude Code MAX/OAuth: deep reasoning, architecture/security review, long-context synthesis, post-implementation third-party review, weekly strategy/project-health review.
- GPT Pro / Codex: concrete implementation, tests, refactors, scripts, schemas, fixtures, and review-blocker fixes.
- Obsidian: durable decisions and strategy notes so the same reasoning is not repeated every session.

## Default cybersec workflow

For non-trivial changes, especially scope gates, recon automation, module/plugin execution, reporting, evidence, or runtime integrations:

1. Hermes classifies the workstream and enforces scope/safety.
2. Claude/Cowork handles reasoning-heavy design/proposal or pre-implementation review when needed.
3. Codex implements one narrow, testable patch.
4. Hermes validates locally with safe/offline checks.
5. Claude/Cowork independently reviews Codex output for blockers and strategic fit.
6. Codex fixes blocking review items.
7. Hermes verifies, updates handoff state, and records durable summaries in Obsidian when meaningful.

Skip the independent review only for trivial documentation-only edits or explicit operator instruction.

## Quota/value rules

- Do not spend Claude on low-value mechanical edits or simple file changes.
- Do not spend Codex on vague strategy discussion.
- Split large work into reviewable phases; one task should produce concrete artifacts or a clear review verdict.
- Prefer local tools for deterministic checks, file inspection, and simple validation.
- Use Obsidian/handoff files to avoid repeatedly re-deriving settled decisions.
- If GPT/OpenAI quota is constrained, route more reviews, synthesis, and strategy to Claude Code.
- If Claude quota is constrained, keep Claude for final/high-risk reviews and let Codex handle small implementation/test patches.

## Standard Claude review output

```text
Verdict: ACCEPT / ROUTE_BACK
Blocking issues:
Non-blocking recommendations:
Architecture fit:
Safety concerns:
Testing gaps:
Next phase recommendation:
Suggested Codex task if fixes are needed:
```

## Standard Codex task framing

```text
Read .hermes.md and the task-specific handoff file.
Implement <NARROW_TASK> only.
Allowed files/areas: <ALLOWLIST>.
Forbidden: config/scope.txt, credentials, OAuth/session files, loot/, secret logs, deployment/scheduler settings unless explicitly requested.
Do not run target-touching automation.
Run syntax/compile checks and relevant offline tests.
Update handoff/codex_review.md with files changed, validation, and remaining risks.
```

## Repo artifact pattern

For durable project adoption, create a repo-local handoff template such as:

- `handoff/WORKER_PROMPT_TEMPLATES.md` — copy/paste prompts for Claude architecture review, Codex implementation, Claude post-Codex review, and Hermes final arbitration.
- `handoff/CLAUDE_CODEX_ROUTING_POLICY.md` — short policy summary for the workspace.
- Obsidian decision note — e.g. `Projects/Cybersec Lab/04_Decisions/Claude Max GPT Pro Usage Policy.md`.

These are policy/templates, not session logs; they should not include transient PR numbers, target details, secrets, or one-off task status.
