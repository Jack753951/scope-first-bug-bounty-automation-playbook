> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Worktree Cleanup Index — 2026-05-28

Status: active cleanup checkpoint
Boundary: offline repository organization only. No live target contact, no scan/fuzz/exploit/callback/OAST, no credential handling, no account mutation, no report submission.

## Decision

Clean in place. Do not reset, do not `git clean -fdx`, and do not create a replacement repository as the main line.

## Active files added/updated in this cleanup pass

- `docs/ENGINEERING_INDEX.md` — top-level minimal engineering index and future read order.
- `docs/policy/README.md` — active policy set and archived/superseded policy list.
- `docs/policy/repo_hygiene_policy.md` — cleanup rules, no-reset/no-clean boundary, archive/quarantine discipline.
- `handoff/INDEX.md` — active handoff root rules and archive locations.
- `handoff/current_artifact_index.md` — now points to the engineering index and policy archive.
- `README.md` — quick entrypoints now point to the engineering index and policy/handoff indexes.

## Policy files archived, not deleted

Moved to `docs/policy/archive/2026-05-cleanup/`:

- `CLAUDE_CODEX_ROUTING_POLICY.md`
- `memory_coexistence_policy.md`
- `periodic_third_party_review_process.md`
- `program_policy_dry_run_closeout_20260519.md`
- `p3_13_module_risk_tier_policy_result.md`
- `p3_15_manifest_profile_policy_crosswalk_20260520.md`
- `phase4b_lab_fast_lane_policy_20260521.md`
- `architecture_review_next_schema_contracts_20260526.md`
- `tactical_risk_rebalance_20260526.md`

Rationale: these are historical, superseded, phase-specific, or folded into the active policy set. They remain available for provenance.

## Root handoff files archived, not deleted

Moved to `handoff/archive/phase_history/2026-05-27-root-handoff/`:

- `after_syfe_no_email_target_decision_20260527.md`
- `dual_track_agent_synthesis_20260527.md`
- `h1_freshness_first_target_shortlist_20260527.md`
- `h1_next_target_quick_triage_after_front_park_20260527.md`
- `latest_rce_cve_lane_2026_20260527.md`
- `latest_vuln_lane_correction_2026_recent_20260527.md`
- `nextjs_cve_2025_29927_detector_run_card.md`

Rationale: root `handoff/` should remain a current collaboration surface, not a dated-document dump.

## Deliberately not touched

- `config/scope.txt`
- `programs/<slug>/scope.json`
- `programs/<slug>/lane_state*.json`
- `handoff/live_bounty_evidence/`
- `reports/`
- `logs/`
- `scans/`
- `loot/`
- `<artifact-output-dir>/`
- browser/session/local profile material
- raw evidence or sensitive runtime material

## Future rule

New policy/strategy/handoff material must either update an existing active file or be created under a clearly indexed current/archive location. Root-level dated sprawl is not allowed.
