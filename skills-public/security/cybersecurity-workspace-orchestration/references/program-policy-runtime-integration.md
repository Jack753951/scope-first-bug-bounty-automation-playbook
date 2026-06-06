> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Program Policy Runtime Integration Pattern

Use this reference when moving an offline program-scope policy helper into recon/runtime automation. It captures the P1-4 design-review lessons from a cybersecurity lab workflow and should be treated as a reusable default-deny integration pattern, not a one-off task log.

## Phase Shape

Do not jump from an offline policy helper directly into full recon-stage wiring. Split runtime integration into small reviewable phases:

1. CLI surface only
   - Add flags such as `--program <slug>`, `--policy-mode {dry-run,planned,live}`, and optional CIDR posture flags.
   - Enforce strict slug/path restrictions before any helper is called: lowercase slug only (for example `^[a-z0-9][a-z0-9-]{0,62}$`), no `/`, `\\`, `..`, whitespace/control chars, leading `.`, leading `-`, reserved directories such as `_examples`/`_schema`, or path-like values.
   - Resolve the program file only as `$PROJECT/programs/<slug>/scope.json`; require an existing readable regular file, resolve symlinks/realpaths, reject anything outside `$PROJECT/programs/` or inside reserved schema/example directories, and reject same-tree aliasing by requiring the resolved relative path to equal exactly `<slug>/scope.json` (not another program's scope via symlink).
   - Make `--program` incompatible with scope-bypass flags such as `--skip-scope-check`; program policy is additive, not a reason to bypass global scope.
   - Require explicit `--policy-mode` whenever `--program` is present, reject `--policy-mode` without `--program`, and force lowercase values so shell options such as `nocasematch` cannot accidentally accept `DRY-RUN`/`LIVE`.
   - Require `--policy-mode dry-run` to be paired with runtime `--dry-run`; planned/live may be accepted in dry-run for validation, but dry-run policy must never authorize target-touching execution.
   - If CLI flags are accepted before per-stage gates are wired, print/audit a clear warning that the CLI is inert and only the existing global target gate is active.
   - Preserve no-program behavior as byte-identical zero side-effect behavior.
   - Add regression tests proving no new stdout/stderr, audit rows, Python checks, helper calls, or artifact files occur without `--program`.
2. Boundary wrapper
   - Add a jq-free Python stdlib wrapper around the offline helper.
   - Handle subprocess timeout, JSON parsing, schema/contract validation, and atomic artifact writes.
   - Return simple shell-readable status to bash instead of making bash parse nested JSON.
3. Per-stage integration
   - Only after CLI and boundary wrapper review, connect each runtime stage/target to fresh policy decisions.
   - Add stage-specific negative tests before broad rollout.

## Safety Invariants

- `safe_target` or equivalent global scope allowlist remains the first gate.
- Program policy is an additional deny gate, never a replacement for global scope checks.
- Both gates must pass before any target-touching tool invocation.
- No cached allow decisions: every target/stage/technique decision is fresh.
- Program `out_of_scope` precedence and global+program intersection remain binding.
- Unknown schema, unsupported technique, missing/invalid policy output, timeout, or boundary parse error defaults to deny.

## Policy Mode Rules

- `--program` should be opt-in.
- `--policy-mode` should be explicit whenever program policy is enabled.
- `--policy-mode dry-run` must only be accepted with the runtime dry-run flag; it must not authorize real target-touching execution.
- Target-touching execution should require `--policy-mode planned` or `--policy-mode live`, with stricter checks such as automation permission, valid testing window, and no active blackout.

## Vocabulary And Contract Discipline

Before implementation, reconcile technique names with the existing schema enum. Do not introduce fake or review-only techniques into decision artifacts unless they are formally added to the schema.

Common pitfalls:

- `dir_bruteforce` vs `directory_bruteforce` style drift.
- Adding notification/webhook/policy-preflight techniques without schema support.
- Using nonexistent rate-limit keys from the schema.
- Letting initial prechecks write decisions before evidence/artifact directories exist.
- Allowing no-program paths to emit harmless-looking audit or log lines; these still break zero-side-effect compatibility.

If an environment preflight is needed, make it a non-decision check (for example `policy_env_preflight`) and do not emit a `policy_decision/1.0` allow for it.

## Boundary Wrapper Contract

Prefer a wrapper like `scripts/program_policy_boundary.py` that:

- Calls the offline helper, e.g. `scripts/program_policy_check.py --json`.
- Enforces subprocess timeout.
- Parses JSON using Python stdlib.
- Requires `schema_version == policy_decision/1.0` or the current versioned contract.
- Validates `verdict`, `deny_reason_codes`, and `provenance` before allowing execution.
- Writes decision artifacts atomically only after the evidence/artifact directory exists; write exactly one artifact for each boundary invocation, including helper timeouts, invalid JSON, contract failures, and other boundary errors when the artifact directory is writable.
- Emits simple shell-readable fields/status for the runtime script.
- Treats malformed output, missing fields, helper failure, helper verdict/exit-code contradiction, timeout, or artifact write failure as fail-closed (`deny` or boundary `error`, never allow).

Bash should not parse nested JSON with grep/sed and should not depend on `jq` unless the project has explicitly made `jq` a required dependency.

### Boundary Subprocess Hardening

Treat the policy boundary invocation itself as part of the security perimeter. A fixed helper path is not enough if the interpreter or import environment can be influenced.

- Do not allow production runtime overrides such as `PROGRAM_POLICY_BOUNDARY` or `PROGRAM_POLICY_PYTHON` to replace the boundary script/interpreter. If tests need overrides, gate them behind explicit test-only paths that cannot be used in normal runs.
- Resolve the boundary script to the repository-owned file (for example `$SCRIPT_DIR/scripts/program_policy_boundary.py`) and fail closed if missing.
- Run Python boundary wrappers in isolated mode when available: `python -I scripts/program_policy_boundary.py ...`. This blocks `PYTHONPATH`, `PYTHONHOME`, user site packages, and `sitecustomize.py` from forging boundary stdout before the wrapper runs. At minimum use `-E -s`, but prefer `-I`.
- Treat child helper subprocesses launched by the boundary as part of the same trust boundary. If the boundary calls an offline helper such as `program_policy_check.py`, invoke it with isolated mode too, e.g. `[sys.executable, "-I", helper_path, ...]`; otherwise the parent boundary may be isolated while the child helper is still vulnerable to `PYTHONPATH/sitecustomize.py` allow-forgery.
- Clear known problematic environment variables for Windows/Git-Bash Python encoding without weakening isolation, e.g. `env -u PYTHONIOENCODING -u PYTHONUTF8 python -I ...`.
- Add two malicious `PYTHONPATH/sitecustomize.py` regressions: one targeting boundary startup/stdout/artifact forgery, and one targeting the child helper `--json` invocation. Both should prove a denied technique remains denied and no target-touching dry-run command is emitted.
- For allow decisions, do not rely only on stdout saying `allow` plus “artifact exists”. Prefer validating that the artifact path is inside the policy artifact directory and that the artifact JSON request/decision fields match the current stage, target, technique, mode, program hash, and global-scope hash.
- For local runtime-only denials (for example CIDR target without explicit `--allow-cidr`), prefer a forced-deny artifact path that still uses the boundary contract, records deny reason codes, hashes program/global scope files, and exits non-zero without invoking target-touching tools.

## Review Gates

Before per-stage runtime wiring:

- Run Codex engineering review on the proposal/design and route back for blocking issues.
- Run Cowork/Claude design fixes when Codex finds contract or safety mismatches.
- Re-run Codex review and require an implementation verdict such as `ACCEPT_FOR_IMPLEMENTATION`.
- Hermes validates compile/tests/review wrapper and confirms no target-touching behavior changed during design-only phases.

Recommended initial implementation scope after design acceptance: Task A (CLI/no-program regressions) and Task B (boundary wrapper) only. Defer full per-stage integration until those pass review.