> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.1 Direction Review

Date: 2026-05-19
Reviewer: Claude Code MAX/OAuth via `hermes claude-impl` (design-only direction review)
Review tier: T3 direction review + OSS Recon Gate, design-only
Milestone: Phase 3 start, first slice (curated near-real offline fixtures)
Source prompt: `handoff/cowork_p3_1_direction_prompt.md`
Predecessor: `handoff/cowork_p2_25_closeout_review.md` (verdict `CLOSE_PHASE_2`)

## Verdict

PROCEED_WITH_FIXTURE_ONLY_P3_1

## Rationale

P2.25 already authorized P3.1 in principle, with a worker-ready task framing and
explicit boundary locks. The job of this direction review is therefore not to
re-litigate whether P3.1 should happen, but to (a) confirm that no Phase 3
boundary has shifted since P2.25, (b) tighten the implementation boundary to the
smallest useful first slice, (c) attach a focused OSS Recon Gate, and (d) name
acceptance gates that the implementer can apply mechanically without inviting
scope creep.

The P2.19 -> P2.23 chain is the right surface to stress with curated fixtures,
for four reasons:

1. **Real learning, zero new surface.** Every other Phase 3 candidate
   (second module, reviewer prompts, evidence-locator, redaction gate, report
   drafting) requires either a new contract or a new behavior. Curated fixtures
   require neither. They exercise the existing contracts and consumers at their
   current `0.1-trial` version and let the chain itself surface what is missing.
   That is the cheapest possible directional signal for Phase 3.

2. **The chain's vocabulary coverage is currently asserted only on synthetic
   minimal inputs.** Existing `tests/fixtures/candidate_review_packet/`
   subdirectories (`empty`, `forbidden_status`, `info_severity`,
   `invalid_finding`, `low_confidence`, `with_evidence`) prove envelope and
   error paths. They do not stress the per-stage state machine across a single
   shaped review packet that contains a mix of cases. P3.1 will exercise that
   for the first time.

3. **No safety boundary is crossed.** Adding committed, synthetic, redacted
   `finding/1.0` documents under `tests/fixtures/...` does not change any
   contract, does not touch `LIVE_TARGET_FLAGS`, does not import scanner output,
   does not modify any consumer's behavior, and does not promote any schema.
   The implementation boundary is materially smaller than P2.23 was.

4. **The P2.24 deferral remains correct under this slice.** P3.1 does not add
   a third file-reading consumer, does not add a fifth stdin consumer, does not
   promote any schema, and does not propose any `LIVE_TARGET_FLAGS` change. None
   of the P2.25 P2.24 revisit triggers fire.

The slice should be **fixture-only with test extensions**, not "fixture + minor
implementation tweak". Any change to `scripts/build_*` consumer behavior is an
out-of-scope escalation and should be lifted into a separate slice with its own
direction review. See "Implementation Boundary" below.

## Approved Fixture Scope

### Count and shape

- **Target count: 6 curated cases.** P2.25 sized P3.1 at 4-8; six is the
  narrowest count that can simultaneously cover all required vocabulary states
  and a representative spread of stress conditions without padding. Fewer than
  five would force at least one case to multitask; more than seven would push
  this slice into "second fixture-quality slice" territory and dilute the
  P3.1 / P3.2 boundary.
- **Cases live under** `tests/fixtures/candidate_review_packet/p3_1_curated_<case_slug>/expected_findings.json`,
  one expected-findings file per case directory. Reuse the existing P2.19
  allowlist pattern; do not introduce a new fixture root, a new prefix
  constant, or a new validator entry point.
- **One findings document per case directory.** Each `expected_findings.json`
  may contain one or more `finding/1.0` entries if the case is a chained or
  duplicate-pair scenario. Single-finding cases stay single-finding; do not
  split a chained-precondition case across two directories.
- **Slug convention:** `p3_1_curated_<short_underscored_descriptor>`. Lowercase,
  ASCII, no dashes, no leading/trailing underscores. The `p3_1_curated_`
  namespace prefix is required so future curated rounds (`p3_2_curated_...`,
  etc.) cannot collide and so review tooling can grep one boundary.

### Required cases (six)

Each case description below states (a) what the case is trying to expose, (b)
which stage in the chain should classify it, and (c) the expected terminal
state at the gate. The implementer should choose realistic but obviously
synthetic content (`.example.test` targets, redacted-by-construction evidence,
fabricated `policy_decision_sha256` placeholders). No real CVE IDs, no real
vendor names, no real bounty programs, no real disclosed URLs.

1. **`p3_1_curated_partial_evidence`** -- a single candidate with an evidence
   array that has a redacted `http_exchange` but is missing canonical request
   metadata that a reviewer would normally want. Expected: P2.20 emits gap
   codes, P2.21 plan_state `blocked`, P2.22 gate_state `blocked`.

2. **`p3_1_curated_ambiguous_scope_text`** -- a candidate whose `target` is an
   in-scope domain (per the synthetic fixture's own narrative; this must NOT
   touch `config/scope.txt` or invoke any scope runtime), but whose
   `verification_guidance` text describes behavior on an out-of-scope subpath.
   Expected: P2.20 emits `reviewer_decision_required` because text-level
   ambiguity is exactly the case the report-readiness rubric leaves to a human.
   Plan_state `needs_manual_review`, gate_state `needs_manual_review`.
   The case must not invent or extend any scope contract; ambiguity lives
   purely in free-form text fields the chain already permits.

3. **`p3_1_curated_chained_precondition`** -- two `finding/1.0` entries in one
   file where finding B's exploitability depends on finding A (expressed only
   in human-readable `verification_guidance` / `remediation` text; no new
   contract field). Expected: both findings land at `needs_manual_review` at
   the gate because neither carries unambiguous, self-sufficient evidence.
   The case documents (in test comments only) that the chain currently cannot
   model the dependency; that observation is a Phase 3 follow-up candidate,
   not a P3.1 blocker.

4. **`p3_1_curated_low_signal_informational`** -- one candidate with
   `severity_hint: informational`, redacted evidence that proves the
   observation but no exploitability narrative. Expected: P2.20
   review_state `not_ready` (this is the canonical `not_ready` exemplar for
   the chain), so the per-finding `not_ready` count in the gap report's
   summary is nonzero. Because P2.21 only forwards `not_ready` and
   `reviewer_decision_required`, this case maps to plan_state `blocked` and
   gate_state `blocked` in later stages; the `not_ready` label itself is
   visible only in the gap-report stage of the workflow fixture bundle.
   The implementer should assert this exact behavior in tests rather than
   expecting `not_ready` to survive to the gate.

5. **`p3_1_curated_duplicate_pair`** -- two near-duplicate candidates from
   notional different sources (different `source.module_id`, near-identical
   `summary` / `target`, possibly identical evidence sha256). Expected: chain
   does not deduplicate today; both surface independently and both land at
   `needs_manual_review`. The case documents that dedupe is a future
   directional question (DefectDojo-shaped) but is explicitly **not** in
   scope for P3.1. Tests should assert both candidates survive as distinct
   entries with stable per-finding ordering.

6. **`p3_1_curated_non_finding_control`** -- one candidate-shaped entry whose
   evidence proves benign behavior (e.g., headers present, expected response
   code). Expected: P2.20 review_state `not_ready` and zero gap codes that
   warrant escalation; plan_state `blocked` at P2.21 (because P2.21 treats
   `not_ready` as `blocked`). This case is the explicit control: it
   demonstrates that the chain refuses to promote a non-finding even when the
   evidence is "clean".

A seventh "conflicting source records" case from the prompt's candidate list
is intentionally **deferred** out of P3.1. Conflict resolution is a non-trivial
gap-stage decision that does not have a stable answer in the current chain;
forcing the chain to render an opinion on it would either require behavior
changes (out of P3.1 scope) or yield a low-confidence assertion that locks in
an arbitrary outcome. Park it as a candidate for P3.4+ after reviewer prompts
exist. The seventh slot also gives the implementer room to land six cases
without one slipping into a marginal edge case.

### Cross-case requirements

- **Vocabulary coverage.** Across the six cases, the workflow fixture bundle
  must emit each of `blocked`, `needs_manual_review`, and `not_ready` at
  least once in its respective stage (`not_ready` at the gap-report stage;
  `blocked` and `needs_manual_review` at both plan and gate stages). This is
  the P2.25 acceptance criterion read precisely: the vocabulary lives across
  stages, not all on one stage.
- **`reviewer_decision_required` should also appear** at least once in the
  gap-report stage (from case 2). It is part of the non-promotional
  vocabulary and absent from P2.25's three-state list only because it maps
  forward to `needs_manual_review`; including it explicitly proves the
  mapping is exercised.
- **Determinism.** Re-running `build_candidate_workflow_fixture.py` over the
  same fixtures must produce byte-identical stdout across reruns. Tests must
  assert this by capturing one canonical bundle and asserting equality.
- **Provable synthetic origin.** Every fixture must visibly use
  `.example.test` / `.invalid` / `.test` domains, fabricated module IDs
  prefixed with `p3_1_curated.`, and `policy_decision_sha256` placeholder
  hashes (e.g., 64-character constant hex strings clearly not derived from
  real artifacts). Reviewer should be able to confirm fakeness by reading the
  file alone.
- **Validator clean.** Every fixture passes
  `scripts.validate_finding_evidence.validate_data` without warnings under
  the existing `finding/1.0` schema. No fixture may rely on the validator
  relaxing or extending.

### Out of scope for P3.1

The following are explicitly **not** part of P3.1 and any implementation that
introduces them should be rejected at implementation review:

- Any change to `modules/_schema/**`.
- Any behavior change in `scripts/build_candidate_review_packet.py`,
  `scripts/review_candidate_packet_gaps.py`,
  `scripts/build_candidate_verification_plan.py`,
  `scripts/build_report_readiness_gate.py`, or
  `scripts/build_candidate_workflow_fixture.py`.
- New live-target flag, new "ignore_live_flags" parameter, new
  `LIVE_TARGET_FLAGS` member, or any relaxation of argument rejection.
- New fixture root, new allowlist prefix, new validator entry point.
- New consumer script, new helper module, or extraction of the deferred
  `scripts/core/offline_consumer.py` helper.
- Any redaction or evidence-locator behavior (these are P3.3+ candidates).
- Any reviewer-notes scaffold, reviewer-prompt JSON, or UX surface.
- Any platform adapter, importer, exporter, or external-source ingest.
- Any change to `recon.sh`, `safe_target`, `config/scope.txt`,
  `config/recon.conf`, or the program policy boundary.
- Any change to `loot/`, `.env`, credentials, OAuth, scheduler, deployment,
  billing, or production settings.

## OSS Recon Gate Notes

Review tier: T3 (contract-adjacent: new fixture material that the chain
promises to remain valid for, even though no schema is changing).
Milestone: Phase 3, slice 1.

Comparisons (design-only, no targets touched, no third-party code imported):

- **<bug-bounty-platform> / Bugcrowd public report shape concepts**
  - Useful pattern: a report carries `title`, `severity`, `impact`,
    `steps_to_reproduce`, `affected_asset`, `evidence`, `remediation`, and a
    duplicate state (`duplicate`, `informative`, `not_applicable`,
    `triaged`, `resolved`).
  - Adopt/adapt/ignore: **adapt narrative shape only.** The curated
    fixtures should use realistic field content that mirrors how a real
    report-shape candidate would look (a real-feeling `summary`, a real
    `verification_guidance`, a redacted `http_exchange` evidence ref) so the
    chain is stressed by realistic data, not by toy values.
  - Safety concern: **reject** all of `duplicate`, `informative`,
    `not_applicable`, `triaged`, `resolved` as fixture-level status values.
    Those are promotion-flavored states and our `finding/1.0` chain explicitly
    forbids `confirmed`, `verified`, `accepted`; fixtures must continue to
    use `candidate` only. Do not import <bug-bounty-platform> / Bugcrowd field names
    (`weakness`, `disclosed_at`, `bounty_amount`, `program_handle`); they are
    out of contract.
  - Contract impact: none. Fixtures stay inside `finding/1.0`.

- **DefectDojo finding lifecycle / dedupe concepts**
  - Useful pattern: explicit lifecycle (`active`, `verified`, `false_p`,
    `risk_accepted`, `out_of_scope`, `mitigated`) and a dedupe key model
    (hash-based dedupe across importers).
  - Adopt/adapt/ignore: **ignore lifecycle, adapt dedupe shape only as a
    fixture stressor.** Use the `duplicate_pair` case to expose that our
    chain does not dedupe today, which is correct for a triage-only chain.
  - Safety concern: importing DefectDojo lifecycle states now would invite
    `verified` / `risk_accepted` into the trial vocabulary. Hard reject.
  - Contract impact: none. The dedupe observation becomes a Phase 3 follow-up
    question, not a P3.1 behavior change.

- **SARIF result shape / levels**
  - Useful pattern: `runs[].results[].level` separates tool-emitted level
    (`note` / `warning` / `error`) from later promotion state; results
    carry `kind` (`pass` / `fail` / `open` / `informational` / `review`)
    and `properties` for tool-specific data.
  - Adopt/adapt/ignore: **adapt level vocabulary in fixture severity_hint
    only.** Our `severity_hint` already supports `informational`, which
    aligns with SARIF's `note`/`informational`. The
    `low_signal_informational` case should use `severity_hint:
    informational` deliberately.
  - Safety concern: SARIF's `kind: fail`/`pass` is promotion-flavored and
    must not appear in fixtures, in tests, or in implementer comments. Use
    our existing `report_readiness` / review_state vocabulary instead.
  - Contract impact: none.

- **Nuclei template findings / scanner JSON conventions**
  - Useful pattern: clean separation between template metadata (tags,
    severity, references, matcher-name) and runtime execution; output JSON
    carries `template-id`, `info.severity`, `matcher-name`, `host`,
    `matched-at`.
  - Adopt/adapt/ignore: **ignore.** Nuclei's output ergonomics are
    target-touching by construction. Fixtures must not mimic Nuclei output
    shape, must not include a `template-id` field, must not include
    `matched-at` URLs, and must not encourage future importer wiring by
    looking importer-shaped. Use only `finding/1.0` fields the chain
    already speaks.
  - Safety concern: any fixture that looks like scanner-tool output makes
    a future scanner-importer slice feel "natural", which is exactly the
    boundary the closeout list forbids. Hard reject.
  - Contract impact: none.

- **OWASP ZAP alert fields**
  - Useful pattern: `risk`, `confidence`, `evidence`, `solution`,
    `reference`, `cweid`, `wascid`.
  - Adopt/adapt/ignore: **adapt narrowly to confirm our existing fields
    are sufficient.** Our `finding/1.0` carries `severity_hint`,
    `confidence`, `evidence[]`, `remediation`, `references[]`,
    `classifications.cwe`. The mapping is clean enough that no new field is
    needed. Adopt ZAP-shaped *content* (a realistic remediation paragraph,
    a CWE classification array of length 1) in the fixtures so they look
    like a real ZAP-style alert without inheriting the scanner-confirmed
    semantics.
  - Safety concern: ZAP marks alerts as scanner-confirmed by default. Our
    fixtures must keep `triage.scanner_output_only: true` and
    `triage.manual_verification_required: true` on every candidate, which
    is the explicit non-promotion guard.
  - Contract impact: none.

**Net OSS Recon Gate decision for P3.1: APPROVE.** All five references support
the proposed P3.1 boundary. Each contributes shape-level realism to fixtures
without any contract change or any new behavior. No reference suggests we
should add a new field, a new vocabulary, a new consumer, or a new lifecycle.

Tier/milestone impact:

- Escalation required: **no.** Stays at T3.
- Can this gate cover later slices: **no.** A separate OSS Recon Gate must run
  for any subsequent slice that (a) adds a second module fixture, (b)
  introduces reviewer-prompt JSON, (c) introduces redaction, (d) promotes any
  schema, or (e) introduces any importer.
- Re-review trigger if assumptions change: any of the following invalidates
  this gate -- a proposal to extract or share the curated fixtures across
  multiple chains; a proposal to attach scanner-importer adapters to the
  fixtures; a proposal to promote any `0.1-trial` schema in the same slice; a
  proposal to add a dedupe behavior to the chain triggered by case 5.

## Implementation Boundary

This boundary is intended to be handed directly to `hermes claude-impl`
(default) or `hermes codex` (fallback) without further direction review.

### Worker route

- Default: **Claude Code Impl** (`hermes claude-impl`). The slice is
  test-and-fixture heavy with structured JSON construction. Six curated
  fixtures plus matching tests fits Claude Code's local-edit profile and
  visibly consumes Claude Code MAX/OAuth usage.
- Fallback: **Codex** (`hermes codex`) if Claude Code Impl declines, runs out
  of turns, or produces non-deterministic JSON.

### Files allowed to write

```text
tests/fixtures/candidate_review_packet/p3_1_curated_partial_evidence/expected_findings.json
tests/fixtures/candidate_review_packet/p3_1_curated_ambiguous_scope_text/expected_findings.json
tests/fixtures/candidate_review_packet/p3_1_curated_chained_precondition/expected_findings.json
tests/fixtures/candidate_review_packet/p3_1_curated_low_signal_informational/expected_findings.json
tests/fixtures/candidate_review_packet/p3_1_curated_duplicate_pair/expected_findings.json
tests/fixtures/candidate_review_packet/p3_1_curated_non_finding_control/expected_findings.json
scripts/test_candidate_workflow_fixture.py   (extend only)
scripts/test_candidate_review_packet.py      (extend only if a curated case
                                              forces a new test assertion;
                                              otherwise leave alone)
scripts/test_candidate_packet_gaps.py        (extend only if needed)
scripts/test_candidate_verification_plan.py  (extend only if needed)
scripts/test_report_readiness_gate.py        (extend only if needed)
scripts/README.md                            (fixture catalog note only)
handoff/accepted_changes.md                  (append-only summary)
handoff/claude_code_result.md                (worker summary)
```

### Files forbidden to modify

```text
modules/_schema/**
scripts/validate_finding_evidence.py
scripts/build_candidate_review_packet.py
scripts/review_candidate_packet_gaps.py
scripts/build_candidate_verification_plan.py
scripts/build_report_readiness_gate.py
scripts/build_candidate_workflow_fixture.py
scripts/program_policy_boundary.py
scripts/module_runner.py
modules/**/*    (no module manifest, no module profile changes)
config/scope.txt
config/recon.conf
recon.sh
loot/**
scans/**
reports/**
.env
credentials, OAuth, scheduler, deployment, billing, production settings
```

Any deviation from these lists is a scope escalation that must route back
through Hermes for a direction-review re-issue, not be absorbed inside the
P3.1 slice.

### Smallest-allowed exception clause

If, and only if, the workflow fixture builder
(`build_candidate_workflow_fixture.py`) genuinely cannot discover the new
curated fixtures because its allowlist is hardcoded to a closed set, the
**only** permitted code change is to widen the allowlist by adding the six
new `p3_1_curated_*` directory names by exact match, in a single PR that
otherwise lands no behavior change. Even this should be avoided if the
builder already enumerates the `candidate_review_packet` directory by
prefix; verify before editing. If a code change is needed, log it explicitly
in `handoff/accepted_changes.md` as a P3.1 scope escalation and update this
review's "Files allowed to write" list in a follow-up. No other consumer may
be touched under this exception.

### Tests required (extensions only; no new test file)

Add the following assertions to existing test files, in the cheapest place
that proves the assertion:

1. **Per-case fixture validity.** For each of the six curated cases, a test
   asserts that `validate_finding_evidence.validate_data` returns success
   over each finding in `expected_findings.json`. Cheapest home: extend
   `scripts/test_candidate_review_packet.py` with a parametric-style loop or
   six small `test_p3_1_curated_<slug>_validates` methods.

2. **Vocabulary coverage across the chain.** In
   `scripts/test_candidate_workflow_fixture.py`, build the workflow fixture
   over the six curated cases and assert:
   - the gap-report stage's `summary` contains `not_ready_count >= 1`,
     `reviewer_decision_required_count >= 1`, and `blocked_count >= 1`;
   - the verification-plan stage's per-finding `plan_state` set includes both
     `blocked` and `needs_manual_review`;
   - the report-readiness-gate stage's per-finding `gate_state` set includes
     both `blocked` and `needs_manual_review`.

3. **Determinism.** Build the workflow fixture twice in the same test and
   assert byte-identical stdout. The existing P2.23 test pattern already does
   this for the smoke fixture; extend it for the curated fixture.

4. **Non-promotional vocabulary lock.** Assert that no per-finding entry in
   any stage of the curated workflow bundle carries a status value in
   `{"confirmed", "verified", "accepted", "ready_for_submission", "fail",
   "pass"}`. This is an explicit safety guard against future drift that would
   silently introduce promotion vocabulary via a fixture.

5. **Synthetic-origin assertion.** Assert that every fixture finding's
   `target.value` ends with one of `.example.test`, `.invalid`, or `.test`,
   and that every `source.module_id` starts with the literal prefix
   `p3_1_curated.`. Cheapest home: a small test in
   `scripts/test_candidate_review_packet.py`.

6. **Forbidden-status fixture guard preserved.** Re-run the existing
   `forbidden_status` fixture test to confirm the contract still rejects
   promoted statuses; the curated additions must not alter this behavior.

Skip adding tests for: per-case JSON shape beyond validator coverage; tests
that lock in specific gap-code strings (those are emergent from the chain
and locking them in fixtures would tightly couple the test to per-stage
implementation details, defeating the slice's purpose of exposing emergent
behavior). The intent is to assert that the chain produces *some* gap codes
and the right vocabulary spread, not to canonize the exact codes.

### Documentation

- Add one short paragraph to `scripts/README.md` (in the existing
  candidate-workflow-chain section) noting that the
  `tests/fixtures/candidate_review_packet/p3_1_curated_*` directories are
  curated near-real synthetic cases used to stress the chain's vocabulary
  coverage, that they remain at `finding/1.0` / `0.1-trial`, and that they
  must not be promoted to importer or scanner-output fixtures without a
  fresh OSS Recon Gate.
- Append one entry to `handoff/accepted_changes.md` summarizing the six new
  fixture directories, the test extensions, and the slice verdict. Treat
  `accepted_changes.md` as append-only.

### Acceptance bundle

The slice is acceptable when:

- All six fixtures exist with the exact slugs above.
- `python -m unittest discover -s scripts -p 'test_*.py'` is green (P2.25
  baselined at `354 OK, 8 skipped`; this slice should add tests, not break
  any). Any newly skipped test must be justified in the worker summary.
- The vocabulary-coverage, determinism, non-promotion, and
  synthetic-origin assertions above all pass.
- `hermes review` is green (JSON valid, Python compiles, `bash -n` clean,
  `.agent.lock` released, scope unchanged).
- `handoff/accepted_changes.md` carries the P3.1 entry.
- `scripts/README.md` carries the curated-fixture paragraph.
- No file outside the "allowed to write" list has changed.
- Worker summary in `handoff/claude_code_result.md` lists changed files,
  validation steps run, and any deviation from this boundary.

## Required TDD / Validation Gates

The implementer should follow this sequence to prevent scope drift:

1. **RED first.** Add the vocabulary-coverage and determinism assertions in
   `scripts/test_candidate_workflow_fixture.py` *before* the six fixture
   files exist. The tests should fail with a clear "fixture directory not
   found" or "vocabulary coverage shortfall" message. This proves the test
   is actually exercising the curated set, not silently passing on the
   existing smoke fixture.

2. **One fixture at a time.** Land the six fixtures in this order so the
   RED tests go green incrementally:
   1. `p3_1_curated_non_finding_control` (simplest; turns on `not_ready`
      coverage).
   2. `p3_1_curated_low_signal_informational` (second `not_ready` exemplar;
      proves the case is not an accident).
   3. `p3_1_curated_partial_evidence` (turns on `blocked` coverage end to
      end).
   4. `p3_1_curated_ambiguous_scope_text` (turns on
      `reviewer_decision_required` -> `needs_manual_review` coverage).
   5. `p3_1_curated_duplicate_pair` (proves chain handles two near-duplicate
      candidates without crashing or merging).
   6. `p3_1_curated_chained_precondition` (most complex; proves text-level
      dependency does not break stable ordering).

3. **Validator gate per fixture.** Run
   `python -m scripts.validate_finding_evidence <fixture_path>` per fixture
   before committing it. Reject the fixture locally if validation fails;
   do not "fix" the validator.

4. **Per-stage smoke per fixture.** After each fixture lands, run
   `python scripts/build_candidate_workflow_fixture.py
   --repo-root <repo> --json` (or equivalent invocation matching the
   builder's actual argv) and visually confirm the per-finding gate_state
   matches the expected state from "Required cases" above. If the chain
   produces an unexpected state, **investigate the fixture, not the
   chain**. Behavior changes to the chain are out of scope.

5. **Determinism gate.** Run the workflow fixture builder twice over the
   final six-fixture set, redirect to two files, and `diff` them. Bytes
   must match. The existing P2.23 test already does this in-process; this
   step is a manual sanity check before the unit test asserts it.

6. **Full-suite gate.** Run the full `python -m unittest discover -s
   scripts -p 'test_*.py'`. The suite must remain green and the test
   count must increase (the new tests must be reachable).

7. **Hermes review gate.** Run `hermes review`. Resolve any JSON or
   `bash -n` failures by fixing the offending file, not by skipping the
   check.

8. **Independent implementation review.** Per
   `handoff/review_tiering_policy.md` T3 row, request a separate
   Claude/Cowork or Codex implementation review against this direction
   boundary before acceptance.

## Safety Boundary Confirmation

This review is design-only. The reviewer did not:

- run live scans, probes, scanners, fuzzers, exploit tooling, callbacks,
  OAST / relay infrastructure, proxy / pivot tooling, or target-touching
  automation;
- import, vendor, or invoke any third-party scanning code;
- modify `config/scope.txt`, `config/recon.conf`, `recon.sh`, anything
  under `modules/**`, `scripts/*.py`, `tests/**`, `loot/**`, `scans/**`,
  `reports/**`, `.env`, credentials, OAuth, scheduler, billing,
  deployment, or production-side settings;
- promote any `*/0.1-trial` schema, draft any report, add any platform
  adapter, change any status to `confirmed` / `verified`, or add any
  runner runtime / recon wiring / module execution surface.

Files this review reads (read-only):
`handoff/cowork_p3_1_direction_prompt.md`,
`handoff/cowork_p2_25_closeout_review.md`,
`handoff/cowork_p2_24_direction_review.md`,
`handoff/oss_recon_gate.md`,
`handoff/review_tiering_policy.md`,
`scripts/build_candidate_review_packet.py`,
`scripts/build_candidate_workflow_fixture.py`,
`scripts/review_candidate_packet_gaps.py` (partial, grep only),
`scripts/build_candidate_verification_plan.py` (partial, grep only),
`scripts/build_report_readiness_gate.py` (partial, grep only),
`tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json`.

Files this review writes:
`handoff/cowork_p3_1_direction_review.md` (this file) and
`handoff/claude_code_result.md` (worker summary stub).

Binding rules from `.hermes.md` preserved: authorization-first, no
exfiltration, no destructive defaults, no silent overwrites, lock
discipline, secrets out of git, report integrity (`accepted_changes.md`
treated as append-only), no production-side changes. None of these were
touched.

The implementation slice that follows this review must preserve the same
posture and is bound by the explicit "forbidden to modify" list above.
Specifically: no live-target affordance is added, no scope semantics are
changed, no schema is promoted, no runner runtime is wired, no scanner
importer is created, and no status above `needs_manual_review` is emitted
by any stage.

## Blocking Issues

None.

The P2.25 closeout already returned `CLOSE_PHASE_2` with explicit
authorization for this slice, sized 4-8 cases, with named boundary locks.
This direction review confirms that authorization, tightens the count to
six, names exactly which cases, attaches an OSS Recon Gate, and writes a
mechanically-applicable implementation boundary. Nothing in the current
chain or repository state blocks implementation.

## Non-Blocking Recommendations

1. **Park the seventh "conflicting source records" case as a P3.4 candidate.**
   When reviewer prompts (P3.3) exist, conflict resolution becomes a natural
   place for human input rather than chain logic. Capture the deferral in
   `handoff/accepted_changes.md` so the case is not lost.

2. **Consider a tiny `scripts/test_curated_fixture_inventory.py` later
   (NOT in P3.1).** Once P3.1 lands, a single test that walks
   `tests/fixtures/candidate_review_packet/p3_1_curated_*` and asserts a
   manifest is present per directory would catch accidentally orphaned or
   added fixtures in future slices. Defer this until at least one future
   curated round is proposed; pre-building inventory tooling for one round
   is premature.

3. **Watch for dedupe-shaped pull from the `duplicate_pair` case.** If
   reviewers see the duplicate pair and immediately propose a dedupe stage,
   that proposal is a new slice with its own OSS Recon Gate (DefectDojo
   territory) -- not a P3.1 follow-on. Hermes should reject "while we're in
   here" dedupe scope creep at intake.

4. **Use the chained-precondition case as the prompt for whether
   `finding/1.0` needs a `relations[]` field at the Phase 3 schema-promotion
   boundary.** This direction review explicitly does not propose adding such
   a field; the case is allowed to demonstrate the gap and the gap is the
   directional signal for a future slice.

5. **Keep the curated fixtures small.** Per case: one short `summary`, one
   short `verification_guidance`, at most two evidence refs, at most two
   classification entries. Bloated fixtures dilute the assertion that the
   chain stresses correctly without becoming a documentation surface.

6. **At implementation-review time, spot-check that no fixture content
   resembles real disclosed reports.** The OSS Recon Gate above adopts shape
   only, not content. Implementer should not paste from public <bug-bounty-platform> /
   Bugcrowd disclosures even with redaction; rewrite from scratch using the
   `.example.test` synthetic narrative.

7. **Hermes should re-confirm baseline before P3.1 begins** with a single
   `hermes review` run plus a `python -m unittest discover -s scripts -p
   'test_*.py'` invocation, so any pre-existing drift is attributed to its
   real source rather than to P3.1.
