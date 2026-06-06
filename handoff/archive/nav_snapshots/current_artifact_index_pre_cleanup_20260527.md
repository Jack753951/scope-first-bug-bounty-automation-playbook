> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Current Artifact Index — Cybersec Lab

Status: active cleanup/navigation index
Source: Hermes repo-noise cleanup pass
Date: 2026-05-26
Repo truth: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`, `.gitignore`

## Purpose

This file reduces handoff sprawl by classifying the current working artifacts. It is not a replacement for `current_navigation.md`; it is the cleanup map that tells future workers which files are current, reference-only, superseded, machine state, local-only, or ignored.

Boundary: navigation/file-hygiene only. This index does not authorize target-touching actions, scope changes, account creation, scanning, fuzzing, exploit execution, callbacks/OAST/tunnels, credential handling, report submission, or deletion of evidence.

## Status classes

- `active-entrypoint`: must-read or current route artifact.
- `active-engineering`: current code/schema/test/template substrate for the next hardening slice.
- `active-lane-state`: machine-readable lane/evidence state used by helpers.
- `active-strategy-reference`: current strategy/reference docs used for planning.
- `target-lane-reference`: target/lane-specific record; read only when that target/lane is in scope.
- `local-evidence-reference`: redacted/promoted evidence in repo handoff; do not delete casually.
- `historical-reference`: useful history, not default current context.
- `cleanup-record`: file-hygiene inventory/audit artifact.
- `ignored-local`: local cache/raw output/quarantine/log/evidence ignored by git.
- `operator-owned`: user/scope-controlled; never auto-clean.

## Must-read current entrypoints

| Status | Path | Notes |
|---|---|---|
| active-entrypoint | `.hermes.md` | Project contract and safety gate. |
| active-entrypoint | `handoff/current_navigation.md` | Primary route map; should stay compact. |
| active-entrypoint | `handoff/active_strategy_queue.md` | Compact active priorities and next lanes. |
| active-entrypoint | `handoff/current_artifact_index.md` | This cleanup/navigation index. |
| active-entrypoint | `handoff/accepted_changes.md` | Append/prepend accepted change log; already large, keep future entries compact. |
| active-entrypoint | `notes/obsidian_projects/Cybersec Lab.md` | Long-term strategy/rationale bridge. |

## Operator-owned / never auto-clean

| Status | Path | Notes |
|---|---|---|
| operator-owned | `config/worker_roles.txt` | Canonical worker role vocabulary for multi-agent artifacts; local workflow contract only, no target-touching authority. |
| operator-owned | `config/scope.txt` | Authorization whitelist. Modified in current working tree; review manually, never reset/delete automatically. |
| operator-owned | `loot/` | Sensitive runtime output; ignored. Do not inspect/delete without explicit operator direction. |
| operator-owned | `.env`, keys, tokens, browser profiles | Ignored by policy. Treat as sensitive/local. |

## Current engineering substrate for next hardening

| Status | Path | Notes |
|---|---|---|
| active-engineering | `schemas/live_bounty_lane_state.schema.json` | Lane-state contract. |
| active-engineering | `schemas/live_bounty_evidence.schema.json` | Evidence contract. |
| active-engineering | `schemas/attack_path_candidate.schema.json` | Tactical attack-path candidate contract. |
| active-engineering | `schemas/attack_path_role_synthesis.schema.json` | Role-conflict synthesis contract for bounded-lane / blocked-preserve decisions. |
| active-engineering | `schemas/kali_readiness_state.schema.json` | Kali/noVNC readiness state contract; readiness is not authorization. |
| active-engineering | `schemas/no_finding_learning_seed.schema.json` | No-finding/surface-only learning seed contract. |
| active-engineering | `scripts/live-bounty-lane-status.py` | Local lane/evidence summary helper. |
| active-engineering | `scripts/live-bounty-lane-runner.py` | Local-only queue runner; no target touching. |
| active-engineering | `scripts/live-bounty-preview-grounding.py` | Local-only reference grounding generator. |
| active-engineering | `scripts/live-bounty-preview-synthesize.py` | Local-only attack-path preview synthesizer. |
| active-engineering | `scripts/attack-path-role-synthesize.py` | Local-only role-conflict synthesizer; rejects target-like args. |
| active-engineering | `scripts/kali-readiness-state.py` | Local-only Kali readiness state seed/validate/summarize helper; no VM/network actions. |
| active-engineering | `scripts/no-finding-learning-seed.py` | Local-only no-finding/surface-only learning seed helper. |
| active-engineering | `scripts/check-worker-attestation.py` | Static worker artifact checker; validates worker identity, checked context read attestation, validation, verdict, and canonical role vocabulary when configured. |
| active-engineering | `scripts/evidence-redaction-check.py` | Evidence redaction check. |
| active-engineering | `scripts/post-proof-consolidation.sh` | Post-proof handoff checklist helper. |
| active-engineering | `templates/role_packet_base.md` | Base template for canonical role artifacts under the worker attestation contract. |
| active-engineering | `templates/live_bounty_attack_path_candidate_packet.md` | Attack-path packet template. |
| active-engineering | `tests/test_live_bounty_state_and_redaction.sh` | Focused regression. |
| active-engineering | `tests/test_live_bounty_lane_runner.sh` | Focused regression. |
| active-engineering | `tests/test_live_bounty_preview_grounding.sh` | Focused regression. |
| active-engineering | `tests/test_live_bounty_preview_synthesize.sh` | Focused regression. |
| active-engineering | `tests/test_agent_capability_substrate.sh` | Agent capability substrate regression for role synthesis, Kali readiness state, and no-finding learning seeds. |
| active-engineering | `tests/test_worker_context_attestation.sh` | Worker artifact contract regression for memory sync and role-separated collaboration. |
| active-engineering | `tests/test_worker_roles_vocabulary.sh` | Canonical role vocabulary / role coverage regression. |
| active-engineering | `tests/test_hermes_review_fail_closed.sh` | Hermes local review fail-closed regression for JSON, Python, shell, lock, and worker-attestation checker failures. |
| active-engineering | `tests/test_recon_gate.sh` | Authorization/dry-run gate regression. |
| active-engineering | `tests/test_post_proof_consolidation.sh` | Handoff checklist regression. |

## Current machine-readable lane / evidence state

| Status | Path | Notes |
|---|---|---|
| active-lane-state | `handoff/live_bounty_lane_queue.json` | Current local lane queue. Keep trackable. |
| active-lane-state | `handoff/live_bounty_lane_runner_status.json` | Latest structured runner status pointer. Keep for now; not ignored. |
| active-lane-state | `handoff/kali_vm_operations_state.json` | Seed/current Kali readiness state; readiness only, not authorization. |
| active-lane-state | `handoff/live_bounty_learning_seeds.jsonl` | Line-delimited no-finding/surface-only learning seeds for target/lane selection. |
| active-lane-state | `handoff/tines_surface_learning_seed_20260526.json` | <program-redacted> surface-only no-finding learning seed source artifact. |
| active-lane-state | `handoff/third_target_contact_checkpoint_20260526.json` | Third-target checkpoint: <program-name> scope/contact lane opened; auth completed by operator; current work is passive-only mapping. |
| active-lane-state | `handoff/program-redacted_first_contact_scope_and_signup_gate_20260526.md` | <program-name> confirmed-scope + first-contact signup gate packet. |
| active-lane-state | `handoff/program-redacted_pre_contact_ready_checkpoint_20260526.md` | Current readiness checkpoint: Kali/noVNC reachable, latest continuation shows <program-name> signup gate, operator gate remains blocking. |
| active-lane-state | `handoff/program-redacted_pre_contact_verification_summary_20260526.md` | Verification summary: focused tests, hermes review, diff check, local noVNC HTTP check, and independent subagent review passed. |
| active-lane-state | `handoff/restart_checkpoint_20260526_front_signup_phone_gate.md` | Restart checkpoint for <program-name> signup phone gate after non-secret fields were prefilled. |
| active-lane-state | `programs/<program-redacted>/scope.json` | <program-name> logged-in <bug-bounty-platform> scope converted to program scope. |
| active-lane-state | `programs/<program-redacted>/lane_state.json` | <program-name> A2 lane state; current status `A2_SURFACE_MAP_COMPLETE` / `surface_only` after Account B passive owned-surface map. |
| active-lane-state | `handoff/program-redacted_account_b_passive_surface_map_20260526.md` | Account B passive owned UI surface summary; no report-ready evidence. |
| active-lane-state | `handoff/live_bounty_evidence/<program-redacted>/owned_account_signup_profile_workspace_surface_map/evidence_surface_map_20260526.json` | Redacted structured evidence summary for Account B surface-only mapping. |
| active-lane-state | `handoff/program-redacted_authorized_attacker_flow_packet_20260526.md` | <program-name> post-auth attacker-flow packet; candidate bundle preserved and tightened after multi-agent BLOCK. |
| active-lane-state | `handoff/program-redacted_multi_agent_review_synthesis_20260526.md` | Hermes synthesis of actual Claude Code + Codex <program-name>-specific review; proof blocked, passive mapping allowed. |
| active-lane-state | `handoff/program-redacted_passive_docs_bundle_map_20260526.md` | Passive public-docs object/permission matrix and no-exclusion bundle set for <program-name> shared-inbox lane. |
| active-lane-state | `programs/<program-slug>/scope.json` | <program-redacted> program policy/scope artifact. |
| active-lane-state | `programs/<program-slug>/lane_state.json` | <program-redacted> lane state; currently no-finding/closed. |
| active-lane-state | `programs/<program-slug>/lane_state_pending_second_account.json` | <program-redacted> parked lane state. |
| local-evidence-reference | `handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_seed_20260525.json` | Initial redacted seed evidence. |
| local-evidence-reference | `handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_surface_map_20260525.json` | Redacted/promoted no-finding/surface evidence. |

## Current strategy / planning references

| Status | Path | Notes |
|---|---|---|
| active-strategy-reference | `handoff/proof_library_live_bounty_bridge_20260525.md` | Required before next live-target step. |
| active-strategy-reference | `handoff/live_bounty_autonomous_workflow_policy_20260525.md` | Operating policy for authorized bounty lanes. |
| active-strategy-reference | `handoff/live_bounty_automation_engineering_slice_20260525.md` | Implementation slice reference. |
| active-strategy-reference | `handoff/live_bounty_automation_substrate_closeout_20260525.md` | Closeout: substrate sealed unless reopened deliberately. |
| active-strategy-reference | `handoff/live_bounty_high_hit_rate_target_filter_20260526.md` | High-hit-rate target selection criteria. |
| active-strategy-reference | `handoff/live_bounty_attack_class_matrix_20260526.md` | Attack class selection matrix. |
| active-strategy-reference | `handoff/next_live_bounty_shortlist_20260526.md` | Candidate shortlist; passive only. |
| active-strategy-reference | `handoff/live_bounty_tactical_preview_template_20260526.md` | Current tactical preview template. |
| active-strategy-reference | `handoff/live_bounty_no_finding_feedback_log.md` | Converts no-finding into learning/selection updates. |
| active-strategy-reference | `handoff/live_bounty_account_ab_operator_action_card_20260526.md` | Account B / tenant B operator gate card. |
| active-strategy-reference | `handoff/tactical_freedom_platform_direction_20260526.md` | Current direction: preserve full attack paths; compile bounded proof surrogates. |
| active-strategy-reference | `handoff/multi_agent_bug_hunting_operating_model_20260526.md` | Multi-agent operating model. |
| active-strategy-reference | `handoff/multi_agent_bug_hunting_engineering_plan_20260526.md` | Engineering backlog; next hardening should start here. |
| active-strategy-reference | `handoff/multi_agent_tactical_review_memory_sync_rule_20260526.md` | Hard rule: non-trivial attacker-flow role separation must actually invoke suitable Claude/Codex-style workers or record passive-only exception; workers receive memory-sync context. |
| cleanup-record | `handoff/redundant_file_inventory_20260526.md` | Repo-noise inventory and first cleanup pass. |
| cleanup-record | `handoff/dirty_tree_checkpoint_audit_20260526.md` | Current dirty-tree classification for <program-name> pre-contact readiness checkpoint. |

## Target / lane-specific references

Read these only when working on the named target/lane.

| Status | Path | Notes |
|---|---|---|
| target-lane-reference | `handoff/program-redacted_target_selection_preview_20260526.md` | Third target selection preview; scope now confirmed and lane is at operator signup/auth gate. |
| target-lane-reference | `handoff/tines_automation_vdp_phase5a_dry_run_packet_20260525.md` | <program-redacted> first-lane dry-run packet. |
| target-lane-reference | `handoff/tines_automation_vdp_owned_account_surface_map_20260525.md` | <program-redacted> no-finding owned-account surface map. |
| target-lane-reference | `handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md` | <program-redacted> grounding packet. |
| target-lane-reference | `handoff/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md` | <program-redacted> boundary result; needs second account. |
| target-lane-reference | `handoff/coupang_tw_single_account_surface_map_20260525.md` | <program-redacted> single-account surface map. |
| target-lane-reference | `handoff/account_b_phone_gate_status_20260526.md` | Account/phone gate status. |
| historical-reference | `handoff/thanks_only_vdp_shortlist_20260525.md` | Earlier VDP shortlist; superseded by higher-hit-rate process but still useful history. |
| historical-reference | `handoff/restart_checkpoint_20260525_hackerone_coupang_guidance.md` | Restart checkpoint. |
| historical-reference | `handoff/restart_checkpoint_20260526_tines_closeout_validation_followup.md` | Restart checkpoint. |
| historical-reference | `handoff/tactical_risk_rebalance_20260526.md` | Directional record; current direction is in tactical freedom artifact and active queue. |
| historical-reference | `handoff/bundle_freshness_automation_plan_20260526.md` | Planning reference; not default next lane unless explicitly reopened. |

## Ignored local / quarantine / bulky evidence

These are intentionally not part of normal git status. Do not delete automatically.

| Status | Path | Notes |
|---|---|---|
| ignored-local | `setting/local/` | Machine/browser/tool/cache/quarantine. May contain sensitive local browser state. |
| ignored-local | `setting/local/quarantine/cve_brief_20260526_unverified_do_not_use.{json,md}` | Unverified CVE/current-intel draft moved from repo root. Fresh primary-source verification required before use. |
| ignored-local | `<artifact-output-dir>/` | Local lab run outputs/provenance. Archive whole runs instead of piecemeal deletion. |
| ignored-local | `logs/` | Runtime/audit logs. |
| ignored-local | `scans/` | Runtime scan outputs. |
| ignored-local | `handoff/worker_logs/` | Worker raw logs; ignored. |
| ignored-local | `handoff/tmp/` | Future handoff scratch/debug output; ignored. |
| historical-reference | `cves/unverified/2026-05-22_websearch_fallback_unverified.md` | Moved from root `cve_brief_20260522.md`; unverified web-search fallback. Fresh primary-source verification required before use. |
| historical-reference | `cves/unverified/2026-05-23_websearch_fallback_unverified.md` | Moved from root `cve_brief_20260523.md`; unverified web-search fallback. Fresh primary-source verification required before use. |
| ignored-local | root `cve_brief_*.{json,md}` | Now ignored for future accidental root drafts; move verified content to `cves/` or handoff, keep unverified drafts in quarantine/unverified. |
| ignored-local | root `UsersOwnerAppDataLocalTemp*.json` | Temp-path leak artifacts; now ignored if recurrence happens. |
| ignored-local | `handoff/*_stdout_check.json` | One-run stdout/debug checks; now ignored. |

## Superseded / archived conventions

- Keep active docs discoverable through `current_navigation.md`, `active_strategy_queue.md`, and this index.
- Keep dated handoff docs as references unless a later explicit cleanup pass marks them safe to archive.
- For old rolling files, prefer `handoff/archive/rolling/` if the wrapper created it.
- For large local outputs, compress/archive entire run directories outside the repo rather than deleting individual evidence files.
- Never auto-delete `config/scope.txt`, `loot/`, browser profiles, credentials, raw evidence, or reports that may be needed for provenance.

## Next hardening slice now unblocked

The repo is clean enough to proceed with engineering hardening if `./bin/hermes review` passes. Recommended next slice:

```text
third-target <program-name> passive mapping / proof-blocked bundle preservation
```

Expected focus:
- <program-name> signup/auth completed by operator; Hermes has post-auth passive mapping artifacts.
- Current state: proof blocked beyond passive mapping after <program-name>-specific Claude Code + Codex review.
- Continue only passive UI/docs mapping; stop before object creation, invite/role mutation, API-token/API call, customer data, integration/channel/OAuth, workflow activation, callback, scanner/fuzzer/DAST, report actions.
- Preserve all useful bundles in `handoff/program-redacted_passive_docs_bundle_map_20260526.md`; keep `programs/<program-redacted>/lane_state.json` as the machine-readable state pointer.
