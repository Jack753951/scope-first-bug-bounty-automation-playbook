> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Independent Review — Phase 1 P1-3 Program Policy Decision Helper

Generated: 2026-05-15
Reviewer: Claude/Cowork (third-party, independent of Codex)
Scope: offline read-only review of P1-3 artifacts. No scans, probes, or target-touching commands executed.

Files reviewed:

- `scripts/core/__init__.py`, `scripts/core/scope.py`, `scripts/core/policy.py`
- `scripts/program_policy_check.py`, `scripts/test_program_policy_check.py`
- `programs/README.md`
- `handoff/codex_task.md`, `handoff/codex_review.md`
- `.hermes.md`, `HERMES_WORKFLOW.md`, `handoff/sustained_review_loop.md`

## Verdict

**ACCEPT** for P1-3 as an offline decision helper.

The implementation satisfies the P1-3 contract: default-deny, validator-as-necessary-not-sufficient, program/global scope intersection, out-of-scope precedence, technique allow/deny, automation/window gating for `planned`/`live`, IDN denial, and a structured `audit_event`. Tests cover every required case in the task. Runtime boundary is preserved — `recon.sh`, `config/scope.txt`, `config/recon.conf` are untouched.

P1-4 must not consume this helper until the non-blocking items in §3 are at least triaged, because they shape the runtime contract.

## Blocking Issues

None.

I considered the following as potential blockers and concluded they are not blocking for P1-3 (offline policy computation only). They become blocking before P1-4 runtime wiring:

- `_load_program_json` reads the program file again after the validator already opened it — there is a short read-after-read window where the file could change. Acceptable offline; before runtime wiring, the validator and the decision engine should share a single parsed-and-validated structure.
- `_check_technique` emits two errors when a technique is both `forbidden` and absent from `allowed`. Harmless for the verdict; produces noisier audit text than needed.

## Non-Blocking Improvements

1. **Single-parse program data.** Refactor `validate_program_scope.validate_file` (or add a sibling) to return both the verdict and the already-parsed `dict`, so `_load_program_json` can be deleted. This removes a TOCTOU surface and ~15 lines.
2. **Granular audit events.** `audit_event` only carries `PROGRAM_POLICY_ALLOW` / `PROGRAM_POLICY_DENY`. Add a `deny_reason_code` enum (`OUT_OF_SCOPE`, `NOT_IN_PROGRAM_SCOPE`, `NOT_IN_GLOBAL_SCOPE`, `FORBIDDEN_TECHNIQUE`, `AUTOMATION_DISABLED`, `OUTSIDE_WINDOW`, `BLACKOUT`, `INVALID_TARGET`, `VALIDATOR_DENY`) so future log analytics can pivot on cause without parsing free-text. Cheap to add now; expensive to retrofit once runtime depends on it.
3. **Populate `reasons` for allow paths.** The field is always `[]`. Use it to list which scope entries and which window matched (e.g., `matched program in_scope[2] domain example.test`, `matched global scope.txt:7 wildcard *.example.test`, `inside testing_windows.allowed[0]`). This gives reviewers explainability and supports report generation later.
4. **Validator error pass-through hygiene.** `_check_global_scope` and the validator-failure path both `extend(errors)` raw. Prefix or namespace them (`validator:`, `global_scope:`) so downstream consumers can group errors. Two-line change.
5. **Don't double-flag forbidden techniques.** Short-circuit in `_check_technique`: if forbidden, append one error and return; only fall through to the "not allowed" check when it is neither forbidden nor allowed.
6. **Test gap — global scope ambiguity.** Add a unit test for empty/all-comment `config/scope.txt` (current code returns `errors` with "no usable entries" → deny). And for a `config/scope.txt` whose only error is a non-fatal malformed line: should warn, not deny, if at least one entry parses. Lock today's behavior in tests so it can't regress silently.
7. **Test gap — IPv4 CIDR target with global IP scope.** No test covers target `10.0.0.0/24` against global `10.0.0.0/8`. The code supports it via `network.subnet_of`; needs to be pinned.
8. **Test gap — URL with port + url_prefix.** Add a test where target has explicit port and url_prefix omits it (and vice-versa), to lock the strict port-match semantic.
9. **Module-level mutable defaults.** `PolicyDecision.reasons/errors/warnings` use `field(default_factory=list)` (good). Confirm `validate_program_scope.validate_file` returns fresh lists, not shared module state — worth a quick second look.
10. **Doc clarity in `programs/README.md`.** The line "dry-run mode is intentionally treated as non-target-touching" is correct here, but P1-4 must enforce that the runtime cannot promote a `dry-run` allow into a `planned`/`live` execution without rechecking. Add a one-line warning to the README so the contract is hard to misread.

## Strategic Recommendations

These are architecture/product-security suggestions aligned with the long-term goal of an extensible, update-friendly, authorized testing platform.

1. **Decision object as a stable cross-phase contract.** Treat `PolicyDecision.as_dict()` as the wire format between offline preflight, the future `recon.sh --program` runtime, and any future module/plugin manifest layer. Version it (`schema_version: "policy_decision/1.0"`), and add it to the schema/examples directory so future modules can validate that they consumed a real decision and not a hand-crafted dict. This is the seam where evasion of the gate is most attractive; making it a typed, versioned contract closes that hole early.

2. **Two-key safety before P1-4 runtime wiring.** When `recon.sh --program <slug>` consumes a decision, require *both* a fresh in-process decision (not a cached file) *and* the operator-visible `config/scope.txt` match. Never trust a previously-stored allow. Document this as the "no-cache rule" so future refactors do not break it.

3. **Effective rate cap composition (P1-4 input).** `rate_limits` is loaded for validation but unused for decisions. Phase 1.4 should compute `min(program.rate_limits.*, config/recon.conf.*)` and return that in the decision object so scanners cannot pull faster than either source allows. Building the composition function in `scripts/core/` (next to `policy.py`) keeps the safe-defaults layer in one place.

4. **Provenance fields.** Add `program_file_sha256`, `global_scope_sha256`, and `decided_at_utc` to the decision. These are cheap to compute (stdlib `hashlib`) and become essential audit evidence once decisions feed `logs/audit.log` and later report templates. Without them, "we allowed this target on day X" cannot be reproduced from history.

5. **IPv6 stance.** `scope.py` is IPv4-only by design. Codify this in the schema and README as an explicit deny ("IPv6 targets are denied until P1.x adds reviewed support") and add a unit test that an IPv6 target string (`::1`, `2001:db8::1`) returns a clear unsupported-target deny rather than relying on the catch-all "invalid target syntax" message. Today it does deny — make it deny with a code that ops can recognize.

6. **Schema-vocabulary drift guard.** Techniques are matched as raw strings. If `programs/_schema/scope.schema.json` adds a technique tag that is not yet recognized by a module or by `recon.sh`, decisions could allow techniques the runtime cannot execute safely. Add a small `scripts/core/vocab.py` that exposes the canonical technique enum, and have both the validator and `_check_technique` consult it. Drift then becomes a test failure, not a silent capability gap.

7. **Wildcard apex semantics surfaced in the decision.** Currently `*.example.test` includes apex (`include_apex=True` default). Echo the chosen semantic in `reasons`/`warnings` when the apex is what matched, so an operator who expected the strict semantic (subdomain-only) sees the mismatch in the decision output before P1-4 wires it to real scans.

8. **CIDR-target decision is a runtime risk.** Allowing a `cidr` target is allowing a fan-out. Even though scope-wise it is correct, a future module consuming this decision could scan thousands of hosts. Add either (a) a policy-level `expand_cidr: false` default and a separate explicit opt-in, or (b) a `target_cardinality_estimate` field in the decision so the runtime can refuse or chunk before execution.

9. **Helper reuse direction.** `scripts/core/scope.py` is a strong starting point for the shared infrastructure layer described in `extensible_architecture_direction.md`. Promote `normalize_target`, `load_global_scope`, and `entries_from_program_scope` into stable APIs with docstrings and `__all__`; future module manifests, finding schemas, and `recon.sh` helpers should depend on these, not re-implement them.

10. **Default-deny on unknown decision fields.** When P1-4+ extends the decision object, older consumers will see new fields. Document that consumers MUST treat unknown fields as deny-on-uncertainty rather than ignoring them. Add this rule to `programs/README.md` and to the future policy_decision schema.

## Architecture Fit

Strong fit against the long-term goals stated in `.hermes.md`, `HERMES_WORKFLOW.md`, and `extensible_architecture_direction.md`.

- **Extensibility:** `scripts/core/` is the right home and is correctly stdlib-only. Scope and policy are cleanly separated. Adding IPv6, new technique tags, or a finding schema does not require touching `program_policy_check.py`.
- **Updateability:** Schema-version on the policy decision (recommendation §1) is the missing piece; everything else is already in shape for future updates.
- **Modularity:** The CLI is a thin wrapper around `decide_program_policy`. Future module runners and `recon.sh --program` can import the same function. Good.
- **Safety gates:** Default-deny is consistent and observable. The validator-then-decision sequence preserves the "P1-2 necessary but not sufficient" rule.
- **Agent-assisted analysis:** The structured output (with the improvements in §1, §3, §4) gives Cowork/Codex a stable artifact to reason about without parsing logs.

The one architectural soft spot is the double-parse of the program JSON (validator + policy engine). Fixing that during P1-4 prep is the cleanest way to land runtime integration without TOCTOU questions.

## Safety/Scope Assessment

- No live network behavior. No socket, DNS, subprocess (except in the CLI test, which only spawns `sys.executable` on the helper itself).
- Default-deny is correct on every branch I traced: invalid mode, validator deny, malformed target, scope.in_scope miss, out_of_scope hit, global miss, forbidden technique, unknown technique, automation-disabled live/planned, blackout match, window miss, missing/invalid timezone, missing tzdata.
- IDN: raw Unicode targets fail `isascii()` check in `normalize_target` and are rejected with a clear ASCII/punycode message. Confirmed by `test_deny_raw_unicode_idn_target`.
- Out-of-scope precedence: `_check_program_scope` evaluates out_of_scope before in_scope and returns early. Correct.
- Global scope file: parser ignores comments and blanks, rejects non-ASCII, rejects malformed lines with a warning, returns an error if no usable entries remain. Will not silently allow on a corrupted file.
- `--skip-scope-check` and override tokens are not exposed by this helper, and should never be. Confirmed.
- One small surface-area note: `--program PATH` accepts arbitrary paths. The P1-2 validator enforces slug/path consistency for `programs/<slug>/scope.json` shape; for example files in `_examples/` the consistency check is relaxed. P1-4 runtime should refuse `--program` paths outside `programs/<slug>/scope.json`. Not a P1-3 blocker.

## Testing/Validation Assessment

- 11 unit tests, all required scenarios from `handoff/codex_task.md` §Tests are present and meaningful (not boilerplate).
- The CLI test is real end-to-end against `sys.executable`, which validates the import path setup in `scripts/program_policy_check.py`.
- Codex recorded that the local `python` launcher in this Windows shell is broken; the workaround using the Epic Python binary is documented in `handoff/codex_review.md`. This is an environment issue, not a code defect, and `bin/hermes review` passed once a working Python was on PATH.
- Coverage gaps to close in a small follow-up task (not blocking):
  - empty `config/scope.txt` and warning-only malformed lines (§2.6)
  - IPv4 CIDR target vs global IP/CIDR scope (§2.7)
  - URL target with explicit port vs url_prefix without port, and vice versa (§2.8)
  - IPv6 target rejection (§3.5)
  - Blackout match emits the expected deny reason (currently asserted via free-text)
- Suggested CI guard for the future: a lint test that fails if anything under `scripts/core/` imports a non-stdlib module, to keep the safe-defaults layer dependency-free.

## Recommendation For Next Phase

Proceed to **P1-4 runtime integration planning**, but route through one short cleanup task first:

1. **Cleanup task (Codex, ~½ day)** — non-blocking improvements §1, §2, §3, §5, §6, §7, §8 above. These are mechanical and they harden the decision contract before any runtime consumer is added.
2. **P1-4 design pass (Cowork)** — produce `handoff/cowork_p1_4_proposal.md` covering: where in `recon.sh` the decision is invoked, the "no-cache rule" (Strategic §2), effective rate cap composition (Strategic §3), provenance fields (Strategic §4), and refusal of `--program` paths outside `programs/<slug>/scope.json`. Include a CIDR-fanout decision (Strategic §8) before any module is allowed to consume a CIDR allow.
3. **P1-4 implementation (Codex)** — minimal: invoke the helper once per stage, abort the stage on deny, write the decision object to `logs/audit.log` and to the run's evidence directory. Do **not** introduce caching, fallbacks, or override paths in P1-4.
4. **Independent review (Cowork)** before any live target is allowed under `--program`.

P1-3 itself is ready to accept. Record this review in `handoff/accepted_changes.md` and proceed.
