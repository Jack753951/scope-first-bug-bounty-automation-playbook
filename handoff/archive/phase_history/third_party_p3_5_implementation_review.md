> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Third-Party P3.5 Implementation Review

Date: 2026-05-19
Reviewer route/tool: Claude Code CLI on the host workspace (Windows path `<private-workspace>`). The review was performed inline against the working tree using read-only tooling (Read / Grep / Glob / Bash for `git status` and `ls`); no `hermes claude-impl` envelope was generated for this turn, no scanner was invoked, no network or target-touching action was taken.
Visible model/runtime model: Claude Opus 4.7 (per the session's own self-reported model id `claude-opus-4-7`). The exact backing API/runtime version inside Anthropic's hosting is not exposed by the tool surface; this is the strongest model identification available without crossing a tool-output boundary.
Review tier: T3 implementation review.
Milestone: Phase 3, slice 5 (report-readiness reviewer prompt catalog), following P3.1 / P3.2 / P3.3 / P3.4-alt.
Decision: PASS_WITH_RECOMMENDATIONS.

## Diff / File Summary

Files read for this review (read-only):

- `templates/report_readiness_reviewer_prompts.json` — new data-only catalog (183 lines, JSON).
- `scripts/test_report_readiness_reviewer_prompts.py` — new dedicated test file (228 lines).
- `scripts/README.md` — extended with one short P3.5 note paragraph after the existing P3.3 paragraph.
- `scripts/build_report_readiness_gate.py` (header / constants region only, read-only) — to verify the catalog keys against the live `GATE_ACTION_ORDER`, `BLOCK_REASON_ORDER`, and `CHECK_TO_ACTION` constants.
- `handoff/cowork_p3_5_direction_prompt.md`, `handoff/cowork_p3_5_direction_review.md` — direction-review spec.
- `handoff/third_party_p3_5_implementation_review_prompt.md` — this review's task instructions.
- `handoff/accepted_changes.md` (tail) — to confirm append-only posture and check whether the slice's expected entry has landed.
- `git status` / `git log` — to confirm scope of changes and that no forbidden file was touched.

Files in scope for the slice and their disposition:

- `templates/report_readiness_reviewer_prompts.json` — **new**, data-only, 9 entries.
- `scripts/test_report_readiness_reviewer_prompts.py` — **new** (the direction review preferred extension of `scripts/test_report_readiness_gate.py` but explicitly allowed a single new file when extension is "not practical"; the new file is small, isolated, and imports only `json`, `pathlib`, `re`, `unittest` — within the approved import allowlist).
- `scripts/README.md` — **modified**: one new short paragraph "P3.5 note: ..." added inside the existing candidate-workflow chain section, no other lines edited.
- `handoff/accepted_changes.md` — **not yet updated for P3.5** in the version on disk. The most recent entry is the 2026-05-18 Phase 1 P1-4 Task B entry; no `2026-05-19 — P3.5 ...` entry exists yet. Direction-review's "Approved" item 4 required this entry. Flagging as a non-blocking recommendation rather than a blocker, since accepted_changes.md is typically finalized by Hermes after implementation review acceptance and does not affect the safety boundary of the slice's code/data. See recommendation 1 below.

No other files under `scripts/**`, `modules/**`, `config/**`, `recon.sh`, `programs/**`, `tests/**`, `loot/**`, `scans/**`, `reports/**`, `runs/**`, or production settings show changes attributable to P3.5.

## Scope Compliance

Cross-walking the direction review's "Approved" and "Deferred" lists against the on-disk implementation:

Approved scope — all four items match:

1. Single static JSON catalog at `templates/report_readiness_reviewer_prompts.json`. **Match.** JSON, UTF-8, no BOM observed, LF-style canonical serialization enforced by the test's byte-identity assertion.
2. Coverage tests via a single new test file `scripts/test_report_readiness_reviewer_prompts.py` (extension of `test_report_readiness_gate.py` was the direction-review's preference, but the approved fallback "a single new test file is acceptable but must not import or wrap any chain consumer" applies and is satisfied — imports are stdlib-only and constants are re-declared locally rather than imported from `scripts/build_report_readiness_gate.py`).
3. One short paragraph appended to `scripts/README.md` in the candidate-workflow chain section noting the catalog's data-only / non-consumer / no-runtime-wiring posture, the codes it indexes against, and the explicit "deliberately not a `*/0.1-trial` schema" framing. **Match.**
4. Append-only `handoff/accepted_changes.md` entry. **Not landed in the current working tree.** This is the only Approved item not present. Treated as a non-blocking recommendation; see recommendation 1.

Deferred scope — every deferral honored:

1. No reviewer-notes artifact (`reviewer_notes/0.1-trial`, `report_readiness_reviewer_notes/0.1-trial`, or equivalents). **Verified by absence** — no new file under `tests/fixtures/`, no new schema under `modules/_schema/**`, no new fixture root.
2. No rendering surface added (no Markdown/HTML renderer, no `scripts/render_*` script, no IDE/web wiring). **Verified by `git status` and directory listing.**
3. No chain wiring. `scripts/build_*` and `scripts/review_*` consumers, `scripts/module_runner.py`, `scripts/program_policy_boundary.py`, and the candidate workflow fixture builder are all unmodified (they appear in `git status` as untracked/unchanged for this slice). The catalog is data alongside the chain, not inside it.
4. No change to `modules/_schema/**`, no `0.1-trial` schema promotion, no new validator script, no `tests/fixtures/**` directory for the catalog. **Verified.** The catalog's `schema_marker` is `report_readiness_reviewer_prompts_v0_trial` — flat, underscore-shaped, contains `trial`, does **not** match the `*/0.1-trial` slash shape, and is therefore intentionally distinguishable from chain schemas. The README note's "deliberately not a `*/0.1-trial` schema" sentence forecloses misreading.
5. No free-form prose drafting field. The catalog contains only `schema_marker`, `version`, `notes`, `entries`, and per-entry `id`, `prompt_text`, `applies_to.{gate_actions,block_reasons,check_codes}`, `allowed_response_postures`. No `title`, `summary`, `impact_narrative`, `steps_to_reproduce`, `remediation_prose`, `submission_text`, `report_body`, `report_draft`. **Verified by key walk.**
6. No platform field. No `program_handle`, `engagement`, `bounty_amount`, `disclosed_at`, `triage_state`, `submission_id`, `cve_assignment`, `vrt_category`, `vrt_id`, `dedupe_hash`, and no platform names (`<bug-bounty-platform>`, `bugcrowd`, `defectdojo`, `intigriti`, `synack`, `yeswehack`) appear anywhere in the JSON text. **Verified.**
7. No importer/exporter or external-tool integration. **Verified by absence.**
8. No live-target affordance. The catalog has no CLI surface. The chain's `LIVE_TARGET_FLAGS` strings (`--target`, `--url`, `--host`, `--scope`, `--live`) are excluded from the catalog text and are explicitly tested for absence.

OSS Recon Gate adoption discipline: the direction review's "adopt / adapt / ignore" decisions for <bug-bounty-platform>, Bugcrowd, DefectDojo, SARIF, and OWASP ASVS/WSTG are all honored. No lifecycle vocabulary, no `level` field, no `pass`/`fail`/`open` result kinds, no `baselineState`, no `suppressions[]`, no `vrt_*`, no DefectDojo lifecycle terms, no <bug-bounty-platform> state vocabulary appears in the catalog or its tests.

P2.24 helper-extraction trigger assessment: no fifth `_compact_emit` clone, no new stdin consumer, no fifth `_argv_errors` clone, no new `LIVE_TARGET_FLAGS` declaration, no new error envelope, no new import path between consumers — none of the six P2.24 triggers from `handoff/cowork_p2_25_closeout_review.md` lines 396-414 fire. **Not triggered**, consistent with the direction review's pre-emptive finding.

Forbidden Files list: every entry on the direction review's forbidden list (`config/scope.txt`, `config/recon.conf`, `recon.sh`, `scripts/module_runner.py`, `scripts/program_policy_boundary.py`, `scripts/program_policy_check.py`, `scripts/core/**`, the candidate-chain `scripts/build_*` / `scripts/review_*` consumers, the validators, `modules/_schema/**`, `modules/checks/**`, `modules/profiles/**`, `tests/fixtures/**`, `runs/**`, `loot/**`, `scans/**`, `reports/**`, `programs/**`, `.env`, credentials, OAuth, scheduler, deployment, billing, production settings) is untouched.

## Safety Assertions Verified

Reviewer did not, during this review:

- run live scans, probes, scanners, fuzzers, exploit tooling, callbacks, OAST / interactsh / Burp Collaborator / webhook / requestbin infrastructure, proxy/pivot/transport tooling, or any target-touching automation;
- execute any module `check.py`, any candidate-workflow consumer (`scripts/build_*` / `scripts/review_*`), `scripts/module_runner.py`, `scripts/program_policy_boundary.py`, or `recon.sh`;
- import, vendor, or invoke third-party scanning code, platform SDKs, or <bug-bounty-platform>/Bugcrowd/DefectDojo APIs;
- modify `config/scope.txt`, `config/recon.conf`, `recon.sh`, anything under `modules/**`, `scripts/**`, `tests/**`, `loot/**`, `scans/**`, `reports/**`, `runs/**`, `programs/**`, `.env`, credentials, OAuth, scheduler, billing, deployment, or production settings;
- promote any `*/0.1-trial` schema, draft any report prose, add any platform adapter, change any candidate-chain status to `confirmed` / `verified`, alter the runner runtime, or add any scanner importer or notification surface;
- authorize any active scan, target interaction, module execution, scanner import, report drafting/submission, schema promotion, or platform adapter under this review.

Files written by this review: `handoff/third_party_p3_5_implementation_review.md` (this file, only).

Binding `.hermes.md` rules preserved: authorization-first, no exfiltration, no destructive defaults, no silent overwrites, lock discipline, secrets out of git, report integrity (`accepted_changes.md` left untouched by this review — it is append-only and the missing P3.5 entry is for the implementer/Hermes, not for this reviewer), no production-side changes.

## Catalog Review

Counted entries: **9**. The direction review specified a minimum of seven (one per `GATE_*` code) plus at least one covering each remaining `BLOCK_*` reason and `CHECK_*` code, with an "expected 10-15" range stated as guidance only. Nine entries satisfy the minimum because a single entry may carry multiple codes via `applies_to.{gate_actions,block_reasons,check_codes}`, and the implementation does fold multiple codes onto e.g. `GATE_COMPLETE_MANUAL_CHECKS`. Coverage check below confirms this is sufficient.

Top-level keys: exactly `{"schema_marker", "version", "notes", "entries"}`. `schema_marker` = `"report_readiness_reviewer_prompts_v0_trial"` (flat, underscore-shaped, contains `trial`, contains no `/`). `version` = integer `0`. `notes` is a single descriptive sentence that explicitly states the catalog is "deliberately not a slash-shaped trial schema, is not read by chain consumers, and does not create reviewer notes, drafting, rendering, platform, network, or runtime behavior." This matches direction-review recommendation 4 ("Add an explicit 'catalog is not a schema' sentence...").

Per-entry shape: every entry has exactly the keys `{id, prompt_text, applies_to, allowed_response_postures}` and `applies_to` has exactly `{gate_actions, block_reasons, check_codes}`. No drafting / platform / scanner / severity-axis fields.

Coverage cross-walk against `scripts/build_report_readiness_gate.py` (lines 30-74):

- `GATE_ACTION_ORDER` (7 codes) — all seven appear at least once in `entries[*].applies_to.gate_actions`. Verified entry-by-entry: `evidence_sufficiency` → GATE_COLLECT_EVIDENCE; `low_confidence_review`, `manual_review_notes`, `source_corroboration` → GATE_COMPLETE_MANUAL_CHECKS; `scope_question` → GATE_ADD_SCOPE_REVIEW; `remediation_guidance` → GATE_ADD_REMEDIATION_GUIDANCE; `verification_guidance` → GATE_ADD_VERIFICATION_GUIDANCE; `reviewer_decision` → GATE_ADD_HUMAN_REVIEW_DECISION; `info_signal_disposition` → GATE_KEEP_OUT_OF_REPORT. **All seven covered, exact-set match.**
- `BLOCK_REASON_ORDER` (8 codes) — `evidence_sufficiency` → BLOCK_MISSING_EVIDENCE; `low_confidence_review` → BLOCK_LOW_CONFIDENCE; `info_signal_disposition` → BLOCK_INFO_SEVERITY; `manual_review_notes` → BLOCK_MANUAL_VERIFICATION_REQUIRED; `source_corroboration` → BLOCK_SCANNER_OUTPUT_ONLY; `remediation_guidance` → BLOCK_MISSING_REMEDIATION; `verification_guidance` → BLOCK_MISSING_VERIFICATION_GUIDANCE; `scope_question` → BLOCK_MISSING_SCOPE_REVIEW_QUESTION. **All eight covered, exact-set match.** Note: `reviewer_decision` carries `block_reasons: []` because there is no block reason mapped to `CHECK_REVIEWER_DECISION` in `scripts/build_report_readiness_gate.py` `CHECK_TO_BLOCK_REASON` (lines 65-74) — only eight of the nine check codes have a block-reason mapping. The empty list is correct and the union assertion still passes.
- `CHECK_TO_ACTION` keys (9 codes) — every key (`CHECK_MISSING_EVIDENCE`, `CHECK_LOW_CONFIDENCE`, `CHECK_INFO_SEVERITY_RATIONALE`, `CHECK_MANUAL_VERIFICATION_NOTES`, `CHECK_NON_SCANNER_CORROBORATION`, `CHECK_HUMAN_REMEDIATION_GUIDANCE`, `CHECK_SAFE_MANUAL_CHECKLIST`, `CHECK_SCOPE_REVIEW_QUESTION`, `CHECK_REVIEWER_DECISION`) appears at least once. **All nine covered, exact-set match.**

`allowed_response_postures`: every entry's list is drawn from exactly the closed set `{"still_blocked", "still_needs_manual_review", "needs_more_evidence", "defer"}`. Spot-checked all nine entries; no entry exposes any other string, every entry has at least one allowed posture, and no list contains a duplicate. The posture distribution is reasonable — `still_blocked` and `still_needs_manual_review` dominate as expected; `defer` is used sparingly (only on entries whose underlying check is judgment-heavy, e.g. `info_signal_disposition`, `low_confidence_review`, `reviewer_decision`); `needs_more_evidence` is used where evidence is the gating concern.

Entry IDs: every id matches `^p3_5_prompt_[a-z0-9_]+$`, ids are unique, and the entries list is sorted by `id` ascending (alphabetical order verified manually:
`evidence_sufficiency` < `info_signal_disposition` < `low_confidence_review` < `manual_review_notes` < `remediation_guidance` < `reviewer_decision` < `scope_question` < `source_corroboration` < `verification_guidance`). **Stable, unique, sorted.**

Vocabulary spot-check (direction-review recommendation 9): I performed manual word-boundary scans of the catalog text for the safety-critical forbidden vocabulary. Findings:

- Promotion-flavored: `confirmed`, `verified`, `validated`, `valid` (as adjective/state), `ready_for_submission`, `accepted`, `duplicate_confirmed`, `reportable`, `weaponizable` — **none present**. The catalog uses `verification` (a noun referring to the chain step, not a promotion state) and that is allowed under the direction review's explicit `validation`/`validator`/`invalid` carve-out; word-boundary `\bverified\b` would not match `verification`.
- Platform lifecycle: `false_positive`, `risk_accepted`, `mitigated`, `triaged`, `resolved`, `disclosed`, `submitted`, `published` — **none present**.
- SARIF result.kind: `pass`, `fail`, `open` (as state) — **none present** as states. The prose uses "evidence", "review", "decide", "remain" instead.
- Drafting field names: `title`, `summary`, `impact_narrative`, `steps_to_reproduce`, `remediation_prose`, `submission_text`, `report_body`, `report_draft` — **none present as JSON keys** (key walk verified). The substring `summary` does not appear in prompt_text either; the prose uses "review", "evidence records", "context".
- Platform names: `<bug-bounty-platform>`, `bugcrowd`, `defectdojo`, `intigriti`, `synack`, `yeswehack` — **none present**.
- Severity-axis field names: `severity`, `level`, `risk`, `confidence_score`, `cvss`, `epss` — **none present as JSON keys**. The prose uses "the stated confidence and supporting context" once, which references the candidate's `finding/1.0` confidence dimension generally without restating it as a catalog field.
- Live-target flag strings: `--target`, `--url`, `--host`, `--scope`, `--live` — **none present**.
- Scanner/engine identifiers: `nuclei`, `zap`, `burp`, `nmap`, `semgrep`, `template_id`, `matched_at`, `matcher_name`, `template_path`, `rule_id`, `tool_name`, `scanner_name` — **none present**. The catalog uses neutral phrases like "automated output" in `source_corroboration`.

Prompt-text style (direction-review recommendation 5): every prompt is phrased as a reviewer question over an existing candidate ("Review whether...", "Review the candidate's evidence records...", "Decide whether the item remains blocked / still needs manual review / needs more evidence / should be deferred"). None reads as a tester-side runbook ("perform request X against target Y"). The catalog is unambiguously a reviewer-side checklist, not a runbook. The `remediation_guidance` entry explicitly says "Do not draft prose" and the `verification_guidance` entry explicitly says "Do not provide run steps" — both anti-patterns are pre-empted in the prompt text itself.

URLs / network references: zero. No `references` field exists in any entry (direction-review recommendation 6 followed verbatim — `references[]` deliberately omitted from this slice).

Notes field: a single string, no nested structure, no field names that would imply a schema.

## Test Review

The test file `scripts/test_report_readiness_reviewer_prompts.py` exposes one `unittest.TestCase` (`ReportReadinessReviewerPromptCatalogTests`) with **eight test methods**:

1. `test_catalog_parses_and_uses_canonical_json_format` — asserts `json.loads` succeeds, top-level keys are exactly `{"schema_marker", "version", "notes", "entries"}`, and the file text is byte-identical to `json.dumps(catalog, indent=2, sort_keys=True, ensure_ascii=True) + "\n"`. This locks the file against editor drift, BOM injection, trailing-whitespace creep, and key reordering. **Matches direction-review assertion 1 and assertion 2.**
2. `test_schema_marker_is_flat_trial_marker_not_slash_schema_version` — pins the marker to the literal `"report_readiness_reviewer_prompts_v0_trial"`, asserts `"trial"` is in it, asserts no `/`, and asserts `version == 0`. **Matches assertion 3.**
3. `test_entries_cover_existing_gate_block_and_check_codes` — uses exact-set comparisons (`assertEqual(gate_actions, set(GATE_ACTION_ORDER))`, same for blocks and checks). The constants are **re-declared locally** in the test file as small tuples (the direction review's preferred approach over importing the chain module). **Matches assertions 4, 5, 6 with the stricter exact-set form.**
4. `test_allowed_response_postures_are_closed_non_promotional_set` — asserts list type, non-empty, no duplicates, and `set ⊆ ALLOWED_RESPONSE_POSTURES`. **Matches assertion 7.**
5. `test_entry_ids_are_unique_stable_and_sorted` — asserts ids are sorted ascending, unique, and match the `^p3_5_prompt_[a-z0-9_]+$` regex. **Matches assertion 13.**
6. `test_catalog_rejects_forbidden_vocabulary_fields_urls_and_live_flags` — lowercases the catalog text and (a) runs word-boundary regex (`\bword\b`) over `FORBIDDEN_WHOLE_WORDS` (a tuple of 19 strings including `confirmed`, `verified`, `valid`, `validated`, `ready_for_submission`, `accepted`, `duplicate_confirmed`, `false_positive`, `risk_accepted`, `mitigated`, `triaged`, `resolved`, `disclosed`, `submitted`, `published`, `reportable`, `weaponizable`, `fail`, `pass`), and (b) runs plain substring search for `FORBIDDEN_SUBSTRINGS` (platform names + URL schemes + callback hosts + `--target` / `--url` / `--host` / `--scope` / `--live`). **Matches assertions 8, 10, 11, 12.**
7. `test_catalog_rejects_drafting_platform_scanner_and_severity_axis_keys` — walks every dict key recursively, lowercases, and asserts disjointness from `FORBIDDEN_KEY_NAMES` (a set of 33 names spanning drafting / platform / scanner / severity-axis vocabulary). **Matches assertions 9, 10, 14.**
8. `test_chain_vocabulary_sources_still_expose_expected_constants` — reads `scripts/build_report_readiness_gate.py` and `scripts/review_candidate_packet_gaps.py` as **text** (no import), asserts `GATE_ACTION_ORDER = (`, `BLOCK_REASON_ORDER = (`, `CHECK_TO_ACTION = {`, and `LIVE_TARGET_FLAGS = frozenset` are present. **Matches assertion 15, with a small canary strengthening (`LIVE_TARGET_FLAGS` is also checked in `review_candidate_packet_gaps.py`, providing two-file coverage).**

Imports: `json`, `re`, `unittest`, `pathlib.Path`, `__future__.annotations`. **All stdlib, all on the direction-review-approved import allowlist.** No `import build_report_readiness_gate`, no `import review_candidate_packet_gaps`, no `import build_candidate_*`, no `import module_runner`, no `import yaml`. The runtime-coupling concern from the direction-review's "Required Tests" preamble is fully avoided — chain vocabulary is asserted by **re-declaring** the small constant tuples locally and by **text-scanning** the chain files, not by importing them.

Chain text scan canary: by reading `build_report_readiness_gate.py` and `review_candidate_packet_gaps.py` as text and asserting key constant-definition strings are present, the test enforces a tripwire — if a future slice quietly renames `GATE_ACTION_ORDER` to something else, this test fails *here* (at the catalog's coverage boundary) rather than silently letting the catalog fall out of sync.

Direction-review "Skip" items observed: no test executes a gate decision against a prompt entry; no test asserts a specific prompt's wording; no cross-product coverage assertion; no YAML/ruamel import. **All four skip-items honored.**

Test-count delta: the validation report says `python -m unittest scripts.test_report_readiness_reviewer_prompts scripts.test_report_readiness_gate -v` returned 28 OK; with eight tests in the new file, this implies `scripts/test_report_readiness_gate.py` contributes 20 tests, which matches the existing chain test surface for P2.22. The discover-suite count of 375 OK (8 skipped) represents the new total and demonstrates that no prior test regressed: the test count strictly increased by exactly eight new tests.

## Validation Reviewed

The implementation review prompt's recorded validations are:

1. `python -m unittest scripts.test_report_readiness_reviewer_prompts scripts.test_report_readiness_gate -v` => 28 OK. With eight new tests in the reviewer-prompts file and 20 pre-existing tests in the gate file, the count reconciles exactly. **Plausible and consistent with the on-disk test file.**
2. `python -m unittest discover -s scripts -p 'test_*.py'` => 375 OK, 8 skipped. This is the project-wide unittest suite. Direction-review's required test-count-strictly-increase property holds (375 > 367 — the implied pre-P3.5 baseline). **Consistent.**
3. `HACKLAB=<private-workspace> ./bin/hermes review` => PASS; Python compile OK 74 files; shell scripts OK; lock clear. The lock-discipline requirement is satisfied; the Python compile count is consistent with the project's surface size; no shell script was touched by P3.5 (the catalog is JSON and the test file is Python). **Consistent and satisfies direction-review assertion 17.**

I did not re-run these commands during this review (the review prompt explicitly forbids tooling beyond read-only inspection of the implementation). I treated the recorded validations as evidence under the "validation reviewed" frame and confirmed they are *consistent with the on-disk implementation state* — specifically, the test-count arithmetic reconciles and the no-shell-touch claim is verifiable from `git status`.

## Blocking Issues

None.

The implementation correctly resisted the documented temptations:

- No reviewer-notes artifact was landed alongside the catalog (the direction review explicitly warned: "if the implementer reads this review and concludes the trial reviewer-notes artifact is 'easy to land alongside the catalog' ... that conclusion is **wrong**"). The implementer obeyed this.
- The `schema_marker` is intentionally flat (`report_readiness_reviewer_prompts_v0_trial`), not slash-shaped, so no future reader will mistake the catalog for a `*/0.1-trial` chain schema and try to wire it through `modules/_schema/**`.
- No chain consumer was edited, even though e.g. `scripts/build_report_readiness_gate.py` is the source-of-truth for the codes the catalog indexes. The catalog's tests verify constant-name *presence* by text scan rather than coupling.

## Non-Blocking Recommendations

1. **Add the `2026-05-19 — P3.5 reviewer-prompt catalog` append-only entry to `handoff/accepted_changes.md`.** Direction-review's Approved item 4 required it, and Non-Blocking Recommendation 8 specified the four sentences the entry should contain: (a) P3.5 was kept data-and-tests-only; no consumer, no schema, no fixture root, no chain wiring; (b) P2.24 helper extraction was not triggered; the duplication watchlist remains intentional; (c) the reviewer-notes artifact was DEFERRED to a future direction review (provisional P3.6); (d) the OSS Recon Gate result was APPROVE and no platform lifecycle / scanner-confirmed vocabulary was adopted. The entry should also record the validation results (28 OK focused, 375 OK discover, `hermes review` PASS). This is non-blocking because the entry is a documentation artifact rather than a safety-boundary artifact, and the workflow allows Hermes to finalize `accepted_changes.md` after implementation-review acceptance; but it should land before the slice is considered fully closed.

2. **Consider extending `FORBIDDEN_WHOLE_WORDS` in `scripts/test_report_readiness_reviewer_prompts.py` to also cover `informative`, `not_applicable`, `won_t_fix`, and (where safe) <bug-bounty-platform>/Bugcrowd report-state vocabulary the direction review listed.** The current catalog text contains none of these (I spot-checked), so this is not a corrective change for the existing artifact; but the test would catch a future drift where a well-meaning author added e.g. `"informative"` to a prompt's prose. Keep `pass` / `fail` word-boundary-protected to avoid false positives on `password` (which the regex already handles), and skip `open` because it has too many benign uses ("review the candidate's open questions") to be a safe whole-word tripwire — the direction review explicitly classed `open` only "as a state", which is hard to enforce mechanically. This is a defense-in-depth improvement, not a defect.

3. **In a future slice, consider extending the test file's chain-text canary to also assert `scripts/build_candidate_workflow_fixture.py` exposes a stable chain-helper signature (the function that wires P2.19→P2.22).** The current canary only covers the two consumers that own the gate/block/check code vocabulary. The fixture builder is one rename away from drifting silently relative to the catalog if the chain ever consolidates helpers. This is forward-leaning and explicitly NOT in P3.5's scope; record it on the P3.6 / P3.7 backlog rather than landing it now.

4. **Park the reviewer-notes artifact as the explicit P3.6 candidate, exactly as the direction review recommended.** This implementation correctly resisted landing the artifact in P3.5; the next direction review should decide whether the artifact is justified now (external need surfaced?) and, if yes, whether it lands as fixture-only (no consumer; shape tests only) or as a consumer-backed artifact (fires P2.24 trigger 2 — fifth stdin consumer — and must run the helper-extraction review in the same slice). Pre-commit to neither path; let the next direction review decide.

5. **Document the catalog's "9 entries" choice in the next slice's direction review.** The direction review said "10-15 entries expected" but only as guidance; the minimum is met. A short forward-looking note in P3.6's direction prompt confirming whether 9 remains acceptable (after any future check-code or block-reason additions to `scripts/build_report_readiness_gate.py`) will prevent silent under-coverage. Not a defect of the current slice — purely future-paving.

## Deferred Follow-ups

Carrying forward the direction review's deferral list verbatim, with one P3.5-specific addition:

- Reviewer-notes artifact contract — deferred to a fresh direction review (provisional P3.6).
- Rendering surface (Markdown / HTML / web UI / IDE) — deferred to a separate slice; if attempted, keep Markdown-only and in `docs/` or `scripts/render_reviewer_prompts.py` with no chain integration.
- Chain wiring of the catalog (`scripts/build_*` consuming it; `module_runner.py` linking it into preview output; the candidate workflow fixture builder emitting prompts) — explicitly deferred.
- Any change to `modules/_schema/**`, schema promotion, validator script, or `tests/fixtures/**` directory for the catalog — explicitly deferred.
- Drafting fields (`title`, `summary`, `impact_narrative`, `steps_to_reproduce`, `remediation_prose`, `submission_text`) — explicitly deferred; do not introduce without a fresh OSS Recon Gate.
- Platform fields and platform-coupled identifiers — explicitly deferred.
- Importer/exporter / external-tool integration (SARIF, DefectDojo, <bug-bounty-platform>, Bugcrowd, webhook, notification) — explicitly deferred.
- Live-target affordance on the catalog (CLI surface, `--target` / `--url` / `--host` / `--scope` / `--live`) — explicitly forbidden; the catalog must remain a pure data file.
- P3.5-specific addition: `accepted_changes.md` entry per recommendation 1 above. Track this as a slice-closeout follow-up rather than a future-slice deferral.

A future slice that proposes a reviewer-notes **consumer** (a script reading the prompt catalog plus a `report_readiness_gate/0.1-trial` document on stdin and emitting a `reviewer_notes/0.1-trial` artifact) fires P2.24 trigger 2 (fifth stdin consumer) and **must** run a fresh P2.24 review in the same slice. Hermes should pre-flag this on any P3.6 / P3.7 proposal that mentions reviewer notes.

## Acceptance Notes

- The implementation cleanly obeys the approved P3.5 scope: data-only catalog + tests-only + a short README note, with every deferral honored and every Forbidden Files list entry untouched.
- The catalog covers all seven `GATE_*` codes, all eight `BLOCK_*` codes, and all nine `CHECK_*` codes via 9 well-formed entries; `allowed_response_postures` is closed to the four-posture set; ids are stable, unique, and sorted; canonical JSON is enforced by byte-identity test.
- The new test file's import surface is stdlib-only and within the direction-review-approved allowlist; chain vocabulary is asserted by local constant re-declaration and by text-scan canary, never by importing a chain consumer.
- The recorded validations (28 OK focused, 375 OK discover with 8 skipped, `hermes review` PASS) are consistent with the on-disk state; no shell script was touched and no schema was promoted.
- P2.24 helper-extraction is **not triggered** by this slice; the duplication watchlist remains intentional, as predicted by the direction review.
- One non-blocking gap: the `2026-05-19 — P3.5 ...` entry in `handoff/accepted_changes.md` has not yet landed. Recommendation 1 lists the four sentences it should contain. Closing this gap completes the slice's documentation surface.

Decision: **PASS_WITH_RECOMMENDATIONS**. The implementation is safe to land; the recommendations above (especially #1) should be addressed before the slice is treated as fully closed, but none of them block acceptance of the catalog and tests as implemented.
