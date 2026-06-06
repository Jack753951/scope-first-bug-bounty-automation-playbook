> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersec Lab Current Navigation

Status: active
Source: User + Hermes navigation cleanup
Date: 2026-05-25
Repo truth: `.hermes.md`, `handoff/accepted_changes.md`, `handoff/active_strategy_queue.md`, `handoff/current_artifact_index.md`, `handoff/live_bounty_autonomous_workflow_policy_20260525.md`, `handoff/live_bounty_lane_queue.json`, `handoff/lab_safety_contract.md`, `notes/obsidian_projects/Cybersec Lab.md`

## Purpose

This is the short entry map for the Cybersec Lab. It should answer, in under 10 minutes, which route is current, which lab targets are active, which vulnerability lanes are worth doing next, where artifacts go, and which lanes are intentionally parked.

This cleanup is navigation-only. It does not authorize public target testing, new scanning, exploitation, VM network changes, scheduler changes, report submission, credential handling, or publication of findings.

Bug bounty autonomy policy: `handoff/live_bounty_autonomous_workflow_policy_20260525.md` is now the project-level operating policy for live bounty autonomy. Hermes should own safe authorized steps and checkpoint only at lane/target completion or true operator gates, while still fail-closing on scope ambiguity, sensitive actions, stronger techniques, or report submission.

Live-bounty automation substrate: `schemas/live_bounty_lane_state.schema.json`, `schemas/live_bounty_evidence.schema.json`, `handoff/live_bounty_lane_queue.json`, `scripts/live-bounty-lane-status.py`, `scripts/live-bounty-lane-runner.py`, `scripts/live-bounty-preview-grounding.py`, and `scripts/evidence-redaction-check.py` now provide machine-readable lane state, evidence summaries, queue validation, status summaries, local-only queue runner decisions, reference-grounded preview packets, and local evidence redaction checks. This engineering substrate is sealed at `handoff/live_bounty_automation_substrate_closeout_20260525.md`; do not add more local-only tooling by default before resolving the next operator gate. Current implementation handoff: `handoff/live_bounty_automation_engineering_slice_20260525.md`.

## Worker context entrypoints

`bin/hermes` now injects a required-context-read block into Cowork, Claude Impl, and Codex prompts. Workers should read these entrypoints when present before planning/editing/reviewing:

```text
handoff/current_navigation.md
handoff/active_strategy_queue.md
handoff/current_artifact_index.md
handoff/accepted_changes.md (recent entries / append-only history)
notes/obsidian_projects/Cybersec Lab.md
handoff/proof_library_live_bounty_bridge_20260525.md (when planning live-bounty lanes)
```

This preserves current-stage and long-term goal context without dumping the whole Obsidian vault into every worker prompt. For live-bounty planning, workers should use the bridge to map local proof patterns to live prerequisites before proposing target-touching work.

## Current phase entry

Current Phase 5A is active: authorized-assessment readiness, one-shot vulnerability-intelligence intake, cautious live-bounty bridge work, and high-hit-rate live investigation selection. The first-flow practice goal is satisfied by <program-redacted>; new live work should start with A0 passive OSINT/program scoring, tactical preview that expands options before narrowing, then one selected bounded lane with A/B or tenant controls. Operator correction on 2026-05-26: the platform should not exclude tactics merely because realistic attackers use dangerous methods; instead it should model full attack paths, compile them into bounded proof surrogates, and stop before harm/data access/destructive impact. Current platform-direction artifact: `handoff/tactical_freedom_platform_direction_20260526.md`. Current high-hit-rate planning artifacts: `handoff/live_bounty_high_hit_rate_target_filter_20260526.md`, `handoff/live_bounty_attack_class_matrix_20260526.md`, `handoff/next_live_bounty_shortlist_20260526.md`, `handoff/live_bounty_tactical_preview_template_20260526.md`, `handoff/live_bounty_no_finding_feedback_log.md`, `handoff/live_bounty_account_ab_operator_action_card_20260526.md`, and `handoff/program-redacted_target_selection_preview_20260526.md`. `<program-redacted>` / <program-name> is the selected third target. Scope is confirmed from logged-in <bug-bounty-platform> CSV; `programs/<program-redacted>/scope.json`, `programs/<program-redacted>/lane_state.json`, and selected global scope entries already exist. Account B signup/auth was completed locally by the operator, and Hermes performed a low-speed owned/passive onboarding/dashboard map only. Current <program-name> artifacts: `handoff/program-redacted_account_b_passive_surface_map_20260526.md` and `handoff/live_bounty_evidence/<program-redacted>/owned_account_signup_profile_workspace_surface_map/evidence_surface_map_20260526.json`. Current state is `surface_only` / `not_report_ready`: shared inbox labels exist, external channel connection is still the hard gate, and Hermes must stop before channel/OAuth/mailbox connection, invite/team mutation, workflow/rule/Topics activation, API tokens/calls, messages/comments/discussions, scanners/fuzzers/DAST, report promotion, or report submission.

<program-redacted> Taiwan <bug-bounty-platform> status: a minimal program scope artifact now exists at `programs/<program-slug>/scope.json`, selected assets are present in `config/scope.txt`, and the first pre-second-phone single-account surface/auth boundary check is complete in `handoff/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md`. Result: no reportable vulnerability; no owned object ID suitable for IDOR/BOLA proof; Account B or program-provided test accounts remain required for cross-account ownership testing. Use `handoff/proof_library_live_bounty_bridge_20260525.md` before any next live-target step.

Live automation gate status: `gate_fixed_dry_run_verified` for the previously observed compatibility blockers, with additional fail-closed hardening coverage. Focused regressions now verify `--program <program-slug> --policy-mode dry-run` accepts exact in-scope <program-redacted> dry-runs, global scope validation accepts intentional `localhost`, `example.org` remains rejected, malformed/path-like slugs fail before target processing, `--skip-scope-check` cannot combine with program policy, `--policy-mode dry-run` requires `--dry-run`, and `--policy-mode` without `--program` is rejected. This is still only dry-run readiness; live scanner-like automation remains blocked unless a separate narrow operator-approved plan confirms exact <bug-bounty-platform> rules/scope/technique.

Thanks-only/VDP first-complete-flow lane: <program-redacted> VDP policy intake, operator <bug-bounty-platform>-alias signup/login gate, and first noVNC owned-account auth/session/profile/workspace empty-state surface map are complete. Artifacts: `programs/<program-slug>/scope.json`, `programs/<program-slug>/lane_state.json`, `handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_surface_map_20260525.json`, `handoff/tines_automation_vdp_owned_account_surface_map_20260525.md`, and `handoff/tines_automation_vdp_phase5a_dry_run_packet_20260525.md`. `login.<program-redacted>.com` remains the only <program-redacted> entry in `config/scope.txt`; the generated owned workspace subdomain was treated as browser-only post-login continuation and was not promoted to scanner/script scope. Result: `NO_FINDING_CLOSEOUT` / `no_finding` with evidence status `surface_only`; runner decision is `lane_closed_or_parked` / exit `0`. Scanners/fuzzers/DAST, workflow execution, run-script, callbacks, integrations, cross-tenant testing, non-owned data, setting mutation, API-key/credential creation, and report submission remain blocked. Any next <program-redacted> lane requires a separately approved plan.

Arcane local-bootstrap prep status: `handoff/arcane_global_variables_precheck_posture_20260525.md` records a fail-closed precheck from the Windows control plane (`docker CLI missing`). Arcane setup/proof remains blocked until a disposable victim-lab Docker daemon/proxy posture is confirmed.

Phase 4 is effectively closed unless the operator identifies a concrete missing ability gap. The next default work is not more local lab vulnerability quantity; it is bridge/live-prerequisite conversion, authorization-gate hardening, scope/package readiness, report-readiness conversion, and metadata-only vulnerability-intelligence routing.

Current Phase 5A anchors:

```text
handoff/live_bounty_lane_queue.json
scripts/live-bounty-lane-runner.py
scripts/live-bounty-preview-grounding.py
handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md
handoff/live_bounty_automation_substrate_closeout_20260525.md
handoff/tines_automation_vdp_owned_account_surface_map_20260525.md
handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_surface_map_20260525.json
schemas/live_bounty_lane_state.schema.json
schemas/live_bounty_evidence.schema.json
handoff/phase5a_authorized_live_target_dry_run_template.md
handoff/phase5a_report_readiness_checklist.md
handoff/proof_library_live_bounty_bridge_20260525.md
tools/vuln_intel_refresh.py
handoff/vuln_intel/vuln_intel_candidates_20260523T130000Z.md
```

## Current default route

- Repo root on Windows host: `<private-workspace>`.
- Preferred VM-side project mount: Kali `/mnt/hacking` / `~/projects/cybersec` when available.
- Default attacker / target-touching VM: `<attacker-vm>`.
- Deprecated attacker VM: old registered `<attacker-vm>`; treat as forensic archive only because of broken snapshot / differencing disk state.
- Victim / vulnerable-target VM: `<victim-vm>`.
- Known host-only IP evidence from latest handoff:
  - attacker: `<lab-ip>`
  - victim: `<lab-ip>`
- Default network posture: host-only.
- NAT posture: closed by default. Operator permits Hermes to open a temporary NAT window without asking again when needed to download/install/update tooling, pull vulnerable-target images, or make a better local靶機 environment; close NAT and verify Internet is closed before target-touching proof execution unless the proof specifically needs a documented temporary install window.
- Current clean attacker snapshot: `clean-attacker-v2-tools-4096m-4cpu-20260522` (`bcee6035-c86d-41f0-8da1-62b3b42ec388`).
- Attacker baseline resources: 4096 MB RAM, 4 CPUs, Docker / Compose / baseline tools available per `handoff/accepted_changes.md`.

## Current active local lab targets

Active targets are local, intentionally vulnerable, and recoverable. They are suitable for bounded local proof waves only.

1. DVWA
   - Primary use: command injection, callback-control proof, marker write/readback, shell-command impact boundary.
   - Current status: true attacker-side callback proof is already verified and should be used as the callback evidence baseline.

2. WebGoat
   - Primary use: authenticated/session workflows, JWT learning lanes, IDOR/access control, path traversal, XSS lessons.
   - Current status: authenticated session handling and JWT decode lane have verified handoff/bundle records.

3. Juice Shop
   - Primary use: SQLi behavior, file listing/read metadata, upload validation, auth/access boundary, browser XSS probe calibration.
   - Current status: bounded `q` SQLi behavior and earlier verified/candidate flows are recorded; keep outputs candidate/report-readiness gated.

4. `labs/modern_vuln_api/modern_vuln_api.py`
   - Primary use: disposable source-controlled patterns for SSRF, XXE safe-marker, browser-runtime XSS, unsafe deserialization marker, upload retrieval, IDOR, auth/session role separation.
   - Current status: useful local target when Docker is unnecessary or when a precise proof primitive is needed; now includes a verified multi-role admin-audit/secure-admin-control proof shape.

## Current proof library index

The short reusable proof-pattern map is now:

```text
handoff/proof_library_index_20260523.md
```

Use it before starting a new wave. It maps verified/candidate bundles to targets, scripts, handoffs, artifact roots, minimum evidence shapes, and next-lane routing.

## Top active lanes

1. First <bug-bounty-platform> authorized-scope intake
   - Current status: waiting for operator-provided <bug-bounty-platform> program policy/scope package.
   - Intake packet: `handoff/hackerone_first_scope_intake_20260525.md`.
   - Next use: once filled, Hermes converts exact policy facts into `programs/<program-slug>/scope.json`, asks for explicit confirmation before adding global `config/scope.txt` entries, and prepares a single-lane dry-run packet.

2. Phase 5A authorized live-target dry-run readiness
   - Current status: templates created in `handoff/phase5a_authorized_live_target_dry_run_template.md` and `handoff/phase5a_report_readiness_checklist.md`.
   - Next use: when the operator provides a legal target/scope package, fill these before any target-touching work.

3. Vulnerability-intelligence refresh / latest capability intake
   - Current status: one-shot metadata-only MVP implemented at `tools/vuln_intel_refresh.py` and sampled into `handoff/vuln_intel/vuln_intel_candidates_20260523T130000Z.md`.
   - Routing: `local_bootstrap_review`, `local_or_live_review_high_impact`, `needs_authorized_live_target`, or `reference_only_review`.
   - Boundary: no scanning, exploit execution, target bootstrap, live-target probing, or report submission.

4. Selected local-bootstrap planning candidate
   - Selected candidate: Arcane `<specific-ghsa-id>`, missing admin authorization on global variables endpoint.
   - Current artifacts: `handoff/phase5a_arcane_global_variables_bootstrap_plan_20260523.md`, `handoff/phase5a_arcane_global_variables_feasibility_review_20260525.md`, `handoff/arcane_global_variables_bootstrap_precheck_run_card_20260525.md`, `handoff/arcane_global_variables_precheck_posture_20260525.md`, `scripts/labs/arcane_global_variables_bootstrap_precheck.sh`, and `targets/catalog/arcane_ghsa_jpjh_jm2p_39hh.md`.
   - Current status: source/install feasibility reviewed; fail-closed precheck/run-card drafted; Windows control-plane precheck was blocked/fail-closed because Docker CLI is missing; no target touched. Feasible only with a disposable Docker daemon/proxy posture; do not mount a host/user Docker socket.
   - Boundary: setup/proof must not run until the disposable Docker daemon/socket posture is confirmed from the intended victim-lab environment.

Recent completed proof lanes retained for reuse:

- Deserialization bounded-marker operator proof: `handoff/modern_api_deserialization_bounded_marker_operator_verified_20260523.md`.
- File-read/path traversal safe-marker proof: `handoff/modern_api_path_traversal_file_read_wave1_20260523.md`.
- Auth/session role-separation proof wave: `handoff/modern_api_auth_role_separation_wave1_20260523.md`.

Completed packetization:

- SSRF true-attacker callback evidence packet: `handoff/modern_api_ssrf_true_attacker_callback_evidence_packet_20260523.md`.
- DVWA command-injection callback evidence packet standard: `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md`.
- WebGoat browser-runtime XSS evidence packet: `handoff/webgoat_browser_runtime_xss_evidence_packet_20260523.md`.

## Tactical preview / Claude Code review lenses

Current one-vulnerability wave sequence includes two lightweight tactical perspectives, not new safety gates:

```text
OSS/source reconnaissance
-> Hermes tactical preview
-> Kali bounded-script execution
-> artifact/evidence pullback
-> Claude Code read-only review
-> Hermes synthesis: verified-impact / bundle / evidence-packet promotion
```

- Hermes owns preview before target-touching execution. Preview should broaden tactical options, compare tool/wrapper/custom runner choices, identify weak proof/value/artifact gaps, and choose the highest-project-value local-lab path without prematurely eliminating viable lanes. Preview must enumerate useful possibilities before prioritizing; it is not a narrowing filter.
- Each wave preview must answer these five tactical questions before execution:
  1. What is the maximum safe proof for this vulnerability behavior: callback, marker file write/readback, browser-runtime DOM marker, auth-boundary bypass, server-side identity, or controlled config/data exposure?
  2. Can the current target prove that maximum safe proof? If not, do not force it; add/modify a recoverable local target or choose a better local lane.
  3. What is the minimum positive/control evidence required? Without a meaningful control, do not label the result `verified-impact`.
  4. If the primary trigger is blocked, what two alternate lanes still have learning value: operator-run exact trigger, source-level sink/gadget inventory, adjacent safe-marker lane, or equivalent disposable target?
  5. Which proof-library capability does this wave add? If it only adds another log with no reusable evidence pattern, downgrade or choose a better lane.
- Claude Code owns post-evidence review by default, using a compact read-only evidence packet. Review should challenge proof value and overclaim risk, classify status, and recommend stop/rerun/switch/packetize.
- Neither preview nor review should become a new safety process, approval layer, or governance-first gate. Existing scope/recovery boundaries remain, but the purpose here is tactical perspective and project value.
- Do not default to multiple reviewers. Escalate only when the operator explicitly asks or when Hermes needs specialist perspective for an unusually ambiguous local-lab lane.

## Exploration breadth principle

- Operator preference: do not shrink the project to only the easiest or already-proven lanes. In the authorized recoverable local lab, try every useful proof possibility that can be tested with bounded scope, source/provenance, pre/post health, artifacts, and honest status labeling.
- Operator preference: do not categorically filter out vulnerability classes just because the best proof needs a live/real target. If a candidate cannot be faithfully reproduced in the local lab but appears valuable and could be tested legally, pause and ask the operator what authorized target/scope/rules they can provide instead of dropping the lane.
- `Can be tried` does not mean `must be claimed successful`: retain useful attempts as `verified-impact`, `valuable-candidate`, `attempted-not-verified`, `blocked/deferred`, or `reference-only` according to evidence.
- When a primary path is blocked or unsuitable, preserve breadth by switching route rather than abandoning the class: operator-run script, source-level proof, equivalent disposable target, adjacent safe-marker lane, mature OSS tool wrapper, or local target expansion.
- Do not use safety/process/navigation cleanup as a reason to prematurely narrow the project. Use them to keep exploration recoverable, artifacted, and searchable.

## Live target escalation rule

- Default remains local/recoverable lab first, because it is fastest, safest, and easiest to rerun.
- Local-lab fit is a prioritization signal, not a hard exclusion filter. Do not discard classes such as cloud/service-specific bugs, SaaS/business-logic issues, auth flows, OAuth/OIDC, webhook behavior, payment/workflow bugs, mobile/API behavior, or product-specific CVEs solely because they need a real/live target to prove.
- If a live target is needed, Hermes should ask the operator for the minimum legal scope package before target-touching work:
  - target URL/app/API/product/version and environment type;
  - written authorization or program/scope link;
  - in-scope and out-of-scope assets/actions;
  - allowed test classes, rate limits, time windows, and notification/reporting rules;
  - account/test-data availability and whether destructive/state-changing tests are allowed;
  - required redaction/evidence handling and whether external callbacks/OAST/tunnels are allowed.
- Until that package is provided, keep the candidate as `needs_authorized_live_target` / `blocked-awaiting-scope`, retain source/proof notes, and prefer local simulation only when it preserves the vulnerability's real proof value.
- Never silently convert this into public-target testing; authorized live-target work is a user-provided scope lane, not an automatic escalation.

## Secondary lanes after top 3

- Auth/session handling: throwaway accounts, cookie/session/token capture, role separation, re-auth, replay controls.
- Evidence packet / report-readiness gate: turn one strong local proof into a reusable packet with impact, limits, cleanup, and retest notes.
- Source-driven script/tool selection: use source/context to select or adapt a small script/tool chain; only modularize after a useful proof exists.
- Mandatory OSS-first rule: before every new script and before every meaningful bundle optimization, first check mature open-source projects/tools/templates/docs, then record `adopt`, `wrap`, `adapt`, `reference-only`, or `write-custom` with provenance.
- Target-environment expansion: if the current靶機 is the wrong surface, Hermes may automatically add/modify a recoverable local VM/container target, including temporary NAT for downloads/pulls, provided scope, pre/post health, artifact path, and close/verify are recorded.

## Parked / deprecated lanes

Parked for now, not deleted:

- Contract-first / schema-first / importer-first / report-generator-first work.
- Large governance or validator expansion that does not directly improve local proof quality.
- Public or real bug bounty target testing.
- Authorized live/real target lanes without a user-provided scope package; if the operator can provide legal target/scope/rules, keep the candidate active as `needs_authorized_live_target` instead of permanently parking it.
- Automated confirmation, automatic report submission, scheduler/CI target-touching automation.
- Broad platform integration before proof packets stabilize.
- Old `<attacker-vm>` route except for forensic recovery/reference.

## Recovery and snapshot rules

- Treat the local lab as recoverable but not disposable without records.
- Before destructive/aggressive local tests: confirm the correct VM route, snapshot/recovery plan, pre-health, artifact path, and cleanup plan.
- Operator explicitly allows aggressive/destructive scripts against the authorized recoverable local靶機 when the work remains inside the lab and recovery/post-health are verified; this includes bounded marker overwrite, service breakage, or lab-state corruption if snapshot/container recovery is known.
- Operator also allows Hermes to make necessary recoverable local靶機 changes automatically when a better target surface is needed: add/modify Docker containers, pull vulnerable images, install lab tools, or create small source-controlled vulnerable services. Use temporary NAT only as needed, document provenance/source, then close/verify NAT before normal proof execution.
- After tests: record post-health, cleanup, restored network posture, and whether snapshot restore was needed.
- NAT windows must be temporary and must be followed by a close/verify note.
- Runtime VM state is not durable truth; repo handoff and named artifacts are the durable project record.

## Execution-layer safety blocker handling

- If Hermes terminal/tool safety blocks an authorized local-lab exploit trigger with `BLOCKED` / `Do NOT retry`, do not rewrite, disguise, encode, split, or move the same trigger into another command just to bypass the block.
- Treat this as an execution-layer limitation, not as a project capability dead-end.
- Preserve project capability growth by choosing one explicit route:
  1. convert the blocked step into a reviewed operator-run run-card with exact command, scope, expected artifact, rollback, and verification so the human operator can run it manually in the authorized lab if desired;
  2. redesign the proof as a source-level unit/integration test inside the disposable target when that still proves the vulnerability behavior truthfully;
  3. switch to an equivalent local靶機/lane that avoids the blocked pattern while preserving the same learning objective;
  4. record the blocker and continue with adjacent proof capability instead of stalling the project.
- For high-value lanes likely to trigger safety filters — SSRF callback, XXE external entity callback, deserialization gadget behavior, command injection callbacks, internal callback proof — prepare the run-card/operator route up <program-name> instead of discovering the block late.
- Operator preference: when the same execution-layer blocker pattern appears, do not keep trying variants through Hermes. Instead, create a Kali-side operator-run script/run-card like the first successful SSRF operator path: precheck-only mode, exact local-lab scope, artifact directory, cleanup/post-health, and a human confirmation gate before the single sensitive trigger. Hermes may then review/pull back artifacts after the operator runs it.

## Artifact location convention

Default artifact root:

```text
<artifact-output-dir>/<lane_name>_<YYYYMMDDTHHMMSSZ>/
```

Each meaningful proof wave should preserve:

- `README.md` or `summary.md` with target, route, vulnerability class, proof narrative, boundaries, and cleanup.
- command transcript or exact rerun commands.
- request/response summaries or tool output.
- callback logs, browser evidence, marker file evidence, or session evidence when relevant.
- pre-health and post-health result.
- limitations / false-positive controls.
- report-readiness decision: `local_learning`, `reusable_methodology`, `candidate_needs_manual_review`, or `report_ready_lab_only`.

Promote only stable, reusable workflows to:

```text
modules/bundles/<bundle_name>.md
scripts/SCRIPT_INVENTORY.md
```

## Evidence packet minimum shape

For each one-vulnerability proof wave, record:

```text
Target:
Vulnerability class:
Authorized scope:
Route/tool:
Preconditions:
Exploit/probe path:
Evidence:
Impact:
Controls / false-positive boundary:
Cleanup:
Rerun commands:
Report-readiness:
Project benefit:
New/changed artifacts:
```

## Memory and Obsidian routing

- Hermes global memory: compact cross-project signposts only.
- Repo handoff: engineering truth, validation, active lane, safety boundaries, accepted changes.
- Obsidian `Projects/Cybersec Lab/`: strategy, rationale, methodology, navigation synthesis.
- `session_search`: recall only; verify against repo or Obsidian before treating it as current.
- Do not store raw sensitive targets, scans, credentials, loot, tokens, hashes, private scope/rules, or exploit evidence dumps in global memory or broad Obsidian notes.

## Next safe slice

Recommended next implementation/research sequence:

1. Use this navigation cleanup as the current map.
2. DVWA attacker-callback proof packet standardization is complete; use `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md` as the callback baseline.
3. Browser-runtime XSS proof packet is now complete for WebGoat; path traversal upload-write and Zip Slip are also verified for WebGoat.
4. Next best lane: Phase 5A authorized-assessment readiness. Use `handoff/phase5a_authorized_live_target_dry_run_template.md`, `handoff/phase5a_report_readiness_checklist.md`, and `tools/vuln_intel_refresh.py`; do not touch live targets without an operator-provided legal scope package.

## Freshness rule

When this file conflicts with a frozen review or older handoff:

1. Current explicit operator instruction wins.
2. Live repo/config/tool state wins for facts that can be verified.
3. `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/lab_safety_contract.md`, and `handoff/accepted_changes.md` are the current navigation layer.
4. Older handoff and archived queues remain rationale/history, not current navigation.
