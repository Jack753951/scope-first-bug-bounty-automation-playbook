> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Direction Review — P2.20 Candidate Review Packet Gap Report Consumer

Date: 2026-05-18
Route: independent read-only third-party review via Hermes delegate_task
Verdict: ACCEPT_WITH_CHANGES

## Summary

P2.20 is the right next step after P2.19. It redirects the project from CTF calibration back to the authorized bug bounty review workflow by adding the first downstream consumer for `candidate_review_packet/0.1-trial`.

The slice is acceptable if implementation remains strictly offline/read-only/stdin-to-stdout and consumes only the packet fields already emitted by P2.19.

## Blocking changes before implementation

1. Define a deterministic structured JSON error contract for malformed JSON, wrong schema version, non-object packets, `status != ok`, non-empty packet errors, missing/invalid findings, promoted statuses, and live-target flags. Do not rely on argparse stderr/tracebacks.
2. Keep CLI strictly stdin-to-stdout. Do not add `--input`, `--repo-root`, output paths, fixture paths, or file read/write options. Unknown args and live-target flags must fail closed with JSON error output.
3. Make the output a gap/action report only, not a bug bounty submission report draft. Do not emit Markdown, report prose, impact/repro/remediation rewrites, platform-specific wording, or submission-ready text.
4. Preserve status boundaries. Output must never use `ready`, `approved`, `confirmed`, `verified`, or `accepted`; highest allowed workflow state is `reviewer_decision_required` / `not_ready` / `blocked` / `needs_manual_review` style language.
5. Validate `schema_version == candidate_review_packet/0.1-trial`, reject packet-level `status != ok`, and reject non-empty packet `errors` even if status says ok.
6. Derive gap/action codes only from packet fields. Do not read targets, DNS, HTTP, runtime artifacts, config/scope.txt, scanner/module output, or evidence files.
7. Tests must include AST/static safety guards for no network clients, subprocess/process launch, file writes, scanner/module/runtime imports, schema promotion, CI/hook/scheduler/recon wiring, and live/report-promotion semantics.

## Accepted gap/action code direction

- `MISSING_EVIDENCE`
- `LOW_CONFIDENCE`
- `INFO_SEVERITY_REPORT_BLOCKED`
- `MANUAL_VERIFICATION_REQUIRED`
- `SCANNER_OUTPUT_ONLY`
- `MISSING_REMEDIATION`
- `MISSING_VERIFICATION_GUIDANCE`
- `MISSING_SCOPE_REVIEW_QUESTION`

`MISSING_SCOPE_REVIEW_QUESTION` should be derived from fixed packet review question keys such as `scope_in_authorized_scope`, not by checking real scope.

## Recommended output shape

- `schema_version: candidate_review_gap_report/0.1-trial`
- `status: ok | error`
- `source_schema_version`
- `summary`
- `finding_gaps[]`
- `errors[]`

Keep it trial-only. Do not create JSON Schema yet.

## Safety boundary

No schema promotion, no formal report drafting, no vulnerability confirmation, no live scans, no target interaction, no scope/config/credentials/loot/runs/scans/evidence reads, no output file writes, no network, no subprocess, no scanner/module/runtime imports, no CI/scheduler/runner/recon/platform-adapter wiring, and no production/OAuth/billing/deployment changes.

## Worker route recommendation

Use Claude Code MAX/OAuth implementation plus Hermes verification. No API-backed Claude needed.
