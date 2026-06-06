> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Multi-agent bug-hunting engineering plan — 2026-05-26

> For Hermes: use `subagent-driven-development` for implementation slices after operator approval. This document is a plan only; it does not authorize live target-touching, scanner/fuzzer/DAST execution, callbacks/OAST, scope expansion, credential handling, or report submission.

Goal: turn the current cybersec lab into a measurable multi-agent bug-hunting platform that thinks through realistic attacker paths, compiles them into bounded ethical proof surrogates, executes only authorized recoverable steps, and produces report-quality evidence/learning artifacts.

Architecture: build offline-first artifacts and helpers around existing repo conventions. The first milestone is T2/T3 local tooling and templates only. Planning should not exclude tactics merely because real attackers use dangerous methods; execution must still stop before unauthorized access, non-owned data contact, destructive impact, DDoS/resource exhaustion, credential theft, malware, stealth/persistence/evasion, or report submission. Any live execution remains gated by existing program scope, `config/scope.txt`, operator auth/OTP handling, and explicit lane approval.

Tech stack: Python stdlib, JSON/Markdown artifacts, existing `handoff/`, `programs/`, `modules/bundles/`, `scripts/`, `tests/` structure, Hermes `delegate_task`/cron orchestration.

---

## Milestone 1 — Offline data model and templates

Tier: T2/T3 depending on schema strictness. No live target touch.

### Task 1: Add A/B matrix artifact template

Objective: standardize redacted Account A/B evidence capture without storing secrets.

Files:
- Create: `templates/live_bounty_ab_matrix_template.md`
- Optional test: `tests/test_live_bounty_ab_matrix_template.py`

Content requirements:
- Header fields: program_slug, lane_id, object_family, object_label, accounts: A/B labels only.
- Matrix rows: operation, A positive expected/observed, B negative expected/observed, evidence_ref, result.
- Stop conditions: third-party data, PII, payment/order/KYC/support/recovery/seller/admin/upload/workflow/integration/API-key, policy ambiguity.
- Evidence rules: no cookies, tokens, OTPs, phone numbers, emails, raw full responses, screenshots with identifiers.

Verification:
- Template contains all required forbidden strings/sections.
- No field asks for secrets or raw identifiers.

### Task 2: Add redacted evidence packet schema/helper

Objective: make evidence packets machine-checkable before report-readiness review.

Files:
- Create: `schemas/live_bounty_ab_matrix.schema.json` or lightweight JSON contract doc.
- Create: `scripts/live-bounty-ab-matrix-validate.py`
- Create: `tests/test_live_bounty_ab_matrix_validate.sh` or `.py`

Data fields:
- program_slug
- lane_id
- scope_artifact
- object_family
- object_label
- request_budget
- accounts: `["Account A", "Account B"]` only, no raw usernames/emails
- tests: list of positive/negative controls
- evidence_refs: paths under `handoff/live_bounty_evidence/`
- result: `surface_only | blocked | candidate | report_ready | no_finding`

Validation rules:
- Reject likely secrets: cookie/token/session/authorization headers, OTP-like labels, phone-like values, raw email patterns.
- Reject evidence paths outside `handoff/live_bounty_evidence/`.
- Require Account A/B labels, not real account identifiers.
- Require stop_condition_acknowledged when result is blocked or candidate.

### Task 3: Add one-lane run-card generator

Objective: generate a narrow object-ownership run-card from template + program slug.

Files:
- Create: `scripts/live-bounty-ab-run-card.py`
- Test: `tests/test_live_bounty_ab_run_card.py`

CLI shape:

```bash
python scripts/live-bounty-ab-run-card.py \
  --program <program-slug> \
  --lane object_ownership \
  --object-family <safe_label> \
  --out handoff/live_bounty_evidence/<program-slug>/object_ownership/run_card_YYYYMMDD.md
```

Safety behavior:
- Refuse unknown program unless `programs/<slug>/scope.json` exists.
- Refuse object family strings that look like payment/order/KYC/support/recovery/seller/admin/upload/workflow/integration/API-key.
- Emit a plan/run-card only; do not browse, request, scan, or call target.

---

## Milestone 2 — Bundle freshness / vuln-intel coverage loop

Tier: T2/T3 offline tooling. No scanner or target touch.

### Task 4: Add bundle metadata parser

Objective: index current bundle docs by class, maturity, date, product refs, and CVE/GHSA refs.

Files:
- Create: `tools/bundle_index.py`
- Test: `tests/test_bundle_index.py`

Behavior:
- Read `modules/bundles/*.md` excluding README.
- Extract title, file path, dates, `CVE-*`, `GHSA-*`, inferred vuln classes, maturity/status.
- Support optional YAML-ish fields if added later: `vuln_classes`, `cwe`, `cve_refs`, `product_refs`, `last_verified`, `safe_proof_posture`.
- Output JSON to stdout or file.

### Task 5: Add vuln-intel to bundle coverage diff

Objective: compare newest vuln-intel candidates against bundle coverage.

Files:
- Create: `tools/vuln_intel_to_bundle_index.py`
- Test: `tests/test_vuln_intel_to_bundle_index.py`

Inputs:
- `handoff/vuln_intel/*.json`
- `modules/bundles/*.md`

Outputs:
- `handoff/bundle_freshness_delta_<stamp>.md`
- `handoff/bundle_freshness_delta_<stamp>.json`

Classification:
- `covered_by_existing_bundle`
- `needs_bundle_update`
- `new_local_bootstrap_candidate`
- `needs_authorized_live_target`
- `reference_only`
- `reject_low_signal`

Safety:
- Metadata-only. No calls to recon, scanners, PoC, browser, noVNC, or targets.
- Include top 3 recommendations only by default to avoid backlog sprawl.

### Task 6: Add scheduled metadata-only freshness job proposal

Objective: create a self-contained cron prompt, but do not enable without operator approval if treated as persistent scheduling.

Files:
- Create: `handoff/cron_prompts/bundle_freshness_delta_prompt_20260526.md`

Prompt requirements:
- Run `python tools/vuln_intel_refresh.py`.
- Run `python tools/vuln_intel_to_bundle_index.py`.
- Summarize only deltas and top one next action.
- Explicitly forbid scanning, exploitation, target touch, scope edits, report submission.

Activation: T5/persistent automation gate; requires operator approval before `cronjob create`.

---

## Milestone 3 — Multi-agent attack-path preview packet

Tier: T1/T2 docs and offline helper; T3 if introducing machine schema.

### Task 7: Add attack-path candidate packet template

Objective: make Adversarial Planner / Boundary Engineer / Evidence Critic roles produce comparable outputs without using risk labels as a tactic-exclusion filter.

Files:
- Create: `templates/live_bounty_attack_path_candidate_packet.md`
- Optional schema: `schemas/attack_path_candidate.schema.json`

Sections:
- Program facts and scope source.
- Scout score using high-hit-rate filter.
- Product model: users, roles, tenants, objects, APIs, state transitions.
- Attack-path candidates: at least 5 realistic hypotheses, including strong attacker-like paths when relevant.
- `proof_boundary`: owned accounts/objects, in-scope assets, allowed request budget, callback/OAST/tunnel allowance, state-change boundary, data-contact boundary, destructive-impact boundary.
- `proof_surrogate`: how to demonstrate impact without completing harmful access, non-owned data contact, or destructive effect.
- `stop_before`: unauthorized access completion, non-owned data, destructive action, DDoS/resource exhaustion, credential theft, malware, stealth/persistence/evasion, scope expansion, report submission.
- Hermes lane decision: choose one bounded proof surrogate or park/preserve the candidate.

### Task 8: Add preview synthesis helper

Objective: merge multiple reviewer packets into one Hermes decision table focused on attack path -> boundary -> proof surrogate -> evidence feasibility.

Files:
- Create: `scripts/live-bounty-preview-synthesize.py`
- Test: `tests/test_live_bounty_preview_synthesize.sh`

Behavior:
- Read 2–3 JSON companion preview packets conforming to `schemas/attack_path_candidate.schema.json`; markdown reviewer packets must either include this JSON companion or be manually converted before machine synthesis.
- Extract attack-path candidates, proof boundaries, proof surrogates, stop conditions, evidence requirements, and role-separated notes from companion packets when present.
- Preserve high-impact candidates even when execution is blocked; do not silently discard them because they are dangerous-looking.
- Produce table sorted by impact potential + proof-surrogate feasibility + authorization readiness.
- Require at least five candidate paths per packet.
- Require a single selected bounded lane or explicit `park/preserve`.
- Reject output if more than one live lane is marked selected.
- Reject output if a selected lane lacks a concrete proof boundary, callback/OAST/tunnel allowance, owned-control scope, stop-before-harm rule, or proof surrogate.

---

## Milestone 4 — Report readiness and learning loop

Tier: T2/T3 offline artifacts.

### Task 9: Add report-readiness checker for A/B matrix packets

Objective: prevent overclaiming and catch missing controls.

Files:
- Create: `scripts/live-bounty-report-readiness.py`
- Test: `tests/test_live_bounty_report_readiness.py`

Checks:
- Scope artifact exists.
- Account A positive and Account B negative controls exist.
- Evidence redaction validator passes.
- Impact statement exists.
- Remediation/retest placeholders exist.
- No blocked forbidden-flow labels are present.

Verdicts:
- `report_ready`
- `candidate_needs_more_control`
- `no_finding`
- `blocked`

### Task 10: Add no-finding feedback updater helper

Objective: make every parked/no-finding lane update selection rules consistently.

Files:
- Create: `scripts/live-bounty-feedback-entry.py`
- Test: `tests/test_live_bounty_feedback_entry.py`

Behavior:
- Generate a sanitized entry for `docs/strategy/live_bounty/live_bounty_no_finding_feedback_log.md`.
- Require reason classes: missing_account_control, missing_tenant_control, missing_role_control, missing_safe_owned_object, policy ambiguity, product empty state, high_value_surface_is_A4, evidence_not_report_ready.
- No raw target secrets or identifiers.

---

## Multi-agent execution pattern for implementation

For each milestone, use role-separated agents:

1. Adversarial planner agent:
   - Generates realistic attack-path candidates and impact hypotheses.
   - Must not execute or provide raw harmful execution against live targets; output is planning/boundary input.

2. Boundary engineer / implementer agent:
   - Converts one candidate into templates, schemas, scripts, tests, or bounded run cards.
   - Builds only offline/local helpers unless a separate live lane is explicitly approved.

3. Spec reviewer:
   - Checks exact plan compliance and that high-impact candidates were preserved rather than filtered by fear.

4. Safety/proof reviewer:
   - Checks stop-before-harm rules, proof surrogates, no unauthorized data contact, no destructive impact, no DDoS/resource exhaustion, no credential theft, no malware, no stealth/persistence/evasion, no target touch, no scope edits, and no secret storage.

5. Hermes verifier:
   - Runs tests.
   - Runs `hermes review` when scripts or scope-related helpers changed.
   - Updates `handoff/accepted_changes.md` if code is accepted.

## Suggested order

Do not build everything at once. Recommended first three engineering slices:

1. Attack-path candidate packet + proof-boundary/proof-surrogate schema.
2. Preview synthesis helper that preserves high-impact candidates but requires bounded proof surrogates before selection.
3. A/B matrix template + validator for the first executable owned-object proof family.

These three create the minimum viable system:

```text
think like attacker -> compile ethical proof boundary -> execute one bounded matrix -> learn/update bundles
```

## Acceptance criteria for first version

- All new scripts have tests.
- All helpers are offline-only and do not import or call live recon/scanner/browser tools.
- Redaction tests reject obvious secrets/PII.
- Coverage diff can identify that current bundle docs have no CVE/GHSA references.
- Preview synthesis requires one selected bounded lane or park/preserve.
- Report readiness refuses incomplete A/B controls.
- Handoff docs clearly state activation is not authorized.
- Selected candidates must include `proof_boundary`, `proof_surrogate`, and `stop_before` fields.
- High-impact candidates must be preserved as blocked/parked when they cannot be ethically executed; they must not be deleted merely because the raw attacker path is dangerous.
