> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Project Memory Governance Adoption Pattern

Use this when a user asks to borrow another project's memory/review workflow and apply only the useful parts to the current repository.

## Goal

Convert a cross-project memory/process lesson into project-local governance without turning Hermes durable memory or the skill library into a project database.

## Pattern

1. Load this skill first, then inspect the target repo's local context and existing handoff/governance files.
2. Adopt the process shape, not source-project facts:
   - authority order for current instruction, live repo, handoff, Obsidian, durable memory, session_search;
   - active strategy queue or equivalent short current-lane navigator;
   - periodic/deep review freshness metadata and drift checks;
   - explicit sensitive-data exclusions for the target domain.
3. Prefer project-local files for the adopted contract:
   - `handoff/memory_and_strategy_routing.md` or equivalent for the repo's memory authority rules;
   - `handoff/active_strategy_queue.md` or equivalent for current lane, next slices, deferred lanes, and approval-locked work;
   - periodic review README/templates for frozen-packet freshness and authority-if-stale rules;
   - project context file (`.hermes.md`, `AGENTS.md`, etc.) for asset/cadence pointers only.
4. Keep `accepted_changes.md` / changelog append-only and use it for the adoption record, not as the current-lane navigator.
5. Do not update global Hermes memory with PR numbers, commit IDs, phase logs, target names, or validation transcripts. At most, save a compact pointer that the project has repo-local memory routing if that will help future sessions.
6. Validate docs-only changes with the repo's lightweight review/static checks and a safety scan appropriate to the domain. Do not run unrelated runtime workflows just to record governance.

## Minimum useful fields for an active strategy queue

- Current lane / decision under review.
- Authoritative prompt or source file.
- Next candidate slices.
- Deferred lanes.
- Work blocked until explicit operator approval.
- Last review/update timestamp if the project uses dated governance.

## Minimum useful fields for periodic freshness

- Packet frozen at.
- Latest live handoff inspected.
- Latest commit or state inspected, if relevant.
- Post-packet changes included.
- Post-packet changes excluded.
- Authority rule if a frozen packet conflicts with active queue, accepted changes, live repo state, or current operator instruction.
- Memory drift, handoff drift, goal drift, and structure drift checks.

## Pitfalls

- Do not copy source-project risks verbatim; translate them into the target project's activation risks.
- Do not let `accepted_changes.md` become the only way to know what to do next once it grows long; add a compact queue.
- Do not encode project-specific state in this skill. Store only this reusable adoption pattern here.
