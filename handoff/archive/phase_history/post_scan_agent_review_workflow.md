> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Post-Scan Agent Review Workflow

Date: 2026-05-15
Status: Architectural direction / workflow contract

## Answer

Post-scan review must not rely only on scripts. Scripts/modules produce structured evidence and candidate findings, but agents participate in triage, reasoning, report quality, and workflow decisions.

## Intended Division of Labor

### Scripts / Modules

Responsibilities:

- collect raw observations within authorized scope
- normalize outputs into structured finding candidates
- preserve evidence paths and hashes
- record policy/scope decisions
- avoid claiming confirmed vulnerabilities by themselves

Output status should default to:

```text
candidate
```

not:

```text
confirmed
```

### Hermes

Responsibilities:

- verify authorization/scope/run manifest before analysis
- ensure outputs came from allowed program/profile/modules
- check audit logs for out-of-scope or policy-denied events
- route structured candidates to Claude/Cowork for analysis
- route automation defects to Codex
- maintain handoff and accepted/rejected decisions

### Claude / Cowork

Responsibilities:

- review scan candidates and evidence context
- identify likely false positives or missing proof
- map observations to impact and realistic attack paths
- propose manual verification steps
- draft report language only for verified or verification-ready findings
- distinguish triage observations from confirmed vulnerabilities
- produce analyst notes and route-back requests

### Codex

Responsibilities:

- fix parser/module/report-generator bugs discovered during analysis
- add regression tests and dry-run fixtures
- improve structured output quality
- never reinterpret results as confirmed vulnerabilities without analyst evidence

## Candidate Finding Lifecycle

```text
module output
  -> candidate finding JSON
  -> Hermes scope/run review
  -> Claude/Cowork triage analysis
  -> needs_manual_verification OR rejected_false_positive OR verification_ready
  -> manual verification evidence
  -> verified finding
  -> report draft
  -> final report / submission
  -> retest tracking
```

## Required Review Artifacts

For each non-trivial scan run:

```text
runs/<run_id>/run.json
runs/<run_id>/audit.log
runs/<run_id>/outputs/
runs/<run_id>/findings/candidates/*.json
handoff/analysis_<run_id>.md
handoff/report_review_<run_id>.md
```

Claude/Cowork should write `handoff/analysis_<run_id>.md` with:

- scope/run summary
- candidate finding table
- evidence quality assessment
- likely false positives
- recommended manual verification steps
- impact hypotheses
- reportability decision
- route-back items for Codex

## Safety Rules

- No automated finding becomes `verified` without human/operator-approved evidence.
- No report should be generated directly from raw scanner output.
- Agent analysis must cite local evidence paths and run IDs.
- Any out-of-scope evidence is quarantined and not used for reporting.
- If evidence includes secrets/tokens/PII, Hermes routes to redaction before analysis.

## Long-Term Goal

Scripts provide repeatability and coverage. Agents provide reasoning, prioritization, false-positive reduction, impact analysis, and report quality. The project should combine both rather than replacing analyst judgment with scanner output.
