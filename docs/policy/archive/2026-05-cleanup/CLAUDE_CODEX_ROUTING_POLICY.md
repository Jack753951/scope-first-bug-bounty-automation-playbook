> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude/Codex Routing Policy

This note captures the default worker routing policy for the cybersec lab.

## Roles

- Hermes: coordinator, authorization/scope gate, verifier, memory/Obsidian recorder.
- Claude Max / Claude Code: deep reasoning, architecture, security review, long-context synthesis, post-Codex independent review.
- GPT Pro / Codex: concrete implementation, tests, refactors, scripts, schemas, fixtures, review-blocker fixes.
- Obsidian: durable knowledge, strategy, decisions, and weekly review notes.

## Default workflow

For non-trivial cybersec changes:

1. Hermes classifies workstream and checks scope/safety.
2. Claude/Cowork proposes/reviews strategy when reasoning-heavy.
3. Codex implements narrow, testable patches.
4. Hermes validates locally.
5. Claude/Cowork independently reviews Codex output.
6. Codex fixes blocking issues if needed.
7. Hermes verifies, updates handoff, and records durable summary.

## Templates

Use worker prompt templates here:

```text
handoff/WORKER_PROMPT_TEMPLATES.md
```

## Safety boundaries

- No target-touching automation without authorization/scope.
- No secrets or loot in worker prompts, repo, or Obsidian.
- No production-side changes without explicit operator approval.
- Scanner output is triage-only until manually verified.
