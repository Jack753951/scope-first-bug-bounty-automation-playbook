> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Project-as-capability-library routing

Use when the user corrects a project framing from human-readable notes / behavioral narrative toward an agent-owned, growing capability substrate.

## Signal

The user says a project should be treated as a dedicated, growing capability library for Hermes/agents, not as a human-facing narrative or presentation layer.

## Routing

1. Save only a compact global/user preference if it will affect future sessions.
2. Put the operational interpretation in the project-local authority layer: `.hermes.md`, repo handoff policy, active strategy queue, or equivalent.
3. Prefer reusable, executable substrate:
   - scripts and deterministic probes;
   - validation recipes;
   - machine-readable queues/contracts;
   - evidence-state schemas;
   - redaction/scope gates;
   - worker prompts and handoff templates;
   - compact indexes pointing to active artifacts.
4. Avoid adding long prose that only explains human behavior or narrates what happened.
5. If documentation is needed, make it agent-actionable: authority, inputs, outputs, gates, next action, verification command, and artifact path.
6. For multi-agent projects, make worker context explicit. Do not assume Claude/Codex/Cowork inherit Hermes memory or Obsidian; put required reads and handoff paths in the worker task.
7. Keep sensitive or project-specific details out of global memory and class-level skills. Use repo-local ignored storage, sanitized handoff summaries, or the project Obsidian namespace as appropriate.

## Skill-library consequence

When reviewing the skill library after this kind of correction, do not create a narrow skill named after the project/session. Update the umbrella skill that governs routing/orchestration, and add only class-level references like this one.

## Anti-patterns

- Writing a polished human-readable retrospective instead of adding runnable capability.
- Saving detailed project state to Hermes durable memory because it is important.
- Treating "capability library" as permission to store secrets, raw targets, loot, private scope, or unredacted evidence globally.
- Asking the user to choose next steps when the repo authority layers can be inspected and a safe checkpoint can be advanced.
