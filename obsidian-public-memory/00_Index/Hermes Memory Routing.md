> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Hermes Memory Routing for Cybersec Lab

Status: active
Source: User / Hermes
Date: 2026-05-21
Updated: 2026-05-28
Repo truth: `<user-home>`, `handoff/current_navigation.md`, `handoff/accepted_changes.md`, `hermes/proposals/2026-05-28_structure_index_drift_check.md`
Legacy repo note: `<user-home>` is reference-only unless the operator explicitly reactivates it.

## Purpose

This note lets the hacking2 / Cybersec Lab project understand the global memory compaction rule: Hermes durable memory should not be a project database. Cybersec project facts should be read from this Obsidian namespace and the `hacking2` repo handoff before relying on compact global memory.

## Operating rule

Before continuing cybersec project work that depends on current phase, scope, safety posture, roadmap, active lane, or report/evidence workflow:

1. Read the live repo context and current handoff files under `<user-home>`: `.hermes.md`, `SAFETY.md`, `INDEX.md`, `handoff/current_navigation.md`, and `handoff/accepted_changes.md`.
2. Check active lanes/queue: `handoff/live_bounty_lane_queue.json` and relevant `programs/<slug>/lane_state.json` if a lane is active.
3. Check this Obsidian namespace for long-term methodology, roadmap, decisions, and review synthesis.
4. Treat Hermes durable memory as only a compact cross-project signpost.
5. Verify session_search memories against files before acting.

## Workflow/process change routing

User preference recorded 2026-05-22: when the hacking/Cybersec Lab workflow or process changes, the decision should be recorded in the project Obsidian namespace as well as the repo handoff layer. Do not rely only on chat or Hermes global memory for collaboration rules, review tiers, safety gates, lab routing, evidence/report workflow, worker routing, memory governance, or other process decisions that future agents need to follow.

Use repo handoff for engineering truth and validation state; use Obsidian for durable rationale and future-planning context. Keep secrets, raw target details, exploit payloads, loot, credentials, private scope/rules, and sensitive evidence out of global memory and broad Obsidian notes.

## Status-answer preference

When summarizing Cybersec Lab status, clearly distinguish catalog/planning coverage from implemented reusable pipeline coverage, and distinguish candidate/observation status from confirmed vulnerability status. Status answers should state that the long-term goal explicitly includes bounded, policy-gated automation; then state the current phase, remaining gates, and safest next action.

## What belongs here

- Long-term methodology and bug-bounty workflow rationale.
- Roadmap and phase rationale.
- Research synthesis and public-source security methodology notes.
- Review synthesis that should guide future project decisions.
- Non-sensitive decision records.

## What belongs in the hacking2 repo handoff

- Accepted implementation changes.
- Validation outcomes.
- Worker outputs and review artifacts.
- Active strategy queue, blocked lanes, approval gates.
- Exact engineering state and current safety boundaries.

## What must not be stored in global memory or broad Obsidian notes

- Secrets, API keys, cookies, tokens, credentials.
- Raw scan outputs, target details, exploit payloads, loot, hashes, private scope/rules, or client-sensitive evidence.
- One-off phase progress, commit IDs, validation transcripts, or stale artifact IDs.

## Compatibility note for future agents

If global Hermes memory is shorter than past sessions, do not infer that project direction changed. The detailed cybersec truth was intentionally routed into repo handoff and this Obsidian namespace. Use the authority order above.
