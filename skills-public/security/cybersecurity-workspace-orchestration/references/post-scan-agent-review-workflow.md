> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Post-Scan Agent Review Workflow

Use this reference for authorized cybersecurity labs where scan/module output must be reviewed by agents rather than treated as final truth.

## Principle

Scripts and modules provide repeatable collection and normalization. Agents provide triage reasoning, false-positive reduction, impact analysis, manual verification planning, and report-quality review.

Automated scanner/module output should default to `candidate`, not `confirmed`.

## Division of Labor

### Scripts / Modules

- Collect observations only within authorized scope.
- Normalize outputs into structured candidate findings.
- Preserve local evidence paths and hashes.
- Record policy/scope decisions and run metadata.
- Do not claim confirmed vulnerabilities by themselves.

### Hermes

- Verify authorization, program scope, run manifest, and audit log integrity before analysis.
- Ensure outputs came from allowed program/profile/modules.
- Check for out-of-scope or policy-denied events.
- Route structured candidates to Claude/Cowork for analysis.
- Route automation defects to Codex.
- Maintain handoff and accepted/rejected decisions.

### Claude / Cowork

- Review candidate findings and evidence context.
- Identify likely false positives and missing proof.
- Map observations to plausible impact and attack paths.
- Propose manual verification steps.
- Draft report language only for verified or verification-ready findings.
- Distinguish triage observations from confirmed vulnerabilities.
- Produce analyst notes and route-back requests.

### Codex

- Fix parsers, module output, fixtures, report generators, and validators.
- Add regression tests and dry-run fixtures.
- Do not reinterpret scanner output as confirmed vulnerability without analyst evidence.

## Candidate Lifecycle

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

## Recommended Artifacts

For each non-trivial run:

```text
runs/<run_id>/run.json
runs/<run_id>/audit.log
runs/<run_id>/outputs/
runs/<run_id>/findings/candidates/*.json
handoff/analysis_<run_id>.md
handoff/report_review_<run_id>.md
```

Claude/Cowork analysis should include:

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
- Out-of-scope evidence is quarantined and not used for reporting.
- Evidence containing secrets/tokens/PII must be routed to redaction before analysis.
