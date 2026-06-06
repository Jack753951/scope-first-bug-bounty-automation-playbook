> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Direction Review — P2.21 Candidate Verification Checklist Consumer

Date: 2026-05-18
Route: independent read-only third-party review via Hermes delegate_task
Verdict: ACCEPT_WITH_CHANGES

## Summary

P2.21 is an appropriate next Phase 2 slice after P2.19 candidate review packets and P2.20 gap/action reports. The proposed stdin/stdout-only consumer should convert `candidate_review_gap_report/0.1-trial` into a deterministic `candidate_verification_plan/0.1-trial` human-checklist JSON document.

The slice is acceptable if implementation remains strictly offline, trial-only, read-only, stdin-to-stdout, and does not become report drafting, schema promotion, or target-touching runtime behavior.

## Required clarifications before implementation

1. Deterministic review-state mapping:
   - `finding_gaps[].review_state == "not_ready"` maps to `plan_state: "blocked"`.
   - `finding_gaps[].review_state == "reviewer_decision_required"` maps to `plan_state: "needs_manual_review"`.
   - Unknown `review_state` values must fail closed with structured JSON errors.
2. Deterministic gap-code mapping:
   - Each known P2.20 gap code maps one-to-one to a stable `check_items[].code` such as `CHECK_MISSING_EVIDENCE`.
   - Unknown `gap_codes[]` values must fail closed with structured JSON errors.
3. Summary counts must be pinned in tests:
   - `source_gap_code_counts` mirrors or deterministically recomputes source gap counts.
   - `check_item_count` equals total emitted check items.
   - `blocked_count` and `needs_manual_review_count` match emitted plan states.
4. Ordering must be deterministic:
   - `verification_plans` sorted by `(finding_id, target_value, module_id)`.
   - `check_items` sorted by the P2.20 gap-code order.

## Required tests

- Full chain: P2.19 builder -> P2.20 gap consumer -> P2.21 checklist consumer.
- Hand-built minimal valid P2.20 gap report -> P2.21 output.
- Exact mapping coverage for all known source gap codes.
- Error contract coverage for wrong schema, non-ok source status, source errors present, malformed stdin, non-object input, missing/non-list `finding_gaps`, non-object entries, invalid/unknown `review_state`, unknown gap codes, and invalid gap-code count shape.
- CLI denial for positional/unknown args and live-target flags (`--target`, `--url`, `--host`, `--scope`, `--live`) with structured JSON and no stderr.
- AST/static safety guards for no network, subprocess, file reads/writes, scanner/runtime imports, schema promotion, report drafting, platform adapters, or live affordances.

## Safety boundary

No live scans, target interaction, network, subprocess, file input/output options, output file writes, scanner/module runtime imports, schema promotion, report drafting, Markdown/HTML/PDF, platform adapters, report titles, impact/repro/remediation prose, status promotion, scope/config/runs/scans/loot/evidence/credential reads, scheduler, deployment, billing, OAuth, or production settings.

Allowed states remain below confirmation language: `blocked` and `needs_manual_review`. Output must not use `ready`, `approved`, `confirmed`, `verified`, or `accepted` as workflow states.
