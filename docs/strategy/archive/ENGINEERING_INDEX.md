> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Engineering Index

Status: active engineering entrypoint
Boundary: index only; this file does not authorize live target testing, scanning, exploitation, account mutation, credential handling, scheduler activation, report promotion, or final submission.

## Read order for any future agent

1. `.hermes.md` — project contract, safety gate, routing, and worker expectations.
2. `PROJECT_CHARTER.md` — product north star and repository shape.
3. `docs/policy/README.md` — active policy set and archived-policy boundary.
4. `handoff/INDEX.md` — active handoff map.
5. `handoff/current_navigation.md` — current route, blockers, and stop-before gates.
6. `handoff/active_strategy_queue.md` — next decisions and active priorities.
7. `handoff/current_artifact_index.md` — current artifacts, lane state, and platform substrate pointers.
8. `docs/strategy/platform/engineering_direction_20260527.md` — current engineering backlog and anti-patterns.

If these conflict, follow the authority order in `docs/policy/memory_and_strategy_routing.md`: current operator instruction, live repo/config/validation state, repo handoff, Obsidian, durable memory, session recall.

## Active project truth

| Area | Active entrypoint | Rule |
|---|---|---|
| Mission | `PROJECT_CHARTER.md` | Keep short; no dated variants. |
| Agent contract | `.hermes.md` | Binding safety/routing contract. |
| Repo hygiene | `docs/policy/repo_hygiene_policy.md` | No broad reset/clean; classify then archive/quarantine. |
| Safety/testing | `docs/policy/lab_safety_contract.md`, `docs/policy/active_testing_policy.md`, `docs/policy/live_bounty_autonomous_workflow_policy_20260525.md` | Target-touching work requires scope + policy + operator gate. |
| Memory/routing | `docs/policy/memory_and_strategy_routing.md` | Global memory is a compact signpost, not project state. |
| Worker/review | `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md`, `docs/policy/multi_party_review_decision_policy.md`, `docs/policy/review_tiering_policy.md` | Use external review when boundaries/contracts/platform shape change; blockers must be concrete. |
| Source guidance | `docs/policy/oss_recon_gate.md` | Lightweight OSS comparison; not ceremony. |
| Model/tool routing | `docs/policy/model_usage_routing_policy.md` | Edit this file if routing changes; do not create variants. |
| Current state | `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/current_artifact_index.md` | Edit existing current files; archive snapshots only when needed. |

## Repository zones

| Zone | Path | Keep minimal by |
|---|---|---|
| Platform code | `platform/`, `modules/`, `schemas/`, `tests/`, production `scripts/` | Test/schema required before promotion. |
| Program state | `programs/<slug>/` | Do not bulk-delete; lane state is provenance. |
| Evidence/report | `handoff/live_bounty_evidence/`, `reports/`, `labs/proofs/` | Redacted, scoped, and operator-gated. |
| Handoff | `handoff/` | Root holds current map/queue/state/rolling IPC only. Old items go to `handoff/archive/`. |
| Policy | `docs/policy/` | Active set in README; superseded files go to `docs/policy/archive/`. |
| Strategy/reference | `docs/strategy/` | One active engineering direction; dated material is reference. |
| Local/runtime | `logs/`, `scans/`, `loot/`, `<artifact-output-dir>/`, browser profiles | Usually ignored; never auto-clean broadly. |

## Promotion gates

A file may move into active project truth only if it passes the relevant gate:

- It has a clear owner/path and does not duplicate an existing active file.
- It does not contain passwords, cookies, tokens, OTPs, verification links, private scope/rules, customer data, or raw sensitive evidence.
- If it is automation, default mode is offline/dry-run/no-target unless separately approved.
- If it can touch a target, it references `config/scope.txt`, `programs/<slug>/scope.json`, stop-before rules, and operator gate.
- If it is platform code, it has tests or a documented local validation command.
- If it is policy/strategy, it edits the active file instead of creating a dated variant.

## Commit discipline

Split work by intent:

1. structure/index
2. policy
3. platform code/schema
4. tests
5. program/lane state
6. archive/quarantine
7. redaction/deletion with explicit approval

No mega-commits. Every commit should state whether it is target-touching, whether it can contain sensitive/private data, and what validated it.

## Minimal cleanup rule

When unsure, archive or quarantine; do not delete. A visually clean tree is less important than preserving authorization, scope, evidence, and lane-decision provenance.
