> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Active Strategy Queue

Status: active
Source: Hermes navigation cleanup after operator direction
Date: 2026-05-23
Repo truth: `handoff/current_navigation.md`, `handoff/lab_safety_contract.md`, `handoff/live_bounty_autonomous_workflow_policy_20260525.md`, `handoff/accepted_changes.md`, `.hermes.md`, `notes/obsidian_projects/Cybersec Lab.md`
Autonomy note: for authorized bug bounty lanes, Hermes should act as project owner for safe non-sensitive steps and checkpoint at lane/target completion or true operator gates.
Archived previous queue: `handoff/archive/active_strategy_queue_pre_navigation_cleanup_20260523.md`

## Purpose

This file is the compact current-navigation layer for Cybersec Lab. It should stay short. Detailed history belongs in named handoff artifacts, `handoff/accepted_changes.md`, `<artifact-output-dir>/`, `modules/bundles/`, and Obsidian strategy notes.

## Long-term goal

Build a legal, recoverable, scope-aware, script-first security research platform that can produce high-value bug bounty / pentest proof packets from authorized contexts.

The current emphasis is:

```text
script-first + context-driven bundles + one-vulnerability max-impact proofs
```

Automation remains a project goal, but it should grow from proven local proof patterns, not from contract/schema/governance-first scaffolding.

## Current phase

Phase 5A is active: authorized-assessment readiness, one-shot vulnerability-intelligence intake, cautious live-bounty bridge work, and high-hit-rate live investigation selection.

- Phase 4 is effectively closed unless the operator identifies a concrete missing ability gap.
- Do not add more local lab vulnerability waves by default; reuse existing proof patterns.
- Current Phase 5A work has shifted from first-flow practice toward high-hit-rate live investigation: A0 passive OSINT/program scoring, one selected bug class, A/B or tenant controls, timeboxed A2 viability, and A3 bounded proof only when exact policy/scope and owned controls exist.
- New high-hit-rate artifacts: `handoff/live_bounty_high_hit_rate_target_filter_20260526.md`, `handoff/live_bounty_attack_class_matrix_20260526.md`, and `handoff/next_live_bounty_shortlist_20260526.md`.
- New tactical-freedom/learning-loop artifacts: `handoff/live_bounty_tactical_preview_template_20260526.md`, `handoff/live_bounty_no_finding_feedback_log.md`, `handoff/live_bounty_account_ab_operator_action_card_20260526.md`, and `handoff/tactical_freedom_platform_direction_20260526.md`. Use the preview template to expand tactical options before narrowing; use the feedback log after every no-finding/surface-only/blocked lane; use the operator card for Account B / tenant B / object visibility gates without collecting secrets. Latest operator direction: do not exclude tactics merely because realistic attackers use dangerous methods; model full attack paths, compile bounded proof surrogates, and stop before unauthorized access, non-owned data contact, destructive impact, DDoS/resource exhaustion, credential theft, malware, stealth/persistence/evasion, or report submission.
- Multi-agent memory/workflow hardening now has an enforcing local contract: `scripts/check-worker-attestation.py`, `config/worker_roles.txt`, `templates/role_packet_base.md`, `tests/test_worker_context_attestation.sh`, and `tests/test_worker_roles_vocabulary.sh`. Cowork/Claude and Codex wrapper runs must output checked context read attestations, canonical roles, validation, and verdicts; `hermes review` enforces present artifacts. The local review gate is now fail-closed for invalid JSON (with Python fallback when `jq` is unavailable), Python compile failures, shell syntax failures, active `.agent.lock`, and missing/unavailable worker attestation checks; regression: `tests/test_hermes_review_fail_closed.sh`. Operator correction on 2026-05-26: for attacker-flow/non-trivial live-bounty lanes, role separation must actually invoke suitable independent agents (Claude Code/Cowork for tactical/boundary/evidence roles and Codex for deterministic/skeptical review) or explicitly record the skipped/unavailable route and remain passive-only. Workers must receive the memory-sync context packet, not just a single MD file. Repo truth: `handoff/multi_agent_tactical_review_memory_sync_rule_20260526.md`. This is workflow hardening only and does not authorize target-touching work.
- Agent capability substrate v1 is implemented and Codex-reviewed: `schemas/attack_path_role_synthesis.schema.json`, `schemas/kali_readiness_state.schema.json`, `schemas/no_finding_learning_seed.schema.json`, `scripts/attack-path-role-synthesize.py`, `scripts/kali-readiness-state.py`, `scripts/no-finding-learning-seed.py`, and `tests/test_agent_capability_substrate.sh`. These add local-only role-conflict synthesis, Kali readiness state, and no-finding learning seed helpers; target-like flags fail closed, readiness is not authorization, and learning seeds are not evidence promotion. Third-target <program-name> contact is formally opened within confirmed in-scope assets: `programs/<program-redacted>/scope.json`, `programs/<program-redacted>/lane_state.json`, `handoff/program-redacted_first_contact_scope_and_signup_gate_20260526.md`, and `handoff/program-redacted_pre_contact_ready_checkpoint_20260526.md`; current state is `READY_FOR_OPERATOR_GATE` / `A2_PENDING_OPERATOR_AUTH` at the signup identity/phone gate, with local noVNC reachable and the latest continuation showing the official <program-name> signup form in the Kali browser.
- Recommended next target candidate: `<program-redacted>` / <program-name>, selected from Kali passive <bug-bounty-platform> policy/program-metadata intake and recorded in `handoff/program-redacted_target_selection_preview_20260526.md`. Logged-in <bug-bounty-platform> Scope CSV confirmed in-scope assets on 2026-05-26: `<in-scope-host>`, `<in-scope-host>`, mobile app IDs, and Mac/Windows executables. Only `<in-scope-host>` and `<in-scope-host>` were added to `config/scope.txt`; `<program-domain>` remains out-of-scope except as the official signup page reached from the in-scope app sign-in flow. Current live state: `https://<in-scope-host>/signin` first contact completed, `Try for Free` revealed `https://<program-domain>/signup` form with email/name/company/job/industry/phone/company-size fields; Hermes stopped for operator signup/phone/identity input.
- <program-redacted> Taiwan current status: minimal program scope exists at `programs/<program-slug>/scope.json`; selected assets are present in `config/scope.txt`; pre-second-phone single-account surface/auth boundary check is complete in `handoff/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md`; result is no finding / `needs_second_account` for IDOR/BOLA.
- Before any next live-target action, read `handoff/proof_library_live_bounty_bridge_20260525.md` and classify the lane as `surface_only`, `needs_second_account`, `blocked_state_change`, `blocked_sensitive_flow`, `candidate`, or `report_ready`.
- Live automation gate compatibility is fixed and regression-covered for dry-run readiness: `tests/test_recon_gate.sh` verifies `<program-slug>` program dry-run accepts exact in-scope <program-redacted> target, intentional `localhost` scope entries no longer poison validation, `example.org` remains rejected, malformed/path-like slugs fail before target processing, `--skip-scope-check` cannot combine with program policy, policy dry-run requires `--dry-run`, and `--policy-mode` without `--program` is rejected. This does not authorize live scanner-like automation without a separate operator-approved plan.
- Vulnerability intelligence should not exclude classes that need live/real targets. If a promising lane cannot be faithfully proven locally, keep it as `needs_authorized_live_target` and ask the operator for legal target/scope/rules instead of silently dropping it.
- Full periodic scheduling comes later only after the one-shot MVP stays compact and useful.

## Current default route

- Work repo: `<private-workspace>`.
- Default attacker VM: `<attacker-vm>`.
- Deprecated attacker VM: old registered `<attacker-vm>`; forensic archive only.
- Victim/target VM: `<victim-vm>`.
- Default network: host-only.
- NAT: closed by default; temporary installs/pulls only, then close and verify.
- Clean attacker snapshot: `clean-attacker-v2-tools-4096m-4cpu-20260522` (`bcee6035-c86d-41f0-8da1-62b3b42ec388`).

See `handoff/current_navigation.md` and `handoff/lab_safety_contract.md` for the full operational map.

## Active local lab targets

1. DVWA
   - Best for command injection, marker write/readback, attacker callback proof baseline.
2. WebGoat
   - Best for authenticated/session handling, JWT, IDOR/access control, path traversal, XSS lessons.
3. Juice Shop
   - Best for SQLi behavior, file listing/read metadata, upload validation, auth/access boundary, XSS calibration.
4. `labs/modern_vuln_api/modern_vuln_api.py`
   - Best for source-controlled SSRF, XXE safe-marker, browser-runtime XSS, deserialization marker, upload retrieval, IDOR, and auth/session role separation.

## Top active lanes

1. Proof-library → live-bounty bridge, post-proof consolidation, authorization-gate dry-run health, and lane-state automation substrate
   - Current status: bridge exists at `handoff/proof_library_live_bounty_bridge_20260525.md`; lightweight consolidation checklist exists at `scripts/post-proof-consolidation.sh`; authorization-gate compatibility blockers are fixed and regression-covered; machine-readable lane/evidence schemas, queue, status helper, redaction checker, local-only queue runner, and reference-grounding generator now exist; the engineering substrate is sealed at `handoff/live_bounty_automation_substrate_closeout_20260525.md`.
   - New automation artifacts: `schemas/live_bounty_lane_state.schema.json`, `schemas/live_bounty_evidence.schema.json`, `handoff/live_bounty_lane_queue.json`, `scripts/live-bounty-lane-status.py`, `scripts/live-bounty-lane-runner.py`, `scripts/live-bounty-preview-grounding.py`, `scripts/evidence-redaction-check.py`, `tests/test_live_bounty_state_and_redaction.sh`, `tests/test_live_bounty_lane_runner.sh`, `tests/test_live_bounty_preview_grounding.sh`, `handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md`, `handoff/live_bounty_automation_engineering_slice_20260525.md`, `handoff/live_bounty_automation_substrate_closeout_20260525.md`.
   - Purpose: map verified local proof patterns to live-bounty prerequisites, blocked states, minimum live evidence, report-readiness thresholds, public methodology references, and make each target/lane resumable and learnable through structured state/evidence plus runner exit codes before wrap-up.
   - Next engineering slice: none by default. Do not add approval-heavy safety process, extra schema/governance, or more local-only tooling unless explicitly requested or a focused test fails. Next value is the operator identity/session gate followed by noVNC owned-account surface mapping; dry-run pass, runner exit `0`, or grounding output is not permission for live scanner automation.

2. <program-redacted> Taiwan pre-second-phone single-account lane
   - Current status: low-speed logged-in Kali/noVNC observation complete; no finding; `needs_second_account` for IDOR/BOLA.
   - Artifacts: `handoff/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md`, `handoff/coupang_tw_single_account_surface_map_20260525.md`, `programs/<program-slug>/scope.json`.
   - Next live step only after Account B/program guidance: build an Account A/B object-ownership matrix from normally visible owned objects. Before then, do not manufacture state or touch support/recovery/payment/KYC/upload/seller/admin.

3. Thanks-only / VDP first complete-flow lane
   - Current status: <program-redacted> VDP first flow is complete as `NO_FINDING_CLOSEOUT` / `no_finding` with evidence status `surface_only`; operator <bug-bounty-platform>-alias signup/login gate was completed locally in Kali/noVNC; Hermes performed low-speed browser-only owned-account surface mapping and did not run workflow/publish/integration/API-key/credential/user-invite/setting-mutation/scanner actions.
   - Artifacts: `handoff/thanks_only_vdp_shortlist_20260525.md`, `programs/<program-slug>/scope.json`, `programs/<program-slug>/lane_state.json`, `handoff/tines_automation_vdp_owned_account_surface_map_20260525.md`, `handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_surface_map_20260525.json`, `handoff/tines_automation_vdp_phase5a_dry_run_packet_20260525.md`.
   - Next safe action: none by default for <program-redacted>. Any next <program-redacted> lane requires a separately approved plan; possible later lanes include read-only profile review, API policy review, or second-owned-account controls. Scanner/fuzzer/DAST, workflow execution, run-script, callbacks, integrations, cross-tenant tests, non-owned data, mutation of settings, credential/API-key creation, and report submission remain blocked.

4. First <bug-bounty-platform> authorized-scope intake pattern
   - Current status: reusable intake packet exists at `handoff/hackerone_first_scope_intake_20260525.md`; use it for the selected VDP or any operator-provided program.
   - Next use: once filled, Hermes converts exact policy facts into `programs/<program-slug>/scope.json`, asks for explicit confirmation before adding global `config/scope.txt` entries, and prepares a single-lane dry-run packet.

5. Phase 5A authorized live-target dry-run readiness
   - Current status: templates created in `handoff/phase5a_authorized_live_target_dry_run_template.md` and `handoff/phase5a_report_readiness_checklist.md`.
   - Next use: when the operator provides a legal target/scope package, fill these before any target-touching work.

6. Vulnerability-intelligence refresh / latest capability intake
   - Current status: one-shot metadata-only MVP implemented at `tools/vuln_intel_refresh.py` and sampled into `handoff/vuln_intel/vuln_intel_candidates_20260523T130000Z.md`.
   - Current candidate handling: shortlist can include `needs_authorized_live_target`, `needs_lab_bootstrap`, or `local_candidate`; do not force everything into local-only testing.
   - Next use: run only when an explicit “what should we learn/test next?” question needs current CVE/advisory context; keep output as candidate routing, not exploit automation.

7. Selected local-bootstrap planning candidate
   - Selected candidate: Arcane `<specific-ghsa-id>`, missing admin authorization on global variables endpoint.
   - Current artifacts: `handoff/phase5a_arcane_global_variables_bootstrap_plan_20260523.md`, `handoff/phase5a_arcane_global_variables_feasibility_review_20260525.md`, `handoff/arcane_global_variables_bootstrap_precheck_run_card_20260525.md`, `handoff/arcane_global_variables_precheck_posture_20260525.md`, `scripts/labs/arcane_global_variables_bootstrap_precheck.sh`, and `targets/catalog/arcane_ghsa_jpjh_jm2p_39hh.md`.
   - Current status: source/install feasibility reviewed; fail-closed precheck/run-card drafted; Windows control-plane precheck was blocked/fail-closed because Docker CLI is missing; no target touched. Feasible only with a disposable Docker daemon/proxy posture; do not mount a host/user Docker socket.
   - Next gate: do not run setup/proof until the disposable Docker daemon/socket posture is confirmed from the intended victim-lab environment.

Recent completed proof lanes retained for reuse:

- Deserialization bounded-marker operator proof: `handoff/modern_api_deserialization_bounded_marker_operator_verified_20260523.md`.
- File-read/path traversal safe-marker proof: `handoff/modern_api_path_traversal_file_read_wave1_20260523.md`.
- Auth/session role-separation proof wave: `handoff/modern_api_auth_role_separation_wave1_20260523.md`.

Completed packetization:

- SSRF true-attacker callback: `handoff/modern_api_ssrf_true_attacker_callback_evidence_packet_20260523.md`.
- DVWA command-injection callback: `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md`.
- WebGoat browser-runtime XSS: `handoff/webgoat_browser_runtime_xss_evidence_packet_20260523.md`.

## Wave process update

One-vulnerability local-lab waves now include lightweight tactical perspectives, not new safety gates:

```text
OSS/source reconnaissance -> Hermes tactical preview -> Kali bounded-script execution -> artifact/evidence pullback -> Claude Code read-only review -> Hermes synthesis / verified-impact/bundle/evidence-packet promotion
```

- Hermes preview increases tactical sight before execution: proof path, tool choice, project value, artifact plan, and alternative local target surface.
- Claude Code review challenges evidence and value before overclaiming: status classification, missing evidence, false-positive controls, and whether to stop/rerun/switch/packetize.
- Keep this lightweight; do not turn it into governance-first blocking, approval workflow, or extra safety process.

## Secondary lanes

- Auth/session handling: throwaway users, cookies/tokens, re-auth, role separation, replay controls. Current ability-gap proof is complete in `handoff/modern_api_auth_role_separation_wave1_20260523.md`; reuse it instead of adding more lab variants by default.
- Evidence packet / report-readiness gate: turn one strong local proof into a reusable packet.
- Source-driven script/tool selection: inspect context/source, choose a small tool chain, modularize only after value is proven.
- Vulnerability-intelligence refresh + target bootstrap: Phase 5 work. Produce candidates from current sources, try local/recoverable target setup where faithful, and route valuable live-target-dependent candidates to an operator scope request rather than filtering them out.

## Parked or deprecated lanes

- Public or real bug bounty target testing without a user-provided legal scope package.
- Live/real target candidates are not deprecated solely because they need a live target; hold them as `needs_authorized_live_target` until the operator provides target/scope/rules or declines the lane.
- Contract-first / schema-first / importer-first / report-generator-first work.
- Large governance/validator expansion that does not improve local proof quality.
- Automatic finding confirmation, automatic report submission, scheduler/CI target-touching automation.
- Old `<attacker-vm>` route except forensic/reference use.

## Current hard boundary

Allowed now:

- Read-only navigation cleanup.
- Documentation/handoff/Obsidian routing updates.
- Local/offline agent capability substrate work: role synthesis, Kali readiness state, no-finding learning seeds, and validation.
- Local lab proof waves only after explicit instruction and scope/route confirmation.

Not authorized by this queue:

- Continuing <program-name> beyond the visible signup identity/phone gate until the operator fills the form locally in Kali/noVNC and reports a non-sensitive status such as `front_signup_complete`, `blocked_phone`, `blocked_email_verification`, `blocked_captcha`, `blocked_payment`, `blocked_policy`, or `stop`. Current noVNC checkpoint: `handoff/program-redacted_pre_contact_ready_checkpoint_20260526.md`; latest screenshot pointer: `setting/local/screenshots/program-redacted_live_20260526/signup_gate.png`.
- Additional public/real targets unless the operator supplies an explicit legal scope package for that lane.
- <program-redacted> live automation/scanner-like/scripted runners until `gate_fail_closed_needs_fix` is resolved and dry-runs prove in-scope pass / out-of-scope fail.
- <program-redacted> Account A/B object-ownership testing until Account B is operator-owned/program-provided and the lane is classified through `handoff/proof_library_live_bounty_bridge_20260525.md`.
- Scope/config changes that authorize live targets without explicit operator-provided target/scope/rules.
- Credential theft, real exfiltration, malware, stealth/persistence/evasion, uncontrolled propagation.
- External callbacks/OAST/tunnels/pivots/public listeners without explicit approval.
- Automatic confirmed/reportable finding promotion or submission.
- VM network/snapshot changes unless explicitly requested for lab recovery/install needs.

## Artifact convention

Default proof artifact root:

```text
<artifact-output-dir>/<lane_name>_<YYYYMMDDTHHMMSSZ>/
```

Each one-vulnerability proof should include:

- target / route / vulnerability class;
- authorization boundary;
- proof narrative and exact commands;
- evidence and controls;
- pre/post health;
- cleanup/recovery notes;
- limitations;
- project benefit and new/changed artifacts;
- report-readiness status.

## Current navigation files

- Main map: `handoff/current_navigation.md`.
- Artifact cleanup/index map: `handoff/current_artifact_index.md`.
- Safety contract: `handoff/lab_safety_contract.md`.
- Accepted history: `handoff/accepted_changes.md`.
- Obsidian strategy/navigation: `notes/obsidian_projects/Cybersec Lab.md`.
- Archived pre-cleanup long queue: `handoff/archive/active_strategy_queue_pre_navigation_cleanup_20260523.md`.

## Freshness rule

1. Current explicit operator instruction wins.
2. Live repo/config/tool state wins for verifiable facts.
3. `handoff/current_navigation.md`, `handoff/current_artifact_index.md`, this queue, `handoff/lab_safety_contract.md`, and `handoff/accepted_changes.md` are current navigation.
4. Frozen reviews and archived queues are history/rationale, not current routing.

## 2026-05-26 — <program-name> Account B passive owned-surface map

- Current <program-name> lane state: `A2_SURFACE_MAP_COMPLETE` / `surface_only` in `programs/<program-redacted>/lane_state.json`.
- Operator completed Account B signup/auth locally; Hermes performed only low-speed noVNC owned/passive UI observation. Evidence summary: `handoff/program-redacted_account_b_passive_surface_map_20260526.md` and `handoff/live_bounty_evidence/<program-redacted>/owned_account_signup_profile_workspace_surface_map/evidence_surface_map_20260526.json`.
- Observed owned surfaces: Customer Support shared section, `Support` and `Support - Priority` owned inbox labels, Sandbox/demo sections, setup guide, and hard gate to connect first shared channel. No customer/non-owned data was observed.
- Do not exclude potentially useful bundles yet. Preserved bundle families live in `handoff/program-redacted_passive_docs_bundle_map_20260526.md`: inbox membership, non-public group linking, conversation cross-listing, message/comment/draft splits, workflow/rule routing, channel/OAuth, API/UI mismatch, plugin context, archive/delete residue, metadata-only leaks.
- Next safe work: passive UI/docs mapping only, or stop. No external channel/OAuth/mailbox connection, invite/role/team mutation, workflow/rule/Topics activation, API token/API calls, messages/comments/discussions, customer/non-owned data, scanner/fuzzer/DAST, report-ready promotion, or report submission.
