> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Direction Prompt — P2.20 Candidate Review Packet Gap Report Consumer

Date: 2026-05-18
Proposed tier: T3 workflow/contract consumer review
Worker route preference: Claude Code MAX/OAuth read-only review first; use API-backed Claude only if explicitly justified.

## Context

The long-term project goal is an authorized bug bounty automation platform, not a CTF tool. CTF work is calibration only. P2.19 introduced a trial-only, offline `candidate_review_packet/0.1-trial` builder that reads committed candidate finding fixtures and emits a deterministic review packet. It explicitly does not promote findings, generate reports, touch targets, or wire runtime.

## Proposed P2.20 slice

Build a first downstream consumer for the P2.19 packet: a read-only, stdout-only gap report helper.

Suggested script:

- `scripts/review_candidate_packet_gaps.py`
- focused tests: `scripts/test_candidate_packet_gaps.py`

## Required behavior

The helper should:

1. Read one `candidate_review_packet/0.1-trial` JSON document from stdin.
2. Emit one deterministic `candidate_review_gap_report/0.1-trial` JSON document to stdout.
3. Validate the packet enough to fail closed on malformed JSON, wrong schema version, non-object packet, missing/invalid `findings`, forbidden promoted statuses, and packet-level `status != ok`.
4. Produce per-finding stable gap/action codes such as:
   - `MISSING_EVIDENCE`
   - `LOW_CONFIDENCE`
   - `INFO_SEVERITY_REPORT_BLOCKED`
   - `MANUAL_VERIFICATION_REQUIRED`
   - `SCANNER_OUTPUT_ONLY`
   - `MISSING_REMEDIATION`
   - `MISSING_VERIFICATION_GUIDANCE`
   - `MISSING_SCOPE_REVIEW_QUESTION`
5. Preserve triage-only semantics. The helper may report `reviewer_decision_required` but must never emit `ready`, `approved`, `confirmed`, `verified`, or `accepted` as report/finding status.
6. Reject live-target CLI flags (`--target`, `--url`, `--host`, `--scope`, `--live`) with structured JSON error output.
7. Remain standard-library-only, deterministic, read-only, no output file writes, no network clients, no subprocess, no scanner/module imports, no runner/recon/CI/scheduler/runtime wiring.

## Explicit non-goals

- No schema promotion under `modules/_schema/`.
- No report drafting.
- No platform adapter.
- No target interaction.
- No live scans.
- No status promotion.
- No changes to `config/scope.txt`, credentials, loot, OAuth, deployment, billing, or production settings.

## Review questions

1. Is this the right next step after P2.19, or should P2.20 be even narrower?
2. Are the proposed gap/action codes enough to prove workflow value without overbuilding another schema layer?
3. What blocker conditions should Hermes enforce before accepting implementation?
4. Does this properly redirect from CTF calibration to bug bounty review workflow?

## Expected verdict format

Return a concise direction review with:

- Verdict: ACCEPT / ACCEPT_WITH_CHANGES / REQUEST_CHANGES
- Blocking changes before implementation
- Non-blocking recommendations
- Safety boundary
- Worker route recommendation
