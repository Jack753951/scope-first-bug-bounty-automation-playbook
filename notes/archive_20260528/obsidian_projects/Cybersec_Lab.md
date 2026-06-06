> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersec Lab

## Active north star: automated multi-agent bug bounty platform

Status: active project direction / supersedes narrower first-bounty-only framing
Source: Operator direction + Hermes synthesis
Last updated: 2026-05-28
Repo truth: `.hermes.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `platform/`, `programs/<slug>/`, `docs/policy/`

Maintenance note: keep this active section current by editing it in place. Use dated sections
below only for historical/audit checkpoints, not as the default way to evolve strategy.

- The project’s active goal is an automated, multi-agent collaborative bug bounty platform and capability library, not a human-readable notes repo or a one-off first-report sprint.
- Hermes is the project owner: task decomposer, scheduler, worker router, final verifier, and safety gate. Hermes should maintain a clear expected working-tree and engineering direction, object to work that drifts from the long-term platform/capability-library goal, and pause for strong-agent or operator advice when direction is unclear.
- Strong external agents should be called frequently for unclear direction, architecture, tactic selection, recurring automation, target-pattern fit, evidence/reporting, implementation review, and safety-boundary dissent. Before invocation, sync memory/context by engineering means: `.hermes.md`, current navigation, active queue, artifact index, this Obsidian bridge, accepted changes, relevant program state, and stop-before rules.
- Practical hunting runs on two tracks: (1) recurring latest-vulnerability/intel/recon work validates proof in local lab/靶機, then consolidates reusable bundles/library entries; (2) multi-agent target matching applies proven patterns to suitable in-scope targets for bounded proof-only tests.
- In-scope testing, including aggressive or attack-shaped scripts, is authorized when exact bug-bounty scope and program rules allow the target and technique. The execution boundary remains strict: obtain only minimum proof, do not browse/download/modify/exfiltrate internal/customer/non-owned data, and keep final submission operator-gated.
- For signup/auth gates, Hermes may fill and submit env-stored email/password/phone/default alias fields when program rules allow account creation; stop and notify the operator for email verification, SMS verification, OTP, CAPTCHA, unexpected billing/payment gates, or final report submission.
- Every practical run should feed the capability library: website/product type, suitable vulnerability classes, common vulnerable objects, controls/kill criteria, evidence patterns, and report lessons.

### Recurring cadence target

- Minute-level: CT log subscription, Censys/SecurityTrails-style enrichment, new program/scope expansion alerts, CVE/PoC GitHub/RSS intake.
- Hourly: differential `subfinder`/`dnsx`/`httpx` and nuclei only on newly discovered endpoints or changed asset state.
- Daily: full passive inventory refresh, tech fingerprint refresh, NVD recent-modified, CISA KEV diff, nuclei template update, and allowed-scope sweep.
- Weekly: deep feroxbuster/wordlist, JS endpoint extraction, Arjun parameter discovery, bundle/CMS version inventory, disclosed-report mining, and new-program policy intake.
- Monthly: full asset re-inventory, tech-stack pivot assessment, bug-class strategy review, metrics/funnel review, and capability-library cleanup.

### Structural engineering direction

- First priorities: contract alignment for `scope.json`/`lane_state.json`, platform core migration, evidence-to-report pipeline, detector harness, artifact/path integrity checker, repo hygiene, and environment-specific validation profiles.
- Near-term ROI lanes: reporting automation, authentication/session state management, submission tracking, hourly differential recon, disclosed-report mining, mobile static analysis, and vendor advisory diffing.
- Do not spend platform time on web UI, SaaS/multi-tenant, distributed scanner, custom vulnerability database, custom ML, or reimplementing mature tools unless the operator explicitly changes strategy.

## 2026-05-27 process gate simplification

Status: active strategy correction / no target touched
Repo truth: `docs/policy/review_tiering_policy.md`, `docs/policy/multi_party_review_decision_policy.md`, `docs/policy/active_testing_policy.md`, `docs/policy/oss_recon_gate.md`, `.hermes.md`, `handoff/active_strategy_queue.md`

- Operator rejected additional tiering and asked to simplify/delete unnecessary gates that affect project growth.
- Active direction: historical review tiers and multi-party approval ceremony are no longer blockers. Hermes should favor capability-library growth, local-lab proof iteration, runnable scripts, compact machine-readable handoff, and checkpoint-driven bounty progress.
- Claude/Cowork/Codex review is advisory unless it names a concrete hard-stop blocker: authorization/scope ambiguity, live external side effect, secret/customer-data risk, unsafe account mutation, failing validation, or data/capability loss.
- Hard boundaries remain strict for live-target active testing, callbacks/OAST/tunnels, OAuth/integrations/API tokens, scheduler/deployment/publishing, secrets/PII/customer data, destructive behavior, report promotion, and final submission.

## 2026-05-27 Hermes profile isolation boundary

Status: profile created / cron-Gateway migration pending / no target touched
Repo truth: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`, `.hermes/plans/2026-05-27_142630-hermes-profile-isolation-plan.md`

- Created a dedicated Hermes `cybersec` profile for future Cybersec Lab sessions; use `hermes --profile cybersec` or alias `cybersec` from `<private-workspace>`.
- Also created a separate `youtube` profile for the YouTubeAgent project, but Cybersec Lab truth remains in this repo and this Obsidian note.
- `default` remains the current Gateway/cron owner during transition; profile creation intentionally did not migrate or duplicate scheduled jobs.
- Boundary: memory/session/profile hygiene only; no live target contact, scanner/fuzzer/DAST, exploit/callback, account mutation, scope edit, report promotion, or report submission.

## 2026-05-27 cleanup checkpoint + <program-name> practical passive resume

Status: checkpointed / live passive mapping resumed / not report-ready
Repo truth: `0412cb7`, `programs/<program-redacted>/notes/program-redacted_live_practical_resume_20260527.md`, `programs/<program-redacted>/lane_state.json`, `handoff/kali_vm_operations_state.json`

- Checkpointed the broad cleanup migration before continuing live work.
- Resumed <program-name> through Kali/noVNC only as passive observation of an already authenticated owned workspace.
- Current useful next work: map visible <program-name> settings/sidebar/setup-guide gates and preserve candidate bundles, without Create/Connect/Save/Invite/Send/Token/API/Activate actions.
- Boundary remains strict: no scanner/fuzzer/DAST, scripts against target, channel/OAuth/mailbox/webhook/integration connection, invite/role/team mutation, workflow/rule/Topics activation, API token/API call, customer/non-owned data, secret/cookie/token handling, report promotion, or report submission.

## 2026-05-27 periodic third-party agent review and cleanup closeout

Status: complete / conditional continue / no target touched
Repo truth: `handoff/periodic_reviews/2026-05-27/agent_review_synthesis.md`, `handoff/periodic_reviews/2026-05-27/cleanup_closeout_status.md`, `handoff/active_strategy_queue.md`

- Ran three read-only Hermes delegate_task third-party reviewers: strategy/goal drift, engineering cleanup hygiene, and memory-sync/worker-attestation.
- Synthesis verdict: direction remains aligned with the long-term goal of a legal, recoverable, scope-aware, script-first platform that turns authorized contexts into high-value proof packets.
- Cleanup verdict: migration direction is sound and manifest reconciliation passed, but the broad dirty tree should be checkpointed before unrelated new work.
- Memory-sync verdict: formal Cowork/Claude Impl/Codex wrapper routes have tested context-read/attestation gates; delegate_task reviews are useful but must be persisted as named artifacts when used as formal review evidence.
- Boundary: review/docs/index cleanup only; no live target, scanner/fuzzer/DAST, exploit/callback/OAST, VM/browser action, credential handling, scope edit, report promotion, or report submission.


## 2026-05-27 GHSA tmp path traversal verified local proof

Status: complete / verified local-lab proof / not live-authorized
Repo truth: `handoff/tmp_path_traversal_ghsa_ph9p_verified_local_lab_20260527.md`, `modules/bundles/verified_lab_flow_tmp_path_traversal_arbitrary_file_creation.md`, `labs/proofs/tmp_path_traversal_ghsa_ph9p_20260527.md`

- Continued the 2026-05-27 vuln-intel loop beyond metadata planning into a disposable Kali victim-lab proof after explicit operator instruction.
- Selected `<specific-ghsa-id>` / npm `tmp@0.2.5` because it is verifiable with synthetic marker files and no live target, account, scanner, callback, or privileged Docker posture.
- Result: `verified_tmp_path_traversal_arbitrary_file_creation_lab_only`; control file stayed inside `safe-base`, escaped marker landed in sibling `escape-zone`, and temporary victim NAT was closed after package acquisition.
- Boundary: local proof pattern only; live use requires exact program scope/rules, app data-flow into vulnerable tmp options, owned synthetic paths/files, and stop-before rules for sensitive file access, overwrite, web-root write, persistence, code execution, callbacks, and report submission.


## 2026-05-26 <program-name> Account B passive owned-surface map

Status: complete / surface_only / not report-ready
Repo truth: `programs/<program-redacted>/lane_state.json`, `programs/<program-redacted>/notes/program-redacted_account_b_passive_surface_map_20260526.md`, `handoff/live_bounty_evidence/<program-redacted>/owned_account_signup_profile_workspace_surface_map/evidence_surface_map_20260526.json`

- Operator completed Account B signup/auth locally; Hermes observed only post-auth owned/passive UI via Kali/noVNC.
- Observed owned surfaces: Customer Support shared section, `Support` and `Support - Priority` inbox labels, setup guide, and the first shared-channel connection gate.
- Current lane state is `A2_SURFACE_MAP_COMPLETE` / `surface_only`; useful bundles remain preserved, but proof/reporting is blocked without a fresh owned A/B boundary and explicit approval for any state-changing action.
- Boundary: no external channel/OAuth/mailbox connection, invite/role/team mutation, workflow/rule/Topics activation, API token/API calls, messages/comments/discussions, customer/non-owned data, scanners/fuzzers/DAST, report-ready promotion, or report submission.

## 2026-05-26 <program-name> BLOCK reduction + bundle preservation

Status: passive mapping extended / proof not ready / no target app touched
Repo truth: `programs/<program-redacted>/notes/program-redacted_passive_docs_bundle_map_20260526.md`, `programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md`, `programs/<program-redacted>/lane_state.json`

- Resolved only the safe, non-target-touching BLOCK issues: tightened object-creation language, added docs-derived expected permission matrix, and preserved all useful bundle families.
- Current lane remains blocked for proof. Allowed next work is passive UI/docs mapping only.
- Bundle preservation rule for <program-name>: do not throw away inbox membership, non-public group linking, conversation cross-listing, message/comment/draft split, workflow/rule routing, channel/OAuth, API/UI mismatch, plugin context, archive/delete residue, or metadata-only leak families until a later synthesis deliberately parks them.


## 2026-05-26 <program-name>-specific multi-agent workflow practical test

Status: completed / BLOCK beyond passive mapping / no target touched
Source: actual Claude Code + Codex read-only review
Date: 2026-05-26
Repo truth: `programs/<program-redacted>/notes/program-redacted_multi_agent_review_synthesis_20260526.md`, `programs/<program-redacted>/lane_state.json`, `handoff/claude_program-redacted_tactical_boundary_evidence_review_20260526.json`, `handoff/codex_program-redacted_deterministic_review_20260526.md`

- Tested the new memory-sync + multi-agent rule on <program-name> `<program-name>-shared-inbox-object-permission`.
- Claude Code provided tactical/boundary/evidence findings and returned REQUEST_CHANGES; Codex deterministic review returned BLOCK.
- Hermes synthesis keeps <program-name> passive-only: no object creation, invite/role action, token/API call, workflow activation, external channel connection, customer/non-owned data, scanner/fuzzer/DAST, or report submission.
- Value: workflow preserved realistic attacker hypotheses while preventing premature proof execution. Next safe step, if continued, is passive UI/docs mapping only.


## 2026-05-26 multi-agent tactical review + memory-sync correction

Status: active workflow rule / no target touched
Source: operator correction + Hermes skill update
Date: 2026-05-26
Repo truth: `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md`, `handoff/active_strategy_queue.md`, user-local skill `authorized-attacker-flow`

- Role-separated attacker-flow work must not be reduced to one model reading an MD file. Non-trivial lanes require actual suitable worker invocation when available: Claude Code/Cowork for tactical, boundary, evidence, and strategy perspectives; Codex for deterministic/skeptical review and script/checklist sanity; Hermes for final synthesis and authorization gates.
- Workers must receive the project memory-sync packet (`.hermes.md`, current navigation, active queue, artifact index, Cybersec Lab Obsidian bridge, recent accepted changes, active scope/lane state, current candidate/evidence packet, and stop-before rules), not only a single task artifact.
- If Claude/Codex/Cowork routes are unavailable, skipped, timed out, or replaced by Hermes for speed, the artifact must record that blocker and the lane remains passive-only unless the operator approves a fresh exception.
- This is workflow/process memory only; it does not authorize target-touching work, scanner/fuzzer/DAST, callbacks, token handling, customer/non-owned data contact, or report submission.
- Same-day Claude Code and Codex read-only reviews returned `REQUEST_CHANGES`; incorporated the stricter rule: non-trivial lanes require actual Claude/Cowork + Codex participation or a structured skipped-route/passive-only record, plus invocation evidence beyond artifact shape.


## 2026-05-26 tactical-freedom platform correction

Status: active design direction / no target touched
Source: operator correction + Hermes synthesis
Date: 2026-05-26
Repo truth: `docs/policy/tactical_freedom_platform_direction_20260526.md`, `docs/strategy/platform/multi_agent_bug_hunting_engineering_plan_20260526.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`

- The project should not exclude tactics merely because realistic attackers use dangerous or destructive-looking methods. High-value bug bounty work needs realistic attack-path imagination, not conservative scanning by default.
- The core ethical line is different: model the full attack path, but execute only bounded, authorized, recoverable proof surrogates and stop before unauthorized access, non-owned data contact, destructive impact, DDoS/resource exhaustion, credential theft, malware, stealth/persistence/evasion, uncontrolled propagation, or report submission.
- The prior L0-L5 ladder is now secondary/internal; the preferred planning primitive is `attack path -> proof boundary -> proof surrogate -> stop condition -> evidence packet`.
- Multi-agent advantage should be role separation: adversarial planner maximizes realistic hypotheses, boundary engineer converts them into lawful proof plans, implementer/toolsmith builds bounded offline helpers, evidence critic challenges overclaiming, Hermes synthesizes and enforces authorization gates.
- Immediate engineering direction: offline/local platform slice first—attack-path candidate packet, proof-boundary/proof-surrogate schema, preview synthesis helper, and A/B matrix validator. This does not authorize live scanning, exploitation, account actions, target-touching automation, or report submission.

## 2026-05-26 <program-name> target selection for first new-process live run

Status: selected candidate / pending exact asset-scope confirmation
Source: Hermes passive policy/program-metadata intake from Kali VM
Date: 2026-05-26
Repo truth: `programs/<program-redacted>/notes/program-redacted_target_selection_preview_20260526.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`

- Selected `<program-redacted>` / <program-name> as the recommended first target for the new high-hit-rate workflow.
- Reason: open bounty program, explicit researcher signup route, <bug-bounty-platform> alias requirement, API docs, customer-ops/team/workspace product shape, and policy interest in cross-company/cross-tenant disclosure plus admin/API permission boundaries.
- Deprioritized alternatives for the immediate first run: `hex` requires emailing for a bounty instance and public JSON shows no bounties; `frontegg` is strong but identity-platform-sensitive; `discourse` has temporary bounty suspension; `airtable` is staging/enterprise-request heavy.
- Critical blocker: unauthenticated public <bug-bounty-platform> JSON did not expose <program-name>'s structured asset table; exact logged-in <bug-bounty-platform> asset/scope confirmation is required before any `programs/<program-redacted>/scope.json`, `config/scope.txt`, signup/login, or target-touching work.
- Boundary: passive <bug-bounty-platform> program JSON/policy intake only; no <program-name> app navigation, signup, account creation, scan/fuzz/exploit, credential handling, customer interaction, or report submission.

## 2026-05-26 tactical-freedom and no-finding learning loop

Status: active / template and feedback loop added
Source: Hermes synthesis after operator confirmed the improvement direction
Date: 2026-05-26
Repo truth: `docs/strategy/live_bounty/live_bounty_tactical_preview_template_20260526.md`, `docs/strategy/live_bounty/live_bounty_no_finding_feedback_log.md`, `docs/strategy/live_bounty/live_bounty_account_ab_operator_action_card_20260526.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`

- Added the tactical preview template so live-bounty previews expand options before narrowing, list default and adjacent creative lanes, classify risk/prerequisites, and preserve blocked ideas as next-preview seeds.
- Added the no-finding feedback log so <program-redacted>/<program-redacted> no-finding and surface-only outcomes update target-selection rules instead of becoming dead history.
- Added the Account A/B operator action card with safe reply phrases for Account B, Tenant B, object visibility, and auth/phone/email/CAPTCHA blocks; secrets and raw identifiers stay out of repo/chat.
- Boundary: planning/templates/strategy only; no target asset navigation, account creation, scope expansion, scanning/fuzzing/DAST, exploit execution, credential handling, or report submission.

## 2026-05-26 high-hit-rate live investigation selection

Status: active / passive OSINT-first selection layer
Source: Hermes A0 passive program-directory OSINT and local synthesis
Date: 2026-05-26
Repo truth: `docs/strategy/live_bounty/live_bounty_high_hit_rate_target_filter_20260526.md`, `docs/strategy/live_bounty/live_bounty_attack_class_matrix_20260526.md`, `docs/strategy/live_bounty/next_live_bounty_shortlist_20260526.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`

- The second live/VDP flow achieved the process-familiarity goal, so the next default is no longer another full-flow surface-only practice run.
- New high-hit-rate loop: A0 passive OSINT/program scoring -> select one bug class -> confirm A/B or tenant controls -> timebox A2 viability -> run A3 bounded proof only when exact policy/scope and owned controls exist.
- Created a reusable target filter, attack-class matrix, and passive shortlist. Initial high-fit candidates for later exact policy intake are `<program-redacted>`, `discourse`, `hex`, `frontegg`, and `airtable`; these are triage leads only, not authorization.
- <program-redacted> remains useful only after Account B is ready and a safe owned object exists; otherwise park it as `blocked_no_owned_object` and switch to a better SaaS/workspace/API candidate.
- Boundary: passive public program-directory OSINT only; no target asset navigation, account creation, scope expansion, scanner/fuzzer/DAST, exploit, credential handling, or report submission.

## 2026-05-25 <program-redacted> VDP first owned-account surface map

Status: complete / no finding / surface_only
Source: Hermes noVNC live-bounty first-flow checkpoint
Date: 2026-05-25
Repo truth: `programs/<program-slug>/notes/tines_automation_vdp_owned_account_surface_map_20260525.md`, `handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_surface_map_20260525.json`, `programs/<program-slug>/lane_state.json`, `handoff/live_bounty_lane_queue.json`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`

- Operator completed the <bug-bounty-platform>-alias <program-redacted> signup/login gate locally in Kali/noVNC; no password, OTP, verification link, cookie, token, or raw alias was recorded.
- Hermes performed low-speed browser-only observation of the owned <program-redacted> workspace: Stories dashboard/editor, Credentials empty state, Resources empty state, Users/settings count, API Keys empty state, Authentication settings, Workbench, and account menu.
- Result: no reportable vulnerability observed; lane state is `NO_FINDING_CLOSEOUT` / `no_finding`, evidence status `surface_only`; local runner now returns `lane_closed_or_parked` / exit `0` for this lane.
- Boundaries respected: no scanner/fuzzer/DAST, no workflow publish/run, no Workbench prompt/tool execution, no integration/webhook/callback, no run-script, no API key/credential/resource creation, no invite, no setting mutation, no cross-tenant/non-owned data, no report submission, no <program-redacted> scope expansion beyond browser-only post-login observation.
- Next safe action: none by default for <program-redacted>. Any further <program-redacted> work requires a separately approved lane plan.

## 2026-05-25 live-bounty automation substrate

Status: sealed / local-only automation substrate complete
Source: Hermes TDD engineering slice
Date: 2026-05-25
Repo truth: `handoff/live_bounty_automation_engineering_slice_20260525.md`, `handoff/live_bounty_automation_substrate_closeout_20260525.md`, `schemas/live_bounty_lane_state.schema.json`, `schemas/live_bounty_evidence.schema.json`, `handoff/live_bounty_lane_queue.json`, `scripts/live-bounty-lane-status.py`, `scripts/live-bounty-lane-runner.py`, `scripts/live-bounty-preview-grounding.py`, `scripts/evidence-redaction-check.py`, `handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md`, `programs/<program-slug>/lane_state.json`, `programs/<program-slug>/lane_state_pending_second_account.json`, `handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_seed_20260525.json`

- Added machine-readable lane/evidence schemas, queue, status validator, local-only queue runner, reference-grounding generator, redaction checker, and focused regression tests so live-bounty work can resume at lane checkpoints instead of relying only on markdown context.
- <program-redacted> lane machine state: `A2_PENDING_OPERATOR_AUTH` / `blocked_operator_action`; next operator gate is <bug-bounty-platform> alias signup/login in Kali/noVNC or explicit proxy/header strategy; next autonomous action after that is noVNC owned-account auth/session/profile/workspace empty-state mapping.
- <program-redacted> second-account lane is parked as machine-readable state at `programs/<program-slug>/lane_state_pending_second_account.json` so the queue has no dangling state reference.
- The evidence schema keeps candidate/no-finding/report-ready vocabulary explicit and rejects unreviewed promotional states. Redaction checker is local-only and blocks common secrets/PII/token patterns before promotion, redacts findings output, and allows normal ISO dates.
- Independent review: first delegated review returned `REQUEST_CHANGES` on queue coherence and redaction-output leakage; fixes were added with regression tests; second delegated review returned `PASS`.
- Local runner status: `scripts/live-bounty-lane-runner.py` emits JSON decisions with exit codes `0/10/20/30`; current queue returns `10` / `blocked_operator_action` because the <program-redacted> top lane is waiting for an operator identity/login gate. Target-like args including bare `--target` fail closed as structured JSON exit `30`.
- Preview grounding status: `scripts/live-bounty-preview-grounding.py` generated `handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md` with OWASP WSTG/ASVS, PortSwigger, public report/docs, positive/negative controls, blocked techniques, and evidence thresholds as reference-only/non-authorizing guidance. Independent review returned `PASS`.
- Boundary: engineering/systematization only; no new safety workflow, no target request, no signup/login, no scan/fuzz/exploit, no credential handling, no report submission.
- Closeout: `handoff/live_bounty_automation_substrate_closeout_20260525.md` seals the local-only engineering substrate. Do not add more schema/governance/tooling by default; next value is resolving the <program-redacted> operator identity/session gate and then using the existing queue/status/grounding/redaction substrate for low-speed owned-account surface mapping.

## 2026-05-25 <program-redacted> VDP first-complete-flow policy intake

Status: policy intake complete / no <program-redacted> target touched
Source: Hermes passive <bug-bounty-platform> program metadata read
Date: 2026-05-25
Repo truth: `programs/<program-slug>/scope.json`, `programs/<program-slug>/notes/tines_automation_vdp_phase5a_dry_run_packet_20260525.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`

- Selected <program-redacted> VDP as the first thanks-only/VDP full-flow practice candidate.
- Policy facts captured: use research signup/login paths, use <bug-bounty-platform> email alias or `X-<bug-bounty-platform>-Research: [H1 username]`, owned accounts/data only, no service disruption, no public disclosure outside VDP.
- First lane remains small: researcher-account auth/session/profile/workspace empty-state surface map.
- Next safe action: operator confirms whether to add `login.<program-redacted>.com` to `config/scope.txt`; then run dry-run gate before account creation or live requests.
- Boundary: policy/metadata only; no target asset request, account signup, scan, exploit, fuzz, credential handling, or report submission.

## 2026-05-25 proof-library to live-bounty bridge

Status: active bridge + gate dry-run compatibility fixed / no new live target touched
Source: Hermes synthesis after <program-redacted> Taiwan single-account dry run
Date: 2026-05-25
Repo truth: `docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md`, `programs/<program-slug>/notes/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`

- Added the live-bounty bridge that maps verified local proof patterns to live prerequisites, blocked states, minimum live evidence, and report-readiness thresholds.
- <program-redacted> dry-run value: confirmed the live safety profile works on a real <bug-bounty-platform> program, converted single-account observations into `surface_only` / `needs_second_account` / `blocked_state_change`, and discovered authorization-gate compatibility blockers before any scanner-like automation.
- Current gate state: `recon.sh` now accepts lowercase underscore program slugs such as `<program-slug>`, intentionally accepts `localhost` for local-lab scope/target validation, and has focused coverage in `tests/test_recon_gate.sh` for in-scope pass / out-of-scope fail plus fail-closed CLI boundary cases: malformed/path-like slugs, `--skip-scope-check` with program policy, policy dry-run without `--dry-run`, and `--policy-mode` without `--program`. This remains dry-run readiness only, not permission for live automation.
- Added `scripts/post-proof-consolidation.sh` as the lightweight semi-automatic checklist Hermes should run after new proof/bundle/live-surface artifacts; it points to accepted_changes, navigation, active queue, Obsidian, proof index/bridge, validation commands, and wrap-up fields.
- Boundary: documentation/navigation synthesis only; no additional live target request, scan, exploit, fuzz, cross-account test, credential handling, report submission, or VM/network change.

## 2026-05-25 pre-live-target prep and <bug-bounty-platform> intake

Status: prepared / waiting for operator-provided <bug-bounty-platform> scope
Source: Hermes local prep
Date: 2026-05-25
Repo truth: `handoff/hackerone_first_scope_intake_20260525.md`, `handoff/arcane_global_variables_precheck_posture_20260525.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`

- Prepared a <bug-bounty-platform> first authorized-scope intake packet. Live-target work remains blocked until exact program policy/scope facts are supplied and converted into `programs/<program-slug>/scope.json` plus explicitly confirmed `config/scope.txt` entries.
- Ran Arcane bootstrap helper help/precheck from the Windows control plane. The helper failed closed because Docker CLI is missing on this host; no Arcane target was launched, no Docker socket was mounted, no account/proof request was sent.
- Moved the unverified CVE brief artifact to ignored local quarantine: `setting/local/quarantine/cve_brief_20260525_unverified_do_not_use.md`.
- Public methodology export staging is retained under `public_exports/`.

## 2026-05-25 Hermes worker context-read injection

Status: implemented / prompt-plumbing regression-tested
Source: Hermes local repo implementation
Date: 2026-05-25
Repo truth: `bin/hermes`, `scripts/test_hermes_worker_context_prompt.py`, `.hermes.md`, `handoff/accepted_changes.md`

- Cowork, Claude Impl, and Codex worker prompts now include a fixed required-context-read block before the task body.
- Workers are explicitly told to read `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `notes/obsidian_projects/Cybersec Lab.md`, and recent `handoff/accepted_changes.md` entries when present.
- Intent: preserve long-term goal/current-stage context for workers without dumping the whole Obsidian vault into every prompt.
- Boundary: prompt/context plumbing only; no real worker invocation against Claude/Codex and no target-touching work.

## 2026-05-25 Phase 5A Arcane source/install feasibility review

Status: feasibility reviewed / no target touched
Source: Hermes source-only review of GitHub Advisory API, `getarcaneapp/arcane` tag `v1.19.1`, patched tag `v1.19.2`, and install examples
Date: 2026-05-25
Repo truth: `handoff/phase5a_arcane_global_variables_feasibility_review_20260525.md`, `handoff/phase5a_arcane_global_variables_bootstrap_plan_20260523.md`, `targets/catalog/arcane_ghsa_jpjh_jm2p_39hh.md`

- Completed the source/install feasibility review for Arcane `<specific-ghsa-id>`; no Arcane target was launched, no Docker socket was mounted, and no proof/exploit request was sent.
- Finding: the vulnerable tag `v1.19.1` registers `PUT /api/environments/{id}/templates/variables` with Bearer/API-key auth but no `checkAdminInternal(ctx)` in `UpdateGlobalVariables`; patched `v1.19.2` adds the admin check.
- Feasibility: `ghcr.io/getarcaneapp/arcane:v1.19.1` and `:v1.19.2` manifests exist; default SQLite/admin bootstrap and login/user-management paths are identifiable, so local bootstrap appears feasible.
- Critical boundary remains high-risk: official examples use `/var/run/docker.sock` or a proxy to a Docker daemon. Any next bootstrap must use only a disposable Docker-in-Docker or isolated victim-lab daemon/proxy; never mount or expose a host/user Docker socket.
- Current next slice: fail-closed bootstrap precheck/run-card has been drafted in `scripts/labs/arcane_global_variables_bootstrap_precheck.sh` and `handoff/arcane_global_variables_bootstrap_precheck_run_card_20260525.md`. Do not run setup/proof until disposable Docker daemon/socket posture is confirmed. Live-target work remains blocked until the operator provides the promised legal scope package.

## 2026-05-23 Phase 5A selected local-bootstrap candidate: Arcane <specific-ghsa-id>

Status: selected / plan-only / superseded by 2026-05-25 feasibility review for current next action
Source: Hermes selection from `handoff/vuln_intel/vuln_intel_candidates_20260523T130000Z.md` plus GitHub advisory metadata
Date: 2026-05-23
Repo truth: `handoff/phase5a_arcane_global_variables_bootstrap_plan_20260523.md`, `targets/catalog/arcane_ghsa_jpjh_jm2p_39hh.md`

- Selected Arcane `<specific-ghsa-id>` as the first Phase 5A candidate to move from vulnerability intelligence into local-bootstrap planning.
- Rationale: recent advisory, available source/package metadata, high-value admin authorization/role-separation shape, and strong reuse of the completed Phase 4 auth/session role-separation proof pattern.
- Critical boundary: Arcane is a Docker management app; future bootstrap must use only disposable Docker-in-Docker or isolated victim-lab daemon. Never mount or expose a host/user Docker socket.

## 2026-05-23 Phase 5A authorized-assessment readiness + vuln-intel intake

Status: started / intake-only
Source: Hermes local repo implementation + public advisory metadata fetch
Date: 2026-05-23
Repo truth: `handoff/phase5a_authorized_live_target_dry_run_template.md`, `handoff/phase5a_report_readiness_checklist.md`, `tools/vuln_intel_refresh.py`, `handoff/vuln_intel/vuln_intel_candidates_20260523T130000Z.md`

- Started Phase 5A after the auth/session role-separation ability-gap proof completed Phase 4's main technical gap.
- Added a legal scope package / target map / role-account matrix / evidence-packet dry-run template for authorized live-target work.
- Added a report-readiness checklist to convert evidence into submit/not-submit decisions without overclaiming.
- Added a one-shot vulnerability-intelligence intake script that fetches metadata from CISA KEV, NVD recent, and GitHub Advisories when reachable, then classifies candidates as `local_bootstrap_review`, `local_or_live_review_high_impact`, `needs_authorized_live_target`, or `reference_only_review`.
- Generated first sample intake artifacts under `handoff/vuln_intel/`.
- Boundary: metadata-only intake; no target was scanned, exploited, bootstrapped, probed, or submitted; no scheduler was created.

## 2026-05-23 modern_vuln_api auth/session role-separation proof

Status: completed / verified_role_separation_bypass_lab_only
Source: Hermes local disposable-lab run
Date: 2026-05-23
Repo truth: `handoff/modern_api_auth_role_separation_wave1_20260523.md`, `<artifact-output-dir>/modern_api_auth_role_separation_20260523T124050Z/`, `modules/bundles/verified_lab_flow_modern_api_auth_role_separation.md`, `scripts/labs/modern_api_auth_role_separation_wave1.sh`

- Completed the Phase 4 ability-gap proof for real-target-style auth/session role separation.
- Added `modern_vuln_api` admin-path fixtures: vulnerable `/api/admin/audit-log` with lab-owned marker and secure-control `/api/admin/settings` that rejects normal users.
- Verified evidence: unauth admin-audit 401, Alice normal-user session 200, Alice admin-audit 200 with `ADMIN_AUDIT_MARKER_HERMES_LOCAL_LAB` while role=user, admin audit baseline 200, Alice admin-settings secure-control 403, admin settings 200 with `ADMIN_SETTINGS_CONTROL_HERMES_LOCAL_LAB`, post-health 200.
- Project value: fills the main Phase 4 bug-bounty-readiness gap for role/account matrix proof; future new lab vulnerability tests should be limited to explicit ability gaps, while periodic vulnerability-intelligence refresh and target bootstrap move to Phase 5.
- Boundary: local disposable lab only; no public/live target, brute force, credential theft, sensitive data, destructive write, exfiltration, callback/OAST, or finding/report promotion.

## 2026-05-23 modern_vuln_api path traversal file-read safe-marker

Status: completed / verified_file_read_safe_marker_lab_only
Source: Hermes local-lab run + read-only evidence review
Date: 2026-05-23
Repo truth: `handoff/modern_api_path_traversal_file_read_wave1_20260523.md`, `<artifact-output-dir>/modern_api_path_traversal_file_read_20260523T094352Z/`, `modules/bundles/verified_lab_flow_modern_api_path_traversal_file_read.md`, `handoff/claude_review_modern_api_path_traversal_file_read_20260523.md`

- Added a bounded `/file-read?name=` route to `labs/modern_vuln_api/modern_vuln_api.py` to create a clean second file-read/path traversal surface after the WebGoat direct-read attempt stayed attempted-not-verified.
- Ran `scripts/labs/modern_api_path_traversal_file_read_wave1.sh` from `<attacker-vm>` against victim Docker target `<lab-ip>:18083`.
- Verified evidence: pre-health 200, public-file control marker yes, missing-file negative control 404, traversal positive marker yes (`FILE_READ_SAFE_MARKER_HERMES_LOCAL_LAB`), post-health 200, target cleanup, attacker/victim Internet closed.
- Review classification: `verified_file_read_safe_marker_lab_only`; do not claim real-target exploitability, arbitrary sensitive file read, shell, persistence, exfiltration, or report-ready bug.
- Project value: fills the proof-library gap for actual marker content read via path traversal, complementing WebGoat upload-write, Zip Slip overwrite, and XXE safe-marker patterns.

## 2026-05-23 deserialization bounded-marker operator proof

Status: completed / verified_bounded_marker_lab_only
Source: Operator manual run + Hermes artifact verification
Date: 2026-05-23
Repo truth: `handoff/modern_api_deserialization_bounded_marker_operator_verified_20260523.md`, `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/`, `modules/bundles/verified_lab_flow_modern_api_deserialization_bounded_gadget.md`

- Operator manually ran `scripts/labs/operator_deser_bounded_marker_run.sh` from `<attacker-vm>` after the earlier Hermes execution-layer blocker.
- Hermes pulled attacker/victim artifacts to `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/`.
- Verified evidence: pre-health 200, invalid/control deserialize 400, positive marker deserialize 200, `/deser-log` marker present, post-health 200, cleanup removed `modern-api-deser-18082`, attacker/victim Internet closed.
- Marker: `DESER_OPERATOR_modern_api_deser_operator_20260523T093300Z` with event type `bounded_pickle_gadget`.
- Classification: verified local-lab unsafe-deserialization bounded marker proof / reusable methodology, not a public-target finding or report-ready bug bounty issue by itself.
- Boundary: local authorized lab only; exactly one bounded marker trigger; no shell, arbitrary command, persistence, callback, credential access, public target, exfiltration, or automatic finding/report promotion.

## 2026-05-23 WebGoat Path Traversal direct file-read retry

Status: attempted-not-verified / useful control evidence
Source: Hermes local-lab run
Date: 2026-05-23
Repo truth: `handoff/webgoat_pathtraversal_file_read_retry_20260523.md`, `<artifact-output-dir>/webgoat_pathtraversal_file_read_20260523T090724Z/`, `handoff/accepted_changes.md`

- Continued testing under the exploration-breadth principle: did not abandon the file-read/path-traversal family just because WebGoat already had upload-write and Zip Slip proofs.
- Ran existing `scripts/labs/webgoat_pathtraversal_file_read_wave1.sh` from `<attacker-vm>` against Docker-backed WebGoat on `<victim-vm>`.
- Result: `attempted-not-verified`; pre-health 200, login 302, lesson/js/control 200, raw traversal 400, encoded traversal 400, `secret_marker_found=no`, post-health 200.
- Project value: useful endpoint rejection/control evidence; no verified direct file-read impact claimed.
- Next possibilities: source-level WebGoat route review, equivalent disposable local marker-read target, or adjacent safe-marker lane.

## 2026-05-23 exploration breadth principle

Status: active workflow preference
Source: User
Date: 2026-05-23
Repo truth: `handoff/current_navigation.md`, `handoff/accepted_changes.md`, Hermes skill `owasp-single-vuln-lab-wave`

Operator preference: do not shrink Cybersec Lab to only the easiest or already-proven lanes. In the authorized recoverable local lab, try every useful proof possibility that can be tested with bounded scope, source/provenance, pre/post health, artifacts, and honest status labeling.

Live-target nuance: do not categorically filter out vulnerability classes just because the best proof needs a live/real target. Local-lab fit is a prioritization signal, not a hard exclusion filter. If a promising candidate cannot be faithfully reproduced locally but could be tested legally, Hermes should keep it as `needs_authorized_live_target` / `blocked-awaiting-scope` and ask the operator for a legal scope package rather than dropping the lane.

Interpretation:

- `Can be tried` does not mean `can be claimed successful`; evidence controls status.
- Useful outcomes include `verified-impact`, `valuable-candidate`, `attempted-not-verified`, `blocked/deferred`, and `reference-only`.
- If the primary path is blocked or unsuitable, preserve breadth by switching route: operator-run script, source-level proof, equivalent disposable target, adjacent safe-marker lane, mature OSS tool wrapper, local target expansion, or an explicit operator request for authorized live target/scope/rules when live proof is genuinely required.
- Safety/process/navigation cleanup should prevent chaos and overclaiming, not prematurely narrow the project.
- Preview should enumerate useful possibilities before prioritizing; it is not a narrowing filter.

## 2026-05-23 operator-run route for repeated execution-layer blockers

Status: active workflow preference
Source: User
Date: 2026-05-23
Repo truth: `handoff/current_navigation.md`, `handoff/accepted_changes.md`, Hermes skill `owasp-single-vuln-lab-wave`

If a local-lab proof hits the same execution-layer blocker pattern (`BLOCKED` / `Do NOT retry`) on a sensitive trigger, Hermes should not keep trying variants through its own terminal/tools. Default next action: write a Kali-side operator-run script/run-card for the user to execute manually, following the first successful SSRF operator path.

Required shape:

- `--precheck-only` mode that verifies route, target health, listener/marker readiness, and artifact directory without sending the sensitive trigger.
- Exact local-lab scope and fixed target URL/IP/port; no public targets or broad scanning.
- Human confirmation gate before the one sensitive trigger.
- One-shot trigger, fixed timeout/request cap, and clear expected evidence.
- Cleanup/post-health checks and artifact pullback path.
- Hermes reviews artifacts afterward and labels the result honestly as verified/candidate/blocked/deferred.

## 2026-05-23 five tactical questions for each proof wave

Status: active methodology
Source: User + Hermes synthesis
Date: 2026-05-23
Repo truth: `handoff/current_navigation.md`, `handoff/accepted_changes.md`, Hermes skill `owasp-single-vuln-lab-wave`

Before each new one-vulnerability proof wave, Hermes preview must answer:

1. What is the maximum safe proof for this vulnerability behavior: callback, marker file write/readback, browser-runtime DOM marker, auth-boundary bypass, server-side identity, or controlled config/data exposure?
2. Can the current target prove that maximum safe proof? If not, do not force it; add/modify a recoverable local target or choose a better local lane.
3. What is the minimum positive/control evidence required? Without meaningful controls, do not label the result `verified-impact`.
4. If the primary trigger is blocked, what two alternate lanes still have learning value: operator-run exact trigger, source-level sink/gadget inventory, adjacent safe-marker lane, or equivalent disposable target?
5. Which proof-library capability does this wave add? If it only adds another log with no reusable evidence pattern, downgrade or choose a better lane.

Intent: expand tactical attack-path thinking while keeping the project script-first, context-driven, local-lab-only, and evidence-first. This is not a new governance gate.

## 2026-05-23 preview/review process test on deserialization lane

Status: process-test passed / vulnerability rerun blocked-deferred / operator-run path prepared
Source: Hermes + Claude Code read-only review
Date: 2026-05-23
Repo truth: `handoff/modern_api_deserialization_preview_review_process_test_20260523.md`, `handoff/claude_review_deser_preview_test_20260523.md`, `handoff/deser_operator_run_card_20260523.md`, `scripts/labs/operator_deser_bounded_marker_run.sh`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`

- Tested the new tactical preview / Claude Code review flow once on the current top lane: dedicated modern_vuln_api unsafe deserialization bounded-marker rerun.
- Flow completed through: OSS/source recon -> Hermes tactical preview -> bounded execution attempt -> blocker record -> Claude Code read-only review -> Hermes synthesis.
- Result: preview/review process worked and stayed tactical/project-value focused, not a new safety gate.
- The runtime deserialization rerun itself is still not verified: execution layer returned `BLOCKED: User denied. Do NOT retry`; Hermes did not retry, encode, disguise, split, or move the trigger.
- Claude Code review recommended separating `process test passed` from `vulnerability rerun blocked/deferred`, and not borrowing the prior broad historical deserialization bundle to claim this dedicated wave succeeded.
- Operator-run path is now prepared: `scripts/labs/operator_deser_bounded_marker_run.sh` with run-card `handoff/deser_operator_run_card_20260523.md`. It has `--precheck-only`, health/control checks, exact human confirmation, one marker-only trigger, `/deser-log` verification, cleanup, and artifact path.

## 2026-05-23 tactical preview / Claude Code review lenses

Status: active process update
Source: User + Hermes synthesis
Date: 2026-05-23
Repo truth: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`, Hermes skill `owasp-single-vuln-lab-wave`

- Added two lightweight tactical perspectives to OWASP single-vulnerability local-lab waves; these are explicitly not new safety gates or governance approvals.
- New flow: `OSS/source reconnaissance -> Hermes tactical preview -> Kali bounded-script execution -> artifact/evidence pullback -> Claude Code read-only review -> Hermes synthesis / verified-impact / bundle / evidence-packet promotion`.
- Rationale: increase tactical visibility and project-value focus without returning to governance-first process.
- Hermes owns preview: challenge planned proof path/tool choice/target surface/artifact value before execution.
- Claude Code owns post-evidence review by default: from a compact read-only packet, challenge proof value and overclaim risk, then recommend verified/candidate/attempted/blocked/reference-only plus stop/rerun/switch/packetize.
- Boundary unchanged: local authorized lab only unless separately scoped; no public target activation, safety-bypass, credential theft, exfiltration, or automatic finding/report promotion. The point is tactical perspective and project value, not more safety process.

## 2026-05-23 SSRF evidence packet consolidation

Status: completed / reusable_methodology / verified-impact lab-only packet
Source: Hermes synthesis
Date: 2026-05-23
Repo truth: `handoff/modern_api_ssrf_true_attacker_callback_evidence_packet_20260523.md`, `handoff/modern_api_ssrf_true_attacker_callback_verified_20260523.md`, `handoff/proof_library_index_20260523.md`

- Converted the verified SSRF true-attacker callback run into the first post-cleanup one-vulnerability evidence packet.
- Packet records target, vulnerability class, authorized scope, route/tool, preconditions, exact trigger path, callback evidence, impact, controls/false-positive boundary, cleanup, rerun gate, and report-readiness.
- Report-readiness decision is `reusable_methodology`: strong local proof, not a real bug bounty/pentest finding.
- Updated active navigation so the next top lane is now dedicated deserialization bounded-marker rerun, followed by second safe-marker file-read/path traversal target and XSS packet hardening.

## 2026-05-23 proof library navigation index

Status: active navigation / proof-pattern index
Source: Hermes synthesis
Date: 2026-05-23
Repo truth: `handoff/proof_library_index_20260523.md`, `handoff/current_navigation.md`, `handoff/vulnerability_test_inventory_20260523.md`

- Added a short proof-library map so future Cybersec Lab work starts from existing verified/candidate proof patterns instead of re-reading the whole handoff pile.
- Current reusable patterns are grouped by evidence type: true attacker callback, browser-runtime XSS, file read/path traversal/XXE safe-marker, auth/session/JWT/access control, injection/server-side execution, upload/exposure triage, and candidate/attempted shelves.
- The index explicitly routes future agents to reuse bundles/scripts/handoffs before creating new scripts, and to keep OSS/tooling reconnaissance mandatory for new script or meaningful bundle optimization.
- Current next best lanes are: evidence packet consolidation/report-readiness rehearsal, dedicated deserialization bounded-marker rerun, and a second file-read/path traversal/XXE safe-marker target.

## 2026-05-23 dedicated XXE safe-marker one-vulnerability proof

Status: completed / verified-impact lab-only
Source: Hermes
Date: 2026-05-23
Repo truth: `handoff/modern_api_xxe_safe_marker_wave1_20260523.md`, `modules/bundles/verified_lab_flow_modern_api_xxe_safe_marker.md`

- Continued testing after the SSRF trigger blocker by switching to a high-value adjacent lane that preserves capability growth without bypassing the execution layer.
- Followed OSS-first policy: saved PayloadsAllTheThings XXE and OWASP XXE Prevention Cheat Sheet references under `setting/local/oss_refs/xxe_safe_marker_20260523/`; one generic nuclei XXE URL fetched only 14 bytes and is check-later.
- Added dedicated runner `scripts/labs/modern_api_xxe_safe_marker_wave1.sh` instead of relying on the older multi-vulnerability `modern_api_wave2_test.sh`.
- Ran from `<attacker-vm>` against Docker-published `modern_vuln_api` on `<victim-vm>` at `<lab-ip>:18081`.
- Verified lab-owned marker expansion: `XXE_SAFE_MARKER_HERMES_LOCAL_LAB`; no-entity and wrong-file controls did not return the marker; pre/post health 200.
- Cleanup completed: removed `modern-api-xxe-18081`; attacker/victim Internet remained closed; artifacts under `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/`.
- Boundary: no `/etc/passwd`, cloud metadata, external callback/OAST, public target, secrets, credential theft, or exfiltration.

## 2026-05-23 SSRF true-attacker callback expansion

Status: completed / verified-impact lab-only / operator-confirmed trigger
Source: Hermes + operator-run Kali script
Date: 2026-05-23
Repo truth: `handoff/modern_api_ssrf_true_attacker_callback_verified_20260523.md`, `handoff/ssrf_operator_run_card_20260523.md`, `modules/bundles/verified_lab_flow_modern_api_ssrf_isolated_callback.md`
Artifacts: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/`

- Continued with the next recommended lane: SSRF attacker-callback adaptation.
- Followed mandatory OSS-first rule: saved PayloadsAllTheThings SSRF and SSRFmap references under `setting/local/oss_refs/ssrf_callback_20260523/`; one attempted nuclei generic SSRF reference fetched only 14 bytes and is check-later.
- Used the newly authorized local-target expansion path: temporary NAT on attacker/victim to pull `python:3-alpine`, then closed/verified Internet closed.
- Created Docker-published attacker listener `<lab-ip>:18183` and Docker-published `modern_vuln_api` target on victim `<lab-ip>:18081`.
- Initial Hermes-side SSRF trigger was denied by the local execution layer. Hermes did not retry/bypass it; instead it created `scripts/labs/operator_ssrf_true_callback_run.sh` with a manual confirmation gate.
- Operator manually confirmed `RUN_SSRF_ON_LOCAL_LAB`; script sent exactly one SSRF trigger to `/fetch?url=attacker-callback`.
- Verified: pre-health 200, trigger status 200, post-health 200, callback marker found, callback source victim IP `<lab-ip>` found, trigger path found; verdict `verified_impact_lab_only`.
- Callback evidence: `callback/requests.jsonl` contains the true trigger callback `client=<lab-ip>`, `path=/ssrf-callback?marker=modern_api_ssrf_operator_20260523T074358Z`, `User-Agent=HermesModernVulnAPI-SSRF-Lab`.
- Cleanup completed: removed attacker listener and victim target containers; attacker Internet remained closed; no public target, metadata endpoint, localhost/internal scan, public OAST, secrets, credentials, exfiltration, or automatic report/finding promotion.

## 2026-05-23 OSS-first / auto local-target expansion policy correction

Status: active workflow policy
Source: User + Hermes
Date: 2026-05-23
Repo truth: `handoff/current_navigation.md`, `handoff/vulnerability_test_inventory_20260523.md`, `handoff/accepted_changes.md`

- Operator clarified that OSS/tooling/source reconnaissance is mandatory every time before new script work, not just optional or occasional.
- Meaningful bundle optimization follows the same rule: first check mature open-source projects/tools/templates/docs and official/training-lab source, then record `adopt`, `wrap`, `adapt`, `reference-only`, or `write-custom` with provenance.
- Operator permits Hermes to automatically open temporary NAT and/or change/add recoverable local靶機 environments when the current target is unsuitable for the desired proof. Examples: install tools, pull vulnerable Docker images, add/modify a local vulnerable service, or adjust VM/container lab state.
- Required guardrails remain: local/recoverable only, document source/provenance, pre-health, artifact path, recovery/rollback, close/verify NAT afterward, post-health, and keep public/unknown targets, malware, stealth/persistence, real credential theft/exfiltration/loot retention, uncontrolled propagation, automatic report submission, and finding promotion out of scope.

## 2026-05-23 WebGoat path traversal / Zip Slip destructive-lab proofs

Status: completed / reusable local-lab proof patterns
Source: Hermes
Date: 2026-05-23
Repo truth: `handoff/vulnerability_test_inventory_20260523.md`, `handoff/webgoat_pathtraversal_upload_write_20260523.md`, `handoff/webgoat_zipslip_overwrite_20260523.md`

- Confirmed current vuln-testing workflow: derive lanes from vulnerability libraries / external intelligence / OSS projects, then validate locally; new scripts and bundles should keep doing OSS/tooling reconnaissance before custom code.
- Operator explicitly permits aggressive/destructive scripts on authorized recoverable local靶機, with recovery/post-health verification. Boundary remains: no public/unknown targets, malware, stealth/persistence, real credential theft/exfiltration, uncontrolled propagation, loot retention, or automatic report submission/finding promotion.
- Added inventory `handoff/vulnerability_test_inventory_20260523.md` summarizing tested vulnerabilities, source lineage, and bundle status.
- Completed WebGoat Path Traversal upload-write proof: `<artifact-output-dir>/webgoat_pathtraversal_upload_write_20260523T033108Z/`, marker-only file write outside per-user upload directory, post-health 200.
- Completed WebGoat Zip Slip profile overwrite proof: `<artifact-output-dir>/webgoat_zipslip_overwrite_20260523T033158Z/`, bounded throwaway profile-image overwrite through zip entry traversal, post-health 200.
- Added runners: `scripts/labs/webgoat_pathtraversal_upload_write_wave1.sh`, `scripts/labs/webgoat_zipslip_overwrite_wave1.sh`, and attempted retrieval runner `scripts/labs/webgoat_pathtraversal_file_read_wave1.sh`.
- Added bundles: `modules/bundles/verified_lab_flow_webgoat_pathtraversal_upload_write.md`, `modules/bundles/verified_lab_flow_webgoat_zipslip_profile_overwrite.md`.
- Next best lane: SSRF attacker-callback adaptation using the DVWA callback evidence packet, or a stricter safe-marker file-read proof on a target that supports lab-owned marker reads cleanly.

## 2026-05-23 WebGoat browser runtime XSS safe-marker proof

Status: completed / reusable local-lab proof pattern
Source: Hermes
Date: 2026-05-23
Repo truth: `handoff/webgoat_browser_runtime_xss_wave1_20260523.md`, `modules/bundles/verified_lab_flow_webgoat_browser_runtime_xss_safe_marker.md`, `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/`

- Completed the next proof wave: WebGoat browser-runtime XSS safe-marker proof from `<attacker-vm>` to Docker-backed WebGoat on `<victim-vm>`.
- Verified marker: `WG_XSS_RUNTIME_webgoat_browser_runtime_xss_20260523T030746Z` appeared as browser runtime DOM state on origin `http://<lab-ip>:8080`, path `/WebGoat/CrossSiteScripting/attack5a`; control request did not set `data-xss`.
- Added reusable runner `scripts/labs/webgoat_browser_runtime_xss_wave1.sh` and minimal CDP helper `scripts/labs/cdp_runtime_xss.py` because Kali Playwright remains broken/missing.
- Artifact packet: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/` with summary, observations, browser_result JSON, positive/control DOM, payload/URLs, and screenshot.
- Boundary: local lab only, throwaway WebGoat session, safe DOM marker mutation; no cookie/token theft, exfiltration, callback/OAST, persistence, shell, destructive write, public target, or finding/report promotion.
- Limitation to remember: WebGoat `/attack5a` returns JSON, so the CDP helper renders the JSON `output` into a same-origin DOM sink for runtime validation. This is a reusable proof-pattern calibration, not a public-target report by itself.
- Current next best lane: file read / path traversal / XXE safe-marker proof packet, unless improving XSS to full lesson-page UI interaction is more valuable first.

## 2026-05-23 DVWA attacker-callback evidence packet standardization

Status: active methodology / completed standardization
Source: Hermes
Date: 2026-05-23
Repo truth: `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md`, `templates/one_vuln_evidence_packet_template.md`, `modules/bundles/verified_lab_flow_dvwa_command_injection_true_attacker_callback.md`

- The DVWA command-injection true attacker-callback proof is now the baseline callback evidence pattern for future SSRF/XXE/deserialization/callback-dependent lanes.
- Standard packet added: `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md`.
- Reusable packet template added: `templates/one_vuln_evidence_packet_template.md`.
- Future reruns should use `<attacker-vm>`; historical artifact labels that say `<attacker-vm>` are old route metadata, not the current default.
- Script hardening: `scripts/labs/dvwa_command_injection_impact_wave1.sh` now supports optional `EXTERNAL_CALLBACK_LOG` so Docker/external listener evidence can be counted in the script summary/observations instead of being orphaned from the runner's local callback path.
- No new exploit rerun was performed: read-only VirtualBox check showed both attacker and victim VMs powered off with NIC2/NAT off.
- Next best proof lane after this standardization: browser runtime XSS proof pattern, unless the operator wants to rerun the DVWA packet after manually/explicitly starting the lab route.

## 2026-05-23 current navigation cleanup

Status: active
Source: User + Hermes
Date: 2026-05-23
Repo truth: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `docs/policy/lab_safety_contract.md`, `handoff/accepted_changes.md`

Current project direction:

- Default route: `<attacker-vm>` as attacker / target-touching VM; `<victim-vm>` as victim/靶機 route.
- Network posture: host-only by default; NAT closed by default and only opened temporarily for installs/pulls/tool recovery, then closed and verified.
- Old `<attacker-vm>` is deprecated/forensic archive only.
- Active local targets: DVWA, WebGoat, Juice Shop, and `labs/modern_vuln_api/modern_vuln_api.py`.
- Current best next lanes:
  1. browser runtime XSS proof pattern;
  2. file read / path traversal / XXE safe-marker proof pattern;
  3. attacker callback proof adaptation using `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md` as the baseline.
- Parked for now: public/real bug bounty activation, contract-first/schema-first/importer-first/report-generator-first work, automatic finding promotion/submission, and broad platform integration before proof packets stabilize.
- Evidence style: one vulnerability behavior/class per wave; prefer one-vuln max-impact proof packets with route/tool, exact evidence, controls, cleanup, project benefit, and new/changed artifacts.
- Memory routing: Hermes global memory remains a compact signpost; repo handoff is engineering truth; this Cybersec Lab note stores strategy/rationale/navigation; raw sensitive evidence, credentials, loot, private scope, exploit dumps, and raw scans stay out of broad memory notes.

## 2026-05-22 workflow / memory routing confirmation

Status: active
Source: User + Hermes
Date: 2026-05-22
Repo truth: `.hermes.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`

Process changes confirmed for future agents:

- Default target-touching attacker route is `<attacker-vm>`; old `<attacker-vm>` is deprecated/forensic archive only.
- Lab infrastructure recovery may use a temporary NAT window only for installs/pulls/tool recovery, then NAT must be closed and verified afterward.
- `<victim-vm>` remains the victim/靶機 lane; attacker/victim separation should be preserved for local proofs.
- Project-specific cybersec workflow state belongs in repo handoff plus this Cybersec Lab Obsidian project note; Hermes global memory should keep only compact cross-project signposts.
- Sensitive material still does not belong in Obsidian: no raw targets, scans, credentials, loot, tokens, hashes, private scope, or exploit evidence dumps.

## 2026-05-21 verified exploit-flow wave 1

Artifact: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/`.

Verified lab flows:

- SQLi login bypass to admin lab JWT, then `/api/Users` read with unauth 401 control.
- Unauthenticated `/rest/admin/application-configuration` configuration read.
- `/ftp/` directory listing plus bounded reads of `legal.md` and `acquisitions.md`.
- Unauthenticated Swagger UI/API docs and Prometheus `/metrics` operational counters.

Attempted-not-verified: JWT alg-none probe, coupon/business logic probe, XSS execution marker, source-map disclosure, missing host tools for ffuf/nikto/nmap/sqlmap.

## 2026-05-22 attacker route migration

Default attacker/target-touching VM is now `<attacker-vm>`.

- Cloned from healthy `kali-linux-2026.1-virtualbox-amd64`.
- Old `<attacker-vm>` is deprecated/forensic archive only because VirtualBox reports a broken snapshot/differencing disk chain.
- New attacker VM config: 4096 MB RAM, 4 CPUs, host-only NIC1 default, NAT NIC2 closed after temporary tool recovery.
- Clean snapshot: `clean-attacker-v2-tools-4096m-4cpu-20260522` (`bcee6035-c86d-41f0-8da1-62b3b42ec388`).
- Attacker IP evidence: `<lab-ip>`; victim remains `<victim-vm>` / `<lab-ip>`.
- Docker/Compose and baseline tools were recovered during operator-approved temporary NAT; no public-target testing was performed during this infrastructure recovery.

## 2026-05-23 WebGoat browser-runtime XSS rerun

Status: active lab result / verified local-lab runtime proof rerun
Source: Hermes + read-only artifact review
Repo truth: `handoff/webgoat_browser_runtime_xss_rerun_20260523.md`, `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/`

Reran the WebGoat XSS safe-marker proof on the current default route (`<attacker-vm>` -> `<victim-vm>`). The proof again produced browser runtime DOM mutation with marker `WG_XSS_RUNTIME_webgoat_browser_runtime_xss_20260523T105506Z`, origin/path labels, negative control with no `data-xss`, pre/post WebGoat health 200, and Internet closed on the attacker route. This confirms the project can currently rerun authenticated browser-runtime XSS evidence, not just static reflection checks. Keep it lab-only/reusable-methodology; no public-target or report-ready claim.

## 2026-05-23 Phase 4 closeout direction

Status: active strategy / estimate
Source: Hermes synthesis
Repo truth: `handoff/phase4_exit_assessment_20260523.md`, `handoff/webgoat_browser_runtime_xss_evidence_packet_20260523.md`

WebGoat browser-runtime XSS packet hardening is now complete, joining SSRF true-attacker callback and DVWA callback packet standards. Phase 4 no longer needs many more vulnerability waves to justify closing. Recommended close condition: final closeout note + active queue update + validation, then move to Phase 5 as report-readiness / authorized-assessment preparation, not automatic public target testing. If one more technical proof is desired before closeout, pick exactly one bounded lane such as auth/session role separation or file-read/deserialization report packetization.
