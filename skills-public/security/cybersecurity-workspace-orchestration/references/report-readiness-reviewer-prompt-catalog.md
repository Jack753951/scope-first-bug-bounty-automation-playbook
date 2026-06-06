> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Report-Readiness Reviewer Prompt Catalog (trial, data-only)

Use this reference when a cybersecurity automation workspace has reached candidate/gap/report-readiness classifiers and wants to improve reviewer consistency without creating a new runtime consumer.

## Safe slice shape

A low-risk first slice is a static JSON prompt catalog keyed to existing report-readiness code vocabularies:

- one flat trial marker such as `report_readiness_reviewer_prompts_v0_trial`
- entries keyed to existing `GATE_*`, `BLOCK_*`, and `CHECK_*` codes
- stable entry IDs, sorted deterministically
- prompt text that asks reviewers for critique/classification, not report drafting
- a closed allowed-response posture set such as:
  - `still_blocked`
  - `still_needs_manual_review`
  - `needs_more_evidence`
  - `defer`

Keep this as data-only. Do not give it a `*/0.1-trial` schema version, validator contract, renderer, artifact consumer, submission adapter, scanner hook, runtime chain wiring, or report-generation path until those boundaries receive separate review.

## Direction-review questions

Before adding this catalog, ask the reviewer to decide:

1. Is a prompt catalog useful now, or is the workflow not ready?
2. Should it remain fixture/data-only, or should reviewer-notes artifacts be designed first?
3. Would any consumer-backed reviewer-notes artifact introduce a fifth stdin/stdout consumer or similar refactor trigger?
4. Are existing gate/block/check codes stable enough to key prompts without adding a new schema?
5. What vocabulary must remain forbidden to avoid status promotion or report drafting?

## Test expectations

Add tests that prove:

- JSON parses and is canonical pretty-printed byte-for-byte.
- Trial marker is a flat marker, not a slash-shaped schema/version.
- `GATE_*`, `BLOCK_*`, and `CHECK_*` coverage matches the existing classifier code sets exactly.
- Response postures are a closed set and do not include promotion/dismissal values.
- Entry IDs are stable, unique, and sorted.
- No drafting/platform/scanner/severity-axis keys exist.
- No URL/callback/live-target flags or target affordance strings appear.
- The test only text-scans upstream constants or uses a narrow data import; it must not wire the catalog into workflow consumers.

Suggested forbidden vocabulary canary:

- `confirmed`
- `exploitable`
- `submit`
- `submission`
- `draft_report`
- `severity`
- `informative`
- `not_applicable`
- `won_t_fix`

## Handoff and validation

Record the slice as data-and-tests-only in `handoff/accepted_changes.md`. Include reviewer route/tool, visible model/runtime limitation if exact runtime is not exposed, focused tests, full script tests, and project review result.

Validation pattern:

```bash
python -m unittest scripts.test_report_readiness_reviewer_prompts scripts.test_report_readiness_gate -v
python -m unittest discover -s scripts -p 'test_*.py'
HACKLAB=<user-home> ./bin/hermes review
```

Adjust paths/commands to the project wrapper, but preserve the focused + full + review rhythm.

## Pitfalls

- Do not treat reviewer prompt catalogs as report generation. They should guide a human/agent reviewer to keep records blocked, needs-manual-review, or needing more evidence.
- Do not add a reviewer-notes artifact, renderer, or consumer in the same low-risk slice unless the review tier explicitly covers that new contract boundary.
- Do not use `informative`, `not_applicable`, or `won_t_fix` as allowed postures in early report-readiness gates; these can become silent dismissal/promotion vocabulary.
- Do not add live target CLI flags or URL-shaped examples to a data-only catalog.
