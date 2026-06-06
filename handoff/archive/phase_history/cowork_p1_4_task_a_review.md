> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

I have all the context needed. Writing the independent review now.

# Cowork Review — P1-4 Task A CLI Surface

Verdict: **ACCEPT** (with non-blocking recommendations and one safety-UX item to address before Task B reaches operator hands)

## Blocking issues

None. The implementation matches the Task A scope from `handoff/codex_task.md` and the §4.1 / §4.5 / §5.3 contract from `handoff/cowork_p1_4_proposal.md`. All declared non-goals (boundary helper, `policy_decide`, per-stage gates, rate-limit composition, evidence artifacts, `safe_target` changes) were respected. `recon.sh:245-307` is the only real surface added, and it is fenced cleanly behind `[[ -z "$PROGRAM_SLUG" ]]`.

Verified specifically:
- Slug regex `^[a-z0-9][a-z0-9-]{0,62}$` is enforced (`recon.sh:254`) and uppercase rejection is handled defensively via `${PROGRAM_SLUG,,}` compared with `[ … != … ]` — important because `shopt -s nocasematch` is set globally at `recon.sh:14`, which would otherwise let `BadSlug` pass the regex.
- `--program` ↔ `--skip-scope-check` mutual exclusion fires before the override-token logic (call ordering at `recon.sh:320-335`).
- `--policy-mode dry-run` requires `--dry-run` (`recon.sh:278-281`); `planned`/`live` may combine with `--dry-run`.
- Symlink/path escape is caught by `resolve_existing_path` + literal prefix check (`recon.sh:291-296`), with fail-closed when neither `realpath` nor `readlink -f` is available.
- `programs/_examples` / `programs/_schema` are blocked at the resolved-path level (`recon.sh:298-304`) — the real safety check; the slug-name check at `:258` is dead code under the regex but harmless.
- No-`--program` runs are byte-identical: the early-return at `recon.sh:248-251` ensures zero new stdout/stderr/audit/file behavior, and `scripts/test_recon_program_cli.py:109-115` asserts the audit log contains no `POLICY_` rows.

## Non-blocking recommendations

1. **Add a `warn` when `--program` is supplied but policy is not yet wired.** With Task A merged and Task B not yet shipped, `recon.sh --program p --policy-mode live target` will pass validation, run all stages, and never consult `programs/p/scope.json`. The operator likely believes program policy is enforcing — it isn't. A single `warn "--program accepted; per-stage policy gating arrives in P1-4 Task B (not wired)"` immediately after `validate_program_flags` would close the false-sense-of-security gap without violating §4.5 (which only constrains the no-`--program` path). I recommend folding this into Task B's plan as a "must land before Task A is exercised against any non-lab target."

2. **`nocasematch` leaks into `--policy-mode` validation.** Both `case "$POLICY_MODE" in dry-run|planned|live)` (`:274`) and `[[ "$POLICY_MODE" == "dry-run" ]]` (`:278`) accept uppercase forms (`DRY-RUN`, `LIVE`) because of `shopt -s nocasematch` at `:14`. The downstream behavior is still safe (the dry-run ↔ `--dry-run` requirement still fires for `DRY-RUN`), but the surface is inconsistent with the documented enum. Either lowercase `POLICY_MODE` once after parse, or wrap the validation in a local `shopt -u nocasematch` / restore.

3. **Redundant guards in slug validation.** The `*"/"*`, `*"\\"*`, `*".."*`, `[[:space:][:cntrl:]]`, leading `.`/`-`, and `_examples`/`_schema` checks (`:258-265`) are all unreachable under the prior regex. Defense in depth is fine, but a one-line comment marking them as such would prevent a future maintainer from "simplifying" the regex and accidentally weakening the wall.

4. **`case "$program_real" in "$programs_real"/*` is glob-pattern matching.** If `HACKLAB` ever resolves through a path containing glob metacharacters (`*`, `?`, `[`), the prefix check becomes a pattern match rather than a literal match. Vanishingly unlikely for this repo but worth a `[[ "$program_real" == "$programs_real"/* ]]` rewrite or a `case` pattern that explicitly anchors with quoted literals.

## Testing gaps

- **Directory-level symlink not tested.** `scripts/test_recon_program_cli.py:196-215` only covers `programs/<slug>/scope.json` being a symlink. A test where `programs/<slug>` itself is a symlink to outside `programs/` would exercise the same realpath check from a different angle and is one extra subtest.
- **`--policy-mode planned|live` without `--dry-run` is not asserted.** This is the path most likely to be exercised by an operator post-Task-A; a test pinning that it parses as valid (and currently runs without policy enforcement) would lock in the contract for Task B.
- **`--policy-mode planned --dry-run` combination not covered** (proposal §4.1 says it must be allowed).
- **Case-sensitivity of `--policy-mode` not covered** — see recommendation #2.
- **Tests place temp dirs under `REPO_ROOT`** (`scripts/test_recon_program_cli.py:59`). Functional, but couples the suite to a writable repo. Not blocking.
- **Empty `{}` program file is accepted** as the test fixture. Task A doesn't read content (correct), but a comment in the test explaining "Task A does not validate JSON content; Task B will" would help future readers.

## Safety/authorization assessment

- `safe_target` semantics, `validate_scope_file`, `REQUIRE_SCOPE_CHECK=false` rejection, and `--skip-scope-check` token discipline are all untouched.
- No call to `scripts/program_policy_check.py`, `scripts/core/policy.py`, or any Python from `recon.sh`. No `policy_decide`, `policy_env_preflight`, or evidence directory creation. Matches Task A non-goals.
- No edits to `config/scope.txt`, `config/recon.conf`, real `programs/<slug>/scope.json` files, `programs/_schema/*`, scheduler/deployment, reports, loot, logs containing secrets, or `accepted_changes.md`. Confirmed against `git diff --stat` (only `recon.sh`, `handoff/codex_review.md`, `handoff/codex_task.md` modified; only `scripts/test_recon_program_cli.py` added by Codex).
- Tests use synthetic `authorized.test` targets and temp `HACKLAB` only. No external DNS, no network tools, no scanner invocation. `--dry-run` enforced in every CLI test.
- Symlink escape, path traversal in slug, reserved-directory targeting, and uppercase-slug bypass all fail closed.
- **One residual safety-UX risk:** `--program … --policy-mode live` currently passes validation and then runs live stages with *only* the global `safe_target` gate. The operator-facing implication of this needs a warn (recommendation #1) or Task B must land before Task A is exposed beyond a lab.

## Architecture/roadmap assessment

- `PROGRAM_SCOPE_FILE`, `POLICY_MODE`, `ALLOW_CIDR` state vars are pre-staged correctly for Task B to consume; no rework will be needed.
- `validate_program_flags` is positioned correctly inside `validate_runtime_flags` (called before the skip-scope-check token logic), preserving the proposal's gate ordering.
- `resolve_existing_path` is small, single-purpose, and reusable for the upcoming `policy_env_preflight` SHA-256 + path checks in Task B.
- The split between slug syntax (`exit 2`, CLI usage error) and file-existence/path-resolution (`exit 1`, runtime authorization error) matches the convention `recon.sh` already uses elsewhere — good for operators reading audit logs.
- Task B can add `policy_env_preflight` and `policy_decide` calls, plus the `filter_safe_and_policy_targets` wrapper, without restructuring `validate_program_flags` or `parse_args`. The seam is clean.
- Minor maintainability concern: the regex-vs-explicit-checks duplication (recommendation #3) will get harder to reason about once Task B adds more checks.

## Recommended next step

**Accept Task A as-is; queue the warn-when-not-wired safeguard (non-blocking #1) as the first item of Task B before any per-stage gating lands**, and during Task B implementation also resolve the `nocasematch` leak (#2). Hermes should append the Task A acceptance row to `handoff/accepted_changes.md` (per task spec it was deliberately not appended by Codex). After acceptance, ensure no operator runs `recon.sh --program … --policy-mode {planned,live}` against non-lab targets until Task B is merged — the validation accepts the flags but the program scope file is not yet consulted.
