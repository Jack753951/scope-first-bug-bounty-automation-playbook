> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cross-project memory governance pattern

Use this when a user has multiple projects sharing one Hermes profile and wants durable project memory without cross-project contamination.

## Layer authority order

When facts conflict, prefer:

1. Current explicit user instruction.
2. Live project files/config/validation output.
3. Repo handoff files for accepted engineering state.
4. Active Obsidian project notes for strategy, research, decisions, experiments, and review conclusions.
5. Hermes durable memory for compact cross-project preferences, safety rules, and pointers.
6. session_search only as recall; verify before acting.

## Destination rules

- Hermes memory: user-wide preferences, stable cross-project rules, and short pointers. Do not store detailed project state, run logs, PR/issue/commit IDs, or one-off validation results.
- Repo handoff: engineering truth — accepted changes, validation, worker outputs, blocked follow-ups, safety gates tied to code/config/runtime.
- Obsidian project namespace: long-term strategy, research, decision rationale, experiments, periodic review synthesis, and content/workflow rules.
- Shared Obsidian namespace: cross-project governance/templates only; never single-project state.
- session_search: discovery lead only; verify against files/notes before acting.

## Recommended Obsidian note metadata

```markdown
Status: active | superseded | rejected | experiment | reference
Source: User | Hermes | Claude | Codex | Mixed
Date: YYYY-MM-DD
Repo truth: path/to/handoff-or-code-file, if applicable
```

## Namespace pattern

Prefer one vault with project namespaces unless hard isolation is needed:

```text
Shared/
Projects/YouTubeAgent/
Projects/Cybersec Lab/
Projects/InvestmentAutomation/
```

Each project should maintain an index note linking only to active/current guidance. Mark old notes `superseded`, `rejected`, or `reference`; do not silently leave stale strategy as if active.

## Periodic review checklist

Recurring project-health reviews should check:

- Hermes memory remains compact and cross-project safe.
- Project index points to active decisions.
- Repo handoff matches implementation reality.
- Obsidian strategy notes match accepted direction.
- Superseded notes are clearly marked.
- No secrets or credential values were copied into memory layers.
- session_search findings were verified before being treated as truth.
