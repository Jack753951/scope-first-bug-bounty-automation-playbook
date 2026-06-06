> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.9 Direction Review — Dry-Run Recon-to-Runner Bridge

Status: COMPLETE — design/read-only review
Date: 2026-05-19
Prepared by: Claude Code Impl (worker route for design-only direction review)
Review tier: T3 design-only direction review with OSS Recon Gate
Milestone: Gate C — dry-run recon-to-runner bridge direction
Source prompt: `handoff/cowork_p3_9_direction_prompt.md`
Visible model/runtime: invoked via `bin/hermes claude-impl` / Claude Code CLI; the immediate runtime is `claude-opus-4-7` per the wrapper's default model selection. Underlying Anthropic serving runtime is not exposed beyond the CLI's tool surface.

## Executive Verdict

**Decision: APPROVE_WITH_CHANGES.**

A narrow offline-only bridge exercise is the right next mainline slice after Gate B closeout, but **only if implemented as a tests/fixtures/docs slice that does not modify `recon.sh` or `module_runner.py` runtime code.** Both sides of the bridge already speak `policy_boundary/1.0` + `policy_decision/1.0` and both already enforce dry-run semantics; the bridge can be demonstrated entirely through offline test choreography. Runtime emission/consumption changes that would auto-couple the two tools must remain deferred to a separate T4 review and operator approval.

## 1. Review Tier and Milestone Boundary

### Default tier

This prompt is correctly framed as **T3 design-only direction review**. The OSS Recon Gate is mandatory because the slice introduces a *cross-tool consumption pattern* between two existing platform contracts (program-policy boundary on the recon side, run-manifest/policy-artifact consumption on the runner side). Even if no schema is being changed, the act of declaring that one tool's artifact is consumed by the other tool's runner is a platform-boundary decision under `handoff/review_tiering_policy.md` row "T3: Contract/platform boundary."

### Escalation analysis

The bridge is *adjacent* to T4 but does not itself cross it, provided the approved slice satisfies all of these:

- Both tools remain dry-run only at every call site.
- No runtime code in either `recon.sh` or `scripts/module_runner.py` changes.
- No CLI affordance is added to either tool to auto-locate, auto-rename, auto-copy, or auto-promote the recon-side artifact into the runner-side `runs/<run_id>/policy/<file>` location.
- The path translation (recon's `policy_boundary_<ts>_<pid>_<nanos>_<target>.json` → runner's `runs/<run_id>/policy/decision.json`) is performed **only by the test harness**, never by production code.
- The test never runs against a real program slug, real target, or `config/scope.txt`-listed asset; only `programs/_examples/sample-lab/` (the synthetic fixture already in tree).

Escalation to T4 is required if any of the following appears in the implementation:

- A new flag in either tool that emits/consumes the bridged artifact.
- A wrapper script under `bin/` or `scripts/` that copies a recon artifact into the runner's expected location at runtime.
- Any change to `recon.sh` artifact filename, location, or schema that nudges it toward the runner's expected layout.
- Any new policy decision step gated on the runner's verdict (i.e., runner output feeding back into recon decisions).
- Any test that uses a non-`_examples/` slug or invokes either tool without `--dry-run` / `mode=dry-run`.

### Can implementation stay offline without operator approval?

Yes, provided the slice stays in the **tests/fixtures/docs-only** boundary above. Per `handoff/multi_party_review_decision_policy.md`, Hermes has *conditional* authority for aligned T3 offline work. Operator approval is **not** required for the test/fixture slice. Operator approval becomes required for any T4 follow-up (runtime bridge), as does a fresh direction review with OSS Recon Gate.

## 2. Whether to Bridge Now

### Recommendation: bridge now, with the narrow scope below

The bridge slice is the right next mainline lane after Gate B closeout for four reasons:

1. **The two contracts are already aligned.** Both `program_policy_boundary.py` and `scripts/module_runner.py::_validate_policy_artifact` use `policy_boundary/1.0` + `policy_decision/1.0`, both require `boundary.status == "allow"`, both require `audit_event == "PROGRAM_POLICY_ALLOW"`, both check `helper.returncode == 0`, both fence on canonical SHA-256 program/global-scope hashes, and both check `request.target` and `request.mode` parity. The runner additionally checks that `request.mode` matches and that the artifact file sits under `runs/<run_id>/policy/`. There is no schema drift to resolve in this slice; only an offline demonstration of inter-tool compatibility.

2. **It is the smallest credible step on the launch path.** `handoff/project_launch_estimate_20260519.md` Gate C explicitly names "Recon-to-runner bridge, still dry-run only" as the next slice, estimated at 4–8 small slices. A tests-only bridge demonstration retires the largest design uncertainty (does the recon-emitted artifact actually pass the runner's validator?) at near-zero runtime risk.

3. **It unblocks a real triage question without creating new surface.** Today the runner is exercised only with fixture artifacts (`test_module_runner.py::policy_artifact`). The bridge slice proves the recon side's real emission also satisfies the runner's validator, which is a precondition for any later P3.10+ "discovery → planning" review without committing to that bridge in runtime.

4. **The Gate B closeout deferred items are not blocking.** Per `handoff/program_policy_dry_run_closeout_20260519.md`, the only remaining Gate B items are (a) the "stale artifact / target / mode / technique mismatch E2E harness" and (b) optional follow-up triggers if `recon.sh` or policy helpers change. Both are non-blocking. Item (a) is in fact *partially served* by the bridge slice's negative tests for tampered artifacts (see §6 below), so doing P3.9 first reduces the eventual cost of the deferred harness.

### Lanes that should NOT be done first

- Implementing recommendation 2 from `handoff/third_party_p3_7_implementation_review.md` (malformed-scope exit-code semantics). That is a runtime fix and belongs in a separate, fresh micro-direction review with its own tiering. It is not blocked by P3.9 and P3.9 is not blocked by it.
- Promoting any `*/0.1-trial` schema. Out of scope for Gate C entirely.
- Module-runner CLI flag additions. The runner already has every flag P3.9 needs (`--policy-artifact`, `--run-id`, `--target`, `--target-type`, `--mode`, `--profile`, `--include-module-io-preview`, `--persist-preview-bundle`); the bridge slice adds zero new flags.

## 3. Approved Implementation Shape

### Smallest safe slice

**Add one offline test plus one design note. No runtime code edits to `recon.sh` or `module_runner.py`.**

Concrete shape:

1. New test file `scripts/test_recon_runner_bridge_dry_run.py`. Subprocess-driven offline `unittest`. For each positive/negative case:
   - Create a per-test `tempfile.TemporaryDirectory` as HACKLAB.
   - Install the existing `programs/_examples/sample-lab/scope.json` into `HACKLAB/programs/sample-lab/scope.json` (the same approach `test_recon_program_policy_dry_run.py` already uses).
   - Install a copy of the committed `modules/profiles/audit-baseline.json` and the committed `modules/checks/level1/*` module manifests into HACKLAB so the runner has discoverable manifests under the temp tree only.
   - Invoke `recon.sh --dry-run --program sample-lab --policy-mode planned <target>` in HACKLAB and assert a `policy_boundary_*.json` allow artifact is emitted.
   - Use the **test harness alone** to copy the emitted artifact to `HACKLAB/runs/<run_id>/policy/decision.json` (the bridge step).
   - Invoke `scripts/module_runner.py --policy-artifact <copied-path> --run-id <id> --target <same-target> --target-type <type> --mode dry-run --discover-root <HACKLAB> --json` and capture its JSON output.
   - Assert `verdict == "allow"`, `plan.status == "planned"`, `plan.policy.decision == "allow"`, `plan.execution.dry_run == True`, `plan.execution.target_touching == False`, and no module status is anything other than `planned`.

2. Optional design note `docs/recon_runner_bridge_design.md` (or a section appended to existing module-runner documentation under `scripts/README.md`) that:
   - Documents the artifact path translation explicitly as "performed by the operator or test harness, never by runtime code in P3.9."
   - Lists the runtime emission points (recon) and consumption points (runner) without prescribing any auto-bridge.
   - Names the fields each side validates and reaffirms the dry-run-only boundary.

3. Rolling/named handoff artifacts:
   - `handoff/cowork_p3_9_direction_review.md` (this file).
   - `handoff/claude_code_task_p3_9.md` for the implementation slice (named).
   - `handoff/claude_code_result_p3_9.md` for the implementation summary (named).
   - Rolling `handoff/claude_code_task.md`, `handoff/claude_code_result.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md` updates.

### Maximum file list (hard cap, do not exceed)

The approved slice may touch only:

- `scripts/test_recon_runner_bridge_dry_run.py` (new, ≤600 lines including assertion helpers — match the structure already used by `test_recon_program_policy_dry_run.py`)
- `docs/recon_runner_bridge_design.md` **OR** an append-only section in `scripts/README.md` (≤200 lines), not both
- `handoff/cowork_p3_9_direction_review.md` (this file)
- `handoff/claude_code_task_p3_9.md`
- `handoff/claude_code_result_p3_9.md`
- Rolling pointers: `handoff/claude_code_task.md`, `handoff/claude_code_result.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`
- Worker-emitted artifacts: `handoff/claude_code_impl_run_*.json`, `handoff/archive/rolling/*` (managed by `bin/hermes`/wrapper)

### Files that MUST stay byte-identical

- `recon.sh`
- `scripts/program_policy_boundary.py`
- `scripts/program_policy_check.py`
- `scripts/core/policy.py`
- `scripts/module_runner.py`
- `scripts/validate_module_io_bundle.py`
- `scripts/validate_module_io_contract.py`
- `scripts/validate_preview_manifest.py`
- `scripts/validate_preview_ledger.py`
- `scripts/validate_run_manifest.py`
- `scripts/profile_issues.py`
- `modules/checks/**`, `modules/profiles/**`, `modules/_schema/**`
- `config/scope.txt`, `config/recon.conf`
- `programs/_examples/sample-lab/scope.json` (re-use as-is)
- `programs/_examples/README.md`
- `bin/hermes`, `run_hermes_worker.ps1`

### May runtime files be edited?

**No.** Default is "no" and there is no strict justification for an exception in this slice. The bridge can be demonstrated entirely with the existing runtime surfaces. Any temptation to add even a one-line "convenience" flag to either tool should be rejected as a smuggled T4 change.

## 4. Safety Boundary

### Forbidden surfaces — explicit confirmation

The implementation slice must NOT introduce any of:

- target-touching activity (sockets, DNS, HTTP requests, subprocess of scanner binaries, OAST callbacks, webhooks, beacons, listeners, tunnels, proxy/pivot, brute force, fuzzing, exploit attempts);
- scanner execution (nuclei, nmap, naabu, subfinder, feroxbuster, httpx, dnsx, katana, ffuf, gobuster, sqlmap, etc.);
- module-runner execution beyond its existing dry-run preview path (i.e., the runner's `check.py` import/execution machinery — the runner already refuses to import module code; the bridge slice must not change that);
- live lab activation;
- real program scope file creation under `programs/<real-slug>/` (only `programs/_examples/sample-lab/` is allowed; the synthetic fixture is re-used);
- `config/scope.txt` mutation (the test must verify the file's sha256 is unchanged across the whole run, matching the pattern already used by `test_recon_program_policy_dry_run.py`);
- schema promotion of any `policy_boundary/1.0`, `policy_decision/1.0`, `run/1.0`, `module_input/1.0`, `module_result/1.0`, `preview_manifest/1.0`, `*/0.1-trial`, or other versioned artifact;
- report drafting, report submission, platform adapter, finding/evidence promotion to non-trial status, finding deduplication that crosses tool boundaries;
- scheduler/CI automation;
- credentials, OAuth, API keys, tokens, private keys, deployment, billing, or production-side configuration;
- changes to `_examples/` enforcement at `recon.sh` (the line-319 exclusion).

### `module_runner.py` invocation mode

The runner may be invoked **only in its existing dry-run preview mode** (`--mode dry-run`, the only mode it currently supports). The bridge test must not pass any other mode; the runner already errors on non-dry-run, but the test should explicitly fence this by using `mode="dry-run"` and asserting the runner's "supports dry-run mode only" error when negative cases probe `mode=planned` / `mode=live`.

### `recon.sh` invocation mode

`recon.sh` may be invoked **only with `--dry-run`** in tests, against synthetic `_examples/sample-lab` fixtures installed into a temporary `HACKLAB`. `--policy-mode planned` is allowed; `--policy-mode live` is allowed only as offline regression (the `--dry-run` flag preempts execution and is the binding gate). The test must:

- assert `--policy-mode live` paired with absence of `--dry-run` still errors (exit code 2) — this is already covered by lines 296–308 of `recon.sh` and we should not weaken that;
- never set or override `--skip-scope-check`;
- never set `config/scope.txt` to anything but its current committed value (sha256 fenced in `setUpClass`/`tearDownClass`).

## 5. OSS Recon Gate

### Review tier and milestone

Tier: T3. Milestone: Gate C — dry-run recon-to-runner bridge direction.

### Relevant references

1. **SARIF v2.1.0 (`runs`/`results`/`artifacts`/`rules` model).**
   - Useful pattern: SARIF defines `runs[].results[].locations[]` with explicit linkages between tool, run, rule, and artifact. Each `run` carries its own `tool`, `invocation`, and `artifacts` array, and results reference rule IDs that live in `tool.driver.rules`. The run boundary is *explicit* and is never auto-derived from another run's output.
   - Adopt / adapt / ignore: **adapt**. Preserve the principle that recon's policy boundary artifact and the runner's planned run manifest are two separate, separately-rooted documents linked only by explicit references (e.g., `plan.policy.decision_artifact_path`, `plan.policy.decision_sha256`). Do not collapse them into one document; do not introduce a "merged" interchange format in this slice.
   - Safety concern: SARIF allows `automationDetails.id` to chain runs; do not import that pattern as an excuse to auto-promote one tool's output into another tool's input. Path translation must remain explicit and operator-driven.
   - Contract impact: confirms current `plan.policy.decision_artifact_path` and `plan.policy.decision_sha256` are the right boundary. No schema change.

2. **DefectDojo engagement/test/finding model.**
   - Useful pattern: DefectDojo separates *engagement* (program/scope-level context), *test* (one tool run within an engagement), and *finding* (one issue within a test). The recon-side policy decision corresponds roughly to engagement-level authorization; the runner-side planned manifest corresponds to test-level scoping. Findings are *not* attached at engagement level.
   - Adopt / adapt / ignore: **adapt for terminology, ignore for storage.** Preserve the conceptual boundary (engagement ≠ test ≠ finding) in design notes. Do **not** introduce a DefectDojo-shaped storage layer in this slice; the runner's existing `runs/<run_id>/preview/*` directory layout is already sufficient and slimmer.
   - Safety concern: DefectDojo defaults to importing scanner outputs as findings; never adopt that default. Findings/evidence remain empty in P3.9 previews.
   - Contract impact: validates that `run/1.0` and `module_input/1.0` already model "test-level scoping" correctly. No new fields required.

3. **Nuclei workflows (chained templates with stage dependencies).**
   - Useful pattern: Nuclei workflows express stage chaining (`subdomain → http_probe → vuln_check`) with explicit per-stage matchers/extractors. Workflows make the chain visible in YAML rather than implicit.
   - Adopt / adapt / ignore: **ignore for execution; adapt only for the design note's narrative.** Nuclei workflows assume each chained step is *executed* against a target. The P3.9 bridge must adopt the opposite default: even when two stages are connected on paper, neither executes without an explicit operator decision and a separate T4 review.
   - Safety concern: nuclei workflows are the canonical example of "automatic chaining = automatic target-touching." Hard-coded ignore.
   - Contract impact: none. Inform the design note's wording about "chained but not executed" so future readers don't expect P3.9 to imply execution.

4. **OWASP ZAP context vs scan policy separation.**
   - Useful pattern: ZAP decouples *context* (where you are allowed to scan) from *scan policy* (which checks you are allowed to run). The two are loaded independently and the scanner errors if either is missing or contradictory.
   - Adopt / adapt / ignore: **adopt the separation principle.** Recon-side authorization (`program_policy_boundary.py` + `programs/<slug>/scope.json` + `config/scope.txt`) corresponds to context; runner-side profile (`modules/profiles/<profile>.json`) and module gates correspond to scan policy. The bridge must keep these decoupled: the runner re-verifies the policy artifact independently rather than trusting it implicitly, which is already the current behavior.
   - Safety concern: ZAP allows aggressive defaults via `--config`. Do not adopt aggressive defaults; both tools currently default to safe/no-op states.
   - Contract impact: validates the current dual-check design. No change.

5. **ProjectDiscovery pipeline conventions (`subfinder | httpx | nuclei`).**
   - Useful pattern: ProjectDiscovery tools chain over stdin/stdout JSON, with explicit per-tool contracts.
   - Adopt / adapt / ignore: **ignore for stdin/stdout chaining; adapt for explicit per-tool boundaries.** The recon-to-runner bridge uses *files-on-disk* under `runs/<run_id>/policy/`, not piped JSON. That is the correct choice because (a) the artifact must be re-readable for audit, (b) the SHA-256 fence in `plan.policy.decision_sha256` requires the artifact to exist at a stable path, and (c) piping invites accidentally chaining into network-touching downstreams.
   - Safety concern: ProjectDiscovery's defaults network-touch on first invocation. Hard-coded ignore.
   - Contract impact: justifies keeping artifact-on-disk over pipe-based design.

### Contract impact summary

- **Program scope**: unchanged. `programs/_examples/sample-lab/scope.json` re-used as-is. No new `programs/<slug>/` directory.
- **Policy decisions**: unchanged. Both sides already speak `policy_boundary/1.0` + `policy_decision/1.0`.
- **Finding schema**: unchanged. The bridge does not emit findings.
- **Evidence schema**: unchanged. The bridge does not emit evidence.
- **Run manifest**: unchanged. The bridge consumes the existing `run/1.0` planned shape.
- **Module manifest**: unchanged. Re-uses committed manifests under `modules/checks/level1/`.
- **Module profile**: unchanged. Re-uses `audit-baseline`.
- **Module I/O preview**: unchanged. The bridge test exercises the existing `--include-module-io-preview` path only as an optional positive assertion; bundle persistence (`--persist-preview-bundle`) is optional and remains the runner's existing offline write path.
- **Dry-run runner**: unchanged.

### Safety decision

- Offline-only preview possible: **yes**.
- Requires active behavior: **no**.
- Requires new policy gate: **no**.
- Requires schema migration: **no**.

### Implementation guidance

- Implement now: one test, one optional design note.
- Defer: any runtime bridge step in either tool; any auto-copy/auto-rename script; any wrapper that runs both tools together by default; any change to artifact filenames or directory layout in either tool.
- Tests required: see §6.
- Unsafe defaults to prevent: do not write or check a `runs/<run_id>/policy/` location *under the real repo*; the test must only operate inside a per-test `TemporaryDirectory`. Do not introduce a default `--auto-bridge` flag in either tool.

### Tier/milestone impact

- Escalation required: **no** for this design-only review and for the approved implementation slice. **Yes** for any runtime bridge work (T4).
- Can this gate cover later slices: **no.** This gate covers only the P3.9 tests/fixtures/docs slice. A fresh OSS Recon Gate is required for (a) any runtime bridge, (b) any change to either tool's artifact emission/consumption shape, (c) any P3.10+ slice that chains the runner's planned manifest into module execution.
- Re-review trigger if assumptions change: any of the "Files that MUST stay byte-identical" list (§3) is modified; any new flag is added to either tool; the artifact path/filename in either tool changes; the bridge test starts asserting against real targets or non-`_examples/` slugs.

## 6. Required Tests / Safety Assertions

The implementation slice must include the following focused tests. Group them in `scripts/test_recon_runner_bridge_dry_run.py` using the same `setUpClass`/`tearDownClass` sha256 fences and per-test `TemporaryDirectory` pattern as `scripts/test_recon_program_policy_dry_run.py`.

### Positive bridge assertions

1. **Allow path round-trip.** `recon.sh --dry-run --program sample-lab --policy-mode planned <synthetic-in-scope-url>` emits one `policy_boundary_*.json` with `boundary.status == "allow"`. Copy it to `runs/<run_id>/policy/decision.json` in the temp HACKLAB. Invoke `module_runner.py` with that artifact. Assert `verdict == "allow"`, `plan.status == "planned"`, `plan.policy.decision == "allow"`, `plan.execution.dry_run == True`, `plan.execution.target_touching == False`, and every entry in `plan.modules[*].status == "planned"`.

2. **Optional preview-bundle round-trip.** Repeat (1) with `--include-module-io-preview` on the runner side and assert `module_input_previews` and `module_result_previews` are returned with `dry_run == True`, `target_touching == False`, `status == "not_executed"`, `findings == []`, `evidence == []`. Do not require `--persist-preview-bundle` in this slice (it is supported but writing under `runs/` is unnecessary noise for a single assertion-focused test).

3. **Hash consistency.** Assert `plan.policy.decision_sha256 == sha256(copied-artifact-bytes)` and `plan.policy.decision_artifact_path == "runs/<run_id>/policy/decision.json"`.

### Negative bridge assertions (fail-closed)

4. **No scanner execution leakage.** In every positive and negative case, scan the captured combined recon stdout/stderr plus runner stdout/stderr for the absence of: `DRY: nuclei`, `DRY: nmap`, `DRY: subfinder`, `DRY: naabu`, `DRY: feroxbuster`, `DRY: curl -s https://crt.sh`, `Nmap scan report`, `[critical]`, `[high]`, `Open: `, `Found `. Re-use the helper structure from `test_recon_program_policy_dry_run.py`.

5. **No module execution leakage.** Assert no `check.py` import or subprocess affordance appears in runner output. Concretely: assert `plan.modules[*].status == "planned"`, `plan.execution.dry_run == True`, `plan.execution.target_touching == False`, and the runner's `verdict == "allow"` does not transition any module to `executed`/`running`/`completed`/`failed`.

6. **Target mismatch denied.** Take a valid recon-emitted artifact for target `https://a.test/`, copy it to `runs/<run_id>/policy/decision.json`, then invoke the runner with `--target https://b.test/`. Assert runner verdict is `deny` with an error message naming `policy artifact request.target must match requested target` or the corresponding decision-level error.

7. **Mode mismatch denied.** Take an artifact whose `request.mode == "planned"`, run the runner with `--mode dry-run` (the only supported mode); the runner currently only supports `dry-run`, so the test asserts the runner's mode mismatch deny when the artifact's `decision.mode` does not equal the runner's requested mode. (If the recon emission uses `mode == "planned"`, the test must either request that mode in the runner — which the runner will reject — or use a "dry-run" emission. Document which path the test exercises.)

8. **Hash drift denied.** Mutate a single byte of the copied artifact after recon emission. Assert runner verdict `deny` with an error naming `policy artifact schema_version` or `policy decision program_file_sha256 must be canonical sha256` (or whichever field fails first under the mutation).

9. **Path-outside-`runs/<run_id>/policy/` denied.** Place the copied artifact at `runs/<run_id>/other/decision.json` instead of `runs/<run_id>/policy/decision.json`. Assert the runner's `_policy_artifact_run_path` error: `policy artifact path must be under runs/<run_id>/policy/<file> and match run_id`.

10. **Helper failure denied.** Construct an artifact whose `helper.returncode == 1` or `helper.timed_out == true`. Assert the runner denies with `policy artifact helper.returncode must be 0 for allow` or `policy artifact helper.timed_out must be false for allow`.

11. **Audit event mismatch denied.** Construct an artifact whose `boundary.audit_event == "PROGRAM_POLICY_DENY"` (with status forced back to "allow"). Assert deny with `policy artifact boundary.audit_event must be PROGRAM_POLICY_ALLOW`.

### Filesystem/scope safety fences

12. **No `config/scope.txt` mutation.** Use the same `setUpClass`/`tearDownClass` sha256 fence pattern as `test_recon_program_policy_dry_run.py`. Snapshot the real `config/scope.txt` sha256 at start; re-verify at end.

13. **No real-repo `runs/` write.** Snapshot the list of files under the real-repo `runs/` directory at setup; re-verify identical at teardown. The test must only write under a per-test `TemporaryDirectory`.

14. **No real-repo `loot/`, `scans/`, `evidence/`, `reports/` write.** Same snapshot/teardown pattern.

15. **Reserved `_examples` slug stays rejected by `recon.sh`.** Already covered by `test_recon_program_policy_dry_run.py::test_reserved_examples_slug_is_rejected_by_recon`; assert the bridge test does not weaken this — i.e., the bridge test installs into a temp `HACKLAB/programs/sample-lab/`, not into the real repo's `programs/_examples/`.

### Operator-friendliness assertions

16. **Determinism.** Run the positive bridge test twice with different `--run-id` values; assert both succeed and produce the expected `plan.run_id` echoed. Determinism here is "no flaky timing" rather than "byte-identical output" (timestamps in the artifact will differ).

17. **No new CLI affordance.** Assert that the runner's `--help` and `recon.sh --help` outputs do **not** contain any new bridge-specific flag. (A simple `assertNotIn("--auto-bridge", help_text)` plus similar for `--from-recon`, `--bridge`, etc. This is a regression fence against accidental smuggling.)

## 7. Deferred Items and Re-Review Triggers

### Must remain deferred (do not implement in P3.9)

- Any runtime change to `recon.sh` that emits the boundary artifact directly into `runs/<run_id>/policy/<file>`.
- Any wrapper script that auto-copies recon emissions into the runner's expected path.
- Any auto-discovery flag in `module_runner.py` that locates a recent recon emission.
- Any change to `recon.sh` artifact filename convention (`policy_boundary_<ts>_<pid>_<nanos>_<target>.json`).
- Any module-runner change that consumes anything other than a `policy_boundary/1.0` allow artifact.
- Module execution (i.e., the runner actually importing and calling `check.py`). Remains deferred to Gate D/E.
- Finding/evidence emission. Deferred.
- Report drafting/submission, platform adapters, scheduler/CI hooks. Deferred.
- Live mode in either tool. Deferred to Gate E+ with operator approval.
- Schema promotion for `*/0.1-trial` artifacts. Deferred.
- Stale-artifact / target / mode / technique mismatch E2E harness as a *separate* file. The P3.9 negative tests cover a significant fraction; the standalone harness can remain deferred or be folded into a later T2/T3 slice.
- Implementation of the P3.7 third-party review's non-blocking recommendation 2 (malformed-scope exit-code semantics). Separate fresh micro-direction review.

### Triggers requiring a fresh T3/T4 review

- Any proposal to move the bridge path translation into runtime code in either tool.
- Any proposal to add a CLI flag in either tool that references the other tool's artifact layout.
- Any change to either tool's artifact filename, directory layout, or schema version.
- Any change to the runner's mode allowlist (currently `{"dry-run"}`).
- Any introduction of a new schema or contract version touched by either tool.
- Any expansion of the bridge test to use a non-`_examples/` slug, a real target, or `config/scope.txt`-listed scope entries.
- Any operator request to invoke either tool in live mode.
- Any future P3.10+ slice that proposes to consume the runner's planned manifest in a downstream execution path.

### Optional but recommended hardening (separate slices, not P3.9)

- A T1/T2 docs slice that updates `scripts/README.md` and/or `programs/_examples/README.md` to name the recon-runner bridge as a "demonstrated offline interoperability point, not a runtime coupling." Defer until after P3.9 lands and any review feedback is integrated.
- A T2 test slice that folds the deferred stale/mismatch E2E harness into a sibling test file. Defer until either (a) operator interest reopens it, or (b) a future runtime change to `recon.sh`/policy helpers requires it.

## Validation Performed for This Review

Design-only review; no code/runtime changes made by this artifact. Validation actions:

- Read `handoff/cowork_p3_9_direction_prompt.md` end-to-end.
- Read `handoff/program_policy_dry_run_closeout_20260519.md`, `handoff/active_strategy_queue.md`, `handoff/project_launch_estimate_20260519.md`, `handoff/third_party_p3_7_implementation_review.md`, `handoff/review_tiering_policy.md`, `handoff/multi_party_review_decision_policy.md`, `handoff/oss_recon_gate.md`, and the relevant portion of `.hermes.md` (loaded by harness context).
- Inspected `scripts/module_runner.py` end-to-end (1159 lines) to confirm the runner's `_validate_policy_artifact`, `_policy_artifact_run_path`, mode whitelist, and dry-run-only semantics.
- Inspected `recon.sh` policy emission path (`policy_decide`, `policy_validate_artifact`, `--policy-mode` argument handling, exit codes 2 and 3, `_examples/` exclusion at line 319) for shape compatibility with the runner's validator.
- Inspected `scripts/program_policy_boundary.py` decision contract validation (`_validate_decision_contract`, `_artifact_payload`, `_forced_deny_decision`, mode/technique enums).
- Inspected `scripts/test_module_runner.py` to understand the existing fixture-shaped `policy_artifact` payload and its compatibility with `recon.sh`'s actual emission.
- Inspected `scripts/test_recon_program_policy_dry_run.py` indirectly (via the closeout/review artifacts) for the per-test HACKLAB / sha256-fence pattern the bridge test should re-use.
- Cross-checked `scripts/README.md` for the runner's documented CLI surface.

No runtime code was executed; no scanners, modules, or targets were touched; no files outside this review artifact and the rolling worker result were modified.

## Final Decision Block

```text
Decision: APPROVE_WITH_CHANGES
Tier: T3 design-only direction review; approved implementation slice is T2 (tests/fixtures/docs only) but inherits this T3 review's OSS Recon Gate
Milestone: Gate C — dry-run recon-to-runner bridge direction
Hermes authority: conditional — Hermes may accept the implementation slice after independent implementation/safety review confirms no runtime change, no live affordance, no new CLI flag in either tool, and all required negative tests pass; otherwise escalate
Reviewers consulted:
- Claude Code Impl direction review pass (this artifact); visible model/runtime: claude-opus-4-7 per Claude Code CLI default; underlying Anthropic serving runtime not exposed at the tool surface
Validation performed:
- read prompt + all referenced source-of-truth handoff artifacts
- read scripts/module_runner.py (full), recon.sh policy emission path, scripts/program_policy_boundary.py, scripts/test_module_runner.py policy_artifact fixture, scripts/README.md runner row
- design-only; no scanners, modules, targets, runtime files, schemas, or config touched
Blocking findings:
- none, conditional on the §3 maximum file list and §3 byte-identical list being honored
Non-blocking recommendations:
- prefer appending a section to scripts/README.md over creating docs/recon_runner_bridge_design.md, to minimize artifact sprawl
- include a regression assertion that neither tool's --help mentions a bridge flag (§6 item 17), to fence accidental scope creep
- defer the stale/mismatch standalone E2E harness; the P3.9 negative tests cover the most valuable subset
Safety boundary:
- offline/local only; dry-run only in both tools; no real targets; only programs/_examples/sample-lab/ fixtures; no config/scope.txt change; no real-repo runs/ writes; no module execution; no new CLI affordance; no schema promotion
OSS Recon Gate: attached (§5)
User approval required: no for the approved tests/fixtures/docs slice; yes before any T4 runtime bridge follow-up, live-mode use, or real-program onboarding
```
