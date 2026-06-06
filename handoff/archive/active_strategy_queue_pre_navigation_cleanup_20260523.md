> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Active Strategy Queue

Status: active
Source: Hermes synthesis of current handoff state
Date: 2026-05-20
Repo truth: `handoff/accepted_changes.md`, `handoff/p3_9_closeout_next_direction_20260520.md`, `handoff/phase4a_controlled_lab_calibration_plan_20260520.md`, `scripts/test_recon_runner_bridge_dry_run.py`, `.hermes.md`

## Purpose

This is the compact current-navigation layer for the cybersec lab. It is intentionally shorter than `handoff/accepted_changes.md` and should be updated at milestone boundaries, closeout reviews, and direction-review decisions.

The queue answers: what is active now, what is next, what is deferred, and what is blocked until operator approval.

## Long-term goal

The Cybersec Lab long-term goal explicitly includes automation. The project is building a policy-gated, scope-aware, script-first automation platform for authorized bug-bounty / pentest work: collect preview and recon context, choose existing module bundles or bounded script combinations, execute only under the appropriate local-lab or authorized-scope gates, review candidate/observation output, modularize useful checks, and support evidence/report-readiness workflows without automatic finding confirmation or submission.

Automation is therefore a core project outcome, not a side effect. Safety gates, manifests, profiles, validators, and review artifacts exist to make automation bounded, auditable, reusable, and authorization-aware; they should not replace the operator-facing script-first automation loop.

## 2026-05-21 Current Update

Phase 4B is still the active project phase, but the architecture direction has been reset by operator correction: the project should use a script-first, context-driven module loop instead of continuing contract-first / safety-process-first scaffolding. The accepted reset is recorded in `handoff/phase4b_script_first_architecture_reset_20260521.md`, with the operator-facing script map in `scripts/SCRIPT_INVENTORY.md` and the new bundle direction in `modules/bundles/`.

Current safe next lane:

- 2026-05-22 attacker route migration: default attacker/target-touching VM is now `<attacker-vm>`, cloned from healthy `kali-linux-2026.1-virtualbox-amd64`, configured with 4096 MB RAM and 4 CPUs, host-only NIC1 default, NIC2/NAT closed after temporary tool recovery, and clean snapshot `clean-attacker-v2-tools-4096m-4cpu-20260522` (`bcee6035-c86d-41f0-8da1-62b3b42ec388`). Host-only IP evidence remains `<lab-ip>`; use `<victim-vm>` at `<lab-ip>` for vulnerable targets. Old registered `<inaccessible>` `<attacker-vm>` is deprecated/forensic archive only, not the current route.

- 2026-05-22 lab route refresh/source-driven test update: previous temporary working attacker VM was `kali-linux-2026.1-virtualbox-amd64` at `<lab-ip>`; the old registered `<inaccessible>` `<attacker-vm>` entry is stale and should not be used for current routing. Victim VM `<victim-vm>` was reset/reached at `<lab-ip>`; Juice Shop is healthy at `:3000`, WebGoat redirects at `:8080/WebGoat/`. No tool redownload needed: Kali tools and downloaded source repos remain present. New compact handoff: `handoff/compact_status_and_vuln_source_test_20260522.md`; source-driven parameter-discovery artifact: `<artifact-output-dir>/source_driven_param_discovery_fallback_retry_20260522T110522Z/`; follow-up bounded Juice Shop `q` SQLi behavior artifact: `<artifact-output-dir>/juice_q_sqli_bounded_wave_20260522T110815Z/` with handoff `handoff/juice_q_sqli_bounded_wave_20260522.md`. Next lane can promote/refine this as a reusable single-vulnerability module/bundle, or deliberately open a temporary NAT window to install Arjun dependencies before rerunning the full tool.

- `<specific-cve-id>` kernel/local lane has been triaged non-destructively and is likely locally relevant but not proven exploitable. Victim-lab has kernel `6.18.12+kali-amd64` / `6.18.12-1kali1`, `CONFIG_RDS=m`, RDS module files present, and RDS not loaded. Upstream fix `e174929793195e0cd6a4adb0cad731b39f9019b4` adds `rm->data.op_nents = 0` in `net/rds/message.c`. Handoff: `handoff/cve_2026_43494_kernel_lane_triage_20260522.md`; artifacts: `<artifact-output-dir>/cve_2026_43494_kernel_lane_20260522/`. Destructive testing is blocked until operator manually recovers `<attacker-vm>`, which is stuck in VirtualBox `livesnapshotting` after a live snapshot attempt; use powered-off clone/snapshot for any RDS module-load/crash/LPE testing.

- DVWA command-injection true attacker-side callback wave completed: after Docker was installed on `<attacker-vm>`, verified one-vulnerability max-impact chain `command injection -> www-data OS command execution -> /tmp marker write/readback -> outbound callback to attacker VM <lab-ip>:18182`. Artifact: `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/`; callback evidence: `attacker_docker_callback/requests.jsonl`; handoff: `handoff/dvwa_command_injection_true_attacker_callback_20260522.md`; bundle: `modules/bundles/verified_lab_flow_dvwa_command_injection_true_attacker_callback.md`. Temporary target/listener containers removed; aggressive-lab NAT closed and Internet verified unavailable; Juice Shop/WebGoat still reachable. Next max-impact lane can reuse aggressive-lab Docker listener for SSRF/XXE/deserialization/WebGoat callback-style proofs without reopening NAT unless new images are needed.

- DVWA command-injection callback-control wave 2 completed: verified `www-data` command execution, lab marker write/readback, and Docker-bridge callback record with matching marker in `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T054954Z/callback_docker_listener/requests.jsonl`; handoff `handoff/dvwa_command_injection_callback_wave2_20260522.md`; source inventory `handoff/vulnerability_source_coverage_inventory_20260522.md`. Important limitation: this is local Docker-bridge callback, not true attacker-VM callback; aggressive-lab inbound is blocked except SSH and has no Docker runtime. Next max-impact infra lane: give aggressive-lab a Docker-published listener or operator-approved host-only firewall opening, then rerun for true attacker-side callback.

- DVWA command-injection impact wave 1 completed against disposable Docker-backed DVWA on `<victim-vm>`: verified OS command execution as `www-data` and lab marker file write/readback under `/tmp`, with artifacts `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T052046Z/`; handoff `handoff/dvwa_command_injection_impact_wave1_20260522.md`; bundle `modules/bundles/verified_lab_flow_dvwa_command_injection_container_control.md`. Callback/control was attempted but not verified because high-port listeners on aggressive-lab/Windows host were unreachable; next max-impact infrastructure lane should build a Docker-published callback listener or operator-approved host-only callback port before claiming external callback/control.

- WebGoat JWT wave 3 completed against Docker-backed WebGoat after authenticated wave 2: added `scripts/labs/webgoat_jwt_wave3.sh`, verified the bounded JWT decode assignment (`/WebGoat/JWT/decode`, decoded user value `user`, `lessonCompleted=true`), and mapped future JWT lanes for signing/role escalation, weak keys, refresh tokens, JKU, and KID. Artifacts: `<artifact-output-dir>/webgoat_jwt_wave3_20260522T045749Z/`; handoff: `handoff/webgoat_jwt_wave3_20260522.md`; bundle: `modules/bundles/verified_lab_flow_webgoat_jwt_decode_token_inspection.md`. Next WebGoat lanes: JWT weak-key/signing or refresh-token manipulation, reflected XSS runtime proof after fixing/replacing browser driver, and Path Traversal safe-marker proof.

- WebGoat authenticated wave 2 completed against Docker-backed WebGoat: throwaway users/session handling now works, authenticated lesson menu enumeration confirmed IDOR/JWT/CrossSiteScripting/PathTraversal lanes, and first verified WebGoat Access Control / IDOR proof is recorded. Artifacts: `<artifact-output-dir>/webgoat_authenticated_wave2_20260522T040820Z/`; handoff: `handoff/webgoat_authenticated_wave2_20260522.md`; bundle: `modules/bundles/verified_lab_flow_webgoat_idor_lesson_access_control.md`.

- Verified exploit-flow rerun wave 1 completed with artifacts under `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/`: promoted SQLi auth-bypass + `/api/Users` read, unauth admin config read, `/ftp/` listing/file-read, and API-docs/metrics exposure to lab-only verified-flow bundles; recorded JWT/coupon/XSS/source-map/tooling blockers in `attempted_not_verified_flows_wave1.md`. Correction: target-touching work must default to Kali, not Windows host. Kali verified-flow wave 2 corrected the route via `<attacker-vm>`, reran `ffuf`/`nikto`/`nmap`/`sqlmap`-class tooling, reconfirmed SQLi auth-bypass from Kali, and added `verified_lab_flow_file_upload_marker_pdf` for authenticated upload state-change evidence; artifacts under `<artifact-output-dir>/kali_verified_flow_wave2_20260522T001525Z/` and `<artifact-output-dir>/kali_verified_flow_wave2b_20260522T001740Z/`.

- New intelligence lane: CISA KEV, NVD, Exploit-DB, GitHub PoC/tooling, and HTB/training-lab patterns are now explicit OWASP/CVE lab-test sources. Official KEV JSON was fetched to `cves/cisa_kev_catalog_latest.json`; pattern candidates were written to `cves/cisa_kev_lab_pattern_candidates_20260522.json`; mapping/backlog lives at `handoff/cisa_kev_owasp_cve_lab_mapping_20260522.md`. NVD recent modified, Exploit-DB CSV, and GitHub lab/tool searches were mirrored/summarized in `handoff/external_vuln_intel_sources_20260522.md` and `cves/nvd_exploitdb_github_lab_pattern_candidates_20260522.json`. Use product-specific CVEs as pattern inspiration unless the lab actually has the affected product/version/component. Retain valuable bundles even without full target control/file read when they provide reproducible workflow, false-positive handling, toolchain knowledge, or clear preconditions. Kali intel-driven wave 3 completed against Juice Shop with artifacts under `<artifact-output-dir>/kali_intel_wave3_20260522T005554Z/` and handoff `handoff/kali_intel_wave3_20260522.md`; retained valuable bundles for KEV-style path/file-read variants, upload retrieval/validation, browser-backed XSS runtime probing, and auth/access boundary expansion. Script acquisition wave 2 downloaded Exploit-DB reference scripts and GitHub tools/repos under `setting/local/tool_acquisition/wave2_20260522/` with handoff `handoff/script_acquisition_wave2_20260522.md`; treat as reference until reviewed and bounded to lab. New disposable modern API target `labs/modern_vuln_api/modern_vuln_api.py` was deployed on Kali `127.0.0.1:18080` and tested in wave 1 `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/`, producing verified IDOR/object ownership, upload retrieval, and isolated SSRF callback bundles; wave 2 `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/` extended it with verified browser-runtime XSS, bounded XXE safe-marker, and bounded unsafe-deserialization gadget bundles. Docker/Compose setup was attempted under operator-authorized NAT/reboot; NAT was opened, shared-folder boot issue was recovered, but Docker install was blocked because Kali sudo requires a password and local safety policy blocks piping/guessing sudo passwords. NAT was closed afterward. Continued with `source_reviewed_wrapper_wave1` artifacts under `<artifact-output-dir>/source_reviewed_wrapper_wave1_20260522T024602Z/`, using Exploit-DB/PayloadsAllTheThings/Arjun/Dalfox/XSStrike patterns as bounded local wrappers without raw exploit execution. Operator then completed Docker setup on `<victim-vm>` (<lab-ip>), which is now the Docker target host while `<attacker-vm>` remains tester. WebGoat/WebWolf were deployed as `webgoat-lab` on 8080/9090, NAT was closed after deployment, and baseline artifacts are under `<artifact-output-dir>/webgoat_docker_wave1_20260522T031708Z/` with handoff `handoff/webgoat_docker_wave1_20260522.md`. Next: authenticated WebGoat registration/login and one verified lesson proof at a time. Operator explicitly wants the lab to include capability-building tests for Access Control / IDOR-style lessons, JWT/token lessons, reflected XSS lessons, and path traversal safe-marker lessons, including classes that may be higher-risk if misused. Treat these as required WebGoat capability lanes, but execute only in authorized local lab, one lesson per run, with bounded payloads, no credential theft, no external callbacks, no destructive writes, no real secret reads, safe markers for file/path traversal, pre/post health checks, and artifacted request/response evidence.

- Adopt `SCRIPT_FIRST_CONTEXT_LOOP`: preview + recon results -> choose module bundle -> if no module fits, choose scripts from script library -> execute a small situation-specific script combination -> review -> modularize useful combination -> repeat -> report.
- Reporting convention: after every test wave, summarize `對專案有什麼幫助` and `新增/更新了什麼` alongside route/tool, artifacts, boundaries, blockers, and next lane.
- Treat `modules/checks/**/module.json`, profiles, validators, and preview contracts as guardrails/report-integrity layers, not the operator-facing path.
- Use `scripts/SCRIPT_INVENTORY.md` as the primary map of practical scripts and `modules/bundles/` as the new home for context-driven reusable script combinations.
- Current completed fast-lane slices: `lab_directory_listing_triage` around `/ftp/` now includes bounded `ftp_filename_content_class_verifier.py`, focused tests, local-lab run artifacts, and active bundle documentation; `benign_reflection_redirect_triage` now includes bounded `wave2_benign_params.py` rerun artifacts and active bundle documentation for inert reflection/open-redirect triage; reusable skill `owasp-single-vuln-lab-wave` now defines the one-vulnerability-at-a-time workflow, including destructive-lab snapshot/recovery gates. Important correction: the earlier `owasp_three_class_trial` is now explicitly treated as pilot/stress-test only. Its useful paths have been split into three active one-vulnerability modules: `lab_access_control_unauth_route_metadata`, `lab_crypto_transport_metadata`, and `lab_exceptional_condition_metadata`, all with focused adapters, tests, bundle docs, possible-vulnerability summaries, and local-lab artifacts under `<artifact-output-dir>/phase4b_single_vuln_three_20260521T081506Z/`. Latest mature-tool wrapper wave added `lab_ffuf_sensitive_path_discovery`, `lab_nikto_server_misconfig`, and `lab_nmap_http_fingerprint`, with final artifacts under `<artifact-output-dir>/phase4b_tool_wrapper_three_20260521T085200Z/`. Latest learning-stage script-first runs added `lab_headers_cors_baseline` using existing `headers_audit.sh`/`cors_audit.sh` with artifacts under `<artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/`, plus `lab_sqli_acquisition_triage` using newly acquired sqlmap with artifacts under `<artifact-output-dir>/phase4b_sqli_acquisition_learning_20260521T105021Z/`. Latest service-scanner bundle work added `lab_service_baseline_targets`. Latest three-exposure bundle work added `lab_api_docs_exposure_triage`, `lab_metrics_exposure_triage`, and `lab_source_map_disclosure_triage`, with artifacts under `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/`. Latest delayed-continuation catch-up added `lab_auth_surface_no_bruteforce`, `lab_component_metadata_triage`, `lab_integrity_metadata_triage`, and `lab_api_docs_metrics_manual_verification`, with artifacts under `<artifact-output-dir>/phase4b_owasp_cve_continuation_20260521T232928Z/`.
- Next candidate slice: use `handoff/owasp_2017_2021_2025_single_vuln_modularization_tracker_20260521.md` to pick one unmapped/partial OWASP class or practical tool workflow at a time. Latest operator directive in `handoff/phase4b_learning_stage_safety_pause_20260521.md`: for the current learning stage, pause the project's over-broad internal safety/tier/profile controls instead of adding more layers. Against the authorized disposable local靶機, do not category-ban broad scanners, fuzzers, Burp/session workflows, TLS scanners, OSS tools, exploit-shaped scripts, or destructive scripts; prefer script-first learning loops. Keep external/legal red lines, local artifacts, recoverability, and candidate-only output semantics. Additional operator direction in `handoff/phase4b_bundle_and_service_scanner_direction_20260521.md`: grow lightweight bundles as the practical module layer, seed command-library docs from real lab runs, and plan service-specific scanner bundles for Apache, Tomcat, OpenSSL, HAProxy, Envoy, and Traefik before adding more governance scaffolding.
- Continue preserving candidate/observation-only semantics for lab runs. Long-term target is bug-bounty finding support, but a lab module is not bug-bounty-ready until it has program scope/rules checks, safe public-target defaults, evidence hygiene, offline importer, candidate-review bridge, manual verification, and report-readiness gate. In the current learning-stage pause, local disposable-lab execution should not be blocked by missing tier/profile/review artifacts: run useful tools/scripts, keep artifacts local, recover/reset if needed, and record lessons as candidate-only. For public/real targets, scope/rules and technique gates remain mandatory. No confirmed vulnerability, reportable, ready_for_submission, public target, real bug-bounty target without scope/rules, real credential theft, real exfiltration, malware, stealth persistence, unauthorized pivoting, or automatic submission is authorized by this update.

## Current Lane

Current active lane as of 2026-05-21: Phase 4B — OWASP Top 10 modular lab-check library.

Latest accepted Phase 4B state:

- Wave1A metadata local-lab flow has been modularized into adapter/importer/candidate-review chain and remains candidate-only.
- OWASP Top 10 release coverage policy tracks official release editions only: 2003, 2004, 2007, 2010, 2013, 2017, 2021, and 2025.
- `modules/owasp_top10_release_traceability_matrix.json` and `modules/OWASP_TOP10_RELEASE_TRACEABILITY_MATRIX.md` provide offline/catalog-only mapping from historical/latest OWASP categories to the current 2021 project taxonomy.
- Current runtime/module taxonomy remains OWASP Top 10 2021 until a separate 2025 migration review is accepted.
- `handoff/phase4b_owasp_2025_migration_review_notes_20260521.md` is now the offline baseline for 2025 alias planning, checklist-only additions, blocked runtime classes, and attack/victim engineering-detail preservation.
- Phase 4B direction reset: operator corrected the architecture toward script-first, context-driven module bundles. Accepted direction is `SCRIPT_FIRST_CONTEXT_LOOP`, with `scripts/SCRIPT_INVENTORY.md` as the practical script map and `modules/bundles/` as the reusable script-combination layer. Heavy manifests/profiles/validators remain guardrails, not the main workflow.
- Next safest candidate slice: add the `/ftp/` filename-class offline importer/bridge after the active `lab_directory_listing_triage` bundle run; keep candidate-only semantics and avoid retaining file contents.

Current hard boundary:

- No public/real bug bounty target activation.
- Broad scanners/fuzzers/Burp/TLS tooling are allowed only for the authorized disposable local lab under the lab-tooling update with recovery/scope/artifact gates; public/real targets remain locked behind program scope/rules and technique approval.
- No exploit/bruteforce/callback/pivot/destructive/loot behavior outside the authorized disposable lab/snapshot-recovery gate; no credential theft or real-account brute force.
- No schema/runtime/report promotion or automatic confirmed/verified/reportable/accepted finding promotion.

## Previous Phase 3/4A navigation snapshot

Phase 3 dry-run/local MVP closeout is accepted via `handoff/phase3_dry_run_local_mvp_closeout_20260520.md` with decision `PASS_WITH_CONDITIONS / CLOSE_PHASE_3_OFFLINE_MVP`. P3.15 documentation-only manifest/profile policy crosswalk remains complete via `handoff/p3_15_manifest_profile_policy_crosswalk_20260520.md`, following the P3.14 decision to defer formal field promotion. P3.14 module manifest/profile risk-field promotion direction review remains complete via `handoff/cowork_p3_14_module_field_promotion_direction_review.md` and synthesized in `handoff/p3_14_module_field_promotion_direction_result.md`: decision is to DEFER formal field promotion and proceed only with documentation-only mapping/planning if continuing. P3.13 module risk-tier / active-testing policy follow-up remains accepted as a T1 docs-only slice after Cowork direction review `handoff/cowork_p3_13_module_risk_tier_direction_review.md` (`APPROVE_WITH_CHANGES`) and Hermes local policy edit/result `handoff/p3_13_module_risk_tier_policy_result.md`. P3.12 SOC reviewer-gap catalog-only slice remains accepted and closed out by `handoff/p3_12_closeout_current_thread_pause_20260520.md` after Cowork direction review (`PROCEED_CATALOG_ONLY` / `APPROVE_WITH_CHANGES`), Claude Code MAX/OAuth implementation, Hermes validation, independent implementation/safety review `handoff/third_party_p3_12_implementation_review.md` (`PASS` after a narrow symmetric drift-lock fix), and Hermes closeout synthesis.

Current decision:

- P3.11 remains accepted as T2 direct-authority offline/local fixture/docs/test work.
- P3.12 remains accepted as T2 direct-authority offline/local static catalog/docs/test work.
- P3.12 artifacts are limited to `fixtures/soc_evidence_bucket/reviewer_gap_catalog.{md,json}` and `scripts/test_soc_reviewer_gap_catalog.py` plus handoff/notes.
- The catalog is a companion artifact only: synthetic, trial, non-contractual, offline, non-promotional, not a schema, not a runtime consumer, and not a report gate.
- SOC calibration work should pause here; trial-consumer design remains deferred and requires a separate future T3 direction review.
- No schema/runtime/report/gate promotion is approved.
- P3.15 is accepted as documentation-only crosswalk; it maps existing manifest/profile 1.0 fields to P3.13 policy dimensions and explicitly keeps all future field candidates non-contractual.
- Phase 3 is accepted as closed for the offline/dry-run local MVP milestone with conditions: the repo should still run the local dry-run demo checklist and final validation before a formal commit/release bundle, and unrelated untracked artifacts should be cleaned or intentionally preserved.
- Next default lane is Phase 4A.1 lab target selection / activation-boundary direction planning. Phase 4A Controlled Lab Semi-Automated Calibration is now after Phase 3 closeout and before any real bug-bounty private beta; no field promotion, lab activation, scanner/module execution, or target interaction is approved by P3.14/P3.15/Phase 3 closeout/Phase 4A planning.
- Forbidden surfaces remain locked: no live SIEM, scanner/module execution, target interaction, scope/config changes, runtime consumer, schema promotion, report drafting/submission, platform adapter, credentials/loot, scheduler/CI, proxy/pivot/transport, lab activation, real program activation, or production settings.
- Claude implementation turn-budget convention: keep the repo default at 25 turns; for fixture/test/handoff-heavy offline slices use a temporary invocation such as `CLAUDE_IMPL_MAX_TURNS=35` or `CLAUDE_IMPL_MAX_TURNS=40 HACKLAB=$(pwd) ./bin/hermes claude-impl` rather than changing the global default. P3.12 still reached `error_max_turns` at 35, so future similarly broad slices should be split or use a higher one-off cap only with a tighter task.

- P3.10 completed on 2026-05-20 after T3/T4 design review and independent implementation/safety review.
- `handoff/cowork_p3_10_direction_prompt.md` was prepared for the direction review.
- `handoff/cowork_p3_10_direction_review.md` returned `APPROVE_WITH_CHANGES`: allow a narrow direct-read bridge, but no auto-copy, auto-discovery, scheduler, scanner/module execution, live target behavior, or report/schema promotion.
- `handoff/third_party_p3_10_implementation_review.md` returned `PASS_WITH_RECOMMENDATIONS`; reviewer route/tool was Hermes `delegate_task` subagent and exact child runtime was not exposed.
- P3.10 implementation updated `scripts/module_runner.py` to directly read explicit policy artifacts from either `runs/<run_id>/policy/<file>` or `scans/<scan-dir>/evidence/policy/policy_boundary_*.json`, with repo-root, traversal, outside-root, wrong-shape, symlink, and regular-file checks.
- P3.10 updated `scripts/validate_run_manifest.py` and `scripts/test_run_manifest_schema.py` so only `policy.decision_artifact_path` accepts the narrow recon evidence path shape; finding/evidence artifacts remain run-local.
- P3.10 expanded `scripts/test_recon_runner_bridge_dry_run.py` with direct-read/no-copy, repo-relative non-repo-cwd, traversal, malformed scan-dir, wrong filename/directory, outside-root, hash/provenance, no bridge-specific flag, and no scanner/module-execution leakage coverage.
- P3.10 validation passed: focused bridge suite (`18 OK`), adjacent runner/module-IO/bridge/run-manifest suite (`78 OK, 1 skipped`), `git diff --check` (line-ending warnings only), diff security scan (0 hits), and `HACKLAB=$(pwd) ./bin/hermes review` (Python compile OK for 76 files, shell scripts OK, lock clear, 12 scope entries).
- P3.9 closeout checkpoint remains at `handoff/p3_9_closeout_next_direction_20260520.md`; decision `PASS_WITH_CONDITIONS`.
- P3.9 T2 follow-up is complete: copied-artifact byte/hash drift negative coverage and explicit test-harness-only bridge-copy comment in `scripts/test_recon_runner_bridge_dry_run.py`.
- `handoff/third_party_p3_9_implementation_review.md` returned `PASS_WITH_RECOMMENDATIONS` with no blockers; review route/tool was Hermes `delegate_task` subagent and visible model/runtime was reported as `gpt-5.5 / openai-codex`.

- P3.9 implementation added `scripts/test_recon_runner_bridge_dry_run.py`; bridge path translation is test-harness-only and runtime bridge remains deferred.
- P3.9 validation passed focused bridge tests, adjacent suites, full `python -m unittest discover scripts`, `git diff --check`, added-line secret/target-touching scan, and `hermes review`.
- P3.9 process caveat: Claude Code implementation worker exceeded the parent Hermes timeout after creating the test file; Hermes completed cleanup/verification directly and recorded incomplete RED evidence in `handoff/claude_code_result_p3_9.md`.
- `handoff/cowork_p3_8_direction_review.md` returned `APPROVE_WITH_CHANGES` for malformed-scope exit-code semantics.
- P3.8 implementation hardens `recon.sh` so program-policy boundary/config errors exit `3`, while valid policy denies remain exit `0`.
- The literal CIDR forced-deny follow-up was handled as T2 coverage inside the existing P3.7/P3.8 boundary, not as a fresh direction-review slice.
- P3.7 direction/review artifacts remain the baseline for the return-to-mainline program-policy regression.
- Implementation commit: `c7dfe2c` (`test: add P3.7 program policy dry-run regression`).
- Independent implementation/safety review: `handoff/third_party_p3_7_implementation_review.md` returned `PASS_WITH_RECOMMENDATIONS`.
- Launch estimate: `handoff/project_launch_estimate_20260519.md`.
- Preferred route remains: close Gate B and request P3.9 T3 design-only direction review before any recon-to-runner bridge implementation.

Completed implementation boundary:

- Added: synthetic fixture `programs/_examples/sample-lab/scope.json`, offline test `scripts/test_recon_program_policy_dry_run.py`, append-only handoff/result/review updates.
- Added follow-up docs: `programs/_examples/README.md` clarifies `_examples/` fixtures are never real program slugs and `automation_permitted: true` under `_examples/` is test-only, not live authorization.
- Added P3.8 runtime hardening: `recon.sh` reserves exit code `3` for program-policy boundary/config errors and preserves exit `0` for valid policy denies/no-work dry-run outcomes.
- Added T2 CIDR forced-deny coverage: literal `192.0.2.0/24` without `--allow-cidr` stays dry-run, policy-denied with `CIDR_REQUIRES_ALLOW_CIDR`, emits a deny artifact, and does not plan scanner execution.
- Added P3.9 tests-only offline bridge coverage: `scripts/test_recon_runner_bridge_dry_run.py` demonstrates recon dry-run policy artifact consumption by existing module runner preview, with test-harness-only artifact copying into temp `runs/<run_id>/policy/decision.json`.
- Added P3.9 T2 follow-up coverage: direct copied-artifact byte/hash drift denial and source-level comment regression for test-only path translation.
- Forbidden surfaces stayed untouched: recon/runtime bridge code, program policy helper contracts, module runner, configs, `config/scope.txt`, schemas, modules, report/submission surfaces, scanner/module execution, and any target-touching automation.

## Latest Stable Boundary

The P3.1-P3.6 line is coherent enough to pause:

- P3.1: curated near-real offline fixture set.
- P3.2: terminal-state expectation matrix.
- P3.3: two-module runner discovery coverage.
- P3.4-alt: runner-indifference coverage for `check.py` presence/absence.
- P3.5: report-readiness reviewer prompt catalog, data-only and non-consumer.
- P3.6: periodic multi-party review templates; reviewer-notes artifact deferred.
- P3.7 direction: return to program-policy mainline approved with a tests/fixture-only boundary.

No P3.1-P3.11 slice authorized live targets, scanner/module execution, schema promotion, report drafting/submission, platform adapters, scope/config changes, credentials, OAuth, scheduler, deployment, billing, or production settings. P3.11 remains fixture-only and non-contractual.

## Next Candidate Slices

Likely next lanes after the Phase 4A external-tool lab calibration checkpoint:

1. External-tool artifact redaction checker.
   - Source: `handoff/phase4a_external_tool_adapter_result_20260520.md`, `handoff/phase4a_nuclei_ffuf_spike_result_20260520.md`.
   - Boundary: offline/local artifact inspection only; no target interaction, no scanner execution, no submission, no secrets retention.
   - Goal: scan external-tool outputs for raw bodies, tokens, cookies, credentials, loot-like strings, callback URLs, and oversized sensitive artifacts before any observation is eligible for candidate review.

2. ZAP baseline/passive importer, importer-first.
   - Boundary: parse fixture/sample ZAP JSON/HTML/XML outputs only; no live ZAP execution yet.
   - Goal: compare ZAP alert schema with current `external_tool_observations/0.1-trial`, preserve scanner-output-only semantics, and prevent auto-confirmed/reportable promotion.

3. Nuclei allowlisted-template registry and validator.
   - Boundary: metadata/template validation only before any template-pack execution; no broad nuclei template run.
   - Goal: define local allowlist records, reject intrusive/dos/fuzz/OAST templates, require severity/tag/rate/timeout policy, and keep generated/local templates distinguishable from third-party packs.

4. Tiny-wordlist content-discovery tool comparison.
   - Boundary: lab-only and tiny generated wordlist; compare feroxbuster/gobuster/ffuf output schemas without broad wordlists or recursion.
   - Goal: choose which content-discovery output format is easiest to normalize safely.

5. Observation-to-candidate bridge.
   - Boundary: local/offline candidate packet construction only; no automatic confirmed findings, report submission, or real target activation.
   - Goal: allow manually selected httpx/katana/nuclei/ffuf observations to become candidate-review inputs with provenance, safety flags, manual verification TODOs, and redaction status.

6. Phase 4B Lab-to-report workflow trial.
   - Boundary: still lab-only and candidate/verification/report-readiness focused; no real bug-bounty target, no external submission, no automatic confirmed findings.
   - Goal: take 1-2 lab candidate findings through manual verification, evidence packet, impact reasoning, remediation, retest note, and report-draft readiness without submission.

7. Phase 4C one-program authorized bug-bounty private-beta planning.
   - Boundary: planning only unless the operator provides a specific program/scope/rules and approves the activation gate.
   - Goal: translate Phase 4A/4B lessons into one real program scope/rules, allowed-technique mapping, redaction/report rules, and manual approval checkpoints.

8. SOC trial-consumer design-only review, only after a separate fresh direction prompt.
   - Boundary: no implementation until T3 direction review; no runtime consumer, report path, SIEM integration, schema promotion, or target-touching behavior.
   - Goal: decide whether normalizing reviewer feedback into non-promotional gap categories is useful and safe.

9. Deferred future activation: automated recon-to-runner coupling.
   - Boundary: current P3.10 is explicit direct-read only. Any future auto-discovery, auto-copy, scheduler/CI linkage, live target behavior, scanner/module execution, finding/evidence promotion, or report/submission pipeline still requires fresh T3/T4/T5 review plus explicit operator approval where applicable.

10. Launch planning reference.
   - `handoff/project_launch_estimate_20260519.md` estimates: dry-run/local MVP ~1–2 weeks, controlled lab beta ~2–6 weeks, authorized bug-bounty private beta ~5–16 weeks, production-like multi-program platform ~9–35 weeks.

## Deferred Lanes

These require a fresh direction review or explicit re-trigger before implementation:

- Reviewer-notes artifact / reviewer-answer capture.
- Fifth stdin consumer or third file-reading consumer in the candidate workflow chain.
- Shared `scripts/core/offline_consumer.py` helper extraction.
- Schema promotion for any current `*/0.1-trial` document.
- Report drafting, HTML/Markdown submission rendering, or platform submission adapters.
- External scanner-output importers or exporter/importer boundaries.
- Real evidence-locator stage or redaction gate driven by scanner outputs.
- Automated recon-to-runner coupling beyond explicit direct-read, including auto-discovery, auto-copy, scheduler/CI linkage, scanner/module execution, finding/evidence promotion, or report/submission pipeline.

## Blocked Until Explicit Operator Approval

The following remain blocked until the operator gives explicit narrow approval and the required review tier is satisfied:

- `config/scope.txt` changes.
- Real program scope/rules changes that authorize target-touching automation.
- Live target execution, scanner execution, fuzzing, brute force, exploit attempts, callbacks, OAST, proxy/pivot/tunnel/beacon/relay/reverse-listener behavior.
- Weakening or bypassing `safe_target`, `--skip-scope-check` confirmation, program policy gates, or policy artifact validation.
- Scheduler/CI automation that touches targets.
- Credentials, OAuth, tokens, private keys, loot, production settings, deployment, billing, or repo-setting changes.

## Review Freshness

When this queue conflicts with a frozen review packet, use this rule:

1. Current explicit operator instruction wins.
2. Live repo state and validation output win over stale review text.
3. `handoff/accepted_changes.md` and this queue are the current handoff navigation layer.
4. Frozen review packets remain evidence and rationale, not automatic current authority.

Next periodic or milestone-boundary review should record:

- packet frozen date;
- latest live handoff inspected;
- latest commit inspected;
- post-packet changes included/excluded;
- memory/handoff/goal/structure drift status.
