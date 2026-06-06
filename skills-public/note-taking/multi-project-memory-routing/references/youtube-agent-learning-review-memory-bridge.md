> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent learning review memory bridge

Use when coordinating a project where Hermes has private/persistent memory but external worker agents (Claude Code, Codex, other CLI agents) must participate in long-horizon content learning or review.

## Durable lesson

External coding/review agents do not automatically receive Hermes private memory, user profile, or external Obsidian vault context. For non-trivial multi-agent project work, create or update explicit repo-local bridge files before delegating.

Recommended bridge set:

- Project orchestrator context: `.hermes.md` or equivalent.
- Claude Code context: `CLAUDE.md`.
- Codex-style context: `AGENTS.md`.
- Repo handoff index: `handoff/active_strategy_queue.md`.
- Memory governance: `handoff/memory_governance.md`.
- Learning/review destination docs: e.g. `handoff/learning/README.md`.
- Repo-local Obsidian mirror/index: e.g. `notes/obsidian_projects/Projects/<ProjectName>/00_Index.md` plus focused long-term decision notes.

## Multi-agent learning review pattern

For content automation systems, put multi-party review after production/data collection, not inside the production path:

```text
production loop -> artifacts/analytics -> evidence packet -> role-separated reviewers -> Hermes synthesis -> promoted/mature learning -> future generation hints
```

Reviewer roles should be separated by responsibility, not duplicated as generic opinions:

1. Creative/channel-fit reviewer: hook, tone, retention mechanics, payoff, audience fit.
2. Technical artifact QA reviewer: media facts, readability, timing, audio/subtitle/video evidence.
3. Learning/strategy integrity reviewer: data maturity, overfitting risk, distribution/no-signal vs creative failure, promotion eligibility.
4. Engineering/pipeline reviewer: optional only when evidence shows systemic pipeline problems.

## Boundary to preserve

A learning review layer is not a new safety gate and should not slow or block an approved daily production loop unless the user explicitly asks for that. Raw reviewer opinions should not directly mutate production prompts/templates/schedulers. Only Hermes-synthesized mature/promoted learning should feed future generation.

Make the boundary explicit in the bridge docs and scheduled-job prompt:

- learning-only / review-only;
- no create/remake/render/upload/publish/schedule unless separately authorized;
- no OAuth/token/client_secret/default-privacy/channel/scheduler/runtime-data mutation;
- 0-24h metrics are health/observe only, not prompt-rule evidence.

## Verification

After implementing this bridge, verify:

- external-agent bridge files exist and point to current goals/technical notes;
- evidence packet builder includes those context files and repo-local Obsidian notes;
- scheduled learning job explicitly delegates separate reviewer roles;
- output paths are durable under `handoff/learning/` or equivalent;
- project validation confirms no privacy/scheduler/runtime mutation.