> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.6 Direction Review — Reviewer Notes Artifact / Multi-Party Review Output Boundary

Date: 2026-05-19
Reviewer route/tool: Claude Code MAX/OAuth via `hermes claude-impl` (design-only direction review, read-only inspection plus this one review file). The visible runtime/tool is the Claude Code CLI; the exact backing API/runtime version is not exposed by the tool surface.
Visible model/runtime model: Claude Opus 4.7 (per the session's own self-reported model id `claude-opus-4-7`). The exact runner identifier inside Anthropic's hosting is not exposed by the tool surface; this is the strongest model identification available without crossing a tool-output boundary.
Review tier: T3 direction review (one structural element under evaluation — periodic-review artifact templates — would be T1; the slice is tiered at the highest applicable element).
Milestone: Phase 3, candidate slice 6 (after P3.1 curated fixtures, P3.2 terminal-state matrix, P3.3 two-module discovery coverage, P3.4-alt runner-indifference coverage, P3.5 data-only reviewer-prompt catalog).
Source prompt: `handoff/cowork_p3_6_direction_prompt.md`.
Predecessors: `handoff/cowork_p2_24_direction_review.md`, `handoff/cowork_p3_5_direction_review.md`, `handoff/third_party_p3_5_implementation_review.md`, `handoff/multi_party_review_decision_policy.md`, `handoff/review_tiering_policy.md`, `handoff/oss_recon_gate.md`.

Decision: APPROVE_WITH_CHANGES.

## Executive Summary

**Adopt Option 1 (DEFER reviewer-notes artifact) plus a strictly scoped Option-1 sub-slice: tighten `handoff/periodic_reviews/YYYY-MM-DD/` templates so scheduled multi-party reviews follow `handoff/multi_party_review_decision_policy.md` without introducing any new chain consumer, schema, fixture root, or runtime wiring.** Reject Options 2, 3, 4, and 5 for P3.6 specifically; each would either introduce premature contract surface, fire a P2.24 trigger, or <program-name>-load schema work that has no current consumer.

Concretely, P3.6's approved surface is:

1. Update `handoff/periodic_reviews/2026-05-18/review_template.md` in place (or, preferably, add a sibling `handoff/periodic_reviews/review_template_v0.md` so the 2026-05-18 dated artifact remains a frozen snapshot of the older shape) so the template explicitly captures the four reviewer roles, the Multi-Party Review Decision Block, OSS Recon Gate applicability, Hermes authority level, and the operator-approval-required flag, in the language that `handoff/multi_party_review_decision_policy.md` adopted on 2026-05-19.
2. Add a short README-style index at `handoff/periodic_reviews/README.md` that explains the directory's purpose, the template's lineage, the cadence (informational; not a scheduler change), and the rule that *no periodic review artifact may carry a `*/0.1-trial` schema header or be machine-parsed by any chain consumer*.
3. Add one optional empty-skeleton "next periodic review" folder pre-populated with the new template (`handoff/periodic_reviews/<NEXT_DATE_PLACEHOLDER>/`) only if Hermes prefers to land the placeholder now; this is non-blocking, may be deferred to the actual next cadence, and must not be implemented as anything other than empty placeholder Markdown files.

The reviewer-notes artifact itself — whether fixture-only or consumer-backed — is **DEFERRED**, with explicit re-trigger conditions documented below. No external operator need has surfaced for it. The P3.5 catalog is already usable by humans and by Claude/Cowork reading the JSON directly; an artifact contract is currently a solution looking for a problem, and landing one now either creates an unverifiable fixture-only contract or fires the P2.24 fifth-stdin-consumer trigger (mandating an in-slice helper-extraction review) — neither buys real reviewer-workflow value at this phase.

Choosing the periodic-review-templates path for P3.6 has three concrete benefits: (a) it operationalizes `handoff/multi_party_review_decision_policy.md` (which is policy-only as of 2026-05-19 and has no operational artifact yet); (b) it consolidates the multi-party review output surface where it actually belongs (a milestone/periodic artifact directory, not the candidate-chain runtime); (c) it avoids both the P2.24 trigger and any schema promotion, while still progressing the project's overall review hygiene.

## Review Tier and Milestone Boundary

- **Tier: T3 direction review** (because it touches a workflow artifact surface that future Phase 3 slices may key off — periodic review templates and the multi-party policy's operationalization). The implementation slice that follows is T1 (Markdown templates, no executable surface), but the *direction* must be reviewed at T3 because it pre-decides which of the five options to pursue and pre-commits the deferral of a contract-shaped artifact.
- **Milestone: Phase 3, slice 6** (review-workflow consolidation), after P3.5 closeout. This is a workflow/governance slice, not a chain-consumer slice. It does not extend the P2.19→P2.23 candidate workflow chain or the P3.5 catalog. It does not promote any schema. It does not introduce or modify any runtime path.
- **No new milestone** is required for the periodic-review-template work; reuse Phase 3's existing milestone framing. A new milestone would be needed if and when the reviewer-notes artifact itself is approved in a future direction review (provisional P3.7 or later).

## Decision

**APPROVE_WITH_CHANGES.** The five options posed by `handoff/cowork_p3_6_direction_prompt.md` decompose as follows:

- **Option 1 (DEFER reviewer-notes artifact; tighten periodic multi-party review artifacts): APPROVE.** This is the slice's primary surface. See "Approved Scope" below.
- **Option 2 (Data-only reviewer-notes fixture/artifact sketch, no consumer, no schema, no runtime wiring): REJECT.** A fixture with no consumer is fundamentally unverifiable beyond shape — its tests can only assert "this JSON parses and these keys exist". That is a documentation artifact dressed as data; documenting it as data invites a future "while we're here" consumer slice that quietly converts the sketch into a contract without the contract review that would otherwise be required. The P3.5 catalog is already the safe place to land "data-only reviewer surface"; adding a second one in P3.6 is duplicate surface without duplicate value.
- **Option 3 (Consumer-backed reviewer-notes artifact reading P3.5 catalog and/or P2.22 gate output, emitting reviewer notes): REJECT for P3.6.** This fires P2.24 revisit trigger 2 (fifth stdin consumer joining the chain) per `handoff/cowork_p2_24_direction_review.md` lines 274-279 and `handoff/cowork_p2_25_closeout_review.md` lines 396-414. The P2.24 review itself anticipated this exact scenario (`handoff/cowork_p3_5_direction_review.md` line 282: "A future slice that proposes a reviewer-notes *consumer* — i.e., a script that reads the prompt catalog plus a `report_readiness_gate/0.1-trial` document on stdin and emits a `reviewer_notes/0.1-trial` artifact — *would* fire trigger 2 (fifth stdin consumer) and require a fresh P2.24 review"). Approving Option 3 now would require landing the P2.24 helper extraction (`scripts/core/offline_consumer.py` with the strictly bounded public surface in `handoff/cowork_p2_24_direction_review.md` lines 178-220) in the same slice — a structurally larger T3 contract change than P3.6 is sized for. If the project later decides Option 3 is justified, it must be its own direction review with its own OSS Recon Gate and must explicitly run the P2.24 extraction-or-defer decision in-scope.
- **Option 4 (Core offline-consumer helper extraction first, before any reviewer-notes consumer): REJECT for P3.6.** This is the prerequisite for Option 3, not an alternative to Option 1. Doing it speculatively (before a reviewer-notes consumer is approved) <program-name>-loads a refactor whose only justification is a slice that does not yet exist; `handoff/cowork_p2_24_direction_review.md` explicitly chose to defer this exact refactor until a real trigger appears, and chose deferral on safety grounds (centralization of `LIVE_TARGET_FLAGS` and `reject_all_args(...)` is described as an "attractive nuisance" — see lines 31-46). Reversing that decision without the triggering consumer in hand would weaken the safety argument for the deferral itself.
- **Option 5 (Schema/contract promotion for reviewer notes): REJECT and explicitly forbid for P3.6.** Promotion to `modules/_schema/**` would be a T3+ contract change with full OSS Recon Gate and likely operator approval; it is also out-of-scope per `handoff/cowork_p3_5_direction_review.md` "Deferred (must not be landed under P3.5)" item 4, and per `handoff/cowork_p2_25_closeout_review.md` "What not to build next" item 2. P3.6 must not weaken that posture.

## Safety Boundary

P3.6 is design-and-templates-only.

The implementation slice approved here must not:

- run live scans, probes, scanner execution, fuzzers, brute force, callbacks, OAST / interactsh / Burp Collaborator infrastructure, exploit tooling, webhook clients, proxy/pivot/transport tooling, or any target-touching automation;
- execute any module `check.py`, any candidate-workflow consumer (`scripts/build_*`, `scripts/review_*`), `scripts/module_runner.py`, `scripts/program_policy_boundary.py`, `scripts/program_policy_check.py`, or `recon.sh`;
- modify `config/scope.txt`, `config/recon.conf`, `recon.sh`, anything under `modules/**`, anything under `scripts/**`, anything under `tests/**`, anything under `templates/**`, anything under `loot/**`, `scans/**`, `reports/**`, `runs/**`, `programs/**`, `.env`, credentials, OAuth, scheduler, billing, deployment, or production-side settings;
- promote any `*/0.1-trial` schema, draft any report prose, add any platform adapter, change any candidate-chain status to `confirmed` / `verified`, alter the runner runtime, add any scanner importer, add any notification surface;
- introduce any new live-target CLI affordance such as `--target`, `--url`, `--host`, `--scope`, `--live`;
- create any new stdin/stdout JSON consumer of `0.1-trial` chain documents;
- centralize `LIVE_TARGET_FLAGS`, `_compact_emit`, `_error_payload`, `_argv_errors`, or any other safety-load-bearing per-consumer helper;
- create or modify any file under `scripts/core/**`;
- introduce any importer/exporter, external-tool integration, or platform SDK call (SARIF, DefectDojo, <bug-bounty-platform>, Bugcrowd, Intigriti, Synack, YesWeHack, webhook, notification, mail, RSS).

The implementation slice approved here may:

- add or replace Markdown templates under `handoff/periodic_reviews/**` (including dated subdirectories) so they reflect the four-reviewer-role structure of `handoff/multi_party_review_decision_policy.md`;
- add a short `handoff/periodic_reviews/README.md` describing the directory's purpose and lineage and stating that no periodic review artifact is machine-parsed;
- append a single entry to `handoff/accepted_changes.md` summarizing the slice;
- optionally add `handoff/cowork_p3_6_direction_review.md` (this file) and any third-party review artifact `handoff/third_party_p3_6_implementation_review.md` after implementation.

This boundary is intentionally narrower than P3.5's because P3.6 deliberately does not extend the chain catalog, the schema surface, or the runtime path; it only formalizes a review-workflow Markdown template that the multi-party review decision policy already governs.

## OSS Recon Gate

**OSS Recon Gate: not applicable for P3.6 as scoped (templates-only).**

`handoff/oss_recon_gate.md` lines 22-34 list the triggering surfaces: "program scope or policy decision contracts; finding, evidence, report, or run manifest schemas; module manifests/profiles/discovery/I/O; runner/executor boundaries; scanner-result importers or adapters; post-scan triage/review workflow; external tool integration or update mechanism." P3.6 as scoped touches none of these. The periodic review template is a workflow-Markdown artifact, not a contract or runtime surface.

However, this review still notes design alignment with relevant OSS reviewer-workflow references for forward-paving, because the deferred reviewer-notes question (provisional P3.7+) *would* require a fresh OSS Recon Gate, and the references below should be the starting point for that future gate.

- **SARIF — `suppressions[]`, `result.kind: review`, `baselineState`.**
  - Useful pattern: SARIF supports a `suppressions[]` array with per-result justification text and a `kind` of `review`/`under-review`, plus a `baselineState` (`new`/`unchanged`/`updated`/`absent`). The closest analog to what a future reviewer-notes artifact would record is a triple `{rule.id, suppression.justification, baselineState}`.
  - Adopt/adapt/ignore: **adapt at the future reviewer-notes slice, not now.** The conceptual triple maps to `{P3.5 prompt.id, reviewer answer, "is this candidate the same as last review's"}`. The shape is helpful as a forward reference.
  - Safety concern: SARIF's `result.kind: pass`/`fail`/`open` is promotion-flavored and must remain hard-rejected (already locked by P3.5 assertion 8). `baselineState` would imply a baseline-diff behavior P3.6 does not need.
  - Contract impact for P3.6: **none.** Periodic review templates are Markdown.
- **DefectDojo notes / lifecycle.**
  - Useful pattern: DefectDojo exposes a per-finding `notes` field that is free-form, timestamped, and authored. A reviewer-notes artifact would benefit from `timestamp`, `reviewer_id`/`reviewer_route`, and the prompt id it responds to.
  - Adopt/adapt/ignore: **adapt at the future reviewer-notes slice, not now.** Avoid DefectDojo lifecycle states (`verified`/`false_p`/`risk_accepted`/`mitigated`/`active`) at the same time — `handoff/cowork_p3_5_direction_review.md` already hard-rejected these.
  - Safety concern: DefectDojo's importer model couples notes to imported findings; we have no importer and must not gain one in P3.6.
  - Contract impact for P3.6: **none.**
- **<bug-bounty-platform> / Bugcrowd triage comments.**
  - Useful pattern: triage reviewers thread comments per submission; each comment is short, often references a structured check (scope, severity, dedupe), and the state of the submission is recorded separately from the comment body.
  - Adopt/adapt/ignore: **ignore at P3.6**; the entire platform vocabulary remains hard-rejected per `handoff/cowork_p3_5_direction_review.md` lines 29-42 and the "Non-Promotional Vocabulary Rules" section.
  - Safety concern: any drift toward `triaged`/`resolved`/`disclosed`/`duplicate-confirmed`/`bounty-awarded` vocabulary must remain blocked. Period. The periodic review template must not carry these words even informally.
  - Contract impact for P3.6: **none.**
- **OWASP checklist evidence notes (ASVS, WSTG).**
  - Useful pattern: a reviewer answers structured items with `met`/`not_met`/`N/A` plus a short rationale. Already mapped onto P3.5's four-posture closed enum (`still_blocked`, `still_needs_manual_review`, `needs_more_evidence`, `defer`).
  - Adopt/adapt/ignore: **already adopted** at the catalog layer (P3.5).
  - Safety concern: keep the closed posture set closed; do not widen even informally in the periodic-review template.
  - Contract impact for P3.6: **none.**
- **Project-internal periodic review artifacts (`handoff/periodic_reviews/2026-05-18/`).**
  - Useful pattern: the 2026-05-18 snapshot already structures a review across long-term goal alignment, workflow review, memory/handoff flow, project structure, safety governance, test quality, roadmap, and constructive recommendations. The `hermes_synthesis.md` artifact adopts a verdict + phase-exit-estimate + suggested next-phase shape.
  - Adopt/adapt/ignore: **adopt** — this is the closest direct match. Extend by binding it to `handoff/multi_party_review_decision_policy.md`'s four reviewer roles and the policy's Final Decision Block.
  - Safety concern: the existing artifact is informational and does not carry a schema or live behavior. Preserve that posture.
  - Contract impact for P3.6: **none** (only Markdown changes).

**Net OSS Recon Gate verdict for P3.6: not applicable** because no contract, schema, or runtime is touched. Documenting the alignment here paves the way for a fresh OSS Recon Gate on the eventual reviewer-notes artifact slice.

## P2.24 Trigger Assessment

Walking the six revisit triggers from `handoff/cowork_p2_25_closeout_review.md` lines 396-414 (also restated in `handoff/cowork_p2_24_direction_review.md` lines 274-279) against the approved P3.6 scope:

1. **Third file-reading consumer joins the chain — NOT TRIGGERED.** P3.6 adds no consumer. The only files added or edited are Markdown templates under `handoff/periodic_reviews/**` plus a single `accepted_changes.md` append. The `handoff/periodic_reviews/README.md` is documentation, not a consumer.
2. **Fifth stdin-only consumer joins the chain — NOT TRIGGERED.** No stdin/stdout JSON consumer is added; no `_compact_emit`, `_error_payload`, `_argv_errors`, or `LIVE_TARGET_FLAGS` declaration is added; the four-consumer count (P2.20–P2.23) is unchanged. This is the trigger that Option 3 *would* fire and is the primary structural reason Option 3 is rejected.
3. **Any `*/0.1-trial` schema promoted to `modules/_schema/...` — NOT TRIGGERED.** No schema is touched. The periodic review templates are Markdown and carry no schema header.
4. **Cross-consumer drift in `_compact_emit` / `_error_payload` / argv rejection — NOT TRIGGERED.** No consumer is edited; no drift can be introduced by Markdown templates.
5. **Operator-approved change to `LIVE_TARGET_FLAGS` — NOT TRIGGERED.** The constant is not touched and the periodic review templates explicitly must not embed the flag spellings (`--target`, `--url`, `--host`, `--scope`, `--live`).
6. **New import path between consumers — NOT TRIGGERED.** No Python module is touched.

**P2.24 helper extraction is NOT triggered by P3.6.** This is structurally important because it confirms the periodic-review-template path is the only one of the five options that *both* operationalizes the multi-party review decision policy *and* avoids the helper-extraction prerequisite.

**Forward note for Hermes**: if any future slice proposes a reviewer-notes consumer (the deferred candidate), Hermes must pre-flag it as a P2.24 trigger-2 scenario and require the helper-extraction direction review and implementation in the same slice (or, if the consumer is rejected at direction-review time, document the rejection).

## Multi-Party Review Fit

`handoff/multi_party_review_decision_policy.md` was adopted 2026-05-19 (today) and currently has **no operational artifact** beyond the policy text. The existing `handoff/periodic_reviews/2026-05-18/review_template.md` predates the policy and does not encode:

- the four reviewer roles (Hermes local-validation, implementation reviewer, safety/security reviewer, architecture/roadmap reviewer);
- the visible-model/runtime tag (policy section "Implementation reviewer" → "reviewer route/tool and visible model/runtime if exposed");
- the Final Decision Block (`PASS / PASS_WITH_CONDITIONS / REQUEST_CHANGES / DEFER / ESCALATE_TO_OPERATOR`);
- Hermes authority level (direct / conditional / escalation-only);
- explicit operator-approval-required field;
- OSS Recon Gate applicability flag;
- the "Reviewer disagreement" handling rubric (blocking vs non-blocking).

P3.6 should land these as Markdown template fields so that the next periodic review (and every milestone-boundary review thereafter) records the multi-party policy's structural outputs without exaggerating evidence. The template fields must require the reviewer to fill in:

- which reviewer roles were consulted (and which were explicitly not applicable);
- the visible model/runtime for each consulted reviewer route (or a stated "not exposed" limitation);
- which validation commands were actually run (with raw outcomes — exit code, test count delta, hermes review PASS/FAIL);
- what was *not* validated and why (so the review does not implicitly claim coverage it does not have);
- which OSS references were consulted (or "OSS Recon Gate: not applicable; reason: ...");
- the final decision block verbatim;
- the explicit operator-approval-required line.

**Should P3.6 prioritize improving `handoff/periodic_reviews/YYYY-MM-DD/` output templates instead of adding reviewer notes to the candidate chain?** Yes, unambiguously. The candidate chain is not where multi-party review output belongs — the candidate chain is a triage workflow whose four consumers each fail closed and emit deterministic `0.1-trial` JSON. Reviewer-of-the-review-workflow output is a governance artifact and belongs in `handoff/periodic_reviews/**`. Conflating the two surfaces would either pull governance vocabulary into the chain (where it would muddy the chain's strict triage-only semantics) or pull chain vocabulary into governance (where it would invite the `0.1-trial` schema temptation in a place it has no business being).

The clearest forward statement: **the candidate workflow chain is the place to record gate decisions; the periodic reviews directory is the place to record multi-party review decisions.** P3.6 should make that boundary explicit in the new README.

## Approved Scope

The implementer is expected to write at most **five files**:

```text
handoff/periodic_reviews/review_template_v0.md         (new — the
                                                        multi-party-policy-
                                                        aware periodic review
                                                        template; v0 marker
                                                        in filename so 2026-
                                                        05-18's older shape
                                                        remains frozen as a
                                                        snapshot)
handoff/periodic_reviews/README.md                     (new — short index
                                                        explaining purpose,
                                                        cadence, template
                                                        lineage, and the
                                                        "no machine parsing"
                                                        rule)
handoff/accepted_changes.md                            (append-only entry
                                                        per `.hermes.md`
                                                        rule)
handoff/claude_code_result.md                          (worker summary stub,
                                                        if the slice routes
                                                        through `hermes
                                                        claude-impl`)
handoff/third_party_p3_6_implementation_review.md      (written after
                                                        implementation by
                                                        independent reviewer;
                                                        not written by the
                                                        implementer)
```

The 2026-05-18 dated subdirectory (`handoff/periodic_reviews/2026-05-18/review_template.md`, `project_snapshot.md`, `hermes_synthesis.md`) **must remain unchanged** as a historical snapshot. The new template lives at `handoff/periodic_reviews/review_template_v0.md` so that the dated artifact is preserved for audit trail and so that future dated subdirectories can copy the template verbatim without disturbing earlier ones.

Detailed shape of `handoff/periodic_reviews/review_template_v0.md`:

- A YAML-style metadata block at the top is **forbidden**. The template is pure Markdown to discourage future drift toward machine parsing. (If a future slice decides periodic reviews should be machine-parseable, that decision needs its own direction review and its own OSS Recon Gate.)
- Sections, in order:
  1. **Review metadata.** Review date, reviewer route/tool, visible model/runtime per reviewer (or "not exposed" limitation), review tier (one of T0-T5), milestone, scope-statement of what is and is not under review.
  2. **Multi-party reviewer roles consulted.** Four labeled subsections (Hermes local validation, Implementation reviewer, Safety/security reviewer, Architecture/roadmap reviewer). Each subsection must either have content or carry the explicit text "Not consulted; reason: ..." (no silent omissions). This pattern mirrors `handoff/multi_party_review_decision_policy.md` "Acceptance Checklist for Hermes" → "required reviewer roles were consulted or explicitly deemed not applicable".
  3. **Validation performed.** Concrete commands and outcomes. Explicitly forbid "all tests passed" without a count; require test-count delta and `hermes review` exit status. Include a "not validated" sub-section for honesty.
  4. **OSS Recon Gate.** One of: "not applicable; reason: ..." / "attached; reference: ..." / "required before implementation; status: ...". Mirrors `handoff/multi_party_review_decision_policy.md` Final Decision Block.
  5. **Long-term goal alignment.** Carried forward from the 2026-05-18 template; keep its prompts about drift risks and correction.
  6. **Workflow / memory / handoff flow.** Carried forward; keep the prompt about what should move from chat to handoff to memory.
  7. **Project structure / system health.** Carried forward; add an explicit "duplication watchlist status" sub-prompt that points readers at `handoff/cowork_p2_24_direction_review.md` lines 178-220.
  8. **Safety governance.** Carried forward; expand to require an explicit "scope / authorization posture unchanged: yes/no" line and a "live-target affordance check (greppable list of `--target`/`--url`/`--host`/`--scope`/`--live` across the working tree)" line.
  9. **Test / validation quality.** Carried forward.
  10. **Roadmap / next phase.** Carried forward; add an explicit "deferred items with re-trigger conditions" sub-prompt so deferred work does not silently rot.
  11. **Disagreement handling.** New section. Per-reviewer-role disagreement is captured as either blocking or non-blocking with the rubric from `handoff/multi_party_review_decision_policy.md` "Disagreement Handling".
  12. **Final Decision Block.** Verbatim use of the block from `handoff/multi_party_review_decision_policy.md` "Final Decision Block" (lines 207-223 of that policy file). The template should reproduce the block as a fenced code block with placeholders, so reviewers fill it in directly.
  13. **Operator-approval line.** Explicit "User approval required: yes/no; reason: ...". This is already in the Final Decision Block but should be repeated as its own line so it cannot be missed.
  14. **Accepted-changes pointer.** Line reserved for the eventual `handoff/accepted_changes.md` entry's date/summary; reviewers fill it in when synthesizing.

The total length should be roughly 2-4 pages of Markdown; smaller is acceptable as long as every required section is present.

Detailed shape of `handoff/periodic_reviews/README.md`:

- One short paragraph stating the directory's purpose: "house periodic and milestone-boundary multi-party review artifacts following `handoff/multi_party_review_decision_policy.md`."
- One paragraph stating cadence is informational and not scheduler-controlled (P3.6 must not touch scheduler/cron).
- One paragraph stating template lineage: the 2026-05-18 subdirectory is preserved as a historical snapshot; `review_template_v0.md` is the current template; future dated subdirectories should copy the current template at the time of writing.
- One paragraph stating the rule: **no periodic review artifact carries a `*/0.1-trial` schema header, none is machine-parsed by any candidate-chain consumer, and none is required to be parseable by tools.** This is the most important sentence in the README and is the primary structural defense against future drift toward turning periodic reviews into a contract.
- One paragraph linking to `handoff/multi_party_review_decision_policy.md`, `handoff/review_tiering_policy.md`, and `handoff/oss_recon_gate.md` as authoritative sources for the template's structure.

Detailed shape of the `handoff/accepted_changes.md` append:

- Date heading: `## 2026-05-19 — P3.6 periodic review template alignment with multi-party decision policy`.
- One sentence on what landed.
- Three explicit declarations, mirroring `handoff/cowork_p3_5_direction_review.md` non-blocking-recommendation 8's pattern: (a) "P3.6 was kept templates-and-docs-only; no new consumer, no new schema, no new fixture root, no chain wiring"; (b) "P2.24 helper extraction was not triggered; the duplication watchlist remains intentional"; (c) "the reviewer-notes artifact remains DEFERRED to a future direction review (provisional P3.7 or later), with explicit re-trigger conditions in `handoff/cowork_p3_6_direction_review.md`".
- Validation results (`hermes review` PASS, no test surface added so no test-count delta).
- Safety boundary line confirming the binding rules from `.hermes.md` were preserved.

## Forbidden Files

The implementer must not touch any of the following under P3.6 cover:

```text
config/scope.txt                                       (operator-only)
config/recon.conf
recon.sh
scripts/**                                             (no script edits at all;
                                                        the periodic review
                                                        templates have no
                                                        runtime path)
scripts/core/**                                        (no extraction; P2.24
                                                        decision is preserved)
modules/_schema/**                                     (no schema bump, no
                                                        field add)
modules/checks/**
modules/profiles/**
templates/**                                           (the P3.5 catalog is
                                                        NOT touched; if a
                                                        future reviewer-notes
                                                        consumer needs a
                                                        sibling artifact,
                                                        that is its own
                                                        direction review)
tests/fixtures/**                                      (no new fixture root)
tests/**
runs/**
loot/**
scans/**
reports/**
programs/**
handoff/periodic_reviews/2026-05-18/**                 (FROZEN — preserve as
                                                        historical snapshot;
                                                        do not edit the
                                                        2026-05-18 template,
                                                        snapshot, or
                                                        synthesis files)
handoff/multi_party_review_decision_policy.md          (POLICY; the slice
                                                        implements it, not
                                                        edits it)
handoff/review_tiering_policy.md                       (POLICY)
handoff/oss_recon_gate.md                              (POLICY)
.hermes.md                                             (no changes to the
                                                        binding context)
.gitignore                                             (no weakening)
.env, credentials, OAuth, scheduler, deployment, billing, production settings
```

Any deviation is a scope escalation and must route back to Hermes for a fresh direction review.

The implementer must specifically not:

- "fix" any 2026-05-18 file ("while we're here" edits of the snapshot are forbidden);
- create a YAML/JSON/TOML metadata header on the new template (Markdown only);
- add a script that renders the template (rendering surface was deferred by P3.5 non-blocking recommendation 2 and is not P3.6 scope);
- add a fixture or test that asserts the template's shape (it is Markdown for humans, not a contract);
- add any link from a chain consumer to the new template;
- create or modify any file under `scripts/**` even for a "small README update" — `scripts/README.md` is not part of P3.6 because P3.6 is not a chain-consumer slice;
- import any new vocabulary into the template that is forbidden by `handoff/cowork_p3_5_direction_review.md` "Non-Promotional Vocabulary Rules" (`confirmed`, `verified`, `valid` as state, `ready_for_submission`, `accepted`, `false_positive`, `risk_accepted`, `mitigated`, `triaged`, `resolved`, `disclosed`, `submitted`, `published`, `reportable`, `weaponizable`, platform names, etc.). Periodic review templates may still use the words `verification` and `validation` as nouns referring to chain steps (the P3.5 carve-out applies).

## Required Tests / Safety Assertions

P3.6 is templates-only and therefore has no automated test surface to add. The required validation is the standard offline gate:

1. **`hermes review` PASS.** JSON-validity check trivially passes (no JSON added). Python compile trivially passes (no Python added). `bash -n` trivially passes (no shell touched). `.agent.lock` released after the run.
2. **Markdown lints clean (informational).** The repo does not enforce a Markdown linter today; if a future slice adds one, the new template should pass. No new lint dependency is added under P3.6.
3. **Greppable safety check.** A spot-grep of the new template and README for the forbidden vocabulary list above must return zero hits. The implementer should perform this grep before requesting review.
4. **No 2026-05-18 files modified.** `git status` and `git diff` show no edits to `handoff/periodic_reviews/2026-05-18/**`.
5. **No file outside `handoff/**` modified.** `git status` shows no edits to `scripts/**`, `modules/**`, `templates/**`, `config/**`, `tests/**`, `runs/**`, `loot/**`, `scans/**`, `reports/**`, `programs/**`, or any production setting.
6. **No new live-target affordance.** A grep across the new template and README for `--target`, `--url`, `--host`, `--scope`, `--live`, `http://`, `https://`, `oast.`, `interactsh.`, `burpcollaborator.`, `ngrok.`, `webhook.`, `requestbin.` returns zero hits.
7. **Existing chain tests still green.** `python -m unittest discover -s scripts -p 'test_*.py'` exits 0 with the same count and skip set as before P3.6. Test count does not change (no test added or removed).
8. **`accepted_changes.md` is append-only.** The diff for `handoff/accepted_changes.md` is purely additive at the end of file; no prior content is altered.

Skip:

- Any test that asserts the new template's section headings or wording (locks too much; review wording at PR time instead);
- Any new Markdown linter or new test dependency;
- Any execution of a periodic review template against a hypothetical reviewer route (templates are documents, not runners).

## Out-of-Scope / Deferred Items

**Carried forward verbatim from `handoff/cowork_p3_5_direction_review.md`** (with the P3.6-specific deferrals layered on top):

1. Reviewer-notes artifact contract — **DEFERRED to a future direction review (provisional P3.7 or later).** Re-trigger conditions:
   - an operator or Claude/Cowork reviewer explicitly asks "where do I record my answers" during a real bug-bounty triage session, and ad-hoc note capture in chat or scratch files proves insufficient;
   - or a periodic review uses the new template (per P3.6) and the reviewer concludes the template's free-form answer fields are insufficient to capture reviewer answers to P3.5 catalog prompts;
   - or two consecutive periodic reviews carry "deferred: reviewer-notes artifact still useful" without operator pushback, indicating the artifact's absence is creating real friction.
   When any of these fires, the next direction review must answer: (a) is the artifact justified now? (b) if yes, does it land as fixture-only (no consumer; shape tests only) or as a consumer-backed artifact that fires P2.24 trigger 2 (fifth stdin consumer) and runs the helper-extraction review in the same slice?
2. Rendering surface (Markdown / HTML / web UI / IDE integration of the P3.5 catalog) — deferred to a separate slice; if attempted, keep Markdown-only and isolated in `docs/` or `scripts/render_reviewer_prompts.py` with no chain integration.
3. Chain wiring of the P3.5 catalog (`scripts/build_*` consuming it; `module_runner.py` linking it; the candidate workflow fixture builder emitting prompts) — deferred.
4. Any change to `modules/_schema/**`, schema promotion, validator script, or `tests/fixtures/**` directory for the catalog — deferred.
5. Drafting fields (`title`, `summary`, `impact_narrative`, `steps_to_reproduce`, `remediation_prose`, `submission_text`) — explicitly deferred and explicitly forbidden in any P3.6 artifact.
6. Platform fields and platform-coupled identifiers — explicitly deferred and forbidden.
7. Importer/exporter / external-tool integration (SARIF, DefectDojo, <bug-bounty-platform>, Bugcrowd, Intigriti, Synack, YesWeHack, webhook, notification, mail, RSS) — explicitly deferred and forbidden.
8. Live-target affordance — explicitly forbidden everywhere in this slice.

**P3.6-specific deferrals:**

9. **Machine-parseable periodic review artifacts.** P3.6 makes them Markdown specifically to defer this. If a future slice wants periodic reviews to be machine-readable (for example, to aggregate verdicts across milestones), that is its own T3 direction review with its own OSS Recon Gate.
10. **Automated periodic-review cadence (scheduler/cron).** P3.6 is informational about cadence. Any actual scheduling is T5 (production-side, scheduler) and must route through operator approval.
11. **Dated subdirectory automation** (a script that creates `handoff/periodic_reviews/YYYY-MM-DD/` with the template pre-populated). Deferred; manual creation is fine for now.
12. **A periodic-review-template renderer or printer.** Deferred. The template is a Markdown document; reviewers read it as text.
13. **A periodic-review index that aggregates verdicts across dated subdirectories.** Deferred. The README is a static index, not a generated rollup.

## P2.24 Trigger Assessment (Final Statement)

P2.24 helper extraction is **NOT TRIGGERED** by the approved P3.6 scope. The duplication watchlist (`LIVE_TARGET_FLAGS`, `_compact_emit`, `_error_payload`, `_argv_errors`, per-stage error dataclasses across `scripts/review_candidate_packet_gaps.py`, `scripts/build_candidate_verification_plan.py`, `scripts/build_report_readiness_gate.py`, `scripts/build_candidate_workflow_fixture.py`) remains intentionally per-script for the safety reasons given in `handoff/cowork_p2_24_direction_review.md` lines 31-66. The slice explicitly records this in `accepted_changes.md` so a future reader does not infer that P3.6's lack of action on duplication implies forgetting; the opposite is true — P3.6 was scoped specifically to avoid the trigger.

A future slice that proposes a reviewer-notes consumer (the deferred candidate) **will** fire P2.24 trigger 2 (fifth stdin consumer) and must run the helper-extraction direction review (`handoff/cowork_p2_24_direction_review.md` lines 178-231) in the same slice or as an immediate prerequisite. Hermes should pre-flag this on any P3.7 / P3.8 proposal that mentions reviewer notes, reviewer answers, or reviewer-state capture.

## Reviewer Route / Tool and Visible Model / Runtime

- **Reviewer route/tool:** Claude Code MAX/OAuth via `hermes claude-impl` (worker invocation per `.hermes.md` "Worker invocation reference" table). The implementation slice that follows is expected to route through the same envelope so a Claude Code Impl run JSON is emitted under `handoff/claude_code_impl_run_<timestamp>.json`.
- **Visible model/runtime model:** Claude Opus 4.7 (per the session's own self-reported model id `claude-opus-4-7`). Exact runner identifier inside Anthropic's hosting is not exposed by the tool surface; this is the strongest model identification available without crossing a tool-output boundary.
- **Independent reviewer route/tool for the implementation review that follows:** any of (a) a fresh Claude Code MAX/OAuth session in a separate context (preferred for tier consistency), (b) Codex secondary review for narrow safety-vocabulary spot-checks, or (c) Cowork direct in the desktop app. The independent reviewer must write `handoff/third_party_p3_6_implementation_review.md` and must spot-check the forbidden-vocabulary grep (assertion 6) and the no-2026-05-18-edits constraint (assertion 4).

## Blocking Issues

**None on the approved scope.**

One pre-emptive lock to call out, similar to the one in `handoff/cowork_p3_5_direction_review.md`: if the implementer reads this review and concludes "the periodic review template is just a Markdown file, so I can also land a tiny reviewer-notes JSON skeleton in `handoff/periodic_reviews/` while I'm there", that conclusion is **wrong** and the impulse must be rejected at intake. The deferral of the reviewer-notes artifact is explicit and load-bearing. Landing both in one slice converts a templates-only governance slice into a contract slice (artifact = contract), which (a) crosses the prompt's stated "do not introduce any reviewer-notes artifact" line; (b) creates a fixture-only contract that no consumer reads (and thus cannot be tested for correctness beyond shape); or (c) demands a fifth stdin consumer, firing P2.24 trigger 2.

A second pre-emptive lock: the implementer must not "fix" the 2026-05-18 dated artifacts to match the new template. Those files are a historical snapshot of the older review shape and are preserved deliberately for audit lineage; editing them retroactively would erase the lineage signal that future readers depend on. If the new template needs to reference the 2026-05-18 artifacts, the reference belongs in `handoff/periodic_reviews/README.md`, not in edits to the 2026-05-18 files themselves.

## Non-Blocking Improvements

1. **Pre-populate the next dated subdirectory.** If Hermes prefers, the implementer may create an empty `handoff/periodic_reviews/<NEXT_DATE>/` subdirectory with the new template copied in as `review_template.md`, ready for the next scheduled review. This is non-blocking; manual creation at the time of the next review is equally acceptable. If the implementer chooses to pre-populate, the date should be a real cadence-aligned date agreed with Hermes (not a placeholder string).
2. **Add a short "what counts as a periodic review trigger" paragraph to the README.** Suggested triggers: (a) milestone closure (e.g., end-of-phase reviews like the 2026-05-18 P2.20 baseline); (b) operator request; (c) accumulation of three or more deferred items in `accepted_changes.md` without re-trigger; (d) any safety-boundary near-miss or noticed drift. This is a non-binding cadence signal, not a scheduler.
3. **Add a "reviewer-notes artifact watchlist" pointer in the README.** The README should briefly note that the reviewer-notes artifact is currently deferred (provisional P3.7 or later) and link to this P3.6 direction review for the re-trigger conditions. This forecloses a "we never decided" reading by a future reviewer.
4. **Mention `handoff/cowork_p2_24_direction_review.md`'s duplication watchlist by name in the new template's "Project structure / system health" section.** Periodic reviews are the natural place to check whether any of the six P2.24 triggers have started firing without anyone noticing.
5. **Explicitly require the visible-model/runtime tag in every reviewer-role subsection of the template.** This catches future cases where a reviewer-role is filled in without the route/tool/model line, mirroring `handoff/multi_party_review_decision_policy.md` "Prompt Add-On for Multi-Party Reviews" item 5.
6. **Add a "what was NOT validated and why" sub-prompt to the validation section.** This is a small but important honesty discipline that prevents reviews from implicitly claiming coverage they did not have (a failure mode that periodic reviews are particularly prone to since they often span many surfaces).
7. **Run `hermes review` and the full unittest suite before P3.6 implementation begins** to baseline the test count and `hermes review` exit, so any divergence during P3.6 is attributable to the slice. Standing recommendation from `handoff/cowork_p3_1_direction_review.md` non-blocking 7, restated in `handoff/cowork_p3_5_direction_review.md` non-blocking 7.
8. **At implementation acceptance, ensure the `accepted_changes.md` entry records the three explicit declarations** listed under "Approved Scope" → "Detailed shape of the `handoff/accepted_changes.md` append" above. These three sentences let any future reader confirm scope discipline without re-reading the direction review.
9. **Independent implementation review is required at T3** per `handoff/review_tiering_policy.md` and `handoff/multi_party_review_decision_policy.md`. The independent reviewer must read the landed templates, run `hermes review`, confirm no forbidden file has been touched, perform the forbidden-vocabulary grep, and write `handoff/third_party_p3_6_implementation_review.md` with verdict PASS / PASS_WITH_RECOMMENDATIONS / ROUTE_BACK / BLOCK.

## Codex / Claude Implementation Scope (Forward Brief)

If Hermes routes the implementation slice to `hermes claude-impl` (default for offline coding slices), the implementation task should:

- Add `handoff/periodic_reviews/review_template_v0.md` with the section structure in "Approved Scope" above.
- Add `handoff/periodic_reviews/README.md` with the paragraphs described above.
- Append the `2026-05-19 — P3.6 ...` entry to `handoff/accepted_changes.md` per the shape above.
- Write `handoff/claude_code_result.md` summarizing the slice and recording the `hermes review` outcome.
- **Not** modify any file under the Forbidden Files list.
- **Not** add any test file, fixture, schema, script, or runtime path.

If Hermes routes the implementation slice to Codex (fallback), the same boundaries apply. Codex must not "extract" anything from the templates into shared helpers; the periodic review templates are documents, not modules.

## Final Recommendation for Next Implementation Slice

Implement P3.6 as scoped here: periodic-review-template alignment with `handoff/multi_party_review_decision_policy.md`, no chain consumer added, no schema added, no fixture root added, no `scripts/**` edited, 2026-05-18 subdirectory preserved frozen, three explicit declarations recorded in `accepted_changes.md`. The reviewer-notes artifact remains DEFERRED with the re-trigger conditions documented above.

The next direction review after P3.6 (provisional P3.7) should re-examine the reviewer-notes question if any of the three re-trigger conditions has fired. If none has fired, P3.7 should pick from the deferred items in `handoff/cowork_p3_5_direction_review.md` "Deferred" list (rendering surface — but only if external need surfaces; chain wiring — but only after reviewer-notes is settled; second Level 1 module fixture — see `handoff/cowork_p2_24_direction_review.md` "P2.25 Closeout Questions" item 2 second sub-bullet) or from Phase 1 program-policy work (`scripts/program_policy_boundary.py` Task C, the dry-run stage integration noted in the 2026-05-18 P1-4 Task B accepted-changes entry).

## Safety Boundary Confirmation

This review is design-only. The reviewer did not:

- run live scans, probes, scanners, fuzzers, exploit tooling, callbacks, OAST / interactsh / Burp Collaborator / webhook / requestbin infrastructure, proxy/pivot/transport tooling, or any target-touching automation;
- execute any module `check.py`, any candidate-workflow consumer (`scripts/build_*` / `scripts/review_*`), `scripts/module_runner.py`, `scripts/program_policy_boundary.py`, `scripts/program_policy_check.py`, or `recon.sh`;
- import, vendor, or invoke third-party scanning code, platform SDKs, or <bug-bounty-platform>/Bugcrowd/DefectDojo/Intigriti/Synack/YesWeHack APIs;
- modify `config/scope.txt`, `config/recon.conf`, `recon.sh`, anything under `modules/**`, anything under `scripts/**`, anything under `tests/**`, anything under `templates/**`, anything under `loot/**`, `scans/**`, `reports/**`, `runs/**`, `programs/**`, `.env`, credentials, OAuth, scheduler, billing, deployment, or production-side settings;
- promote any `*/0.1-trial` schema, draft any report prose, add any platform adapter, change any candidate-chain status to `confirmed`/`verified`, alter the runner runtime, add any scanner importer, add any notification surface;
- authorize any active scan, target interaction, module execution, scanner import, report drafting/submission, schema promotion, or platform adapter under this review.

Files this review reads (read-only):
`handoff/cowork_p3_6_direction_prompt.md`,
`handoff/cowork_p3_5_direction_review.md`,
`handoff/third_party_p3_5_implementation_review.md`,
`handoff/cowork_p2_24_direction_review.md`,
`handoff/review_tiering_policy.md`,
`handoff/multi_party_review_decision_policy.md`,
`handoff/oss_recon_gate.md`,
`handoff/periodic_reviews/2026-05-18/review_template.md`,
`handoff/periodic_reviews/2026-05-18/project_snapshot.md`,
`handoff/periodic_reviews/2026-05-18/hermes_synthesis.md`,
`handoff/accepted_changes.md` (tail),
`handoff/claude_code_task.md`,
`.hermes.md` (loaded as project context),
`templates/report_readiness_reviewer_prompts.json` (header only),
directory listings for `handoff/periodic_reviews/`, `handoff/`, `templates/`.

Files this review writes:
`handoff/cowork_p3_6_direction_review.md` (this file, only).

Binding rules from `.hermes.md` preserved: authorization-first, no exfiltration, no destructive defaults, no silent overwrites, lock discipline, secrets out of git, report integrity (`accepted_changes.md` treated as append-only and was not touched by this review), no production-side changes. None of these were touched.

## Direction-Review Output Block

```text
Review tier: T3 (direction review); implementation slice T1 (Markdown templates)
Milestone: Phase 3, slice 6 — review-workflow consolidation (periodic-review-
  template alignment with multi-party review decision policy)
Decision: APPROVE_WITH_CHANGES
Safety boundary: design-and-templates-only; no live scans / probes / scanner
  execution / fuzz / brute force / callbacks / OAST / proxy / pivot /
  transport / target-touching automation; no chain-consumer creation; no
  schema promotion; no script edits; no scheduler / deployment / billing /
  credential / production change; `config/scope.txt` unchanged; the four
  candidate-chain consumers (P2.20-P2.23) unchanged; the P3.5 catalog
  unchanged; the 2026-05-18 periodic review snapshot preserved frozen
OSS Recon Gate: not applicable — periodic-review templates are Markdown and
  touch no contract, schema, runtime, importer, or external-tool boundary.
  Design alignment with SARIF suppressions, DefectDojo notes, <bug-bounty-platform> /
  Bugcrowd triage comments, OWASP ASVS / WSTG, and the existing 2026-05-18
  template is noted for forward-paving; a fresh OSS Recon Gate will be
  required at the eventual reviewer-notes-artifact direction review.
Blocking issues: none on the approved scope
Non-blocking improvements: 9, see "Non-Blocking Improvements" section
Codex/Claude implementation scope: add
  `handoff/periodic_reviews/review_template_v0.md` (new),
  `handoff/periodic_reviews/README.md` (new), append entry to
  `handoff/accepted_changes.md`, write `handoff/claude_code_result.md`. Do
  not modify any file under the "Forbidden Files" list. No test, fixture,
  schema, script, or runtime path is added.
Required tests/safety assertions: `hermes review` PASS; no Markdown linter
  added; greppable safety check zero hits for forbidden vocabulary; no
  2026-05-18 edits; no file outside `handoff/**` modified; no new live-
  target affordance; existing `python -m unittest discover -s scripts -p
  'test_*.py'` count unchanged; `handoff/accepted_changes.md` append-only.
Out-of-scope/deferred items: reviewer-notes artifact (contract, fixture,
  consumer, schema) — DEFERRED with explicit re-trigger conditions; renderer
  surfaces; chain wiring of the P3.5 catalog; `modules/_schema/**` changes;
  schema promotion; drafting / platform / importer / notification surfaces;
  live-target affordances; machine-parseable periodic reviews; automated
  periodic-review cadence; dated-subdirectory automation
P2.24 trigger assessment: NOT TRIGGERED. None of the six revisit triggers
  fires under the approved P3.6 scope. A future reviewer-notes consumer
  WOULD fire trigger 2 (fifth stdin consumer) and would require the P2.24
  helper-extraction direction review in the same slice.
Reviewer route/tool and visible model/runtime: Claude Code MAX/OAuth via
  `hermes claude-impl`; visible model `claude-opus-4-7` (Claude Opus 4.7).
  Exact runner identifier inside Anthropic's hosting is not exposed by the
  tool surface; this limitation is stated explicitly per
  `handoff/multi_party_review_decision_policy.md` "Prompt Add-On for Multi-
  Party Reviews" item 5.
```

## Multi-Party Review Decision Block

```text
Decision: PASS_WITH_CONDITIONS
Tier: T3 (direction review); implementation slice T1
Milestone: Phase 3, slice 6 — review-workflow consolidation (periodic-review-
  template alignment with multi-party review decision policy)
Hermes authority: conditional. Hermes may accept the implementation slice
  after running `hermes review`, confirming the forbidden-vocabulary grep
  returns zero hits, confirming no file outside `handoff/**` was touched,
  confirming the 2026-05-18 subdirectory is unchanged, and obtaining the
  required T3 independent implementation review per
  `handoff/review_tiering_policy.md` and
  `handoff/multi_party_review_decision_policy.md`. Authority is conditional
  rather than direct because the slice operationalizes a newly adopted
  policy (`handoff/multi_party_review_decision_policy.md`, adopted 2026-05-
  19) and the policy's first operational artifact deserves a second
  reviewer pass; it is not escalation-only because no activation, target-
  touching, scheduler, credential, or production-side change is involved.
Reviewers consulted:
  - Claude Code MAX/OAuth direction review via `hermes claude-impl`
    (this artifact); visible model/runtime: Claude Opus 4.7 (`claude-opus-
    4-7`); exact backing API/runtime version is not exposed by the tool
    surface.
  - Implementation reviewer: will be consulted at implementation-review
    time; route/tool TBD by Hermes (Claude Code MAX/OAuth in a fresh
    session preferred for tier consistency; Codex secondary review
    acceptable for narrow safety-vocabulary spot-checks).
  - Safety/security reviewer: combined with the implementation reviewer
    role for this slice because the slice's safety surface is small
    (Markdown documents, no runtime). The implementation reviewer must
    perform the forbidden-vocabulary grep and the no-2026-05-18-edits
    constraint check explicitly.
  - Architecture/roadmap reviewer: this direction review serves the
    architecture/roadmap role for the P3.6 slice; the implementation
    review will revisit architecture fit only if the implementer departed
    from the approved scope.
Validation performed:
  - Read of `.hermes.md` project context, `handoff/cowork_p3_6_direction_
    prompt.md`, `handoff/cowork_p3_5_direction_review.md`,
    `handoff/third_party_p3_5_implementation_review.md`,
    `handoff/cowork_p2_24_direction_review.md`,
    `handoff/review_tiering_policy.md`,
    `handoff/multi_party_review_decision_policy.md`,
    `handoff/oss_recon_gate.md`,
    `handoff/periodic_reviews/2026-05-18/*.md`,
    `handoff/accepted_changes.md` tail,
    `templates/report_readiness_reviewer_prompts.json` header.
  - Confirmed P2.24 trigger assessment by re-walking the six triggers
    against the approved scope.
  - Confirmed OSS Recon Gate non-applicability against the gate's "When
    Required" list (`handoff/oss_recon_gate.md` lines 22-34).
  - Confirmed the Forbidden Files list excludes every file under
    `scripts/**`, `modules/**`, `templates/**`, `config/**`, `tests/**`,
    `runs/**`, `loot/**`, `scans/**`, `reports/**`, `programs/**`, and the
    2026-05-18 subdirectory.
  - Did NOT execute `hermes review`, `python -m unittest discover -s
    scripts`, any chain consumer, any module check, any scanner, or any
    target-touching automation (this is a design-only review).
Blocking findings: none on the approved scope.
Non-blocking recommendations: 9 (enumerated in "Non-Blocking Improvements"
  section).
Safety boundary: design-and-templates-only; `config/scope.txt` unchanged;
  no chain-consumer creation; no schema promotion; no script edit; no
  scheduler / deployment / billing / credential / production change; the
  four candidate-chain consumers (P2.20-P2.23) and the P3.5 catalog
  unchanged; the 2026-05-18 periodic review snapshot preserved frozen;
  no new live-target affordance; no importer / exporter / external-tool
  integration; reviewer-notes artifact deferred with explicit re-trigger
  conditions.
OSS Recon Gate: not applicable. Periodic-review templates are Markdown and
  touch no contract, schema, runtime, importer, or external-tool boundary.
  Forward references (SARIF suppressions, DefectDojo notes, <bug-bounty-platform> /
  Bugcrowd triage comments, OWASP ASVS / WSTG, the existing 2026-05-18
  template) are noted in the OSS Recon Gate section for the eventual
  reviewer-notes-artifact direction review, which will require a fresh
  gate.
User approval required: no for the templates-only implementation slice
  (no target-touching, no scheduler/deployment/billing/credential change,
  no `config/scope.txt` edit, no live-mode activation, no schema promotion,
  no external-side-effect activation). Operator approval would become
  required if (a) any deferred item is pulled into scope, (b) any file
  outside `handoff/**` is touched, (c) any scheduler / cron / cadence
  automation is added, or (d) the reviewer-notes artifact is landed
  without a fresh direction review.
Accepted changes updated: not applicable for this direction review
  (the review file is the artifact). The implementer is required to
  append a single entry to `handoff/accepted_changes.md` at
  implementation-acceptance time per `.hermes.md` rule 4 (no silent
  overwrites; append-only). The entry shape is specified in "Approved
  Scope" → "Detailed shape of the `handoff/accepted_changes.md` append".
Next action: route this direction review to Hermes for assignment of the
  implementation slice to `hermes claude-impl` (preferred) or Codex
  (fallback), with the Forbidden Files list and Required Tests / Safety
  Assertions copied into the task brief. After implementation, an
  independent implementation reviewer must produce
  `handoff/third_party_p3_6_implementation_review.md` with verdict
  PASS / PASS_WITH_RECOMMENDATIONS / ROUTE_BACK / BLOCK; Hermes then
  synthesizes per `handoff/multi_party_review_decision_policy.md`
  "Acceptance Checklist for Hermes" and updates `handoff/accepted_
  changes.md`.
```
