> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# SOC Reviewer-Gap Catalog (P3.12)

This file is the **P3.12 SOC reviewer-gap catalog only** companion artifact.
It is **synthetic**, **trial**, **non-contractual**, **offline**,
**non-promotional**, and **calibration-only**.

It is **not a contract** and **not a schema**. It is a companion artifact
only; the source vocabulary remains the P3.11 fixture and its sibling test.

## Posture (binding)

- The catalog is **synthetic**, **trial**, **non-contractual**, **offline**,
  **non-promotional**, and **calibration-only**.
- The catalog is **not a contract** and **not a schema**.
- The catalog is a **companion artifact** only. The source of truth for the
  SOC gap-code vocabulary and the SOC non-promotional status vocabulary
  lives in `fixtures/soc_evidence_bucket/sample_timeline_01.json` and its
  sibling test `scripts/test_soc_evidence_bucket_fixture.py`.
- The catalog is **not loaded by any runtime consumer**. The only consumer
  is the sibling test `scripts/test_soc_reviewer_gap_catalog.py`, which
  asserts well-formedness and vocabulary equality with the P3.11 fixture.
- The catalog **must not be wired** into any chain consumer
  (`scripts/build_candidate_review_packet.py`,
  `scripts/review_candidate_packet_gaps.py`,
  `scripts/build_candidate_verification_plan.py`,
  `scripts/build_report_readiness_gate.py`,
  `scripts/build_candidate_workflow_fixture.py`, or any future consumer),
  the report-readiness gate, modules, the recon runtime, scanner adapters,
  any SIEM / Elastic / Kibana / Splunk log-aggregation integration, run
  manifests, module manifests, platform adapters, or any reviewer-answer
  capture surface without a fresh T3+ direction review.
- The data file is deliberately a **flat-marker** JSON document
  (`schema_marker: "soc_reviewer_gap_catalog_v0_trial"`); it is **not** a
  `*/0.1-trial` schema. No validator script reads it; only the sibling
  test under `scripts/` reads it.
- Reviewer-answer / reviewer-notes capture remains **deferred** to a
  separate future direction review. The catalog records *questions to ask*,
  never *answers given*.

## Relationship to `templates/report_readiness_reviewer_prompts.json`

The P3.5 catalog at `templates/report_readiness_reviewer_prompts.json` is a
**parallel pattern reference only**. The SOC reviewer-gap catalog does not
replace, extend, depend on, or wire into the P3.5 catalog, its sibling test,
or the report-readiness gate consumer. The two catalogs share only a
*pattern* (a closed gap/code list paired with a short neutral prompt and a
closed allowed-response-posture set); they do **not** share a contract.

## Per-entry shape

Each entry in `reviewer_gap_catalog.json` carries:

- `id` — a stable, snake_case identifier prefixed `p3_12_prompt_`. Entries
  are sorted by `id`.
- `gap_code` — exactly one of the in-fixture P3.11 gap codes. Exactly one
  entry exists per allowed gap code.
- `prompt_text` — a short, neutral, evidence-completeness question. It must
  not read as a report-readiness gate, a submission-readiness check, a
  severity assessment, or a detection-rule trigger.
- `allowed_response_postures` — a non-empty subset of the in-fixture
  non-promotional status vocabulary.
- `metadata` (optional) — a small flat map only if useful. Nested
  complexity is avoided.

## Allowed in-fixture gap-code vocabulary

The catalog mirrors exactly the gap codes already exercised by the P3.11
fixture and its sibling test. Adding a gap code to this catalog without
also adding it to the fixture vocabulary, or vice versa, must fail closed
under the sibling test.

- `MISSING_HOST_IOC`
- `MISSING_NETWORK_IOC`
- `MISSING_HASH`
- `MISSING_SOURCE_URL`
- `MISSING_DESTINATION_PATH`
- `MISSING_COMMAND_LINE`
- `MISSING_FOLLOW_ON_IMPLICATION`
- `PARENT_TECHNIQUE_TOO_BROAD`
- `TACTIC_MISMATCH`
- `ASSET_ROLE_AMBIGUOUS`
- `TIMESTAMP_EVENT_ROLE_MISMATCH`
- `NEEDS_SECOND_PASS_HUNT`

## Allowed in-fixture non-promotional status vocabulary

`allowed_response_postures` for each entry is a non-empty subset of:

- `needs_more_evidence`
- `needs_mapping_review`
- `needs_asset_reconciliation`
- `needs_second_pass_hunt`
- `not_report_ready`

These statuses are deliberately non-promotional so that a catalog entry
cannot read as a ready-to-submit finding gate.

## Forbidden substitutions

The catalog must not substitute any of the following:

- real lab data, credentials, simulator hashes, captured logs;
- real domains, real public IPs, real bug-bounty platform URLs;
- loot-class data;
- scanner names, SIEM endpoints, real platform domains;
- URL schemes of any kind;
- severity, CVSS, impact, lifecycle, or submission-readiness vocabulary.

## What this catalog is **not** for

- Not a runtime input to any module, runner, scanner, recon stage, report
  generator, scope helper, scheduler, or external platform.
- Not a schema. No promotion to `modules/_schema/`, no `*/0.1-trial`
  document, no module manifest field, no run-manifest field.
- Not a SIEM payload. No Elastic / Kibana / Splunk / log-aggregation
  integration may consume this catalog.
- Not a finding template. No HTML / Markdown / submission rendering may
  reference this catalog as a starting payload.
- Not a reviewer-answer capture artifact. The catalog records *questions
  to ask*, never *answers given*.

## Re-trigger conditions for a fresh direction review

A fresh T3+ direction review is required before any of the following can
be considered:

- Promoting any field above into a runtime contract, schema, module
  manifest, run manifest, or report-readiness gate.
- Wiring the catalog into any candidate-workflow consumer, the
  report-readiness gate, any module runner, any validator, any recon
  code, any scanner adapter, any SIEM path, any platform adapter, or any
  reviewer-notes capture surface.
- Harmonizing the SOC gap-code vocabulary with the report-readiness
  gate's `GATE_*` / `BLOCK_*` / `CHECK_*` vocabulary.
- Adding a reviewer-answer / reviewer-notes capture artifact.
- Substituting any real lab, simulator, or bug-bounty platform data.
