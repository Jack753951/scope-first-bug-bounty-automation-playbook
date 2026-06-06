> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Repo Cleanup Plan — 2026-05-19

Status: proposed cleanup plan
Owner: Hermes / Operator
Safety posture: inspect-first; no deletion of evidence, recon outputs, CVE briefs, worker artifacts, or generated reports without explicit operator approval

## Why cleanup is needed

The workspace is healthy enough to keep working, but `git status` is noisy:

- modified tracked files from several accepted slices
- many untracked handoff/review artifacts
- new scripts, validators, templates, modules, and fixtures from Phase 2 / Phase 3 slices
- unverified CVE brief artifacts
- ignored runtime/cache directories
- one accidental root-level browser/evaluation artifact: `x.includes('buy')`

Noise makes it harder for Hermes, Claude/Cowork, and Codex to review only the current slice.

## Current inventory snapshot

Generated from local git status on 2026-05-19.

- Modified tracked files: 26
- Untracked files/directories: 171
- Ignored runtime/cache paths include `.pytest_cache/`, `__pycache__/`, `handoff/latest_check.md`, `handoff/worker_logs/`, `logs/`, `scans/`, `node_modules/`, `reports/generated/`, and `setting/`.

Important modified tracked files include:

- `.gitignore`
- `.hermes.md`
- `HERMES_WORKFLOW.md`
- `bin/hermes`
- `handoff/accepted_changes.md`
- `handoff/codex_review.md`
- `modules/_schema/README.md`
- `package.json`
- `scripts/README.md`
- `scripts/module_runner.py`
- `scripts/program_policy_boundary.py`
- `scripts/test_module_runner.py`
- `scripts/test_program_policy_boundary.py`

Important untracked categories include:

- handoff/review/worker artifacts: direction reviews, implementation reviews, Claude Code run metadata, task prompts
- new scripts/tests/validators: P2.17-P3.5 candidate workflow, CTF calibration, preview ledger/manifest, report-readiness helpers
- new schemas/modules/templates/fixtures: preview schemas, security_headers_baseline module, candidate review fixtures, CTF metadata template, report-readiness prompt catalog
- unverified CVE artifacts: `cve_brief_20260519.md`, `cves/unverified/2026-05-18_websearch_fallback_unverified.md`
- misc inspection-required artifacts: `p2_18_review.diff`, `x.includes('buy')`

## Cleanup principles

1. Do not delete before inspecting contents.
2. Do not delete or commit `loot/`, raw logs, scans, generated reports, packet captures, credentials, tokens, keys, or local machine config.
3. Keep accepted handoff/review artifacts if they document decisions, usage, model routing, safety boundaries, or review outcomes.
4. Move or quarantine unverified intelligence rather than treating it as canonical.
5. Separate cleanup into reviewable commits by purpose instead of one giant mixed commit.
6. Run `HACKLAB=<private-workspace> ./bin/hermes review` after each cleanup batch.

## Recommended cleanup batches

### Batch A — Commit accepted workflow/process documentation

Purpose: preserve the new review governance and make future routing less ambiguous.

Candidate files:

- `docs/policy/multi_party_review_decision_policy.md`
- `.hermes.md`
- `handoff/accepted_changes.md`
- related existing policy docs if their diffs are confirmed intentional: `HERMES_WORKFLOW.md`, `handoff/model_usage_routing_policy.md`

Validation:

```bash
HACKLAB=<private-workspace> ./bin/hermes review
```

Suggested commit message:

```text
docs: adopt multi-party review decision gate
```

### Batch B — Commit Phase 2 / Phase 3 implementation artifacts as accepted work

Purpose: reduce untracked implementation noise while preserving validated scripts/tests/schemas/fixtures.

Candidate groups:

- `scripts/build_candidate_review_packet.py`
- `scripts/review_candidate_packet_gaps.py`
- `scripts/build_candidate_verification_plan.py`
- `scripts/build_report_readiness_gate.py`
- `scripts/build_candidate_workflow_fixture.py`
- corresponding `scripts/test_*` files
- `templates/report_readiness_reviewer_prompts.json`
- `tests/fixtures/candidate_review_packet/**`
- `modules/_schema/preview_manifest.schema.json`
- `modules/_schema/preview_ledger.schema.json`
- `scripts/validate_preview_manifest.py`
- `scripts/validate_preview_ledger.py`
- corresponding tests and README updates
- `modules/checks/level1/security_headers_baseline/**`

Validation:

```bash
python -m unittest discover -s scripts -p 'test_*.py'
HACKLAB=<private-workspace> ./bin/hermes review
```

Suggested commit message:

```text
feat: add offline candidate workflow and preview validation artifacts
```

If this commit is too large, split by milestone:

- P2.14-P2.16 preview/module artifacts
- P2.17-P2.18 CTF calibration artifacts
- P2.19-P3.5 candidate workflow/report-readiness artifacts

### Batch C — Commit durable handoff and review records

Purpose: preserve review evidence and model/worker usage metadata that explains why accepted work was safe.

Candidate groups:

- `handoff/cowork_p*_direction_prompt.md`
- `handoff/cowork_p*_direction_review.md`
- `handoff/third_party_*_implementation_review*.md`
- `handoff/claude_code_impl_run_*.json`
- `handoff/claude_code_*_run.json`
- `handoff/claude_code_*_notools.txt`
- `handoff/periodic_reviews/**`
- `handoff/p2_16_triage/**`
- `handoff/p2_24_core_extraction_scope.md`

Suggested commit message:

```text
docs: preserve phase review and worker handoff records
```

### Batch D — Quarantine or remove inspection-required misc artifacts

Do this only after inspection.

Candidate actions:

- `x.includes('buy')`: appears to contain only a failed browser/evaluation JSON error. Safe candidate for deletion after operator approval.
- `p2_18_review.diff`: inspect whether it is duplicated by committed review artifacts. If redundant, delete; if useful, move under `handoff/archive/` or `handoff/review_diffs/`.
- `cve_brief_20260519.md`: root-level unverified CVE brief includes sandbox/web-search fallback caveats and active testing suggestions. Move to `cves/unverified/2026-05-19_websearch_fallback_unverified.md` or delete after preserving a warning header. Do not use it as canonical intelligence.
- `cves/unverified/2026-05-18_websearch_fallback_unverified.md`: keep quarantined unless explicitly pruned later.

Suggested commands after approval:

```bash
mkdir -p cves/unverified handoff/review_diffs
mv cve_brief_20260519.md cves/unverified/2026-05-19_websearch_fallback_unverified.md
mv p2_18_review.diff handoff/review_diffs/p2_18_review.diff
rm -- "x.includes('buy')"
```

### Batch E — Leave ignored runtime/cache artifacts alone or clean locally only

Ignored paths are already excluded and should not be committed:

- `.pytest_cache/`
- `__pycache__/`
- `handoff/latest_check.md`
- `handoff/worker_logs/`
- `logs/`
- `scans/`
- `reports/generated/`
- `setting/`
- `node_modules/`

These may be cleaned locally only after confirming they do not contain evidence needed for current work. In this cybersec workspace, inspect `logs/`, `scans/`, and `reports/generated/` before deleting anything.

## Recommended next action

Start with Batch D inspection and quarantine because it removes obvious noise without touching accepted source code. Then run Hermes review. After that, stage/commit Batch A, then split Batch B/C by milestone.

## Safety boundary

This cleanup plan does not authorize deletion, network access, live scans, target interaction, report submission, scheduler changes, deployment, billing, credential handling, OAuth changes, scope changes, or production changes.
