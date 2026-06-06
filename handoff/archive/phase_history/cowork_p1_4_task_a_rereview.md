> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Re-Review — P1-4 Task A (Hermes follow-up)

## Verdict: **ACCEPT**

The two follow-up changes correctly address non-blocking recommendations #1 (warn) and #2 (nocasematch leak) from `handoff/cowork_p1_4_task_a_review.md`. No new blockers introduced.

## Blocking issues

None.

## Verification of the two changes

**1. Warn at `recon.sh:287`** — fires only after the no-`--program` early-return at `:248-251`, so the §4.5 byte-identical contract for runs without `--program` is preserved. `warn` is the standard `_log "WARN"` helper (`recon.sh:106`) already used elsewhere; no audit/file side effects, no `POLICY_` row emission, no scanner state change. Message accurately describes the gap operators were previously unaware of.

**2. Lowercase `--policy-mode` check at `recon.sh:274-277`** — uses single-bracket `[ ... ]` (POSIX test), which correctly bypasses the globally-set `shopt -s nocasematch` at `:14`. `"DRY-RUN"` now exits 2 with the documented enum error before reaching the case statement at `:278-281`. The slug-side analog at `:254` (`[ "$PROGRAM_SLUG" != "$slug_lower" ]`) also uses single-bracket test, so both surfaces are consistent.

Ordering check (all clean):
- `--policy-mode` without `--program` still rejected first (`:249`).
- Lowercase enforcement runs before the case enum (`:274` then `:278`), so mixed-case never reaches nocasematch-affected pattern matching.
- Warn fires after all syntactic/mode validation but before path-existence checks, which means a user with a valid slug + missing scope file will see both WARN + ERR before exit 1. Informational only; not a blocker.

## Remaining non-blocking items

1. **Warn placement** — emitted before path existence checks at `:292-310`, so it prints even on runs that then fail with exit 1 (missing/unreadable/escaping scope file). Cleaner placement is at the end of `validate_program_flags`, just before `PROGRAM_SCOPE_FILE="$program_real"` at `:312`, so the warn only fires on a fully-validated `--program` run. Style nit; the current placement is still correct and informational.
2. **No new test for the lowercase `--policy-mode` enforcement.** Recommendation #2 had a paired test gap ("Case-sensitivity of `--policy-mode` not covered"); the enforcement landed without a paired assertion in `scripts/test_recon_program_cli.py` (no test changes in this diff). Should be covered when Task B's tests land — locking in that `--policy-mode DRY-RUN` exits 2 with the documented error message protects against future regressions if the `nocasematch` global is ever moved.
3. The prior review's other non-blocking items (#3 redundant slug guards, #4 glob-metachar `case` prefix, directory-symlink test, `--policy-mode planned|live` without `--dry-run` test, `--policy-mode planned --dry-run` test, temp-dir-under-`REPO_ROOT` coupling) are unchanged by this delta. Carry forward as previously assessed.

## Safety assessment

- `safe_target`, `validate_scope_file`, `REQUIRE_SCOPE_CHECK=false` rejection, and `--skip-scope-check` token discipline still untouched.
- No call into `scripts/program_policy_check.py`, `scripts/core/policy.py`, or any Python helper from `recon.sh`. Matches Task A non-goals.
- No edits to `config/scope.txt`, real program scope files, `programs/_schema/*`, scheduler/deployment, reports, loot, audit logs, or `accepted_changes.md`. `git diff --stat` is limited to `recon.sh`, `handoff/codex_review.md`, `handoff/codex_task.md`.
- No-`--program` runs remain byte-identical: empty-slug branch returns at `:251` before either the warn or the new lowercase check; existing assertion at `scripts/test_recon_program_cli.py:109-115` still holds.
- The residual "operator runs `--program X --policy-mode live` without per-stage gates" safety-UX risk from the prior review is now mitigated by the warn — operator sees explicit notice that only `safe_target` is enforcing.

## Recommended next step

Hermes should append the Task A acceptance row to `handoff/accepted_changes.md` and proceed to scope Task B. During Task B, fold in: (a) the warn-placement move to end-of-function, (b) the paired test for uppercase/mixed-case `--policy-mode` rejection, and (c) the directory-symlink and `--policy-mode planned|live`-without-`--dry-run` tests deferred from the first review. Operators must still avoid `recon.sh --program ... --policy-mode {planned,live}` against non-lab targets until Task B's per-stage gating lands.
