> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.10 Direction Review — Dry-Run Recon-to-Runner Runtime Bridge

Reviewer identity:
- Reviewer route/tool: Hermes delegate_task subagent
- Visible model/runtime: exact child runtime not exposed
- Tier: T4-adjacent / T3+T4 hybrid. The implementation is a runner/platform-boundary change (T3) that consumes policy-boundary artifacts and affects dry-run/runtime safety decisions (T4 trigger), but the approved slice remains offline/dry-run-only with no activation.
- Hermes authority: conditional for implementation acceptance only if reviewers align, tests pass, and no activation occurs; escalation-only for any scanner/module/live/target-touching activation.

Decision:
- APPROVE_WITH_CHANGES

Summary:
- 建議允許實作一個非常窄的直接讀取橋接：`scripts/module_runner.py --policy-artifact <path>` 可讀取明確指定的 recon.sh dry-run `policy_boundary/1.0` artifact，路徑限於 `scans/<target>_<timestamp>/evidence/policy/policy_boundary_*.json` 或既有 `runs/<run_id>/policy/<file>`。
- 不批准任何自動探索、自動複製、recon.sh 旗標、掃描器執行、模組執行、scheduler/CI 連接、scope/config/schema/report/credential/deployment 變更。
- “WITH_CHANGES” 的原因不是概念阻擋，而是實作前必須加入明確 repo-root/path fail-closed 檢查與測試；現有 `module_runner.py` 只接受 `runs/<run_id>/policy/<file>` 形式。

OSS Recon Gate:
- references considered:
  1. SARIF
     - Useful pattern: run/artifact provenance, tool metadata, stable artifact URI/reference, deterministic hashes.
     - Adopt/adapt/ignore: ADAPT. 採用 artifact provenance/hash 與真實 artifact path 的可追溯性；不採用 SARIF 的完整 finding/result 結構。
     - Safety concern / reason not to copy directly: SARIF 偏向程式碼位置與掃描結果交換；直接套用會過度擴張 finding/report contract，可能把 triage output 誤當 confirmed finding。
     - Contract impact: policy decision path 應保留真實 repo-relative evidence path；run manifest 記錄 sha256；finding/evidence schema 不變；module manifest/profile/module I/O preview 不變；dry-run runner 僅讀取與驗證。
  2. ProjectDiscovery tools / JSONL pipeline ergonomics
     - Useful pattern: composable pipeline outputs, structured machine-readable artifacts, explicit handoff between stages.
     - Adopt/adapt/ignore: ADAPT. 採用「上游產生 artifact、下游明確讀取」的管線邊界；保留 explicit `--policy-artifact`。
     - Safety concern / reason not to copy directly: ProjectDiscovery tooling normally performs network-touching recon/enumeration;不得複製 live defaults、auto-pipeline 或 template execution 行為。
     - Contract impact: program scope 不變；policy decision artifact 可作離線輸入；run manifest/module I/O preview 可引用該 artifact；不得新增 scanner adapter 或 auto-discovery。
  3. Nuclei templates
     - Useful pattern: metadata, severity/tags, explicit unsafe/intrusive distinctions, template-driven validation mindset.
     - Adopt/adapt/ignore: ADAPT narrowly. 只採用 unsafe defaults must be denied 的思想，用於 module/profile constraints 與測試；不採用 template execution。
     - Safety concern / reason not to copy directly: Nuclei 的核心是 active scanning；即使 dry-run 字樣也可能容易被誤解成執行 preview。此 slice 不得引入 nuclei/template 執行或 recon scanner changes。
     - Contract impact: module manifest/profile 仍需 target_touching=false、network_access=false、dry_run=true；policy decision contract 不擴張；finding/evidence schema 不變。
  4. DefectDojo
     - Useful pattern: engagement/test lifecycle, dedup/status separation, triage vs verified lifecycle.
     - Adopt/adapt/ignore: IGNORE for implementation now; ADAPT conceptually for future lifecycle separation.
     - Safety concern / reason not to copy directly: DefectDojo 是完整 vulnerability management platform；現在導入會造成 reports/submission/lifecycle scope creep。
     - Contract impact: report/finding schema 不變；不建立 engagement/test import；run manifest 僅 planned preview。
  5. OWASP ZAP alert model
     - Useful pattern: risk/confidence/evidence separation and clear distinction between observed evidence and confirmed vulnerability.
     - Adopt/adapt/ignore: IGNORE for this bridge implementation; keep as future reporting reference.
     - Safety concern / reason not to copy directly: ZAP alerts derive from active web scanner behavior; copying alert semantics now could imply scanner-confirmed findings.
     - Contract impact: no finding/evidence/report promotion; module result previews stay `not_executed`, `findings: []`, `evidence: []`.
- adopt/adapt/ignore decisions:
  - Adopt/adapt: explicit artifact provenance, canonical sha256, stable repo-relative path, structured offline artifact handoff, unsafe defaults denied by tests.
  - Ignore/defer: active scanner execution patterns, automatic pipeline chaining, report/vulnerability lifecycle import, finding confirmation semantics.
- rejected unsafe patterns:
  - No ProjectDiscovery/Nuclei/ZAP-style active probing or template execution.
  - No recon artifact auto-location or automatic scan-to-run copying.
  - No DefectDojo-style report/submission/lifecycle integration in this slice.
  - No scanner output as confirmed finding.

Approved implementation boundary:
- in scope:
  - `scripts/module_runner.py` may be changed to accept explicit `--policy-artifact` paths in either:
    - existing `runs/<run_id>/policy/<file>` path; or
    - recon dry-run evidence path `scans/<target>_<timestamp>/evidence/policy/policy_boundary_*.json`.
  - Focused tests may be added/updated, especially `scripts/test_recon_runner_bridge_dry_run.py` or a narrow adjacent unit test file.
  - Handoff docs may be updated for review/implementation notes.
  - The bridge must read the artifact in place; no copy, move, normalization write, or auto materialization into `runs/`.
  - `plan.policy.decision_artifact_path` should reflect the real repo-relative evidence path when the explicit input is a recon evidence artifact, not a fabricated `runs/<run_id>/policy/decision.json`.
- out of scope:
  - No `recon.sh` changes.
  - No `config/scope.txt`, real program scope, schema, module manifest/profile, report, scheduler, CI, credentials, deployment, billing, production settings, OAuth/token/private-key changes.
  - No live target behavior, scanner/module execution, fuzzing, brute force, exploit attempts, callbacks/OAST, proxy/pivot/tunnel, beacon/relay, notification/webhook activation.
  - No `--auto-bridge`, `--from-recon`, `--recon-artifact`, `--auto-locate-policy`, run-directory scan, latest-scan lookup, glob-based discovery, or scheduler linkage.
- required fail-closed checks:
  - Mode remains `dry-run` only; any non-dry-run mode denies before plan emission.
  - Artifact must parse as JSON object and pass existing policy checks:
    - `schema_version == policy_boundary/1.0`
    - `boundary.status == allow`
    - `boundary.audit_event == PROGRAM_POLICY_ALLOW`
    - `boundary.errors`, `contract_errors`, `boundary_errors`, `deny_reason_codes` empty
    - `helper.returncode == 0`
    - `helper.timed_out is False`
    - `request.target` matches CLI target
    - `request.mode` matches CLI mode
    - embedded `decision.schema_version == policy_decision/1.0`
    - `decision.verdict == allow`
    - `decision.audit_event == PROGRAM_POLICY_ALLOW`
    - `decision.target`, `target_type`, and `mode` match CLI inputs
    - `decision.errors` and `decision.deny_reason_codes` empty
    - `warnings` and `reasons` are lists of strings
    - `program_slug`, `target_type`, `program_file_sha256`, `global_scope_sha256`, `decided_at_utc` are non-empty strings
    - sha256 fields are canonical 64-hex strings
    - `decided_at_utc` is canonical UTC timestamp.
  - Path must be explicit from `--policy-artifact`; no fallback discovery.
  - Resolve selected repo root from explicit runner context (`--discover-root` or `--profile-root`/profile root) and require artifact resolved path to stay under that repo root.
  - Reject path traversal and absolute/relative escapes after resolution.
  - Reject symlinked repo root, symlinked artifact file, and symlinked lexical/resolved parent segments from repo root to artifact.
  - For `runs/` policy artifacts: preserve existing requirement `runs/<run_id>/policy/<file>` and run_id match.
  - For `scans/` recon evidence artifacts:
    - resolved path includes a `scans/<scan-dir>/` ancestor under repo root;
    - immediate parent is exactly `evidence/policy`;
    - filename matches `policy_boundary_*.json`;
    - file is a regular file;
    - `scan-dir` is one path segment, not path traversal or symlink-expanded escape;
    - generated plan records repo-relative POSIX path such as `scans/<scan-dir>/evidence/policy/policy_boundary_....json`.
  - If artifact path is neither allowed `runs/` nor allowed `scans/` shape, deny and emit no plan.
  - If any validation error exists, verdict must be `deny`, return non-zero from CLI, and no `plan`, module I/O previews, preview bundle, findings, evidence, reports, or run writes should be emitted.
- required tests:
  - Positive: direct read of explicit recon evidence artifact in dry-run preview returns allow and `decision_artifact_path` equals repo-relative `scans/.../evidence/policy/policy_boundary_*.json`.
  - Positive: `decision_sha256` equals the exact bytes of the evidence artifact; no copied `runs/<run_id>/policy/decision.json` is created.
  - Negative: wrong target, target_type, mode, helper returncode, helper timeout, boundary audit event/status, decision verdict/audit event, non-empty errors/deny codes all deny with no plan.
  - Negative path tests: outside repo, wrong directory, wrong filename, missing `scans/<scan-dir>` ancestor, wrong parent (`evidence/other`, `policy` elsewhere), path traversal, symlink file, symlink parent, symlink repo root if feasible on platform.
  - Regression: runner/recon help contain no auto-bridge/from-recon/auto-locate flags.
  - Regression: no scanner/module execution markers; modules remain planned/not_executed; `findings` and `evidence` arrays stay empty.
  - Mutation safety: tests must use temp HACKLAB/repo fixture and verify real repo protected dirs (`runs`, `scans`, `loot`, `reports`, `evidence`) and `config/scope.txt` are unchanged.
  - Persistence safety: if `--persist-preview-bundle` is used in tests, it must still write only the explicit preview bundle under the temp repo `runs/<run_id>/preview`; direct-read bridge must not copy policy artifacts.

Codex/implementation guidance:
- files allowed:
  - `scripts/module_runner.py`
  - focused tests, preferably `scripts/test_recon_runner_bridge_dry_run.py` and/or a narrow path-validation unit test file under `scripts/`
  - handoff docs for task/result/review notes
- files forbidden:
  - `recon.sh`
  - `config/scope.txt`
  - real `programs/*/scope.json` activation files except inert test fixtures already present/explicitly temp-copied in tests
  - schemas unless a separate T3 review approves schema changes
  - modules/check runtime code, scanners, reports, scheduler/CI, credentials, deployment/billing/production settings
- acceptance checks:
  - Python syntax/targeted tests for module_runner and bridge dry-run behavior.
  - No scan or target-touching commands during implementation verification beyond existing dry-run test harness if explicitly allowed by parent; for this direction review no scans were run.
  - `git diff`/review must show no runtime-code changes outside allowed files and no recon.sh/config/scope changes.
  - Final implementation review must re-check OSS Recon Gate alignment and path-fail-closed tests.

Safety boundary:
- operator approval required before activation: yes for any activation beyond this dry-run direct-read preview. Existing operator authorization is sufficient to proceed with offline implementation if all blocked surfaces remain blocked; it is not sufficient to activate scanner/module/live behavior.
- target-touching/scanner/module execution status: prohibited. The bridge reads JSON and constructs preview data only. It must not invoke recon.sh, scanner tools, module code, subprocess scanners, network clients, callbacks, notifications, or write findings/evidence/reports.

Review questions answered:
1. Decision: APPROVE_WITH_CHANGES.
2. Tier: T3 platform/runner boundary plus T4 trigger because it consumes policy artifacts and dry-run runtime safety decisions. Treat as T4-adjacent; implementation can proceed only as offline dry-run preparation.
3. Operator approval: sufficient for this dry-run-only implementation path if no activation or scope/config changes occur; not sufficient for live execution.
4. Runner should accept explicit recon evidence paths, not require copied `runs/<run_id>/policy/decision.json`, because direct read reduces copy drift and avoids creating a second source of truth.
5. Direct read is safer than runtime copying because it preserves provenance and sha256 of the original recon-emitted artifact, avoids stale/tampered copied bytes, avoids writes into run dirs, and makes audit path truthful.
6. Exact fail-closed checks: listed above under required fail-closed checks.
7. `decision_artifact_path` should reflect the real explicit recon evidence path for recon evidence artifacts; only existing run-policy artifacts should record `runs/<run_id>/policy/<file>`.
8. Mandatory tests: listed above under required tests.
9. Blocked until T4/T5 approval: live target behavior, scanner/module execution, recon.sh bridge flags, auto-discovery/copying, scheduler/CI/deployment/credentials, scope/config activation, reports/submission, callbacks/OAST/proxy/pivot/tunnel.
10. Minimal implementation scope: `module_runner.py` + focused tests + handoff docs only; recon.sh unchanged.

Blocking issues:
- No conceptual blocker for the narrow dry-run direct-read bridge.
- Implementation must not proceed if it cannot identify a selected repo root and enforce repo-local/symlink/path-shape checks fail-closed.
- Any proposal to add auto-discovery, recon.sh flags, copy behavior, scanner/module execution, or schema/report/scheduler changes is outside this approval and should be BLOCK/DEFER.

Non-blocking recommendations:
- Prefer extracting path classification into a small pure helper, e.g. classify allowed policy artifact path as `runs_policy` or `recon_evidence`, to simplify tests.
- Keep error messages stable enough for negative tests, but avoid adding new public CLI flags beyond existing `--policy-artifact`.
- Document in handoff that this bridge is not a recon runner integration; it is only an explicit artifact reader for dry-run preview.
- Consider future schema-level provenance only after a separate T3 review; not needed for P3.10.

Final Decision Block:
Decision: APPROVE_WITH_CHANGES
Tier: T4-adjacent / T3+T4 hybrid
Milestone: P3.10 dry-run recon-to-runner runtime bridge
Hermes authority: conditional for offline implementation acceptance; escalation-only for activation/live behavior
Reviewers consulted:
- Hermes delegate_task subagent; visible model/runtime: exact child runtime not exposed
Validation performed:
- Design-only local review of `.hermes.md`, `handoff/cowork_p3_10_direction_prompt.md`, `handoff/review_tiering_policy.md`, `handoff/multi_party_review_decision_policy.md`, `handoff/oss_recon_gate.md`, `scripts/module_runner.py`, and `scripts/test_recon_runner_bridge_dry_run.py`.
- No scans, target-touching commands, scanner/module execution, or tests were run for this direction review.
Blocking findings:
- None for the narrow approved concept.
- Blocking if implementation omits repo-root/path/symlink fail-closed checks or broadens scope beyond explicit dry-run read-only `--policy-artifact`.
Non-blocking recommendations:
- Use a small pure path-classification helper; keep provenance path truthful; defer schema/report/lifecycle expansion.
Safety boundary:
- Dry-run preview only; read explicit JSON artifact only; no recon.sh changes; no scanner/module/live execution; no target-touching; no copies; no auto-discovery; no scope/config changes.
OSS Recon Gate:
- Applied using local catalog references: SARIF, ProjectDiscovery, Nuclei, DefectDojo, OWASP ZAP. Adopt/adapt provenance and explicit artifact handoff; reject active scanning, auto-pipelines, and report/finding promotion.
User approval required:
- No additional operator approval required for this offline implementation if the approved boundary is preserved.
- Yes, explicit operator approval required before any activation, live target behavior, scanner/module execution, scheduler/deployment, credential, scope/config, report submission, proxy/pivot/tunnel, callback/OAST, or production-side change.
Next action:
- Proceed to minimal implementation in `scripts/module_runner.py` plus focused tests and handoff docs only, with `recon.sh` unchanged, or route back if implementer needs to broaden the boundary.
