> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P2.25 Phase 2 Closeout Review

Date: 2026-05-19
Reviewer: Claude Code MAX/OAuth via `hermes claude-impl` (design-only closeout review)
Review tier: T3 closeout / roadmap review, design-only
Milestone: Phase 2 bug-bounty candidate review workflow closeout
Source prompt: `handoff/cowork_p2_25_closeout_prompt.md`

## Verdict

CLOSE_PHASE_2

## Executive Summary

Phase 2 has delivered everything it set out to deliver and the marginal
return on the next Phase 2 slice is now lower than the marginal return on
the first Phase 3 slice. The contract layer (`finding/1.0`, `evidence/1.0`,
`run/1.0`, `module_manifest`, `module_profile`, `module_input/1.0`,
`module_result/1.0`, `preview_manifest/1.0`, `preview_ledger/1.0`), the
first Level 1 fixture module, the dry-run module runner with
discovery/profile/policy/IO-bundle gating and persisted preview bundles,
and the trial-only candidate review chain P2.19 -> P2.23 together prove an
offline path from a candidate finding to a report-readiness gate result
with deterministic JSON, fail-closed behavior, no schema promotion, and no
target-touching affordances.

P2.24 has already returned `DEFER_REFACTOR_AND_CLOSE_PHASE_2` with strong
safety rationale: the duplication across the chain is real but bounded,
and centralizing the live-target denylist before Phase 3 would weaken the
per-script safety review that this project has chosen elsewhere. Re-running
the P2.24 question inside P2.25 yields the same answer.

The first Phase 3 slice should be **real offline fixture quality**:
replace the synthetic `expected_findings.json` material with curated,
near-real bug-bounty-shaped cases that stress the full chain and expose
genuine gaps in the candidate -> verification -> readiness flow. This is
the highest-value, lowest-risk way to discover what Phase 3 must really
build, without any schema promotion, runtime wiring, report drafting,
platform adapter, or live target work. It also keeps the door closed on
the more attractive but more dangerous Phase 3 directions until they are
specifically requested by the operator.

## Phase 2 Value Assessment

Phase 2 set out to build an offline, modular, policy-gated contract layer
and prove an end-to-end candidate-review workflow without running live
scans. Measured against that goal, Phase 2 has delivered:

1. **Versioned, default-deny contracts.** `modules/_schema/` carries
   `finding/1.0`, `evidence/1.0`, `run/1.0`, `module_manifest`,
   `module_profile`, `module_input/1.0`, `module_result/1.0`,
   `preview_manifest/1.0`, and `preview_ledger/1.0`. Each contract is
   strict-versioned, rejects unknown fields, denies promotion-flavored
   values (no `confirmed` finding status, no completed `module_result`),
   and binds policy/profile/program/target metadata where applicable.

2. **Standard-library-only validators.** `validate_finding_evidence.py`,
   `validate_run_manifest.py`, `validate_module_manifest.py`,
   `validate_module_profile.py`, `validate_module_io_contract.py`,
   `validate_module_io_bundle.py`, `validate_preview_manifest.py`, and
   `validate_preview_ledger.py` give every contract a fail-closed,
   read-only, dependency-free check, suitable for both runner gates and
   later importer/exporter boundaries.

3. **Dry-run module runner with layered gates.** `module_runner.py`
   supports discovery, single-profile selection, manifest validation,
   policy decision binding, optional module I/O preview envelopes, bundle
   consistency checking, and opt-in persisted preview bundles with
   safe-path/symlink/duplicate-run-id rejection. No module code is
   imported, no subprocess is launched, no network is opened, and result
   previews stay `not_executed`.

4. **First Level 1 fixture module.** `modules/checks/level1/
   policy_decision_metadata_audit/module.json` proves the manifest-to-plan
   path end-to-end with zero target touching, zero findings, and zero
   evidence.

5. **Candidate review workflow chain.** P2.19 -> P2.23 demonstrates the
   intended candidate -> review -> gap -> verification -> readiness flow
   without schema promotion, runtime wiring, or report drafting:
   - `build_candidate_review_packet.py` reads only allowlisted committed
     finding fixtures via explicit `--repo-root`, emits
     `candidate_review_packet/0.1-trial`, and rejects forbidden statuses.
   - `review_candidate_packet_gaps.py` consumes the packet from stdin and
     emits `candidate_review_gap_report/0.1-trial` with deterministic
     per-finding gap/action codes.
   - `build_candidate_verification_plan.py` consumes the gap report and
     emits `candidate_verification_plan/0.1-trial` with per-gap human
     checklist items, preserving only `blocked` / `needs_manual_review`.
   - `build_report_readiness_gate.py` consumes the verification plan and
     emits `report_readiness_gate/0.1-trial` with per-finding gate actions,
     never above report-confirmation language.
   - `build_candidate_workflow_fixture.py` chains all four in memory from
     P2.19-allowlisted fixtures and emits one deterministic
     `candidate_workflow_fixture/0.1-trial` JSON document.

6. **Workflow governance.** `handoff/review_tiering_policy.md`,
   `handoff/oss_recon_gate.md`, `handoff/model_usage_routing_policy.md`,
   and the periodic-review baseline at
   `handoff/periodic_reviews/2026-05-18/` give Hermes a repeatable way to
   classify, route, and verify future work without ad-hoc decisions.

Net Phase 2 value: high enough to justify closing now. The contract layer
is broader than it strictly needs to be for the current chain, but the
breadth is the point - it gives Phase 3 a stable surface to plug curated
fixtures, second-module fixtures, and reviewer prompts into without
re-deciding contract shape.

## Candidate Workflow Chain Assessment

The chain demonstrates the intended bug-bounty triage flow end to end on
fixture data. Specifically:

- **Inputs** are committed `finding/1.0` candidates that pass
  `validate_finding_evidence.py`, so the chain starts from contract-clean
  data rather than free-form scanner output.
- **Stage transitions** are deterministic and content-addressed: each
  stage takes one JSON document and emits one JSON document with stable
  sort order, byte-identical compact emission, and per-finding stable
  ordering. The P2.23 fixture chains all four in memory and produces one
  bundle.
- **Status promotion is impossible.** No stage can output `confirmed`,
  `verified`, `ready_for_submission`, or similar promotion-flavored
  vocabulary. The strongest downstream label is `needs_manual_review`,
  with `blocked` / `not_ready` / `reviewer_decision_required` available
  below it.
- **Live-target argument rejection is enforced in-script.** Every stdin
  consumer rejects `--target`, `--url`, `--host`, `--scope`, `--live` and
  their `--flag=value` assignment forms, plus all positional arguments.
  P2.19 and P2.23 declare their own argv grammars because they read
  files; the rejection still applies to live-target affordances.
- **Failures fail closed.** Bad envelopes, wrong schema versions, source
  errors, missing required fields, or unexpected statuses all produce
  structured JSON error envelopes with explicit error codes and non-zero
  exit. P2.23 fails the entire bundle when any upstream stage errors.

Primitives that are present:

- packet builder, gap/action consumer, verification checklist consumer,
  report-readiness gate, end-to-end fixture builder;
- deterministic per-finding ordering and per-finding stable code emission;
- shared but per-stage status vocabulary;
- shared `LIVE_TARGET_FLAGS` discipline duplicated for safety review;
- non-promotional `report_readiness` slots inside the packet builder.

Primitives that are explicitly **not** present and should remain absent
until Phase 3 directionally requests them:

- evidence-locator stage (collecting/redacting evidence pointers per
  candidate);
- redaction gate (pre-emit secret/PII scrub for reviewer artifacts);
- reviewer-notes scaffold (free-form reviewer commentary attached to a
  candidate without leaking into the JSON contracts);
- per-program policy binding inside the chain (so a candidate carries its
  program scope/rules slug forward);
- second-module fixture wiring (so the chain exercises a non-headers
  module path);
- report draft surface (Markdown/HTML reviewer prompt rendering); no
  prose drafting yet.

These are real Phase 3 candidates but they are not blocking Phase 2
closeout. The current chain is sufficient evidence that the offline
workflow shape works.

## Safety Boundary Assessment

The Phase 2 safety posture is intact and tightening over time, not
loosening. Specifically:

- `config/scope.txt` has not been modified by any Phase 2 slice and
  remains operator-only.
- `recon.sh` and `safe_target` semantics have not been changed by any
  Phase 2 candidate-chain slice. P1.4 -> P1.6 runtime hardening
  established artifact validation, evidence integrity, and program
  policy boundary; Phase 2 has only added offline contracts/consumers
  alongside it.
- No live scans, probes, callbacks, OAST, proxy/pivot/transport, or
  target-touching automation has been added. The module runner remains
  dry-run-only with `target_touching: false`, `network_access: none`,
  and empty findings/evidence arrays in all preview paths.
- Module code is not imported. Manifests and profiles are loaded as JSON
  data. The runner does not `exec`, `eval`, or `subprocess.run` any
  module artifact, and discovery refuses path-escaping manifest paths
  and duplicate `module_id` values.
- All schemas remain at `0.1-trial` for the candidate review chain and
  `1.0` for the platform contracts. No `*/0.1-trial` has been promoted to
  a stable contract. No finding status has been promoted to `confirmed`
  or `verified`.
- `loot/`, `.env`, credentials, OAuth, tokens, scheduler, deployment,
  billing, and production settings have not been touched.
- `accepted_changes.md` has been treated as append-only across all
  Phase 2 slices.
- Independent review (Claude/Cowork or Hermes verification with focused
  re-review) has been applied at every T3+ slice. P2.19, P2.20, P2.21,
  P2.22, P2.23, and P2.24 all carry handoff artifacts and validation
  evidence.

Net safety posture: green. Closing Phase 2 does not require any
mitigating action. The boundary that must be guarded most carefully in
Phase 3 is the live-target denylist and the per-script safety review
that goes with it; see "Boundary Locks Requiring Operator Approval".

## Test and Fixture Quality Assessment

Test coverage and discipline are healthy:

- Every Phase 2 slice landed with focused unit tests under
  `scripts/test_*.py`. The full `python -m unittest discover -s scripts
  -p 'test_*.py'` suite reportedly stands at `354 OK, 8 skipped` after
  P2.23, with adjacent P2.19-P2.23 suites at `96 OK`.
- Tests prove fail-closed paths, not just happy paths: malformed
  envelopes, wrong schema versions, source errors, error-bearing inputs,
  promotion-flavored statuses, positional arg rejection, live-target
  assignment-form rejection, byte-for-byte compact JSON emission, and
  deterministic ordering are all asserted.
- Fixtures are committed under `tests/fixtures/` and consumed via
  allowlist-style explicit `--repo-root` arguments rather than ambient
  filesystem traversal.
- Independent implementation review (Claude/Cowork third-party
  perspective, separate from Hermes static review) has been requested
  for T3 slices, with `REQUEST_CHANGES` outcomes addressed before
  acceptance.

Gaps worth naming, none of them blockers for closeout:

- **Synthetic fixture realism.** The current `expected_findings.json`
  inputs are deliberately simple to exercise the contract. They do not
  yet stress the chain with realistic bug-bounty-shaped cases
  (chained-precondition findings, partial evidence, ambiguous scope
  matches, conflicting source records). Phase 3 should add curated
  near-real cases.
- **Single module path.** Only `policy_decision_metadata_audit` exists
  under `modules/checks/level1/`. The runner is generic but only one
  module's `validate_finding_evidence` path is exercised end to end.
- **Drift assertions across consumers.** P2.19-P2.23 each maintain
  independent `_compact_emit` and `_error_payload` shapes. There is no
  cross-script test that asserts byte-identical envelope shape across
  consumers; any drift would be caught only by per-script tests on the
  affected consumer. P2.24 deferred extraction; drift detection is the
  trigger to revisit.

Phase 2 closeout does not require closing any of these gaps; they belong
in Phase 3.

## Phase 3 Priority Recommendation

Phase 3 should be sequenced as follows, in order of recommended
execution. Each item lists why it is sequenced where it is.

**P3.1 (first slice): Real offline fixture quality / curated near-real
findings.**

Replace synthetic `expected_findings.json` material with a small curated
set (target: 4-8 cases) of near-real bug-bounty-shaped findings, still
fully committed and fully offline. Cases should stress:

- partial / messy evidence (truncated, redacted, missing canonical
  references);
- ambiguous scope match (in-scope domain but out-of-scope subpath, or
  in-scope domain via wildcard);
- chained-precondition findings (where the gap report has to surface a
  dependency between two candidates);
- low-severity / informational signal that should not be reportable;
- duplicate / near-duplicate candidates from notional different
  scanners;
- conflicting source records (two records that disagree on severity or
  scope);
- a non-finding control case that should drop out at the gap stage.

Acceptance criteria for P3.1:
- All cases pass `validate_finding_evidence.py`.
- The full P2.19 -> P2.23 chain runs over them with deterministic JSON
  output that is byte-identical across re-runs.
- The fixture builder includes the new cases.
- The chain visibly produces `blocked`, `needs_manual_review`, and
  `not_ready` states for at least one case each, exercising the full
  non-promotional vocabulary.
- Tests assert at least one case lands in each vocabulary state.
- No schema is promoted from `0.1-trial`.

Rationale: this is the highest-value direction because it generates real
learning about whether the chain's per-stage shape is right, without
adding any new surface. It also tells us which Phase 3 directions matter
next - if the curated cases reveal evidence-locator or redaction gaps,
those become P3.2 and P3.3 candidates with concrete acceptance criteria
already in hand.

**P3.2 (second slice): A second Level 1 module fixture.**

Add a second module under `modules/checks/level1/` that exercises a
different module shape (suggested: a metadata-only "scope_match_audit"
or "policy_decision_trace_audit") and validate that the runner's
discovery, profile selection, and bundle consistency layers work for
two modules in the same profile. Still no findings, still no evidence,
still dry-run-only.

Acceptance criteria for P3.2:
- Manifest validates under existing schema with no changes to the
  schema.
- Runner discovery returns both modules and the bundle consistency
  validator produces an `allow` verdict over the two-module preview.
- No new live-target flags, no new network posture, no
  finding/evidence emission.

Rationale: Phase 2 only exercised one module path. Adding a second
module before any reviewer-UX or evidence-locator work confirms that
the runner contract is general, not a single-module accident.

**P3.3 (third slice): Report-readiness reviewer prompts without
submission drafting.**

Add a structured prompt set that a human reviewer or Claude/Cowork can
answer per gate result, still without drafting any submission prose.
This is the smallest UX step that adds value to a real bug-bounty
workflow without crossing into "drafting" or "submission" surface.

Acceptance criteria for P3.3:
- Prompts are stored as JSON or YAML data, not as runnable code.
- Prompts attach to `report_readiness_gate/0.1-trial` outputs by stable
  gate-action code; no free-form prose is emitted by the chain.
- A reviewer answering the prompts produces a structured reviewer-notes
  artifact under a new `*/0.1-trial` schema; status never rises above
  `needs_manual_review`.
- No report drafting, no submission adapter, no platform adapter, no
  network.

Rationale: the value of the candidate chain only materializes once a
reviewer can act on its output. Prompts are the lightest possible UX
without falling into report drafting.

**Explicitly deprioritized for Phase 3 first three slices:**

- Candidate/evidence UX surfaces beyond reviewer prompts (rendering,
  HTML, web UI, IDE integration). These require a separate direction
  review and would be premature before curated fixtures and reviewer
  prompts exist.
- Real evidence-locator stage (collecting actual evidence pointers from
  a scanner run). This is gated on the live-execution boundary and
  belongs much later.
- Redaction gate. Useful, but should be designed only after curated
  fixtures show what kinds of secrets/PII actually appear.

## Explicit Deferrals / What Not To Build Next

The following will not be pursued in Phase 3 until a separate direction
review explicitly approves them:

1. Report generation, report drafting, or report submission adapters.
2. Schema promotion of any `*/0.1-trial` document to a stable
   `modules/_schema/...` contract.
3. Confirmed / verified finding status promotion.
4. Module-runner / recon / scanner runtime wiring or platform adapters.
5. Any live-target flag, callback, OAST, proxy / pivot / transport, or
   network-touching feature, even in lab mode.
6. Any helper that parameterizes the `LIVE_TARGET_FLAGS` denylist or
   allows opting out of it.
7. Pre-emptive core helper extraction (`scripts/core/offline_consumer.py`
   or equivalent). P2.24 deferred this; P2.25 confirms the deferral.
   Re-triggers are listed below.
8. New stdin-only consumer that adds a fifth `_compact_emit` clone
   without first re-running the P2.24 question.
9. Scheduler, deployment, billing, OAuth, or production settings
   changes.
10. CTF schema/runtime promotion. CTF support remains calibration only.
11. Webhook / notification surface for candidate or readiness outputs.
12. External-source ingest (e.g., scanner JSON importers) without a
    fresh OSS Recon Gate.

## Boundary Locks Requiring Operator Approval

The following remain locked until the operator explicitly approves a
narrow change in writing:

- `config/scope.txt` modifications.
- `recon.sh` semantics, `safe_target` behavior, and program policy
  boundary semantics. Hardening that strictly tightens these is in
  scope; weakening or relaxing them is not.
- Program policy boundary (`scripts/program_policy_boundary.py`)
  remains design-only and read-only inside Phase 3 candidate workflow
  slices unless an explicit T4 review covers the change.
- `accepted_changes.md` append-only discipline.
- `loot/`, `.env`, credentials, OAuth tokens, private keys, scheduler
  configs, deployment, and billing.
- Any change that introduces a network client, raw socket, callback
  endpoint, OAST infrastructure, proxy/pivot, beacon, tunnel, or
  reverse listener, even if marked dry-run, lab-only, or test-only.
- Any change that adds `subprocess`, `os.exec*`, `os.spawn*`,
  `multiprocessing`, or `asyncio.create_subprocess_*` to any candidate
  workflow consumer or to the module runner's planning path.
- Schema promotion of any current `*/0.1-trial` schema. The promotion
  itself is a T3 milestone, not a T2 cleanup.

Phase 3 slices that need to cross any of these locks must stop and
route through Hermes for direction review before implementation.

## Revisit Triggers for P2.24 Refactor

The P2.24 deferral remains correct. Reopen the core-helper extraction
question when **any one** of these triggers fires:

1. A third file-reading consumer joins the chain (P2.19 + P2.23 + new).
2. A fifth stdin-only consumer joins the chain (P2.20 + P2.21 + P2.22 +
   new + new).
3. Any `*/0.1-trial` schema is promoted to a stable
   `modules/_schema/...` contract; the matching error/payload/emit
   primitives should be promoted in the same review.
4. Any cross-consumer drift in `_compact_emit`, `_error_payload`, or
   live-flag rejection behavior is observed during review or caught by
   a future cross-consumer test.
5. Any operator-approved change to `LIVE_TARGET_FLAGS` is proposed; a
   single change should be visible in exactly one place, not five.
6. Any consumer needs to import or be imported by another consumer for
   reasons other than the existing P2.23 in-memory chaining (which is
   acceptable as-is).

If none of the above fires, do not extract. Duplication that has not
caused a maintenance event is cheaper than a centralized helper that
quietly relaxes a safety boundary.

If the trigger fires, the minimum task boundary in P2.24 section "If
Proceeding: Minimal Task Boundary" stands as the authoritative starting
point. Name the helper `scripts/core/offline_consumer.py`, hardcode the
denylist, forbid any "ignore_live_flags" / "permissive_argv" parameter,
require RED tests and byte-for-byte compatibility tests before
migration, migrate exactly one consumer first, and never migrate P2.19.

## Suggested First Phase 3 Slice

Slice name: **P3.1 Curated near-real offline fixture set**

Suggested task framing for Hermes to convert into a worker task:

```text
Goal: Add 4-8 curated, near-real, fully offline bug-bounty-shaped
finding cases under tests/fixtures/, run the existing P2.19 -> P2.23
chain over them, and assert deterministic JSON output plus full
non-promotional vocabulary coverage (blocked, needs_manual_review,
not_ready) across the cases.

Files allowed to write:
- tests/fixtures/<new curated cases>/expected_findings.json
- tests/fixtures/<new curated cases>/evidence/*.json (if any; redacted)
- scripts/test_candidate_workflow_fixture.py (extend existing tests)
- scripts/test_candidate_review_packet.py (extend if needed)
- scripts/test_candidate_packet_gaps.py (extend if needed)
- scripts/test_candidate_verification_plan.py (extend if needed)
- scripts/test_report_readiness_gate.py (extend if needed)
- scripts/README.md (fixture catalog note only)
- handoff/cowork_p3_1_direction_review.md (direction review output)
- handoff/accepted_changes.md (append summary)

Files forbidden to modify:
- modules/_schema/** (no schema promotion)
- scripts/build_candidate_review_packet.py (no behavior change)
- scripts/review_candidate_packet_gaps.py (no behavior change)
- scripts/build_candidate_verification_plan.py (no behavior change)
- scripts/build_report_readiness_gate.py (no behavior change)
- scripts/build_candidate_workflow_fixture.py (no behavior change beyond
  pointing at additional allowlisted fixture roots if absolutely
  required, with explicit per-case allowlist; otherwise leave alone)
- config/scope.txt, recon.sh, modules/**/* runtime, loot/**, .env,
  credentials, OAuth, scheduler, deployment, billing, production

Safety boundary:
- Offline / local only. No live scans, callbacks, OAST, network, or
  target interaction.
- No new live-target flags. No "ignore_live_flags" parameter anywhere.
- No status promotion above needs_manual_review. No confirmed /
  verified findings.
- No report drafting, no submission adapter.
- No subprocess, no network client, no scanner import.
- Fixtures must not contain real secrets, real credentials, real
  tokens, real client data, real session material, or unredacted
  personally identifying information. Use synthetic redacted material
  that is shaped like the real thing but is provably fabricated.

Acceptance criteria:
- All cases pass validate_finding_evidence.py.
- Chain runs end-to-end deterministically; byte-identical across reruns.
- At least one case lands in each of {blocked, needs_manual_review,
  not_ready}.
- Full scripts unittest discovery remains green.
- Independent implementation review (Claude/Cowork or third-party)
  records no blockers.
- handoff/accepted_changes.md appended with summary.

Review tier: T3 (contract-adjacent: new fixture material that the
chain promises to remain valid for).
OSS Recon Gate: required as a brief design-only comparison against
<bug-bounty-platform> / Bugcrowd / DefectDojo public finding shapes, with adopt /
adapt / ignore decisions, and an explicit rejection of any
target-touching default.
```

This task is precise enough for Hermes to route through the existing
`hermes claude-impl` / `hermes codex` pipeline without further
direction review, and small enough to land in one slice.

## Blocking Issues

None.

Phase 2 has no outstanding blocker that prevents closeout. The P2.19 ->
P2.23 chain, the contract layer, the module runner, the policy boundary,
and the review/governance docs all stand at a coherent stopping point.
No safety boundary was found weakened. No schema is mid-promotion. No
consumer has a known correctness bug. `accepted_changes.md` is current.

## Non-Blocking Recommendations

1. **Write a Phase 2 closeout note to `accepted_changes.md`.** A single
   append-only entry summarizing the Phase 2 boundary (contract layer,
   candidate workflow chain, governance docs) and explicitly recording
   the verdict `CLOSE_PHASE_2`, the deferral of P2.24, and the chosen
   first Phase 3 slice. This gives any future agent a single
   discoverable closing record for Phase 2.

2. **Add a "Phase 2 closeout state" note to `scripts/README.md`.** A
   short paragraph stating that the candidate workflow chain
   (P2.19-P2.23) is trial-only at `0.1-trial`, that the chain must not
   be promoted without explicit operator approval, and that the
   duplication watchlist from P2.24 (LIVE_TARGET_FLAGS, *_Error,
   _error_payload, _compact_emit, _argv_errors / _live_flag_errors)
   remains intentional until a P2.24 revisit trigger fires.

3. **Capture the "Phase 3 must not pull in from OSS without an OSS
   Recon Gate" list.** Add a short note (suggested:
   `handoff/p3_oss_caution_list.md`) listing SARIF, Nuclei templates,
   DefectDojo lifecycles, OWASP ZAP, <bug-bounty-platform> / Bugcrowd public
   finding shapes, and any scanner JSON importer convention as
   "appealing but each carries a target-touching or promotion-flavored
   default that must remain rejected until a Phase 3 direction review
   explicitly accepts a narrow piece." This is design-only documentation
   and should not be confused with adoption.

4. **Consider documenting the error-code vocabulary convention.** P2.20 -
   P2.23 share a naming convention (`LIVE_TARGET_FLAG_NOT_ALLOWED`,
   `ARGUMENT_NOT_ALLOWED`) but do not formally publish it. A short
   convention paragraph in `scripts/README.md` (no code change) reduces
   drift risk in any future stdin consumer without triggering the P2.24
   extraction question.

5. **Keep the current routing cadence for Phase 3 T3 slices.** Hermes
   direction -> Claude/Cowork direction review with OSS Recon Gate ->
   Claude Code Impl or Codex fallback implementation -> Hermes review ->
   Claude/Cowork or third-party implementation review. P2.24's
   lightweight design-only routing confirmed this is adequate; do not
   require a heavier review by default unless the slice escalates to T4
   (any change that introduces or relaxes a safety boundary, live
   transport, or scope semantics).

6. **Treat any future temptation to add report drafting, submission
   adapters, or platform integrations as a hard stop.** These are the
   most attractive next steps and the easiest to silently expand. Any
   such proposal should be a fresh direction review with explicit
   operator authorization, not an inline addition to a Phase 3 fixture
   or UX slice.

7. **Run `hermes review` once Phase 3 starts** to confirm `.agent.lock`
   discipline, JSON validity, Python compile, and `bash -n` cleanliness
   are still green at the Phase 2 / Phase 3 boundary, before adding any
   new files. Catching baseline drift at the boundary is cheaper than
   debugging it mid-slice.

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
  adapter, change any status to `confirmed`/`verified`, or add any
  runner runtime / recon wiring / module execution surface.

Files this review reads (read-only):
`handoff/cowork_p2_25_closeout_prompt.md`,
`handoff/cowork_p2_24_direction_review.md`,
`handoff/cowork_p2_24_direction_prompt.md`,
`handoff/p2_24_core_extraction_scope.md`,
`handoff/codex_review.md`,
`handoff/accepted_changes.md`,
`scripts/README.md`,
`modules/_schema/README.md`,
`handoff/periodic_reviews/2026-05-18/project_snapshot.md`,
`handoff/periodic_reviews/2026-05-18/hermes_synthesis.md`,
`handoff/review_tiering_policy.md`,
`handoff/oss_recon_gate.md`.

Files this review writes:
`handoff/cowork_p2_25_closeout_review.md` (this file) and
`handoff/claude_code_result.md` (worker summary stub).

Binding rules from `.hermes.md` preserved: authorization-first, no
exfiltration, no destructive defaults, no silent overwrites, lock
discipline, secrets out of git, report integrity (`accepted_changes.md`
treated as append-only), no production-side changes. None of these were
touched.
