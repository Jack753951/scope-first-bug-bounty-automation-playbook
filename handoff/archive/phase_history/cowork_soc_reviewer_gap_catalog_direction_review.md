> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Direction Review — P3.12 SOC Reviewer-Gap Catalog Only

Date: 2026-05-20
Reviewer: Claude / Cowork (direction review only)
Source prompt: `handoff/cowork_soc_reviewer_gap_catalog_direction_prompt.md`
Depends on: accepted P3.11 SOC evidence-bucket synthetic fixture
Repo truth consulted:
- `.hermes.md`
- `handoff/active_strategy_queue.md`
- `handoff/cowork_soc_evidence_bucket_direction_review.md`
- `handoff/third_party_p3_11_implementation_review.md`
- `handoff/claude_code_result_p3_11.md`
- `fixtures/soc_evidence_bucket/README.md`
- `fixtures/soc_evidence_bucket/sample_timeline_01.json`
- `scripts/test_soc_evidence_bucket_fixture.py`
- `handoff/oss_recon_gate.md`
- `handoff/review_tiering_policy.md`
- `handoff/multi_party_review_decision_policy.md`
- `handoff/active_testing_policy.md`
- `templates/report_readiness_reviewer_prompts.json` (as parallel-pattern precedent only)

Posture: design-only. No implementation. No code, scope, schema, module, runner, report, scheduler, credential, OAuth, or production change is approved by this review.

---

## 1. Final verdict

`PROCEED_CATALOG_ONLY` — accepted with narrowing.

Decision: `APPROVE_WITH_CHANGES`.

The narrowing relative to Option 1 as written in the prompt:

- The catalog lives **under `fixtures/soc_evidence_bucket/`**, not under `templates/`. Reason: `templates/report_readiness_reviewer_prompts.json` is the existing precedent for *consumer-adjacent* data, and putting a second look-alike under `templates/` invites a future reader (or runtime code) to load it. Co-locating with the P3.11 fixture preserves the "this is calibration data tied to the synthetic fixture" framing already established by the fixture README.
- The catalog is **two artifacts**: a Markdown explanation and a small JSON data file. Both are clearly marked trial / non-contractual. JSON-without-Markdown loses the human reviewer affordance; Markdown-without-JSON loses the testable vocabulary lock that prevented vocabulary drift in P3.5 and P3.11.
- The JSON's `gap_code` set must be asserted **byte-equal** to the in-fixture vocabulary in `fixtures/soc_evidence_bucket/sample_timeline_01.json` / `scripts/test_soc_evidence_bucket_fixture.py`. This is the cross-file lock that prevents the catalog from quietly growing a parallel vocabulary the fixture does not exercise.
- The vocabulary lock is the only allowed cross-file coupling. No runtime consumer, no schema, no module manifest, no report gate, no candidate-workflow consumer, no `scripts/` constant module is touched. `scripts/test_soc_evidence_bucket_fixture.py` may be extended or, preferably, a sibling test `scripts/test_soc_reviewer_gap_catalog.py` may be added — both options are acceptable; see §4.
- Reviewer-notes / reviewer-answer capture remains deferred. The catalog records *questions to ask*, never *answers given*. Capturing answers would convert this into a consumer surface and require T3 review.

Why not the other options:

- `PROCEED_MARKDOWN_ONLY` (Option 2): rejected. Markdown alone cannot enforce the gap-code vocabulary lock against the fixture; the P3.5 precedent shows that the value of a "catalog" comes precisely from the testable data-only file pinning the vocabulary. Markdown-only would leak vocabulary discipline back into prose.
- `DEFER_AND_CLOSE_SOC_THREAD` (Option 3): rejected. The P3.11 fixture is freshly grounded and the SOC lesson is still durable in the repo. Deferring now risks the calibration window closing before the catalog is written; later it becomes hard to write a non-overfit catalog because the original simulator lesson will have decayed. The next mainline platform slice can run in parallel without this catalog and is not blocked by approving a narrow catalog now.
- `BLOCK` (Option 4): rejected. The proposed boundary is offline, data-only, and reuses the precedent that P3.5 already proved safe. The risks called out in §3 are mitigable with the narrowing above and the vocabulary lock; they do not warrant a block.
- `REQUEST_OPERATOR_INPUT` (Option 5): rejected. Nothing in the slice touches `config/scope.txt`, program scope, runtime behavior, callbacks, credentials, scheduler, billing, deployment, or any surface that requires operator activation. Hermes has direct authority at this tier under the multi-party review decision policy.

Recommended slice name: `P3.12 — SOC reviewer-gap catalog only (offline, non-contractual; co-located with P3.11 fixture)`.

---

## 2. Review tier and authority

Tier: **T2** (standard implementation: offline data, docs, tests).

Why T2 and not T3:

- No new schema is added under `modules/_schema/` or any `*/0.1-trial` location.
- No module manifest, runner surface, validator, or runtime gate is created.
- The catalog is not loaded by any existing consumer. The only consumer is the sibling test, which asserts well-formedness and vocabulary equality with the fixture.
- The JSON is a flat trial marker (e.g. `soc_reviewer_gap_catalog_v0_trial`), explicitly distinguished from chain schemas — mirroring the P3.5 discipline.
- The catalog vocabulary is the fixture's vocabulary; it does not introduce a *new* shared vocabulary that other code would import.

Escalation triggers that would force T3 (must therefore be avoided in this slice):

- creating a Python module under `scripts/` (or anywhere) that *defines* the gap-code or status vocabulary as constants other code imports — the vocabulary must continue to live in the fixture/test/catalog data only
- wiring the catalog into any existing candidate-workflow consumer (`scripts/build_candidate_review_packet.py`, `scripts/review_candidate_packet_gaps.py`, `scripts/build_candidate_verification_plan.py`, `scripts/build_report_readiness_gate.py`, `scripts/build_candidate_workflow_fixture.py`, or any future consumer)
- adding a reviewer-prompt JSON under `templates/` that the existing report-readiness gate consumer reads, or otherwise giving the SOC catalog a path into the chain
- promoting any field set under `modules/_schema/` or any `*/0.1-trial` schema location
- adding tests that assert a *production* contract uses the catalog vocabulary
- adding any reviewer-answer / reviewer-notes capture surface (still deferred)

If during implementation any of the above triggers appears unavoidable, the slice must stop and re-enter a fresh T3 direction review with full OSS Recon Gate.

Hermes authority: **direct**.

Per `handoff/multi_party_review_decision_policy.md` table:

- T2 + reviewers aligned + no external-side-effect activation → Hermes direct.
- Operator approval is **not** required because the slice introduces no contract, no runtime path, no safety-boundary change, no external side effect, no scope/policy change, no scanner/module execution, no target interaction, and no public-submission path.
- Operator approval becomes required if any §5 forbidden surface comes into play, or if any reviewer materially disagrees on safety during implementation review.

Independent implementation review: **required** at slice completion. Route is Hermes' choice (Claude Code implementation review, Codex fresh-context, or a fresh-context Cowork pass). Reviewer must record route/tool and visible model/runtime in the implementation review artifact, with the limitation explicitly stated if model/runtime is not exposed by the harness — matching the P3.11 reviewer-disclosure pattern.

---

## 3. OSS Recon Gate posture and risk analysis

### 3.1 OSS Recon Gate requirement

Strictly per `handoff/review_tiering_policy.md` and `handoff/oss_recon_gate.md`:

- T2 changes that do not introduce or materially change platform contracts, schemas, modules, runners, reports, evidence/finding lifecycles, external-tool integrations, or update mechanisms **do not require** a formal OSS Recon Gate.
- P3.12 as narrowed in §1 does not introduce any of those surfaces. The catalog is data co-located with the synthetic fixture and used only by a sibling test.

Therefore: **OSS Recon Gate is informational, not required.**

However, since the catalog's vocabulary could later influence a T3 contract slice (a real reviewer-prompt consumer, or a SOC evidence record schema), this review records the informational adopt/adapt/ignore deltas relative to the P3.11 direction review so a future T3 review does not re-derive them from scratch.

### 3.2 Informational OSS adopt/adapt/ignore deltas (built on top of the P3.11 informational baseline)

The P3.11 direction review already recorded adopt/adapt/ignore notes for MITRE ATT&CK, Sigma / Elastic detection rules, STIX 2.1 / OpenCTI, SARIF, and DefectDojo / <bug-bounty-platform> / Bugcrowd reviewer-workflow concepts. Those notes carry over unchanged. For P3.12 specifically, the relevant deltas are:

- **DefectDojo / <bug-bounty-platform> / Bugcrowd reviewer-workflow concepts**
  - Useful pattern (catalog-specific): each gap category carries a short, neutral reviewer prompt rather than free-text. This is precisely the discipline already proven by `templates/report_readiness_reviewer_prompts.json`.
  - Adopt/adapt/ignore: **Adapt** the "gap_code → reviewer_prompt" pairing and the closed allowed-response-posture pattern (in this catalog, the closed set is the in-fixture status vocabulary: `needs_more_evidence`, `needs_mapping_review`, `needs_asset_reconciliation`, `needs_second_pass_hunt`, `not_report_ready`). **Ignore** platform lifecycle states (`triaged`, `accepted`, `resolved`, `duplicate`, `informative`, `won_t_fix`, `not_applicable`), submission language, severity axes, scanner-confirmed vocabulary, ticket IDs, and any external-side-effect verbs.
  - Safety concern: the closer the prompts read to "is this ready to submit?" the more the catalog risks report-readiness creep. Prompts must remain *evidence-completeness questions*, not submission-readiness gates.
  - Contract impact (future): a later T3 review could decide whether SOC gap codes harmonize with the existing report-readiness `BLOCK_*` / `CHECK_*` / `GATE_*` vocabulary; this slice deliberately does not pre-commit that.

- **Semgrep rule metadata / SARIF `rule` objects**
  - Useful pattern: each rule/prompt carries `id`, short `message`/`prompt_text`, optional `metadata`. Stable IDs are sortable and reviewable.
  - Adopt/adapt/ignore: **Adapt** the "stable string ID + short prompt + small metadata block" shape per entry. **Ignore** any rule-evaluation semantics, severity axes, fix suggestions, or auto-remediation language.
  - Safety concern: SARIF/Semgrep idiom encourages thinking of entries as *rules that fire*. The catalog entries must read as *questions a human asks*, never as detection rules. Avoid words like `match`, `trigger`, `detect`, `firing`, `rule`.
  - Contract impact (future): a later T3 review could decide whether catalog entry IDs become part of a real reviewer-prompt contract; deliberately not pre-committed here.

- **MITRE ATT&CK technique/sub-technique vocabulary**
  - Useful pattern (catalog-specific): the `PARENT_TECHNIQUE_TOO_BROAD` gap code already maps cleanly to a reviewer prompt about sub-technique specificity.
  - Adopt/adapt/ignore: **Adopt** the gap code as already present in the fixture and surface a single neutral reviewer prompt for it; do not import or vendor an ATT&CK STIX bundle, technique catalog, or any external taxonomy file.
  - Safety concern: ATT&CK strings must remain *labels for review*, never automatic findings. The catalog must not embed a "confirmed technique" notion.
  - Contract impact (future): unchanged from P3.11 baseline.

### 3.3 Risks of vocabulary promotion, schema creep, report-readiness creep, and runtime coupling

These are the four named risks in the prompt; each is addressed below with the mitigation that defines this slice's narrowing.

**Vocabulary promotion risk.** A new catalog of reviewer prompts looks authoritative. Other code, future tests, or future agents could begin importing the catalog as the source of truth for "the SOC gap-code vocabulary." Mitigation:

- The catalog explicitly states (in its own header and in its Markdown sibling) that the vocabulary lives in `fixtures/soc_evidence_bucket/sample_timeline_01.json` + `scripts/test_soc_evidence_bucket_fixture.py`; the catalog is a *companion artifact*, not the source of truth.
- The vocabulary-equality test in §5 enforces this by failing closed if the catalog and the fixture-side allow-list ever diverge.
- No Python constants are introduced. There is no "import this module to know the gap codes" surface.

**Schema creep risk.** A JSON file with `entries`, `id`, `metadata`, and a version-like marker can easily be mistaken for the start of a schema and pull a future reader toward promoting it under `modules/_schema/` or a `*/0.1-trial` location. Mitigation:

- Flat marker style (e.g. `soc_reviewer_gap_catalog_v0_trial`) — deliberately not slash-shaped, mirroring the P3.5 precedent.
- Top-level `version` is `0` (integer) or `"0"` (string); version promotion requires its own future direction review.
- Markdown sibling states explicitly: "this catalog is a data file with a flat marker, deliberately not a `*/0.1-trial` schema; no validator script reads it, only the sibling test in `scripts/`."
- The catalog stays under `fixtures/soc_evidence_bucket/`, not `modules/_schema/`, not `templates/`, not any directory whose existing semantics imply schema or consumer-ready data.

**Report-readiness creep risk.** Reviewer prompts naturally drift toward "is this ready to write up?" language. That would import the report-readiness gate's job into a separate SOC-flavored vocabulary. Mitigation:

- Prompts must be **evidence-completeness questions** ("what evidence is missing?" / "which asset role is ambiguous?" / "is the parent technique still too broad?"), never report-readiness questions ("is this ready to submit?" / "should this be reported?" / "what severity?").
- The closed allowed-response-posture set is the fixture's non-promotional status vocabulary only; promotional terms like `submit_ready`, `report_ready`, `confirmed_finding`, `live_target`, `production`, `real_target`, `real_credential`, `severity`, `cvss`, `impact_score`, `triaged`, `accepted`, `resolved`, `duplicate`, `informative`, `won_t_fix`, `not_applicable` are forbidden by the negative-string test in §5.
- The Markdown sibling explicitly cross-links to `templates/report_readiness_reviewer_prompts.json` as a *parallel pattern reference*, not a consumer dependency, and states that the SOC catalog does not replace, extend, or wire into the report-readiness gate.

**Runtime coupling risk.** Any consumer that loads the catalog (even a test that imports an existing chain consumer to read it) becomes the first cross-file coupling and silently expands the slice. Mitigation:

- The only allowed consumer is the sibling test, and that test imports only standard library modules (`json`, `pathlib`, `re`, `unittest`).
- The test does **not** import any chain consumer (`build_candidate_review_packet`, `review_candidate_packet_gaps`, `build_candidate_verification_plan`, `build_report_readiness_gate`, `build_candidate_workflow_fixture`, `module_runner`, etc.).
- The test does not import the existing P3.5 reviewer-prompts test either; it stands alone.
- The vocabulary lock between the catalog and the fixture is implemented by re-reading the fixture JSON at test time and comparing sets, not by importing a constants module.

---

## 4. Exact allowed implementation boundary

The implementation slice that may follow this review may:

- Add `fixtures/soc_evidence_bucket/reviewer_gap_catalog.md` — a short Markdown explanation that:
  - Names the slice (`P3.12 SOC reviewer-gap catalog only`).
  - States the catalog is **trial, non-contractual, offline, non-promotional, calibration-only**.
  - States the vocabulary lives in `fixtures/soc_evidence_bucket/sample_timeline_01.json` and `scripts/test_soc_evidence_bucket_fixture.py`; the catalog is a *companion artifact*, not the source of truth.
  - States the catalog is not loaded by any runtime consumer, not a schema, and must not be wired into any chain consumer, scope helper, report gate, module manifest, run manifest, scanner adapter, SIEM/Elastic/Kibana/Splunk integration, or platform adapter without a fresh T3+ direction review.
  - Cross-links to `templates/report_readiness_reviewer_prompts.json` as a *parallel pattern reference* only; explicitly states it does not replace, extend, or wire into the report-readiness gate.
  - Documents the per-entry shape (`id`, `gap_code`, `prompt_text`, optional small `metadata`) and the closed `allowed_response_postures` set (matching the fixture's non-promotional status vocabulary).
  - Forbids substituting real lab data, credentials, simulator hashes, captured logs, real domains, real public IPs, or real bug-bounty platform language.
- Add `fixtures/soc_evidence_bucket/reviewer_gap_catalog.json` — a static JSON data file that:
  - Has top-level keys: `schema_marker` (string literal, flat, deliberately not slash-shaped — recommended `"soc_reviewer_gap_catalog_v0_trial"`), `version` (`0` integer or `"0"` string), `entries` (list of entry objects).
  - Each entry object has: `id` (stable, sorted, snake-case, prefixed e.g. `p3_12_prompt_<topic>`), `gap_code` (exact string from the in-fixture vocabulary), `prompt_text` (short neutral question), `allowed_response_postures` (subset of the fixture's non-promotional status vocabulary; non-empty), optional `metadata` (small flat map, no nested structure beyond one level).
  - Exactly one entry per gap code in the in-fixture vocabulary (all 12). Two entries for the same gap code are not approved by this slice (avoids subtle vocabulary fragmentation); future slices may revisit.
  - Pretty-printed for human review, but round-trips byte-identical to `json.dumps(..., sort_keys=True, indent=2)` to enforce stable diffs (mirrors the P3.5 discipline).
- Add **either** (a) a sibling test `scripts/test_soc_reviewer_gap_catalog.py` **or** (b) extend `scripts/test_soc_evidence_bucket_fixture.py` with a new test class. Option (a) is preferred for separation of concerns. Whichever is chosen, the new test must use only standard library imports (`json`, `pathlib`, `re`, `unittest`) and must implement the assertions in §5.
- Update `handoff/accepted_changes.md` (append-only) with the slice summary, files added, validation performed, safety boundary, and reviewer route/tool plus visible model/runtime if exposed (otherwise the explicit limitation).
- Update `handoff/active_strategy_queue.md` to mark P3.12 accepted, re-list the still-deferred trial-consumer design slice with its re-trigger conditions, and update the "Current Lane" pointer.
- Update `notes/daily/2026-05-20.md` (or the date of acceptance) with a short note.

The implementation may **not**:

- Place the catalog under `templates/`, `modules/`, `modules/_schema/`, `scripts/`, `runs/`, `scans/`, `reports/`, `loot/`, `logs/`, `config/`, `programs/`, or any `*/0.1-trial` location.
- Introduce a Python module (under `scripts/` or elsewhere) that defines the gap-code or status vocabulary as constants other code imports.
- Wire the catalog into any existing candidate-workflow consumer, the report-readiness gate, any module runner, any validator, any recon code, any scanner adapter, any SIEM/Elastic/Kibana/Splunk path, any platform adapter, or any reviewer-notes capture surface.
- Add a reviewer-answer or reviewer-notes capture artifact (still deferred to a separate future direction review).
- Modify `templates/report_readiness_reviewer_prompts.json`, `scripts/test_report_readiness_reviewer_prompts.py`, `scripts/build_report_readiness_gate.py`, `scripts/review_candidate_packet_gaps.py`, or any other existing chain consumer/test.
- Promote any field name into `modules/_schema/`, any module manifest, any run-manifest field, or any candidate-workflow field.
- Substitute any real lab data, credentials, simulator hashes, captured logs, real domains, real public IPs, real bug-bounty platform URLs, or any loot-class artifact.
- Write to `loot/`, `logs/`, `scans/`, `runs/`, or `reports/`.
- Consult any real SIEM, Elasticsearch, Kibana, TryHackMe, TryGovMe, <bug-bounty-platform>, Bugcrowd, Intigriti, Synack, YesWeHack, or external service.

---

## 5. Exact forbidden surfaces

The following surfaces are explicitly out of scope. Touching any of them requires returning to direction review:

- Live SIEM / Elastic / Kibana / Splunk / any log-aggregation integration.
- Target-touching behavior of any kind: scan, probe, fuzz, brute force, exploit, callback, OAST, proxy, pivot, tunnel, beacon, relay, reverse listener, DNS exfil, webhook to external host.
- Scanner or module execution (nuclei, httpx, subfinder, naabu, katana, ffuf, dnsx, etc.).
- `recon.sh` runtime, `safe_target`, `--skip-scope-check`, or any scope/policy gate change.
- `config/scope.txt` change.
- Any change under `programs/*/scope.json` or `programs/*/rules*.json` other than `programs/_examples/` synthetic fixtures, and even those are out of scope for this slice.
- Module runner change (`scripts/module_runner.py`).
- Run manifest change (`scripts/validate_run_manifest.py`, `scripts/test_run_manifest_schema.py`).
- Schema promotion or addition under `modules/_schema/` or any trial schema directory.
- Report drafting, report rendering, report submission, HTML/Markdown finding output, platform adapter (<bug-bounty-platform>, Bugcrowd, DefectDojo, etc.).
- Reviewer-prompt JSON wiring into existing consumers, including any change to `templates/report_readiness_reviewer_prompts.json` consumers or its sibling test `scripts/test_report_readiness_reviewer_prompts.py`.
- Any reviewer-notes / reviewer-answer capture artifact.
- Trial-consumer plan, design, or stub (still deferred to its own future direction review).
- Credentials, cookies, OAuth, tokens, API keys, private keys, .env, lab secrets, password hashes, or any loot-class data.
- Loot/, logs/, `*.pcap`, `*.cap`, `*.kdbx`, `*.key`, `*.pem`, `creds*` — none may be committed, referenced, or substituted into the catalog.
- Real TryHackMe / TryGovMe screenshots, log exports, simulator hashes, or simulator-specific IOCs.
- Scheduler, CI activation, cron, systemd, deployment, billing, publishing, or any persistent automation.
- Production-side settings, repo permissions, Git ignore weakening, branch protection.
- Subagent or model-route changes.
- Live mode flags or anything that flips dry-run defaults.

---

## 6. Minimum validation expectations

The implementation must record all of the following as having passed before the slice is accepted:

- `python -m unittest scripts.test_soc_reviewer_gap_catalog` (or, if extending the existing test file, `python -m unittest scripts.test_soc_evidence_bucket_fixture`) — green.
- `python -m unittest discover scripts` — green; no regression in candidate workflow, runner, bridge, run-manifest, report-readiness, or P3.11 fixture tests.
- `HACKLAB=$(pwd) ./bin/hermes review` — Python compile OK, shell scripts `bash -n` OK, lock clear, recon scope entries unchanged, no `accepted_changes.md` truncation, no new secrets-style strings introduced.
- `git diff --check` — clean (line-ending warnings tolerated as elsewhere in the repo).
- Added-line scan for target-touching or live-mode strings — zero hits for: `http://`, `https://`, `ftp://`, any real public domain reference, `nuclei`, `httpx`, `subfinder`, `naabu`, `katana`, `ffuf`, `dnsx`, `subprocess`, `requests.`, `urllib`, `socket.`, `loot/`, real credential-like patterns, real SIEM endpoints, real TryHackMe/TryGovMe URLs, real <bug-bounty-platform>/Bugcrowd/Intigriti/Synack/YesWeHack URLs.
- No new files under `loot/`, `logs/`, `scans/`, `runs/`, `reports/`, `config/`, `programs/<real-slug>/`, `modules/`, `modules/_schema/`, `templates/`, or the runtime path.

Test-level assertions the new/extended test must make (this is the binding contract for the slice):

1. **Parse / shape.** JSON parses; top-level has `schema_marker`, `version`, `entries`; `entries` is a non-empty list.
2. **Stable marker.** `schema_marker` is a flat lowercase underscore-delimited string containing `trial` and is **not** slash-shaped (assertion: `"/" not in schema_marker`). Recommended literal: `"soc_reviewer_gap_catalog_v0_trial"`.
3. **Stable version.** `version` is `0` or `"0"`.
4. **Stable, sorted IDs.** Entry IDs are unique, snake_case, prefixed (e.g. `p3_12_prompt_*`), and the list is sorted by `id`.
5. **Vocabulary lock (cross-file).** The set of `gap_code` values across `entries` is **byte-equal** to the in-fixture allowed gap-code vocabulary read from `scripts/test_soc_evidence_bucket_fixture.py` *or* re-declared as a local constant whose value equals `ALLOWED_GAP_CODES` in that file. The preferred implementation re-declares the constant locally (mirroring the P3.5 discipline of not importing the chain) and adds a separate test that re-reads the P3.11 test file as text and asserts the local constant string appears verbatim, so drift fails closed.
6. **Coverage.** Exactly one entry per gap code in the allowed vocabulary (12 entries total). No duplicates.
7. **Closed posture set per entry.** `allowed_response_postures` is non-empty and a subset of the in-fixture non-promotional status vocabulary (`needs_more_evidence`, `needs_mapping_review`, `needs_asset_reconciliation`, `needs_second_pass_hunt`, `not_report_ready`), re-declared as a local constant.
8. **Prompt shape.** `prompt_text` is a non-empty string under a reasonable length cap (e.g. ≤ 300 chars), contains no URL scheme, no scanner/SIEM/platform name, no severity/CVSS/impact axis, and no submission/lifecycle vocabulary (negative whole-word lock against `submit_ready`, `report_ready`, `confirmed_finding`, `live_target`, `production`, `real_target`, `real_credential`, `severity`, `cvss`, `impact_score`, `triaged`, `accepted`, `resolved`, `duplicate`, `informative`, `won_t_fix`, `not_applicable`, `cve`, `cwe`, `epss`).
9. **Round-trip stability.** `json.dumps(json.loads(text), sort_keys=True, indent=2) + "\n"` equals the on-disk bytes (LF, UTF-8 no BOM). This prevents accidental drift of formatting.
10. **No runtime imports / no consumer wiring.** The test imports only `json`, `pathlib`, `re`, `unittest` (and `ipaddress` only if reused from P3.11; not needed here). A `git grep` style assertion (or re-read of the test source) confirms the test does not reference `build_candidate_review_packet`, `review_candidate_packet_gaps`, `build_candidate_verification_plan`, `build_report_readiness_gate`, `build_candidate_workflow_fixture`, `module_runner`, `recon`, or any chain consumer.
11. **Markdown sibling posture.** The Markdown file is present and contains the literal phrases `synthetic`, `non-promotional`, `not a contract`, `offline`, `companion artifact`, and the cross-link sentence to `templates/report_readiness_reviewer_prompts.json` as a *parallel pattern reference only*. The Markdown file must not contain any URL scheme, scanner name, SIEM endpoint, or real platform domain.
12. **Negative drift assertion.** A documented test (or test comment) explicitly states that if a gap_code is added to the catalog without also being added to the fixture vocabulary, or vice versa, this test must fail closed — mirroring the P3.11 "synthetic-range" negative-test contract.

Optional but recommended:

- `git grep -n "soc_reviewer_gap_catalog"` should return matches only under `fixtures/soc_evidence_bucket/`, `scripts/test_soc_reviewer_gap_catalog.py` (or the extended P3.11 test file), `handoff/`, and `notes/`. No match outside those allowed paths.

---

## 7. Claude implementation turn-budget convention

**Use the adjusted temporary turn budget convention; do not raise the global default.**

Specifically:

- Keep the repo default `CLAUDE_IMPL_MAX_TURNS=25` in `bin/hermes` unchanged.
- For this slice, invoke as `CLAUDE_IMPL_MAX_TURNS=35 HACKLAB=$(pwd) ./bin/hermes claude-impl` (recommended starting point) or `CLAUDE_IMPL_MAX_TURNS=40 HACKLAB=$(pwd) ./bin/hermes claude-impl` if early evidence in the run shows the test file is taking many small edits.

Rationale:

- P3.11 hit `error_max_turns` at `num_turns=26` with the default of 25 and required Hermes fixup. P3.12 is in the same fixture/docs/test/handoff-heavy category and will plausibly need similar capacity (Markdown + JSON + test file + handoff updates + active-strategy-queue update + accepted-changes append + daily note).
- The recent operator convention (recorded in `handoff/active_strategy_queue.md` "Current Lane") is exactly: keep the repo default at 25, raise per-invocation for fixture/test/handoff-heavy offline slices, and only consider raising the global default if repeated slices systematically exhaust the per-invocation raise. Two slices is not enough evidence to change the default.
- The invocation-level raise is preferable because it preserves the small-default safety property (a misbehaving long-running plan is bounded) while giving this specific narrow slice room.

If Claude implementation again exceeds the per-invocation budget for this slice, Hermes should record the budget exhaustion in the implementation result artifact (matching the P3.11 `error_max_turns` disclosure), complete any minimal remaining work itself within the approved §4 boundary, and treat the third consecutive over-budget run as the trigger for a separate review of whether to raise the global default. Do not raise the global default as part of P3.12 acceptance.

---

## 8. Whether existing precedent / helper extraction is implicated

**Not implicated.**

- The deferred shared helper `scripts/core/offline_consumer.py` is *not* touched by this slice. The new test imports nothing from a shared offline-consumer helper.
- The existing P3.5 reviewer-prompts catalog (`templates/report_readiness_reviewer_prompts.json`) and its sibling test (`scripts/test_report_readiness_reviewer_prompts.py`) are *not* extended, modified, or wired to. The two catalogs remain entirely separate. They share only a *pattern*, not a contract.
- The candidate-workflow chain (build_candidate_review_packet → review_candidate_packet_gaps → build_candidate_verification_plan → build_report_readiness_gate → build_candidate_workflow_fixture) is not touched.
- The P2.24 fifth-stdin-consumer trigger is not pulled. The new test is the catalog's only "consumer" and is a stdlib-only unittest, not a chain stdin consumer.
- A future direction review may decide whether the SOC gap-code vocabulary should be harmonized with the report-readiness gate's `GATE_*` / `BLOCK_*` / `CHECK_*` vocabulary. P3.12 deliberately preserves the option to harmonize *or* keep them separate; either decision can be made later without rework, because nothing in this slice asserts harmonization.

---

## 9. Multi-Party Review Decision final block

```text
Decision: APPROVE_WITH_CHANGES
Tier: T2
Milestone: Post-P3.10 project workflow calibration — P3.12 SOC reviewer-gap catalog only (offline, non-contractual; co-located with P3.11 fixture)
Hermes authority: direct
Reviewers consulted:
- Claude / Cowork direction review (this document); visible model/runtime: not exposed by Cowork harness — recorded as limitation per multi-party review decision policy
- Implementation review required at slice completion: a fresh-context implementation reviewer (Claude Code implementation review, Codex fresh-context, or fresh-context Cowork pass — Hermes selects); visible model/runtime to be recorded at that time, with explicit limitation statement if not exposed
- Safety reviewer: Hermes safety gate (the slice has no target-touching surface, so a separate safety reviewer is not required beyond Hermes synthesis; if implementation drifts toward any runtime wiring, schema promotion, chain consumer wiring, reviewer-notes capture, or any §5 forbidden surface, a Cowork safety re-review must be triggered)
- Architecture/roadmap reviewer: this direction review (Cowork)
Validation performed (at direction review):
- Read .hermes.md, review_tiering_policy.md, multi_party_review_decision_policy.md, oss_recon_gate.md, active_testing_policy.md
- Read active_strategy_queue.md, cowork_soc_evidence_bucket_direction_review.md, third_party_p3_11_implementation_review.md, claude_code_result_p3_11.md
- Inspected fixtures/soc_evidence_bucket/README.md, fixtures/soc_evidence_bucket/sample_timeline_01.json, scripts/test_soc_evidence_bucket_fixture.py for vocabulary set and posture
- Inspected templates/report_readiness_reviewer_prompts.json and the P3.5 review/test as parallel-pattern precedent
- Confirmed no current runtime touches the proposed catalog path
- Confirmed the in-fixture gap-code vocabulary is exactly 12 codes and the in-fixture status vocabulary is exactly 5 codes (used to size catalog coverage assertion in §6)
Blocking findings:
- None at direction-review stage. The slice is APPROVE_WITH_CHANGES because the narrowed location (fixtures/, not templates/), the dual Markdown+JSON requirement, the cross-file vocabulary lock, the closed allowed-response-posture set, the negative-vocabulary lock, and the forbidden runtime-coupling assertions are required modifications relative to Option 1 as written in the prompt.
Non-blocking recommendations:
- After P3.12 acceptance, a separate future T3 direction review may evaluate whether the SOC gap-code vocabulary should harmonize with the report-readiness gate's GATE_*/BLOCK_*/CHECK_* vocabulary. Defer until concrete pressure exists.
- Consider, in a *separate* future T2/T3 direction review, whether a third SOC fixture stage variant (sparse-evidence early-stage incident, dense-evidence late-stage incident) would calibrate prompts further. Out of scope here.
- The Markdown sibling should include a one-line statement that this catalog does not replace, extend, or wire into the report-readiness gate, and a one-line statement that reviewer-answer/reviewer-notes capture remains deferred.
- If extension of `scripts/test_soc_evidence_bucket_fixture.py` is chosen over a new sibling test file, keep the new assertions in a clearly named separate `TestCase` class so future readers can see the catalog-vs-fixture lock without mixing concerns.
Safety boundary:
- Offline, synthetic, redacted only. No SIEM/Elastic/Kibana/Splunk, no scanner/module execution, no target-touching, no scope/config changes, no schema promotion, no report drafting/submission, no credentials/loot, no scheduler/CI activation, no proxy/pivot/transport, no reviewer-answer capture. RFC reserved ranges and example.tld only (and the catalog itself contains no IPs/hostnames/URLs).
OSS Recon Gate: attached as informational baseline (not formally required at T2); adopt/adapt/ignore deltas recorded in §3.2 so a future T3 contract review does not start from zero.
User approval required: no.
- Reason: the slice is offline data/docs/tests only, introduces no contract, no runtime path, no safety-boundary change, no external side effect, and no scope/policy change. Hermes has direct authority at T2 per the multi-party review decision policy table.
- Operator approval becomes required if any forbidden surface in §5 is later in play, if any reviewer disagrees materially on safety, or if drift toward a runtime consumer / schema / report path / reviewer-notes capture is observed during implementation.
Accepted changes updated: not applicable at direction-review stage; required at implementation acceptance per §6.
Next action:
- Hermes synthesizes this verdict, prepares a narrow implementation task at handoff/claude_code_task.md (or handoff/codex_task.md depending on routing) restricted to §4, §5, and §6, runs hermes review pre- and post-implementation, invokes Claude Code implementation with the per-invocation turn budget raise from §7 (CLAUDE_IMPL_MAX_TURNS=35 or 40), requests a fresh-context implementation review at slice completion, then records acceptance in handoff/accepted_changes.md and handoff/active_strategy_queue.md.
```

---

## Reviewer self-disclosure (multi-party policy add-on)

- Reviewer route/tool: Claude / Cowork direction-review session invoked via the Hermes cowork task path.
- Visible model/runtime: not exposed to this reviewer by the harness. Recorded as a limitation in line with `handoff/multi_party_review_decision_policy.md`.
- This reviewer did not execute any scan, probe, scanner, module, callback, exploit attempt, brute force, fuzz, OAST, or target-touching action.
- This reviewer did not modify `config/scope.txt`, program scope files, runtime behavior, schemas, modules, reports, credentials, scheduler, deployment, billing, OAuth, or production settings during this review.
- Only the file `handoff/cowork_soc_reviewer_gap_catalog_direction_review.md` (this document) was written; no other repository file was modified.
