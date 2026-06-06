> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.7 Direction Review — Return-to-Mainline / Program-Policy Dry-Run Boundary

Date: 2026-05-19
Reviewer route/tool: Claude Code MAX/OAuth via `hermes claude-impl` (design-only direction review, read-only inspection plus this one review file). The visible runtime/tool is the Claude Code CLI; the exact backing API/runtime version is not exposed by the tool surface.
Visible model/runtime model: Claude Opus 4.7 (per the session's own self-reported model id `claude-opus-4-7`). Exact runner identifier inside Anthropic's hosting is not exposed by the tool surface; this is the strongest model identification available without crossing a tool-output boundary.
Review tier: T3 direction review (the implementation slice it pre-decides is T2/T1; the direction itself is tiered at the highest applicable element because it chooses whether to re-open the program-policy mainline lane).
Milestone: Phase 3 closeout / Phase 1 program-policy mainline re-entry, slice 7 (after P3.6 periodic-review template alignment).
Source prompt: `handoff/cowork_p3_7_direction_prompt.md`.
Predecessors: `handoff/cowork_p2_25_closeout_review.md`, `handoff/cowork_p2_24_direction_review.md`, `handoff/cowork_p3_5_direction_review.md`, `handoff/cowork_p3_6_direction_review.md`, `handoff/cowork_p1_4_proposal.md`, `handoff/active_strategy_queue.md`, `handoff/multi_party_review_decision_policy.md`, `handoff/review_tiering_policy.md`, `handoff/oss_recon_gate.md`, `handoff/accepted_changes.md` (P1-4 Task A/B, P1-4 Task B boundary contract tightening, P2-4 module runner skeleton, P2-7 module profile, P2-14 preview manifest).

Decision: APPROVE_WITH_CHANGES.

## Executive Summary

**Adopt Option 1 (CLOSE_PHASE_3_AND_RETURN_TO_PROGRAM_POLICY_MAINLINE) bundled with a tightly scoped sub-slice of Option 3 (PLAN_RECON_DRY_RUN_POLICY_STAGE_EXERCISE).** Reject Options 2, 4, 5, and 6 for P3.7 specifically. Rationale in one paragraph:

The P3.1-P3.6 candidate-chain / reviewer-artifact line is structurally coherent and has reached an honest pause point. None of P3.6's three re-trigger conditions for the deferred reviewer-notes artifact has fired (no operator note-capture request, no periodic review concluding the new template is insufficient, no two-consecutive deferrals with no operator pushback). The mainline program-policy work named in the 2026-05-18 P1-4 Task B accepted-changes entry and re-affirmed by `handoff/cowork_p2_25_closeout_review.md` lines 374-380 has a real next slice: the `recon.sh` policy gate is wired, validated, and audit-emitting (78 policy-touching lines, `policy_validate_artifact` enforcing schema/source-hashes/audit-event/target/mode/technique/staleness, `policy_decide` failing closed on missing artifact / boundary error / contract mismatch), but the project has never landed an end-to-end synthetic offline exercise that demonstrates `recon.sh --dry-run --program <slug> --policy-mode planned|live` against committed synthetic fixtures inside `programs/_examples/` (which is explicitly excluded from real-program resolution at `recon.sh` line 319). That exercise is the smallest safe next step toward mainline readiness: it does not run scans, does not touch real targets, does not change `config/scope.txt`, does not relax `safe_target` or policy artifact validation, does not promote any schema, does not add a runner-to-recon coupling. It does formalize what already works end-to-end into a regression test suite and a short docs page, which is exactly the kind of hardening `handoff/cowork_p2_25_closeout_review.md` line 376 calls in scope ("Hardening that strictly tightens these is in scope; weakening or relaxing them is not").

Option 4 (PLAN_MODULE_RUNNER_POLICY_ARTIFACT_BRIDGE) is **rejected for P3.7 as scoped**, not forbidden in principle. `module_runner.py` already validates `policy_boundary/1.0` artifacts in dry-run (lines 507-594 of `scripts/module_runner.py`), so a "bridge" slice would either be a no-op or would silently introduce a recon-to-runner coupling that crosses the explicit `handoff/cowork_p2_25_closeout_review.md` lines 378-380 lock ("Program policy boundary remains design-only and read-only inside Phase 3 candidate workflow slices unless an explicit T4 review covers the change"). If approved later, that slice must be its own T3 direction review with its own OSS Recon Gate and explicit operator acknowledgement that recon and runner share a policy artifact namespace.

Option 5 (CONTINUE_PHASE_3_OFFLINE_REVIEW_LINE) is **rejected for P3.7**. P3.6 already disposed of the three obvious candidates (reviewer-notes fixture, reviewer-notes consumer, schema promotion); attempting a fifth/sixth offline review-line slice now invites the "while we're here" pattern P3.6 explicitly locked.

Option 6 (BLOCK_OR_DEFER) is **rejected as the primary decision** because the proposed scope of Option 1 + scoped Option 3 sits well below the T4/T5 activation threshold and does not silently cross any safety boundary. Defer language is used internally for specific sub-questions (e.g., recon-to-runner artifact coupling) so the deferrals are recorded explicitly rather than implied.

Concretely, P3.7's approved direction-review verdict pre-authorizes an implementation slice with this five-file maximum surface:

```text
programs/_examples/sample-lab/scope.json            (new — synthetic program scope
                                                     for offline regression only;
                                                     under the _examples directory
                                                     that recon.sh already
                                                     excludes from real-program
                                                     resolution at line 319)
scripts/test_recon_program_policy_dry_run.py        (new — offline-only,
                                                     subprocess-invoked, asserts
                                                     recon.sh dry-run policy
                                                     gate behavior against
                                                     synthetic scope/target;
                                                     no network, no real
                                                     target, only the
                                                     authorized.test / lab.local
                                                     pattern already used by
                                                     scripts/test_recon_program_cli.py)
handoff/cowork_p3_7_direction_review.md             (this file)
handoff/accepted_changes.md                         (append-only entry)
handoff/claude_code_result.md                       (worker summary stub if
                                                     routed through hermes
                                                     claude-impl)
```

Plus optionally one of:

```text
docs/recon_policy_dry_run.md                        (new — short docs page;
                                                     describes the dry-run
                                                     policy gate workflow for
                                                     operators; no live-mode
                                                     instructions, no
                                                     "production" wording)
```

The implementation slice approved here is **T2** because it adds offline test coverage and (optionally) one docs page around existing T3+ runtime that is itself locked. It is not T3 because no contract, schema, runtime path, or safety helper is modified.

## Question 1 — Review Tier and Milestone Boundary

- **Tier: T3 direction review.** Even though the implementation slice it pre-decides is T2, the direction review itself is T3 because it (a) chooses to close the offline Phase 3 review-line and re-open Phase 1 mainline work, and (b) pre-decides which of the six options to pursue. Per `handoff/review_tiering_policy.md`, a slice is tiered at the highest applicable element and "uncertain safety impact escalates to the higher tier."
- **Milestone: Phase 3 closeout / Phase 1 program-policy mainline re-entry, slice 7.** This is a bridge slice: it closes the P3.1-P3.6 line and re-enters the P1-4 (Task C / dry-run stage integration) lane. The next milestone after P3.7's implementation slice lands should be named "Phase 1 mainline continuation" or similar, with its own direction review for the actual recon-to-runner artifact bridge (deferred from P3.7).
- **No new "Phase 4" milestone** is created here. Creating one would imply the project has graduated to a new phase, which would be misleading: the work is returning to a Phase 1 lane that was paused mid-flight when P2 took the dry-run-only module runner detour and P3 took the candidate-chain / reviewer-artifact detour.

## Question 2 — Decision

**APPROVE_WITH_CHANGES.**

The six options decompose as follows:

- **Option 1 (CLOSE_PHASE_3_AND_RETURN_TO_PROGRAM_POLICY_MAINLINE): APPROVE.** This is the primary direction. See "Approved Scope" below.
- **Option 2 (ADD_OFFLINE_POLICY_BINDING_FIXTURE_ONLY): REJECT for P3.7.** A fixture-only artifact carrying "program slug + policy artifact hash" with no consumer would be either (a) a contract-shaped fixture that no chain consumer reads (i.e., a documentation artifact dressed as data, the same anti-pattern P3.6 rejected for reviewer-notes), or (b) a covert step toward a future recon-to-runner artifact bridge that crosses `handoff/cowork_p2_25_closeout_review.md` lines 378-380. The honest framing for what Option 2 would build is "an offline test fixture under `programs/_examples/`", which is exactly what the Option 3 sub-slice approves.
- **Option 3 (PLAN_RECON_DRY_RUN_POLICY_STAGE_EXERCISE): APPROVE as scoped sub-slice.** This is the right next step. See "Approved Scope" below. The "tiny hardening change" carve-out the prompt mentions is NOT exercised in P3.7 — no `recon.sh` edit, no `program_policy_check.py` edit, no `program_policy_boundary.py` edit. If a hardening change surfaces during implementation review, it must route back to Hermes for a fresh micro-direction review before landing.
- **Option 4 (PLAN_MODULE_RUNNER_POLICY_ARTIFACT_BRIDGE): REJECT for P3.7.** `scripts/module_runner.py` lines 507-594 already validate `policy_boundary/1.0` artifacts in dry-run; the bridge is not missing, it is unexercised end-to-end. The end-to-end exercise belongs in P3.7's recon-side coverage; a recon-to-runner coupling slice would silently re-open the P2.25 closeout lock and must be its own T3 direction review with its own OSS Recon Gate.
- **Option 5 (CONTINUE_PHASE_3_OFFLINE_REVIEW_LINE): REJECT for P3.7.** None of P3.6's three re-trigger conditions has fired. No operator has asked for reviewer-note capture. No periodic review has run against the new P3.6 template yet (the template just landed today, 2026-05-19). The "two consecutive deferrals without pushback" counter is at zero. Continuing the offline review-line would either repeat one of the rejected Options 2-5 from P3.6 or invent a sixth review-line slice with no surfaced need.
- **Option 6 (BLOCK_OR_DEFER): REJECT as the primary decision.** No operator activation is required for the approved sub-slice, no T4/T5 boundary is crossed, and no silent contract-shaping is introduced. BLOCK is reserved for specific sub-questions inside the approved scope (e.g., recon-to-runner coupling deferred until its own review; "tiny hardening" carve-out blocked from being exercised in-slice).

## Question 3 — Preferred Option and Rationale

**Preferred option: Option 1 + Option 3 (scoped) bundled.**

Rationale, in five points:

1. **P3.1-P3.6 is structurally coherent and has reached an honest pause.** `handoff/active_strategy_queue.md` lines 27-38 list the six P3 slices and the boundary they collectively held. P3.6 explicitly disposed of the reviewer-notes question with concrete re-trigger conditions. Continuing the offline review-line in P3.7 without a re-trigger would weaken the deferral's force.
2. **Mainline program-policy work has a real next step.** `handoff/accepted_changes.md` 2026-05-15 P1-4 Task B entry's "Remaining non-blocking carry-forward" calls out "Do not use `--program --policy-mode planned/live` against non-lab targets until Task B wires actual per-stage policy gates" — Task B *did* wire them (`recon.sh` lines 718-810 `policy_decide`), but no offline regression test exercises the end-to-end `recon.sh --dry-run --program <slug> --policy-mode planned|live` flow against a committed synthetic program. That gap is fillable in P3.7 without touching runtime code.
3. **The existing infrastructure is mature enough to build tests around.** The P1-6 policy artifact validation (`policy_validate_artifact` at `recon.sh` line 613) covers path, request match, schema, status, source hashes, boundary audit event, decision target/technique/mode, and staleness. The P1-4 Task B boundary contract tightening (2026-05-18 entry) closed the "unexpected helper contract fields" hole. There are 17 `test_program_policy_check.py` tests and 7+ `test_program_policy_boundary.py` tests passing today. What's missing is the recon-side end-to-end test that wires them together.
4. **The slice is small, reversible, and self-contained.** A new synthetic program scope under `programs/_examples/sample-lab/scope.json` (where `recon.sh` line 319 already forbids real-program resolution against `_examples`), one new test file invoking `recon.sh` as a subprocess in `--dry-run` against a `lab.local` / `authorized.test` target, and at most one short docs page. No edits to runtime scripts, schemas, configs, scope files, modules, or policies.
5. **It progresses the operator's long-term goal (a bug-bounty automation platform with strict scope gates) more than another P3 review-line slice would.** Per `.hermes.md` "Phase 1 will add per-program scope files at `programs/<program-slug>/scope.json`; once present, bug bounty automation must require both `config/scope.txt` and the active program scope/rules to allow the target and technique." Today, only `config/scope.txt` is enforced end-to-end in tests; the program scope side has unit-test coverage but no end-to-end regression. P3.7 closes that loop.

## Question 4 — Safety Boundary

P3.7 is design-and-tests-only.

### What remains offline/local

The implementation slice approved here may:

- create `programs/_examples/sample-lab/scope.json` (new file, under the `_examples` directory `recon.sh` line 319 explicitly forbids from real-program resolution);
- create `scripts/test_recon_program_policy_dry_run.py`, an offline-only subprocess-driven test that invokes `recon.sh --dry-run --program sample-lab --policy-mode planned` and `--policy-mode live` against the existing `lab.local` / `authorized.test` synthetic target pattern (already used by `scripts/test_recon_program_cli.py`, see the 2026-05-15 P1-4 Task A accepted-changes entry);
- assert the recon dry-run produces the expected policy decision artifacts under a temporary run directory, that the audit log contains `PROGRAM_POLICY_ALLOW` / `PROGRAM_POLICY_DENY` events at the expected stages, and that no target-touching subprocess is spawned;
- assert deny paths fire correctly: missing scope file, malformed scope file, CIDR target with `--allow-cidr` forced-deny, stale allow artifact, wrong audit event, wrong schema version, wrong target/mode/technique;
- optionally add `docs/recon_policy_dry_run.md`, a 1-2 page operator-facing docs note describing the dry-run workflow against synthetic targets — must not contain live-mode instructions, real-program slugs, real targets, or any "production" / "live deployment" framing;
- append a single entry to `handoff/accepted_changes.md` recording the slice;
- write `handoff/claude_code_result.md` if the slice routes through `hermes claude-impl`;
- after implementation, an independent reviewer may write `handoff/third_party_p3_7_implementation_review.md`.

### What is forbidden without fresh operator approval

The implementation slice approved here must not:

- run live scans, probes, scanner execution, fuzzers, brute force, callbacks, OAST / interactsh / Burp Collaborator / webhook / requestbin infrastructure, exploit tooling, proxy/pivot/transport tooling, or any target-touching automation;
- invoke `recon.sh` against any host not in the existing test allowlist (`lab.local`, `authorized.test`, or local synthetic targets defined inside the test's temporary `HACKLAB`/scope fixture);
- modify `recon.sh`, `scripts/program_policy_boundary.py`, `scripts/program_policy_check.py`, `scripts/module_runner.py`, any other `scripts/build_*` or `scripts/review_*`, any module under `modules/**`, any schema under `modules/_schema/**`, `config/scope.txt`, `config/recon.conf`, `bin/hermes`, `run_hermes_worker.ps1`, or any production-side setting;
- exercise the prompt's "tiny hardening change" carve-out (the prompt allows it "if the reviewer explicitly justifies" it; this reviewer explicitly does not, to keep the slice T2 and reversible);
- modify any file under `programs/` other than the new `programs/_examples/sample-lab/scope.json` (no real-program slug creation, no edits to `programs/_schema/**` if such exists, no edits to existing `programs/_examples/**` files except the new synthetic);
- modify any file under `tests/fixtures/**`, `templates/**`, `evidence/**`, `runs/**`, `loot/**`, `scans/**`, `reports/**`;
- promote any `*/0.1-trial` schema (the policy contracts `policy_decision/1.0` and `policy_boundary/1.0` are already at 1.0; no change permitted);
- introduce any new live-target CLI affordance (`--target`, `--url`, `--host`, `--scope`, `--live`) anywhere — and specifically must not surface `--policy-mode live` to docs or tests as a "supported live use" except in the context of "this is offline regression coverage for the gate that will deny it";
- weaken `safe_target`, `--skip-scope-check` confirmation, policy artifact validation, CIDR forced-deny, or any other safety helper;
- add scanner-output ingest, importer/exporter behavior, platform adapter, report drafting, submission vocabulary (`confirmed`, `verified`, `valid`, `reportable`, `accepted`, `resolved`, `triaged`, `disclosed`, `submitted`, `published`, `bounty-awarded`, platform names);
- add scheduler / cron / CI auto-execution against targets, deployment, billing, OAuth, credential, secrets, or repo-setting changes;
- add `subprocess`, `os.exec*`, `os.spawn*`, `multiprocessing`, or `asyncio.create_subprocess_*` paths to the module runner or to any candidate-chain consumer; the test itself may use `subprocess.run` to invoke `recon.sh` (this is the standard pattern used by `scripts/test_recon_program_cli.py`), but no production code path gains a new subprocess call;
- create a recon-to-runner artifact coupling (i.e., the test must not invoke `module_runner.py` against policy artifacts produced by `recon.sh`; that coupling is the deferred Option 4 question);
- create or modify any file under `scripts/core/**` (P2.24 helper extraction is not triggered, see "P2.24 trigger assessment" below).

### Whether the next implementation slice is T3, T4, or T5

**T2.** Justification:

- T2 (per `handoff/review_tiering_policy.md`) applies to "moderate-impact offline test/docs/fixture work that exercises existing runtime without modifying it, or that exercises stable contracts without changing them." P3.7's slice fits exactly: new test file, new offline fixture, optional docs page, no runtime code modified, no contract modified.
- T3 (direction-review level) applies to the direction review itself, but the implementation slice it pre-decides is T2.
- T4/T5 (activation, scheduler, deployment, real-program rules, target-touching) is explicitly out of scope; the slice is reversible by `git revert` without rollback complications.

Independent implementation review is required at T2 level per `handoff/review_tiering_policy.md`, but it may be a lighter review than the T3 direction review that produced this artifact: spot-check the forbidden-files list, run the new test suite, confirm `hermes review` PASS, confirm no `config/scope.txt` change, confirm no `recon.sh` edit. Hermes may accept under conditional authority per `handoff/multi_party_review_decision_policy.md`.

## Question 5 — OSS Recon Gate

**OSS Recon Gate: not applicable for P3.7 as scoped (tests/fixture/docs only against existing locked runtime), with forward references recorded for the deferred recon-to-runner coupling slice (Option 4) which would require a fresh gate.**

`handoff/oss_recon_gate.md` lines 22-34 triggering surfaces: "program scope or policy decision contracts; finding, evidence, report, or run manifest schemas; module manifests/profiles/discovery/I/O; runner/executor boundaries; scanner-result importers or adapters; post-scan triage/review workflow; external tool integration or update mechanism." The approved P3.7 scope touches **none** of these as a contract change — it only exercises existing contracts (`policy_decision/1.0`, `policy_boundary/1.0`) from a new test file. The test does not define new contracts; it does not add new schemas; it does not add a new I/O surface to the runner; it does not import scanner results; it does not add an external integration.

However, this review notes forward design alignment with relevant OSS references because the deferred Option 4 (recon-to-runner artifact bridge) and any future per-program-policy live activation *will* require a fresh OSS Recon Gate. The references below are for forward-paving, not for P3.7 implementation:

- **Nuclei workflow / template gating (`workflows/*.yaml`, template `requires` and `conditions`).**
  - Useful pattern: Nuclei separates *workflows* (multi-template execution gated by conditions like `matchers` results) from *templates* (single-finding probes). The gating is explicitly per-target and per-template-tag; `severity` and `tags` form an allow/deny matrix.
  - Adopt/adapt/ignore for P3.7: **ignore** (P3.7 does not introduce gating logic; the gating logic already exists in `recon.sh` `policy_decide` and `program_policy_check.py`).
  - Adopt/adapt/ignore for any future recon-to-runner bridge: **adapt** the pattern of per-technique allow/deny decided once and consumed by multiple downstream stages without re-asking. The existing `policy_decision/1.0` already follows this shape.
  - Safety concern: Nuclei's default templates include `intrusive` and `fuzz` tags; `recon.sh` already excludes them at `normal` intensity. Any future runner bridge must preserve this exclusion and must not let a "allowed by program policy" decision implicitly upgrade to "allow intrusive templates."
  - Contract impact for P3.7: none.
- **OWASP ZAP context / policy concepts (`Scan Policy`, `Context`).**
  - Useful pattern: ZAP separates *Context* (which URLs/hosts are in scope) from *Scan Policy* (which rules and thresholds to apply). The split maps onto the project's `config/scope.txt` (global) + `programs/<slug>/scope.json` (per-program) + `policy_decision/1.0` (per-stage technique decision).
  - Adopt/adapt/ignore for P3.7: **ignore** (already adopted at the Phase 1 design level; the structural separation is in place).
  - Safety concern: ZAP's `Force User` and `Active Scan` modes are exactly the kind of "looks innocuous, escalates immediately" features the project must not adopt. Any future slice must not import a "force scan" affordance under any name.
  - Contract impact for P3.7: none.
- **DefectDojo engagement / test scoping.**
  - Useful pattern: DefectDojo's `Engagement` object scopes a set of `Test` runs by date range, environment, and product; it requires explicit linkage from finding → test → engagement → product.
  - Adopt/adapt/ignore for P3.7: **ignore** (the project does not have an engagement-shaped object and must not gain one in P3.7; the periodic-review templates from P3.6 are the operator-side workflow surface).
  - Safety concern: DefectDojo's importer model couples engagements to imported scanner outputs; the project has no importer and must not gain one. The `handoff/cowork_p3_6_direction_review.md` deferral of platform-coupled vocabulary stands.
  - Contract impact for P3.7: none.
- **SARIF `run.invocations[].arguments`, `run.tool.driver`, `result.provenance`.**
  - Useful pattern: SARIF's `run` object captures the exact invocation (CLI args, working directory, tool driver, version) and per-result provenance for downstream consumers. The project's `run/1.0` manifest (from `scripts/module_runner.py`) already records execution context for dry-run previews.
  - Adopt/adapt/ignore for P3.7: **ignore** (existing `run/1.0` already covers the dry-run preview surface; P3.7 does not extend it).
  - Adopt/adapt/ignore for any future runner-policy bridge: **adapt** the idea that the `run` manifest should record which `policy_boundary/1.0` artifact was consumed (already done by `module_runner.py` lines 587-594) and not just summarize it. Useful forward reference for the deferred Option 4.
  - Safety concern: SARIF `result.kind: pass`/`fail`/`open` is promotion-flavored and remains hard-rejected (`handoff/cowork_p3_5_direction_review.md` assertion 8). `result.suppressions` and `baselineState` would imply a "compared against last run" semantics that the project explicitly does not have.
  - Contract impact for P3.7: none.
- **CI security-scan dry-run patterns (GitHub Actions `dry-run` job, Trivy `--exit-code 0 --dry-run`-equivalent, ZAP baseline `-d` flag).**
  - Useful pattern: most CI security scanners offer a "no-op" or "report-only" mode that exercises the gate without producing actionable scan output. The project's `recon.sh --dry-run --policy-mode dry-run|planned` is conceptually the same.
  - Adopt/adapt/ignore for P3.7: **adapt**. P3.7's test file is the first end-to-end "dry-run regression" for the program-policy gate. The test pattern should mirror CI dry-run semantics: invoke the runtime as a subprocess, capture stdout/stderr, parse the audit log, assert *no* target-touching action was taken (no nuclei output, no nmap output, no nslookup output, no DNS resolution beyond what `safe_target`'s syntax check requires). Standard CI dry-run patterns use stderr regex for "would have run" lines; the project already has this in `recon.sh` audit events.
  - Safety concern: CI dry-run modes occasionally have "but make a real request anyway" escape hatches (Trivy `--scan-type vuln` still hits image registries even in `--exit-code 0` mode). P3.7's test must explicitly assert the absence of such escape hatches — i.e., the test must verify no DNS query, no socket open, no subprocess of `nuclei`/`nmap`/`subfinder`/`crt.sh` is spawned during dry-run.
  - Contract impact for P3.7: **adapt the test pattern** (offline subprocess invocation with stdout/stderr/audit-log inspection); no contract change.

**Net OSS Recon Gate verdict for P3.7: not applicable** (no contract, schema, runtime, importer, or external-tool boundary is touched). Forward references are recorded so the eventual recon-to-runner-bridge direction review and the eventual program-policy live-activation direction review will have a starting point. Both of those future reviews require a fresh full OSS Recon Gate per `handoff/oss_recon_gate.md`.

## Question 6 — Existing Phase 1 / P1-6 Status Check

**Is the current `recon.sh` policy gate mature enough to build tests/docs around, or should a hardening review happen first?**

**Mature enough.** Evidence:

- `recon.sh` policy gate surface is 78 policy-touching lines spanning CLI parsing (lines 209-319), `safe_target` integration (lines 538-570), `policy_decide` per-stage gate (lines 718-810), artifact validation (`policy_validate_artifact` at line 613, including schema-version check, source-hash check, audit-event check, target/mode/technique check, and staleness check inside a Python isolated-mode subprocess at line 670+), and the boundary helper invocation path (lines 749-810).
- `scripts/program_policy_boundary.py` had its contract surface tightened on 2026-05-18 ("Phase 1 P1-4 Task B Boundary Contract Tightening" entry in `handoff/accepted_changes.md`) so unexpected helper contract fields fail closed; this is the strictest the boundary has been.
- `scripts/program_policy_check.py` has 17 passing unit tests (`scripts/test_program_policy_check.py`, per 2026-05-15 entry).
- `scripts/program_policy_boundary.py` has 7+ passing unit tests (`scripts/test_program_policy_boundary.py`, per 2026-05-15 entry, expanded by the 2026-05-18 tightening).
- `scripts/test_recon_program_cli.py` has 12-13 passing offline regression tests for the recon CLI parsing layer (per 2026-05-15 entries).
- `module_runner.py` independently validates `policy_boundary/1.0` artifacts in dry-run (lines 507-594), so the artifact contract has a second consumer that would catch single-consumer drift in policy decisions.

**Known unresolved risks** (none of which require P3.7 hardening, all of which P3.7's new tests should explicitly probe):

1. **Stale allow artifacts.** `policy_validate_artifact` checks staleness at `recon.sh` line ~670+. The risk: the staleness threshold is configurable via env (`PROGRAM_POLICY_TIMEOUT_SECS`), and any future "long-running campaign" use case could be tempted to widen it. P3.7's test must assert that an artifact older than the default staleness threshold fails validation; this exercises the path but does not modify it.
2. **Program / global hash validation.** The boundary records `program_file_sha256` and `global_scope_sha256` and re-checks them. The risk: a future change to `config/scope.txt` or `programs/<slug>/scope.json` between policy decision and stage consumption could silently invalidate the cached artifact. P3.7's test should construct a scenario where the scope file is rewritten mid-run and assert the validation fails.
3. **Target / mode / technique mismatch.** `policy_validate_artifact` requires the artifact's decision target/mode/technique to match the stage's request. The risk: an attacker (or buggy caller) writes an artifact for `target=lab.local mode=dry-run technique=passive` and then asks the stage to consume it for `target=lab.local mode=live technique=intrusive`. P3.7's test must assert this fails.
4. **CIDR forced-deny.** `--allow-cidr` is documented as accepted-but-deny under program policy mode (`recon.sh` line 157, `policy_decide` line 747). The risk: a future "convenience" change that auto-expands CIDR ranges before the boundary check. P3.7's test should pass `--allow-cidr 10.0.0.0/24` against a program policy and assert the deny code is `CIDR_REQUIRES_ALLOW_CIDR` exactly.
5. **Python boundary execution.** `select_policy_python` (`recon.sh` line 589) picks `python3` or `python` and the boundary runs in Python isolated mode (per the P1-4 Task B design, `python -I` to avoid `PYTHONPATH`/`sys.path` injection). The risk: a future "just use the venv" change that drops isolated mode. P3.7's test should not modify this path but should record the expectation that the boundary runs in isolated mode in a comment-block in the test file's preamble.

A targeted hardening review **is not required before P3.7**. The current gate is the strictest it has been. If P3.7's new regression tests surface a real defect, that becomes its own micro-direction review.

## Question 7 — Phase 2 / 3 Boundary Check

Walking the P2.24 revisit triggers from `handoff/cowork_p2_25_closeout_review.md` lines 396-414 against the approved P3.7 scope:

1. **Third file-reading consumer joins the chain — NOT TRIGGERED.** P3.7 adds a *test file*, not a chain consumer. The new test invokes `recon.sh` as a subprocess and inspects audit log files / temporary run directories; it does not implement a stdin-or-file-reading consumer of any candidate-chain `0.1-trial` document. The candidate chain (P2.20-P2.23) is untouched.
2. **Fifth stdin-only consumer joins the chain — NOT TRIGGERED.** No stdin/stdout JSON consumer is added. No `_compact_emit`, `_error_payload`, `_argv_errors`, or `LIVE_TARGET_FLAGS` declaration is added.
3. **Any `*/0.1-trial` schema promoted to `modules/_schema/...` — NOT TRIGGERED.** No schema is touched. The policy contracts in scope (`policy_decision/1.0`, `policy_boundary/1.0`) are already 1.0 and not being changed.
4. **Cross-consumer drift in `_compact_emit` / `_error_payload` / argv rejection — NOT TRIGGERED.** No candidate-chain consumer is edited.
5. **Operator-approved change to `LIVE_TARGET_FLAGS` — NOT TRIGGERED.** The constant is not touched.
6. **New import path between consumers — NOT TRIGGERED.** No Python module is imported between candidate-chain consumers.

Additional Phase 2/3 boundary checks the prompt asks about:

- **Schema promotion?** No. `policy_decision/1.0` and `policy_boundary/1.0` remain at 1.0 (they have always been; they are not `0.1-trial` artifacts). P3.7 does not promote any `0.1-trial` schema; the candidate-chain `*/0.1-trial` schemas are untouched.
- **Shared helper extraction?** No. `scripts/core/**` is forbidden under P3.7.
- **Scanner-output ingest?** No. The new test does not ingest nuclei/subfinder/crt.sh/nmap output; it asserts these subprocesses are *not* spawned in dry-run mode.
- **Report / submission surface?** No. No file under `reports/`, no draft, no platform vocabulary.
- **Fifth file-reading consumer?** No (see trigger 1 above; the test is not a chain consumer).

**Phase 2/3 boundary verdict: clean.** P3.7 closes the offline Phase 3 review-line cleanly and re-enters the Phase 1 mainline lane without firing any of the six revisit triggers and without touching any Phase 2/3 contract surface.

## Question 8 — Minimal Implementation Boundary

### Exact files / directories allowed to change

```text
programs/_examples/sample-lab/scope.json               (NEW. Synthetic
                                                        program scope for
                                                        offline regression
                                                        only. Must live
                                                        under _examples
                                                        because recon.sh
                                                        line 319 explicitly
                                                        forbids real-
                                                        program resolution
                                                        against _examples.
                                                        Content: a JSON
                                                        object matching
                                                        whatever shape
                                                        programs/_schema/
                                                        scope.schema.json
                                                        defines (or a
                                                        minimal valid
                                                        shape if no
                                                        schema yet);
                                                        targets list must
                                                        be exactly the
                                                        synthetic test
                                                        targets (lab.local,
                                                        authorized.test,
                                                        or scope.test).
                                                        Must NOT include
                                                        any real host,
                                                        real IP except
                                                        127.0.0.1 or
                                                        10.x in the
                                                        RFC1918 range
                                                        with explicit
                                                        "synthetic"
                                                        labelling, or
                                                        any external
                                                        wildcard.)
scripts/test_recon_program_policy_dry_run.py           (NEW. Offline-only
                                                        subprocess test
                                                        invoking
                                                        recon.sh in
                                                        dry-run with the
                                                        synthetic program.
                                                        Mirror the
                                                        pattern from
                                                        scripts/test_recon
                                                        _program_cli.py
                                                        for temporary
                                                        HACKLAB setup.
                                                        Standard-library
                                                        only. No network.
                                                        No real targets.
                                                        Must include a
                                                        preamble comment
                                                        listing what the
                                                        test does NOT
                                                        cover (real
                                                        targets, scanner
                                                        invocation,
                                                        live mode end-
                                                        to-end, recon-to-
                                                        runner coupling)
                                                        so a future
                                                        reader does not
                                                        infer coverage
                                                        that is not
                                                        there.)
docs/recon_policy_dry_run.md                           (OPTIONAL.
                                                        Operator-facing
                                                        docs page for the
                                                        dry-run program-
                                                        policy workflow.
                                                        Must NOT include
                                                        live-mode
                                                        instructions,
                                                        real-program
                                                        slugs, real
                                                        targets,
                                                        production
                                                        framing, or
                                                        submission /
                                                        platform
                                                        vocabulary.
                                                        Skipping this
                                                        file is fine;
                                                        if skipped,
                                                        the test file's
                                                        preamble must
                                                        carry the
                                                        operator notes
                                                        instead.)
handoff/cowork_p3_7_direction_review.md                (this file)
handoff/accepted_changes.md                            (append-only
                                                        single entry,
                                                        ".hermes.md" rule)
handoff/claude_code_result.md                          (worker summary
                                                        stub if the slice
                                                        routes through
                                                        hermes claude-
                                                        impl; rolling
                                                        pointer)
handoff/claude_code_task_p3_7.md                       (NEW named
                                                        artifact if
                                                        Hermes chooses
                                                        named-and-
                                                        rolling pattern
                                                        per ".hermes.md"
                                                        collaboration
                                                        contract step 5)
handoff/claude_code_result_p3_7.md                     (NEW named
                                                        artifact, mirror
                                                        of the task file
                                                        above)
handoff/third_party_p3_7_implementation_review.md      (written by
                                                        independent
                                                        reviewer after
                                                        implementation;
                                                        not by the
                                                        implementer)
```

### Exact files / directories forbidden to change

```text
recon.sh                                               (LOCKED per
                                                        handoff/cowork_p2_25_
                                                        closeout_review.md
                                                        lines 375-377)
scripts/program_policy_check.py                        (LOCKED)
scripts/program_policy_boundary.py                     (LOCKED per
                                                        handoff/cowork_p2_25_
                                                        closeout_review.md
                                                        lines 378-380)
scripts/module_runner.py                               (LOCKED for P3.7;
                                                        any coupling
                                                        change is the
                                                        deferred Option 4)
scripts/build_candidate_review_packet.py               (LOCKED)
scripts/build_candidate_verification_plan.py           (LOCKED)
scripts/build_candidate_workflow_fixture.py            (LOCKED)
scripts/build_report_readiness_gate.py                 (LOCKED)
scripts/review_candidate_packet_gaps.py                (LOCKED)
scripts/validate_*.py (every existing validator)       (LOCKED)
scripts/core/**                                        (P2.24 helper
                                                        extraction NOT
                                                        triggered; do
                                                        not create the
                                                        directory)
config/scope.txt                                       (OPERATOR-ONLY)
config/recon.conf                                      (LOCKED for P3.7)
modules/_schema/**                                     (LOCKED — no
                                                        schema bump)
modules/checks/**
modules/profiles/**
templates/**                                           (LOCKED — P3.5
                                                        catalog
                                                        untouched)
tests/fixtures/**                                      (P3.7 uses
                                                        programs/_examples/
                                                        for its synthetic
                                                        program, not
                                                        tests/fixtures;
                                                        do not add a
                                                        new fixture root
                                                        for this slice)
runs/**                                                (LOCKED)
loot/**                                                (BINDING per
                                                        .hermes.md)
scans/**                                               (LOCKED)
reports/**                                             (LOCKED)
evidence/**                                            (LOCKED)
programs/ (any subdir other than _examples/sample-lab/) (LOCKED — no
                                                         real-program
                                                         slug creation)
programs/_schema/**                                    (LOCKED for P3.7;
                                                         if no schema
                                                         exists yet, the
                                                         test must validate
                                                         the synthetic
                                                         scope.json
                                                         against the
                                                         shape that
                                                         program_policy_
                                                         check.py
                                                         already expects)
handoff/multi_party_review_decision_policy.md          (POLICY; the slice
                                                        respects it, not
                                                        edits it)
handoff/review_tiering_policy.md                       (POLICY)
handoff/oss_recon_gate.md                              (POLICY)
handoff/periodic_reviews/**                            (P3.6 scope —
                                                        unchanged here)
.hermes.md                                             (no changes to
                                                        binding context)
.gitignore                                             (no weakening)
.env, credentials, OAuth, scheduler, deployment, billing, production
```

Any deviation is a scope escalation and must route back to Hermes for a fresh direction review.

### Required tests / safety assertions

The implementer must include at minimum the following assertions in `scripts/test_recon_program_policy_dry_run.py`. The test must be importable as a `unittest.TestCase` and runnable via `python -m unittest scripts/test_recon_program_policy_dry_run.py`:

1. **Synthetic scope round-trip.** `recon.sh --dry-run --program sample-lab --policy-mode dry-run --target lab.local` (or whatever the existing CLI shape requires) exits 0 with the expected audit log entries (`PROGRAM_POLICY_ALLOW` at each policy-gated stage) and produces a `policy_boundary/1.0` artifact under the temporary run directory.
2. **Planned mode.** Same as (1) but with `--policy-mode planned`. Behavior should match dry-run for now (since stages do not run target-touching code in dry-run); the test asserts the audit log records `mode=planned` and the artifact's `decision.mode` is `planned`.
3. **Live mode is denied without explicit target authorization.** `--policy-mode live` against the synthetic target should fail closed unless the synthetic scope explicitly allows live mode. The test should assert the deny path: exit non-zero, audit log records `PROGRAM_POLICY_DENY`, and the deny reason code is in the expected set.
4. **Missing scope file deny.** `--program does-not-exist` exits non-zero with "scope file missing" or equivalent (mirrors `scripts/test_recon_program_cli.py` coverage but exercises the policy path, not just CLI parsing).
5. **CIDR forced-deny.** Passing `--allow-cidr 10.0.0.0/24` with `--program sample-lab --policy-mode planned` exits non-zero; deny code is `CIDR_REQUIRES_ALLOW_CIDR` (or whatever the boundary's exact code string is — the test asserts the actual code from `recon.sh` line 747).
6. **Stale artifact rejection.** Construct a `policy_boundary/1.0` artifact with `decided_at_utc` outside the staleness window and place it where `policy_validate_artifact` would consume it; assert the validation fails closed. (This requires understanding the artifact directory layout; if the layout makes this hard to test from outside `recon.sh`, the assertion is **non-blocking** and may be marked as a separate test method with `@unittest.skip("requires recon.sh internal artifact path access")`.)
7. **Target / mode / technique mismatch rejection.** Construct an artifact whose `decision.target` is `other.test` and ask the stage to consume it for `lab.local`; assert validation fails. Same skip caveat as (6).
8. **No target-touching subprocess spawned during dry-run.** The test must capture child processes (or assert specific subprocess invocations did not occur via a mock or via inspection of audit log "would have run" markers) for `nuclei`, `subfinder`, `crt.sh`, `nmap`, `httpx`, or any other scanner binary. The exact assertion shape depends on `recon.sh`'s current dry-run skip pattern; the test should at minimum capture stdout/stderr and assert no scanner-stage output marker appears.
9. **No DNS resolution beyond syntax validation.** `safe_target`'s syntax validator does not resolve hostnames (per `recon.sh` line 538 context); the test asserts no `nslookup`/`dig`/`getent`/Python `socket.gethostbyname` is invoked during dry-run. This is best asserted by setting `HOSTALIASES` or `LD_PRELOAD`-equivalent stubs on Linux, or by capturing the subprocess audit log on Windows. If platform-cross-compatible stubbing is hard, this assertion may be **non-blocking** with skip.
10. **No `config/scope.txt` change.** Test setup writes a temporary `config/scope.txt`-equivalent under `HACKLAB`; test teardown asserts the real `config/scope.txt` is unchanged (compare sha256 before/after).
11. **No real-program slug resolution.** A test must assert that `--program _examples` (i.e., the reserved directory name itself) is rejected by `recon.sh` line 319's "cannot resolve under programs/_examples or programs/_schema" check.
12. **Audit log records the boundary version.** Audit log entries include `policy_boundary/1.0` or equivalent provenance so a future reader can correlate stage decisions to the boundary version.
13. **Test count delta is exactly the new tests added.** Run `python -m unittest discover -s scripts -p 'test_*.py'` before and after; assert the count delta equals the number of new test methods (no test was accidentally removed from another file).

The implementer may add additional defensive assertions but must not add assertions that:

- depend on running `recon.sh` against a real network host;
- depend on a scanner binary being installed (the test must pass on a host with no nuclei/nmap/subfinder/httpx);
- depend on a specific Python version beyond what `recon.sh`'s `select_policy_python` already requires (`python3` or `python` resolvable on `$PATH`);
- depend on a specific OS (the test must skip cleanly on Windows where Unix symlinks are unavailable, mirroring `scripts/test_recon_program_cli.py`'s skip pattern);
- assert on specific timestamp values (they will rot); only assert on shape, presence, and bounded freshness.

### Whether a named artifact and rolling handoff file are both required

**Both.** Per `.hermes.md` Collaboration Contract step 5: "task-specific named artifacts when the slice matters for audit, e.g. `handoff/claude_code_task_p3_6.md` / `handoff/claude_code_result_p3_6.md`, so `claude_code_task.md` and `claude_code_result.md` can remain convenient rolling pointers without losing review history." P3.7 is a bridge slice that closes Phase 3 and re-opens Phase 1 mainline; it matters for audit. The implementer (or Hermes pre-implementation) must:

- write `handoff/claude_code_task_p3_7.md` (named task brief);
- write `handoff/claude_code_result_p3_7.md` (named result) at implementation acceptance;
- update the rolling pointers `handoff/claude_code_task.md` and `handoff/claude_code_result.md` (the existing `bin/hermes new-task` archival behavior handles the rolling pointer's prior-non-empty-file move to `handoff/archive/rolling/`).

## Question 9 — Multi-Party Review Fit

`handoff/multi_party_review_decision_policy.md` requires Hermes-local validation plus implementation, safety/security, and architecture/roadmap reviews. P3.7 routes as follows:

- **Hermes local validation.** Hermes runs `hermes review`, confirms the forbidden-files list, confirms `python -m unittest discover -s scripts -p 'test_*.py'` PASS with the expected count delta, confirms `git diff --check` clean, confirms no edit to any file under the forbidden list, confirms `config/scope.txt` sha256 unchanged.
- **Implementation reviewer.** Required at T2 per `handoff/review_tiering_policy.md`. Route: Claude Code MAX/OAuth in a fresh session (preferred for tier consistency) OR Codex secondary review (acceptable for narrow safety-vocabulary spot-checks and test-file inspection). Must write `handoff/third_party_p3_7_implementation_review.md` with verdict PASS / PASS_WITH_RECOMMENDATIONS / ROUTE_BACK / BLOCK. Must specifically re-perform the no-target-touching assertion check by reading the test file and confirming it asserts the absence of scanner subprocesses.
- **Safety / security reviewer.** Combined with the implementation reviewer for this T2 slice because the slice's safety surface is small (test file + synthetic scope + optional docs page; no runtime code modified). The combined reviewer must perform the forbidden-vocabulary grep (see assertion list above; the test file and docs page must contain zero occurrences of `confirmed`, `verified` as state, `valid`, `reportable`, `accepted`, `resolved`, `triaged`, `disclosed`, `submitted`, `bounty-awarded`, platform names — the words `verification` and `validation` as nouns referring to chain steps remain permitted under the P3.5 carve-out). The combined reviewer must also re-check the live-target-affordance grep across the new files for `--target`, `--url`, `--host`, `--scope`, `--live` flag introductions outside of explicit deny-test contexts.
- **Architecture / roadmap reviewer.** This direction review serves the architecture/roadmap role for the P3.7 slice. The implementation review revisits architecture fit only if the implementer departs from the approved scope or if a hardening change surfaces during implementation that would alter the recon.sh policy gate shape.

**Hermes authority: conditional.** Justification:

- Not **direct authority** because the slice operationalizes the first end-to-end regression of a T3+ runtime surface (`recon.sh` program-policy gate). The first regression for a safety-load-bearing surface deserves a second reviewer pass to confirm the test asserts the right things (especially the "no target-touching subprocess" and "stale artifact rejection" assertions, which are the highest-value ones).
- Not **escalation-only** because no activation, target-touching, scheduler, credential, real-program scope edit, `config/scope.txt` edit, or production-side change is involved. The slice is reversible by `git revert`.
- **Conditional** means: Hermes may accept the implementation slice after the required validation checks AND the independent implementation review verdict, without operator approval, AND with the operator-approval-required flag in the Final Decision Block set to `no`. Operator approval would become required if (a) any forbidden-file edit surfaces during review, (b) the implementer requests the "tiny hardening" carve-out (this review explicitly does not exercise it), (c) the slice grows beyond the file list above, (d) any deferred item (Option 2, 4) is pulled into P3.7 scope without a fresh direction review.

## Question 10 — Final Recommendation for Next Worker Task

Route the implementation slice to `hermes claude-impl` (default for offline coding slices per `.hermes.md` Routing Rules → "Concrete code / script / template change → Codex first" applies for surgical fixes, but P3.7's slice is "implementation-heavy coding" per `.hermes.md` Collaboration Contract step 5, so Claude Code Impl is the correct routing). Codex is the fallback if `hermes claude-impl` is unavailable.

The next worker task brief should:

- copy the "Exact files allowed" and "Exact files forbidden" lists from this review verbatim;
- copy the "Required tests / safety assertions" list from this review verbatim;
- specify `handoff/claude_code_task_p3_7.md` as the named task artifact and `handoff/claude_code_result_p3_7.md` as the named result artifact;
- require `hermes review` PASS before result file is written;
- require `python -m unittest discover -s scripts -p 'test_*.py'` PASS with count delta exactly equal to the new test methods added in `scripts/test_recon_program_policy_dry_run.py`;
- require the implementer to append a single entry to `handoff/accepted_changes.md` recording: (a) what landed (new test file, new synthetic scope, optional docs page); (b) three explicit declarations: "P3.7 was kept tests-and-fixtures-only; no `recon.sh` / `program_policy_*.py` / `module_runner.py` / candidate-chain edits; no schema promotion; no `config/scope.txt` change; no recon-to-runner artifact coupling"; "P2.24 helper extraction was not triggered; the duplication watchlist remains intentional"; "the recon-to-runner artifact bridge (Option 4) remains DEFERRED to a future direction review";
- require the implementer to NOT exercise the prompt's "tiny hardening change" carve-out without routing back to Hermes;
- require the implementer to NOT add any live-target affordance, NOT introduce any new schema, NOT touch `scripts/core/**`, NOT modify any file outside the allowed list.

After implementation, an independent implementation reviewer must produce `handoff/third_party_p3_7_implementation_review.md` with verdict PASS / PASS_WITH_RECOMMENDATIONS / ROUTE_BACK / BLOCK. Hermes then synthesizes per `handoff/multi_party_review_decision_policy.md` "Acceptance Checklist for Hermes" and updates `handoff/accepted_changes.md`.

The slice that follows P3.7 should be one of:

- **P3.8a: Recon-to-runner artifact bridge direction review** (the deferred Option 4 from P3.7). This is a separate T3 direction review with a fresh OSS Recon Gate. It must answer whether `module_runner.py` should consume `policy_boundary/1.0` artifacts produced by `recon.sh` directly (a real coupling), or only consume committed fixtures (a dry-run-only coupling). The answer materially affects the dependency graph and must not be smuggled into a "small" implementation slice.
- **P3.8b: Per-program scope.json schema direction review** (if `programs/_schema/scope.schema.json` does not yet exist, or if it does but the P3.7 synthetic exposes shape gaps). This is a T3 direction review with a fresh OSS Recon Gate. It must answer how the per-program scope contract relates to `config/scope.txt`, what fields are required vs optional, and what techniques/modes are allowed at the schema layer (versus runtime layer).
- **A second periodic multi-party review** using the P3.6 template, once enough time / activity has accumulated. P3.6's "next periodic review" trigger was deliberately left informational; if the operator wants to schedule one near-term, the template is ready.

## Blocking Issues

**None on the approved scope.**

Three pre-emptive locks the implementer must respect:

1. **Do not exercise the "tiny hardening change" carve-out.** The prompt allows a tiny hardening change to `recon.sh` / `program_policy_*.py` "if the reviewer explicitly justifies" one. This reviewer explicitly does not. Reason: keeping the slice tests-only preserves T2 tier, keeps the slice reversible by `git revert`, and prevents the "while we're here" pattern that has previously inflated test-coverage slices into runtime-modification slices. If a real defect surfaces during implementation, route back to Hermes for a separate hardening micro-direction review.

2. **Do not introduce a recon-to-runner coupling.** The prompt's Option 4 is explicitly deferred. The new test must not invoke `scripts/module_runner.py` against `policy_boundary/1.0` artifacts produced by `recon.sh` in the same test run. If the test author is tempted to "just verify the artifact also passes module_runner validation while we're here", that is the deferred coupling and must not be exercised. The two pieces share an artifact contract; verifying their independent compliance is fine (and already happens via `scripts/test_module_runner.py` and the new `scripts/test_recon_program_policy_dry_run.py` separately), but verifying their end-to-end coupling is the deferred Option 4.

3. **Do not edit the 2026-05-18 P1-4 Task B accepted-changes entry or any other historical record.** `handoff/accepted_changes.md` is append-only per `.hermes.md` rule 7. P3.7's append must be a new entry at the tail; "while we're here" edits to historical entries are forbidden and would erase audit lineage.

## Non-Blocking Improvements

1. **Pre-run `hermes review` and full unittest suite to baseline the test count and exit status** before P3.7 implementation begins, so any divergence during P3.7 is attributable to the slice. Standing recommendation from `handoff/cowork_p3_1_direction_review.md` non-blocking 7, restated in `handoff/cowork_p3_5_direction_review.md` non-blocking 7 and `handoff/cowork_p3_6_direction_review.md` non-blocking 7.

2. **Document the synthetic program scope explicitly as synthetic.** The new `programs/_examples/sample-lab/scope.json` should carry a clear top-level annotation (a comment if the schema allows, or a synthetic-flagged field name like `"_synthetic_for_test_only": true`) so a future operator skimming the directory does not mistake it for a real-program scope file. If the schema is strict (no extra fields), the file should be named distinctively (`sample-lab` is sufficient; `example-lab` or `synthetic-lab` would be even clearer). Verify with `recon.sh` line 319 that the chosen name does not collide with any reserved name.

3. **Add a short "what was NOT tested and why" comment block at the top of `scripts/test_recon_program_policy_dry_run.py`.** This mirrors P3.6's required template field for the periodic-review artifact. It catches the failure mode where a regression test implicitly claims coverage it does not have. Suggested content: "This test does NOT cover (a) live mode end-to-end against a real target; (b) recon-to-runner artifact coupling (the deferred Option 4); (c) per-program scope.json schema validation (the deferred Option 3 from P3.6 / future P3.8b); (d) scanner binary integration; (e) DNS resolution edge cases when `getaddrinfo` is hooked at the OS level."

4. **Cross-reference the new test in `scripts/README.md` if such a file exists.** Per the existing pattern (P2-7 entry references `scripts/README.md` update), the new test should appear in any test-catalog index. This is non-blocking; if `scripts/README.md` is in the locked list for P3.7, defer the cross-reference to the next slice that touches it.

5. **Surface the "Phase 1 mainline re-entry" framing in `handoff/active_strategy_queue.md`** at implementation acceptance time. The queue is already current as of 2026-05-19 and names P3.7 as the current lane; once the slice lands, the queue should rotate to name the next P3.8a or P3.8b slice (or a periodic review trigger) as the new current lane.

6. **At implementation acceptance, ensure the `handoff/accepted_changes.md` entry records the three explicit declarations** listed under "Final Recommendation for Next Worker Task" above. These three sentences let any future reader confirm scope discipline without re-reading the direction review.

7. **Independent implementation review is required at T2** per `handoff/review_tiering_policy.md` and `handoff/multi_party_review_decision_policy.md`. The independent reviewer must read the landed test file, run `hermes review`, confirm no forbidden file has been touched, perform the forbidden-vocabulary grep, perform the live-target-affordance grep, and write `handoff/third_party_p3_7_implementation_review.md` with verdict PASS / PASS_WITH_RECOMMENDATIONS / ROUTE_BACK / BLOCK. The reviewer should specifically confirm the test's "no target-touching subprocess" assertion is actually wired (not just present as a comment).

8. **If the optional docs page `docs/recon_policy_dry_run.md` is written**, it should explicitly state "This page describes offline dry-run regression for the program-policy gate. It does not authorize live-mode use against real targets. Live-mode activation requires explicit operator approval per `.hermes.md` Security Gate." This prevents the docs from being mistaken for a "how to run a real bounty engagement" guide.

9. **Note for the next direction review (P3.8a or P3.8b):** the recon-to-runner artifact coupling decision (Option 4) and the per-program scope.json schema decision (related to Option 3's edge cases) are the two near-term mainline questions. Hermes should pre-flag whichever one is chosen as the next slice as requiring a fresh OSS Recon Gate per `handoff/oss_recon_gate.md` lines 22-34 (both touch contract surfaces).

## Codex / Claude Implementation Scope (Forward Brief)

If Hermes routes the implementation slice to `hermes claude-impl` (default), the implementation task should:

- Create `programs/_examples/sample-lab/scope.json` with a synthetic shape per "Exact files allowed" above.
- Create `scripts/test_recon_program_policy_dry_run.py` with the test methods in "Required tests / safety assertions" above.
- Optionally create `docs/recon_policy_dry_run.md`.
- Append the `2026-05-19 — P3.7 ...` entry to `handoff/accepted_changes.md` per the shape in "Final Recommendation for Next Worker Task" above.
- Write `handoff/claude_code_task_p3_7.md` (named task; if the task brief is generated by Hermes, this file already exists) and `handoff/claude_code_result_p3_7.md` (named result) plus the rolling `handoff/claude_code_result.md` pointer.
- Run `hermes review` and `python -m unittest discover -s scripts -p 'test_*.py'`; record outcomes in the result file.
- Not modify any file under the "Exact files forbidden to change" list above.
- Not add any schema, runtime code, fixture root outside `programs/_examples/`, or live-target affordance.

If Hermes routes the implementation slice to Codex (fallback), the same boundaries apply. Codex must not "extract" anything from the new test into shared helpers; the test is self-contained.

## P2.24 Trigger Assessment (Final Statement)

P2.24 helper extraction is **NOT TRIGGERED** by the approved P3.7 scope. The duplication watchlist (`LIVE_TARGET_FLAGS`, `_compact_emit`, `_error_payload`, `_argv_errors`, per-stage error dataclasses across the four candidate-chain consumers) remains intentionally per-script for the safety reasons given in `handoff/cowork_p2_24_direction_review.md` lines 31-66. P3.7 adds a test file that does not declare any of those primitives and does not import any candidate-chain consumer module.

A future slice that proposes a recon-to-runner artifact coupling (the deferred Option 4) **does not** automatically fire any P2.24 trigger either, because it would be a runner-to-runtime coupling rather than a new candidate-chain consumer. If, however, that future slice introduces a fifth file-or-stdin consumer of any `0.1-trial` chain document, the P2.24 review must be re-opened in the same slice.

## Reviewer Route / Tool and Visible Model / Runtime

- **Reviewer route/tool:** Claude Code MAX/OAuth via `hermes claude-impl` (worker invocation per `.hermes.md` "Worker invocation reference" table). The implementation slice that follows is expected to route through the same envelope so a Claude Code Impl run JSON is emitted under `handoff/claude_code_impl_run_<timestamp>.json`.
- **Visible model/runtime model:** Claude Opus 4.7 (per the session's own self-reported model id `claude-opus-4-7`). Exact runner identifier inside Anthropic's hosting is not exposed by the tool surface; this limitation is stated explicitly per `handoff/multi_party_review_decision_policy.md` "Prompt Add-On for Multi-Party Reviews" item 5.
- **Independent reviewer route/tool for the implementation review that follows:** any of (a) a fresh Claude Code MAX/OAuth session in a separate context (preferred for tier consistency); (b) Codex secondary review for narrow safety-vocabulary and test-file spot-checks; (c) Cowork direct in the desktop app. The independent reviewer must write `handoff/third_party_p3_7_implementation_review.md` and must spot-check the forbidden-vocabulary grep, the live-target-affordance grep, the no-runtime-edits constraint, and the no-target-touching-subprocess assertion in the new test file.

## Safety Boundary Confirmation

This review is design-only. The reviewer did not:

- run live scans, probes, scanners, fuzzers, exploit tooling, callbacks, OAST / interactsh / Burp Collaborator / webhook / requestbin infrastructure, proxy/pivot/transport tooling, or any target-touching automation;
- execute any module `check.py`, any candidate-workflow consumer (`scripts/build_*` / `scripts/review_*`), `scripts/module_runner.py`, `scripts/program_policy_boundary.py`, `scripts/program_policy_check.py`, or `recon.sh`;
- import, vendor, or invoke third-party scanning code, platform SDKs, or <bug-bounty-platform>/Bugcrowd/DefectDojo/Intigriti/Synack/YesWeHack APIs;
- modify `config/scope.txt`, `config/recon.conf`, `recon.sh`, anything under `modules/**`, anything under `scripts/**` other than reading existing files for grep/inspection, anything under `tests/**`, anything under `templates/**`, anything under `loot/**`, `scans/**`, `reports/**`, `runs/**`, `programs/**`, `evidence/**`, `.env`, credentials, OAuth, scheduler, billing, deployment, or production-side settings;
- promote any `*/0.1-trial` schema, draft any report prose, add any platform adapter, change any candidate-chain status to `confirmed`/`verified`, alter the runner runtime, add any scanner importer, add any notification surface;
- authorize any active scan, target interaction, module execution, scanner import, report drafting/submission, schema promotion, or platform adapter under this review.

Files this review reads (read-only):
`handoff/cowork_p3_7_direction_prompt.md`,
`handoff/cowork_p3_6_direction_review.md`,
`handoff/cowork_p2_25_closeout_review.md`,
`handoff/cowork_p2_24_direction_review.md`,
`handoff/active_strategy_queue.md`,
`handoff/accepted_changes.md` (tail spanning P1-4 Task A/B, P1-4 Task B boundary tightening, P2-4 module runner, P2-7 module profile, P2-14 preview manifest),
`recon.sh` (policy/safe_target sections only, lines 1-825 spot-grepped),
`scripts/module_runner.py` (lines 507-594, policy validation surface),
`.hermes.md` (loaded as project context),
directory listings for `handoff/`, `scripts/`.

Files this review writes:
`handoff/cowork_p3_7_direction_review.md` (this file, only).

Binding rules from `.hermes.md` preserved: authorization-first, no exfiltration, no destructive defaults, no silent overwrites (the review file is new), lock discipline, secrets out of git, report integrity (`accepted_changes.md` treated as append-only and was not touched by this review), no production-side changes. None of these were touched.

## Direction-Review Output Block

```text
Review tier: T3 (direction review); implementation slice T2 (offline test + synthetic
  fixture + optional docs)
Milestone: Phase 3 closeout / Phase 1 program-policy mainline re-entry, slice 7
Decision: APPROVE_WITH_CHANGES
Preferred option: Option 1 (CLOSE_PHASE_3_AND_RETURN_TO_PROGRAM_POLICY_MAINLINE)
  bundled with a scoped sub-slice of Option 3 (PLAN_RECON_DRY_RUN_POLICY_STAGE_
  EXERCISE). Reject Options 2, 4, 5, 6 for P3.7. Option 4 is rejected for P3.7 but
  named as the next direction review (P3.8a).
Safety boundary: design-and-tests-only; no live scans / probes / scanner execution /
  fuzz / brute force / callbacks / OAST / proxy / pivot / transport / target-
  touching automation; no edits to `recon.sh`, `scripts/program_policy_*.py`,
  `scripts/module_runner.py`, candidate-chain consumers, schemas, configs, scope
  files, modules, runners, reports, credentials, scheduler, deployment, billing,
  or production settings; `config/scope.txt` unchanged; the four candidate-chain
  consumers (P2.20-P2.23) unchanged; the P3.5 catalog and P3.6 periodic-review
  templates unchanged; the policy boundary scripts unchanged
OSS Recon Gate: not applicable — no contract, schema, runtime, importer, or
  external-tool boundary touched. Forward references (Nuclei workflow gating,
  OWASP ZAP context/policy, DefectDojo engagement, SARIF run provenance, CI
  security-scan dry-run patterns) recorded for the deferred recon-to-runner-
  bridge direction review (provisional P3.8a) and any future per-program scope
  schema direction review (provisional P3.8b); both of those future reviews
  require a fresh full OSS Recon Gate.
Existing P1/P1-6 status assessment: mature enough to build offline regression
  tests around. `recon.sh` policy gate is 78 policy-touching lines spanning CLI
  parsing, `safe_target` integration, per-stage `policy_decide`, artifact
  validation (`policy_validate_artifact` covering path, request match, schema,
  status, source hashes, boundary audit event, decision target/technique/mode,
  staleness via Python isolated-mode subprocess), and boundary helper invocation.
  17 `program_policy_check` tests pass; 7+ `program_policy_boundary` tests pass
  (expanded by the 2026-05-18 Task B contract tightening); 12-13 `recon_program_
  cli` tests pass. Known risks (stale artifacts, scope-file hash invalidation,
  target/mode/technique mismatch, CIDR forced-deny, Python isolated mode) are
  all to be exercised by P3.7's new test, NOT modified. No hardening review
  required before P3.7.
Phase 2/3 boundary assessment: clean. None of the six P2.24 revisit triggers
  fires under the approved scope. P3.7 does not add a chain consumer, does not
  promote any schema, does not extract a shared helper, does not add a scanner-
  output ingest, does not add a report/submission surface, does not couple recon
  to runner. The candidate chain (P2.20-P2.23), the P3.5 catalog, and the P3.6
  periodic-review templates are untouched.
Blocking issues: none on the approved scope. Three pre-emptive locks: do not
  exercise the "tiny hardening" carve-out; do not introduce a recon-to-runner
  coupling in this slice (it is the deferred Option 4); do not edit any
  historical `accepted_changes.md` entry.
Non-blocking improvements: 9, see "Non-Blocking Improvements" section.
Codex/Claude implementation scope: add `programs/_examples/sample-lab/scope.json`
  (synthetic); add `scripts/test_recon_program_policy_dry_run.py` (offline test
  exercising recon.sh dry-run program-policy gate); optionally add `docs/recon_
  policy_dry_run.md`; append entry to `handoff/accepted_changes.md`; write
  `handoff/claude_code_task_p3_7.md` and `handoff/claude_code_result_p3_7.md`
  named artifacts plus rolling `handoff/claude_code_result.md` pointer. Do not
  modify any file under the "Exact files forbidden to change" list. No new
  schema, no runtime edit, no fixture root outside `programs/_examples/`, no
  live-target affordance, no scripts/core/** creation.
Required tests/safety assertions: 13 named assertions in the new test file (see
  "Required tests / safety assertions" section); `hermes review` PASS; full
  unittest discovery PASS with count delta exactly equal to the new tests added;
  forbidden-vocabulary grep zero hits on new files; live-target-affordance grep
  zero hits outside explicit deny-test contexts; no file outside the allowed
  list modified; `config/scope.txt` sha256 unchanged; `handoff/accepted_changes.
  md` append-only.
Out-of-scope/deferred items: Option 2 (offline policy-binding fixture only) —
  REJECTED as duplicative; Option 4 (recon-to-runner artifact bridge) —
  DEFERRED to provisional P3.8a direction review with fresh OSS Recon Gate;
  Option 5 (continue Phase 3 offline review-line) — REJECTED for P3.7 as no
  re-trigger has fired; "tiny hardening" carve-out — explicitly NOT exercised
  in P3.7; per-program scope.json schema work — DEFERRED to provisional P3.8b
  direction review; recon-to-runner end-to-end live coupling — BLOCKED until
  explicit T4 operator activation review; live-mode CLI affordance work,
  scanner-output ingest, importer/exporter, platform adapters, lifecycle
  promotion vocabulary, scheduler/CI auto-execution against targets, credentials,
  deployment, billing, OAuth — all remain BLOCKED until explicit operator
  approval at the appropriate tier.
P2.24 trigger assessment: NOT TRIGGERED. None of the six revisit triggers fires
  under the approved P3.7 scope. The new test file is not a chain consumer.
  A future recon-to-runner coupling (deferred Option 4) does NOT automatically
  fire a P2.24 trigger either, but if it introduces a fifth chain consumer in
  the process, the P2.24 review must be re-opened in the same slice.
Reviewer route/tool and visible model/runtime: Claude Code MAX/OAuth via
  `hermes claude-impl`; visible model `claude-opus-4-7` (Claude Opus 4.7). Exact
  runner identifier inside Anthropic's hosting is not exposed by the tool
  surface; this limitation is stated explicitly per `handoff/multi_party_review_
  decision_policy.md` "Prompt Add-On for Multi-Party Reviews" item 5.
```

## Multi-Party Review Decision Block

```text
Decision: PASS_WITH_CONDITIONS
Tier: T3 (direction review); implementation slice T2
Milestone: Phase 3 closeout / Phase 1 program-policy mainline re-entry, slice 7
Hermes authority: conditional. Hermes may accept the implementation slice after
  running `hermes review` PASS, confirming the forbidden-vocabulary grep returns
  zero hits on the new files, confirming the live-target-affordance grep returns
  zero hits outside explicit deny-test contexts, confirming `config/scope.txt`
  sha256 unchanged, confirming no file outside the allowed list was touched,
  confirming `python -m unittest discover -s scripts -p 'test_*.py'` PASS with
  count delta exactly equal to the new test methods added, and obtaining the
  required T2 independent implementation review per `handoff/review_tiering_
  policy.md` and `handoff/multi_party_review_decision_policy.md`. Authority is
  conditional rather than direct because the slice operationalizes the first
  end-to-end regression for a T3+ safety-load-bearing runtime surface (`recon.sh`
  program-policy gate); it is not escalation-only because no activation, target-
  touching, scheduler, credential, real-program scope edit, or production-side
  change is involved.
Reviewers consulted:
  - Claude Code MAX/OAuth direction review via `hermes claude-impl` (this
    artifact); visible model/runtime: Claude Opus 4.7 (`claude-opus-4-7`); exact
    backing API/runtime version is not exposed by the tool surface.
  - Implementation reviewer: will be consulted at implementation-review time;
    route/tool TBD by Hermes (Claude Code MAX/OAuth in a fresh session preferred
    for tier consistency; Codex secondary review acceptable for narrow safety-
    vocabulary and test-file spot-checks).
  - Safety/security reviewer: combined with the implementation reviewer for this
    T2 slice because the slice's safety surface is small (offline test file +
    synthetic scope + optional docs page; no runtime code modified). The
    combined reviewer must perform the forbidden-vocabulary grep, the live-
    target-affordance grep, and the no-target-touching-subprocess assertion
    confirmation in the new test file.
  - Architecture/roadmap reviewer: this direction review serves the architecture/
    roadmap role for the P3.7 slice; the implementation review revisits
    architecture fit only if the implementer departs from the approved scope or
    if a hardening change surfaces during implementation that would alter the
    `recon.sh` policy gate shape.
Validation performed:
  - Read of `.hermes.md` project context, `handoff/cowork_p3_7_direction_prompt.
    md`, `handoff/cowork_p3_6_direction_review.md`, `handoff/cowork_p2_25_
    closeout_review.md` (sections on locked surfaces and P2.24 triggers),
    `handoff/cowork_p2_24_direction_review.md` (helper extraction triggers),
    `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md` (tail
    spanning P1-4 Task A/B, P1-4 Task B boundary tightening, P2-4 module
    runner, P2-7 module profile, P2-14 preview manifest).
  - Spot-read of `recon.sh` policy and `safe_target` sections (78+ policy-
    touching lines covering CLI parsing, `safe_target`, `policy_decide`,
    `policy_validate_artifact`, boundary invocation).
  - Spot-read of `scripts/module_runner.py` lines 507-594 to confirm
    `policy_boundary/1.0` validation already exists in the runner.
  - Confirmed P2.24 trigger assessment by re-walking the six triggers against
    the approved scope.
  - Confirmed OSS Recon Gate non-applicability against the gate's "When
    Required" list (`handoff/oss_recon_gate.md` lines 22-34) for P3.7's scope;
    recorded forward references for the deferred recon-to-runner bridge and
    per-program-scope-schema reviews.
  - Confirmed the Forbidden Files list excludes every file under `scripts/**`
    except the new test file, `recon.sh`, `modules/**`, `templates/**`,
    `config/**`, `tests/**`, `runs/**`, `loot/**`, `scans/**`, `reports/**`,
    `evidence/**`, `programs/**` (except `programs/_examples/sample-lab/`),
    `scripts/core/**`, `handoff/periodic_reviews/**`, and all policy files.
  - Did NOT execute `hermes review`, `python -m unittest discover -s scripts`,
    `recon.sh`, any chain consumer, any module check, any scanner, any
    `program_policy_*.py` script, or any target-touching automation (this is a
    design-only review).
Blocking findings: none on the approved scope. Three pre-emptive locks the
  implementer must respect: do not exercise the "tiny hardening" carve-out; do
  not introduce a recon-to-runner coupling (the deferred Option 4); do not edit
  any historical `accepted_changes.md` entry.
Non-blocking recommendations: 9 (enumerated in "Non-Blocking Improvements"
  section).
Safety boundary: design-and-tests-only; `config/scope.txt` unchanged; no
  `recon.sh` / `program_policy_*.py` / `module_runner.py` / candidate-chain
  edits; no schema promotion; no `scripts/core/**` creation; no scheduler /
  deployment / billing / credential / production change; the four candidate-
  chain consumers (P2.20-P2.23), the P3.5 catalog, and the P3.6 periodic-review
  templates unchanged; no new live-target affordance; no importer / exporter /
  external-tool integration; recon-to-runner artifact coupling deferred with
  explicit P3.8a re-routing; per-program scope.json schema work deferred with
  explicit P3.8b re-routing.
OSS Recon Gate: not applicable for P3.7 as scoped. Forward references recorded
  (Nuclei workflow gating, OWASP ZAP context/policy, DefectDojo engagement,
  SARIF run provenance, CI security-scan dry-run patterns); the eventual P3.8a
  recon-to-runner-bridge direction review and any P3.8b per-program-scope-schema
  direction review will require fresh full OSS Recon Gates.
User approval required: no for the tests-and-fixtures-only implementation slice
  (no target-touching, no scheduler/deployment/billing/credential change, no
  `config/scope.txt` edit, no real-program scope edit, no `recon.sh`/policy
  script edit, no live-mode activation, no schema promotion, no external-side-
  effect activation). Operator approval would become required if (a) any
  deferred item is pulled into scope, (b) any file outside the allowed list is
  touched, (c) the "tiny hardening" carve-out is exercised, (d) any scheduler /
  cron / cadence automation is added, (e) the synthetic `programs/_examples/
  sample-lab/scope.json` accidentally references a real host or external
  wildcard, or (f) a recon-to-runner coupling is introduced without P3.8a
  direction review.
Accepted changes updated: not applicable for this direction review (the review
  file is the artifact). The implementer is required to append a single entry
  to `handoff/accepted_changes.md` at implementation-acceptance time per
  `.hermes.md` rule 4 / 7 (no silent overwrites; append-only). The entry shape
  is specified in "Final Recommendation for Next Worker Task" above and must
  carry the three explicit declarations.
Next action: route this direction review to Hermes for assignment of the
  implementation slice to `hermes claude-impl` (preferred) or Codex (fallback),
  with the "Exact files allowed", "Exact files forbidden", "Required tests /
  safety assertions", and three pre-emptive locks copied into the task brief
  (`handoff/claude_code_task_p3_7.md`). After implementation, an independent
  implementation reviewer must produce `handoff/third_party_p3_7_implementation_
  review.md` with verdict PASS / PASS_WITH_RECOMMENDATIONS / ROUTE_BACK / BLOCK;
  Hermes then synthesizes per `handoff/multi_party_review_decision_policy.md`
  "Acceptance Checklist for Hermes" and updates `handoff/accepted_changes.md`.
  After P3.7 acceptance, the next direction review (provisional P3.8a) should
  address the deferred recon-to-runner artifact coupling (Option 4) with a
  fresh OSS Recon Gate; provisional P3.8b should address the per-program scope.
  json schema with a fresh OSS Recon Gate; both must precede any implementation
  on those surfaces.
```
