> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Architecture Review: next minimal local contracts

## Worker identity
- route: delegate_task
- tool/runtime: Hermes subagent
- role: deterministic-reviewer
- task file: user request: Architecture reviewer: propose minimal schemas/CLI contracts for role synthesis, Kali readiness, no-finding learning seed
- output artifact: handoff/architecture_review_next_schema_contracts_20260526.md

## Context read attestation
- [x] handoff/current_navigation.md
- [x] handoff/active_strategy_queue.md
- [x] handoff/current_artifact_index.md
- [x] handoff/accepted_changes.md
- [x] notes/obsidian_projects/Cybersec Lab.md
Missing / not read:
- none

## Scope
Local/offline architecture proposal only. No target contact, browser automation, VM/network changes, scanner/fuzzer/DAST, exploit execution, callbacks/OAST/tunnels, account actions, credential handling, scope edits, evidence deletion, or report submission.

Current substrate reviewed:
- schemas/attack_path_candidate.schema.json
- scripts/live-bounty-preview-synthesize.py
- schemas/live_bounty_lane_state.schema.json
- schemas/live_bounty_evidence.schema.json
- scripts/check-worker-attestation.py
- templates/role_packet_base.md
- handoff/current_artifact_index.md
- handoff/accepted_changes.md first current entries

## Recommendation summary

Implement the next slice as three very small, testable local JSON contracts plus one shared validator pattern. Do not merge them into the existing large attack_path_candidate schema yet unless tests prove the small contracts are useful.

Preferred files:
- schemas/attack_path_role_synthesis.schema.json
- scripts/attack-path-role-synthesize.py
- schemas/kali_readiness_state.schema.json
- scripts/kali-readiness-state.py
- schemas/no_finding_learning_seed.schema.json
- scripts/no-finding-learning-seed.py
- tests/test_next_contract_slices.sh

All CLIs should:
- accept only local JSON/markdown file paths, never --target/--url/--host/--scope/--live;
- emit JSON to stdout;
- write files only when an explicit --out path is supplied;
- set target_touching=false in every successful result;
- return exit 0 ok, exit 1 validation/contract errors, exit 30 forbidden target-like args.

## 1. Attack path role synthesis

Purpose: combine small role-specific local packets into one conflict-aware synthesis decision without rerunning workers or touching targets.

Minimal schema: schemas/attack_path_role_synthesis.schema.json

Required top-level fields:
- schema_version: const "1.0"
- synthesis_id: slug string
- program_slug: slug string
- source_packets: array minItems 1
- role_inputs: array minItems 2
- conflicts: array
- decision: object
- updated_at: YYYY-MM-DD string

role_inputs item:
- role: enum ["adversarial-planner", "boundary-engineer", "implementation-worker", "deterministic-reviewer", "safety-reviewer", "evidence-critic", "final-synthesizer", "other"]
- artifact: nonempty string
- verdict: enum ["PASS", "APPROVED", "REQUEST_CHANGES", "BLOCKED", "FAIL", "WARN", "SKIP", "INCOMPLETE"]
- candidate_ids: array of strings, default empty
- claims: array of strings, default empty
- blockers: array of strings, default empty

conflicts item:
- conflict_id: slug string
- type: enum ["authorization", "evidence", "impact", "feasibility", "scope", "role_disagreement", "overclaim"]
- candidate_id: string
- roles: array minItems 1 of role strings
- summary: nonempty string
- resolution: enum ["accept", "downgrade", "park", "block", "needs_operator", "needs_local_simulation"]
- reason: nonempty string

decision:
- selected_candidate_id: string
- decision: enum ["select_bounded_lane", "park_preserve", "blocked_awaiting_scope", "blocked_awaiting_operator", "switch_target", "needs_local_simulation", "no_selection"]
- reason: nonempty string
- required_next_artifact: string

CLI contract: scripts/attack-path-role-synthesize.py
- validate --input synthesis.json
  - validates schema only plus local semantic checks.
- synthesize --candidate-packet attack_path.json --role-artifact role.json --role-artifact role2.json [--out synthesis.json]
  - reads existing attack_path_candidate JSON and compact role-input JSON files.
  - emits synthesis JSON.
  - refuses more than one selected bounded executable lane.
  - if any role verdict is REQUEST_CHANGES/BLOCKED/FAIL and references the selected candidate, decision must be downgraded to park/block/operator/local-sim unless an explicit conflict resolution with reason is present.

Focused tests:
- PASS: two role inputs agree on candidate, no conflict, selected lane emitted.
- REQUEST_CHANGES: evidence-critic flags overclaim on selected candidate; synthesize downgrades to park_preserve or fails validation if still select_bounded_lane.
- FAIL: target-like arg --target exits 30.

Why separate from attack_path_candidate v1: it keeps role-conflict logic testable without expanding the candidate packet or forcing all workers into one schema immediately.

## 2. Kali readiness state

Purpose: record local readiness of the Kali/control route as machine state for planning, not as permission to touch targets.

Minimal schema: schemas/kali_readiness_state.schema.json

Required top-level fields:
- schema_version: const "1.0"
- profile: enum ["windows-control", "<attacker-vm>", "<victim-vm>", "other"]
- checked_at: YYYY-MM-DD string
- readiness: enum ["ready", "degraded", "blocked", "unknown"]
- target_touching_allowed: const false
- checks: array minItems 1
- blockers: array
- next_action: enum ["none", "operator_fix", "local_precheck", "open_temp_nat_for_install", "restore_snapshot", "do_not_use"]

checks item:
- name: enum ["ssh", "project_mount", "python", "docker", "browser", "host_only_network", "nat_closed", "disk_space", "tooling_baseline"]
- status: enum ["pass", "fail", "skip", "unknown"]
- evidence: string
- command_safe_to_rerun: boolean

CLI contract: scripts/kali-readiness-state.py
- validate --input readiness.json
  - schema and invariant checks only.
- summarize --input readiness.json
  - emits compact JSON: readiness, blockers, next_action, target_touching_allowed=false.
- seed --profile <attacker-vm> --out readiness.json
  - creates an unknown/degraded placeholder from provided local facts only; does not SSH, run PowerShell, start VMs, change NAT, or query targets.

Optional later, not in first slice: --probe-local may run local-only commands such as checking a config file or recorded path. Do not add SSH/VM-changing probes in v1.

Focused tests:
- PASS: ready fixture with nat_closed pass and target_touching_allowed=false validates.
- REQUEST_CHANGES: readiness=ready with a failed nat_closed or host_only_network check fails semantic validation.
- FAIL: --url or --host exits 30.

## 3. No-finding learning seed

Purpose: convert no-finding/surface-only/blocked outcomes into a compact machine-readable seed for the next preview/selection pass.

Minimal schema: schemas/no_finding_learning_seed.schema.json

Required top-level fields:
- schema_version: const "1.0"
- seed_id: slug string
- program_slug: slug string
- lane_id: slug string
- source_evidence: string
- outcome: enum ["no_finding", "surface_only", "blocked_operator_action", "blocked_awaiting_scope", "blocked_no_owned_object", "not_report_ready"]
- negative_findings: array minItems 1
- missing_prerequisites: array
- target_selection_updates: array
- next_attack_path_seeds: array
- updated_at: YYYY-MM-DD string

negative_findings item:
- hypothesis: string
- evidence: string
- confidence: enum ["low", "medium", "high"]
- do_not_retry_without: array of strings

next_attack_path_seeds item:
- title: string
- rationale: string
- required_prerequisites: array of strings
- preferred_roles: array of canonical worker role strings
- route: enum ["new_target", "same_target_after_operator_gate", "local_simulation", "reference_only"]

CLI contract: scripts/no-finding-learning-seed.py
- validate --input seed.json
  - schema and semantic validation.
- from-evidence --evidence live_bounty_evidence.json [--lane-state lane_state.json] [--out seed.json]
  - reads existing live_bounty_evidence schema and optionally lane state; emits seed JSON.
  - only accepts evidence statuses no_finding, surface_only, blocked, blocked_operator_action, blocked_awaiting_scope, not_report_ready.
  - report_ready/candidate evidence must fail: this tool is not a promotion path.
- summarize --input seed.json
  - emits compact JSON for preview tooling: outcome, missing_prerequisites, next_attack_path_seeds.

Focused tests:
- PASS: <program-redacted>-style surface_only evidence creates a seed with do_not_retry_without and new target/Account B prerequisites.
- REQUEST_CHANGES: candidate/report_ready evidence passed to from-evidence fails because this is not a finding promotion tool.
- FAIL: empty negative_findings fails schema/semantic validation.

## Shared semantic guardrails for all three CLIs

Reject these arguments exactly like the existing local-only helpers:
- --target
- --url
- --host
- --scope
- --live

Recommended shared function:
- reject_target_like_args(argv) -> structured JSON error and exit 30.

Do not call subprocesses, browsers, scanners, SSH, PowerShell, VirtualBox, curl, requests, sockets, or network APIs in these v1 tools. File reads/writes and JSON schema validation only.

## REQUEST_CHANGES risks to call out before implementation

REQUEST_CHANGES if any implementation does the following:
1. Adds target-touching probes to Kali readiness v1. Readiness state should be a recorded/seeded state artifact first, not an SSH/VM automation runner.
2. Treats readiness=ready as authorization. The schema must keep target_touching_allowed=false; authorization remains in program scope/dry-run artifacts.
3. Expands attack_path_candidate.schema.json aggressively instead of adding a separate role-synthesis schema. That would make the already useful packet harder to test and risk schema churn.
4. Allows role synthesis to override REQUEST_CHANGES/BLOCKED reviewer findings without explicit conflict resolution and reason.
5. Lets no-finding seed ingest candidate/report_ready evidence. That creates an accidental promotion/demotion path and blurs evidence workflow.
6. Stores raw identifiers, secrets, cookies, tokens, OTPs, phone/email values, screenshots, or non-redacted target data in no-finding seeds.
7. Introduces scheduler/cron, report submission, account actions, browser automation, scanner/fuzzer wrappers, or live target URL arguments under the guise of readiness or synthesis.
8. Adds broad markdown parsing of worker artifacts in v1. Prefer compact role-input JSON artifacts; markdown attestation is already covered by scripts/check-worker-attestation.py.
9. Builds a large multi-agent orchestration framework instead of three small validators/generators with fixtures.
10. Omits focused tests for forbidden target-like args and REQUEST_CHANGES/BLOCKED conflict behavior.

## Minimal implementation order

1. Add schemas and tiny fixture JSONs under tests/fixtures/next_contracts/.
2. Add one Python helper per contract with validate first.
3. Add semantic checks only after schema tests pass.
4. Add synthesize/from-evidence/seed commands with stdout JSON.
5. Run focused shell test plus py_compile and existing review gate.

## Validation
- Local checks run: read-only repository inspection; output artifact written. Recommended implementation validation commands are listed above, but no implementation tests were run because this review did not add executable code.
- Files changed/reviewed: created handoff/architecture_review_next_schema_contracts_20260526.md; reviewed existing schemas/scripts/templates/context listed in Scope.
- Safety boundary checked: offline/local architecture review only; no target contact or side-effectful tooling.

## Verdict
PASS with REQUEST_CHANGES risks documented above.
