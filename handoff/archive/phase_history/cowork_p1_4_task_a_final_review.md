> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Final Re-Review — P1-4 Task A CLI Surface

**Verdict: ACCEPT**

Note: `handoff/cowork_p1_4_task_a_final_review.md` exists but is **0 bytes / empty** — there is no prior "final review" content to verify against; this output IS that final review.

## Blocking issues

None.

## Verification of the four checkpoints

1. **Warning placement** — `recon.sh:310` fires at the **end** of `validate_program_flags`, immediately before `PROGRAM_SCOPE_FILE="$program_real"` at `:311`. This is exactly the cleaner placement recommended as non-blocking #1 in `cowork_p1_4_task_a_rereview.md` — it now runs only after slug regex, mode validation, dry-run coupling, dir/file existence, regular-file/readable checks, realpath resolution, prefix containment, and reserved-dir rejection have all passed. No spurious warn on exit-1 paths. The no-`--program` early-return at `:248-251` is untouched, so §4.5 byte-identical contract still holds.

2. **Lowercase `--policy-mode` test** — `scripts/test_recon_program_cli.py:148-152` (`test_policy_mode_is_case_sensitive`) asserts `--policy-mode DRY-RUN` → exit 2 + message `"--policy-mode must be lowercase"`. Pairs correctly with the single-bracket `[ "$POLICY_MODE" != "${POLICY_MODE,,}" ]` check at `recon.sh:274-277` (POSIX test bypasses the global `shopt -s nocasematch` at `:14`). Closes rereview non-blocking #2.

3. **Planned/live dry-run tests** — `test_planned_and_live_modes_are_accepted_with_dry_run` at `:132-146` subtests both `planned` and `live` combined with `--dry-run`, asserting exit 0, presence of the not-wired warn, and absence of `POLICY_` rows. Locks in §4.1 (planned/live may combine with `--dry-run`).

4. **Task A scope discipline** — `git diff` is limited to `recon.sh` (CLI state vars + `resolve_existing_path` + `validate_program_flags` + call site, plus help text), `handoff/codex_review.md` (Task A section), `handoff/codex_task.md` (rewrite to Task A brief). New file: `scripts/test_recon_program_cli.py`. **No** `scripts/program_policy_boundary.py`, **no** call to `scripts/program_policy_check.py` from `recon.sh`, **no** `policy_decide` / `policy_env_preflight` / evidence dirs, **no** per-stage gates, **no** rate-limit composition, **no** CIDR policy wiring, **no** `safe_target` changes, **no** edits to `config/scope.txt`, `config/recon.conf`, real `programs/<slug>/scope.json`, `programs/_schema/*`, scheduler, reports, `accepted_changes.md`. Matches every declared non-goal.

## Safety assessment

- `safe_target`, `validate_scope_file`, `REQUIRE_SCOPE_CHECK=false` rejection, and `--skip-scope-check` token discipline remain untouched.
- Symlink escape, path traversal, reserved-dir resolution, uppercase-slug bypass, and uppercase-policy-mode all fail closed (exit 1 or 2 with explicit messages).
- Tests use a temp `HACKLAB` and synthetic `authorized.test` only; every CLI test passes `--dry-run`; no network, no scanner, no Python helpers invoked from `recon.sh`.
- The "operator runs `--program X --policy-mode live` thinking program policy is enforcing" UX risk is mitigated by the warn — now correctly placed so it only fires on a fully-validated `--program` invocation.

## Remaining non-blocking items (carry into Task B)

1. Redundant slug guards at `recon.sh:258-265` are unreachable under the regex at `:254`. Add a `# defense in depth` comment, or fold into Task B's regex maintenance.
2. `case "$program_real" in "$programs_real"/*)` at `:297-300` is glob-pattern, not literal. Rewrite as `[[ "$program_real" == "$programs_real"/* ]]` for robustness against any future `HACKLAB` containing glob metacharacters. Currently low-risk.
3. **Directory-level** symlink test (`programs/<slug>` itself a symlink outside `programs/`) not covered — only file-level symlink at test:219-238. One extra subtest.
4. `--policy-mode planned|live` **without** `--dry-run` is not asserted as parsing-valid. The current planned/live tests include `--dry-run`; a paired test without `--dry-run` would lock in the §4.1 contract for Task B.
5. Test temp dirs created under `REPO_ROOT` (`scripts/test_recon_program_cli.py:59`) — couples suite to a writable repo. Functional but not ideal.
6. Empty `{}` program fixture lacks a "Task A does not validate JSON content; Task B will" comment.

## Recommended next step

Hermes may append the Task A acceptance row to `handoff/accepted_changes.md` and proceed to Task B scoping. The empty `handoff/cowork_p1_4_task_a_final_review.md` should either be deleted or be filled with this review content before committing. Operators must continue to avoid `recon.sh --program … --policy-mode {planned,live}` against non-lab targets until Task B's per-stage gating lands — the warn now makes that constraint visible at run time.
