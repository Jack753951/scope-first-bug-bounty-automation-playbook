> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cross-Project Multi-Agent Workflow Transfer

This reference captures a reusable lesson from adapting the cybersec lab's Hermes + Codex + Claude/Cowork workflow to a YouTube Shorts automation project. Use it when the operator asks to "learn from" a mature workspace's agent collaboration style and apply it to another repository.

## Transferable Core

The reusable pattern is class-level and not cybersecurity-specific:

```text
Hermes = coordinator / safety gate / scheduler / memory keeper / final verifier
Claude / Claude Code = strategy, long-context synthesis, creative/product/security review, independent reviewer
Codex = narrow implementation, tests, fixtures, validators, review-blocker fixes
Project handoff files = durable memory and audit trail
Human owner = final approval for high-risk actions
```

## Adapt Safety Gates To The Destination Domain

Do not copy cybersec gates literally. Translate them into the destination project's irreversible or high-risk actions.

Examples:

- Cybersecurity: live scans, exploit attempts, fuzzing, callbacks, scope-file edits.
- YouTube/publishing: public upload, scheduler changes, OAuth/token handling, active channel activation, privacy escalation, generated media deletion, copying competitor assets.
- Finance: live trades, leverage changes, broker API actions, allocation changes beyond approved ranges.
- Infrastructure: production deploy, DNS/billing changes, data deletion, secret rotation.

## Destination Repo Artifacts To Create Or Update

1. Add or update a repo-local policy document, e.g. `handoff/multi_agent_collaboration_policy.md`.
2. Reference it from `.hermes.md` and the repo's workflow doc so future agents load it automatically.
3. Record the accepted process change in `handoff/accepted_changes.md`.
4. If the process should survive across sessions, save only a compact durable memory pointing to the policy file.

## Policy Sections That Should Be Present

- Core operating model and role split.
- Why the pattern matters in the destination domain.
- Default sustained loop: `strategy/spec -> constrained implementation -> independent review -> Hermes verification -> accepted history`.
- Workstream routing: Claude-first vs Codex-first vs Hermes-final authority.
- Domain-specific safety gates that require explicit user approval.
- Handoff files and their purpose.
- When independent Claude/Cowork review is required.
- Contracts-before-runtime or spec-before-activation sequencing.
- Periodic whole-project review process and output layout.
- Memory / durable record process.
- Final acceptance checklist.

## Periodic Review Transfer

A mature workspace should not only review patches. Add or verify a recurring offline whole-project review:

1. Hermes builds a safe dated snapshot under `handoff/periodic_reviews/YYYY-MM-DD/`.
2. Codex reviews engineering/system reliability when available.
3. Claude/Cowork reviews strategy, product fit, safety governance, and roadmap sequencing.
4. Hermes synthesizes shared recommendations, disagreements, next actions, defer/avoid items, safety notes, and suggested phase order.

The scheduled job must be restricted to local/offline review artifacts. If a reviewer CLI is unavailable, record the blocker as a review gap rather than taking unsafe substitute actions.

## Memory Layer Transfer

Use four memory layers:

1. Project context/policy files for stable operating rules.
2. Handoff files for project-local working memory and validation outcomes.
3. Persistent Hermes memory for compact, stable cross-session facts only.
4. Obsidian or external notes for settled long-form strategy and evergreen lessons.

Avoid putting PR numbers, commit SHAs, one-off phase completions, file counts, or transient generated artifact paths into persistent memory.

## Pitfalls

- Do not create a narrow skill named after the destination project or today's phase when an umbrella orchestration skill can hold the transferable pattern.
- Do not copy source-domain safety language without translating it to the target domain's real risks.
- Do not let documentation-only adoption imply public activation, deployment, publishing, or live operations.
- Do not rely on chat history as the only record; the next agent should find the policy from `.hermes.md` or the workflow docs.
