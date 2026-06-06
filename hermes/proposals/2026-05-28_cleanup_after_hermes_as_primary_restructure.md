> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cleanup proposal — after hermes-as-primary restructure

Author: Claude (current session, 2026-05-28).
Status: **pending operator decision per item**.
Boundary: this proposal does not authorize destructive ops. Each item below has an operator decision required before execution.

## Context

Today's restructure created:
- `INDEX.md`, `CLAUDE.md`, `.hermes.md` at project root
- `hermes/policies/`, `hermes/loops/`, `hermes/state/`, `hermes/digests/`, `hermes/calls/`, `hermes/proposals/`
- Updated `SAFETY.md` authority order

This proposal lists items that **conflict, duplicate, or are dead-after-restructure**. Each has a recommendation but waits for operator approval. **Per `SAFETY.md`: archive, don't delete.** Destination for archives: `archive/cleanup_hermes_primary_20260528/<subpath>/`.

## A. Active-truth duplicates (HIGH priority)

These overlap with `INDEX.md` / `current_navigation.md` and risk drift. Recommend folding into the new canon.

### A1. `handoff/INDEX.md`
- Current: lists handoff/ files + read-first order (overlap with new `/INDEX.md`).
- Risk: two indexes drift.
- **Recommend**: archive. New `/INDEX.md` covers handoff/.
- **Decision needed**: ARCHIVE / KEEP / SLIM_TO_HANDOFF_ONLY.

### A2. `handoff/active_strategy_queue.md`
- Current: referenced in old `SAFETY.md` as active-truth, but the new `current_navigation.md` already covers "what's active".
- Risk: duplicate route description.
- **Recommend**: fold any non-redundant content into `current_navigation.md`, then archive.
- **Decision needed**: ARCHIVE / KEEP / NEEDS_REVIEW (you read it first).

### A3. `handoff/current_artifact_index.md`
- Current: pointer file to active state files. Overlap with `INDEX.md` § Canonical directory map.
- **Recommend**: archive. INDEX subsumes.
- **Decision needed**: ARCHIVE / KEEP.

## B. Dead schema (MEDIUM priority)

Schema not enforced by any runtime check; actual `scope.json` files deviate freely.

### B1. `programs/_schema/`
- Files: `README.md`, `scope.schema.json`.
- Recommend: archive to `archive/cleanup_hermes_primary_20260528/programs_schema/`.
- **Decision needed**: ARCHIVE / KEEP_AS_REFERENCE / REWRITE_TO_MATCH_PRACTICE.

### B2. `programs/_examples/`
- Files: `README.md`, `client-engagement.example.json`, `ctf-platform.example.json`, `public-bounty.example.json`, `invalid/`, `sample-lab/`.
- Recommend: archive.
- **Decision needed**: ARCHIVE / KEEP.

### B3. `scripts/validate_program_scope.py` + `scripts/test_validate_program_scope.py`
- Validator for the dead schema.
- Recommend: archive.
- **Decision needed**: ARCHIVE / KEEP / REWRITE_FOR_NEW_PRACTICE.

## C. Tmp / orphan scripts (LOW priority)

These look like one-off scripts left from past sessions.

### C1. `scripts/tmp_cdp_inspect_hubspot.py`
### C2. `scripts/tmp_cdp_open_url.py`
### C3. `scripts/tmp_hubspot_click_verify.py`
### C4. `scripts/tmp_hubspot_fill_email.py`
### C5. `scripts/tmp_hubspot_start_trial.py`
### C6. `scripts/fill_signup_secret.py` (possibly tmp)

- All look like ad-hoc <program-redacted> signup helpers from earlier sessions.
- Recommend: review with `scripts/INDEX.md` + `scripts/SCRIPT_INVENTORY.md` before deciding. If those inventory files mark them as live, keep; if not listed, archive.
- **Decision needed**: BATCH_ARCHIVE / KEEP_ALL / NEEDS_REVIEW.

## D. Archived Hermes runtime (DEFER)

`archive/hermes_orchestration_20260528/` is the previous Hermes runtime. The new `bin/hermes` (when written) should:
- Replace the old `bin/hermes` shell script (which was multi-worker routing for review-ping-pong).
- Match the new `.hermes.md` / `hermes/policies/` contract.

But `bin/hermes` itself is NOT in the current working tree — it lives in archive. We need a NEW `bin/hermes` (or `hermes.ps1` for Windows) written for the new architecture. **This is not a cleanup item; it's a build item, separate decision.**

- **Decision needed**: should the new `bin/hermes` / `hermes.ps1` be written by Codex (under `consult_codex.md` rules) now, or deferred until Hermes is online via direct GPT-5.5 API integration?

## E. Items NOT proposed for cleanup (explicit)

To prevent accidental deletion, the following are NOT in this proposal:

- `programs/<active_slug>/` — all active program directories (<program-redacted>, <program-slug>, <program-slug>, <program-redacted>, <program-slug>, <program-redacted>, <program-slug>). Lane state and evidence stay.
- `handoff/accepted_changes.md` — append-only, never touch.
- `handoff/operator_inbox_<date>.md` — regenerated daily, current file stays.
- `handoff/live_bounty_evidence/` — evidence storage, stays.
- `handoff/live_bounty_lane_queue.json`, `pending_intake.json`, `current_navigation.md` — active-truth, stay.
- `handoff/live_bounty_learning_seeds.jsonl`, `live_bounty_lane_runner_status.json`, `kali_vm_operations_state.json` — runtime state, stay.
- `scripts/` core hunting / probe scripts — out of scope here.
- `archive/` — frozen, never touch from active workflow.
- `intelligence/`, `notes/`, `docs/`, `modules/`, `labs/`, `platform/`, `reports/`, `config/`, `setting/` — out of scope here.

## Execution sequence (if approved)

1. Per-item: operator marks ARCHIVE / KEEP / OTHER.
2. For approved ARCHIVEs: Hermes (or Claude during this session, per operator direction) creates `archive/cleanup_hermes_primary_20260528/` mirror structure and `git mv`s files in.
3. Single commit per group (A, B, C). Subject: `chore: archive <group> after hermes-as-primary restructure`.
4. Append summary to `handoff/accepted_changes.md`.

## What's needed from operator

Reply with per-item decision. Minimum:

- A1, A2, A3 → ARCHIVE / KEEP
- B1, B2, B3 → ARCHIVE / KEEP / OTHER
- C → BATCH_ARCHIVE / NEEDS_REVIEW
- D → CODEX_NOW / DEFER

Default if not specified: KEEP (no destructive action).
