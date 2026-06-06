> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Memory and Strategy Routing

Status: active
Source: Hermes, adapted from the YouTubeAgent memory-flow pattern
Date: 2026-05-19
Repo truth: `.hermes.md`, `handoff/accepted_changes.md`, `handoff/active_strategy_queue.md`, `handoff/periodic_reviews/review_template_v0.md`

## Purpose

This document defines where durable project knowledge belongs in the cybersec lab. It adopts the useful parts of the YouTubeAgent memory flow without copying YouTubeAgent project content.

The goal is to keep Hermes global memory small, keep repo-local engineering truth auditable, and keep long-term strategy navigable as the bug-bounty automation platform grows.

## 2026-05-21 Global memory compaction compatibility note

Hermes global memory is intentionally being compacted into a cross-project routing/index layer. Future hacking/Cybersec agents must not infer that project direction changed just because global memory contains fewer cybersec details.

## 2026-05-22 Workflow/process memory routing update

User preference: when the hacking/Cybersec Lab workflow or process changes, do not record it only in chat or Hermes global memory. Durable workflow/process decisions that should guide future Hermes/Codex/Cowork behavior must also be written into this repo's handoff layer and the Obsidian namespace `Projects/Cybersec Lab/`, with rationale and metadata where appropriate.

This applies to collaboration rules, growth-first review policy, safety gates, lab routing, evidence/report workflow, worker routing, memory governance, and other process changes that future agents need to follow. Keep exact sensitive target/evidence/secrets out of global memory and broad notes; store only non-sensitive decision rationale in Obsidian and engineering truth in repo handoff.

Before continuing cybersec work that depends on phase, scope, safety posture, roadmap, active lane, or report/evidence workflow, read:

1. live repo files and current validation/tool output as needed;
2. `handoff/active_strategy_queue.md` for current lane/navigation;
3. `handoff/accepted_changes.md` and named handoff artifacts for engineering truth;
4. Obsidian namespace `Projects/Cybersec Lab/`, especially `00_Index/Hermes Memory Routing.md`, for long-term methodology/strategy decisions.

Global Hermes memory should retain only compact cross-project preferences and pointers. Sensitive cybersec material, exact scan output, private scope/rules, raw evidence, credentials, tokens, payloads, loot, hashes, and one-off phase progress do not belong in global memory.

## Authority Order

When layers disagree, use this order:

1. Current explicit operator instruction.
2. Live repo files, config, validation output, and current git state.
3. Repo handoff files for accepted engineering state and safety boundaries.
4. Obsidian project notes for long-term strategy, decisions, research, experiments, and review synthesis.
5. Hermes durable memory for compact cross-project preferences and signposts.
6. `session_search` only as recall; verify recovered claims against files before acting.

## Layer Responsibilities

### Hermes durable memory

Use only for compact cross-project signposts and stable preferences, such as:

- user-wide language and review/reporting preferences;
- stable safety/routing principles that apply across sessions;
- short pointers to the correct project memory location.

Do not store:

- phase-completion logs, PR/issue/commit IDs, one-off validation results, or daily progress;
- target details, scan output, exploit payloads, hashes, loot, cookies, credentials, tokens, private scope/rules, or client-sensitive data;
- full strategy documents or review reports.

Write memories as declarative facts, not commands.

### Repo handoff files

Repo handoff is the engineering truth for this project.

Use `handoff/` for:

- accepted implementation and documentation changes;
- validation outcomes and review artifacts;
- worker coordination prompts/results;
- safety gates and authorization boundaries;
- current active strategy queue and deferred/blocked lanes.

`handoff/accepted_changes.md` remains append-oriented history, but it should not be the only navigation surface. Use `handoff/active_strategy_queue.md` for the compact current map.

### Active strategy queue

`handoff/active_strategy_queue.md` is the short, current project-navigation layer.

Use it to answer:

- What lane is active now?
- What are the next 1-3 likely slices?
- Which review artifact is authoritative for the current decision?
- Which lanes are deferred?
- Which changes are blocked until operator approval?

Keep it short. It is not a full history file.

### Obsidian project notes

Use Obsidian for long-term strategy, roadmap rationale, research synthesis, experiment results, and periodic-review synthesis that should remain searchable outside one git diff.

Recommended namespace:

```text
Projects/Cybersec Lab/
```

Recommended durable note metadata:

```markdown
Status: active | superseded | rejected | experiment | reference
Source: User | Hermes | Claude | Codex | Mixed
Date: YYYY-MM-DD
Repo truth: path/to/handoff-or-code-file
```

Do not put raw sensitive evidence, secrets, private target details, loot, or credentials in Obsidian. Store methodology and decisions, not sensitive operational data.

### Skills

Use skills for reusable procedures and judgment criteria that should transfer across projects.

Do not store cybersec project state in a skill. If a workflow becomes reusable, update or create a skill with the method only, and keep project facts in repo handoff or Obsidian.

### session_search

Use `session_search` to recover leads from prior conversations. Never treat it as authority by itself. Verify against repo files, Obsidian notes, or live state before acting.

## Periodic Review Freshness Convention

Every periodic or milestone-boundary review should state:

```text
Packet frozen at:
Latest live handoff inspected:
Latest commit inspected:
Post-packet changes included:
Post-packet changes excluded:
Authority if stale:
```

If a frozen review packet conflicts with live code, accepted changes, or the active strategy queue, use the live project-local authority and record the conflict.

## Drift Checks for Reviews

Periodic and direction reviews should explicitly check:

- memory drift: did Hermes global memory over- or understate project truth?
- handoff drift: do accepted changes, rolling handoffs, named artifacts, and active queue agree?
- goal drift: is the project still moving toward authorized bug-bounty automation rather than CTF-only or artifact-only work?
- structure drift: are files, templates, and review artifacts accumulating without a clear active queue?
- safety-boundary drift: did any proposal blur dry-run/internal work with activation, live target execution, scanner/module execution, report submission, scheduler, OAuth, or production changes?

## High-Risk Activation Boundary

Borrowed process lesson from YouTubeAgent: internal preparation and external activation must stay separate.

For this cybersec lab:

- Internal / usually lower-risk: offline fixtures, dry-run artifacts, local validators, read-only review prompts, documentation, static tests.
- Activation / higher-risk: live targets, scanner execution, recon runtime changes, scheduler/CI target automation, report/submission adapters, credentials/OAuth, production settings, scope/rules changes, callbacks/OAST/proxy/pivot/tunnels.

Activation-adjacent work must be checked against `docs/policy/review_tiering_policy.md` and `docs/policy/multi_party_review_decision_policy.md` for hard stops and concrete blockers before implementation. Do not resurrect historical tier ceremony; proceed with focused validation when no hard stop applies.

## Update Rules

- Update `handoff/active_strategy_queue.md` after closeout reviews, direction reviews, or milestone changes.
- Update `handoff/accepted_changes.md` for accepted project changes and validation outcomes.
- Update periodic review templates when drift checks or freshness metadata need to become standard.
- Save only compact cross-project pointers in Hermes memory.
- Create or patch skills only for reusable process, not project state.
