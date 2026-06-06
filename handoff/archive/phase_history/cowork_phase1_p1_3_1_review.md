> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Independent Review — Phase 1 P1-3.1 Policy Decision Contract Hardening

Generated: 2026-05-15
Reviewer: Claude/Cowork (third-party, independent of Codex)
Scope: offline read-only review of P1-3.1 artifacts. No scans, probes, target-touching commands, or source/config edits performed.

Files reviewed:

- `.hermes.md`
- `handoff/codex_task.md` (P1-3.1 task)
- `handoff/codex_review.md` (full file, P1-3.1 section in particular)
- `handoff/cowork_phase1_p1_3_review.md` (prior P1-3 acceptance)
- `programs/README.md`
- `scripts/core/policy.py`
- `scripts/core/scope.py`
- `scripts/program_policy_check.py`
- `scripts/test_program_policy_check.py`
- `git diff HEAD` for all of the above

## Verdict

**ACCEPT** for P1-3.1.

P1-3.1 fully executes the contract-hardening task and addresses the four strategic recommendations from the P1-3 review (§1 schema-version, §2 deny codes, §3 allow reasons, §4 provenance). The policy decision is now a versioned, explainable, auditable wire contract that downstream consumers can route on without parsing free-text. Runtime boundary preserved: no edits to `recon.sh`, `config/scope.txt`, `config/recon.conf`, scheduler, or any target-touching automation; the diff is confined to `scripts/core/policy.py`, `scripts/core/scope.py`, `scripts/program_policy_check.py` test, `programs/README.md`, and handoff files (no diff to `program_policy_check.py` itself — see Non-Blocking §1).

P1-4 runtime integration design may proceed.

## Blocking Issues

None.

I considered the following as candidates and concluded each is non-blocking for P1-3.1 (offline contract hardening only). They should be picked up in P1-4 design or implementation as noted.

- CLI text output (`_print_text` in `scripts/program_policy_check.py`) was not updated to surface the new contract fields. `--json` is complete; text mode is incomplete (see Non-Blocking §1). Not blocking because the wire contract is the JSON path and tests pin it.
- `_load_program_json` still re-reads the program file after the validator parses it (prior review's Non-Blocking §1). The provenance hash is now computed before either read, so the audit story is unchanged-or-better, but the TOCTOU surface remains. P1-4 prep should land the single-read refactor.
- IPv6 detection in the policy layer keys off the substring `"IPv6"` in the scope-layer error string (`policy.py:133`). Works today and is tested, but it couples two modules through a magic word. See Non-Blocking §5.

## Per-Requirement Verification

### 1. Versioned decision schema — DONE

- `SCHEMA_VERSION = "policy_decision/1.0"` defined at `scripts/core/policy.py:33`.
- `PolicyDecision.schema_version` defaults to `SCHEMA_VERSION` (`policy.py:38`) and is emitted in `as_dict()` (`policy.py:71`) on both allow and deny.
- Pinned in `test_safe_example_target_allowed_by_program_and_global_scope` (`test_program_policy_check.py:100`) and `test_cli_json_shape` (`test_program_policy_check.py:279`).
- Documented as a versioned contract in `programs/README.md:104`.

### 2. Deny reason codes — DONE

- `deny_reason_codes: list[str]` added to dataclass (`policy.py:47`).
- `PolicyDecision.deny(code, message)` helper appends a deduplicated code and a free-text error in one call (`policy.py:55-58`). `finalize()` now goes to allow only when both `errors` and `deny_reason_codes` are empty (`policy.py:65`), so a stale or unaccompanied code cannot silently flip a deny to an allow.
- All required codes are emitted by the engine:
  - `UNSUPPORTED_MODE` (`policy.py:111`)
  - `VALIDATOR_DENY` (`policy.py:121`)
  - `PROGRAM_RELOAD_FAILED` for reload/provenance failure on the program file (`policy.py:154`, `policy.py:157`, and via `_record_file_sha256` `policy.py:308`)
  - `INVALID_TARGET` for generic target-normalization failure (`policy.py:135`)
  - `IPV6_UNSUPPORTED` when the parse error mentions IPv6 (`policy.py:133-135`)
  - `PROGRAM_SCOPE_PARSE_ERROR` for malformed scope/techniques blocks (`policy.py:169, 174, 176, 215`)
  - `PROGRAM_OUT_OF_SCOPE` (`policy.py:182`)
  - `NOT_IN_PROGRAM_SCOPE` (`policy.py:185`)
  - `GLOBAL_SCOPE_ERROR` (`policy.py:199`, `policy.py:308` via global provenance)
  - `NOT_IN_GLOBAL_SCOPE` (`policy.py:202`)
  - `FORBIDDEN_TECHNIQUE` (`policy.py:220`)
  - `TECHNIQUE_NOT_ALLOWED` (`policy.py:222`)
  - `AUTOMATION_DISABLED` (`policy.py:227`)
  - `BLACKOUT` (`policy.py:256`)
  - `TESTING_WINDOW_ERROR` (`policy.py:245, 264, 267, 272`)
  - `OUTSIDE_TESTING_WINDOW` (`policy.py:284`)
- Double-flag avoidance: `_check_technique` short-circuits `forbidden` → `elif not in allowed` (`policy.py:219-224`). The test asserts `FORBIDDEN_TECHNIQUE` present and `TECHNIQUE_NOT_ALLOWED` absent (`test_program_policy_check.py:138-139`).
- Validator passthrough now namespaced: `decision.errors.append(f"validator: {error}")` (`policy.py:123`). Clean for downstream log routing.

### 3. Allow-path reasons — DONE

`reason()` helper deduplicates messages (`policy.py:60-62`). Reasons populated along the allow path:

- `program scope validator allowed` (`policy.py:125`)
- `target normalized as <type>` (`policy.py:140`)
- `program in-scope matched` (`policy.py:187`)
- `global scope matched` (`policy.py:204`)
- `technique allowed` (`policy.py:224`)
- `automation permitted for mode` for planned/live (`policy.py:229`) or `dry-run mode does not require automation` for dry-run (`policy.py:231`)
- `dry-run mode does not require testing window` (`policy.py:241`), `testing window always allowed` (`policy.py:260`), or `testing window matched` (`policy.py:282`)

Tests assert `reasons` is non-empty for allows (`test_program_policy_check.py:102, 152, 276`) and that the dry-run reason text appears when automation is disabled (`test_program_policy_check.py:152`). Useful explainability without overclaiming.

### 4. Provenance fields — DONE

- `program_file_sha256: str | None`, `global_scope_sha256: str | None`, `decided_at_utc: str` on the dataclass (`policy.py:51-53`).
- `_record_file_sha256` reads the file as bytes and emits a lowercase hex digest, or sets the field to `None` and denies with the provided code on `OSError` (`policy.py:296-310`). This satisfies the task's "keep the field empty or null; do not crash" rule.
- `_format_utc` zeros microseconds and emits `…+00:00` rewritten as `…Z` (`policy.py:313-318`). Matches the ISO-8601 UTC with `Z` requirement.
- `decided_at_utc` is set at decision construction (`policy.py:104`), so every path — including early denies — carries a timestamp.
- Provenance hashing runs before mode validation, before the validator, and before scope checks (`policy.py:107-108`). A missing-file deny therefore short-circuits cleanly via the `if decision.deny_reason_codes: return decision.finalize()` guard (`policy.py:113-114`) and avoids running the heavier validator. Good defense-in-depth.
- `now=` is plumbed through `decide_program_policy` → `validate_program_scope.validate_file` → `_format_utc` → blackout/window comparisons, giving tests deterministic timestamps without monkey-patching `datetime`. Tested in `test_safe_example_target_allowed_by_program_and_global_scope` (exact equality on `decided_at_utc`) and `test_blackout_denial_emits_code` (forces a specific clock).
- Hash equality asserted against `sha256(path.read_bytes()).hexdigest()` directly in the test (`test_program_policy_check.py:103-104`). Strong regression lock.

Caveat: the provenance hash is taken before the validator re-reads the program file. If the file changes between hash and reload, the validator/reload would emit `PROGRAM_RELOAD_FAILED`, but the recorded hash is the pre-change bytes. For an offline preflight this is acceptable. The single-read refactor recommended for P1-4 prep would also tighten this story to a single byte sample.

### 5. Edge-case test coverage — DONE

Every required test from the task is present and meaningful (not boilerplate):

- `test_empty_or_comments_only_global_scope_denies_with_code` → asserts `GLOBAL_SCOPE_ERROR` (`test_program_policy_check.py:188-191`). Locks the "no usable entries" path against silent regression.
- `test_malformed_global_scope_line_is_warning_only_when_valid_entry_exists` → asserts allow with a warning and an empty `deny_reason_codes` (`test_program_policy_check.py:193-197`). Confirms the parser tolerates partial garbage when at least one entry parses.
- `test_ipv4_cidr_target_requires_program_and_global_scope_intersection` → three sub-cases: allow when both cover, `NOT_IN_PROGRAM_SCOPE` when program does not, `NOT_IN_GLOBAL_SCOPE` when global does not (`test_program_policy_check.py:199-208`). Pins the `subnet_of` semantics in `scope.py:328-337`.
- `test_url_prefix_explicit_port_must_match` → matching port allows, mismatched (default-port) denies with `NOT_IN_PROGRAM_SCOPE` (`test_program_policy_check.py:210-224`). Locks the strict port-presence semantic recommended in the prior review §2.8.
- `test_deny_ipv6_target_with_clear_code` → asserts `IPV6_UNSUPPORTED` (`test_program_policy_check.py:167-170`). Closes prior review Strategic §5.
- `test_blackout_denial_emits_code` → asserts `BLACKOUT` with a deterministic `now=` (`test_program_policy_check.py:226-241`). Closes prior review §2.6/§2.10.
- `test_cli_json_shape` → asserts every new field on the wire path: `schema_version`, `deny_reason_codes`, `program_file_sha256`/`global_scope_sha256` (regex), `decided_at_utc` (regex), and a non-empty `reasons` (`test_program_policy_check.py:243-284`). This is the most important regression test in the file because it exercises the CLI end-to-end via `sys.executable`.

Total: 17 tests, up from 11 in P1-3. RED/GREEN evidence recorded in `handoff/codex_review.md:259-262` (RED replayed against pre-change `HEAD`; GREEN against current).

### 6. Documentation — DONE

`programs/README.md:104-112` was updated to declare:

- the output is a versioned wire contract with the new field list
- consumers must use `deny_reason_codes`, not text errors
- caches must never be trusted; runtime must recheck against current files
- unknown/unsupported schemas/fields are deny-on-uncertainty
- dry-run allow must not be promoted to planned/live without a re-check in the stricter mode

All four prose requirements from the task `programs/README.md` checklist are present.

## Architecture Fit

Strong. P1-3.1 lands the seam-hardening described in the prior review's strategic section:

- **Stable wire contract.** `schema_version: "policy_decision/1.0"` plus typed fields and stable codes turn the decision object into something modules and `recon.sh --program` can validate before consuming, instead of trusting any dict that happens to have `verdict: allow`. This is the single most important change for the long-term extensibility story (`.hermes.md` Collaboration Contract and `extensible_architecture_direction.md` intent).
- **Auditability.** Provenance hashes plus a deterministic decision timestamp make "we allowed target X with technique Y at time Z under these exact policy bytes" reproducible from logs. Once `logs/audit.log` and report templates ingest decisions, evidence reconstruction is one query, not a forensic exercise.
- **Explainability.** Populated `reasons` give Cowork/Codex an artifact to summarize without parsing free text. Pairs naturally with future report generation.
- **Default-deny preserved on every branch.** The `errors`-and-codes coupling in `finalize` (`policy.py:65`) means a future contributor cannot accidentally flip a verdict by clearing one and leaving the other. Cheap, durable safety property.

The remaining architectural soft spots are unchanged and intentionally deferred:

- Double-parse of the program JSON (validator + `_load_program_json`).
- CIDR-fanout cardinality is still implicit; a future module could expand `10.0.0.0/8` into thousands of hosts. P1-4 design should still land either `expand_cidr: false` default + opt-in, or a `target_cardinality_estimate` field, before any runtime module is allowed to consume a CIDR allow.
- Technique vocabulary is still raw strings. Schema-vocab drift (prior review Strategic §6) is not yet guarded.

None of these are blockers for the offline contract; they belong to P1-4 design.

## Safety / Scope Assessment

- No network behavior introduced. No `socket`, `dns`, `subprocess`, `httpx`, `nmap`, `nuclei`, `curl`, fuzzers, or modules added. The only `subprocess` call is the existing CLI shape test invoking `sys.executable` on the helper itself.
- No edits to `recon.sh`, `config/scope.txt`, `config/recon.conf`, scheduler/cron, or `.gitignore`. Verified via `git diff --stat HEAD` — diff is confined to `scripts/core/policy.py`, `scripts/core/scope.py`, `scripts/test_program_policy_check.py`, `programs/README.md`, `handoff/codex_task.md`, `handoff/codex_review.md`.
- `scripts/program_policy_check.py` itself was not modified — the diff stat shows no entry for it. The CLI wrapper passes the new fields through unchanged because it serializes `decision.as_dict()` to JSON, but the text path is incomplete (see Non-Blocking §1).
- Default-deny on every new branch:
  - Provenance read failure → deny with `PROGRAM_RELOAD_FAILED` / `GLOBAL_SCOPE_ERROR`, field set to `None`.
  - IPv6 raw target → deny with `IPV6_UNSUPPORTED` before `urlsplit` or domain parsing can mis-classify it.
  - IPv6 in URL host → deny inside `_normalize_url` (`scope.py:169-170`).
  - Unsupported mode → deny with `UNSUPPORTED_MODE` before any scope or technique evaluation.
  - Validator failure → deny with `VALIDATOR_DENY` and namespaced `validator:` errors before reading the program JSON a second time.
- `--skip-scope-check`, override tokens, and runtime bypass paths are not exposed by this helper; that boundary still holds.
- All tests use `tempfile.TemporaryDirectory` fixtures. No real `programs/` files are exercised, no real `config/scope.txt` is read.

## Testing / Validation Assessment

- 17 unit tests cover every required behavior in the task. Each new test asserts the structured code in `deny_reason_codes`, not only text strings — exactly the contract the task wants downstream consumers to use.
- The CLI shape test exercises the full serialization path including provenance fields and `decided_at_utc` regex. This is the highest-value test in the file because it catches drift between the dataclass, `as_dict`, the CLI wrapper, and downstream consumers in a single assertion.
- `test_safe_example_target_allowed_by_program_and_global_scope` independently recomputes the SHA-256 from the same temp file bytes. Pinning the hash this way is much stronger than asserting the field is non-empty.
- `decided_at_utc` is asserted at exact-equality with an injected `now=`, which means future refactors to `_format_utc` (e.g., adding sub-second precision) will fail loudly. Good.
- RED replay against pre-change `HEAD` was performed in a temp copy and reported `FAILED (failures=2, errors=13)`. The RED count is consistent with the new contract surface (schema_version, codes, reasons, provenance × 17 tests).
- Coverage gaps (non-blocking):
  - No direct test that the `validator: ` prefix appears on validator-failure errors. The prefix change is exercised by every validator-fail path but not asserted by string contains.
  - No test that the provenance hashes are still populated on a deny that happens after both files were successfully read (e.g., a `NOT_IN_PROGRAM_SCOPE` deny should still carry both hashes). Easy to add.
  - No test that `decided_at_utc` is zero-microsecond when `now=` carries microseconds. Easy to add.
  - No test for the IPv6-in-URL-host path (`http://[::1]/`) — only raw `2001:db8::1` is covered. The code path exists in `_normalize_url` (`scope.py:169-170`) but is not pinned.
- Suggested CI guard for the future: a lint test that fails if anything under `scripts/core/` imports a non-stdlib module, to keep the safe-defaults layer dependency-free. This was suggested in the P1-3 review and remains uncreated.

## Non-Blocking Improvements

1. **CLI text output is stale.** `_print_text` in `scripts/program_policy_check.py:18-37` does not print `schema_version`, `deny_reason_codes`, `program_file_sha256`, `global_scope_sha256`, or `decided_at_utc`. An operator reading text output gets the old contract; the JSON path is complete. Add these fields to the text printer (or document explicitly that `--json` is the canonical surface for the versioned contract). One-screen change.

2. **Tag the provenance read so `_load_program_json` can drop.** The provenance hasher already opens the program file as bytes. Cache the bytes alongside the digest and pass them to the validator and `_load_program_json` instead of re-reading. Eliminates the small TOCTOU surface flagged in the P1-3 review and reduces the work to a single read. Best landed during P1-4 prep, not now.

3. **Structured target-parse reasons.** `policy.py:133` derives `IPV6_UNSUPPORTED` from `any("IPv6" in error for error in target_result.errors)`. The intent is clear and tested, but the contract is brittle: if `scope.py` rewords the error to "IP version 6 not supported" the policy layer silently degrades to `INVALID_TARGET`. Replace the string match with an explicit reason tag on `TargetParseResult` (e.g., `ParseReason.IPV6_UNSUPPORTED`) and have the policy layer dispatch on the tag.

4. **Dedup error strings.** `deny()` deduplicates codes but always appends the message. Repeated validator errors with the same code (e.g., several `PROGRAM_SCOPE_PARSE_ERROR` items) will list multiple distinct messages, which is good; the dedup on codes prevents the codes list from becoming a multiset. Consider deduping messages as well, so log analytics sees stable counts. Cosmetic.

5. **`url_prefix` default-port equivalence.** P1-3.1 locks "strict port semantic": prefix `https://api.example.test:8443/v1/` does not match target `https://api.example.test/v1/status`. This is consistent with the prior review's recommendation and is tested. However, prefix `https://api.example.test/` does not match target `https://api.example.test:443/` either, because `_parse_url_prefix` reads `parsed.port` literally (`None` vs `443`). This is documented behavior, but operators who write a port-less prefix often expect default ports to match. Either (a) document this case explicitly in `programs/README.md` Scope Semantics, or (b) normalize default ports inside `_parse_url_prefix`. Surface decision, not a defect.

6. **CIDR target risk surfacing.** A `cidr` target is a fan-out authorization. The decision currently records `target_type: "cidr"` and the matched scope reason, but nothing in the decision object warns the consumer that a single allow may legitimize thousands of hosts at execution. P1-4 design should either compute `target_cardinality_estimate` here, or refuse `cidr` targets at runtime without an explicit operator opt-in. Track as a P1-4 input, not a P1-3.1 regression.

## Strategic Recommendations (P1-4-Adjacent)

These map to the contract this hardening has now stabilized; they should land before any runtime consumer is allowed to act on a `policy_decision/1.0` allow.

1. **`schema_version` consumer enforcement.** Every future consumer (planned: `recon.sh --program`, module manifests, audit-log writer, report generator) must verify `schema_version == "policy_decision/1.0"` and fail closed on anything else. Add this as a one-line gate in each consumer's entry path. The contract is only as strong as the weakest reader.

2. **No-cache rule in runtime.** Document and enforce that runtime calls `decide_program_policy` once per stage with the current program file and current `config/scope.txt`, and never reads a stored allow. The `programs/README.md` text now warns about this; P1-4 implementation must mirror it in code (e.g., a single helper `policy_decide_or_abort()` that the stage entry calls and that cannot be bypassed by a "cached_decision" flag).

3. **Audit-log integration shape.** `audit_event` is still `PROGRAM_POLICY_ALLOW`/`PROGRAM_POLICY_DENY`. With `deny_reason_codes` available, the audit row should include `(audit_event, deny_reason_codes, program_file_sha256, global_scope_sha256, decided_at_utc, normalized_target, technique, mode)`. Define the exact log line in the P1-4 proposal so format drift is impossible.

4. **Effective rate-cap composition (carry-over from P1-3 review §3).** Still not addressed and still out of scope for P1-3.1. P1-4 should compute `min(program.rate_limits.*, config/recon.conf.*)` inside `scripts/core/` and return the result in the decision object, so scanners cannot pull faster than either source allows.

5. **Promote `scripts/core/scope.py` API surface.** `normalize_target`, `load_global_scope`, `entries_from_program_scope`, and `target_matches_any` are now load-bearing. Add `__all__`, docstrings, and a brief contract note ("ASCII/punycode only, no DNS, IPv4-only") at the top of the module before P1-4 starts importing them from `recon.sh` indirectly. Reduces accidental coupling drift.

6. **CIDR-fanout policy.** As above (Non-Blocking §6): decide whether `cidr` targets are allowed in P1-4 at all, or require an explicit `--allow-cidr` operator flag. Build this decision now; retrofitting after a runtime exists will be expensive.

7. **Test the validator-prefix and provenance-on-deny paths.** Two-line additions to existing tests will pin them. Cheap insurance.

## Safety/Scope Statement

Pure documentation/review artifact. This review file is the only thing this pass writes. No source code, configuration, scope file, scheduler, scanner, or runtime behavior was modified. No external request, DNS lookup, or target-touching command was executed. All evidence in this review is derived from reading the files and the local `git diff HEAD` only.

## Recommendation For Next Phase — P1-4 Readiness

**Proceed to P1-4 runtime integration planning.** P1-3.1 has stabilized the contract that P1-4 needs to consume:

1. **(Cowork)** Author `handoff/cowork_p1_4_proposal.md` covering:
   - Where in `recon.sh` the helper is invoked (per stage, before any target-touching command).
   - The no-cache rule and its enforcement shape.
   - The exact `logs/audit.log` row format derived from `policy_decision/1.0`.
   - The CIDR-fanout decision (deny by default, or explicit opt-in).
   - The `schema_version` consumer-side gate.
   - Effective rate-cap composition (`min(program, recon.conf)`).
   - Refusal of `--program` paths outside `programs/<slug>/scope.json`.
2. **(Codex)** Minimal P1-4 implementation: invoke `decide_program_policy` once per stage, abort the stage on deny, write the full decision object to `logs/audit.log` and to the run's evidence directory. No caching, no fallbacks, no override paths.
3. **(Cowork)** Independent review of P1-4 before any live target is allowed under `--program`.

Optional cleanup before P1-4 (none blocking):
- Land the single-read refactor (Non-Blocking §2).
- Bring CLI text output in line with the JSON contract (Non-Blocking §1).
- Replace IPv6 string-match with a structured reason tag (Non-Blocking §3).

P1-3.1 itself is ready to accept. Record this review in `handoff/accepted_changes.md` and proceed.
