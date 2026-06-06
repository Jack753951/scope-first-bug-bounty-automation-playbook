> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 3 Cleanup / Technical Debt / Deferred-Ideas Register

Status: pre-Phase-4A cleanup synthesis
Date: 2026-05-20
Prepared by: Hermes
Scope: documentation synthesis only; no runtime, scope, scanner, module, report, credential, scheduler, or target behavior changed

## Answer

Not everything was implemented or deleted.

What was done before Phase 4A:

1. Process problems that were blocking safe continuation were fixed or governance-controlled.
2. Several technical-debt items were either hardened with tests or explicitly closed.
3. Several over-scoped / premature ideas were deliberately deferred rather than implemented.
4. Remaining gaps were carried forward as Phase 4A blockers instead of being hidden.

So the accurate status is:

**Core cleanup was done enough to close Phase 3 as an offline/dry-run MVP, but not all deferred ideas or technical debt were eliminated. The unresolved items are now tracked as deferred lanes or Phase 4A activation blockers.**

## Cleanup / process issues already handled

### 1. Rolling handoff overwrite risk

Problem:

- Rolling files such as `handoff/cowork_task.md`, `handoff/claude_code_task.md`, and worker result files could overwrite previous important context.

Handled:

- `bin/hermes` was updated to archive previous non-empty rolling handoff files under `handoff/archive/rolling/`.
- Audit-important slices now also get named artifacts such as `handoff/claude_code_task_p3_6.md` / `handoff/claude_code_result_p3_6.md`.

Status: handled.

### 2. Worker route / model visibility confusion

Problem:

- Implementation routing needed to visibly consume Claude Code MAX/OAuth, while Codex remained fallback/surgical.
- Reviews needed route/model/runtime labels where available.

Handled:

- `claude-impl` worker route added.
- Usage JSON artifacts added under `handoff/claude_code_impl_run_<timestamp>.json`.
- Handoff summaries now record route/tool and visible model/runtime when exposed.

Status: handled, with limitation that delegated subagent child runtime is not always exposed.

### 3. Over-heavy review process / micro-slice fatigue

Problem:

- Some small slices consumed high Claude Code turn counts and heavy review effort.

Handled:

- Review tiering / milestone governance adopted.
- Multi-party review decision gate adopted.
- Active strategy queue introduced to prevent rereading the full history every time.
- T1/T2 work can use lighter review inside already-reviewed boundaries.

Status: governance handled; still needs discipline in future slice sizing.

### 4. Worker max-turn / timeout caveats

Problem:

- P3.9 and P3.12 hit Claude Code max-turn or parent timeout constraints.

Handled:

- Hermes completed cleanup/verification locally where boundary allowed.
- Caveats were recorded in named result files.
- Active queue records temporary one-off turn-budget convention and recommends splitting broad slices.

Status: operationally handled; future broad fixture/handoff slices should be split tighter.

### 5. Git-Bash / Windows workflow quirks

Problem:

- Git-Bash/MSYS path and shell behavior can break PowerShell-style assumptions.
- Markdown/backtick PR comments can be shell-mangled.

Handled:

- Project context and workflow docs now require Git-Bash-safe command style and `gh pr comment --body-file` for Markdown/backtick comments.

Status: handled as workflow rule.

## Technical debt fixed or hardened

### 1. `_examples/automation_permitted: true` ambiguity

Problem:

- `_examples/` fixtures could be misread as real authorization.

Handled:

- Added documentation clarifying `_examples/` is examples/offline regression only.
- `automation_permitted: true` under `_examples/` is test-only and never live authorization.

Status: fixed.

### 2. Program-policy malformed-scope exit semantics

Problem:

- Malformed program scope / policy boundary failures needed clearer fail-closed exit behavior.

Handled:

- `recon.sh` reserves exit code `3` for program-policy boundary/config errors.
- Valid policy denies remain normal no-work outcomes.
- Tests updated.

Status: fixed/hardened.

### 3. CIDR forced-deny coverage

Problem:

- Literal CIDR handling needed end-to-end dry-run denial coverage.

Handled:

- Added tests proving CIDR without explicit allow is policy-denied and no scanner plan leaks.

Status: fixed/hardened.

### 4. Recon-to-runner dry-run artifact bridge confidence

Problem:

- Needed evidence that recon dry-run policy artifacts can feed runner preview safely.

Handled:

- Added tests-only bridge harness.
- Added hash-drift/tampered-copied-artifact denial.
- Added explicit comment that test harness path translation must not become runtime copy behavior.
- Later P3.10 added narrow explicit direct-read support with path, shape, symlink, outside-root, and provenance checks.

Status: hardened inside dry-run/direct-read boundary.

### 5. Module runner discovery confidence

Problem:

- Need confidence that module discovery/profile planning remains data-only and does not import or execute module code.

Handled:

- Added two-module discovery coverage.
- Added runner-indifference tests for `check.py` presence/absence.

Status: fixed/hardened.

### 6. Candidate workflow expected terminal states

Problem:

- Curated fixtures needed explicit expectations across packet/gap/verification/readiness states.

Handled:

- Added terminal-state expectation matrix.

Status: fixed/hardened.

### 7. SOC reviewer-gap vocabulary drift

Problem:

- P3.12 implementation review initially found asymmetric drift-lock coverage.

Handled:

- Hermes added AST-based exact vocabulary/status drift-lock assertions.
- Follow-up independent review returned PASS.

Status: fixed.

## Deferred / rejected / parked ideas

These were not forgotten; they were intentionally not implemented before Phase 4A.

### 1. Reviewer-notes artifact / reviewer-answer capture

Reason deferred:

- Current periodic review template is sufficient for now.
- A new artifact/consumer would create a fresh platform boundary.

Current status:

- Deferred behind future direction review.

### 2. Fifth stdin consumer / shared offline consumer helper extraction

Reason deferred:

- Duplication exists across trial consumers, but centralizing too early could weaken per-script safety review.
- Trigger is later schema promotion or observable drift.

Current status:

- Deferred.

### 3. Schema promotion for `*/0.1-trial` documents

Reason deferred:

- Trial workflow still needs lab calibration and real evidence lessons first.

Current status:

- Deferred; no schema promotion approved.

### 4. Formal manifest/profile risk-field promotion

Reason deferred:

- P3.14 decided not to promote new formal fields yet.
- P3.15 only produced documentation crosswalk / design memory.

Current status:

- Deferred; future fields remain non-contractual.

### 5. SOC trial-consumer design

Reason deferred:

- SOC evidence bucket and reviewer-gap catalog are useful calibration artifacts, but a consumer would create a new runtime/reporting boundary.

Current status:

- Deferred behind fresh T3 direction review.

### 6. Automated recon-to-runner coupling

Reason deferred:

- Current P3.10 only allows explicit direct-read of a policy artifact.
- Auto-discovery, auto-copy, scheduler/CI linkage, scanner/module execution, finding/evidence promotion, or report pipeline would cross T3/T4/T5 boundaries.

Current status:

- Deferred.

### 7. Scanner-output importer / exporter boundary

Reason deferred:

- Needs real lab lessons, evidence redaction model, and report-readiness quality criteria first.

Current status:

- Deferred.

### 8. Real evidence locator / redaction gate driven by scanner outputs

Reason deferred:

- Real scanner output can contain secrets, cookies, tokens, request/response bodies, and loot-like data.
- Needs lab calibration and explicit minimization rules.

Current status:

- Deferred; Phase 4A blocker.

### 9. Report drafting / report submission adapters

Reason deferred:

- Current platform is candidate/readiness oriented, not confirmed-finding/report-submission oriented.
- Human verification and evidence quality must mature first.

Current status:

- Deferred.

### 10. Real bug-bounty program activation

Reason deferred:

- Must pass controlled lab calibration first.
- Requires program scope/rules, allowed techniques, operator approval, and T4/T5 gate.

Current status:

- Deferred until Phase 4C/5.

## Remaining activation blockers before touching a lab

These are intentionally still open. They block Phase 4A target-touching until resolved:

1. Exact lab target and scope are not selected yet.
2. Narrow lab scope artifact does not exist yet.
3. T4/T5 activation-boundary review has not approved the exact lab behavior.
4. Runtime deny-by-default tests for non-lab/public targets must be written before activation.
5. Rate limits, timeouts, kill switch, stop conditions, rollback/cleanup, and audit trail must be documented and tested.
6. Real-output evidence redaction/minimization is not ready.
7. Candidate findings cannot become confirmed findings without human verification.
8. Report drafting/submission remains deferred.
9. Real bug-bounty program scope/rules and platform adapters remain out of scope.
10. Scheduler/CI target-touching automation remains blocked.

## Small hygiene still recommended before a formal release bundle

These are not blockers to planning Phase 4A, but should be handled before a formal commit/release bundle:

1. Run local dry-run demo checklist from `handoff/phase3_dry_run_local_mvp_closeout_20260520.md`.
2. Run final local validation:

```bash
git diff --check
USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review
```

3. Clean or intentionally preserve unrelated untracked artifacts.
4. Record dry-run demo results if the operator wants a formal acceptance bundle.

## Conclusion

Phase 3 cleanup was sufficient for a safe milestone closeout, but it was not a blanket "all debt gone" cleanup.

The project is now in this state:

- fixed/hardened: process overwrite risk, route visibility, review governance, examples ambiguity, policy exit semantics, CIDR denial coverage, dry-run bridge safety tests, runner data-only confidence, SOC drift-lock blocker;
- deferred deliberately: schema promotion, reviewer-notes artifact, shared consumer helper extraction, SOC consumer, scanner importers, evidence redaction from real outputs, report adapters, automated recon-to-runner coupling, real bug-bounty activation;
- still required before lab touch: exact target/scope, T4/T5 activation review, deny-by-default tests, rate/timeout/kill/audit controls, evidence minimization plan, explicit operator approval.
