> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P2.21 Direction Prompt — Candidate Verification Checklist Consumer

Review tier: T2/T3 boundary-adjacent offline workflow consumer
Milestone: Phase 2 bug-bounty candidate review workflow closeout path
Route preference: Claude Code MAX/OAuth or Hermes delegate read-only review; no API-backed Claude needed unless ambiguity remains.

## Context

P2.19 created a trial-only `candidate_review_packet/0.1-trial` builder from committed candidate finding fixtures. P2.20 created a trial-only stdin/stdout gap/action consumer emitting `candidate_review_gap_report/0.1-trial`.

The Phase 2 exit estimate says the next useful slice is a verification plan/checklist consumer before any report-readiness gate or end-to-end workflow fixture.

## Proposed slice

Add one offline/stdin-to-stdout trial consumer:

```text
scripts/build_candidate_verification_plan.py
scripts/test_candidate_verification_plan.py
```

It should consume exactly one `candidate_review_gap_report/0.1-trial` JSON document from stdin and emit deterministic `candidate_verification_plan/0.1-trial` JSON to stdout.

## Required boundary

- No live scans or target interaction.
- No file input/output options.
- No output file writes.
- No network clients.
- No subprocess/process launch.
- No scanner/module runtime imports.
- No reading targets, DNS, HTTP, config/scope.txt, runs, scans, loot, evidence files, or credentials.
- No schema promotion under `modules/_schema`.
- No report drafting, Markdown/HTML/PDF, platform adapters, report titles, impact prose, repro prose, or remediation rewriting.
- No status promotion to confirmed/verified/accepted/approved/ready.
- Reject all CLI args, including live target affordances such as `--target`, `--url`, `--host`, `--scope`, and `--live`, with structured JSON errors.

## Desired output shape

```json
{
  "schema_version": "candidate_verification_plan/0.1-trial",
  "status": "ok | error",
  "source_schema_version": "candidate_review_gap_report/0.1-trial",
  "summary": {
    "finding_count": 0,
    "blocked_count": 0,
    "needs_manual_review_count": 0,
    "check_item_count": 0,
    "source_gap_code_counts": {}
  },
  "verification_plans": [
    {
      "finding_id": "...",
      "target_value": "...",
      "module_id": "...",
      "plan_state": "blocked | needs_manual_review",
      "check_items": [
        {
          "code": "...",
          "source_gap_code": "...",
          "action_kind": "...",
          "prompt": "..."
        }
      ]
    }
  ],
  "errors": []
}
```

Allowed plan states should stay below confirmation language: `blocked` and `needs_manual_review` are acceptable. Do not use `ready`, `approved`, `confirmed`, `verified`, or `accepted`.

## Suggested source-gap mapping

- `MISSING_EVIDENCE` -> require collecting/redacting evidence in an authorized manual step before any report draft.
- `LOW_CONFIDENCE` -> require reproducing or corroborating the observation manually.
- `INFO_SEVERITY_REPORT_BLOCKED` -> require severity/risk rationale or keep as informational note.
- `MANUAL_VERIFICATION_REQUIRED` -> require explicit human verification notes.
- `SCANNER_OUTPUT_ONLY` -> require non-scanner corroboration.
- `MISSING_REMEDIATION` -> require human remediation guidance, not auto-generated prose.
- `MISSING_VERIFICATION_GUIDANCE` -> require a safe manual verification checklist.
- `MISSING_SCOPE_REVIEW_QUESTION` -> require explicit authorized-scope review question before any next action.

## Required tests

- Happy path from P2.19 builder -> P2.20 gap consumer -> P2.21 checklist consumer.
- Deterministic repeated output.
- Wrong source schema, source status not ok, source errors present, malformed stdin, non-object input, missing/invalid `finding_gaps`.
- Reject promoted review states / forbidden output words.
- Reject all positional/unknown CLI args and live target flags with structured JSON errors and no stderr.
- AST/static guards for no network, subprocess, file writes, file reads, scanner/runtime imports, schema promotion, report drafting, or platform/live affordances.

## Acceptance boundary

This slice should prove the trial packet/gap vocabulary supports a second downstream bug-bounty workflow consumer without turning into a report generator or target-touching runtime. Keep it trial-only and defer report-readiness gate / end-to-end workflow fixture to later P2.22/P2.23.
