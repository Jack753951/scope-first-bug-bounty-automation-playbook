> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Codex Engineering/Safety Review - P1-4 Runtime Integration Proposal

Generated: 2026-05-15
Reviewer: Codex
Scope: review-only. No scans, probes, target-touching commands, or runtime/config/test/source edits performed.

Files reviewed:

- `.hermes.md`
- `handoff/cowork_p1_4_proposal.md`
- `handoff/cowork_phase1_p1_3_1_review.md`
- `programs/README.md`
- `scripts/program_policy_check.py`
- `scripts/core/policy.py`
- `scripts/core/scope.py`
- `recon.sh`
- `config/recon.conf`

Additional read-only vocabulary checks used `programs/_schema/scope.schema.json` and existing example program JSON files because the task explicitly asked to verify technique vocabulary alignment.

## Verdict

**ROUTE_BACK_FOR_DESIGN_FIXES**

The proposal has the right high-level safety shape: layer program policy on top of `safe_target`, deny on uncertainty, do not cache decisions, and keep `--program` opt-in. It is not ready for a Codex implementation task yet because several concrete details conflict with the current schema/helper/recon behavior. The most serious issues are technique vocabulary mismatches, a `policy_preflight` call that would deny every `--program` run, and a dry-run/planned/live matrix that permits real tool execution while using the helper's lenient `dry-run` policy mode.

## Blocking Issues

1. **Technique vocabulary mismatches would cause systematic denies.**

   The schema enum contains `directory_bruteforce`, not `dir_bruteforce` (`programs/_schema/scope.schema.json:515-521`). The proposal maps the `dir_bruteforce` stage to technique `dir_bruteforce` (`handoff/cowork_p1_4_proposal.md:139`), so the helper would emit `TECHNIQUE_NOT_ALLOWED` for valid program files. The proposal also uses `webhook_notification` for `send_notifications` and `policy_preflight` for `initial_target` (`handoff/cowork_p1_4_proposal.md:141,148`), but neither value exists in the schema enum or examples.

   This is not cosmetic. `scripts/core/policy.py` checks `technique in techniques.allowed` and denies otherwise (`scripts/core/policy.py:217-224`). As proposed, `policy_preflight` at `initial_target` would deny every `--program` run before any stage could start unless every real program file were somehow updated with a non-schema technique.

   Required design fix: use only existing enum values for stage decisions, or explicitly propose a schema/validator/example update before runtime integration. The initial preflight should not be modeled as a technique unless it is added to the contract. Prefer a separate helper/env/file-read precheck that validates program path, global scope readability, helper availability, and schema parseability without asking `decide_program_policy` to authorize a fake technique.

2. **The live execution matrix promotes a dry-run policy allow into target-touching execution.**

   The proposal defaults `--policy-mode` to `dry-run` and allows `--program` without `--dry-run` to execute tools while the helper uses `mode=dry-run` (`handoff/cowork_p1_4_proposal.md:73,437`). That bypasses the helper's stricter `planned`/`live` checks for `automation_permitted=true` and testing windows (`scripts/core/policy.py:225-241`) while still permitting network tools to run.

   This contradicts the P1-3.1 contract in `programs/README.md:114-116`: a dry-run allow must never be promoted to planned or live execution without rechecking in the stricter requested mode.

   Required design fix: if `recon.sh` is not in `--dry-run`, then `--program` must require `--policy-mode planned` or `--policy-mode live`, or the runtime must automatically use a strict execution mode. `--policy-mode dry-run` should be valid only when `--dry-run` is set.

3. **Rate-limit composition references non-existent schema keys.**

   The proposal table uses `requests_per_second`, `concurrency`, `concurrency_web`, and `concurrency_dir` (`handoff/cowork_p1_4_proposal.md:409-415`), and the test plan uses `rate_limits.requests_per_second` (`handoff/cowork_p1_4_proposal.md:498`). The actual schema keys are `max_concurrency`, `max_requests_per_second`, `request_delay_ms`, `nuclei_rate_limit`, `nuclei_concurrency`, `naabu_rate`, `httpx_threads`, and `subfinder_threads` (`programs/_schema/scope.schema.json:166-212`).

   Required design fix: replace the table and tests with the actual schema keys before implementation. If `FEROX_THREADS` has no schema key, say so and leave it unchanged. Do not add runtime code around imaginary keys and defer correctness to a later phase.

4. **Initial precheck ordering conflicts with mandatory artifact write semantics.**

   The proposal requires policy decisions to be written under the run evidence directory before the wrapper can return success (`handoff/cowork_p1_4_proposal.md:113-120,250,290`). But the proposed `initial_target` call is placed immediately after `safe_target`, before the current `run_pipeline` computes and creates `outdir` (`recon.sh:899-913`).

   Required design fix: specify whether `run_pipeline` creates the run directory before initial policy preflight, or whether preflight artifacts live in a separate pre-run location. If an allowed preflight cannot be recorded, execution must fail closed as the proposal says. The design should also state that creating an output directory for a denied `--program` run is acceptable.

5. **JSON parsing and timeout handling are under-specified for a no-new-dependency bash/Python boundary.**

   The proposal says bash parses `--json` output and enforces schema, verdict, hashes, and deny codes, while also adding no new dependency (`handoff/cowork_p1_4_proposal.md:57,113-120,619`). Current `recon.sh` uses `jq` only opportunistically for scanner output, and `jq` cannot become required for the policy gate. A grep/sed parser would be unsafe for this contract, and `timeout` is an external command that the proposal does not require or replace.

   Required design fix: define a jq-free parser/timeout strategy. The cleanest option is a small stdlib Python wrapper that invokes `scripts/program_policy_check.py` with `subprocess.run(..., timeout=...)`, validates the `policy_decision/1.0` JSON, writes the artifact atomically, and returns a small stable shell-readable result. Bash should not parse nested JSON with text tools.

6. **The no-behavior-change requirement for runs without `--program` is internally inconsistent.**

   The proposal says no-`--program` behavior must be byte-identical (`handoff/cowork_p1_4_proposal.md:122`) but later permits "modulo new no-op log lines" (`handoff/cowork_p1_4_proposal.md:176`) and even asks for no-op log lines containing `policy gate not active` (`handoff/cowork_p1_4_proposal.md:507`). V1 then says no policy events in audit log (`handoff/cowork_p1_4_proposal.md:519`).

   Required design fix: make the rule absolute. When `--program` is unset, no new stdout/stderr lines, no new audit rows, no new files, no helper checks, and no Python/tool availability checks should occur.

## Non-Blocking Improvements

- Use synthetic `.test` or temp-fixture targets in tests instead of `scanme.nmap.org`. Dry-run should not touch the target, but test fixtures should still avoid normalizing real public targets into acceptance examples.
- Update `scripts/program_policy_check.py` text output in a separate cleanup so operators see schema version, deny codes, hashes, and decision time outside `--json`. The JSON path is already the canonical contract.
- Consider moving audit-row formatting to a tiny Python helper sooner than P2. The proposed row has enough escaping and field-count requirements that duplicating it in bash will be fragile.

## Implementation Cautions

- `safe_target` strips URL paths and normalizes URLs to `scheme://host[:port]` (`recon.sh:431-465`). Program `url_prefix` path semantics in `scripts/core/scope.py` will not be meaningful if P1-4 always passes `SAFE_TARGET_VALUE` after path stripping. Decide whether this is acceptable for P1-4 or whether the helper should receive the original URL after `safe_target` has validated it.
- Domain enumeration denial needs an explicit fallback file behavior. The proposal says denied `enum_subdomains` falls back to the single-host path, but current `run_pipeline` blindly copies `subdomains.txt` after `enum_subdomains` (`recon.sh:923-925`).
- Stage integration must account for both list-level filters and loop-level calls. `service_fingerprint`, `dir_bruteforce`, and `vuln_scan` have tool-invocation loops or list invocations that need the policy gate immediately before command execution, not only earlier in the pipeline.
- Audit write failures on an allow path must fail closed for policy-gated execution. The existing `audit_log` function appends without checking failure (`recon.sh:249-257`); do not copy that behavior for the new policy artifact/audit path.
- `--program` validation must not check helper availability, create directories, or emit warnings when `--program` is unset.

## Recommended Task Breakdown After Design Fixes

1. **Design patch:** fix technique vocabulary, remove or redesign `policy_preflight`, correct the mode matrix, and replace the rate-limit table with actual schema keys.
2. **Boundary helper:** implement a jq-free stdlib Python wrapper for timeout, JSON contract validation, atomic artifact writing, and shell-readable status.
3. **CLI validation:** add `--program`, `--policy-mode`, and optional CIDR flag validation with zero side effects when `--program` is unset.
4. **Initial precheck and artifacts:** create the run evidence directory before any allowed policy decision can proceed, and fail closed on artifact write failure.
5. **Per-stage gates:** wire corrected technique names into the recon stages, preserving `safe_target` as the first gate.
6. **Rate caps and docs:** compose only existing schema/config keys, record effective caps, update `programs/README.md`, and run backwards-compat regression proving no behavior change without `--program`.

## Safety Statement

This review wrote only `handoff/codex_p1_4_proposal_review.md`. No runtime code, tests, config, scope files, or scanner behavior were modified. No scan, probe, DNS lookup, curl request, or target-touching command was executed.

## Re-review After Design Fixes

Generated: 2026-05-15
Scope: review-only. Re-read `handoff/cowork_p1_4_proposal.md` and this review file. No scans, probes, target-touching commands, or runtime/config/scope/test/source edits performed.

Verdict: **ACCEPT_FOR_IMPLEMENTATION**

The prior blockers are resolved at design level:

- Technique vocabulary now maps only to schema enum values, including `directory_bruteforce`; `webhook_notification` is removed; `send_notifications` is not policy-gated.
- `policy_preflight` is removed as a policy decision. The replacement is a non-decision environment/file/helper precheck and does not emit `policy_decision/1.0`.
- The mode matrix rejects `--policy-mode dry-run` unless `--dry-run` is also set, and `--program` requires an explicit `--policy-mode`.
- Rate-limit composition uses actual schema keys: `naabu_rate`, `nuclei_rate_limit`, `nuclei_concurrency`, `httpx_threads`, `subfinder_threads`, with `max_concurrency`, `max_requests_per_second`, and `request_delay_ms` recorded only. `FEROX_THREADS` is left unchanged.
- Artifact ordering is fixed: the run output and `evidence/policy/` directories are created before any `policy_decide` call; denied `--program` runs may still create the run directory.
- The jq-free boundary is now specified as `scripts/program_policy_boundary.py`, using Python stdlib JSON parsing, subprocess timeout handling, contract validation, atomic artifact writes, and shell-readable status output.
- No-`--program` behavior is now absolute: no helper/Python checks, no new files, no audit rows, and no stdout/stderr changes.

Remaining items are implementation cautions, not design blockers: preserve `safe_target` as the first gate, keep all no-`--program` paths side-effect-free, fail closed on artifact/audit write failures for allow paths, and validate the full V1-V20 matrix before merge.
