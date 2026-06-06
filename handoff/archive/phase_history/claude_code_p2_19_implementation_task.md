> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code Implementation Task — P2.19 Bug-Bounty Candidate Review Packet

Date: 2026-05-18
Worker route: Claude Code MAX/OAuth implementation
Verifier: Hermes
Fallback: Codex/GPT surgical fix only if needed
Tier: T3
Boundary: offline/local only; no target interaction, no runtime wiring

## Read First

- `handoff/cowork_p2_19_direction_review.md`
- `scripts/validate_finding_evidence.py`
- `tests/fixtures/security_headers_baseline/*/expected_findings.json`
- `scripts/README.md`

## Goal

Implement P2.19: an offline/local bug-bounty candidate review packet builder.

This redirects the roadmap away from CTF expansion and back toward the authorized bug-bounty automation platform. The builder packages existing committed `finding/1.0` candidate fixtures into a deterministic review packet for third-party triage/review. It must not draft reports, publish, touch targets, or promote findings.

## Required Deliverables

1. Add:

```text
scripts/build_candidate_review_packet.py
scripts/test_candidate_review_packet.py
tests/fixtures/candidate_review_packet/
```

2. Builder requirements:

- Standard-library only.
- `--repo-root <path>` required.
- `--input <relative path>` repeatable and required.
- stdout JSON only; no file writes.
- `schema_version`: exactly `candidate_review_packet/0.1-trial`.
- Header comment near top: `TRIAL ONLY — schema promotion deferred to P2.20+`.
- Reads allowlisted committed fixture paths only:
  - `tests/fixtures/security_headers_baseline/*/expected_findings.json`
  - optionally `tests/fixtures/candidate_review_packet/**/expected_findings.json`
- Must reject `runs/`, `scans/`, `loot/`, `evidence/`, `programs/`, `config/`, `.env`, `setting/local/`, absolute paths, traversal, backslashes, URL-like paths, NUL, symlink escapes.
- Validate each input finding through `scripts.validate_finding_evidence.validate_data(finding, "finding")` if that function exists; otherwise use the project validator's closest safe public function without invoking its CLI.
- Exclude invalid findings from `findings[]` and report structured errors.
- Never emit `confirmed`, `verified`, or `accepted` anywhere.
- Generate deterministic `review_questions[]` from fixed templates only.
- Generate deterministic `report_readiness`: `not_ready` if no evidence refs OR confidence low OR severity_hint info; otherwise `reviewer_decision_required`. Never emit ready/approved/draft.
- Sort findings by `id` then `target.value`; sort/dedupe summary targets/modules.

3. Tests must cover at least the review's mandatory cases:

- happy path multiple existing security headers fixtures
- single-file happy path
- empty findings fixture
- deterministic output
- input order independence
- validation reuse and invalid finding exclusion
- forbidden status rejection
- path allowlist and repo-root required
- no filesystem writes
- schema-version pin
- manual verification/scanner-output flags preserved
- report-readiness rubric
- summary aggregation determinism
- review-question determinism
- AST/grep guard against network/subprocess/file writes/runtime imports
- no platform name leak
- trial-only header
- no modules/_schema file

4. Update:

```text
scripts/README.md
handoff/accepted_changes.md
```

## Forbidden Changes

- No live scans, HTTP, sockets, DNS, callbacks, exploit attempts, fuzzing, brute force, OAST, or target-touching behavior.
- No subprocess execution.
- No filesystem writes by the builder.
- No imports from runtime/scanner/module runner paths. Allowed only safe reuse of `scripts.validate_finding_evidence` validation logic.
- No new JSON Schema under `modules/_schema/`.
- No registry entry, runner wiring, recon wiring, CI/hook/scheduler/pre-commit wiring, `bin/hermes` integration, or `.github/` workflow changes.
- No platform adapters or platform-name strings.
- No Markdown/HTML/PDF report generation.
- No changes to `config/scope.txt`, `loot/`, `.env`, credentials, tokens, OAuth, scheduler, deployment, billing, or production settings.
- No CTF tooling changes.
- No ANTHROPIC_API_KEY usage; use Claude Code MAX/OAuth only.

## Validation to Run

```bash
python -m py_compile scripts/build_candidate_review_packet.py scripts/test_candidate_review_packet.py
python scripts/test_candidate_review_packet.py
python -m unittest discover -s scripts -p 'test_*.py'
```

If blocked, stop and write a clear blocking note. Otherwise implement, test, and update accepted_changes.
