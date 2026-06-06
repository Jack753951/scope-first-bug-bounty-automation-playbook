> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Proposal — Phase 1 P1-4 Runtime Integration (Design Only)

Generated: 2026-05-15
Author: Claude/Cowork (third-party, independent of Codex)
Status: **DESIGN PROPOSAL — no runtime code, scripts, config, scope, or tests modified**
Predecessors: P1-1 (schema/examples), P1-2 (offline validator), P1-3 (offline policy helper), P1-3.1 (versioned `policy_decision/1.0` contract hardening)

This proposal specifies how `recon.sh` should consume `policy_decision/1.0` from `scripts/program_policy_check.py` (or, for performance, the underlying `decide_program_policy` function) without weakening the existing `safe_target` gate. It is detailed enough for Codex to implement, but Codex must still produce its own task plan, dry-run validation, and Hermes review before merge.

---

## 1. Executive Verdict

**Proceed with P1-4 as a thin, default-deny wrapper layer that runs the program policy decision once per stage, before any target-touching command, in addition to `safe_target`. Never replace `safe_target`; never cache decisions across stages; never accept a stored allow.**

The contract `policy_decision/1.0` (versioned, with `deny_reason_codes`, provenance hashes, and a deterministic `decided_at_utc`) is now stable enough to be a runtime gate. P1-4 should:

1. Add an opt-in `--program <slug>` CLI surface to `recon.sh`, refusing any path other than `programs/<slug>/scope.json`.
2. Map each stage to a fixed `(technique, target_type, mode)` tuple and call the helper once per `(stage, target)` immediately before the stage executes.
3. Treat any non-`allow` result as a hard, audited deny for that stage and that target — never the whole pipeline, never a global "skip the rest", but the stage on this target stops.
4. Compose effective rate limits as `min(program.rate_limits.*, recon.conf.*)` and pass the composed values down to the existing tool flags.
5. Append a structured row to `logs/audit.log` and emit a per-decision JSON artifact under the run's evidence directory.
6. Refuse `--program` together with `--skip-scope-check`. Program mode is an *additional* gate, not a substitute or escape hatch.

The existing global `safe_target` enforcement remains the first gate; the program policy decision is layered on top. **Both must pass for any target to advance to a stage's tool invocation.**

---

## 1.5 Design Revision Notes (2026-05-15)

This revision was produced in response to `handoff/codex_p1_4_proposal_review.md` ROUTE_BACK_FOR_DESIGN_FIXES. Each numbered Codex blocker is resolved below; see the linked sections for the new wording.

1. **Technique vocabulary now uses only schema enum values.**
   - The `dir_bruteforce` stage maps to technique `directory_bruteforce` (§5 table). This is the actual enum value in `programs/_schema/scope.schema.json:519`.
   - `webhook_notification` is removed. `send_notifications` is **no longer policy-gated** in P1-4; notification delivery is governed by existing flags, not by `decide_program_policy`. A future schema/contract update may add a notification technique; that is out of scope for P1-4.
   - `policy_preflight` is removed. The initial preflight is redesigned as a **non-decision environment check** in `validate_runtime_flags` and `run_pipeline` setup: it verifies that the program file exists, is a regular file, is readable, parses as JSON, and that the Python interpreter/helper are runnable. It does **not** invoke `decide_program_policy` and never produces a `policy_decision/1.0` allow. See §5 (preface), §8, §18.1 #1.

2. **Dry-run / planned / live matrix no longer permits target-touching execution under `--policy-mode dry-run`.**
   - `--policy-mode dry-run` is **only valid when `--dry-run` is also set**. Without `--dry-run`, the operator must supply `--policy-mode planned` or `--policy-mode live`. Combining live execution with the helper's lenient `dry-run` mode is rejected in `validate_runtime_flags` with exit 2.
   - There is no implicit default that would let a live run through with `dry-run` policy mode. See §4.1, §14.

3. **Rate-limit composition uses actual schema keys.**
   - The composition table is rewritten against `programs/_schema/scope.schema.json:166-212` keys: `max_concurrency`, `max_requests_per_second`, `request_delay_ms`, `nuclei_rate_limit`, `nuclei_concurrency`, `naabu_rate`, `httpx_threads`, `subfinder_threads`. There is no schema key for `FEROX_THREADS`; that variable is left unchanged in P1-4. See §13.
   - The test plan and validation matrix reference these exact keys (§15 Step 8, §16 V13).

4. **Initial artifact ordering: run output/evidence directory is created before any allow decision must be recorded.**
   - `run_pipeline` now creates the run output directory and `evidence/policy/` subtree **immediately after `safe_target` succeeds** and **before any `policy_decide` call**. This guarantees the artifact-write path exists when the first stage's allow must be persisted.
   - A `--program` run that is denied still has its evidence directory created; per Codex review §Blocking 4, this is explicitly acceptable. The run dir does not constitute target interaction.
   - The non-decision env preflight (§5 preface, §8) does not require an artifact write because it does not authorize execution.

5. **jq-free Python stdlib wrapper is defined.**
   - A new boundary script `scripts/program_policy_boundary.py` (Python stdlib only) is added in P1-4. It wraps `scripts/program_policy_check.py` invocation with `subprocess.run(..., timeout=...)`, validates the `policy_decision/1.0` contract, writes the artifact atomically (`tempfile` + `os.replace` under the run evidence dir), and prints a short, stable, shell-readable status block on stdout. Bash never parses nested JSON. See §4.3, §4.4 (new).
   - This replaces the prior "bash parses helper JSON" wording. `jq` is not required by the policy gate.

6. **`--program` absent is now absolute: no new behavior at all.**
   - When `PROGRAM_SLUG` is unset, `recon.sh` writes no new stdout lines, no new stderr lines, no new audit rows, no new files, and runs no helper, no Python check, and no path/availability check. The "modulo no-op log lines" caveat and the proposed `policy gate not active` log message are removed. See §5.3, §16 V1, §15 Step 10.
   - All `validate_runtime_flags` extensions added by P1-4 are guarded by `if [[ -n "$PROGRAM_SLUG" ]]; then ... fi` at the top so they are skipped entirely otherwise.

Safety boundary (§2), the no-cache rule (§7), and deny-on-uncertainty (§8) are preserved unchanged from the original proposal except where they explicitly reference the items above.

---

## 2. Safety Boundary

P1-4 must preserve every Phase 0 / P1-x safety property:

- `safe_target` runs first and unchanged on every host/URL.
- `REQUIRE_SCOPE_CHECK=false` in `config/recon.conf` remains a hard error (`recon.sh:224-231`).
- `--skip-scope-check` continues to require `SCOPE_OVERRIDE_TOKEN`/`SCOPE_OVERRIDE_CONFIRM` and continues to force `DRY_RUN=true` (`recon.sh:234-247`).
- Domain-expansion output (subfinder/crt.sh) continues to be revalidated and dropped to `subdomains_dropped.txt` before any downstream stage sees it.
- No new code may bypass `safe_target` or `validate_scope_file`.
- The policy decision helper remains stdlib-only, default-deny, and never opens sockets, runs DNS, or invokes scanners.
- No live target interaction is added by P1-4. Every new behavior is a *gate that can deny*, not a new probe.

The single new authority created by P1-4: **a per-stage allow/deny derived from the active program file plus the global scope file**. It can only further restrict the existing pipeline; it can never broaden it.

If a program file exists but the global gate refuses the target, the global gate wins. If the global gate would allow but the program denies, the program denies. There is no `OR`; only `AND`.

---

## 3. Non-Goals

P1-4 deliberately does not include any of the following. They are tracked as later work and must not creep into the implementation:

- A module/plugin runner, finding schema, evidence schema, or run-manifest layer (those are P2-x in `module_system_architecture_notes.md`).
- Live target interaction beyond what `recon.sh` already does — P1-4 only adds a deny gate.
- Any form of decision cache, decision file load, or "previously approved" shortcut.
- Any consumer of `policy_decision/1.0` other than `recon.sh` itself (module/runner consumers come in P2).
- Any change to `config/scope.txt`, `config/recon.conf` defaults, `programs/<slug>/scope.json` content, or the schema.
- Any change to `scripts/core/policy.py` or `scripts/core/scope.py` semantics. P1-4 may add small read-only helpers in `scripts/core/` (for rate-limit composition, audit-row formatting), but it must not change existing decision behavior.
- Any new external dependency. P1-4 stays Python stdlib + bash.
- Changing `safe_target` to delegate to the Python helper. They remain two independent gates.
- Promotion of `dry-run` allow into `planned`/`live` without re-running the helper.
- Notification webhooks based on policy decisions (the existing finding-severity webhook stays as is).

---

## 4. Proposed CLI / Interface Changes

### 4.1 `recon.sh` new flags

Two new flags are added to `parse_args` (`recon.sh:173-221`). All other flags retain current behavior.

| Flag | Type | Default | Description |
|---|---|---|---|
| `--program <slug>` | string | unset | Activate program policy mode using `programs/<slug>/scope.json`. Implies an additional deny gate per stage. |
| `--policy-mode {dry-run\|planned\|live}` | enum | **required when `--program` is set** | Decision mode forwarded to `decide_program_policy`. There is no default — the operator must declare intent. Composition with `--dry-run` is constrained below and in §14. |

Constraints (must be enforced in `parse_args` / `validate_runtime_flags`, all guarded by `[[ -n "$PROGRAM_SLUG" ]]` so they are inert when `--program` is unset):

- `--program` requires a non-empty slug matching `^[a-z0-9][a-z0-9-]{0,62}$`. Reject anything else.
- `--program` resolves to `<HACKLAB>/programs/<slug>/scope.json` and **must not** accept `--program /some/other/path.json` or any value containing `/`, `\`, `..`, NUL, or whitespace. (Detail in §12.)
- `--program` forbids combination with `--skip-scope-check`. If both are supplied: `err "--program is incompatible with --skip-scope-check"; exit 2`.
- `--program` **requires** `--policy-mode`. If `--program` is supplied without `--policy-mode`: `err "--program requires --policy-mode {dry-run|planned|live}"; exit 2`. There is no implicit default; the operator must declare intent.
- `--policy-mode` is meaningless without `--program`. If supplied without `--program`: `err "--policy-mode requires --program"; exit 2`.
- **`--policy-mode dry-run` is only valid when `--dry-run` is also set.** This is the critical rule from the Codex review blocker §2: a dry-run policy decision must never authorize target-touching execution. If `--policy-mode dry-run` is supplied without `--dry-run`: `err "--policy-mode dry-run requires --dry-run; use --policy-mode planned or --policy-mode live for execution"; exit 2`.
- `--policy-mode {planned,live}` plus `--dry-run` is allowed (the helper runs in the stricter mode, command execution stays in dry-run). This makes "would planned/live be approved?" testable without live egress.

### 4.2 New env vars

| Var | Purpose | Default |
|---|---|---|
| `PROGRAM_POLICY_HELPER` | Path to Python helper for testability. | `<HACKLAB>/scripts/program_policy_check.py` |
| `PROGRAM_POLICY_PYTHON` | Python interpreter override. | `python3` if available, else `python`. |
| `PROGRAM_POLICY_TIMEOUT_SECS` | Subprocess timeout per call. | `15` |

These are not documented in `--help` initially; they are escape hatches for CI and the Windows shell that already had a broken `python` launcher (recorded in `accepted_changes.md` 2026-05-15 P1-3 entry).

### 4.3 Helper invocation contract (bash → python boundary wrapper)

`recon.sh` does **not** parse helper JSON directly. The boundary between bash and the Python policy library is a small stdlib-only Python wrapper, `scripts/program_policy_boundary.py`, defined in §4.4. The bash side calls the wrapper as a subprocess and reads a small, stable, line-oriented status block on stdout. This eliminates `jq` from the policy gate and avoids any grep/sed parsing of nested JSON.

The bash side wraps the boundary invocation in a single function with the following signature (proposed name `policy_decide`):

```bash
# policy_decide <stage> <technique> <target> <target_type_hint> <mode>
# Side effects: sets POLICY_VERDICT, POLICY_DENY_CODES, POLICY_REASON_TEXT,
# POLICY_DECISION_JSON_PATH, POLICY_AUDIT_EVENT, POLICY_DECIDED_AT_UTC,
# POLICY_PROGRAM_SHA256, POLICY_GLOBAL_SHA256.
# Return: 0 on allow, non-zero on deny or any error.
```

Rationale for subprocess-per-call rather than a long-lived Python daemon:

- Default-deny is easier to audit when each call is its own process: a crash, hang, or non-status output is treated as deny by the bash wrapper.
- It removes any state coupling between calls — the helper cannot accidentally cache.
- The cost (~tens of milliseconds × calls per stage) is negligible compared to network I/O.
- Codex can later replace the wrapper with a single Python `runner.py` (per `module_system_architecture_notes.md`) without changing the contract.

The bash wrapper consumes only the boundary script's status block (key=value lines). It enforces these properties on every call:

1. The boundary subprocess must exit within `PROGRAM_POLICY_TIMEOUT_SECS`. Timeout → deny (the boundary script also has its own inner timeout; the bash side uses `KillTimer`/coproc-based wallclock as a hard outer bound).
2. The boundary must print a parseable status block on stdout. Parse failure → deny.
3. The boundary must have validated and written the `policy_decision/1.0` artifact before exiting; the bash side only reads `policy_decision_path=` from the status block.
4. The status block must include `verdict=allow|deny`, `audit_event=POLICY_*`, `program_sha256=`, `global_sha256=`, `decided_at_utc=`, and `deny_codes=` (sorted CSV).
5. On allow, the artifact path under the run evidence dir must exist (the boundary atomically renames into place); the wrapper `stat`s the file and denies on missing.

### 4.4 Python stdlib boundary wrapper (`scripts/program_policy_boundary.py`)

New script added in P1-4. Python stdlib only (no third-party imports). Responsibilities:

1. **Invocation:** `python3 scripts/program_policy_boundary.py --program-file <abs path> --global-scope <abs path> --stage <name> --technique <enum value> --target <safe target> --target-type <auto|host|url|ipv4|ipv6|cidr> --mode <dry-run|planned|live> --artifact-dir <run evidence policy dir> --timeout <secs>`.
2. **Helper subprocess management:** invokes `scripts/program_policy_check.py` (or imports and calls `decide_program_policy` directly to avoid double-startup; see implementation note) using `subprocess.run(..., timeout=int)` from `subprocess` stdlib. If the inner timeout fires, the wrapper emits `verdict=deny audit_event=POLICY_HELPER_TIMEOUT` and exits 4.
3. **Contract validation:** parses the helper output with `json.loads` and checks all invariants in §6 — `schema_version == "policy_decision/1.0"`, `verdict in {"allow","deny"}`, `deny_reason_codes` is a list, `program_file_sha256` and `global_scope_sha256` are non-null hex strings on allow. Any violation → `verdict=deny audit_event=POLICY_CONTRACT_VIOLATION` plus a `violation_field=` line.
4. **Atomic artifact write:** wraps the helper's `policy_decision/1.0` payload in the envelope from §10.2 and writes it under `<artifact-dir>/<stage>/<seq>__<safe_target>.json` using `tempfile.NamedTemporaryFile(dir=artifact-dir, delete=False)` + `os.replace`. The wrapper allocates `<seq>` by scanning the artifact dir for existing files and picking the next zero-padded integer (or by reading a `.seq` counter file in the artifact dir, which the wrapper updates under `fcntl`/`msvcrt` advisory lock if available, otherwise it tolerates a small race because seqs are presentational, not load-bearing).
5. **Status block on stdout:** prints exactly one block of `key=value` lines, terminated by a blank line. Keys: `verdict`, `audit_event`, `program_sha256`, `global_sha256`, `decided_at_utc`, `deny_codes`, `policy_decision_path`, `target_type_resolved`, `warnings_count`. Values are percent-encoded the same way bash will encode them into the audit row, so the bash side can copy them through without re-encoding. No other text appears on stdout. Errors and diagnostics go to stderr.
6. **Exit code:** `0` allow, `1` deny (policy verdict), `2` argument/usage error, `3` artifact write failure, `4` helper timeout, `5` contract violation, `6` helper subprocess error. The bash side maps any non-zero exit to deny but uses the exit code plus `audit_event=` for routing.
7. **No mutation outside the artifact dir.** The wrapper does not touch `programs/`, `config/`, or `logs/`.
8. **No network, no DNS, no scanner.** Same constraints as the policy helper itself.

The boundary script is the only Python introduced by P1-4. It depends only on the stdlib and on the existing `scripts/core/policy.py` / `scripts/core/scope.py` (via `scripts/program_policy_check.py`).

### 4.5 No change to existing CLI

When `--program` is absent, `recon.sh` behavior is byte-identical to today. P1-4 does not alter any existing default. This is a strict requirement, and per Codex review blocker §6 it is absolute:

- No new stdout lines.
- No new stderr lines.
- No new audit rows in `logs/audit.log`.
- No new files anywhere (no evidence dir entries, no helper artifacts, no temp files).
- No invocation of the boundary wrapper, helper script, or any Python.
- No availability checks for `python3`, `python`, or the helper.

Every P1-4 code path is fenced by `[[ -n "$PROGRAM_SLUG" ]]` (or equivalent) at the earliest possible point. Operator runs of `recon.sh -d example.test` are bit-for-bit unchanged.

---

## 5. Exact Integration Points In `recon.sh` By Stage

The integration follows a single rule: **immediately before any function inside `run_pipeline` that consumes a target list and calls a network tool, call `policy_decide` per target. Drop denied targets to a `*.policy_dropped.txt` file with the structured deny reason. If the resulting safe-list is empty, skip the stage with a warning, just like `safe_target`'s "no safe hosts" path already does.**

**Initial preflight is a non-decision environment check, not a `policy_decide` call.** Per Codex review blocker §1, no `policy_preflight` technique is ever passed to `decide_program_policy` (the schema would reject it as `TECHNIQUE_NOT_ALLOWED`). The preflight runs in `validate_runtime_flags` and at the top of `run_pipeline`, and only confirms:

- `programs/<slug>/scope.json` exists, is a regular file, and is readable.
- The file parses as JSON (via the boundary wrapper's `--check-readable` mode, which calls `json.load` and exits without invoking `decide_program_policy`).
- `config/scope.txt` is readable (today's `validate_scope_file` continues to enforce this; no new check).
- `PROGRAM_POLICY_PYTHON` resolves to a runnable interpreter and the boundary script is importable.

If any check fails, the run aborts with exit 1 before any stage executes. A `POLICY_RUN_PRECHECK_FAIL` audit row records the failure cause. If all checks pass, a `POLICY_RUN_PRECHECK_OK` row records the resolved python interpreter path, helper SHA-256, program file SHA-256, and global scope SHA-256. **Neither row contains a `verdict` field**; both are environment events, not decisions, and they do not constitute authorization for any subsequent stage.

The mapping of stages to `(technique, target_type)` tuples follows. `mode` is always `--policy-mode` from the CLI (no implicit default; the operator must supply it, see §4.1). Every technique below is a literal enum value from `programs/_schema/scope.schema.json:514-529`.

| Stage (function) | Function line in recon.sh | Technique (schema enum) | Target type fed to helper | Notes |
|---|---|---|---|---|
| `enum_subdomains` | `recon.sh:530` | `subdomain_enumeration` | the apex domain (one call) | Run boundary wrapper *before* subfinder/crt.sh fan out. If denied, the apex skips enumeration and the pipeline falls back to the single-host path. |
| `find_live_hosts` | `recon.sh:572` | `http_probe` | `host` for each input host | Replace `filter_safe_targets` for `find_live_hosts.input` with `filter_safe_and_policy_targets` (§5.4). |
| `port_scan` | `recon.sh:613` | `port_scan` | `host` for each input host | Wrap before naabu invocation. |
| `service_fingerprint` | `recon.sh:645` | `service_fingerprint` | `host` per host (the loop at `recon.sh:663`) | Per-host call; deny removes that host's nmap entry. |
| `web_probe` | `recon.sh:681` | `http_probe` | `url` for each safe URL | Wrap before httpx invocation. |
| `dir_bruteforce` | `recon.sh:717` | `directory_bruteforce` | `url` per URL (loop at `recon.sh:735`) | Per-URL call; deny skips that URL. Fixed from previous `dir_bruteforce` per Codex review. |
| `vuln_scan` | `recon.sh:754` | `vulnerability_scan_passive` for `--quick`/`--normal`; `vulnerability_scan_active` for `--aggressive`/`--full` | `url` for each safe URL | Technique string varies with intensity so the program file can permit passive but forbid active. |

**`send_notifications` is intentionally not in this table.** No schema enum value covers webhook notifications, so P1-4 does not gate notifications via `decide_program_policy`. Notification delivery remains controlled by existing flags (e.g., `--slack`). If a future schema revision adds a notification technique, a follow-up Cowork proposal can add it to the table.

`run_pipeline` setup at `recon.sh:899` becomes, in order:

```bash
safe_target "$target" "initial_target" "auto" || return 1
# create the run output directory and evidence/policy/ subtree BEFORE any policy_decide
# so the first stage's allow artifact can be written. See §10.1.
init_run_output_dirs "$SAFE_TARGET_VALUE" || return 1
if [[ -n "$PROGRAM_SLUG" ]]; then
    # Non-decision env preflight. Logs POLICY_RUN_PRECHECK_OK or _FAIL.
    # Does NOT call decide_program_policy. Does NOT produce a policy_decision/1.0 record.
    policy_env_preflight || return 1
fi
# stages follow, each calling policy_decide per target
```

The first `policy_decide` call in the pipeline happens inside the first stage that actually has a target list (`enum_subdomains` or, if no domain enumeration, `find_live_hosts`). The evidence directory already exists by that point, so the artifact write in §4.4 has a guaranteed destination.

### 5.1 Stage skip semantics

If every target for a stage is denied:

- The stage logs a warning (`warn "no policy-allowed targets for <stage>"`).
- The stage returns without invoking its tool, exactly mirroring today's `[[ -s "$safe_input" ]] || { warn "no safe hosts ..."; return; }` paths.
- The pipeline continues to subsequent stages (which may have empty inputs and likewise no-op).
- Audit rows for each denied target are still written.
- The run's `summary.md` (§9.3) reports the policy-deny count alongside the existing safe-filter dropped counts.

### 5.2 Per-target vs per-stage call

Calls are per-target, not per-stage-list. Reasons:

- A single deny in the list must not block the rest. Today `filter_safe_targets` already operates per-line; the policy gate must mirror that.
- Provenance hashes captured per call let auditors prove "this specific URL was approved at this specific decision time against these specific bytes".
- The helper is fast enough that per-target overhead is dominated by Python startup once per call. If this becomes a problem in practice (1000s of URLs), the `runner.py` consolidation in P2 is the right place to amortize, not P1-4.

Performance budget: assume ≤ 250 ms per call on the existing Windows shell. For a 200-URL `vuln_scan`, that is ~50 s of pre-flight overhead before nuclei runs. Acceptable for P1-4. P2's `runner.py` will reduce this.

### 5.3 Fall-through when `--program` is unset

Every integration point above must be guarded by `if [[ -n "$PROGRAM_SLUG" ]]; then ... fi`. When `PROGRAM_SLUG` is empty the stage runs exactly as today. Per Codex review blocker §6, this is absolute: no new log lines, no audit rows, no files, no helper checks, no Python checks. Codex must verify the P0 / P1-2 / P1-3 dry-run behaviors are **byte-identical** when `--program` is absent (no "modulo" clause).

### 5.4 New helper function `filter_safe_and_policy_targets`

To avoid duplicating the existing per-line loop, add a small wrapper alongside `filter_safe_targets` (`recon.sh:468-498`) that runs `safe_target` first and, on success, runs `policy_decide` with the stage's technique. Targets that fail either gate go to two separate dropped files (`<base>.safe_dropped.txt` and `<base>.policy_dropped.txt`) so audit triage can tell global-scope rejections apart from program-policy rejections.

```bash
# filter_safe_and_policy_targets <input> <output> <safe_dropped> <policy_dropped>
#                                <context> <mode> <stage> <technique> <policy_target_mode>
```

Codex should keep this function under 40 lines and make it call the existing `safe_target` and the new `policy_decide` without re-implementing either.

---

## 6. Schema Version Consumer Gate

The bash wrapper must hard-gate on `schema_version`. Concretely:

```bash
EXPECTED_POLICY_SCHEMA="policy_decision/1.0"
```

Behavior:

- If the JSON's `schema_version` is missing → deny with `audit_event=POLICY_SCHEMA_MISSING`.
- If the JSON's `schema_version` differs from `EXPECTED_POLICY_SCHEMA` → deny with `audit_event=POLICY_SCHEMA_MISMATCH`. Include both expected and observed values in the audit reason.
- Future contract bumps (`policy_decision/1.1`, etc.) are an explicit Codex task: bump the constant only after a proposal and review pass through Cowork. Until then, an upgraded helper that emits `1.1` will fail-closed against an un-upgraded `recon.sh`.

This is the property the P1-3.1 review §1 (Strategic) called the most important seam-protection: the contract is only as strong as the weakest reader.

The same gate should also be enforced on three other invariants, in this order:

1. `verdict` is exactly the string `allow` (not truthy, not present-and-allow-ish).
2. `deny_reason_codes` is an array (even when empty).
3. `program_file_sha256` and `global_scope_sha256` are non-null hex strings on the allow path.

Failure of any of these is a deny with a distinct audit event (`POLICY_CONTRACT_VIOLATION`). The wrapper must log the offending field name and value (truncated) but must not log secrets — these fields contain no secrets by construction.

---

## 7. No-Cache Rule

The contract is: **for every `(stage, target)` pair, `recon.sh` must call the helper afresh against the current bytes of `programs/<slug>/scope.json` and `config/scope.txt` and must never reuse a previous decision.**

Enforcement mechanisms:

1. The bash wrapper has no decision-cache data structure. There is no associative array keyed on `(target, technique)`; there is no `if seen ...` shortcut. Each call is independent.
2. The helper subprocess re-reads both files on every invocation. The provenance hashes prove this in the audit log.
3. The wrapper *does not* read the JSON output of a prior decision file from disk before calling the helper. The on-disk artifact (§9) is for humans and post-run audit, not for runtime.
4. A stored allow file is treated as evidence-only; if anything ever loads it back, default-deny.
5. Codex must add a unit/integration test that two consecutive calls with the same arguments produce two distinct artifact files (different file paths, same hashes) and that mutating `programs/<slug>/scope.json` between calls flips the second decision when appropriate.
6. The helper's `decided_at_utc` provides a per-call timestamp; an audit grep for duplicate timestamps on the same target indicates a caching defect.

Documentation copy already exists in `programs/README.md:112` ("Future runtime consumers must never trust cached `allow` decisions"). P1-4 must add a one-line comment block in `recon.sh` near the wrapper definition stating the rule explicitly so a future contributor cannot remove the per-call pattern accidentally.

If a future operator request asks for "skip the policy check this time because we already approved it", the answer is: re-run the pipeline with the current files; the gate is the gate.

---

## 8. Deny-On-Uncertainty Behavior

Every ambiguous outcome is a deny. Specifically the wrapper must deny in all of:

- Helper subprocess exit code != 0 *and* JSON allow → deny (verdict beats exit code, but a non-zero exit with no JSON is a hard deny).
- Helper subprocess prints non-JSON or empty stdout → deny.
- Helper subprocess prints JSON missing required fields → deny.
- Helper subprocess hangs past `PROGRAM_POLICY_TIMEOUT_SECS` → kill, deny.
- Python interpreter not found → deny *the entire run*, not just one target. This is the only case where a single bad environment fails the pipeline rather than per-target. Reason: every per-target call would fail identically, and the audit log would explode with duplicate noise. Better to fail fast in `validate_runtime_flags` with `err "--program requires a working python interpreter"; exit 1`.
- `programs/<slug>/scope.json` missing → deny the run at `validate_runtime_flags` (before any stage). Similar to above.
- `config/scope.txt` unreadable → already a hard error elsewhere; preserve.
- Schema-version mismatch → per-target deny with `POLICY_SCHEMA_MISMATCH`. Do not fail the run because it could be a partial upgrade situation; the deny will surface the issue immediately on the first call.
- Two consecutive calls with the same input that produce different `verdict` values within the same stage → not an automatic deny (timing windows can flip), but it must be visible in the audit log.

Default-deny extends to the JSON path too: if the subprocess prints `verdict: allow` but the wrapper cannot write the artifact file (disk full, permission denied), the wrapper denies and emits `POLICY_ARTIFACT_WRITE_FAILED`. Otherwise an "approved-but-unrecorded" decision could execute, which would break the audit story.

---

## 9. Audit Log Row Format

### 9.1 Where rows are written

`logs/audit.log` (existing path, `recon.sh:27`). Append-only, one line per event. The existing `audit_log` function (`recon.sh:249-257`) is *kept* for the `safe_target` / `SAFE_TARGET_*` events. P1-4 adds a **second**, structurally compatible appender that emits one richer line per policy decision and per policy-related lifecycle event.

### 9.2 Row shape

Format: pipe-separated `key=value` pairs to keep grep/awk friendly while encoding all required `policy_decision/1.0` fields. Values containing `|`, `=`, whitespace, or non-printable characters are URL-percent-encoded. This matches the existing single-line audit style.

```
<iso8601_utc> | event=<event> | run_id=<run_id> | stage=<stage> | technique=<technique> | mode=<mode> | program_slug=<slug> | target=<original_target> | normalized_target=<normalized> | target_type=<type> | verdict=<allow|deny> | deny_codes=<csv> | program_sha256=<hex|null> | global_sha256=<hex|null> | decided_at_utc=<iso8601_utc> | reasons=<csv_quoted> | warnings_count=<n> | artifact=<relative_path> | user=<user> | dry_run=<true|false> | intensity=<intensity>
```

Field semantics (each is required):

- `event` ∈ `{POLICY_DECISION_ALLOW, POLICY_DECISION_DENY, POLICY_SCHEMA_MISSING, POLICY_SCHEMA_MISMATCH, POLICY_CONTRACT_VIOLATION, POLICY_HELPER_TIMEOUT, POLICY_HELPER_ERROR, POLICY_ARTIFACT_WRITE_FAILED, POLICY_RUN_PRECHECK_OK, POLICY_RUN_PRECHECK_FAIL, POLICY_RUN_SUMMARY, POLICY_CIDR_DENIED}`. Stable enum; future additions require a Cowork proposal. Notification denials are not in this enum because `send_notifications` is not policy-gated in P1-4 (see §5).
- `POLICY_RUN_PRECHECK_OK` and `POLICY_RUN_PRECHECK_FAIL` are **environment events**, not policy decisions. They carry `program_sha256` and `global_sha256` when computable, but they have no `verdict`, `technique`, `target`, or `decided_at_utc` fields — those keys serialize as empty values so the row shape stays uniform but consumers must not treat them as authorization records.
- `run_id` is a per-pipeline UUID-or-timestamp identifier set once at `run_pipeline` entry and reused for every audit row in that pipeline. Today `recon.sh` uses `${TIMESTAMP}` plus `safe_name`; reuse that combination as `run_id=<safe_name>_<TIMESTAMP>`.
- `stage` is the recon.sh stage function name (`run_precheck`, `enum_subdomains`, `find_live_hosts`, `port_scan`, `service_fingerprint`, `web_probe`, `dir_bruteforce`, `vuln_scan`). `run_precheck` is used for the env-preflight rows only.
- `technique`, `mode`, `program_slug`, `target`, `normalized_target`, `target_type`, `verdict`, `deny_codes`, `program_sha256`, `global_sha256`, `decided_at_utc` are passed through verbatim from `policy_decision/1.0`. `deny_codes` is a comma-separated, sorted list. Empty list serializes as `deny_codes=` (empty value, present key).
- `reasons` is the `policy_decision/1.0` `reasons` array, joined by `; ` and percent-encoded. Truncate to 1024 bytes after encoding; append `…` if truncated.
- `warnings_count` is the integer length of `warnings`. The full warnings list is preserved in the JSON artifact (§9.3); the audit log keeps the count to avoid log bloat.
- `artifact` is the relative path to the decision's JSON artifact, anchored at the run output directory (`evidence/policy/<stage>/<safe_target>__<seq>.json`). Empty when no artifact was written (e.g., `POLICY_HELPER_TIMEOUT` before any output).
- `user` and `dry_run` and `intensity` mirror the existing `audit_log` row so a single grep can correlate with `SAFE_TARGET_*` rows.

### 9.3 Why a separate row format

The existing `safe_target` row uses a fixed five-key shape (`recon.sh:253-256`). Extending it in place would either break consumers that currently grep `event=SAFE_TARGET_*` or require all rows to grow new keys. A second, parallel format:

- preserves existing `SAFE_TARGET_*` row stability;
- gives policy decisions room for structured fields without sacrificing greppability;
- keeps both gates traceable within the same file, in chronological order;
- composes cleanly with the future `runs/<run_id>/audit.log` directory structure described in `module_system_architecture_notes.md`.

### 9.4 Atomicity

Audit rows must be written via `printf ... >> "$AUDIT_LOG_FILE"` after the artifact JSON is on disk and `fsync`/`flush` is best-effort by the OS append. The order is: (1) write JSON artifact to a temp file, (2) `mv` to final path, (3) append audit row. If step (2) fails, step (3) is `POLICY_ARTIFACT_WRITE_FAILED` with `verdict=deny` regardless of helper output.

### 9.5 Run-end summary row

At `run_pipeline` exit, append a single `POLICY_RUN_SUMMARY` row with counts: `allow_count`, `deny_count`, distinct `deny_codes`, `program_sha256_observed`, `global_sha256_observed`, `started_at_utc`, `ended_at_utc`. This makes "did this run encounter unexpected denies?" a one-line query.

---

## 10. Evidence Directory Artifact Shape

### 10.1 Layout and creation ordering

Per Codex review blocker §4, the run output directory and `evidence/policy/` subtree are created by `init_run_output_dirs` (§5) **before** any `policy_decide` call. The env-preflight (§5) does not write a `policy_decision/1.0` artifact — it only writes the `POLICY_RUN_PRECHECK_OK|FAIL` audit row — so artifact-write ordering is unambiguous: the directory exists by the time the first stage's allow needs to be persisted. A `--program` run that is denied still creates the run directory; Codex review explicitly accepts this.

```
<scans_root>/<safe_name>_<TIMESTAMP>/
  evidence/
    policy/
      manifest.json              # one summary per run, written at run_pipeline exit
      enum_subdomains/
        000001__example.test.json
      find_live_hosts/
        000002__www.example.test.json
        000003__api.example.test.json
      port_scan/
        000004__www.example.test.json
        ...
      web_probe/
        000010__https__www.example.test_443_.json
        ...
      vuln_scan/
        000020__https__www.example.test_443_.json
        ...
```

There is no `initial_target/` artifact subdirectory because there is no initial-target policy decision (the env preflight does not produce a `policy_decision/1.0` record). There is no `send_notifications/` subdirectory because notifications are not policy-gated.

### 10.2 Per-decision file shape

Each `<seq>__<safe_target>.json` is exactly the helper's `policy_decision/1.0` payload, plus a wrapping envelope so the artifact is self-describing without re-reading the audit log:

```json
{
  "schema_version": "policy_decision_artifact/1.0",
  "run_id": "<safe_name>_<TIMESTAMP>",
  "stage": "vuln_scan",
  "sequence": 20,
  "captured_at_utc": "2026-05-15T12:34:56Z",
  "recon_argv": ["recon.sh", "-d", "--program", "public-bounty-example", "..."],
  "intensity": "normal",
  "dry_run": false,
  "policy_decision": { ... raw policy_decision/1.0 object ... }
}
```

The envelope `schema_version` is distinct from the inner `policy_decision/1.0` so the artifact format can evolve without touching the policy contract. Default-deny rule for any future loader: unknown envelope schemas mean "treat as opaque, do not act on the decision".

`recon_argv` should be sanitized (no env vars expanded, no `--slack` token reproduced). Any flag with `webhook` or `slack` in its name has its value redacted to `***`.

### 10.3 `manifest.json`

Written at `run_pipeline` exit (success or failure). Indexes every artifact by `(stage, sequence)` and includes the same counts as the `POLICY_RUN_SUMMARY` audit row, plus the SHA-256 of every artifact file. This makes evidence tampering detectable post-run.

### 10.4 File naming

`<seq>__<safe_target>.json`. `<seq>` is a zero-padded 6-digit decimal counter, monotonically increasing across the whole run. `<safe_target>` is `SAFE_TARGET_VALUE` with `/`, `:`, and `?` replaced by `_`, truncated to 80 chars. Identical to the existing pattern at `recon.sh:738`.

### 10.5 Permissions and gitignore

The evidence directory inherits the existing `scans/` permissions. `.gitignore` already excludes `scans/`. P1-4 must verify (not change) that `scans/` is in `.gitignore` and add `evidence/` to a new `.gitkeep`-only directory under the existing `scans/` only if Codex can do so without committing real evidence.

---

## 11. CIDR Fan-Out Policy

Today `safe_target` accepts a `cidr` target type. The P1-3.1 review (Non-Blocking §6, Strategic §6) flagged that a single `cidr` allow can legitimize thousands of hosts. P1-4 must take a position rather than defer.

**Decision: refuse `target_type == "cidr"` at the `policy_decide` wrapper unless explicit operator opt-in is supplied.**

Mechanism:

- `recon.sh` gains `--allow-cidr` (off by default).
- Without `--allow-cidr`, any `policy_decide` call where `normalized_target.target_type == "cidr"` is denied at the wrapper layer with `audit_event=POLICY_CIDR_DENIED` *before* invoking the Python helper. (The helper itself still allows CIDR; the wrapper is where the operator gate lives, because the operator is invoking `recon.sh`, not the policy library.)
- With `--allow-cidr`, the wrapper allows the CIDR through to the helper, and the audit row carries an extra `cidr_size_estimate=<n>` field where `n = 2^(32 - prefix)` for IPv4. If `n > 256`, the audit also carries `cidr_warning=large_fanout`.
- Post-decision, when iterating hosts inside the CIDR, P1-4 still calls `policy_decide` per resolved host. That is, `--allow-cidr` permits the CIDR target itself; it does not waive per-host decisions. Today `recon.sh` does not actually expand CIDRs into per-host loops (naabu handles them internally), but the moment a future stage expands them, the per-host gate must run.
- The CIDR-allow path must be loud: a `warn` line in `recon.sh` and a one-paragraph caveat in `summary.md`.

Rationale for refusing CIDR by default rather than computing cardinality: per the strategic recommendations, "build this decision now; retrofitting after a runtime exists will be expensive". Defaulting closed is the cheap, safe position.

`--allow-cidr` does not weaken `safe_target`'s scope check. A CIDR not in `config/scope.txt` is still rejected by `safe_target` as today.

---

## 12. Program Path Restriction

`--program <slug>` must resolve to exactly one canonical path: `${HACKLAB}/programs/<slug>/scope.json`. P1-4 must reject anything else.

Validation steps in `validate_runtime_flags`:

1. Confirm slug regex `^[a-z0-9][a-z0-9-]{0,62}$`. Reject `_examples`, `_schema`, leading `-`, leading `.`, anything containing `/`, `\`, `..`, NUL, or whitespace.
2. Construct `PROGRAM_FILE="${HACKLAB}/programs/${PROGRAM_SLUG}/scope.json"`.
3. Resolve `PROGRAM_FILE` via `realpath` (or `readlink -f`, falling back to a bash canonical-path helper if neither is installed). Confirm the resolved path is identical to the constructed one (no symlink escape).
4. Confirm `realpath` of the resolved file is inside `realpath "${HACKLAB}/programs/"` and not inside `realpath "${HACKLAB}/programs/_examples/"` or `realpath "${HACKLAB}/programs/_schema/"`.
5. Confirm `PROGRAM_FILE` exists, is a regular file (not symlink to outside, not a directory, not a FIFO), and is readable.
6. Pass `PROGRAM_FILE` to the helper as the `--program` value verbatim.

The wrapper does not let the helper see arbitrary user-controlled paths. This is defense-in-depth for the helper, which today accepts any `--program` path (per the P1-3 review §Safety).

`programs/_examples/` is reserved for development/testing. Real runs must not point at it. The validator in P1-2 enforces slug/path consistency only when the path matches `programs/<slug>/scope.json`; the runtime layer must enforce the path itself.

CI/test note: tests that exercise `recon.sh --program` against `_examples/` are explicitly disallowed at runtime. They should construct a temp `programs/<test-slug>/scope.json` instead.

---

## 13. Effective Rate-Limit Composition

The decision object does not currently surface rate limits (Strategic §3 in both the P1-3 and P1-3.1 reviews). P1-4 adds a small composition step using **only the actual `rate_limits` keys defined in `programs/_schema/scope.schema.json:166-212`**. Per Codex review blocker §3, no imaginary keys are introduced.

Composition flow:

1. The boundary wrapper (§4.4) exposes a mode `--emit-rate-limits` that reads the program file once via `json.load` and prints the `rate_limits` object on stdout as `key=value` lines. The bash side reads only these key=value lines; it never parses nested JSON. Keys absent from the program file are simply not emitted.
2. For each `(recon.conf var, schema key)` pair below, bash computes `min(<recon.conf value>, <program rate_limits value>)` using integer arithmetic. If the program omits the key, the recon.conf value is retained unchanged (`min(x, ∞) = x`; the program can only tighten, never loosen).
3. The composed values *replace* the bash variables for the duration of `run_pipeline`. They are not written back to `config/recon.conf`.

Composition pairs (all schema keys verified against `programs/_schema/scope.schema.json:166-212`):

| recon.conf var | `program.rate_limits` key (schema enum) | Compose to |
|---|---|---|
| `NAABU_RATE` | `naabu_rate` | `min(NAABU_RATE, rate_limits.naabu_rate)` |
| `NUCLEI_RATE_LIMIT` | `nuclei_rate_limit` | `min(NUCLEI_RATE_LIMIT, rate_limits.nuclei_rate_limit)` |
| `NUCLEI_CONCURRENCY` | `nuclei_concurrency` | `min(NUCLEI_CONCURRENCY, rate_limits.nuclei_concurrency)` |
| `HTTPX_THREADS` | `httpx_threads` | `min(HTTPX_THREADS, rate_limits.httpx_threads)` |
| `SUBFINDER_THREADS` (if present in recon.conf) | `subfinder_threads` | `min(SUBFINDER_THREADS, rate_limits.subfinder_threads)` |

Schema keys that exist in the program file but have no matching recon.conf variable are recorded in the run summary but not actively composed:

- `max_concurrency` — global per-program concurrency cap. Recorded as `program_max_concurrency` in the `POLICY_RUN_SUMMARY` row.
- `max_requests_per_second` — global per-program RPS cap. Recorded as `program_max_rps`.
- `request_delay_ms` — global per-program minimum inter-request delay. Recorded as `program_request_delay_ms`. P1-4 does not translate this into a sleep between tool invocations; that translation is deferred to a follow-up phase.

`FEROX_THREADS` has **no matching schema key** (Codex review blocker §3). P1-4 leaves `FEROX_THREADS` unchanged. If a future schema revision adds a `feroxbuster_threads` (or similar) key, a follow-up Cowork proposal can add the pair to the composition table. Adding fields to the schema is non-blocking for P1-4.

The composed effective values and the recorded-only program-cap values are emitted in the `POLICY_RUN_SUMMARY` audit row (§9.5). The composition is idempotent and pure; it does not run for runs without `--program`.

---

## 14. Dry-Run / Planned / Live Semantics

Two distinct concepts must remain orthogonal:

- `--dry-run` — a `recon.sh`-level switch that prints commands instead of executing them. No live network egress. (`recon.sh:82`, `recon.sh:540-547`, etc.)
- `--policy-mode {dry-run, planned, live}` — the *mode* passed to the helper, which determines whether `automation_permitted=true` and a valid testing window are required.

**Codex review blocker §2 rule: target-touching execution may never use `--policy-mode dry-run`.** The corrected matrix:

| `--dry-run` | `--policy-mode` | Helper `mode` | Tools execute? | Status |
|---|---|---|---|---|
| not set | `dry-run` | n/a | n/a | **REJECTED** in `validate_runtime_flags` with exit 2. A dry-run policy allow must never authorize live exec. |
| not set | `planned` | `planned` | yes | Authorized planned execution. Helper requires `automation_permitted=true` and a valid testing window. |
| not set | `live` | `live` | yes | Authorized live execution. Helper requires `automation_permitted=true` and a valid testing window. |
| not set | unset | n/a | n/a | **REJECTED** in `validate_runtime_flags`: `--program` requires explicit `--policy-mode`. |
| set | `dry-run` | `dry-run` | no | Standard dry-run preview; cheapest validation. |
| set | `planned` | `planned` | no | Test "would planned be approved?" without live egress. |
| set | `live` | `live` | no | Test "would live be approved?" without live egress. |
| set | unset | n/a | n/a | **REJECTED** in `validate_runtime_flags`: `--program` requires explicit `--policy-mode`. |
| `--skip-scope-check` | any | n/a | refused | `--program` is incompatible with `--skip-scope-check` (§4.1). |

The first row is the central fix from the Codex review: previously the proposal defaulted `--policy-mode dry-run` and would have allowed `--program` without `--dry-run` to execute tools while the helper used the lenient `mode=dry-run` checks. That promoted a dry-run allow into target-touching execution, violating the P1-3.1 contract in `programs/README.md:114-116`. The corrected matrix rejects this combination at CLI validation time.

**Critical rule, from P1-3.1 doc:** a `dry-run` allow must never be promoted to `planned` or `live` execution without re-running the helper. Mechanism: there is no promotion path. Each stage call uses the current `POLICY_MODE`. If the operator changes their mind mid-run, they kill the run and start a new one with a different `--policy-mode`. There is no in-flight mode change.

Independent of the policy gate, `safe_target` continues to apply identically across all modes.

---

## 15. TDD Implementation Plan

This is a Codex-facing plan. The order is important: every behavior listed has a failing test before it has implementation. Steps may be split into multiple Codex tasks if that improves reviewability, but the order must be preserved.

### Step 1 — Wrapper subprocess contract (bash + helper)

- Tests (new file `scripts/test_recon_policy_wrapper.bats` or equivalent shell-test framework available in the lab; if none, a Python `subprocess`-driven test under `scripts/test_recon_policy_wrapper.py` that invokes `bash recon.sh --program ... --dry-run --policy-mode dry-run authorized.test` against temp fixtures):
  - RED: missing `--program` → behavior unchanged.
  - RED: `--program publicbounty-test` with a temp `programs/publicbounty-test/scope.json` and temp global scope allowing `authorized.test` → first stage's `policy_decide` allows.
  - RED: `--program` slug with `/` → exit 2.
  - RED: `--program` plus `--skip-scope-check` → exit 2.
  - RED: helper subprocess that hangs → wrapper kills after timeout, denies.
  - RED: helper subprocess that prints `verdict: allow` but wrong `schema_version` → wrapper denies with `POLICY_SCHEMA_MISMATCH`.
- GREEN: implement `policy_decide`, `validate_runtime_flags` extensions, slug regex.

### Step 2 — Per-stage integration

- Tests: per stage in §5, assert the audit log contains `event=POLICY_DECISION_ALLOW|DENY ... stage=<name> ... technique=<expected>` exactly once per processed target, no more.
- Tests: in dry-run, the stage prints its `DRY:` line only after the policy allow row.
- Tests: a denied input causes the stage's tool not to be invoked; verify by checking that no `DRY:` line for that target appears.

### Step 3 — Schema, contract, and deny-on-uncertainty gates (§6, §8)

- Tests: synthetic helper that emits each of the contract violations one at a time. Wrapper denies and emits the correct `POLICY_*` audit event.

### Step 4 — Audit log row format (§9)

- Tests: parse the audit log post-run, assert every required key is present, deny-codes are sorted CSV, percent-encoded reasons round-trip.
- Tests: `POLICY_RUN_SUMMARY` is appended exactly once per `run_pipeline` exit, counts match per-stage events.

### Step 5 — Evidence artifact shape (§10)

- Tests: artifact JSON files exist per allow/deny, conform to envelope schema, sequence numbers monotonically increase across stages, `manifest.json` contains every artifact's SHA-256.

### Step 6 — CIDR gate (§11)

- Tests: `--program` against a CIDR target → `POLICY_CIDR_DENIED` and tool not invoked.
- Tests: `--program --allow-cidr` against a CIDR target → audit row carries `cidr_size_estimate`.

### Step 7 — Program path restriction (§12)

- Tests: `--program ../../../etc/passwd` → exit 2 in `validate_runtime_flags`.
- Tests: `--program _examples` → exit 2.
- Tests: symlink at `programs/<slug>/scope.json` pointing outside `programs/` → rejected.

### Step 8 — Rate-limit composition (§13)

- Tests: a temp program file with `rate_limits.naabu_rate=10` and `recon.conf` `NAABU_RATE=1000` → composed effective rate is 10, recorded in the `POLICY_RUN_SUMMARY` row as `effective_naabu_rate=10`.
- Tests: a temp program file with `rate_limits.nuclei_rate_limit=20` and `recon.conf` `NUCLEI_RATE_LIMIT=150` → composed effective rate is 20.
- Tests: a temp program file with `rate_limits.httpx_threads=5` and `recon.conf` `HTTPX_THREADS=50` → composed effective threads is 5.
- Tests: program file without `rate_limits` → each `effective_*` value in the summary row equals the corresponding `recon.conf` value.
- Tests: program file with `rate_limits.max_concurrency=2` and `rate_limits.max_requests_per_second=15` (no per-tool keys) → summary row carries `program_max_concurrency=2` and `program_max_rps=15`; per-tool effective values are unchanged from recon.conf.

### Step 9 — Mode matrix (§14)

- Tests: each row of the §14 matrix; assert helper `mode` and `--dry-run`-vs-execute behavior independently.
- Tests: `--program p --policy-mode dry-run` **without** `--dry-run` → exit 2 in `validate_runtime_flags` (Codex blocker §2).
- Tests: `--program p` without any `--policy-mode` → exit 2 in `validate_runtime_flags`.
- Tests: `--program p --policy-mode planned` (no `--dry-run`) → helper invoked with `mode=planned`; tools execute under planned-mode policy approval.

### Step 10 — Backwards-compat regression

- Test: every existing dry-run flow (P0/P1 acceptance evidence) reproduces **byte-identical** pipeline output when `--program` is unset. No new log lines, no new audit rows, no new files, no helper checks, no Python checks. Per Codex review blocker §6, this is absolute; there is no "policy gate not active" log line and no "modulo no-op" carve-out.

Each Codex task PR must include the dry-run output, the audit log excerpts, and the artifact `manifest.json` for each test, mirroring the existing `accepted_changes.md` evidence style.

---

## 16. Validation Matrix

For Hermes acceptance, the following must all pass:

| # | Scenario | Expected outcome |
|---|---|---|
| V1 | `recon.sh --dry-run authorized.test` (no `--program`, temp global scope allowing `authorized.test`) | Identical output to today's dry-run behavior for the same temp scope; no policy events in audit log. |
| V2 | `recon.sh --dry-run --program test-prog --policy-mode dry-run authorized.test` with temp program/global scopes allowing `authorized.test` | Stage-per-stage `POLICY_DECISION_ALLOW`; tool DRY lines unchanged; artifacts written; summary row written. |
| V3 | Same as V2 but program `out_of_scope` includes `authorized.test` | The first stage-level `policy_decide` denies with `PROGRAM_OUT_OF_SCOPE`; that stage does not invoke its tool; audit row recorded. The non-decision preflight still only validates files/environment and does not authorize or deny target scope. |
| V4 | `--program` with technique `port_scan` not in `techniques.allowed` | `port_scan` stage denies; subsequent stages still attempt their own decisions and may proceed. |
| V5 | `--program` with `automation_permitted=false`, `--policy-mode live` | All stage-level decisions deny with `AUTOMATION_DISABLED`; pipeline produces no target-touching command execution for denied targets. |
| V6 | `--program` with the helper unable to find python3 | `validate_runtime_flags` exits 1 before any stage. |
| V7 | `--program` with helper subprocess that prints `policy_decision/9.9` | Per-target `POLICY_SCHEMA_MISMATCH`; pipeline continues; every stage denies. |
| V8 | `--program` with helper subprocess that hangs 30s | Wrapper kills after `PROGRAM_POLICY_TIMEOUT_SECS`, denies, audit `POLICY_HELPER_TIMEOUT`. |
| V9 | `--program ../../etc/passwd` | Exit 2 in `validate_runtime_flags`. |
| V10 | `--program test-prog --skip-scope-check` | Exit 2. |
| V11 | `--program test-prog` against CIDR target without `--allow-cidr` | `POLICY_CIDR_DENIED`. |
| V12 | `--program test-prog --allow-cidr` against CIDR target | Allowed; audit row carries `cidr_size_estimate`. |
| V13 | `--program test-prog` and program file `rate_limits.naabu_rate=10`; `recon.conf` `NAABU_RATE=1000` | `POLICY_RUN_SUMMARY` reports `effective_naabu_rate=10`. |
| V14 | `--program test-prog --policy-mode dry-run` then a second invocation `--program test-prog --policy-mode planned` against same target | Second run re-evaluates; `decided_at_utc` differs; per-stage decisions can differ; no caching. |
| V15 | `--program test-prog` with `programs/test-prog/scope.json` mutated mid-run between two stages | Stage N sees old hash; stage N+1 sees new hash; both audit rows reflect the actual bytes. |
| V16 | All tests in `scripts/test_program_policy_check.py` (existing 17) | Still pass unchanged. |
| V17 | `bash -n recon.sh` | Clean. |
| V18 | `./bin/hermes review` | Clean (Python compile OK, shell scripts OK, lock clear). |
| V19 | Unauthorized synthetic target without `--program` | Still rejected by `safe_target` exactly as today. |
| V20 | `REQUIRE_SCOPE_CHECK=false` | Still hard error. |

V19 and V20 are explicit regression-protection tests; they are the most important non-policy rows in the matrix because they prove P1-4 did not weaken P0.

---

## 17. Rollback Plan

P1-4 is purely additive when `--program` is unset, so rollback is simple but needs a clean recipe.

### 17.1 Code rollback

The change is one bash function (`policy_decide`), one wrapper (`filter_safe_and_policy_targets`), edits in eight stage functions, edits in `parse_args` / `validate_runtime_flags`, and an audit-log appender. Codex must keep these edits self-contained so a single revert PR removes them. The Python side (`scripts/core/`, `scripts/program_policy_check.py`) is unchanged in P1-4, so the rollback never touches it.

`git revert <commit>` of the P1-4 PR must restore byte-identical `recon.sh` behavior, with two exceptions documented in the PR body:

- New audit log rows already written during P1-4 trial runs remain in `logs/audit.log`. They are append-only and harmless; do not truncate.
- New evidence directories under `scans/<run>/evidence/policy/` remain on disk. They are gitignored and harmless; operator may delete after rollback.

### 17.2 Operational rollback (no code change)

If a defect surfaces but reverting is too disruptive (e.g., partial rollouts), the operator simply omits `--program` on the next invocation. The pipeline reverts to today's behavior with no risk. This is the dominant rollback path.

### 17.3 Roll-forward triggers

A roll-forward (re-enabling `--program` after a fix) requires:

- Cowork independent review of the fix.
- A new V1-V20 validation pass.
- A new `accepted_changes.md` entry with the diff summary.

### 17.4 Data rollback

No `programs/<slug>/scope.json` file content is changed by P1-4. No `config/scope.txt` change. Rollback does not touch operator-curated data.

### 17.5 Schema bump rollback

If `policy_decision/1.0` is later bumped to `1.1` and `EXPECTED_POLICY_SCHEMA` was advanced, an emergency rollback to `1.0` is one-line: revert `EXPECTED_POLICY_SCHEMA="policy_decision/1.0"`. The audit log will then show schema mismatches against the upgraded helper, which fail-closed; the operator can downgrade the helper or pin both.

---

## 18. Risks and Open Questions

### 18.1 Blocking prerequisites

These must be resolved before P1-4 implementation merges. They are all design-level, not code-level; the implementation can proceed if Codex handles them as it goes.

1. **Technique vocabulary alignment.** `programs/_schema/scope.schema.json` and the existing `_examples/` files use specific technique strings (e.g., `http_probe`, `port_scan`, `vulnerability_scan_passive`). Codex must grep the schema and confirm the §5 technique strings exactly match. Mismatch is a blocking defect: a stage would deny every target because the technique string is not recognized.
2. **`programs/_examples/` use in tests.** §12 forbids runtime `--program` against `_examples/`. Codex must confirm test fixtures construct ephemeral `programs/<test-slug>/scope.json` files in temp directories rather than reusing `_examples/` paths.
3. **Per-host expansion of CIDR.** Today `naabu` handles CIDR internally and `recon.sh` does not iterate hosts. §11 says "the moment a future stage expands them, the per-host gate must run". Confirm in writing that no current stage in `recon.sh` expands CIDR into a host loop. If any does, that loop must call `policy_decide` per host.
4. **`logs/` directory presence.** `recon.sh:912` creates the run log dir but `audit_log` only `mkdir -p`s on the audit log path. Confirm the policy audit-log appender follows the same pattern and never silently swallows write failures.
5. **Subprocess invocation under Windows shell.** P1-3 acceptance recorded that the default `python` launcher is broken on the operator's Windows shell. The wrapper must accept `PROGRAM_POLICY_PYTHON` and `bin/hermes review` must continue to fall back from a non-runnable `python3` shim to `python` (existing fallback recorded 2026-05-15).

### 18.2 Non-blocking improvements

These should be tracked for after P1-4, not blocked on:

1. Promote the bash subprocess wrapper to a single Python `runner.py` (per `module_system_architecture_notes.md`) once a second consumer (a module) needs the same gate. Until then, per-target subprocess overhead is acceptable.
2. Add a `scripts/core/audit.py` that defines the audit row format programmatically and exposes a `format_row(...)` helper. Today the format is bash-side; later, the same format will need to be emitted by Python (modules, runners). One source of truth is cheaper than two.
3. Replace the IPv6 string-match in `policy.py:133` with a structured reason tag (P1-3.1 review Non-Blocking §3). Cosmetic but worth doing before more consumers depend on the substring.
4. Land the single-read refactor in `policy.py` so `_load_program_json` and the validator share a parse (P1-3 Non-Blocking §1, P1-3.1 Non-Blocking §2). Tightens the TOCTOU surface by one read.
5. Bring CLI text output of `program_policy_check.py` in line with the JSON contract (P1-3.1 Non-Blocking §1). Operators using `--program` will likely run the CLI directly to debug; stale text output is confusing.
6. Promote `scripts/core/scope.py` API surface with `__all__` and docstrings (P1-3 Strategic §9, P1-3.1 Strategic §5).
7. Add `vocab.py` for technique enums (P1-3 Strategic §6) — turns vocabulary drift into a test failure rather than a silent capability gap.
8. After P1-4 lands, write a Cowork review pass focused on whether the audit log is human-readable and whether the artifact directory is small enough to keep per-run.

### 18.3 Open questions for the operator

- Should `--policy-mode planned` *without* `--dry-run` be allowed at all in P1-4, or should the first cut require either `--policy-mode dry-run` or `--dry-run`? Strict default is the safer first move; the matrix in §14 currently allows planned/live exec, but the operator can ask Codex to disable that combination behind an explicit flag.
- Should `POLICY_RUN_SUMMARY` failures (e.g., write fails) abort the run with non-zero exit? Today proposed: log and continue. Operator can override.
- Should the artifact directory live under `scans/<run>/evidence/policy/` (as proposed) or under `runs/<run_id>/evidence/policy/` (matching the future `module_system_architecture_notes.md` layout)? Proposed: keep under `scans/` for P1-4 to avoid creating a new top-level dir; migrate when the `runs/` layout actually materializes.
- Should the `--program` path lookup honor an env var `HACKLAB_PROGRAMS_DIR` for testing? Proposed: no in P1-4. Tests use temp dirs and pass an explicit `HACKLAB`.

---

## 19. Architecture and Maintainability Guidance

P1-4 is the first runtime consumer of `policy_decision/1.0`. Several architectural patterns established here will be reused by P2 modules. Get them right now.

1. **Single source of truth for the contract.** The `EXPECTED_POLICY_SCHEMA` constant in bash and the `SCHEMA_VERSION` constant in `scripts/core/policy.py` must both read `policy_decision/1.0` literally. A future cleanup can move both to a generated header; for P1-4, hard-code in two places and leave a comment in each pointing at the other.

2. **Bash side stays thin.** The bash wrapper passes explicit arguments to `scripts/program_policy_boundary.py`, receives only a small shell-readable status block, and branches on that stable status. Bash does *not* parse nested JSON, implement schema validation, scope matching, target normalization, or artifact-envelope writing. Anything requiring structured JSON belongs in Python.

3. **Python side stays pure.** The helper continues to do offline policy decisions only. P1-4 must not introduce subprocess execution, network I/O, or file mutation in Python.

4. **No new global state in bash.** Use locals and explicit out-vars in `policy_decide`, mirroring `safe_target`'s `SAFE_TARGET_VALUE`/`SAFE_TARGET_HOST`/`SAFE_TARGET_REASON` pattern.

5. **Stable identifier names.** Per-decision artifact filenames, sequence numbers, audit-log keys, and `POLICY_*` events are part of the operator-facing contract from V1. Renames after P1-4 will require a deprecation cycle.

6. **Failure mode visibility.** Every deny path must produce both an audit row and a CLI line. Silent denials erode operator trust faster than wrong allows.

7. **Test layering.** Unit tests for the helper stay in Python. Wrapper tests live alongside `recon.sh`. End-to-end tests use temp `HACKLAB` roots, temp `programs/` dirs, temp `config/scope.txt`, temp scans output. None of the existing 17 helper tests is touched by P1-4.

8. **Dependency direction.** `recon.sh` depends on `scripts/program_policy_check.py`, which depends on `scripts/core/policy.py`, which depends on `scripts/core/scope.py`, which depends on stdlib only. P1-4 must not introduce a cycle and must not let `scripts/core/` import anything outside stdlib.

9. **Documentation as part of the change.** P1-4's PR must update `programs/README.md` to describe the runtime integration shape (one or two paragraphs near §P1-3 Offline Policy Decision Helper). The `accepted_changes.md` entry must include a representative audit-log excerpt and an `evidence/policy/manifest.json` excerpt.

10. **Forward compatibility.** When P2 introduces modules and a `runner.py`, the modules must consume the same `policy_decision/1.0` contract via the same envelope artifact. Codex should sanity-check the proposed envelope (§10.2) against `module_system_architecture_notes.md` before implementing.

---

## 20. Codex Task Breakdown

Suggested task split for `handoff/codex_task.md`. Each task is independently reviewable; later tasks block on earlier merges.

### Task A — CLI surface and validation (small)

- `parse_args` adds `--program`, `--policy-mode`, `--allow-cidr`.
- `validate_runtime_flags` enforces slug regex, path canonicalization, mutual-exclusion with `--skip-scope-check`, helper-availability check.
- Tests for §15 Step 1 (no integration yet).
- Acceptance: `recon.sh --program test-prog --dry-run --policy-mode dry-run authorized.test` exits cleanly with no `policy_decide` calls (function not implemented yet) when temp program/global scopes allow `authorized.test`; invalid slugs/paths exit 2; `--program` + `--skip-scope-check` exits 2.

### Task B — `policy_decide` wrapper + helper subprocess contract

- Add `policy_decide` function as a thin bash caller around `scripts/program_policy_boundary.py`; bash must not parse nested JSON.
- Add `EXPECTED_POLICY_SCHEMA` constant.
- Implement subprocess invocation, timeout handling, JSON parsing, schema/verdict gates, atomic artifact writing, and default-deny on any anomaly in the Python stdlib boundary wrapper.
- Add audit log appender for policy events (§9).
- Add the non-decision `policy_env_preflight` call in `run_pipeline` after output/evidence directories exist; do not add any `initial_target` `policy_decide` call.
- Tests for §15 Steps 1, 3, 4.
- Acceptance: a temp program file allowing `authorized.test` produces the first stage-level allow row; a temp program file denying it causes the first relevant stage to skip that target with a deny row. No fake `initial_target` allow/deny decision is emitted.

### Task C — Per-stage integration

- Add `filter_safe_and_policy_targets`.
- Refactor each of the seven stages in §5 to use the new wrapper for input filtering, and add per-iteration calls inside `service_fingerprint` / `dir_bruteforce` / `vuln_scan` loops.
- Tests for §15 Step 2 across all stages.
- Acceptance: V2-V5 in §16 pass.

### Task D — Evidence artifacts

- Implement artifact write under `evidence/policy/<stage>/<seq>__<safe_target>.json`.
- Implement `manifest.json` write at run end.
- Sanitize `recon_argv` (no secrets).
- Tests for §15 Step 5.
- Acceptance: artifacts conform to envelope schema; manifest hashes match.

### Task E — CIDR, mode matrix, rate-limit composition

- Implement `--allow-cidr` gate (§11).
- Verify mode matrix (§14) by tests.
- Implement rate-limit composition (§13), including a small `scripts/program_rate_limits.py` (or equivalent) read helper.
- Tests for §15 Steps 6, 8, 9.
- Acceptance: V11-V14 pass.

### Task F — Path restriction hardening

- Tighten symlink/realpath checks in `validate_runtime_flags` (§12).
- Tests for §15 Step 7.
- Acceptance: V9 passes; V10 still passes.

### Task G — Documentation and final regression

- Update `programs/README.md` with the runtime section.
- Append to `accepted_changes.md` with audit-log + manifest excerpts.
- Run V1-V20 end-to-end and record evidence.
- Acceptance: Hermes review clean; Cowork independent review writes `handoff/cowork_phase1_p1_4_review.md`.

Total estimated: 5-8 working days for Codex, plus one Cowork review pass per merged task and a final independent Cowork review before any operator runs `--program` against a real target.

---

## 21. Safety / Scope Statement

This proposal is documentation only. No source code, configuration, scope file, scheduler, scanner, or runtime behavior was modified by writing this file. No external request, DNS lookup, target-touching command, or scan was executed. All recommendations preserve existing default-deny gates and add a strict, layered second gate that can only further restrict the pipeline. P1-4 implementation must reproduce these properties; any deviation from them is a blocking defect.
