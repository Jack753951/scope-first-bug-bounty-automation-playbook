> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.3 Direction Review

Date: 2026-05-19
Reviewer: Claude/Cowork via `hermes claude-impl` (design-only direction review)
Review tier: T3 direction review + OSS Recon Gate, design-only
Milestone: Phase 3, third slice (post-P3.1 curated fixtures, post-P3.2 terminal-state matrix)
Source prompt: `handoff/cowork_p3_3_direction_prompt.md` (this conversation)
Predecessors: `handoff/cowork_p2_25_closeout_review.md`, `handoff/cowork_p3_1_direction_review.md`,
`handoff/third_party_p3_1_implementation_review.md`, P3.2 entry in
`handoff/accepted_changes.md` (2026-05-19).

## Verdict

PROCEED_WITH_CHANGES

The proposed slice (add a second Level 1 module fixture) should not proceed as
literally described, because the premise is already satisfied at the manifest
layer by `modules/checks/level1/security_headers_baseline/module.json`, which
was landed in P2-16 (2026-05-18). What is missing is not a second module; it is
**test coverage that proves the runner/profile/bundle/preview contracts are
green across more than one committed module at the same time**. P3.3 should be
a TEST-ONLY slice that exercises two-module discovery against
`audit-baseline`, without touching any manifest, profile, schema, runner code,
fixture, or evaluator.

If the operator's intent is specifically to add a *manifest-only* (no
`check.py`) third Level 1 module for explicit "no evaluator file on disk"
reasons, that is a separate, smaller slice and belongs to P3.4 after the
P3.3 test coverage proves the two-module contract. It should not be folded
into this slice; the change in approach is the whole signal.

## Rationale

Four reasons drive PROCEED_WITH_CHANGES rather than
PROCEED_WITH_SECOND_LEVEL1_MODULE_FIXTURE.

1. **A second Level 1 module already exists in the repo.**
   `modules/checks/level1/security_headers_baseline/module.json` is a clean
   `module_manifest/1.0` with `risk_level: low`, `target_types: [url, domain]`,
   `technique_tags: [passive.http_headers]`, `execution.default_profile:
   audit-baseline`, `execution.requires_network: false`,
   `execution.target_touching: false`, `output_contracts.emits_findings:
   false`, `output_contracts.emits_evidence: false`, and the same safety-gate
   posture as `policy_decision_metadata_audit`. It satisfies every constraint
   in `modules/profiles/audit-baseline.json` and is independently confirmed by
   the P2-16 entry in `handoff/accepted_changes.md`.

2. **The runner's "no module code import" boundary is what makes the
   second-module-with-evaluator situation safe.** `module_runner.py` reads
   `module.json` as data and does not `import` or `exec` `check.py`,
   `subprocess.run` any module artifact, or otherwise execute evaluator
   logic. Discovery treats the manifest file as the authoritative declaration
   of dry-run safety. `check.py` is invoked only by
   `scripts/test_security_headers_baseline.py` for committed-fixture-driven
   workflow validation, not by the runner. The dry-run boundary therefore
   remains intact across both modules.

3. **The actual gap is test coverage, not module count.** A grep of
   `scripts/test_module_runner.py` shows every `--discover-root` test path
   builds a *minimal fixture repo* containing only
   `policy_decision_metadata_audit` and asserts a one-module plan
   (`payload["plan"]["modules"][0]["module_id"] ==
   "level1.policy_decision_metadata_audit"`). No test exercises the live
   two-module repo state, no test asserts both selected manifests appear in
   `selected_manifests`, no test asserts the bundle consistency layer returns
   `allow` over a two-module preview, and no test asserts deterministic
   ordering when more than one manifest is discovered. The directional claim
   "runner is general across more than one committed module" is therefore
   asserted only by manifest existence, not by green tests.

4. **Adding a third Level 1 module would be ceremony, not signal.** Three
   manifests are not meaningfully stronger evidence of runner generality
   than two; what is needed first is the *test* that two-module discovery is
   green. Adding a third module before that test exists would (a) defer the
   actual gap, (b) introduce a new manifest authoring decision with its own
   bikeshed surface (`scope_match_audit` vs `policy_decision_trace_audit` vs
   neutrally-named), (c) expand the discoverable set without the test that
   proves multi-module discovery works at all, and (d) tempt the slice into
   adding a `check.py`-style evaluator that does not belong in a Phase 3
   fixture-only slice. Each of those is a small risk individually; together
   they are the wrong tradeoff for a slice whose entire purpose is to
   strengthen the multi-module contract claim.

The P3.2 deferral logic from the original P2.25 framing ("second Level 1
module fixture") is therefore satisfied indirectly: the second module already
exists, but the contract it proves remains unobserved by tests. P3.3 closes
that observation gap with the smallest possible change.

## Numbering / Roadmap Clarification

The numbering history needs one short clarifying line in
`handoff/accepted_changes.md` when this slice lands. The history is:

- P2.25 closeout review (2026-05-19) labeled "second Level 1 module fixture"
  as P3.2 in its forward-looking sequencing.
- A P3.1 slice (2026-05-19) landed curated fixtures.
- A subsequent slice labeled P3.2 (2026-05-19) landed the terminal-state
  expectation matrix as a test-only hardening pass, occupying the "P3.2" slot
  with a different scope.
- A second Level 1 module (`level1.security_headers_baseline`) had already
  landed earlier in P2-16 (2026-05-18) as part of workflow-validation work,
  before P2.25 articulated the "second Level 1 module fixture" objective.

The cleanest correction is **not** to renumber any landed slice. The slices
themselves are immutable in `handoff/accepted_changes.md` (append-only). The
P3.3 entry should include exactly one clarifying sentence:

> The "second Level 1 module fixture" objective named in
> `handoff/cowork_p2_25_closeout_review.md` was already physically satisfied
> by the P2-16 `level1.security_headers_baseline` module; P3.3 closes the
> remaining test-coverage gap for two-module runner discovery under
> `audit-baseline` instead of introducing a third module.

No retroactive edit, renaming, or note insertion is required elsewhere.
Renumbering `accepted_changes.md` would break its append-only discipline; one
sentence inside the new P3.3 entry is the correct cost of the collision.

## Approved Module Scope

No new module manifest is approved under this slice. This is the central
shift versus the prompt's proposal. The approved scope is exhaustively:

- **No new files under `modules/**`.** No new module manifest, no new
  module directory, no new profile, no new schema, no new evaluator. The
  two existing Level 1 modules are the entire approved module surface.
- **No edits to existing manifests.** `policy_decision_metadata_audit/
  module.json` and `security_headers_baseline/module.json` remain
  byte-identical across the slice. If a test reveals a manifest field
  must change to make two-module discovery green, that is an
  out-of-scope escalation: route back through Hermes for a direction
  re-issue, do not fix the manifest under cover of P3.3.
- **No edits to `modules/profiles/audit-baseline.json`.** The profile is
  intentionally tight (`risk_level: [info, low]`, `network_access: none`,
  `target_touching: false`, etc.); both existing modules already
  satisfy it.
- **No promotion of any `*/0.1-trial` schema.** None is touched.
- **No new `runs/` artifact, no new persisted preview bundle.** All new
  test assertions run in in-memory `discover_profile_manifests` /
  `module_runner.main` calls and against fresh `tempfile.TemporaryDirectory`
  fixture trees following the existing P2-6 / P2-13 test conventions.

If the operator later decides P3.4 should add a *third* Level 1 module that
is intentionally manifest-only (no `check.py`), the recommended name is
`level1.policy_decision_trace_audit`. The prompt's alternative
`scope_match_audit` name should be **rejected** even for a future slice
because it suggests live scope evaluation behavior in the module's identity,
inviting future scope creep toward runtime scope semantics. Use a name that
cannot be read as a runtime affordance.

## OSS Recon Gate Notes

Review tier: T3 (multi-module contract assertion under the existing module
manifest and profile contracts). No schema or contract changes proposed.
Milestone: Phase 3, slice 3.

Five references were compared at the design level only. No third-party code
was imported, no live target was touched, no scanner shape was adopted.

- **Nuclei templates / ProjectDiscovery metadata / severity tags**
  - Useful pattern: clean separation between template metadata (`id`,
    `info.severity`, `info.tags`, `info.classification.cwe`) and runtime
    behavior; templates are loaded as data and only the runner-side engine
    interprets them. Discovery never imports template code.
  - Adopt / adapt / ignore: **affirm current architecture; adopt nothing
    new under P3.3.** The current `module.json` + `audit-baseline.json` shape
    already mirrors the "metadata is data, runtime is separate" pattern.
    The P3.3 test slice is a chance to assert this separation across more
    than one committed manifest; no new field is required.
  - Safety concern: **reject** Nuclei's `tags: dos`, `intrusive`, `fuzz`,
    `oast`, and `network` semantics. Our `technique_tags` allowlist must
    not grow to include any of these without a separate T4 review.
    `recon.sh` already excludes `dos,intrusive,fuzz` nuclei tags at the
    `normal` intensity; that boundary must not soften in the P3.3 test
    surface.
  - Contract impact: none.

- **OWASP ZAP passive scanner add-ons / alert metadata**
  - Useful pattern: passive scanners declare alert templates (rule id,
    risk, confidence, references, CWE/WASC mapping) as metadata; the
    scan engine resolves them at runtime. Add-on registration is data,
    not executable authority.
  - Adopt / adapt / ignore: **affirm current shape; adopt nothing new.**
    Our `references` array and `safety_gates` block already cover the
    equivalent surface for a fixture-only manifest.
  - Safety concern: ZAP add-ons can declare active scan behavior; we must
    not let "passive scanner add-on" framing in P3.3 docs leak the
    expectation that future Level 1 modules can be active. Keep all P3.3
    documentation explicit that Level 1 remains dry-run-only and that
    audit-baseline's `network_access: none` is non-negotiable.
  - Contract impact: none.

- **Semgrep rule metadata and non-executing rule fixtures**
  - Useful pattern: rule metadata (`id`, `severity`, `languages`,
    `message`) lives in YAML/JSON and is loaded as data; the rule body
    (pattern) is interpreted by the Semgrep engine, not imported as
    Python. Non-executing rule *fixtures* (input/expected output pairs)
    sit alongside rules and are loaded only by tests.
  - Adopt / adapt / ignore: **closest match to current state; affirm and
    adopt nothing new.** The existing `security_headers_baseline/check.py`
    + committed fixtures + `scripts/test_security_headers_baseline.py`
    pattern is structurally identical to Semgrep's rule + fixture
    organization. Under P3.3, no Semgrep-side field needs to be adopted.
  - Safety concern: do not promote Semgrep's notion of a confirmed rule
    match into our `finding/1.0`. Semgrep's `match` is a literal positive
    signal from a static analyzer; our `finding/1.0` `status` must remain
    `candidate` for triage-only emission, never promoted to `confirmed`.
  - Contract impact: none.

- **DefectDojo engagement / test / product separation**
  - Useful pattern: imported findings are organized under
    `product -> engagement -> test`; each layer is a distinct entity in
    the database and findings carry a lifecycle (`active`, `verified`,
    `false_p`, `risk_accepted`, `out_of_scope`, `mitigated`).
  - Adopt / adapt / ignore: **ignore for P3.3.** DefectDojo's separation
    is import-database shaped; our two-module discovery test does not
    need it. The lifecycle vocabulary remains explicitly **rejected** in
    fixtures and tests; `finding/1.0` chain stays at `candidate`-only.
  - Safety concern: importing DefectDojo's lifecycle now (or even shadow-
    naming towards it in test assertion strings) would invite `verified`
    / `risk_accepted` into the trial vocabulary. Hard reject.
  - Contract impact: none.

- **SARIF result / run separation and `level` vocabulary**
  - Useful pattern: SARIF separates `runs[]` (one per tool invocation)
    from `results[]` (one per finding) and uses `level` (`note`,
    `warning`, `error`) plus `kind` (`pass`, `fail`, `open`,
    `informational`, `review`). Our `run/1.0` schema borrows the
    run/finding split conceptually but uses a non-promotion-flavored
    status set.
  - Adopt / adapt / ignore: **affirm current `run/1.0` vs `finding/1.0`
    split; adopt nothing new.** The two-module discovery test should
    assert that one planned `run/1.0` preview can bind both modules and
    that each module's preview is independently consistent with the run
    plan. No SARIF field is needed.
  - Safety concern: SARIF's `kind: fail` / `pass` is promotion-flavored
    and must not appear in test assertions, in payload key names, or in
    log strings. Use `verdict: allow` / `deny` (already used by the
    runner) instead.
  - Contract impact: none.

**Net OSS Recon Gate decision for P3.3: APPROVE.** All five references
support the current module + profile + runner separation and the proposed
test-only scope. None recommends adding any new field, vocabulary,
behavior, contract, or runtime. The decision is consistent with the OSS
Recon Gate already applied in `handoff/cowork_p3_1_direction_review.md`;
nothing has shifted to require fresh adoption.

Tier / milestone impact:

- Escalation required: **no.** Stays at T3.
- Can this gate cover later slices: **no.** A fresh OSS Recon Gate must
  run for any subsequent slice that (a) adds a third Level 1 module
  manifest, (b) introduces any evaluator-import path into the runner, (c)
  proposes promoting `module_input/1.0` / `module_result/1.0` /
  `preview_manifest/1.0` / `preview_ledger/1.0` toward a 1.1 or later
  version, or (d) introduces any importer/exporter/platform adapter.
- Re-review triggers if assumptions change: a proposal to load
  `check.py` from `module_runner.py`; a proposal to add an `enabled`
  field or feature-flag to manifests; a proposal to relax
  `audit-baseline.json` constraints (risk allowlist, technique tags,
  execution flags); any proposal to add finding/evidence emission to a
  Level 1 module.

## Implementation Boundary

This boundary is intended to be handed directly to `hermes claude-impl`
(default worker) or `hermes codex` (fallback) without further direction
review.

### Worker route

- Default: **Claude Code Impl** (`hermes claude-impl`). The slice is
  test-extension-heavy with deterministic JSON assertion construction
  against an existing runner. Local edits, no external state, visibly
  consumes Claude Code MAX/OAuth.
- Fallback: **Codex** (`hermes codex`) if Claude Code Impl declines, runs
  out of turns, or produces non-deterministic ordering assertions.

### Files allowed to write

```text
scripts/test_module_runner.py                        (extend only)
scripts/README.md                                    (one short note only)
modules/_schema/README.md                            (one short note only,
                                                      optional, doc-only)
modules/profiles/INDEX.md                            (one short note only,
                                                      optional, doc-only)
handoff/accepted_changes.md                          (append-only summary)
handoff/claude_code_result.md                        (worker summary)
handoff/cowork_p3_3_direction_review.md              (this review; written by
                                                      reviewer, not the
                                                      implementer)
```

The implementer is expected to extend exactly **one** test file
(`scripts/test_module_runner.py`). No new test file. No new helper module.
No new conftest. No new fixture under `tests/fixtures/`. No new
`runs/<run_id>/` artifact directory. No new test data directory anywhere.

### Files forbidden to modify

```text
modules/_schema/**.json                              (no schema bump, no field add)
modules/checks/**/module.json                        (no manifest edit)
modules/profiles/*.json                              (no profile edit)
modules/checks/level1/security_headers_baseline/check.py
modules/checks/level1/security_headers_baseline/README.md
scripts/module_runner.py                             (no behavior change)
scripts/validate_module_manifest.py
scripts/validate_module_profile.py
scripts/validate_module_io_contract.py
scripts/validate_module_io_bundle.py
scripts/validate_preview_manifest.py
scripts/validate_preview_ledger.py
scripts/validate_finding_evidence.py
scripts/validate_run_manifest.py
scripts/build_candidate_review_packet.py
scripts/review_candidate_packet_gaps.py
scripts/build_candidate_verification_plan.py
scripts/build_report_readiness_gate.py
scripts/build_candidate_workflow_fixture.py
scripts/program_policy_boundary.py
scripts/profile_issues.py
tests/fixtures/**
config/scope.txt
config/recon.conf
recon.sh
loot/**
scans/**
reports/**
runs/**
.env
credentials, OAuth, scheduler, deployment, billing, production settings
```

Any deviation from these two lists is a scope escalation and must route
back through Hermes for a direction-review re-issue. The implementer must
not "fix" a manifest field, "tighten" a profile constraint, or "harden" a
validator inside this slice. Those are separate slices.

### Required tests (extensions only; no new test file)

Add the following to `scripts/test_module_runner.py`. Reuse the existing
`tempfile.TemporaryDirectory` + `fixture_root` pattern. Each test should
copy both committed module manifests (`policy_decision_metadata_audit/
module.json` and `security_headers_baseline/module.json`) plus the
committed `audit-baseline.json` profile into a fresh fixture root, write a
synthetic `policy_artifact()` JSON under `runs/<run_id>/policy/decision.json`
in the fixture root, and invoke either `runner.discover_profile_manifests`
(in-process) or `runner.main([...])` (CLI shape).

1. **Two-module audit-baseline discovery happy path (in-process).**
   Invoke `runner.discover_profile_manifests(repo_root=fixture_root,
   profile="audit-baseline", target_type="url", mode="dry-run")` and
   assert:
   - `result.verdict == "allow"`;
   - `set(m["module_id"] for m in result.selected_manifests) ==
     {"level1.policy_decision_metadata_audit",
      "level1.security_headers_baseline"}`;
   - `result.errors == []` and `result.error_codes == []`;
   - `result.warning_codes` does not include `PROFILE_MEMBERSHIP_MISMATCH`,
     `PROFILE_CONSTRAINT_*`, or `PROFILE_EMPTY_SELECTION` for either
     module;
   - The discovered manifest list is sorted deterministically (the exact
     ordering key is implementation-defined by `module_runner.py`; the
     test should assert that two consecutive calls produce
     identically-ordered `selected_manifests` lists, not lock the order
     to a specific string).

2. **Two-module CLI discovery happy path.** Invoke `runner.main([
   "--discover-root", fixture_root, "--profile", "audit-baseline",
   "--policy-artifact", policy, "--run-id", RUN_ID, "--target-type",
   "url", "--target", TARGET, "--json"])` and assert:
   - exit code `0`;
   - `payload["verdict"] == "allow"`;
   - `payload["plan"]["modules"]` has length 2 and contains both
     `level1.policy_decision_metadata_audit` and
     `level1.security_headers_baseline` as `module_id` values;
   - the rendered stdout contains `"profile": "audit-baseline"`.

3. **Two-module bundle consistency with module I/O preview.** Invoke
   `runner.main([..., "--include-module-io-preview"])` (CLI) or the
   equivalent in-process path and assert:
   - `payload["verdict"] == "allow"`;
   - `payload["module_input_previews"]` has length 2 and one entry per
     module_id;
   - `payload["module_result_previews"]` has length 2 and each is
     `status: not_executed`, `dry_run: true`, `target_touching: false`,
     with empty `findings` and `evidence` arrays;
   - the bundle consistency layer (`validate_module_io_bundle`) returns
     `allow` for the multi-module preview (verified via the runner's own
     `verdict: allow` plus, if exposed in the payload, an explicit
     `bundle_consistency` field equal to `allow`).

4. **Multi-module deterministic-ordering regression.** Call
   `runner.discover_profile_manifests` twice in the same test against the
   same fixture root and assert the two `selected_manifests` lists are
   equal element-by-element (locks the deterministic-ordering claim
   without locking the specific order to a magic string).

5. **Live-repo two-module assertion (read-only).** Call
   `runner.discover_profile_manifests(repo_root=ROOT, profile=
   "audit-baseline", target_type="url", mode="dry-run")` against the
   actual repository root and assert exactly the two expected
   `module_id` values appear in `selected_manifests`. This is the
   smallest live-repo assertion needed to defeat the failure mode where
   fixture-tree tests pass but the actual committed repo state has
   diverged. The test must be read-only: no file write under `ROOT`, no
   `runs/` directory creation under `ROOT`, no policy artifact creation
   under `ROOT`. If the runner requires a `policy_artifact` argument to
   produce a plan, this test should bypass that by invoking
   `discover_profile_manifests` directly (which selects manifests
   without requiring a policy artifact) rather than `runner.main`.

6. **Negative: profile-membership mismatch regression preserved.** Confirm
   that the existing `test_profile_discovery_skips_non_member_and_denies
   _empty_selection` (or equivalent) still passes after the new tests
   land. No edit required to that test; just confirm the suite remains
   green.

7. **Negative: malformed second manifest fails closed.** Add a single
   test where the fixture-copied `security_headers_baseline/module.json`
   is overwritten with `{` (malformed JSON) and assert that the
   discovery call fails closed (`verdict: deny`, an explicit malformed-
   manifest `error_code`, and `level1.policy_decision_metadata_audit`
   NOT present in `selected_manifests` — i.e., a partial-discovery
   fallback is NOT allowed). This is the cheapest assertion of the
   "duplicate or malformed manifest fails the whole discovery, not just
   the offending entry" behavior under two-module conditions.

Skip:

- Asserting specific gap-code or finding-code strings emitted by
  evaluators (no evaluator is invoked under P3.3).
- Asserting that `check.py` is or is not imported (the boundary is
  already enforced by the runner's design; a separate static-import
  test would be a different slice).
- Persisted preview bundle write tests (P2-13 already covers that path;
  duplicating it under two-module conditions is out of scope).

### Documentation

- One short paragraph appended to `scripts/README.md` (in the existing
  module runner / discovery section) noting that
  `modules/checks/level1/` now contains two committed modules
  (`policy_decision_metadata_audit` and `security_headers_baseline`),
  both selected by `audit-baseline`, and that `scripts/test_module_runner.py`
  exercises two-module discovery and bundle consistency.
- Optional one-line edits to `modules/_schema/README.md` or
  `modules/profiles/INDEX.md` confirming the two-module discovery state.
  Doc-only; no contract change.
- One append-only entry in `handoff/accepted_changes.md` summarizing the
  test additions, the numbering clarification, and the slice verdict.
  Include the single clarifying sentence about the P3.2/second-Level-1-
  module collision (see "Numbering / Roadmap Clarification" above).

### Acceptance bundle

The slice is acceptable when:

- The six (or seven, depending on how 7 is counted) new test methods
  exist in `scripts/test_module_runner.py` and pass.
- `python -m unittest discover -s scripts -p 'test_*.py'` is green and
  the test count strictly increases versus the post-P3.2 baseline (post-
  P3.2 baseline per `handoff/accepted_changes.md` 2026-05-19 entry:
  `360 OK, 8 skipped`).
- `hermes review` is green (JSON valid, Python compiles, `bash -n`
  clean, `.agent.lock` released, scope unchanged).
- `handoff/accepted_changes.md` carries a single new P3.3 entry with the
  numbering-clarification sentence.
- `scripts/README.md` carries the two-module discovery paragraph.
- No file outside the "allowed to write" list has changed.
- Worker summary in `handoff/claude_code_result.md` lists changed files,
  validation steps run, and any deviation from this boundary.

## Required TDD / Validation Gates

The implementer should follow this sequence to prevent scope drift.

1. **RED first.** Add at least one of the two-module assertions (the
   in-process discovery or the CLI discovery happy path) **before** any
   other change. The test must fail in a way that names the missing
   manifest in its output — e.g., the assertion
   `set(...) == {"level1.policy_decision_metadata_audit",
   "level1.security_headers_baseline"}` should fail with one of those IDs
   absent. This RED step proves the test is actually exercising the
   two-module path; without it, an accidentally-skipped fixture copy step
   would let the test pass for the wrong reason.

2. **GREEN by fixture wiring only.** Make the RED test green by copying
   both committed manifests into the fixture root in `setUp`. Do not
   "fix" anything in `module_runner.py`, `audit-baseline.json`, or
   either module manifest. If GREEN cannot be reached without touching
   one of those, stop and route back to Hermes — it indicates the
   contract is actually broken at a layer P3.3 was not authorized to
   change.

3. **Determinism gate.** Run the deterministic-ordering test in
   isolation twice (`python -m unittest scripts.test_module_runner.
   TwoModuleDiscoveryTests.test_multi_module_deterministic_ordering -v`)
   to manually confirm two back-to-back invocations produce identical
   results.

4. **Live-repo gate.** Run the live-repo two-module assertion against
   the actual checked-out repo state. Confirm the test fails on a
   sentinel run (temporarily rename `security_headers_baseline/
   module.json` to `module.json.bak` in a non-committed local shell —
   restore immediately afterward) to verify the test would catch a
   future regression in which the second module is removed or
   renamed. Then commit only the test.

5. **Negative-path gates.** Run the malformed-second-manifest test and
   confirm the failure mode is "whole discovery fails closed" not
   "partial discovery returns only the well-formed manifest". If the
   runner currently returns a partial result under this condition, do
   NOT change the runner; instead, flag this as a finding in the
   worker summary and route back to Hermes — this is a real divergence
   from the documented "fails closed on duplicate `module_id` values"
   posture and may warrant a separate T3 hardening slice.

6. **Full-suite gate.** Run `python -m unittest discover -s scripts -p
   'test_*.py'`. The suite must remain green and the test count must
   increase. Any newly-skipped test must be justified in the worker
   summary.

7. **Hermes review gate.** Run `hermes review`. Resolve any JSON or
   `bash -n` failures by fixing the offending file, not by skipping the
   check.

8. **Independent implementation review.** Per
   `handoff/review_tiering_policy.md` T3 row, request a separate
   Claude/Cowork or third-party implementation review against this
   direction boundary before final acceptance.

## Safety Boundary Confirmation

This review is design-only. The reviewer did not:

- run live scans, probes, scanners, fuzzers, exploit tooling, callbacks,
  OAST / relay infrastructure, proxy / pivot tooling, or target-touching
  automation;
- import, vendor, or invoke any third-party scanning code;
- modify `config/scope.txt`, `config/recon.conf`, `recon.sh`, anything
  under `modules/**`, `scripts/*.py`, `tests/**`, `loot/**`, `scans/**`,
  `reports/**`, `runs/**`, `.env`, credentials, OAuth, scheduler,
  billing, deployment, or production-side settings;
- promote any `*/0.1-trial` schema, draft any report, add any platform
  adapter, change any status to `confirmed` / `verified`, or add any
  runner runtime / recon wiring / module execution surface.

Files this review reads (read-only):
`handoff/cowork_p3_3_direction_prompt.md` (delivered inline),
`handoff/cowork_p2_25_closeout_review.md`,
`handoff/cowork_p3_1_direction_review.md`,
`handoff/third_party_p3_1_implementation_review.md`,
`handoff/accepted_changes.md` (first 100 lines),
`modules/checks/level1/policy_decision_metadata_audit/module.json`,
`modules/checks/level1/security_headers_baseline/module.json`,
`modules/checks/level1/security_headers_baseline/README.md`,
`modules/profiles/INDEX.md`,
`modules/profiles/audit-baseline.json`,
`modules/_schema/README.md`,
`scripts/test_module_runner.py` (selected ranges).

Files this review writes:
`handoff/cowork_p3_3_direction_review.md` (this file).

Binding rules from `.hermes.md` preserved: authorization-first, no
exfiltration, no destructive defaults, no silent overwrites, lock
discipline, secrets out of git, report integrity (`accepted_changes.md`
treated as append-only), no production-side changes. None of these were
touched.

The implementation slice that follows this review must preserve the
same posture and is bound by the explicit "forbidden to modify" list
above. Specifically: no live-target affordance is added, no scope
semantics are changed, no schema is promoted, no runner runtime is
wired, no scanner importer is created, no evaluator is imported from
the runner, no manifest is edited, and no status above
`needs_manual_review` is emitted by any stage (this slice does not
emit any candidate-chain status at all; it only asserts runner
discovery shape).

## Blocking Issues

None.

The slice as redirected is smaller than P3.1 was, sits inside the
existing P2-6 / P2-13 test conventions, requires no manifest authoring
or profile decision, and produces a directly verifiable improvement in
contract claim strength. The redirection from "add a second module" to
"test the two existing modules together" is itself the principal
finding; once accepted, the implementation slice is mechanically
applicable.

## Non-Blocking Recommendations

1. **Treat the prompt's `scope_match_audit` name as permanently
   off-limits.** Even in a future P3.4 manifest-only-third-module
   slice, the name reads as "evaluates scope at runtime", which is a
   semantics the project explicitly does not want a module to claim.
   Prefer `policy_decision_trace_audit` or a deliberately neutral name
   such as `manifest_contract_audit_b` for any future third manifest.

2. **Do not extract `module_runner.py` discovery helpers under P3.3.**
   The P2.24 deferral remains correct. If the two-module test reveals
   the discovery path is hard to test without a shared helper, that is
   a separate slice with its own direction review; do not absorb it
   into P3.3 as "while we're here".

3. **Watch for runtime-creep pressure from the second-module landing.**
   `security_headers_baseline/check.py` is a real evaluator that some
   future slice might be tempted to wire into `module_runner.py` for
   "consistency". That wiring is a T4 change (it crosses the "no module
   code import" boundary in the runner) and must route through a fresh
   direction review with explicit operator approval. P3.3's test
   coverage should make that boundary harder to cross silently, not
   easier.

4. **Consider a one-line `scripts/README.md` clarification that
   `check.py` is not imported by `module_runner.py`.** The current docs
   say discovery loads manifests as data; they do not explicitly call
   out that any `check.py` files in module directories are ignored by
   the runner. Adding that one sentence (in the same P3.3 doc-only
   paragraph) closes a small drift risk without expanding scope.

5. **Park the "third Level 1 manifest-only module" question as a P3.4
   candidate.** If, after P3.3 lands, the operator still wants a
   strictly manifest-only datapoint, P3.4 can be a small slice that
   adds one manifest under `modules/checks/level1/<neutral_name>/
   module.json` with no `check.py` and no evaluator. That slice would
   need its own OSS Recon Gate (the same five references would apply
   without changes) and its own direction review; it should not be
   absorbed retroactively into P3.3.

6. **Reaffirm the `0.1-trial` lock at slice review time.** Per
   `handoff/cowork_p2_25_closeout_review.md`'s explicit deferrals,
   nothing in P3.3 may promote any `*/0.1-trial` schema. Implementation
   review should spot-check this by grepping the diff for any
   `0.1-trial` or `1.0` string appearing in a non-test path.

7. **Run `hermes review` before P3.3 implementation begins.** Confirm
   the post-P3.2 baseline (per
   `handoff/accepted_changes.md`: `360 OK, 8 skipped`) is reproducible
   locally so any new failures during the slice are attributable to
   the slice rather than to pre-existing drift.

8. **Hermes should record the redirection in the worker task.** When
   converting this direction review into the
   `handoff/claude_code_task.md` (or codex task) prompt, explicitly
   restate the redirection ("do not add a new module; test the two
   existing modules") so the implementer cannot read the older P2.25
   framing and infer a different scope.
