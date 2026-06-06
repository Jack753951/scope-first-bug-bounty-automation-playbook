> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Dirty tree checkpoint audit — third-target pre-contact readiness — 2026-05-26

Status: slice-scoped audit
Source: Hermes `git status --short`, `git diff --stat`, artifact-index inspection
Boundary: classification only; no live target contact, no scanner/fuzzer/DAST/exploit/callback/OAST/tunnel, no credential/OTP/phone/token handling, no report submission.

## Current slice

Goal: make the workspace ready to resume the third real target (`<program-redacted>` / <program-name>) at the operator-controlled signup/auth gate.

Included in this checkpoint:

- <program-name> scope/lane state and pre-contact handoff artifacts.
- noVNC/Kali readiness notes and local readiness verification.
- Navigation/index/active-queue updates that tell future workers <program-name> is the selected third target and currently blocked on operator auth.
- Review-gate / worker-attestation hardening that prevents stale worker outputs from silently passing.
- Quarantine of unverified CVE/current-intel drafts and ignored scratch/debug paths.

Excluded from this checkpoint:

- Any new request to `<in-scope-host>`, `<in-scope-host>`, or `<program-domain>`.
- Any signup submission, phone entry, CAPTCHA/OTP/password/email verification, token/API-key handling, billing/KYC, customer interaction, invite, integration, webhook, or report submission.
- Any attempt to clean or delete operator-owned or sensitive local material.

## Dirty tree classification

### Current checkpoint / active substrate

These are coherent with the current checkpoint and should remain trackable for review/commit once validation passes:

```text
.gitignore
.hermes.md
bin/hermes
config/worker_roles.txt
config/scope.txt
handoff/current_navigation.md
handoff/active_strategy_queue.md
handoff/current_artifact_index.md
handoff/accepted_changes.md
handoff/dirty_tree_checkpoint_audit_20260526.md
programs/<program-redacted>/notes/program-redacted_target_selection_preview_20260526.md
programs/<program-redacted>/notes/program-redacted_first_contact_scope_and_signup_gate_20260526.md
programs/<program-redacted>/notes/program-redacted_pre_contact_ready_checkpoint_20260526.md
handoff/restart_checkpoint_20260526_front_signup_phone_gate.md
handoff/third_target_contact_checkpoint_20260526.json
programs/<program-redacted>/scope.json
programs/<program-redacted>/lane_state.json
scripts/kali-vnc-control.ps1
scripts/check-worker-attestation.py
scripts/test_hermes_worker_context_prompt.py
templates/role_packet_base.md
tests/test_worker_context_attestation.sh
tests/test_worker_roles_vocabulary.sh
tests/test_hermes_review_fail_closed.sh
notes/obsidian_projects/Cybersec Lab.md
```

Rationale:

- These files define the selected third target, operator gate, worker-output contract, local review gate, and VM/noVNC control-plane readiness.
- `config/scope.txt` is operator-owned/authorization-sensitive but intentionally changed: <program-name> in-scope hosts were added from logged-in <bug-bounty-platform> CSV. Never auto-reset; review explicitly.

### Active live-bounty substrate / recent strategy references

These are not all necessary for opening <program-name>, but they are part of the accepted live-bounty substrate and strategy queue now referenced by navigation/index:

```text
handoff/live_bounty_automation_engineering_slice_20260525.md
handoff/live_bounty_automation_substrate_closeout_20260525.md
docs/policy/live_bounty_autonomous_workflow_policy_20260525.md
docs/strategy/live_bounty/live_bounty_high_hit_rate_target_filter_20260526.md
docs/strategy/live_bounty/live_bounty_attack_class_matrix_20260526.md
docs/strategy/live_bounty/live_bounty_tactical_preview_template_20260526.md
docs/strategy/live_bounty/live_bounty_no_finding_feedback_log.md
docs/strategy/live_bounty/live_bounty_account_ab_operator_action_card_20260526.md
docs/strategy/live_bounty/next_live_bounty_shortlist_20260526.md
docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md
docs/policy/tactical_freedom_platform_direction_20260526.md
docs/strategy/platform/multi_agent_bug_hunting_operating_model_20260526.md
docs/strategy/platform/multi_agent_bug_hunting_engineering_plan_20260526.md
handoff/live_bounty_lane_queue.json
handoff/live_bounty_lane_runner_status.json
handoff/live_bounty_learning_seeds.jsonl
schemas/*.schema.json
scripts/live-bounty-*.py
scripts/attack-path-role-synthesize.py
scripts/kali-readiness-state.py
scripts/no-finding-learning-seed.py
scripts/evidence-redaction-check.py
scripts/post-proof-consolidation.sh
templates/live_bounty_attack_path_candidate_packet.md
tests/test_live_bounty_*.sh
tests/test_agent_capability_substrate.sh
tests/test_post_proof_consolidation.sh
tests/test_recon_gate.sh
```

Rationale:

- These files are current platform substrate and regression coverage, not scratch output.
- They remain local-only / bounded; they do not authorize target-touching without the project scope gate.

### Target-lane references / parked history

These are useful records but not the active <program-name> continuation surface:

```text
handoff/account_b_phone_gate_status_20260526.md
programs/<program-slug>/notes/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md
programs/<program-slug>/notes/coupang_tw_single_account_surface_map_20260525.md
programs/<program-slug>/notes/coupang_tw_phase5a_dry_run_packet_20260525.md
handoff/restart_checkpoint_20260525_hackerone_coupang_guidance.md
handoff/restart_checkpoint_20260526_tines_closeout_validation_followup.md
programs/<program-slug>/notes/tines_automation_vdp_phase5a_dry_run_packet_20260525.md
programs/<program-slug>/notes/tines_automation_vdp_owned_account_surface_map_20260525.md
handoff/tines_surface_learning_seed_20260526.json
programs/<program-slug>/lane_state_pending_second_account.json
programs/<program-slug>/scope.json
programs/<program-slug>/lane_state.json
handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/*.json
handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md
```

Rationale:

- Keep for provenance/learning. Do not delete or reset while switching to <program-name>.

### Quarantine / unverified current-intel cleanup

```text
D cve_brief_20260522.md
D cve_brief_20260523.md
cves/unverified/2026-05-22_websearch_fallback_unverified.md
cves/unverified/2026-05-23_websearch_fallback_unverified.md
```

Rationale:

- Root CVE briefs were unverified web-search fallback drafts; quarantine under `cves/unverified/` is the right direction.
- Fresh primary-source verification is required before operational use.

### Rolling/archival artifacts

```text
D handoff/claude_code_result.md
handoff/archive/rolling/*
handoff/codex_review.md
handoff/codex_task.md
handoff/cowork_task.md
```

Rationale:

- Rolling worker files are convenience pointers, not durable authority by themselves.
- Archive files preserve overwritten non-empty results. Keep unless a later dedicated archival cleanup says otherwise.
- `codex_review.md`, `codex_task.md`, and `cowork_task.md` are current rolling handoff surfaces and should be validated by the worker-attestation gate when used.

### Local-only ignored / never commit

```text
setting/local/**
logs/**
scans/**
loot/**
<artifact-output-dir>/**
handoff/tmp/**
handoff/*_stdout_check.json
root cve_brief_*.{json,md}
root UsersOwnerAppDataLocalTemp*.json
```

Rationale:

- These may contain local runtime data, raw output, or scratch/debug artifacts.
- `.gitignore` now explicitly protects common accidental scratch outputs.

## Decision

```text
CHECKPOINT_COHERENT_BUT_NOT_CLEAN_COMMITTED
```

The dirty tree is large but classifiable. The <program-name> pre-contact checkpoint can be declared operationally ready only if the focused tests, `hermes review`, diff check, and secret/sensitive scan pass after this audit is recorded.
