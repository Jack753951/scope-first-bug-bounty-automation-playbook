> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code Implementation Task — P3.12 SOC Reviewer-Gap Catalog Only

Status: READY_FOR_CLAUDE_IMPL
Date: 2026-05-20
Prepared by: Hermes
Route: Claude Code MAX/OAuth via `CLAUDE_IMPL_MAX_TURNS=35 HACKLAB=$(pwd) ./bin/hermes claude-impl`
Source direction prompt: `handoff/cowork_soc_reviewer_gap_catalog_direction_prompt.md`
Source direction review: `handoff/cowork_soc_reviewer_gap_catalog_direction_review.md`
Expected named result: `handoff/claude_code_result_p3_12.md`
Expected rolling result: `handoff/claude_code_result.md`

## Objective

Implement the Cowork-approved T2 catalog-only slice:

`P3.12 — SOC reviewer-gap catalog only (offline, non-contractual; co-located with P3.11 fixture)`

This is a static companion catalog calibrated against the existing P3.11 synthetic fixture. It must not become a runtime consumer, schema, report gate, SIEM integration, platform adapter, or target-touching workflow.

## Required reading before edits

Read:

- `.hermes.md`
- `handoff/cowork_soc_reviewer_gap_catalog_direction_review.md`
- `handoff/cowork_soc_reviewer_gap_catalog_direction_prompt.md`
- `handoff/active_strategy_queue.md`
- `handoff/accepted_changes.md`
- `fixtures/soc_evidence_bucket/README.md`
- `fixtures/soc_evidence_bucket/sample_timeline_01.json`
- `scripts/test_soc_evidence_bucket_fixture.py`
- `notes/daily/2026-05-20.md`

## Required implementation

Create only the approved catalog/docs/test/handoff slice.

### Create

1. `fixtures/soc_evidence_bucket/reviewer_gap_catalog.md`

Must state clearly:

- P3.12 SOC reviewer-gap catalog only
- synthetic, trial, non-contractual, offline, non-promotional, calibration-only
- not a contract and not a schema
- companion artifact only; source vocabulary remains the P3.11 fixture/test
- not loaded by runtime consumers
- not wired into chain consumers, report-readiness gate, modules, recon, scanner adapters, SIEM, platform adapters, run manifests, or reviewer-answer capture
- `templates/report_readiness_reviewer_prompts.json` is only a parallel pattern reference, not a dependency or replacement
- no real lab data, credentials, simulator hashes, captured logs, real domains, real public IPs, platform URLs, or loot-class data may be substituted

2. `fixtures/soc_evidence_bucket/reviewer_gap_catalog.json`

Static pretty-printed JSON. Top-level keys:

- `schema_marker`: literal flat string `soc_reviewer_gap_catalog_v0_trial` (no slash)
- `version`: `0`
- `entries`: exactly 12 entries, sorted by `id`, exactly one per existing P3.11 gap code

Each entry:

- `id`: stable snake_case, prefix `p3_12_prompt_`
- `gap_code`: exactly one of the P3.11 allowed gap codes
- `prompt_text`: short neutral evidence-completeness question, not report/submission/severity language
- `allowed_response_postures`: non-empty subset of the existing non-promotional statuses
- optional `metadata`: small flat map only if useful; avoid nested complexity

Allowed gap codes, copied from P3.11 only:

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

Allowed non-promotional statuses, copied from P3.11 only:

- `needs_more_evidence`
- `needs_mapping_review`
- `needs_asset_reconciliation`
- `needs_second_pass_hunt`
- `not_report_ready`

3. `scripts/test_soc_reviewer_gap_catalog.py`

Use standard library `unittest` only. Preferred imports: `json`, `pathlib`, `re`, `unittest`.

The test must assert:

- JSON parses and has required top-level shape
- `schema_marker` is flat, equals `soc_reviewer_gap_catalog_v0_trial`, includes `trial`, and contains no `/`
- `version` is `0`
- entry ids are unique, sorted, snake_case, and prefixed `p3_12_prompt_`
- exactly 12 entries and exactly one per allowed gap code
- gap-code set is byte-equal / drift-locked to the P3.11 fixture/test vocabulary; do not import runtime consumers or create constants modules
- `allowed_response_postures` is non-empty and subset of the P3.11 non-promotional statuses
- `prompt_text` is non-empty, short, neutral, no URL scheme, no scanner/SIEM/platform name, no severity/CVSS/impact axis, no submission/lifecycle/promotional vocabulary
- JSON round-trip is stable with `json.dumps(data, sort_keys=True, indent=2) + "\n"`
- test imports only standard-library modules and does not reference runtime/chain consumers such as `build_candidate_review_packet`, `review_candidate_packet_gaps`, `build_candidate_verification_plan`, `build_report_readiness_gate`, `build_candidate_workflow_fixture`, `module_runner`, or `recon`
- Markdown sibling exists and contains required posture phrases: `synthetic`, `non-promotional`, `not a contract`, `offline`, `companion artifact`, and a sentence that `templates/report_readiness_reviewer_prompts.json` is a parallel pattern reference only
- Markdown contains no URL scheme, scanner name, SIEM endpoint, or real platform domain
- comment/docstring states that adding a gap code to catalog without fixture vocabulary, or vice versa, must fail closed

### Modify

4. `handoff/active_strategy_queue.md`

Update after implementation to record:

- P3.12 catalog-only slice accepted/implemented if validation passes
- P3.12 remains static fixture/catalog/test only
- trial-consumer design remains deferred behind fresh direction review
- no runtime/schema/report/gate promotion is approved

5. `handoff/accepted_changes.md`

Append only. Add a P3.12 entry with:

- worker route/tool and visible runtime/model limitation if not exposed
- files created/modified
- validation commands run and results
- safety boundary
- source Cowork review

6. `notes/daily/2026-05-20.md`

Append a short P3.12 implementation note with the same safety boundary.

7. `handoff/claude_code_result_p3_12.md`

Write a named result summary with:

- route/tool and visible model/runtime limitation if not exposed
- files changed
- RED/GREEN or equivalent validation evidence
- safety boundaries honored
- deferred follow-ups

## Hard forbidden surfaces

Do not touch or create changes under:

- `config/scope.txt`
- `programs/`
- `modules/`
- `modules/_schema/`
- `templates/`
- `reports/`
- `loot/`
- `scans/`
- `runs/`
- runtime code such as `recon.sh`, `scripts/module_runner.py`, validators, policy helpers, report generators, scanner wrappers, adapters, schedulers, OAuth/deployment/billing settings

Do not run:

- live scans, probes, scanners, modules
- exploit/fuzz/brute force
- callbacks/OAST
- proxy/pivot/tunnel
- target-touching automation
- external service calls

Do not add:

- SIEM/Elastic/Kibana/Splunk integration
- schema promotion
- runtime consumer
- reviewer-answer capture
- report drafting/submission
- platform adapter

## Required validation before reporting done

Run and record:

```bash
python -m unittest scripts.test_soc_reviewer_gap_catalog
python -m unittest scripts.test_soc_evidence_bucket_fixture
python -m unittest discover scripts
git diff --check
HACKLAB=$(pwd) ./bin/hermes review
```

Also perform a local added-file or diff scan for forbidden live/action strings and record the result.

Keep the slice narrow. If implementation appears to require any forbidden surface, stop and write a blocking note instead.
