> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Direction Prompt — P3.12 SOC Reviewer-Gap Catalog Only

Status: READY_FOR_COWORK_DIRECTION_REVIEW
Date: 2026-05-20
Prepared by: Hermes
Route: Claude/Cowork read-only design review via `hermes cowork`
Depends on: P3.11 accepted fixture-only SOC evidence-bucket slice

## Objective

Run a design-only direction review for the next safe SOC-related slice after P3.11:

`P3.12 — SOC reviewer-gap catalog only (static Markdown/JSON candidate; no consumer)`

The goal is to decide whether to create a small static catalog of reviewer/evidence-gap codes and reviewer questions calibrated against the synthetic P3.11 fixture, while keeping every runtime, schema, report, SIEM, scanner, and target-touching surface deferred.

## Current context

Read before deciding:

- `.hermes.md`
- `handoff/active_strategy_queue.md`
- `handoff/cowork_soc_evidence_bucket_direction_review.md`
- `handoff/third_party_p3_11_implementation_review.md`
- `handoff/claude_code_result_p3_11.md`
- `fixtures/soc_evidence_bucket/README.md`
- `fixtures/soc_evidence_bucket/sample_timeline_01.json`
- `scripts/test_soc_evidence_bucket_fixture.py`
- `handoff/active_testing_policy.md`
- `handoff/oss_recon_gate.md`
- `handoff/review_tiering_policy.md`
- `handoff/multi_party_review_decision_policy.md`

## Decision options

Choose exactly one primary option:

1. `PROCEED_CATALOG_ONLY`
   - Allow a static reviewer-gap catalog as Markdown and/or JSON data under a non-runtime location such as `fixtures/soc_evidence_bucket/` or `templates/` only if clearly marked trial/non-contractual.
   - Allow sibling standard-library tests that validate non-promotional vocabulary, no live/action strings, no report-ready language, and no runtime imports/wiring.
   - No executable consumer beyond tests.

2. `PROCEED_MARKDOWN_ONLY`
   - Allow only a Markdown catalog/explanation and defer JSON/testable data until a later review.

3. `DEFER_AND_CLOSE_SOC_THREAD`
   - Do not add a catalog now; return to another mainline platform slice.

4. `BLOCK`
   - Block because the catalog would prematurely promote vocabulary, overfit simulator feedback, or risk report/schema/runtime coupling.

5. `REQUEST_OPERATOR_INPUT`
   - Ask for a specific artifact or decision that cannot be safely inferred from current repo context.

## Required analysis

Please include:

1. Review tier classification and authority level.
2. Whether OSS Recon Gate is required or only informational for this slice.
3. Risks of vocabulary promotion, schema creep, report-readiness creep, and runtime coupling.
4. If proceeding, exact allowed files/locations and exact forbidden files/locations.
5. Minimum validation expectations.
6. Whether Claude implementation should use the adjusted temporary turn budget convention:
   - keep repo default `CLAUDE_IMPL_MAX_TURNS=25`
   - for fixture/test/handoff-heavy offline slices, invoke as `CLAUDE_IMPL_MAX_TURNS=35` or `CLAUDE_IMPL_MAX_TURNS=40 HACKLAB=$(pwd) ./bin/hermes claude-impl`
   - do not raise the global default unless repeated slices show the default is systematically too low.
7. A final Multi-Party Review Decision block.

## Hard boundary

This review is design-only/read-only. Do not implement code or edit files during the Cowork review itself.

Do not approve or perform:

- live SIEM/Elastic/Kibana/Splunk integration
- scanner/module execution
- recon/runtime wiring
- runtime consumer
- schema promotion
- report drafting/submission
- platform adapter
- target interaction
- scope/config changes, including `config/scope.txt`
- credentials, loot, OAuth, deployment, billing, scheduler, CI, or production settings
- proxy/pivot/tunnel/callback/OAST behavior

If any of those are needed, return `BLOCK` or `REQUEST_OPERATOR_INPUT`.
