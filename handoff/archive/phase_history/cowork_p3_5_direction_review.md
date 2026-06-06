> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.5 Direction Review — Report-Readiness Reviewer Prompts

Date: 2026-05-19
Reviewer route/tool: Claude/Cowork in the Claude Code CLI session attached to this repository (no `hermes claude-impl` envelope was generated for this direction-review turn; the review was performed inline against the working tree under read-only tooling). The visible runtime/tool is the Claude Code CLI; the exact backing API/runtime version is not exposed by the tool surface.
Visible model/runtime model: Claude Opus 4.7 (per the session's own self-reported model id `claude-opus-4-7`). The exact runtime/runner identifier inside Anthropic's hosting is not exposed by the tool surface; this is the strongest model identification available without crossing a tool-output boundary.
Review tier: T3 direction review + OSS Recon Gate, design-only.
Milestone: Phase 3, candidate slice 5 (after P3.1 curated fixtures, P3.2 terminal-state matrix, P3.3 two-module discovery coverage, P3.4-alt runner-indifference coverage).
Source prompt: `handoff/cowork_p3_5_direction_prompt.md`.
Predecessors: `handoff/cowork_p2_25_closeout_review.md` (lines 309-329, the original P3.3 framing for reviewer prompts), `handoff/cowork_p3_1_direction_review.md`, `handoff/cowork_p3_3_direction_review.md`, `handoff/cowork_p3_4_direction_review.md`, `handoff/cowork_p2_24_direction_review.md`.

Decision: APPROVE_WITH_CHANGES.

## Executive Summary

Proceed with P3.5, but cut the slice to its smallest correct shape: **a static JSON prompt catalog plus tests-only coverage assertions, with no new script, no new schema, no new artifact, no reviewer-notes contract, and no consumer**. The trial reviewer-notes artifact proposed as the prompt's optional item 2 should be **DEFERRED to a later, separately reviewed slice**; landing it now would either require a fifth stdin consumer (firing one of the P2.24 revisit triggers), or a new `*/0.1-trial` schema under `modules/_schema/**` (forbidden by the prompt and by P2.25), or fixture material with nothing to consume it (sunk cost). None of those is justified by the value the prompts alone deliver.

The catalog must key entries by the exact gate-action codes (`GATE_*`), block-reason codes (`BLOCK_*`), and check-item codes (`CHECK_*`) already emitted by the P2.19→P2.23 chain — concretely the constants `GATE_ACTION_ORDER`, `BLOCK_REASON_ORDER`, and the keys of `CHECK_TO_ACTION` in `scripts/build_report_readiness_gate.py` (lines 30-74) and the corresponding emitter `scripts/review_candidate_packet_gaps.py`. The prompts are reviewer-checklist text only: they may ask a human to assess evidence sufficiency, scope ambiguity, duplicate/chain relationship, remediation clarity, manual verification readiness, and whether the candidate should remain `blocked` / `needs_manual_review` / `not_ready`. They must not draft report titles, summaries, impact narratives, reproduction steps, remediation prose for reporting, or submission text.

Format is JSON, not YAML. The chain is otherwise JSON-only; introducing YAML would require a non-stdlib parser, deviate from the project's standard-library-only validator posture, and split the test surface. The `templates/ctf_verifier_metadata.yaml` precedent is explicitly self-described as "NON-BINDING, UNVERSIONED template (P2.18 trial)" with no parser; it is not a precedent for adding YAML to the active chain.

P2.24 refactor revisit is **not triggered** by this slice as scoped here, because no consumer, no fifth `_compact_emit` clone, no new `_argv_errors` clone, no new `LIVE_TARGET_FLAGS` clone, no new error envelope, and no new file-reading consumer is added. The catalog is data; the tests are validations of data. If a future slice proposes a reviewer-notes *consumer*, that proposal becomes a P2.24 trigger candidate and must route through a fresh direction review.

The OSS Recon Gate yields APPROVE on the prompts-only boundary: each compared reference contributes a check-shape idea (evidence sufficiency, dedupe question, severity rationale, scope question) without contributing a lifecycle, level vocabulary, scanner-confirmed semantic, or platform-submission affordance. Every reference's promotion-flavored vocabulary is hard-rejected.

## OSS Recon Gate Notes

Review tier: T3. Milestone: Phase 3, slice 5. Method: design-only comparison; no third-party code imported, no live target touched, no scanner shape adopted. All comparisons are at the reviewer-checklist conceptual layer, not at the platform/importer layer.

- **<bug-bounty-platform> — public disclosure shape and reviewer-side triage language.**
  - Useful pattern: triage reviewers ask, per finding, about evidence completeness, target-in-scope confirmation, impact rationale, duplicate relationship to existing reports, and remediation clarity. Public reports use fields like `title`, `severity`, `impact`, `steps_to_reproduce`, `affected_asset`, `evidence`, `remediation`, plus a duplicate/lifecycle state.
  - Adopt: the *category of reviewer questions* (evidence completeness, scope confirmation, duplicate relationship, remediation clarity) maps cleanly onto our existing `GATE_*` and `CHECK_*` codes. The catalog's prompt text should ask the human those questions in plain language, anchored to our codes.
  - Adapt: rephrase questions so they ask about reviewer *decision posture* (does this stay blocked, does it stay needs-manual-review, does it need more evidence, defer it) rather than about a forward-looking *report draft*. A <bug-bounty-platform> reviewer ends a triage pass by deciding the report's *state*; our prompts end by deciding the *gate state* and explicitly do not produce draft text.
  - Ignore / hard-reject: every <bug-bounty-platform> *state vocabulary* item (`new`, `triaged`, `duplicate`, `informative`, `not-applicable`, `resolved`, `disclosed`, `bounty awarded`, etc.) and every <bug-bounty-platform> *submission affordance* (title field, impact narrative field, steps-to-reproduce field framed for write-up, severity selector). None may appear in catalog entries, prompt text, allowed-response enums, test strings, or docs. The catalog must not have a `title` slot, an `impact` slot, a `summary` slot, or a `steps_to_reproduce` slot; those are drafting surfaces, not reviewer checks.
  - Contract impact: none. No schema or chain output changes.

- **Bugcrowd — VRT (Vulnerability Rating Taxonomy) and submission triage style.**
  - Useful pattern: VRT formalizes the *kind* of vulnerability and a recommended severity; Bugcrowd's submission flow asks reviewers to confirm category, scope match, demonstrability, and impact. VRT itself is a taxonomy of categories, not a lifecycle.
  - Adopt: nothing new at the contract layer. The taxonomy is more granular than our `severity_hint` and our `classifications` arrays already cover the CWE-style classification dimension. The reviewer *workflow* idea — confirm category, confirm scope, confirm demonstrability — is already encoded by our existing `CHECK_*` codes (`CHECK_MISSING_EVIDENCE`, `CHECK_SCOPE_REVIEW_QUESTION`, `CHECK_MANUAL_VERIFICATION_NOTES`, `CHECK_NON_SCANNER_CORROBORATION`).
  - Adapt: prompts may borrow Bugcrowd's *reviewer-question phrasing style* (short, decisional, oriented at "is this still triage-ready" rather than "is this exploitable in the wild") for the catalog text.
  - Ignore / hard-reject: VRT category enumeration imports (no `vrt_category` field, no `vrt_id` field, no `bugcrowd_*` field), all Bugcrowd submission lifecycle states (`not-applicable`, `triaged`, `resolved`, `won't-fix`, `out-of-scope`, `duplicate`), and any "recommended payout" / "recommended severity" affordance. None may appear in the catalog.
  - Contract impact: none.

- **DefectDojo — finding lifecycle and importer model.**
  - Useful pattern: DefectDojo exposes a lifecycle for each imported finding (`active`, `verified`, `false_p`, `risk_accepted`, `out_of_scope`, `mitigated`) plus an engagement/test/product hierarchy and dedupe-hash strategy. Reviewers move findings through the lifecycle.
  - Adopt: nothing. The lifecycle is precisely the promotion vocabulary the chain's whole point is to refuse to introduce until manual verification policy is drafted (per `handoff/cowork_p2_25_closeout_review.md` deferrals 2 and 3).
  - Adapt: the *concept* that a reviewer answers a structured question and the answer changes future filtering may be borrowed *only as a future Phase 3+ direction question*, not implemented in P3.5. Capture it as a non-blocking recommendation; do not act on it.
  - Ignore / hard-reject: every DefectDojo lifecycle string (`verified`, `false_p`, `risk_accepted`, `mitigated`, `out_of_scope`, `active`) and every DefectDojo importer field (`engagement`, `test`, `product`, `tags`, `dedupe_hash`). The catalog must not have an `accepted` enum value, a `mitigated` enum value, a `verified` enum value, or a `false_positive` enum value. If reviewers need a "this is not actually a finding" answer, the existing chain already encodes that as `BLOCK_INFO_SEVERITY` + `GATE_KEEP_OUT_OF_REPORT`; map there, do not invent `false_positive`.
  - Contract impact: none.

- **SARIF — result, suppression, baseline, and review concepts.**
  - Useful pattern: SARIF separates `result.level` (`note` / `warning` / `error`) from `result.kind` (`pass` / `fail` / `open` / `informational` / `review`); supports `suppressions[]` with justifications; supports `baselineState` (`new` / `unchanged` / `updated` / `absent`); a reviewer marks results for suppression with structured justification text.
  - Adopt: the *idea* of "reviewer answer carries a structured justification field bound to a stable code" is exactly what the prompt catalog supports — each entry's `prompt_text` is the question, the reviewer's hypothetical answer is the justification, and the binding is to our `GATE_*` / `BLOCK_*` / `CHECK_*` codes (analogous to a SARIF `rule.id`).
  - Adapt: catalog entries should expose a small, closed set of *response postures* (e.g., `still_blocked`, `still_needs_manual_review`, `needs_more_evidence`, `defer`) that a future reviewer-notes consumer could one day record. These are *vocabulary placeholders* for a future slice; P3.5 only writes them into the catalog as the allowed answer set, it does not create an artifact that records them today.
  - Ignore / hard-reject: SARIF's `result.kind: fail`, `pass`, `open` — these are promotion-flavored and must not appear in catalog entries, prompt text, allowed-response enums, test assertion strings, or docs. SARIF's `result.level` (`note`/`warning`/`error`) must not be conflated with our `severity_hint` (`informational`/`low`/`medium`/`high`/`critical`); the catalog must not introduce a `level` field, a `severity` field, or a `level` enum. SARIF's `baselineState` is also out of scope: it would imply a baseline-diff behavior we have not built. SARIF's `suppressions[]` schema must not be copied as a field; catalog entries do not record suppression justifications, because no consumer exists to record them and creating one is deferred.
  - Contract impact: none.

- **OWASP ASVS / WSTG — reviewer-checklist style.**
  - Useful pattern: ASVS lists verification *requirements* per security control area; WSTG lists *test cases* a reviewer or tester performs. Both are framed as checklist items with stable identifiers, a one-line statement, and references to background reading. Reviewers answer "met / not met / not applicable" per item.
  - Adopt: this is the closest direct match for what P3.5 should produce. Each catalog entry should look like a short reviewer-checklist row: a stable id, a one-line prompt text, the gate/block/check code(s) it applies to, an optional reference link (only to publicly accessible methodology docs — no scanner/engine docs, no platform docs), and a closed allowed-response enum.
  - Adapt: collapse ASVS/WSTG's three-state answer (met / not met / N/A) onto our four-posture closed enum (`still_blocked`, `still_needs_manual_review`, `needs_more_evidence`, `defer`). Do not import ASVS's `pass` / `fail` framing or WSTG's `confirmed` / `not_confirmed` framing — both are promotion-flavored relative to our chain.
  - Ignore / hard-reject: any ASVS `level` numeric (L1/L2/L3) field in catalog entries (would imply we are evaluating an organization's maturity, which we are not); any WSTG `test_id` or methodology-id field that would suggest the prompt is a *test instruction* to run against a live target rather than a *reviewer question* about a candidate. References are allowed but only as plain documentation URLs, and only to publicly accessible methodology documents.
  - Contract impact: none.

- **Net OSS Recon Gate decision for P3.5: APPROVE.** All five references support the prompts-only boundary. None argues for adding a lifecycle, a level vocabulary, a scanner-confirmed semantic, a draft-prose field, or a submission affordance. The decision is consistent with `handoff/cowork_p3_1_direction_review.md`, `handoff/cowork_p3_3_direction_review.md`, and `handoff/cowork_p3_4_direction_review.md`; nothing has shifted that warrants fresh adoption.

- Tier / milestone impact:
  - Escalation required: **no.** Stays at T3.
  - Can this gate cover later slices: **no.** A fresh OSS Recon Gate must run for any subsequent slice that (a) introduces a reviewer-notes *consumer* or *artifact contract*, (b) promotes any `*/0.1-trial` schema, (c) introduces any importer/exporter/platform adapter, (d) introduces a level/severity field into the catalog, or (e) introduces draft-text generation.
  - Re-review triggers if assumptions change: a proposal to record reviewer answers as a persisted artifact; a proposal to attach the catalog to runtime rendering (HTML, Markdown, web UI); a proposal to widen the allowed-response enum beyond the four postures listed in "Non-Promotional Vocabulary Rules"; a proposal to use the catalog inside `module_runner.py` or any `scripts/build_*` consumer.

## Approved / Deferred Scope

**Approved (the entire P3.5 surface):**

1. Add exactly one data file: `templates/report_readiness_reviewer_prompts.json`. JSON, not YAML. UTF-8 without BOM. LF line endings (consistent with the rest of `templates/`). Pretty-printed for human review, but tests assert the JSON is well-formed and round-trips via `json.dumps(..., sort_keys=True, indent=2)` byte-identical to disk so future drift is caught.
2. Add coverage tests under an existing test file (preferred: extend `scripts/test_report_readiness_gate.py`; if that becomes unwieldy, a *single* new test file `scripts/test_report_readiness_reviewer_prompts.py` is acceptable but must not import or wrap any chain consumer — it must only `json.load` the catalog and assert shape / coverage / vocabulary). No fixture files under `tests/fixtures/**` are required; the catalog *is* the data under test.
3. One short paragraph in `scripts/README.md` (in the existing candidate-workflow-chain section) noting the catalog's path, its data-only / non-consumer / no-runtime-wiring posture, the codes it indexes against, and that no chain consumer reads it. Doc-only; no code reference.
4. One append-only entry in `handoff/accepted_changes.md` summarizing the slice, the verdict, and the explicit deferrals.

**Deferred (must not be landed under P3.5):**

1. Any reviewer-notes artifact (`reviewer_notes/0.1-trial`, `report_readiness_reviewer_notes/0.1-trial`, or similar). The prompt invited this as an optional item; the answer is *not justified by this slice's value alone*. Reasons: (a) writing the artifact contract requires either a fixture-only path (with no consumer to test it against, making the artifact unverifiable and inviting a "while we're here" consumer in a future slice), or a new stdin consumer (triggering P2.24 revisit), or a new schema under `modules/_schema/**` (forbidden by the prompt and by P2.25). (b) The catalog by itself does not require an artifact contract — it is consumable by a human reviewer reading JSON directly, or by Claude/Cowork loading the file as data and answering the prompts in free-form chat. (c) A future direction review for an artifact slice can decide whether to record answers and how. Park the question; do not commit a schema or a fixture skeleton in P3.5.
2. Any rendering surface (Markdown, HTML, web UI, IDE integration). Reviewer prompts read from a JSON file; rendering is a separate slice.
3. Any chain wiring (`scripts/build_*` consuming the catalog, `module_runner.py` linking the catalog into preview output, the candidate workflow fixture builder emitting prompts). The catalog is data alongside the chain, not inside the chain.
4. Any change to `modules/_schema/**`, any promotion of `0.1-trial` schemas, any new validator script, any new fixture directory under `tests/fixtures/**`. The catalog is its own self-validating dataset; the tests validate it without a schema file.
5. Any free-form prose drafting field — `title`, `summary`, `impact_narrative`, `steps_to_reproduce`, `remediation_prose`, `submission_text`, or similar. Prompts are reviewer questions only.
6. Any platform field — `program_handle`, `engagement`, `bounty_amount`, `disclosed_at`, `triage_state`, `submission_id`, `cve_assignment`, `vrt_category`, `dedupe_hash`, or any field whose meaning is platform-coupled.
7. Any importer/exporter or external-tool integration (no SARIF importer, no DefectDojo importer, no <bug-bounty-platform> API client, no Bugcrowd API client, no webhook, no notification).
8. Any change that introduces or relaxes a live-target affordance. The catalog is read-only data; it has no `--target`, `--url`, `--host`, `--scope`, or `--live` surface because it has no CLI surface.

## Allowed Files

```text
templates/report_readiness_reviewer_prompts.json                 (new, data-only)
scripts/test_report_readiness_gate.py                            (extend only,
                                                                  preferred home
                                                                  for new tests)
scripts/test_report_readiness_reviewer_prompts.py                (new file, ONLY
                                                                  if extension is
                                                                  not practical;
                                                                  may import json
                                                                  and the catalog
                                                                  path only; must
                                                                  NOT import any
                                                                  scripts/build_*
                                                                  or scripts/review_*
                                                                  consumer)
scripts/README.md                                                (one short note
                                                                  in candidate
                                                                  workflow chain
                                                                  section)
handoff/accepted_changes.md                                      (append-only)
handoff/claude_code_result.md                                    (worker summary
                                                                  stub, if the
                                                                  slice routes
                                                                  through hermes
                                                                  claude-impl)
handoff/third_party_p3_5_implementation_review.md                (written after
                                                                  implementation
                                                                  by independent
                                                                  reviewer; not
                                                                  written by the
                                                                  implementer)
```

The implementer is expected to write at most six files: one new JSON catalog, at most one new test file (preference is to extend the existing test file), and the four documentation/handoff artifacts. No new helper modules. No new fixture directories. No new schema files. No new consumer scripts.

## Forbidden Files

```text
config/scope.txt                                                 (operator-only)
config/recon.conf
recon.sh
scripts/module_runner.py
scripts/program_policy_boundary.py
scripts/program_policy_check.py
scripts/core/**                                                  (no extraction)
scripts/build_candidate_review_packet.py                         (no behavior
                                                                  change; the
                                                                  catalog is not
                                                                  consumed by any
                                                                  chain script
                                                                  under P3.5)
scripts/review_candidate_packet_gaps.py                          (no behavior
                                                                  change)
scripts/build_candidate_verification_plan.py                     (no behavior
                                                                  change)
scripts/build_report_readiness_gate.py                           (no behavior
                                                                  change; the
                                                                  gate's
                                                                  GATE_ACTION_ORDER,
                                                                  BLOCK_REASON_ORDER,
                                                                  and CHECK_TO_ACTION
                                                                  constants are
                                                                  reference inputs
                                                                  for the catalog,
                                                                  NOT mutation
                                                                  targets)
scripts/build_candidate_workflow_fixture.py                      (no behavior
                                                                  change)
scripts/validate_finding_evidence.py
scripts/validate_run_manifest.py
scripts/validate_module_manifest.py
scripts/validate_module_profile.py
scripts/validate_module_io_contract.py
scripts/validate_module_io_bundle.py
scripts/validate_preview_manifest.py
scripts/validate_preview_ledger.py
modules/_schema/**.json                                          (no schema bump,
                                                                  no field add)
modules/checks/**
modules/profiles/**
tests/fixtures/**                                                (no new fixture
                                                                  directory; the
                                                                  catalog is its
                                                                  own data-under-
                                                                  test)
runs/**
loot/**
scans/**
reports/**
programs/**
.env, credentials, OAuth, scheduler, deployment, billing, production settings
```

Any deviation from these lists is a scope escalation and must route back through Hermes for a direction-review re-issue. The implementer must not "fix" a chain script's emit shape, "harden" a validator, "extract" a helper, or "wire" the catalog into the chain inside this slice. Those are separate slices.

If the implementer discovers during work that the catalog cannot achieve coverage without changing a chain script's emit (for instance, a gate code that is documented but not emitted), the correct response is to stop and route back to Hermes — do not patch the chain under cover of P3.5.

## Required Tests / Validation

Add the following assertions. Preferred home is `scripts/test_report_readiness_gate.py`; if a separate file is used, name it exactly `scripts/test_report_readiness_reviewer_prompts.py` and keep its imports to `json`, `pathlib`, `re`, and `unittest` only. No import of `build_report_readiness_gate`, `review_candidate_packet_gaps`, `build_candidate_verification_plan`, `build_candidate_review_packet`, `build_candidate_workflow_fixture`, or `module_runner` is required — coverage must be asserted against *string constants extracted by reading those files as text*, or by reimplementing the code-vocabulary lists locally in the test file as small constants. **Do not import the gate consumer just to read its constants**; importing introduces a runtime coupling that does not exist today and would make the test harder to reason about as the chain evolves. Re-declaring the small constant lists in the test file is the safer choice and trivially small (7 + 8 + 9 strings).

1. **Catalog parses as JSON.** `json.loads(path.read_text())` succeeds and returns a `dict`. Assert at least the top-level keys `schema_marker`, `version`, `entries`. (See "Catalog shape" below.)

2. **Catalog is byte-identical to its canonical pretty-printed form.** Assert that `json.dumps(json.loads(text), indent=2, sort_keys=True, ensure_ascii=True) + "\n" == text` (or whatever canonicalization the implementer commits to; document it in the file header). This locks the file against accidental drift and against editor-introduced trailing whitespace / BOM.

3. **Schema marker / version pinned.** `schema_marker` is exactly the literal string `"report_readiness_reviewer_prompts_v0_trial"` (or the implementer's chosen equivalent — but it must be present, lowercased, underscore-delimited, contain the word `trial`, and must NOT be `report_readiness_reviewer_prompts/0.1-trial` or any other slash-shaped version string that would imply a `0.1-trial` schema under `modules/_schema/**`). This is intentional: the catalog is a data artifact, not a schema; the marker must distinguish itself from chain schemas. `version` is exactly the integer `0` (or string `"0"`); promoting `version` is a future slice with its own direction review.

4. **Gate-action coverage.** For each of the seven `GATE_*` codes (`GATE_COLLECT_EVIDENCE`, `GATE_COMPLETE_MANUAL_CHECKS`, `GATE_ADD_SCOPE_REVIEW`, `GATE_ADD_REMEDIATION_GUIDANCE`, `GATE_ADD_VERIFICATION_GUIDANCE`, `GATE_ADD_HUMAN_REVIEW_DECISION`, `GATE_KEEP_OUT_OF_REPORT`), at least one catalog entry's `applies_to.gate_actions` list contains the code. Assert by exact-set comparison: `{action for entry in entries for action in entry.applies_to.gate_actions} >= set(GATE_ACTION_ORDER)` — strict subset is fine, exact set is preferred so accidentally orphaned entries are caught.

5. **Block-reason coverage.** Same as (4) but for the eight `BLOCK_*` codes (`BLOCK_MISSING_EVIDENCE`, `BLOCK_LOW_CONFIDENCE`, `BLOCK_INFO_SEVERITY`, `BLOCK_MANUAL_VERIFICATION_REQUIRED`, `BLOCK_SCANNER_OUTPUT_ONLY`, `BLOCK_MISSING_REMEDIATION`, `BLOCK_MISSING_VERIFICATION_GUIDANCE`, `BLOCK_MISSING_SCOPE_REVIEW_QUESTION`).

6. **Check-code coverage.** For each of the nine `CHECK_*` codes that are keys of `CHECK_TO_ACTION` in `scripts/build_report_readiness_gate.py` (`CHECK_MISSING_EVIDENCE`, `CHECK_LOW_CONFIDENCE`, `CHECK_INFO_SEVERITY_RATIONALE`, `CHECK_MANUAL_VERIFICATION_NOTES`, `CHECK_NON_SCANNER_CORROBORATION`, `CHECK_HUMAN_REMEDIATION_GUIDANCE`, `CHECK_SAFE_MANUAL_CHECKLIST`, `CHECK_SCOPE_REVIEW_QUESTION`, `CHECK_REVIEWER_DECISION`), at least one catalog entry's `applies_to.check_codes` list contains the code.

7. **Closed allowed-response enum.** Every entry's `allowed_response_postures` is a list whose entries are drawn from exactly the closed set `{"still_blocked", "still_needs_manual_review", "needs_more_evidence", "defer"}`. Assert no entry exposes any other string. Empty list is rejected: every prompt must have at least one allowed answer. Duplicates within an entry are rejected.

8. **Forbidden vocabulary lock.** The entire catalog text (read as a single string) must NOT contain any of the following substrings, case-insensitive, when read as whole words via a regex word-boundary check: `confirmed`, `verified`, `valid` (when used as an adjective, not as part of `validation` / `validator` / `invalid` — the simplest enforcement is to ban the exact tokens `valid` and `validated` and require the implementer to phrase prompts without them), `ready_for_submission`, `accepted`, `duplicate_confirmed`, `false_positive`, `risk_accepted`, `mitigated`, `triaged`, `resolved`, `disclosed`, `submitted`, `published`, `reportable`, `weaponizable`, and the SARIF promotion vocabulary `fail` / `pass` when used as a state (the implementer must avoid these as verbs or state nouns; phrasing like "manual checks pass" must be rewritten as "manual checks complete" or "manual checks recorded"). The test must use word-boundary regex (`\bfoo\b`) to avoid false positives like `validation`.

9. **No drafting vocabulary.** The catalog must NOT contain any of: `title`, `summary` (as a field name; the word may appear in prose), `impact_narrative`, `steps_to_reproduce`, `remediation_prose`, `submission_text`, `report_body`, `report_draft`. These would imply a drafting surface. Tests assert the exact field names are absent from the JSON keyset.

10. **No platform vocabulary.** The catalog must NOT contain any of: `program_handle`, `engagement`, `bounty_amount`, `disclosed_at`, `triage_state`, `submission_id`, `cve_assignment`, `vrt_category`, `vrt_id`, `dedupe_hash`, `<bug-bounty-platform>`, `bugcrowd`, `defectdojo`, `intigriti`, `synack`, `yeswehack`. Tests assert these substrings (case-insensitive) are absent from the JSON text.

11. **No URLs and no network-style references.** Either the catalog has no `references` field (simplest) or, if it does, every entry in `references[]` matches a strict allowlist of safe documentation hosts. Recommended: ban URLs entirely in P3.5 to keep the slice minimal; ASVS/WSTG references can be cited in prose without hyperlinks. Tests assert no `http://`, `https://`, `ftp://`, `://`, `oast.`, `interactsh.`, `burpcollaborator.`, `ngrok.`, `webhook.`, `requestbin.`, or callback-host substring is present in the catalog text.

12. **No live-target token leak.** Catalog text contains no occurrence of the strings `--target`, `--url`, `--host`, `--scope`, `--live` (these are the chain's `LIVE_TARGET_FLAGS`). The catalog is data and should never embed CLI flag spellings.

13. **Stable entry id and unique ids.** Each entry has a stable `id` string matching `^p3_5_prompt_[a-z0-9_]+$`. Ids are unique across the catalog. The catalog's `entries` list is sorted by `id` ascending; assert sorted order to lock determinism.

14. **No scanner-output-shaped fields.** No entry may contain field names `template_id`, `matched_at`, `matcher_name`, `template_path`, `tool_name`, `scanner_name`, `rule_id`. Tests assert absence.

15. **Static check: chain text scan.** As a tripwire, the test reads `scripts/build_report_readiness_gate.py` and `scripts/review_candidate_packet_gaps.py` as text and asserts the constants `GATE_ACTION_ORDER`, `BLOCK_REASON_ORDER`, and `CHECK_TO_ACTION` are still defined (string-level, e.g. `"GATE_ACTION_ORDER = ("` substring present). This is a thin canary — if a future slice quietly renames a constant, the catalog's coverage assertions would silently fall out of sync; the canary catches that case at this slice's boundary and forces explicit re-review.

16. **Existing chain tests stay green.** No test in the existing `scripts/test_report_readiness_gate.py`, `scripts/test_candidate_packet_gaps.py`, `scripts/test_candidate_verification_plan.py`, `scripts/test_candidate_review_packet.py`, or `scripts/test_candidate_workflow_fixture.py` may regress. Full suite via `python -m unittest discover -s scripts -p 'test_*.py'` must remain green and test count must strictly increase.

17. **`hermes review` clean.** JSON valid (covered by 1), Python compiles, `bash -n` clean for any shell script touched (no shell script is touched under P3.5), `.agent.lock` released, scope unchanged.

Skip:

- Any test that *executes* a gate-decision against a prompt entry (no consumer, no execution).
- Any test that asserts a specific prompt's wording (locks too much; review wording at PR time instead).
- Any test that asserts cross-product coverage between gate actions and block reasons (would couple the catalog to internal mapping the chain may evolve).
- Any test that imports YAML, PyYAML, ruamel, or another non-stdlib parser.

### Catalog shape (recommended, not normative beyond the assertions above)

```json
{
  "schema_marker": "report_readiness_reviewer_prompts_v0_trial",
  "version": 0,
  "notes": "Data-only reviewer prompt catalog ...",
  "entries": [
    {
      "id": "p3_5_prompt_evidence_sufficiency",
      "prompt_text": "Read the candidate's evidence array. ...",
      "applies_to": {
        "gate_actions": ["GATE_COLLECT_EVIDENCE"],
        "block_reasons": ["BLOCK_MISSING_EVIDENCE"],
        "check_codes":  ["CHECK_MISSING_EVIDENCE"]
      },
      "allowed_response_postures": [
        "still_blocked",
        "needs_more_evidence"
      ]
    }
  ]
}
```

The implementer should provide one entry per `GATE_*` code at minimum (seven entries) and at least one entry that covers each remaining `BLOCK_*` reason and `CHECK_*` code (a few additional entries; total entries in the catalog are expected to be 10-15). A single entry may cover multiple codes via the lists in `applies_to`, but the coverage assertions above must hold across the union.

## P2.24 Refactor Revisit Assessment

P2.24 revisit is **NOT TRIGGERED** by the approved P3.5 scope.

Walking the six triggers from `handoff/cowork_p2_25_closeout_review.md` lines 396-414 against this slice:

1. *A third file-reading consumer joins the chain.* — Not triggered. P3.5 adds no consumer of any kind. The catalog is a data file; tests that `json.load` it are not "consumers" in the P2.24 sense (P2.24 means stdin/stdout JSON consumers of `0.1-trial` chain documents). Even if the catalog is read by tests, those tests are not part of the chain's runtime surface.

2. *A fifth stdin-only consumer joins the chain.* — Not triggered. No stdin consumer is added. No `_compact_emit`, no `_error_payload`, no `_argv_errors`, no `LIVE_TARGET_FLAGS` declaration is added anywhere. Greppable in scripts/: still four files, same as today.

3. *Any `*/0.1-trial` schema is promoted to a stable `modules/_schema/...` contract.* — Not triggered. No schema is promoted. The catalog's `schema_marker` is intentionally not in the `*/0.1-trial` slash-shape; it is a flat data marker that distinguishes itself from chain schemas. No file under `modules/_schema/**` is touched.

4. *Any cross-consumer drift in `_compact_emit`, `_error_payload`, or live-flag rejection behavior is observed during review or caught by a future cross-consumer test.* — Not triggered. The slice adds tests for the catalog only, not for chain consumers. No new cross-consumer assertion is introduced.

5. *Any operator-approved change to `LIVE_TARGET_FLAGS` is proposed.* — Not triggered. No change to `LIVE_TARGET_FLAGS` is proposed; the catalog text explicitly does not contain the flag strings (assertion 12 enforces this).

6. *Any consumer needs to import or be imported by another consumer for reasons other than the existing P2.23 in-memory chaining.* — Not triggered. No new import path is created.

Recommendation: explicitly write into `handoff/accepted_changes.md` that P3.5 did not trigger a P2.24 revisit, and that the duplication watchlist remains intentional. This forecloses the failure mode where a future reader infers "they added a reviewer-prompt slice without revisiting the helper extraction question; that must mean the project is letting duplication grow". The opposite is the truth: P3.5 was *kept* data-only specifically so the revisit question would not have to be answered yet.

A future slice that proposes a reviewer-notes *consumer* — i.e., a script that reads the prompt catalog plus a `report_readiness_gate/0.1-trial` document on stdin and emits a `reviewer_notes/0.1-trial` artifact — *would* fire trigger 2 (fifth stdin consumer) and require a fresh P2.24 review. Hermes should pre-flag this on any future P3.6 / P3.7 proposal.

## Non-Promotional Vocabulary Rules

**Allowed answer-posture vocabulary in the catalog (closed set):**

- `still_blocked` — reviewer answered the prompt and judges the candidate remains in the gate's `blocked` state. Maps forward to the existing chain's `blocked` gate_state without changing it.
- `still_needs_manual_review` — reviewer answered and judges `needs_manual_review` is still the right state.
- `needs_more_evidence` — reviewer judges the candidate cannot be assessed yet and more evidence collection is required. Equivalent to "stay blocked but for a specific evidence-gap reason". Maps to the existing `GATE_COLLECT_EVIDENCE` action.
- `defer` — reviewer judges the candidate should be parked until a future review cycle (no positive action now, no negative action now). This is the closest *safe* analog to a "wait state" without invoking any platform lifecycle vocabulary.

Those four are the *entire* allowed-response set. The catalog must not introduce a fifth posture without a fresh direction review. Adding a fifth posture is what would tempt a future slice toward "and now we need a consumer to record these, and a schema to validate the consumer..." which is precisely the deferred trajectory.

**Forbidden vocabulary across catalog text, prompt text, allowed-response enum, test strings, and docs (case-insensitive whole-word match):**

- Promotion-flavored chain vocabulary: `confirmed`, `verified`, `valid` (as state), `validated` (as state), `ready_for_submission`, `accepted`, `duplicate_confirmed`, `reportable`.
- Platform lifecycle vocabulary: `false_positive`, `risk_accepted`, `mitigated`, `triaged`, `resolved`, `disclosed`, `submitted`, `published`, `informative`, `not_applicable`, `won_t_fix`, `out_of_scope` (as a *lifecycle state*; the *concept* of an out-of-scope check is fine, but the word as a state value is not).
- SARIF result.kind: `fail`, `pass`, `open` (as result states).
- DefectDojo lifecycle: `active`, `false_p`, every other DefectDojo state.
- Bugcrowd / VRT submission state: every Bugcrowd submission state.
- <bug-bounty-platform> report state: every <bug-bounty-platform> report state.
- Platform field names: `program_handle`, `engagement`, `bounty_amount`, `disclosed_at`, `triage_state`, `submission_id`, `cve_assignment`, `vrt_category`, `vrt_id`, `dedupe_hash`.
- Platform names as identifiers: `<bug-bounty-platform>`, `bugcrowd`, `defectdojo`, `intigriti`, `synack`, `yeswehack` (the catalog must not reference any specific platform by name even in prose).
- Drafting field names: `title`, `summary_field`, `impact_narrative`, `steps_to_reproduce`, `remediation_prose`, `submission_text`, `report_body`, `report_draft`.
- Severity-axis fields the catalog does not need: `severity`, `level`, `risk`, `confidence_score`, `cvss`, `epss`. The chain already carries `severity_hint` and `confidence`; the catalog is not the place to restate or alias them.
- Live-target CLI affordances: `--target`, `--url`, `--host`, `--scope`, `--live`.
- Scanner / engine identifiers: `nuclei`, `zap`, `burp`, `nmap`, `semgrep`, `template_id`, `matched_at`, `matcher_name`, `template_path`. (References to public methodology like ASVS / WSTG are acceptable in prose without a URL, but specific scanner tool names should not appear as catalog text or fields.)

The forbidden list is enforced both as test assertions (substring + word-boundary regex) and as review-time spot-checks; the implementer should grep the proposed catalog for each substring before requesting review.

## Blocking Issues

None on the approved scope.

One pre-emptive lock to call out: if the implementer reads this review and concludes the trial reviewer-notes artifact is "easy to land alongside the catalog because the catalog already has allowed-response postures", that conclusion is **wrong** and the impulse should be rejected at intake. The deferral is explicit and load-bearing. Landing both in one slice converts a tests-and-data slice into a contract slice (artifact = contract), which (a) crosses the prompt's stated "do not promote any `*/0.1-trial` schema" line if the contract goes under `modules/_schema/**`, (b) creates a fixture-only contract that no consumer reads (and thus cannot be tested for correctness, only for shape), or (c) demands a fifth stdin consumer (P2.24 trigger 2).

## Non-Blocking Recommendations

1. **Park the reviewer-notes artifact as the explicit P3.6 candidate.** When and if Hermes proposes P3.6, the direction review should answer two questions at once: (a) is the artifact justified now (i.e., has at least one external need surfaced — a real Claude/Cowork reviewer asking "where do I record my answers", or an operator request to keep notes between sessions), and (b) if yes, does it land as a fixture-only artifact (no consumer; tests assert shape only) or as a consumer-backed artifact (which fires the P2.24 fifth-consumer trigger and must run the helper-extraction review in the same slice)? Pre-commit to neither path; let the next direction review decide.

2. **If a renderer is ever proposed, keep it Markdown-only and in `docs/` or `scripts/render_reviewer_prompts.py` with no chain integration.** The rendering surface should be a pure transform of the catalog file → human-readable Markdown for a session reviewer to follow, with no side effects on the chain, no chain script edits, and no `runs/` or `loot/` write. That separation keeps the prompt artifact independent of any UX layer.

3. **Maintain the catalog as the canonical reviewer-checklist source even outside the chain.** Once it exists, the operator and Claude/Cowork can use it for ad-hoc bug-bounty reviews without invoking any P2.19-P2.23 script: load the JSON, walk the entries, answer the prompts manually. This is a meaningful UX win that needs no new code surface, which is exactly the kind of low-risk leverage the project is meant to accumulate.

4. **Add an explicit "catalog is not a schema" sentence to the `scripts/README.md` paragraph.** The `schema_marker` field name and the presence of an `entries` array will tempt a future reader to look for a schema under `modules/_schema/**`. The README sentence forecloses that by stating: "the catalog is a data file with a flat marker, deliberately not a `*/0.1-trial` schema; no validator script reads it, only the test suite under `scripts/test_report_readiness_gate.py` (or `scripts/test_report_readiness_reviewer_prompts.py`)".

5. **Spot-check at implementation review that no prompt text describes a *test step against a target*.** ASVS and WSTG framing is helpful, but their language sometimes reads as "perform the following request and observe...". The catalog must phrase prompts as "given the candidate's evidence, decide whether..." not as "execute the following request against the target". This is a wording trap easy to fall into; the safety boundary depends on the catalog being a reviewer-side checklist, not a tester-side runbook.

6. **Do not introduce a `references[]` field in P3.5.** Even with a URL allowlist, references invite the question of whether to validate them, fetch them, or render them, and each answer expands surface area. ASVS / WSTG / OWASP references can appear in prose inside `prompt_text` ("see OWASP ASVS section on session management") without becoming structured data. If a future slice needs structured references, run a fresh direction review.

7. **Run `hermes review` and the full unittest suite before P3.5 implementation begins.** Per the standing recommendation in `handoff/cowork_p3_1_direction_review.md` non-blocking 7, baseline the suite count and the `hermes review` exit so any divergence during P3.5 is attributable to the slice.

8. **At implementation acceptance time, ensure the `accepted_changes.md` entry explicitly records four things**: (a) "P3.5 was kept data-and-tests-only; no consumer, no schema, no fixture root, no chain wiring"; (b) "P2.24 helper extraction was not triggered; the duplication watchlist remains intentional"; (c) "the reviewer-notes artifact was DEFERRED to a future direction review (provisional P3.6)"; (d) "the OSS Recon Gate result was APPROVE and no platform lifecycle / scanner-confirmed vocabulary was adopted." These four sentences let any future reader confirm scope discipline without re-reading the direction review.

9. **Independent implementation review is required at T3.** Per `handoff/review_tiering_policy.md`, an independent reviewer (Claude/Cowork in a separate session, or third-party) must read the landed catalog, run the test suite, confirm no forbidden file has been touched, and write `handoff/third_party_p3_5_implementation_review.md` with verdict ACCEPT / REQUEST_CHANGES / BLOCK. The implementation review should specifically spot-check assertions 8-12 (forbidden vocabulary, no drafting fields, no platform fields, no URLs, no live-target tokens) because those are the safety-critical assertions and a misread on the implementer's part is the most likely failure mode.

## Safety Boundary Confirmation

This review is design-only. The reviewer did not:

- run live scans, probes, scanners, fuzzers, exploit tooling, callbacks, OAST / relay infrastructure, proxy / pivot tooling, or any target-touching automation;
- import, vendor, or invoke any third-party scanning code;
- execute any module `check.py` file, any candidate-workflow consumer, or any other repo script;
- modify `config/scope.txt`, `config/recon.conf`, `recon.sh`, anything under `modules/**`, anything under `scripts/**`, anything under `tests/**`, anything under `loot/**`, `scans/**`, `reports/**`, `runs/**`, `programs/**`, `.env`, credentials, OAuth, scheduler, billing, deployment, or production-side settings;
- promote any `*/0.1-trial` schema, draft any report, add any platform adapter, change any candidate-chain status to `confirmed` / `verified`, or add any runner runtime / recon wiring / module execution surface;
- authorize any active scan, target interaction, module execution, scanner import, report drafting/submission, schema promotion, or platform adapter under this review.

Files this review reads (read-only):
`handoff/cowork_p3_5_direction_prompt.md`,
`handoff/cowork_p2_25_closeout_review.md`,
`handoff/cowork_p3_1_direction_review.md`,
`handoff/cowork_p3_3_direction_review.md`,
`handoff/cowork_p3_4_direction_review.md`,
`handoff/cowork_p2_24_direction_review.md`,
`handoff/oss_recon_gate.md`,
`handoff/accepted_changes.md` (tail only),
`scripts/build_report_readiness_gate.py`,
`templates/ctf_verifier_metadata.yaml`,
directory listing of `templates/`, `tests/fixtures/**`, `modules/_schema/`, `handoff/`,
grep results for `_compact_emit` / `LIVE_TARGET_FLAGS` / `_argv_errors` across `scripts/`.

Files this review writes:
`handoff/cowork_p3_5_direction_review.md` (this file, only).

Binding rules from `.hermes.md` preserved: authorization-first, no exfiltration, no destructive defaults, no silent overwrites, lock discipline, secrets out of git, report integrity (`accepted_changes.md` treated as append-only), no production-side changes. None of these were touched.

The implementation slice that follows this review must preserve the same posture and is bound by the explicit "Forbidden Files" list above. Specifically: no live-target affordance is added, no scope semantics are changed, no schema is promoted, no runner runtime is wired, no scanner importer is created, no chain consumer is edited, no reviewer-notes artifact is introduced, no rendering surface is introduced, and no status above `needs_manual_review` is emitted by any stage (this slice does not emit any candidate-chain status at all; it only adds a data catalog and tests).
