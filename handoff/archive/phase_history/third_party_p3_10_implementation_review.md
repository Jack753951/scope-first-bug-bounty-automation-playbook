> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.10 Implementation / Safety Review — Explicit Recon Policy Evidence Direct-Read Bridge

Reviewer identity:
- Reviewer route/tool: Hermes delegate_task subagent
- Visible model/runtime: exact child runtime not exposed
- Review date: 2026-05-20
- Scope reviewed: current uncommitted P3.10 diff for `scripts/module_runner.py`, `scripts/validate_run_manifest.py`, `scripts/test_recon_runner_bridge_dry_run.py`, `scripts/test_run_manifest_schema.py`, plus direction review context.

Final verdict: PASS_WITH_RECOMMENDATIONS

## Executive summary

此實作大致符合 P3.10 方向：維持 dry-run-only、只接受明確 `--policy-artifact`、直接讀取 recon evidence artifact，不自動探索、不複製、不執行 scanner/module，也未變更 `recon.sh` 或 `config/scope.txt`。

我沒有發現需要 BLOCK/ROUTE_BACK 的安全阻擋缺陷。主要建議是在合併前補強少量 path edge-case 測試，特別是「相對於 explicit repo root 的 relative policy artifact path」與 traversal/symlink coverage，以避免後續誤用或平台差異造成退化。

## Local inspection / validation performed

Safe local-only checks performed:
- `git diff -- scripts/module_runner.py scripts/validate_run_manifest.py scripts/test_run_manifest_schema.py scripts/test_recon_runner_bridge_dry_run.py handoff/cowork_p3_10_direction_review.md`
- `git status --short`
- `git diff --name-only && git diff --check`
- `git diff -- recon.sh config/scope.txt`
- Targeted file reads of the changed implementation and test sections.
- Targeted safe unit test: `python -m unittest scripts.test_run_manifest_schema.RunManifestSchemaTests -v`

Observed validation result from this review:
- `scripts.test_run_manifest_schema.RunManifestSchemaTests`: OK, 12 tests.
- `git diff --check`: no diff-check error output; only line-ending warnings for some Python files.
- `git diff -- recon.sh config/scope.txt`: empty; no changes observed.

I did not run scans or target-touching commands. I also did not rerun the bridge dry-run test class because it invokes the recon dry-run harness; parent context already reports it passed, and this review was limited to safe git/read/test inspection.

## 1. Blocking defects

None found.

Implementation behavior reviewed:
- `scripts/module_runner.py` replaces the old run-only path classifier with `_repo_local_policy_artifact_path(...)`.
- Accepted path shapes are constrained to:
  - `runs/<run_id>/policy/<file>` with run_id match; or
  - `scans/<scan-dir>/evidence/policy/policy_boundary_*.json`.
- The selected repo root is resolved from runner context (`profile_root`, driven by `--discover-root`/`--profile-root` in normal CLI flow).
- The implementation denies paths outside the selected repo root after resolution.
- It rejects symlinked repo roots, symlinked artifact files, symlinked lexical/resolved parent segments, and non-regular existing files.
- It records the truthful repo-relative policy path in `plan.policy.decision_artifact_path` and computes `decision_sha256` from the explicit artifact bytes.
- Existing policy artifact validation remains fail-closed for allow-only policy boundaries and matching target/type/mode.
- On errors, the runner returns deny without plan emission.

No runtime copy, auto-discovery, latest-scan lookup, scanner execution, module execution, finding/evidence promotion, report generation, scheduler/CI/deployment/credential changes, or scope/config activation were observed in the reviewed diff.

## 2. Safety/security concerns

No blocking safety concern found.

Non-blocking safety observations:

1. Relative path with explicit repo root should be tested and possibly normalized before read.
   - `_repo_local_policy_artifact_path(...)` classifies a relative `policy_artifact_path` against the selected `repo_root` by constructing `repo / raw_path`.
   - However, `build_dry_run_plan(...)` still calls `_load_json_file(policy_path, ...)` and `sha256_file(policy_path)` using the original raw path, not the resolved repo-local path returned/used by classification.
   - If the CLI is invoked from a cwd different from the selected repo root and the operator supplies a repo-relative `scans/...` or `runs/...` path, classification can accept the intended repo-local artifact while the subsequent read/hash may resolve relative to cwd instead.
   - Current tests use absolute artifact paths, so this edge is not covered.
   - This is not a direct escalation risk because wrong/missing files fail closed, but it can cause false denies or provenance/read mismatch in non-default invocation layouts. Recommendation: add a test for repo-relative explicit paths when cwd differs from `--discover-root`/`--profile-root`; if it fails, adjust runtime to read/hash the resolved repo-local artifact path.

2. Traversal canonicalization is accepted if it resolves back into an allowed shape.
   - Runtime path classification resolves before shape checks; a benign lexical traversal such as a path containing `../` that canonicalizes back into `scans/<scan-dir>/evidence/policy/...` may be accepted.
   - The manifest validator rejects traversal segments in `policy.decision_artifact_path`, and the emitted plan records the canonical repo-relative path, so the persisted contract remains clean.
   - Direction review asked to reject traversal/escapes; current behavior clearly rejects escapes after resolution, but lexical traversal-specific denial would benefit from a dedicated test/decision.

3. Runtime scan-dir strictness is looser than manifest regex.
   - Runtime only ensures one segment after `scans/` and rejects `.`, `..`, slash/backslash; manifest validation later requires `scans/[A-Za-z0-9][A-Za-z0-9._-]{2,255}/...`.
   - Because generated plans are validated by `validate_run_manifest.validate_run(plan)`, malformed scan-dir paths should still deny before plan emission.
   - Recommendation: keep/expand tests to assert malformed scan-dir paths deny via final run-manifest validation.

## 3. Architecture/roadmap fit

PASS.

The implementation matches the approved minimal bridge architecture:
- Direct-read only, no copy/materialization into `runs/<run_id>/policy` for recon evidence artifacts.
- Explicit `--policy-artifact` only; no new bridge-specific flags were found in `module_runner.py` for `--auto-bridge`, `--from-recon`, `--auto-locate`, or `--recon-artifact`.
- `plan.policy.decision_artifact_path` truthfully records `scans/.../evidence/policy/policy_boundary_*.json` when the explicit input is recon evidence.
- Existing run-policy artifact support remains intact for `runs/<run_id>/policy/<file>`.
- Run manifest validator is narrowly expanded only for policy decision artifact paths; finding/evidence artifact paths remain run-local.
- No schema/report/lifecycle expansion was introduced.

This is consistent with the roadmap goal of preserving provenance and reducing copied-artifact drift without activating recon-to-runner automation.

## 4. OSS Recon Gate alignment

PASS.

The implementation aligns with the prior OSS Recon Gate decisions:
- Adopts/adapts SARIF-like provenance principles: stable artifact path plus exact sha256.
- Adopts/adapts ProjectDiscovery-style explicit artifact handoff, but without pipeline auto-chaining or active recon execution.
- Keeps Nuclei/ZAP-style active scanner/template behavior out of scope.
- Does not introduce DefectDojo-style lifecycle/report submission or finding promotion.
- Maintains scanner output as policy evidence only, not confirmed vulnerability evidence.

Rejected unsafe patterns remain rejected:
- No active probing or scanner/template execution.
- No auto-location of latest scan artifacts.
- No scanner output promoted into findings/evidence arrays.
- No reports, scheduler, callbacks/OAST, proxy/pivot/tunnel, credentials, deployment, or production linkage.

## 5. Required additional tests / recommendations

Recommended before merge, but not blocking this review verdict:

1. Add a direct-read positive test for repo-relative `--policy-artifact` with cwd intentionally different from selected `--discover-root` / `--profile-root`.
   - Expected: runner reads and hashes `<selected_repo_root>/scans/.../evidence/policy/policy_boundary_*.json`, emits the repo-relative `scans/...` path, and does not depend on process cwd.

2. Add lexical traversal negative tests if the intended contract is to reject any `.`/`..` segment in the user-supplied artifact path, even when it canonicalizes back under the repo root.
   - If the team intentionally accepts canonicalized in-repo traversal, document that explicitly; manifest output already remains canonical.

3. Add explicit runtime scan-dir malformed tests aligned to the manifest regex.
   - Examples: too-short scan dir, leading unsupported char, or unexpected characters.
   - Expected: deny with no plan.

4. Keep or extend symlink tests where platform privileges allow.
   - The implementation has symlink checks; Windows may skip symlink creation tests. Ensure non-Windows CI covers symlinked repo root, symlinked artifact file, and symlinked parent directory.

5. If not already covered in the full reported test run, add/keep a test proving direct-read plus `--persist-preview-bundle` still does not copy the policy artifact and writes only preview data under `runs/<run_id>/preview`.

## 6. Final decision block

Decision: PASS_WITH_RECOMMENDATIONS

Blocking findings:
- None.

Non-blocking recommendations:
- Add relative-path-with-explicit-root coverage and, if needed, normalize the artifact read/hash path to the resolved repo-local path.
- Add/clarify traversal, malformed scan-dir, and symlink-parent/file/root tests.

Safety boundary confirmed:
- Dry-run-only policy evidence direct read.
- No `recon.sh` change observed.
- No `config/scope.txt` change observed.
- No auto-bridge/from-recon/auto-locate behavior observed.
- No scanner/module/live/target-touching behavior introduced in the reviewed diff.
- No finding/evidence/report/schema/scheduler/deployment/credential/scope activation introduced.

Overall: safe to proceed within the approved P3.10 boundary, with the above test hardening recommended before final merge.
