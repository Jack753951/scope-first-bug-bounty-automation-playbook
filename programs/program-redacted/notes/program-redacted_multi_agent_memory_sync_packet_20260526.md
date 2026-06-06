> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name>-specific multi-agent memory-sync packet — test run

Purpose: test the practical effect of the new multi-agent rule on the current <program-name>/<program-redacted> lane. This is read-only planning/review. Do not touch live targets, browsers, VMs, accounts, network, credentials, tokens, screenshots, or report submission.

Current selected candidate seed: `<program-name>-shared-inbox-object-permission`. It was downgraded to `needs_multi_agent_review`; it must remain passive-only until actual Claude/Cowork + Codex worker outputs and Hermes synthesis exist.

Stop-before list: external channel connection, OAuth/mailbox consent, invites, role changes, API token creation/storage, API requests, workflow save/activation, webhooks/callbacks/OAST/tunnels, scanners/fuzzers/DAST, customer/non-owned data, outbound messages, billing/KYC/support, report submission.

Required worker output format:

## Worker identity
- route: <claude-code | codex>
- tool/runtime: <visible runtime/model/session if available>
- role: <canonical role(s) from config/worker_roles.txt>
- task file: handoff/program-redacted_multi_agent_memory_sync_packet_20260526.md
- output artifact: <artifact path>
- invocation evidence: <command/session/run/output path summary>

## Context read attestation
- checked reads:
  - .hermes.md
  - handoff/current_navigation.md
  - handoff/active_strategy_queue.md
  - handoff/current_artifact_index.md
  - handoff/accepted_changes.md
  - notes/obsidian_projects/Cybersec Lab.md
  - programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md
  - programs/<program-redacted>/scope.json
  - programs/<program-redacted>/lane_state.json
  - docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md
  - config/worker_roles.txt
- missing / not read:
  - none

## Findings
- role-specific findings:
- objections:
- constraints:
- evidence gaps:
- preserved future lanes:

## Validation
- local checks run:
- files changed/reviewed:
- safety boundary checked:

## Verdict
- PASS / REQUEST_CHANGES / BLOCK:
- required next action before <program-name> bounded proof:

## Memory-sync source excerpts

===== .hermes.md =====
1: # Hermes Project Context — Cybersecurity Lab
2:
3: This repository uses a Hermes + Cowork + Codex orchestration workflow,
4: adapted for an offensive / defensive cybersecurity workspace.
5:
6: Project name: **cybersec lab (hacking)**
7: Mounted at:   Windows `<private-workspace>` ↔ Kali `/mnt/hacking` ↔ `~/projects/cybersec`
8:
9: ---
10:
11: ## Roles
12:
13: - **Hermes** — project coordinator, scheduler, memory keeper, task router, security gate.
14:   Implemented as `bin/hermes` (bash) on Linux and `run_hermes_worker.ps1` (PowerShell) on Windows.
15: - **OSS Recon Gate** — workflow policy for comparing new platform contracts/schemas/modules/runners/reports against mature open-source projects and formats before implementation; documented in `docs/policy/oss_recon_gate.md`.
16: - **Review Tiering / Milestone Governance** — workflow policy for assigning T0-T5 review depth, batching related work into milestones, and escalating proxy/pivot/transport or safety-boundary changes; documented in `docs/policy/review_tiering_policy.md`.
17: - **Multi-Party Review Decision Gate** — workflow policy for replacing single third-party approval with role-separated implementation/safety/architecture reviews plus Hermes synthesis; documented in `docs/policy/multi_party_review_decision_policy.md`. Hermes has direct authority for low-risk offline slices, conditional authority for aligned T3 offline work, and escalation-only authority for T4/T5 activation.
18: - **Claude/Cowork** — strategy, learning plans, documentation cleanup, research synthesis,
19:   threat modeling, report drafting, independent review, and third-party architecture guidance.
20:   Reviews should not only look for blocking defects; they should also assess whether changes
21:   improve extensibility, updateability, modularity, safety gates, testing, and agent-assisted
22:   analysis toward the operator's long-term platform goals. For new contracts, schemas,
23:   module/runner/reporting boundaries, or external-tool integrations, Claude/Cowork should
24:   run the design-only OSS Recon Gate in `docs/policy/oss_recon_gate.md`: compare relevant
25:   open-source projects/formats, choose adopt/adapt/ignore decisions, and avoid copying
26:   unsafe target-touching defaults. Driven by Claude Code CLI (`claude`) or the Cowork desktop app.
27: - **Codex** — surgical fallback, small deterministic fixes, secondary engineering review, script safety, validation, tests, automation.
28:   Driven by OpenAI Codex CLI (`codex`).
29: - **Claude Code Impl** — default implementation worker for offline/local coding slices that should visibly consume Claude Code MAX/OAuth usage and emit usage JSON.
30:   Driven by Claude Code CLI (`claude`) through `hermes claude-impl`; Hermes remains verifier and safety gate.
31:
32: ---
33:
34: ## Security Gate (binding)
35:
36: Before any active scan, exploit, brute force, callback, or target-touching automation,
37: Hermes must confirm one of:
38:
39: - local lab or intentionally vulnerable app
40: - CTF / training platform (HackTheBox, TryHackMe, PortSwigger Labs)
41: - user-owned asset
42: - written client authorization
43: - explicit bug bounty scope
44:
45: The whitelist lives in `config/scope.txt`. `recon.sh` enforces this automatically through the mandatory `safe_target` runtime guard: every host or URL must pass syntax validation and scope matching before any probe, scan, fuzz, nuclei, or notification stage consumes it. Domain-expansion output from subfinder/crt.sh is revalidated and out-of-scope results are dropped with audit reasons.
46:
47: Phase 1 will add per-program scope files at `programs/<program-slug>/scope.json`; once present, bug bounty automation must require both `config/scope.txt` and the active program scope/rules to allow the target and technique. If either source is missing, ambiguous, or disallows automation, Hermes routes the task to clarification, not execution.
48:
49: **Do not create:** stealth persistence, credential theft tooling, malware,
50: destructive actions, evasion of legitimate controls, unauthorized access workflows.
51:
52: Scanner output is **triage only**. Confirmed findings require manual verification,
53: evidence, impact analysis, remediation, and retest steps before they enter `reports/`.
54:
55: ---
56:
57: ## Current Project Assets
58:
59: | Asset | Path | Owner |
60: |---|---|---|
61: | Env bootstrap | `setup_kali_env.sh` | Hermes |
62: | Recon pipeline | `recon.sh` | Cowork (spec) + Codex (impl) |
63: | Recon config | `config/recon.conf` | Codex |
64: | Authorization whitelist | `config/scope.txt` | **Operator only** |
65: | Hermes CLI (Linux) | `bin/hermes` | Hermes |
66: | Orchestration template | `agent_orchestration_template/` | Hermes |
67: | Scan outputs | `scans/<target>_<ts>/` | runtime |
68: | Audit logs | `logs/audit.log`, `logs/hermes_audit.log` | runtime |
69: | Loot (sensitive) | `loot/` | runtime — never commit |
70: | Reports | `reports/` | Cowork (template) + Codex (generator) |
71: | CVE archive | `cves/` | Cowork (curator) + Codex (fetcher) |
72: | Notes | `notes/` | Cowork |
73: | Memory / strategy routing | `docs/policy/memory_and_strategy_routing.md` | Hermes |
74: | Active strategy queue | `handoff/active_strategy_queue.md` | Hermes |
75:
76: ---
77:
78: ## Collaboration Contract
79:
80: 1. **Operator** writes intent → `hermes new-task cowork "topic"` creates `handoff/cowork_task.md`.
113: HERMES_IMPL_WORKER=codex hermes pipeline  # explicit Codex fallback chain
114: ```
115:
116: ### Windows path (PowerShell) — preferred for docs / research on host
117:
118: ```powershell
119: powershell -NoProfile -ExecutionPolicy Bypass -File .\run_hermes_worker.ps1 -Doctor
120: powershell -NoProfile -ExecutionPolicy Bypass -File .\run_hermes_worker.ps1 -Worker cowork
121: powershell -NoProfile -ExecutionPolicy Bypass -File .\run_codex_review.ps1
122: powershell -NoProfile -ExecutionPolicy Bypass -File .\run_hermes_worker.ps1 -Worker codex
123: ```
124:
125: Both surfaces share `handoff/` and `.hermes.md`. Tasks can hop between OS freely.
126:
127: ### Worker invocation reference
128:
129: | Worker | CLI call (used internally) |
130: |---|---|
131: | Cowork | `claude -p "<context+required-context-reads+task>" --max-turns 10 --allowedTools "Read,Edit,Write,Grep,Glob"` |
132: | Claude Impl | `claude -p "<context+required-context-reads+task+safety_footer>" --output-format json --max-turns ${CLAUDE_IMPL_MAX_TURNS:-25} --allowedTools "Read,Edit,Write,Bash,Grep,Glob"` |
133: | Codex fallback | `codex exec --sandbox workspace-write --output-last-message <out> -` |
134:
135: All workers receive **this `.hermes.md` as prefix context** before the task body, plus a required-context-read block instructing them to read the current route/strategy/artifact entrypoints when present:
136: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/current_artifact_index.md`, `notes/obsidian_projects/Cybersec Lab.md`, and recent `handoff/accepted_changes.md` entries. Worker outputs must include `Worker identity`, checked `Context read attestation`, `Validation`, and `Verdict` sections; `scripts/check-worker-attestation.py` enforces this in `hermes review` and after worker runs. When `config/worker_roles.txt` exists, the `role:` field must use its canonical hyphenated vocabulary or `other:<reason>`. This gives workers stable long-term goal context without dumping the whole Obsidian vault into every prompt.
137:
138: ---
139:
140: ## Routing Rules
141:
142: - Vague goal / study plan / docs cleanup → **Cowork first**, then Codex if edits needed.
143: - Concrete code / script / template change → **Codex first**.
144: - Non-trivial platform work → classify with `docs/policy/review_tiering_policy.md` before routing; T3+ requires milestone framing and T4/T5 require strict safety/runtime review.
145: - Current CVE / advisory / weekly review → Hermes gathers primary sources, Cowork synthesizes,
146:   Codex automates archival into `cves/`.
147: - Live incident / suspected compromise → preserve evidence, write IR case note,
148:   do not clean up until evidence handling is decided.
149: - Active target testing → **scope verification before any payload**.
150:
151: ---
152:
153: ## Safety Rules (binding for all agents)
154:
155: 1. **Authorization first.** Never run active scans/exploits against any target absent from
156:    `config/scope.txt`. `--skip-scope-check` requires operator approval and audits.
157: 2. **No exfiltration.** Never transmit `loot/`, `.env`, credentials, hashes, tokens, or
158:    proprietary wordlists outside the local machine. Webhooks send summaries only.
159: 3. **No destructive defaults.** `recon.sh` defaults to `normal` intensity, which excludes
160:    `dos,intrusive,fuzz` nuclei tags. `--full` requires conscious opt-in.
161: 4. **No silent overwrites.** Codex modifying existing files MUST log diff summary to
162:    `handoff/accepted_changes.md`.
163: 5. **Lock discipline.** Long-running worker tasks must respect `.agent.lock`.
164: 6. **Secrets out of git.** `.gitignore` excludes `loot/`, `logs/`, `*.pcap`, `*.cap`,
165:    `*.kdbx`, `*.key`, `*.pem`, `creds*`. Do not weaken.
166: 7. **Report integrity.** Generated reports under `reports/` may be reset.
167:    `accepted_changes.md` is **append-only** — never truncate.
168: 8. **No production-side changes** without explicit operator approval (deployment, billing,
169:    scheduler, publish).
170:
171: ---
172:
173: ## Validation Expectations
174:
175: Before any worker reports "done":
176:
177: - `hermes review` passes (JSON valid, Python compiles, `bash -n` clean on every `.sh`)
178: - `.agent.lock` released
179: - `handoff/codex_review.md` contains concrete findings (not boilerplate)
180: - If a shell script changed → dry-run executed at least once
181: - If `recon.sh` or scope logic changed → unauthorized target rejected in test
182:
183: ---
184:
185: ## Recommended Cadence
186:
187: - **Daily** — record what was studied/tested/changed in `notes/daily/YYYY-MM-DD.md`.
188: - **Milestone / direction boundary** — update `handoff/active_strategy_queue.md` with the active lane, next candidate slices, deferred lanes, and operator-approval locks.
189: - **Periodic / deep review** — include freshness metadata plus memory drift, handoff drift, goal drift, and structure drift checks using `docs/policy/memory_and_strategy_routing.md`.
190: - **Weekly** — refresh `cves/weekly_<YYYYWW>.md` from NVD + CISA KEV.
191: - **Per lab session** — update target inventory in `notes/labs.md`.
192: - **Per script change** — update `accepted_changes.md`, add dry-run example.

===== handoff/current_navigation.md =====
1: # Cybersec Lab Current Navigation
2:
3: Status: active
4: Source: User + Hermes navigation cleanup
5: Date: 2026-05-25
6: Repo truth: `.hermes.md`, `handoff/accepted_changes.md`, `handoff/active_strategy_queue.md`, `handoff/current_artifact_index.md`, `docs/policy/live_bounty_autonomous_workflow_policy_20260525.md`, `handoff/live_bounty_lane_queue.json`, `docs/policy/lab_safety_contract.md`, `notes/obsidian_projects/Cybersec Lab.md`
7:
8: ## Purpose
9:
10: This is the short entry map for the Cybersec Lab. It should answer, in under 10 minutes, which route is current, which lab targets are active, which vulnerability lanes are worth doing next, where artifacts go, and which lanes are intentionally parked.
11:
12: This cleanup is navigation-only. It does not authorize public target testing, new scanning, exploitation, VM network changes, scheduler changes, report submission, credential handling, or publication of findings.
13:
14: Bug bounty autonomy policy: `docs/policy/live_bounty_autonomous_workflow_policy_20260525.md` is now the project-level operating policy for live bounty autonomy. Hermes should own safe authorized steps and checkpoint only at lane/target completion or true operator gates, while still fail-closing on scope ambiguity, sensitive actions, stronger techniques, or report submission.
15:
16: Live-bounty automation substrate: `schemas/live_bounty_lane_state.schema.json`, `schemas/live_bounty_evidence.schema.json`, `handoff/live_bounty_lane_queue.json`, `scripts/live-bounty-lane-status.py`, `scripts/live-bounty-lane-runner.py`, `scripts/live-bounty-preview-grounding.py`, and `scripts/evidence-redaction-check.py` now provide machine-readable lane state, evidence summaries, queue validation, status summaries, local-only queue runner decisions, reference-grounded preview packets, and local evidence redaction checks. This engineering substrate is sealed at `handoff/live_bounty_automation_substrate_closeout_20260525.md`; do not add more local-only tooling by default before resolving the next operator gate. Current implementation handoff: `handoff/live_bounty_automation_engineering_slice_20260525.md`.
17:
18: ## Worker context entrypoints
19:
20: `bin/hermes` now injects a required-context-read block into Cowork, Claude Impl, and Codex prompts. Workers should read these entrypoints when present before planning/editing/reviewing:
21:
22: ```text
23: handoff/current_navigation.md
24: handoff/active_strategy_queue.md
25: handoff/current_artifact_index.md
26: handoff/accepted_changes.md (recent entries / append-only history)
27: notes/obsidian_projects/Cybersec Lab.md
28: docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md (when planning live-bounty lanes)
29: ```
30:
31: This preserves current-stage and long-term goal context without dumping the whole Obsidian vault into every worker prompt. For live-bounty planning, workers should use the bridge to map local proof patterns to live prerequisites before proposing target-touching work.
32:
33: ## Current phase entry
34:
35: Current Phase 5A is active: authorized-assessment readiness, one-shot vulnerability-intelligence intake, cautious live-bounty bridge work, and high-hit-rate live investigation selection. The first-flow practice goal is satisfied by <program-redacted>; new live work should start with A0 passive OSINT/program scoring, tactical preview that expands options before narrowing, then one selected bounded lane with A/B or tenant controls. Operator correction on 2026-05-26: the platform should not exclude tactics merely because realistic attackers use dangerous methods; instead it should model full attack paths, compile them into bounded proof surrogates, and stop before harm/data access/destructive impact. Current platform-direction artifact: `docs/policy/tactical_freedom_platform_direction_20260526.md`. Current high-hit-rate planning artifacts: `docs/strategy/live_bounty/live_bounty_high_hit_rate_target_filter_20260526.md`, `docs/strategy/live_bounty/live_bounty_attack_class_matrix_20260526.md`, `docs/strategy/live_bounty/next_live_bounty_shortlist_20260526.md`, `docs/strategy/live_bounty/live_bounty_tactical_preview_template_20260526.md`, `docs/strategy/live_bounty/live_bounty_no_finding_feedback_log.md`, `docs/strategy/live_bounty/live_bounty_account_ab_operator_action_card_20260526.md`, and `programs/<program-redacted>/notes/program-redacted_target_selection_preview_20260526.md`. `<program-redacted>` / <program-name> is the selected third target. Scope is confirmed from logged-in <bug-bounty-platform> CSV; `programs/<program-redacted>/scope.json`, `programs/<program-redacted>/lane_state.json`, and selected global scope entries already exist. Current checkpoint is `programs/<program-redacted>/notes/program-redacted_pre_contact_ready_checkpoint_20260526.md`: Kali/noVNC is locally reachable; latest continuation opened the official app sign-in -> <program-name> signup path and is blocked at the visible signup identity/phone gate. Hermes must stop at phone/OTP/CAPTCHA/password/email/payment/policy gates.
36:
37: <program-redacted> Taiwan <bug-bounty-platform> status: a minimal program scope artifact now exists at `programs/<program-slug>/scope.json`, selected assets are present in `config/scope.txt`, and the first pre-second-phone single-account surface/auth boundary check is complete in `programs/<program-slug>/notes/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md`. Result: no reportable vulnerability; no owned object ID suitable for IDOR/BOLA proof; Account B or program-provided test accounts remain required for cross-account ownership testing. Use `docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md` before any next live-target step.
38:
39: Live automation gate status: `gate_fixed_dry_run_verified` for the previously observed compatibility blockers, with additional fail-closed hardening coverage. Focused regressions now verify `--program <program-slug> --policy-mode dry-run` accepts exact in-scope <program-redacted> dry-runs, global scope validation accepts intentional `localhost`, `example.org` remains rejected, malformed/path-like slugs fail before target processing, `--skip-scope-check` cannot combine with program policy, `--policy-mode dry-run` requires `--dry-run`, and `--policy-mode` without `--program` is rejected. This is still only dry-run readiness; live scanner-like automation remains blocked unless a separate narrow operator-approved plan confirms exact <bug-bounty-platform> rules/scope/technique.
40:
41: Thanks-only/VDP first-complete-flow lane: <program-redacted> VDP policy intake, operator <bug-bounty-platform>-alias signup/login gate, and first noVNC owned-account auth/session/profile/workspace empty-state surface map are complete. Artifacts: `programs/<program-slug>/scope.json`, `programs/<program-slug>/lane_state.json`, `handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_surface_map_20260525.json`, `programs/<program-slug>/notes/tines_automation_vdp_owned_account_surface_map_20260525.md`, and `programs/<program-slug>/notes/tines_automation_vdp_phase5a_dry_run_packet_20260525.md`. `login.<program-redacted>.com` remains the only <program-redacted> entry in `config/scope.txt`; the generated owned workspace subdomain was treated as browser-only post-login continuation and was not promoted to scanner/script scope. Result: `NO_FINDING_CLOSEOUT` / `no_finding` with evidence status `surface_only`; runner decision is `lane_closed_or_parked` / exit `0`. Scanners/fuzzers/DAST, workflow execution, run-script, callbacks, integrations, cross-tenant testing, non-owned data, setting mutation, API-key/credential creation, and report submission remain blocked. Any next <program-redacted> lane requires a separately approved plan.
42:
43: Arcane local-bootstrap prep status: `handoff/arcane_global_variables_precheck_posture_20260525.md` records a fail-closed precheck from the Windows control plane (`docker CLI missing`). Arcane setup/proof remains blocked until a disposable victim-lab Docker daemon/proxy posture is confirmed.
44:
45: Phase 4 is effectively closed unless the operator identifies a concrete missing ability gap. The next default work is not more local lab vulnerability quantity; it is bridge/live-prerequisite conversion, authorization-gate hardening, scope/package readiness, report-readiness conversion, and metadata-only vulnerability-intelligence routing.
46:
47: Current Phase 5A anchors:
48:
49: ```text
50: handoff/live_bounty_lane_queue.json
51: scripts/live-bounty-lane-runner.py
52: scripts/live-bounty-preview-grounding.py
53: handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md
54: handoff/live_bounty_automation_substrate_closeout_20260525.md
55: programs/<program-slug>/notes/tines_automation_vdp_owned_account_surface_map_20260525.md
56: handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_surface_map_20260525.json
57: schemas/live_bounty_lane_state.schema.json
58: schemas/live_bounty_evidence.schema.json
59: handoff/phase5a_authorized_live_target_dry_run_template.md
60: handoff/phase5a_report_readiness_checklist.md
61: docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md
62: tools/vuln_intel_refresh.py
63: handoff/vuln_intel/vuln_intel_candidates_20260523T130000Z.md
64: ```
65:
66: ## Current default route
67:
68: - Repo root on Windows host: `<private-workspace>`.
69: - Preferred VM-side project mount: Kali `/mnt/hacking` / `~/projects/cybersec` when available.
70: - Default attacker / target-touching VM: `<attacker-vm>`.
71: - Deprecated attacker VM: old registered `<attacker-vm>`; treat as forensic archive only because of broken snapshot / differencing disk state.
72: - Victim / vulnerable-target VM: `<victim-vm>`.
73: - Known host-only IP evidence from latest handoff:
74:   - attacker: `<lab-ip>`
75:   - victim: `<lab-ip>`
76: - Default network posture: host-only.
77: - NAT posture: closed by default. Operator permits Hermes to open a temporary NAT window without asking again when needed to download/install/update tooling, pull vulnerable-target images, or make a better local靶機 environment; close NAT and verify Internet is closed before target-touching proof execution unless the proof specifically needs a documented temporary install window.
78: - Current clean attacker snapshot: `clean-attacker-v2-tools-4096m-4cpu-20260522` (`bcee6035-c86d-41f0-8da1-62b3b42ec388`).
79: - Attacker baseline resources: 4096 MB RAM, 4 CPUs, Docker / Compose / baseline tools available per `handoff/accepted_changes.md`.
80:
143: - WebGoat browser-runtime XSS evidence packet: `handoff/webgoat_browser_runtime_xss_evidence_packet_20260523.md`.
144:
145: ## Tactical preview / Claude Code review lenses
146:
147: Current one-vulnerability wave sequence includes two lightweight tactical perspectives, not new safety gates:
148:
149: ```text
150: OSS/source reconnaissance
151: -> Hermes tactical preview
152: -> Kali bounded-script execution
153: -> artifact/evidence pullback
156: ```
157:
158: - Hermes owns preview before target-touching execution. Preview should broaden tactical options, compare tool/wrapper/custom runner choices, identify weak proof/value/artifact gaps, and choose the highest-project-value local-lab path without prematurely eliminating viable lanes. Preview must enumerate useful possibilities before prioritizing; it is not a narrowing filter.
159: - Each wave preview must answer these five tactical questions before execution:
160:   1. What is the maximum safe proof for this vulnerability behavior: callback, marker file write/readback, browser-runtime DOM marker, auth-boundary bypass, server-side identity, or controlled config/data exposure?
161:   2. Can the current target prove that maximum safe proof? If not, do not force it; add/modify a recoverable local target or choose a better local lane.
164:   5. Which proof-library capability does this wave add? If it only adds another log with no reusable evidence pattern, downgrade or choose a better lane.
165: - Claude Code owns post-evidence review by default, using a compact read-only evidence packet. Review should challenge proof value and overclaim risk, classify status, and recommend stop/rerun/switch/packetize.
166: - Neither preview nor review should become a new safety process, approval layer, or governance-first gate. Existing scope/recovery boundaries remain, but the purpose here is tactical perspective and project value.
167: - Do not default to multiple reviewers. Escalate only when the operator explicitly asks or when Hermes needs specialist perspective for an unusually ambiguous local-lab lane.
168:
228:   3. switch to an equivalent local靶機/lane that avoids the blocked pattern while preserving the same learning objective;
229:   4. record the blocker and continue with adjacent proof capability instead of stalling the project.
230: - For high-value lanes likely to trigger safety filters — SSRF callback, XXE external entity callback, deserialization gadget behavior, command injection callbacks, internal callback proof — prepare the run-card/operator route up <program-name> instead of discovering the block late.
231: - Operator preference: when the same execution-layer blocker pattern appears, do not keep trying variants through Hermes. Instead, create a Kali-side operator-run script/run-card like the first successful SSRF operator path: precheck-only mode, exact local-lab scope, artifact directory, cleanup/post-health, and a human confirmation gate before the single sensitive trigger. Hermes may then review/pull back artifacts after the operator runs it.
232:
224: - Treat this as an execution-layer limitation, not as a project capability dead-end.
225: - Preserve project capability growth by choosing one explicit route:
226:   1. convert the blocked step into a reviewed operator-run run-card with exact command, scope, expected artifact, rollback, and verification so the human operator can run it manually in the authorized lab if desired;
227:   2. redesign the proof as a source-level unit/integration test inside the disposable target when that still proves the vulnerability behavior truthfully;
233: ## Artifact location convention
234:
235: Default artifact root:
236:
237: ```text
238: <artifact-output-dir>/<lane_name>_<YYYYMMDDTHHMMSSZ>/
239: ```
240:
241: Each meaningful proof wave should preserve:
242:
243: - `README.md` or `summary.md` with target, route, vulnerability class, proof narrative, boundaries, and cleanup.
244: - command transcript or exact rerun commands.
245: - request/response summaries or tool output.
246: - callback logs, browser evidence, marker file evidence, or session evidence when relevant.
247: - pre-health and post-health result.
248: - limitations / false-positive controls.
249: - report-readiness decision: `local_learning`, `reusable_methodology`, `candidate_needs_manual_review`, or `report_ready_lab_only`.
250:
251: Promote only stable, reusable workflows to:
252:
253: ```text
254: modules/bundles/<bundle_name>.md
255: scripts/SCRIPT_INVENTORY.md
256: ```
257:
258: ## Evidence packet minimum shape
259:
260: For each one-vulnerability proof wave, record:
261:
262: ```text
263: Target:
264: Vulnerability class:
265: Authorized scope:
266: Route/tool:
267: Preconditions:
268: Exploit/probe path:
269: Evidence:
270: Impact:
271: Controls / false-positive boundary:
272: Cleanup:
273: Rerun commands:
274: Report-readiness:
275: Project benefit:
276: New/changed artifacts:
277: ```
278:
279: ## Memory and Obsidian routing
280:
281: - Hermes global memory: compact cross-project signposts only.
282: - Repo handoff: engineering truth, validation, active lane, safety boundaries, accepted changes.
283: - Obsidian `Projects/Cybersec Lab/`: strategy, rationale, methodology, navigation synthesis.
284: - `session_search`: recall only; verify against repo or Obsidian before treating it as current.
285: - Do not store raw sensitive targets, scans, credentials, loot, tokens, hashes, private scope/rules, or exploit evidence dumps in global memory or broad Obsidian notes.
286:
287: ## Next safe slice
288:
289: Recommended next implementation/research sequence:
290:
291: 1. Use this navigation cleanup as the current map.
292: 2. DVWA attacker-callback proof packet standardization is complete; use `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md` as the callback baseline.
293: 3. Browser-runtime XSS proof packet is now complete for WebGoat; path traversal upload-write and Zip Slip are also verified for WebGoat.
294: 4. Next best lane: Phase 5A authorized-assessment readiness. Use `handoff/phase5a_authorized_live_target_dry_run_template.md`, `handoff/phase5a_report_readiness_checklist.md`, and `tools/vuln_intel_refresh.py`; do not touch live targets without an operator-provided legal scope package.
295:
296: ## Freshness rule
297:
298: When this file conflicts with a frozen review or older handoff:
299:
300: 1. Current explicit operator instruction wins.
301: 2. Live repo/config/tool state wins for facts that can be verified.
302: 3. `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `docs/policy/lab_safety_contract.md`, and `handoff/accepted_changes.md` are the current navigation layer.
303: 4. Older handoff and archived queues remain rationale/history, not current navigation.

===== handoff/active_strategy_queue.md =====
1: # Active Strategy Queue
2:
3: Status: active
4: Source: Hermes navigation cleanup after operator direction
5: Date: 2026-05-23
6: Repo truth: `handoff/current_navigation.md`, `docs/policy/lab_safety_contract.md`, `docs/policy/live_bounty_autonomous_workflow_policy_20260525.md`, `handoff/accepted_changes.md`, `.hermes.md`, `notes/obsidian_projects/Cybersec Lab.md`
7: Autonomy note: for authorized bug bounty lanes, Hermes should act as project owner for safe non-sensitive steps and checkpoint at lane/target completion or true operator gates.
8: Archived previous queue: `handoff/archive/active_strategy_queue_pre_navigation_cleanup_20260523.md`
9:
10: ## Purpose
11:
12: This file is the compact current-navigation layer for Cybersec Lab. It should stay short. Detailed history belongs in named handoff artifacts, `handoff/accepted_changes.md`, `<artifact-output-dir>/`, `modules/bundles/`, and Obsidian strategy notes.
13:
14: ## Long-term goal
15:
16: Build a legal, recoverable, scope-aware, script-first security research platform that can produce high-value bug bounty / pentest proof packets from authorized contexts.
17:
18: The current emphasis is:
19:
20: ```text
21: script-first + context-driven bundles + one-vulnerability max-impact proofs
22: ```
23:
24: Automation remains a project goal, but it should grow from proven local proof patterns, not from contract/schema/governance-first scaffolding.
25:
26: ## Current phase
27:
28: Phase 5A is active: authorized-assessment readiness, one-shot vulnerability-intelligence intake, cautious live-bounty bridge work, and high-hit-rate live investigation selection.
29:
30: - Phase 4 is effectively closed unless the operator identifies a concrete missing ability gap.
31: - Do not add more local lab vulnerability waves by default; reuse existing proof patterns.
32: - Current Phase 5A work has shifted from first-flow practice toward high-hit-rate live investigation: A0 passive OSINT/program scoring, one selected bug class, A/B or tenant controls, timeboxed A2 viability, and A3 bounded proof only when exact policy/scope and owned controls exist.
33: - New high-hit-rate artifacts: `docs/strategy/live_bounty/live_bounty_high_hit_rate_target_filter_20260526.md`, `docs/strategy/live_bounty/live_bounty_attack_class_matrix_20260526.md`, and `docs/strategy/live_bounty/next_live_bounty_shortlist_20260526.md`.
34: - New tactical-freedom/learning-loop artifacts: `docs/strategy/live_bounty/live_bounty_tactical_preview_template_20260526.md`, `docs/strategy/live_bounty/live_bounty_no_finding_feedback_log.md`, `docs/strategy/live_bounty/live_bounty_account_ab_operator_action_card_20260526.md`, and `docs/policy/tactical_freedom_platform_direction_20260526.md`. Use the preview template to expand tactical options before narrowing; use the feedback log after every no-finding/surface-only/blocked lane; use the operator card for Account B / tenant B / object visibility gates without collecting secrets. Latest operator direction: do not exclude tactics merely because realistic attackers use dangerous methods; model full attack paths, compile bounded proof surrogates, and stop before unauthorized access, non-owned data contact, destructive impact, DDoS/resource exhaustion, credential theft, malware, stealth/persistence/evasion, or report submission.
35: - Multi-agent memory/workflow hardening now has an enforcing local contract: `scripts/check-worker-attestation.py`, `config/worker_roles.txt`, `templates/role_packet_base.md`, `tests/test_worker_context_attestation.sh`, and `tests/test_worker_roles_vocabulary.sh`. Cowork/Claude and Codex wrapper runs must output checked context read attestations, canonical roles, validation, and verdicts; `hermes review` enforces present artifacts. The local review gate is now fail-closed for invalid JSON (with Python fallback when `jq` is unavailable), Python compile failures, shell syntax failures, active `.agent.lock`, and missing/unavailable worker attestation checks; regression: `tests/test_hermes_review_fail_closed.sh`. Operator correction on 2026-05-26: for attacker-flow/non-trivial live-bounty lanes, role separation must actually invoke suitable independent agents (Claude Code/Cowork for tactical/boundary/evidence roles and Codex for deterministic/skeptical review) or explicitly record the skipped/unavailable route and remain passive-only. Workers must receive the memory-sync context packet, not just a single MD file. Repo truth: `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md`. This is workflow hardening only and does not authorize target-touching work.
36: - Agent capability substrate v1 is implemented and Codex-reviewed: `schemas/attack_path_role_synthesis.schema.json`, `schemas/kali_readiness_state.schema.json`, `schemas/no_finding_learning_seed.schema.json`, `scripts/attack-path-role-synthesize.py`, `scripts/kali-readiness-state.py`, `scripts/no-finding-learning-seed.py`, and `tests/test_agent_capability_substrate.sh`. These add local-only role-conflict synthesis, Kali readiness state, and no-finding learning seed helpers; target-like flags fail closed, readiness is not authorization, and learning seeds are not evidence promotion. Third-target <program-name> contact is formally opened within confirmed in-scope assets: `programs/<program-redacted>/scope.json`, `programs/<program-redacted>/lane_state.json`, `programs/<program-redacted>/notes/program-redacted_first_contact_scope_and_signup_gate_20260526.md`, and `programs/<program-redacted>/notes/program-redacted_pre_contact_ready_checkpoint_20260526.md`; current state is `READY_FOR_OPERATOR_GATE` / `A2_PENDING_OPERATOR_AUTH` at the signup identity/phone gate, with local noVNC reachable and the latest continuation showing the official <program-name> signup form in the Kali browser.
37: - Recommended next target candidate: `<program-redacted>` / <program-name>, selected from Kali passive <bug-bounty-platform> policy/program-metadata intake and recorded in `programs/<program-redacted>/notes/program-redacted_target_selection_preview_20260526.md`. Logged-in <bug-bounty-platform> Scope CSV confirmed in-scope assets on 2026-05-26: `<in-scope-host>`, `<in-scope-host>`, mobile app IDs, and Mac/Windows executables. Only `<in-scope-host>` and `<in-scope-host>` were added to `config/scope.txt`; `<program-domain>` remains out-of-scope except as the official signup page reached from the in-scope app sign-in flow. Current live state: `https://<in-scope-host>/signin` first contact completed, `Try for Free` revealed `https://<program-domain>/signup` form with email/name/company/job/industry/phone/company-size fields; Hermes stopped for operator signup/phone/identity input.
38: - <program-redacted> Taiwan current status: minimal program scope exists at `programs/<program-slug>/scope.json`; selected assets are present in `config/scope.txt`; pre-second-phone single-account surface/auth boundary check is complete in `programs/<program-slug>/notes/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md`; result is no finding / `needs_second_account` for IDOR/BOLA.
39: - Before any next live-target action, read `docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md` and classify the lane as `surface_only`, `needs_second_account`, `blocked_state_change`, `blocked_sensitive_flow`, `candidate`, or `report_ready`.
40: - Live automation gate compatibility is fixed and regression-covered for dry-run readiness: `tests/test_recon_gate.sh` verifies `<program-slug>` program dry-run accepts exact in-scope <program-redacted> target, intentional `localhost` scope entries no longer poison validation, `example.org` remains rejected, malformed/path-like slugs fail before target processing, `--skip-scope-check` cannot combine with program policy, policy dry-run requires `--dry-run`, and `--policy-mode` without `--program` is rejected. This does not authorize live scanner-like automation without a separate operator-approved plan.
41: - Vulnerability intelligence should not exclude classes that need live/real targets. If a promising lane cannot be faithfully proven locally, keep it as `needs_authorized_live_target` and ask the operator for legal target/scope/rules instead of silently dropping it.
42: - Full periodic scheduling comes later only after the one-shot MVP stays compact and useful.
43:
44: ## Current default route
45:
46: - Work repo: `<private-workspace>`.
47: - Default attacker VM: `<attacker-vm>`.
48: - Deprecated attacker VM: old registered `<attacker-vm>`; forensic archive only.
49: - Victim/target VM: `<victim-vm>`.
50: - Default network: host-only.
51: - NAT: closed by default; temporary installs/pulls only, then close and verify.
52: - Clean attacker snapshot: `clean-attacker-v2-tools-4096m-4cpu-20260522` (`bcee6035-c86d-41f0-8da1-62b3b42ec388`).
53:
54: See `handoff/current_navigation.md` and `docs/policy/lab_safety_contract.md` for the full operational map.
55:
56: ## Active local lab targets
57:
58: 1. DVWA
59:    - Best for command injection, marker write/readback, attacker callback proof baseline.
60: 2. WebGoat
61:    - Best for authenticated/session handling, JWT, IDOR/access control, path traversal, XSS lessons.
62: 3. Juice Shop
63:    - Best for SQLi behavior, file listing/read metadata, upload validation, auth/access boundary, XSS calibration.
64: 4. `labs/modern_vuln_api/modern_vuln_api.py`
65:    - Best for source-controlled SSRF, XXE safe-marker, browser-runtime XSS, deserialization marker, upload retrieval, IDOR, and auth/session role separation.
66:
67: ## Top active lanes
68:
69: 1. Proof-library → live-bounty bridge, post-proof consolidation, authorization-gate dry-run health, and lane-state automation substrate
70:    - Current status: bridge exists at `docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md`; lightweight consolidation checklist exists at `scripts/post-proof-consolidation.sh`; authorization-gate compatibility blockers are fixed and regression-covered; machine-readable lane/evidence schemas, queue, status helper, redaction checker, local-only queue runner, and reference-grounding generator now exist; the engineering substrate is sealed at `handoff/live_bounty_automation_substrate_closeout_20260525.md`.
71:    - New automation artifacts: `schemas/live_bounty_lane_state.schema.json`, `schemas/live_bounty_evidence.schema.json`, `handoff/live_bounty_lane_queue.json`, `scripts/live-bounty-lane-status.py`, `scripts/live-bounty-lane-runner.py`, `scripts/live-bounty-preview-grounding.py`, `scripts/evidence-redaction-check.py`, `tests/test_live_bounty_state_and_redaction.sh`, `tests/test_live_bounty_lane_runner.sh`, `tests/test_live_bounty_preview_grounding.sh`, `handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md`, `handoff/live_bounty_automation_engineering_slice_20260525.md`, `handoff/live_bounty_automation_substrate_closeout_20260525.md`.
72:    - Purpose: map verified local proof patterns to live-bounty prerequisites, blocked states, minimum live evidence, report-readiness thresholds, public methodology references, and make each target/lane resumable and learnable through structured state/evidence plus runner exit codes before wrap-up.
73:    - Next engineering slice: none by default. Do not add approval-heavy safety process, extra schema/governance, or more local-only tooling unless explicitly requested or a focused test fails. Next value is the operator identity/session gate followed by noVNC owned-account surface mapping; dry-run pass, runner exit `0`, or grounding output is not permission for live scanner automation.
74:
75: 2. <program-redacted> Taiwan pre-second-phone single-account lane
76:    - Current status: low-speed logged-in Kali/noVNC observation complete; no finding; `needs_second_account` for IDOR/BOLA.
77:    - Artifacts: `programs/<program-slug>/notes/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md`, `programs/<program-slug>/notes/coupang_tw_single_account_surface_map_20260525.md`, `programs/<program-slug>/scope.json`.
78:    - Next live step only after Account B/program guidance: build an Account A/B object-ownership matrix from normally visible owned objects. Before then, do not manufacture state or touch support/recovery/payment/KYC/upload/seller/admin.
79:
80: 3. Thanks-only / VDP first complete-flow lane
116: ## Wave process update
117:
118: One-vulnerability local-lab waves now include lightweight tactical perspectives, not new safety gates:
119:
120: ```text
121: OSS/source reconnaissance -> Hermes tactical preview -> Kali bounded-script execution -> artifact/evidence pullback -> Claude Code read-only review -> Hermes synthesis / verified-impact/bundle/evidence-packet promotion
122: ```
123:
124: - Hermes preview increases tactical sight before execution: proof path, tool choice, project value, artifact plan, and alternative local target surface.
125: - Claude Code review challenges evidence and value before overclaiming: status classification, missing evidence, false-positive controls, and whether to stop/rerun/switch/packetize.
126: - Keep this lightweight; do not turn it into governance-first blocking, approval workflow, or extra safety process.
153: Not authorized by this queue:
154:
155: - Continuing <program-name> beyond the visible signup identity/phone gate until the operator fills the form locally in Kali/noVNC and reports a non-sensitive status such as `front_signup_complete`, `blocked_phone`, `blocked_email_verification`, `blocked_captcha`, `blocked_payment`, `blocked_policy`, or `stop`. Current noVNC checkpoint: `programs/<program-redacted>/notes/program-redacted_pre_contact_ready_checkpoint_20260526.md`; latest screenshot pointer: `setting/local/screenshots/program-redacted_live_20260526/signup_gate.png`.
156: - Additional public/real targets unless the operator supplies an explicit legal scope package for that lane.
157: - <program-redacted> live automation/scanner-like/scripted runners until `gate_fail_closed_needs_fix` is resolved and dry-runs prove in-scope pass / out-of-scope fail.
127:
128: ## Secondary lanes
129:
130: - Auth/session handling: throwaway users, cookies/tokens, re-auth, role separation, replay controls. Current ability-gap proof is complete in `handoff/modern_api_auth_role_separation_wave1_20260523.md`; reuse it instead of adding more lab variants by default.
131: - Evidence packet / report-readiness gate: turn one strong local proof into a reusable packet.
132: - Source-driven script/tool selection: inspect context/source, choose a small tool chain, modularize only after value is proven.
133: - Vulnerability-intelligence refresh + target bootstrap: Phase 5 work. Produce candidates from current sources, try local/recoverable target setup where faithful, and route valuable live-target-dependent candidates to an operator scope request rather than filtering them out.
134:
135: ## Parked or deprecated lanes
136:
137: - Public or real bug bounty target testing without a user-provided legal scope package.
138: - Live/real target candidates are not deprecated solely because they need a live target; hold them as `needs_authorized_live_target` until the operator provides target/scope/rules or declines the lane.
139: - Contract-first / schema-first / importer-first / report-generator-first work.
140: - Large governance/validator expansion that does not improve local proof quality.
141: - Automatic finding confirmation, automatic report submission, scheduler/CI target-touching automation.
142: - Old `<attacker-vm>` route except forensic/reference use.
143:
144: ## Current hard boundary
145:
146: Allowed now:
147:
148: - Read-only navigation cleanup.
149: - Documentation/handoff/Obsidian routing updates.
150: - Local/offline agent capability substrate work: role synthesis, Kali readiness state, no-finding learning seeds, and validation.
151: - Local lab proof waves only after explicit instruction and scope/route confirmation.
152:
158: - <program-redacted> Account A/B object-ownership testing until Account B is operator-owned/program-provided and the lane is classified through `docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md`.
159: - Scope/config changes that authorize live targets without explicit operator-provided target/scope/rules.
160: - Credential theft, real exfiltration, malware, stealth/persistence/evasion, uncontrolled propagation.
161: - External callbacks/OAST/tunnels/pivots/public listeners without explicit approval.
162: - Automatic confirmed/reportable finding promotion or submission.
163: - VM network/snapshot changes unless explicitly requested for lab recovery/install needs.
164:
165: ## Artifact convention
166:
167: Default proof artifact root:
168:
169: ```text
170: <artifact-output-dir>/<lane_name>_<YYYYMMDDTHHMMSSZ>/
171: ```
172:
173: Each one-vulnerability proof should include:
174:
175: - target / route / vulnerability class;
176: - authorization boundary;
177: - proof narrative and exact commands;
178: - evidence and controls;
179: - pre/post health;
180: - cleanup/recovery notes;
181: - limitations;
182: - project benefit and new/changed artifacts;
183: - report-readiness status.
184:
185: ## Current navigation files
186:
187: - Main map: `handoff/current_navigation.md`.
188: - Artifact cleanup/index map: `handoff/current_artifact_index.md`.
189: - Safety contract: `docs/policy/lab_safety_contract.md`.
190: - Accepted history: `handoff/accepted_changes.md`.
191: - Obsidian strategy/navigation: `notes/obsidian_projects/Cybersec Lab.md`.
192: - Archived pre-cleanup long queue: `handoff/archive/active_strategy_queue_pre_navigation_cleanup_20260523.md`.
193:
194: ## Freshness rule
195:
196: 1. Current explicit operator instruction wins.
197: 2. Live repo/config/tool state wins for verifiable facts.
198: 3. `handoff/current_navigation.md`, `handoff/current_artifact_index.md`, this queue, `docs/policy/lab_safety_contract.md`, and `handoff/accepted_changes.md` are current navigation.
199: 4. Frozen reviews and archived queues are history/rationale, not current routing.

===== handoff/current_artifact_index.md =====
1: # Current Artifact Index — Cybersec Lab
2:
3: Status: active cleanup/navigation index
4: Source: Hermes repo-noise cleanup pass
5: Date: 2026-05-26
6: Repo truth: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`, `.gitignore`
7:
8: ## Purpose
9:
10: This file reduces handoff sprawl by classifying the current working artifacts. It is not a replacement for `current_navigation.md`; it is the cleanup map that tells future workers which files are current, reference-only, superseded, machine state, local-only, or ignored.
11:
12: Boundary: navigation/file-hygiene only. This index does not authorize target-touching actions, scope changes, account creation, scanning, fuzzing, exploit execution, callbacks/OAST/tunnels, credential handling, report submission, or deletion of evidence.
13:
14: ## Status classes
15:
16: - `active-entrypoint`: must-read or current route artifact.
17: - `active-engineering`: current code/schema/test/template substrate for the next hardening slice.
18: - `active-lane-state`: machine-readable lane/evidence state used by helpers.
19: - `active-strategy-reference`: current strategy/reference docs used for planning.
20: - `target-lane-reference`: target/lane-specific record; read only when that target/lane is in scope.
21: - `local-evidence-reference`: redacted/promoted evidence in repo handoff; do not delete casually.
22: - `historical-reference`: useful history, not default current context.
23: - `cleanup-record`: file-hygiene inventory/audit artifact.
24: - `ignored-local`: local cache/raw output/quarantine/log/evidence ignored by git.
25: - `operator-owned`: user/scope-controlled; never auto-clean.
26:
27: ## Must-read current entrypoints
28:
29: | Status | Path | Notes |
30: |---|---|---|
31: | active-entrypoint | `.hermes.md` | Project contract and safety gate. |
32: | active-entrypoint | `handoff/current_navigation.md` | Primary route map; should stay compact. |
33: | active-entrypoint | `handoff/active_strategy_queue.md` | Compact active priorities and next lanes. |
34: | active-entrypoint | `handoff/current_artifact_index.md` | This cleanup/navigation index. |
35: | active-entrypoint | `handoff/accepted_changes.md` | Append/prepend accepted change log; already large, keep future entries compact. |
36: | active-entrypoint | `notes/obsidian_projects/Cybersec Lab.md` | Long-term strategy/rationale bridge. |
37:
38: ## Operator-owned / never auto-clean
39:
40: | Status | Path | Notes |
41: |---|---|---|
42: | operator-owned | `config/worker_roles.txt` | Canonical worker role vocabulary for multi-agent artifacts; local workflow contract only, no target-touching authority. |
43: | operator-owned | `config/scope.txt` | Authorization whitelist. Modified in current working tree; review manually, never reset/delete automatically. |
44: | operator-owned | `loot/` | Sensitive runtime output; ignored. Do not inspect/delete without explicit operator direction. |
45: | operator-owned | `.env`, keys, tokens, browser profiles | Ignored by policy. Treat as sensitive/local. |
46:
47: ## Current engineering substrate for next hardening
48:
49: | Status | Path | Notes |
50: |---|---|---|
51: | active-engineering | `schemas/live_bounty_lane_state.schema.json` | Lane-state contract. |
52: | active-engineering | `schemas/live_bounty_evidence.schema.json` | Evidence contract. |
53: | active-engineering | `schemas/attack_path_candidate.schema.json` | Tactical attack-path candidate contract. |
54: | active-engineering | `schemas/attack_path_role_synthesis.schema.json` | Role-conflict synthesis contract for bounded-lane / blocked-preserve decisions. |
55: | active-engineering | `schemas/kali_readiness_state.schema.json` | Kali/noVNC readiness state contract; readiness is not authorization. |
56: | active-engineering | `schemas/no_finding_learning_seed.schema.json` | No-finding/surface-only learning seed contract. |
57: | active-engineering | `scripts/live-bounty-lane-status.py` | Local lane/evidence summary helper. |
58: | active-engineering | `scripts/live-bounty-lane-runner.py` | Local-only queue runner; no target touching. |
59: | active-engineering | `scripts/live-bounty-preview-grounding.py` | Local-only reference grounding generator. |
60: | active-engineering | `scripts/live-bounty-preview-synthesize.py` | Local-only attack-path preview synthesizer. |
61: | active-engineering | `scripts/attack-path-role-synthesize.py` | Local-only role-conflict synthesizer; rejects target-like args. |
62: | active-engineering | `scripts/kali-readiness-state.py` | Local-only Kali readiness state seed/validate/summarize helper; no VM/network actions. |
63: | active-engineering | `scripts/no-finding-learning-seed.py` | Local-only no-finding/surface-only learning seed helper. |
64: | active-engineering | `scripts/check-worker-attestation.py` | Static worker artifact checker; validates worker identity, checked context read attestation, validation, verdict, and canonical role vocabulary when configured. |
65: | active-engineering | `scripts/evidence-redaction-check.py` | Evidence redaction check. |
66: | active-engineering | `scripts/post-proof-consolidation.sh` | Post-proof handoff checklist helper. |
67: | active-engineering | `templates/role_packet_base.md` | Base template for canonical role artifacts under the worker attestation contract. |
68: | active-engineering | `templates/live_bounty_attack_path_candidate_packet.md` | Attack-path packet template. |
69: | active-engineering | `tests/test_live_bounty_state_and_redaction.sh` | Focused regression. |
70: | active-engineering | `tests/test_live_bounty_lane_runner.sh` | Focused regression. |
71: | active-engineering | `tests/test_live_bounty_preview_grounding.sh` | Focused regression. |
72: | active-engineering | `tests/test_live_bounty_preview_synthesize.sh` | Focused regression. |
73: | active-engineering | `tests/test_agent_capability_substrate.sh` | Agent capability substrate regression for role synthesis, Kali readiness state, and no-finding learning seeds. |
74: | active-engineering | `tests/test_worker_context_attestation.sh` | Worker artifact contract regression for memory sync and role-separated collaboration. |
75: | active-engineering | `tests/test_worker_roles_vocabulary.sh` | Canonical role vocabulary / role coverage regression. |
76: | active-engineering | `tests/test_hermes_review_fail_closed.sh` | Hermes local review fail-closed regression for JSON, Python, shell, lock, and worker-attestation checker failures. |
77: | active-engineering | `tests/test_recon_gate.sh` | Authorization/dry-run gate regression. |
78: | active-engineering | `tests/test_post_proof_consolidation.sh` | Handoff checklist regression. |
79:
80: ## Current machine-readable lane / evidence state
87: | active-lane-state | `handoff/live_bounty_learning_seeds.jsonl` | Line-delimited no-finding/surface-only learning seeds for target/lane selection. |
88: | active-lane-state | `handoff/tines_surface_learning_seed_20260526.json` | <program-redacted> surface-only no-finding learning seed source artifact. |
89: | active-lane-state | `handoff/third_target_contact_checkpoint_20260526.json` | Third-target checkpoint: <program-name> scope/contact lane opened; currently blocked at operator signup/phone/identity gate. |
90: | active-lane-state | `programs/<program-redacted>/notes/program-redacted_first_contact_scope_and_signup_gate_20260526.md` | <program-name> confirmed-scope + first-contact signup gate packet. |
91: | active-lane-state | `programs/<program-redacted>/notes/program-redacted_pre_contact_ready_checkpoint_20260526.md` | Current readiness checkpoint: Kali/noVNC reachable, latest continuation shows <program-name> signup gate, operator gate remains blocking. |
92: | active-lane-state | `handoff/program-redacted_pre_contact_verification_summary_20260526.md` | Verification summary: focused tests, hermes review, diff check, local noVNC HTTP check, and independent subagent review passed. |
93: | active-lane-state | `handoff/restart_checkpoint_20260526_front_signup_phone_gate.md` | Restart checkpoint for <program-name> signup phone gate after non-secret fields were prefilled. |
94: | active-lane-state | `programs/<program-redacted>/scope.json` | <program-name> logged-in <bug-bounty-platform> scope converted to program scope. |
95: | active-lane-state | `programs/<program-redacted>/lane_state.json` | <program-name> A2 lane state; current status blocked_operator_action. |
96: | active-lane-state | `programs/<program-slug>/scope.json` | <program-redacted> program policy/scope artifact. |
97: | active-lane-state | `programs/<program-slug>/lane_state.json` | <program-redacted> lane state; currently no-finding/closed. |
111: | active-strategy-reference | `docs/strategy/live_bounty/live_bounty_attack_class_matrix_20260526.md` | Attack class selection matrix. |
112: | active-strategy-reference | `docs/strategy/live_bounty/next_live_bounty_shortlist_20260526.md` | Candidate shortlist; passive only. |
113: | active-strategy-reference | `docs/strategy/live_bounty/live_bounty_tactical_preview_template_20260526.md` | Current tactical preview template. |
114: | active-strategy-reference | `docs/strategy/live_bounty/live_bounty_no_finding_feedback_log.md` | Converts no-finding into learning/selection updates. |
115: | active-strategy-reference | `docs/strategy/live_bounty/live_bounty_account_ab_operator_action_card_20260526.md` | Account B / tenant B operator gate card. |
116: | active-strategy-reference | `docs/policy/tactical_freedom_platform_direction_20260526.md` | Current direction: preserve full attack paths; compile bounded proof surrogates. |
117: | active-strategy-reference | `docs/strategy/platform/multi_agent_bug_hunting_operating_model_20260526.md` | Multi-agent operating model. |
118: | active-strategy-reference | `docs/strategy/platform/multi_agent_bug_hunting_engineering_plan_20260526.md` | Engineering backlog; next hardening should start here. |
119: | active-strategy-reference | `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md` | Hard rule: non-trivial attacker-flow role separation must actually invoke suitable Claude/Codex-style workers or record passive-only exception; workers receive memory-sync context. |
120: | cleanup-record | `handoff/redundant_file_inventory_20260526.md` | Repo-noise inventory and first cleanup pass. |
121: | cleanup-record | `handoff/dirty_tree_checkpoint_audit_20260526.md` | Current dirty-tree classification for <program-name> pre-contact readiness checkpoint. |
122:
123: ## Target / lane-specific references
127: | Status | Path | Notes |
128: |---|---|---|
129: | target-lane-reference | `programs/<program-redacted>/notes/program-redacted_target_selection_preview_20260526.md` | Third target selection preview; scope now confirmed and lane is at operator signup/auth gate. |
130: | target-lane-reference | `programs/<program-slug>/notes/tines_automation_vdp_phase5a_dry_run_packet_20260525.md` | <program-redacted> first-lane dry-run packet. |
131: | target-lane-reference | `programs/<program-slug>/notes/tines_automation_vdp_owned_account_surface_map_20260525.md` | <program-redacted> no-finding owned-account surface map. |
137: | historical-reference | `handoff/restart_checkpoint_20260525_hackerone_coupang_guidance.md` | Restart checkpoint. |
138: | historical-reference | `handoff/restart_checkpoint_20260526_tines_closeout_validation_followup.md` | Restart checkpoint. |
139: | historical-reference | `handoff/tactical_risk_rebalance_20260526.md` | Directional record; current direction is in tactical freedom artifact and active queue. |
140: | historical-reference | `handoff/bundle_freshness_automation_plan_20260526.md` | Planning reference; not default next lane unless explicitly reopened. |
141:
172:
173: ```text
174: third-target <program-name> signup/auth operator gate
175: ```
176:
177: Expected focus:
178: - operator completes the visible <program-name> signup form locally in Kali/noVNC using H1 alias and operator-owned phone only if comfortable;
179: - Hermes resumes only after a non-sensitive status such as `front_signup_complete`, `blocked_phone`, `blocked_email_verification`, `blocked_captcha`, `blocked_payment`, `blocked_policy`, or `stop`;
180: - after successful auth, Hermes performs browser-only owned-account surface mapping and stops before invites/API-token/customer-data/integration/callback/report actions;
181: - keep `programs/<program-redacted>/lane_state.json` as the machine-readable state pointer.
102: ## Current strategy / planning references
103:
104: | Status | Path | Notes |
105: |---|---|---|
106: | active-strategy-reference | `docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md` | Required before next live-target step. |
107: | active-strategy-reference | `docs/policy/live_bounty_autonomous_workflow_policy_20260525.md` | Operating policy for authorized bounty lanes. |
108: | active-strategy-reference | `handoff/live_bounty_automation_engineering_slice_20260525.md` | Implementation slice reference. |
109: | active-strategy-reference | `handoff/live_bounty_automation_substrate_closeout_20260525.md` | Closeout: substrate sealed unless reopened deliberately. |
110: | active-strategy-reference | `docs/strategy/live_bounty/live_bounty_high_hit_rate_target_filter_20260526.md` | High-hit-rate target selection criteria. |
124:
125: Read these only when working on the named target/lane.
126:
132: | target-lane-reference | `handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md` | <program-redacted> grounding packet. |
133: | target-lane-reference | `programs/<program-slug>/notes/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md` | <program-redacted> boundary result; needs second account. |
134: | target-lane-reference | `programs/<program-slug>/notes/coupang_tw_single_account_surface_map_20260525.md` | <program-redacted> single-account surface map. |
135: | target-lane-reference | `handoff/account_b_phone_gate_status_20260526.md` | Account/phone gate status. |
136: | historical-reference | `handoff/thanks_only_vdp_shortlist_20260525.md` | Earlier VDP shortlist; superseded by higher-hit-rate process but still useful history. |
142: ## Ignored local / quarantine / bulky evidence
143:
144: These are intentionally not part of normal git status. Do not delete automatically.
145:
146: | Status | Path | Notes |
147: |---|---|---|
148: | ignored-local | `setting/local/` | Machine/browser/tool/cache/quarantine. May contain sensitive local browser state. |
149: | ignored-local | `setting/local/quarantine/cve_brief_20260526_unverified_do_not_use.{json,md}` | Unverified CVE/current-intel draft moved from repo root. Fresh primary-source verification required before use. |
150: | ignored-local | `<artifact-output-dir>/` | Local lab run outputs/provenance. Archive whole runs instead of piecemeal deletion. |
151: | ignored-local | `logs/` | Runtime/audit logs. |
152: | ignored-local | `scans/` | Runtime scan outputs. |
153: | ignored-local | `handoff/worker_logs/` | Worker raw logs; ignored. |
154: | ignored-local | `handoff/tmp/` | Future handoff scratch/debug output; ignored. |
155: | historical-reference | `cves/unverified/2026-05-22_websearch_fallback_unverified.md` | Moved from root `cve_brief_20260522.md`; unverified web-search fallback. Fresh primary-source verification required before use. |
156: | historical-reference | `cves/unverified/2026-05-23_websearch_fallback_unverified.md` | Moved from root `cve_brief_20260523.md`; unverified web-search fallback. Fresh primary-source verification required before use. |
157: | ignored-local | root `cve_brief_*.{json,md}` | Now ignored for future accidental root drafts; move verified content to `cves/` or handoff, keep unverified drafts in quarantine/unverified. |
158: | ignored-local | root `UsersOwnerAppDataLocalTemp*.json` | Temp-path leak artifacts; now ignored if recurrence happens. |
159: | ignored-local | `handoff/*_stdout_check.json` | One-run stdout/debug checks; now ignored. |
160:
161: ## Superseded / archived conventions
162:
163: - Keep active docs discoverable through `current_navigation.md`, `active_strategy_queue.md`, and this index.
164: - Keep dated handoff docs as references unless a later explicit cleanup pass marks them safe to archive.
165: - For old rolling files, prefer `handoff/archive/rolling/` if the wrapper created it.
166: - For large local outputs, compress/archive entire run directories outside the repo rather than deleting individual evidence files.
167: - Never auto-delete `config/scope.txt`, `loot/`, browser profiles, credentials, raw evidence, or reports that may be needed for provenance.
168:
169: ## Next hardening slice now unblocked
170:
171: The repo is clean enough to proceed with engineering hardening if `./bin/hermes review` passes. Recommended next slice:

===== handoff/accepted_changes.md =====
## 2026-05-21 Phase 4B lab fast-lane and GET-only adapter

- Added host-only Juice Shop lab fast-lane policy at `handoff/phase4b_lab_fast_lane_policy_20260521.md`, reducing pre-execution overhead for bounded Tier 1/Tier 2 local-lab probes while preserving hard stops for public targets, callbacks, brute force, scanner broad runs, credentials, destructive behavior, and finding promotion.
- Added reusable GET-only local-lab adapter `scripts/lab_modules/phase4b_get_only_metadata_probe.py` plus TDD coverage in `scripts/test_phase4b_get_only_metadata_probe.py`.
- Executed the adapter via the Kali bridge against `http://<lab-ip>:3000/`; artifacts were pulled to `<artifact-output-dir>/phase4b_fast_lane_20260521T053646Z/`.
- Recorded result in `handoff/phase4b_fast_lane_get_only_result_20260521.md`; health remained `pre_health=200`, `post_health=200`, `requests_sent=8`.
- Notable candidate-only observations: `/ftp/` directory listing metadata, `/api-docs/` Swagger UI metadata, SPA fallback false-positive control, and negative open-redirect canary.

## 2026-05-21 Phase 4B Wave2 benign parameter adapter

- Added reusable Wave2 benign parameter fast-lane adapter `scripts/lab_modules/wave2_benign_params.py` plus TDD coverage in `scripts/test_wave2_benign_params.py`.
- Adapter uses fixed GET-only inert canaries for reflection/open-redirect calibration; it rejects public targets, avoids redirect following, executable payloads, crawlers/scanners, callbacks, credentials, brute force, and finding promotion.
- Executed the adapter via the Kali bridge against host-only Juice Shop; artifacts were pulled to `<artifact-output-dir>/phase4b_wave2_benign_20260521T054852Z/`.
- Recorded result in `handoff/phase4b_wave2_benign_params_result_20260521.md`; health remained `pre_health=200`, `post_health=200`, `requests_sent=5`.
- Candidate-only outcome: no XSS/reflection candidate and no open-redirect candidate for the fixed inert canaries; SPA fallback and redirect error-body echo were captured as false-positive controls.

## 2026-05-21 Phase 4B script-first architecture reset

- Accepted operator correction that the desired workflow is script-first and context-driven: preview/recon results -> choose module bundle -> if no module fits, use script library -> execute a small situational script combination -> review -> modularize useful combinations -> repeat -> report.
- Added `handoff/phase4b_script_first_architecture_reset_20260521.md` as the direction reset.
- Added `scripts/SCRIPT_INVENTORY.md` as the operator-facing map of practical shell scripts, lab adapters, generated local scripts, and current bundle candidates.
- Added `modules/bundles/README.md` and `modules/bundles/lab_directory_listing_triage.md` to shift modules toward reusable context-specific script combinations instead of contract-first manifests as the main workflow.
- Updated `handoff/active_strategy_queue.md` and Obsidian project index to make the next slice `lab_directory_listing_triage` with a bounded `ftp_filename_content_class_verifier.py`, not more generic safety scaffolding.
- Boundary preserved: this direction reset does not authorize public/real bug-bounty target activation, broad scanner runs, credentials/brute force, callback/OAST, destructive behavior, loot/secret collection, confirmed-finding auto-promotion, or report submission.

## 2026-05-21 Restart checkpoint before Hermes reopen

- Added `handoff/restart_checkpoint_20260521_hermes_reopen.md` as the current resume point before restarting Hermes.
- Checkpoint preserves the Phase 4B script-first/context-driven reset, keeps multi-agent collaboration as support/review/implementation, and points the next slice to the `/ftp/` directory-listing triage bundle.
- Added matching Obsidian checkpoint note under `Projects/Cybersec Lab/00_Index/Restart Checkpoint Hermes Reopen 2026-05-21.md`.

## 2026-05-21 Phase 4B module/bundle distinction accepted

- Accepted the operator direction to keep `module` and `bundle` as related but distinct layers: `script/tool -> bundle -> module`.
- Added `handoff/module_bundle_distinction_direction_20260521.md` to record that bundles are the default Phase 4B operator-facing tactical workflow, while modules are platform-facing stable capabilities for schema/policy/runner/report integration.
- Direction: start local-learning work from scripts/tools and lightweight bundles; promote to `modules/checks/**/module.json` only after behavior/output/candidate-only semantics are stable or when authorized-assessment/platform integration requires it.
- Preserved boundary: no public target activation, credential theft, exfiltration, malware, stealth persistence, automatic finding confirmation, or report submission is authorized by this distinction.

## 2026-05-21 Phase 4B service baseline scanner targets

- Added `scripts/lab_modules/lab_service_baseline_targets.py`, a bundle-first local-lab adapter for Apache, Tomcat, OpenSSL/TLS, HAProxy, Envoy, and Traefik baseline probes.
- Added focused TDD coverage in `scripts/test_service_baseline_targets.py`; RED first failed because the adapter did not exist, then GREEN passed after implementation.
- Added bundle documentation at `modules/bundles/lab_service_baseline_targets.md` and updated `scripts/SCRIPT_INVENTORY.md` with the adapter, generated runner path, and bundle workflow.
- Boundary: plan-only by default, rejects public targets, requires `--lab-approved` to generate a runner, uses bounded path/TLS metadata probes, and keeps all output candidate-only with no credential attempts, brute force, secret retention, automatic finding confirmation, or report submission.
- Actual local-lab run added `handoff/service_baseline_targets_run_20260521.md` and artifacts under `<artifact-output-dir>/phase4b_service_baseline_targets_20260521T135015Z/`; final runner exit code was 0 after fixing generated-runner quoting/Python-shim bugs.
- Runtime corrections: quote generated service paths such as `'/;csv'`, use `python -` instead of `python3` for Git-Bash/Windows heredoc compatibility, preserve embedded Python newlines with a raw f-string template, suppress generic SPA/root fallback false positives with body-hash comparison, and avoid treating OpenSSL `Cipher is (NONE)`/no-peer-certificate output as a TLS candidate.
- Final candidate-only run summary: only `/metrics` remained as a Traefik-labeled service-baseline candidate; Apache/Tomcat/HAProxy/default path 200s were reclassified as generic root fallback controls; OpenSSL/TLS on the HTTP port was a control; nmap was unavailable in the Windows Git-Bash runtime.

## 2026-05-21 Phase 4B three OWASP exposure bundles

- Added shared bounded web exposure generator `scripts/lab_modules/web_exposure_common.py` plus three adapters: `lab_api_docs_exposure_triage.py`, `lab_metrics_exposure_triage.py`, and `lab_source_map_disclosure_triage.py`.
- Added focused RED/GREEN coverage in `scripts/test_phase4b_three_exposure_bundles.py`: adapters are plan-only by default, reject public targets fail-closed, record mature OSS tool decisions, generate candidate-only runners, and use `python -` in rendered bash.
- Added bundle docs at `modules/bundles/lab_api_docs_exposure_triage.md`, `modules/bundles/lab_metrics_exposure_triage.md`, and `modules/bundles/lab_source_map_disclosure_triage.md`; updated `scripts/SCRIPT_INVENTORY.md` with adapters and generated runners.
- Mature OSS references recorded: OWASP ZAP, nuclei, ffuf, dirsearch, Prometheus/promtool, Retire.js, SecretFinder, trufflehog, and LinkFinder; decision is wrap/reference mature tools but start with fixed GET-only local-lab probes.
- Actual local-lab artifacts saved under `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/` and summarized in `handoff/phase4b_three_exposure_bundles_run_20260521.md`.
- Candidate-only results: `/api-docs` and `/api-docs/` exposed Swagger UI markers; `/metrics` exposed Prometheus-style metrics markers; source-map disclosure produced no candidate after root-fallback filtering. All require manual verification before finding/report language.

## 2026-05-22 Phase 4B OWASP/CVE continuation bundles

- Completed the delayed Phase 4B local-lab continuation immediately against only `http://<lab-ip>:3000/`; run id `phase4b_owasp_cve_continuation_20260521T232928Z`, artifacts under `<artifact-output-dir>/phase4b_owasp_cve_continuation_20260521T232928Z/`.
- Added bounded plan-first adapters: `lab_auth_surface_no_bruteforce.py`, `lab_component_metadata_triage.py`, and `lab_integrity_metadata_triage.py`; each rejects public targets, is plan-only unless `--lab-approved`, generates candidate-only bash runners, and uses fixed GET-only paths.
- Added bundle docs for auth/no-bruteforce, component metadata, integrity metadata, and API-docs/metrics manual verification/logging checklist. Updated `scripts/SCRIPT_INVENTORY.md` and the OWASP 2017/2021/2025 tracker so A06/A07/A08/A09/2025 supply-chain/auth/logging rows no longer show as entirely unmapped.
- Candidate-only run results: auth surface candidate at `/rest/admin/application-configuration`; component/version clue at `/rest/admin/application-version`; integrity metadata candidates at `/.well-known/security.txt`, `/security.txt`, and `/robots.txt`; package-manifest/service-worker/static paths mostly root/SPA fallback controls; `/api/Users` returned 401 access-control observed.
- Added focused tests by extending `scripts/test_phase4b_three_exposure_bundles.py`; validation passed focused tests, py_compile, `bash -n` for generated runners, all three runner executions, post-health HTTP 200, and `HACKLAB=$(pwd) ./bin/hermes review`.
- Boundary: no public targets, no credential attempts/brute force, no callbacks/OAST, no exploit payloads, no recursion/crawling, no destructive actions, no raw secret/loot retention, no CVE claim from version strings, and no confirmed/reportable finding promotion.



## 2026-05-21 — Verified exploit-flow rerun wave 1

- Scope/target: authorized local lab `http://<lab-ip>:3000/`, covered by `<lab-ip>/16` in `config/scope.txt`; pre/post health HTTP 200.
- Artifacts: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/`.
- Added verified-lab-flow bundles: SQLi auth-bypass + `/api/Users` read, unauth admin config read, `/ftp/` listing/file read, API docs + metrics exposure.
- Added attempted-not-verified record for JWT alg-none oracle, coupon route 401, XSS execution not browser-verified, source-map fallback, headers/CORS/component/integrity metadata-only, and missing host tools for ffuf/nikto/nmap/sqlmap.
- Updated script inventory, OWASP tracker, active strategy queue, daily note, and Obsidian-style project note/index.

- 2026-05-25: Fixed the local `bin/hermes` wrapper root-default footgun before live-target intake. `bin/hermes` now defaults `HACKLAB` to the repository that owns the wrapper (`$(dirname ${BASH_SOURCE[0]})/..`) instead of `$HOME/projects/cybersec`, while preserving explicit `HACKLAB=...` overrides. Validation: `bash -n bin/hermes` and bare `./bin/hermes doctor` now report project root `<private-workspace>` with `.hermes.md` and `handoff/` found. Boundary: wrapper path-resolution fix only; no target, scope, credential, VM/network, scanner, exploit, scheduler, or worker-task activation.

- 2026-05-25: Converted the public <program-redacted> Taiwan <bug-bounty-platform> policy/scope into a blocked Phase 5A scope package without touching the target. Added `programs/<program-slug>/scope.json` with the 47 observed in-scope eligible assets, policy exclusions, conservative manual-only rate defaults, and required `X-<bug-bounty-platform>-Researcher: <researcher-alias>` session header. Added `programs/<program-slug>/notes/coupang_tw_phase5a_dry_run_packet_20260525.md` selecting an account-owned access-control/IDOR first lane and documenting the account-creation decision gate. Boundary: no live request, signup, login, scan, fuzz, exploit, callback/OAST, upload, payment/KYC/checkout/cash action, report submission, or `config/scope.txt` authorization change. Next gate: operator must choose whether to create two owned test accounts or explicitly authorize Hermes to attempt official signup with operator-handled CAPTCHA/OTP/email/phone verification.

- 2026-05-25: Recorded operator authorization for Hermes to attempt creating two <program-redacted> Taiwan throwaway accounts through the official in-scope signup flow, with the operator handling CAPTCHA/email/OTP/phone verification. Added the minimal signup/auth assets to `config/scope.txt`: `www.tw.<program-redacted>.com`, `tw.<program-redacted>.com`, `member.tw.<program-redacted>.com`, and `id.tw.<program-redacted>.com`; updated `programs/<program-slug>/notes/coupang_tw_phase5a_dry_run_packet_20260525.md` status and checklist. Boundary: authorization is limited to official signup/account creation and later low-speed manual/browser-assisted owned-account checks; no scan, fuzz, exploit, callback/OAST, payment/KYC/checkout/cash flow, upload test, report submission, or non-owned account/data interaction. Remaining blocker: operator must provide two owned email aliases/addresses for Account A/B before Hermes starts signup.

- 2026-05-25: Added and verified `scripts/kali-vnc-control.ps1` for a safer VM GUI-control route to `<attacker-vm>`: Kali-side x11vnc/noVNC services bind to Kali localhost only (`127.0.0.1:5901` and `127.0.0.1:6080`), Windows access uses an SSH local tunnel at `http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale`, and `start/status/stop` actions manage service/tunnel state. After operator-installed packages, verification showed `x11vnc=running`, `websockify=running`, `local_tunnel=running`, and local noVNC HTTP 200. Boundary: local VM control-plane setup only; no target interaction, no credential/OTP handling, no proxy/Tor enablement, no scanning/fuzzing/exploitation, and no public report/finding promotion.

- 2026-05-25: Started the <program-redacted> Taiwan single-account surface-map lane from the logged-in Kali VM browser using the authorized live-target workflow skill. Created `programs/<program-slug>/notes/coupang_tw_single_account_surface_map_20260525.md` and saved initial redacted screenshots under `setting/local/screenshots/coupang_surface_20260525/`. Verified a logged-in home state, then stopped when the Kali desktop lock screen appeared during the first GUI-control attempt; no post-login target navigation, scanning, fuzzing, exploit, cross-account test, payment/checkout/KYC/upload/seller/admin action, report submission, or credential/OTP/token storage occurred. Hermes attempted non-sensitive lock-prevention settings; operator must unlock the VM locally before the lane resumes.

- 2026-05-26: Closed the <program-name>/<program-redacted> third-target pre-contact readiness checkpoint without making a new live-target request. Added `programs/<program-redacted>/notes/program-redacted_pre_contact_ready_checkpoint_20260526.md` and `handoff/dirty_tree_checkpoint_audit_20260526.md`; updated `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/current_artifact_index.md`, and `handoff/third_target_contact_checkpoint_20260526.json` so the current state is `READY_FOR_OPERATOR_GATE` / `A2_PENDING_OPERATOR_AUTH`. Runtime readiness verified Kali VM/SSH/noVNC local tunnel availability, with Xvfb/Xfce fallback documented because physical `:0` was at LightDM/Xauthority. Boundary: no <program-name> page was opened in this readiness pass; no signup submit, phone/password/OTP/CAPTCHA/email verification, cookie/token/API-key handling, scanner/fuzzer/DAST/exploit/callback/OAST/tunnel, customer/non-owned data access, integration/invite, billing/KYC, report generation, or report submission occurred. Next operator gate: open local noVNC and complete/stop the signup/auth gate locally, then reply with a non-sensitive status such as `front_signup_complete`, `blocked_phone`, `blocked_email_verification`, `blocked_captcha`, `blocked_policy`, or `stop`.


## 2026-05-26 — <program-name> authorized attacker-flow skill/practical checkpoint

- Created user-local Hermes skill `authorized-attacker-flow` for authorized attacker-perspective workflow: scope gate, proof boundary, proof surrogate, stop-before, evidence packet, candidate preservation.
- Ran first practical <program-name> pass after operator reported first owned account creation complete.
- Evidence captured under `setting/local/screenshots/program-redacted_live_20260526/`; latest: `dashboard_channel_connect_gate.png`.
- Wrote attacker-flow packet: `programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md`.
- Updated `programs/<program-redacted>/lane_state.json` and `handoff/third_target_contact_checkpoint_20260526.json` from signup gate to post-auth passive mapping paused at external shared-channel connection gate.
- Safety: no scanner/fuzzer/DAST, no exploit, no API/token capture, no invite sent, no channel connected, no customer/non-owned data touched, no report submitted.

## 2026-05-26 — Authorized attacker-flow multi-agent hard rule

- Patched user-local skill `authorized-attacker-flow` so non-trivial attacker-flow lanes must actually invoke suitable external/independent workers when available, instead of satisfying role separation by having Hermes or one model read an MD file.
- Added skill reference `references/multi-agent-memory-sync-rule.md` covering Claude Code/Cowork + Codex routing, memory-sync packet requirements, worker artifact requirements, verification, and failure handling.
- Added repo workflow artifact `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md` and synced the rule into `handoff/active_strategy_queue.md`, `handoff/current_artifact_index.md`, and `notes/obsidian_projects/Cybersec Lab.md`.
- Safety: workflow/memory update only; no target touched, no browser action, no scanner/fuzzer/DAST, no exploit, no credentials/tokens, no customer/non-owned data, no report submission.


## 2026-05-26 — Multi-agent hard rule reviewed by Claude Code and Codex

- Actually invoked non-Hermes review routes for the workflow rule instead of only reading/writing MD from Hermes:
  - Claude Code CLI output: `handoff/claude_review_multi_agent_tactical_review_memory_sync_20260526.json`
  - Codex CLI output: `handoff/codex_review_multi_agent_tactical_review_memory_sync_20260526.md`
- Both reviewers returned `REQUEST_CHANGES`; incorporated the main fixes into `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md` and user-local skill `authorized-attacker-flow`: mandatory Claude/Cowork + Codex pair for non-trivial lanes, explicit `non-trivial` trigger, invocation evidence requirement, shape-only-attestation warning, and structured skipped-route/passive-only handling.
- Safety: read-only local workflow review and documentation/skill update only; no target touched, no browser/VM/account action, no scanner/fuzzer/DAST, no exploit, no token/credential handling, no customer/non-owned data, no report submission.

## 2026-05-26 — <program-name> candidate downgraded pending actual multi-agent review

- Incorporated stricter Claude/Codex review feedback after the workflow-rule review: reconciled role labels to canonical `config/worker_roles.txt` vocabulary, backfilled invocation evidence for the rule-review runs, fixed rule numbering, and made the <program-name> implication explicit.
- Downgraded `<program-name>-shared-inbox-object-permission` in `programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md` from `bounded_executable` to `needs_multi_agent_review` until a <program-name>-specific Claude/Cowork + Codex packet exists.
- Added `worker_route_status` to `programs/<program-redacted>/lane_state.json` recording that the workflow rule was reviewed, but <program-name> proof-specific routes remain pending and the lane is passive-only until complete.
- Safety: local documentation/JSON state update only; no target touched, no browser/VM/account action, no scanner/fuzzer/DAST, no exploit, no token/credential handling, no customer/non-owned data, no report submission.

===== notes/obsidian_projects/Cybersec Lab.md =====
1: # Cybersec Lab
2:
3: ## 2026-05-26 multi-agent tactical review + memory-sync correction
4:
5: Status: active workflow rule / no target touched
6: Source: operator correction + Hermes skill update
7: Date: 2026-05-26
8: Repo truth: `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md`, `handoff/active_strategy_queue.md`, user-local skill `authorized-attacker-flow`
9:
10: - Role-separated attacker-flow work must not be reduced to one model reading an MD file. Non-trivial lanes require actual suitable worker invocation when available: Claude Code/Cowork for tactical, boundary, evidence, and strategy perspectives; Codex for deterministic/skeptical review and script/checklist sanity; Hermes for final synthesis and authorization gates.
11: - Workers must receive the project memory-sync packet (`.hermes.md`, current navigation, active queue, artifact index, Cybersec Lab Obsidian bridge, recent accepted changes, active scope/lane state, current candidate/evidence packet, and stop-before rules), not only a single task artifact.
12: - If Claude/Codex/Cowork routes are unavailable, skipped, timed out, or replaced by Hermes for speed, the artifact must record that blocker and the lane remains passive-only unless the operator approves a fresh exception.
13: - This is workflow/process memory only; it does not authorize target-touching work, scanner/fuzzer/DAST, callbacks, token handling, customer/non-owned data contact, or report submission.
14: - Same-day Claude Code and Codex read-only reviews returned `REQUEST_CHANGES`; incorporated the stricter rule: non-trivial lanes require actual Claude/Cowork + Codex participation or a structured skipped-route/passive-only record, plus invocation evidence beyond artifact shape.
15:
16:
17: ## 2026-05-26 tactical-freedom platform correction
18:
19: Status: active design direction / no target touched
20: Source: operator correction + Hermes synthesis
21: Date: 2026-05-26
22: Repo truth: `docs/policy/tactical_freedom_platform_direction_20260526.md`, `docs/strategy/platform/multi_agent_bug_hunting_engineering_plan_20260526.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`
23:
24: - The project should not exclude tactics merely because realistic attackers use dangerous or destructive-looking methods. High-value bug bounty work needs realistic attack-path imagination, not conservative scanning by default.
25: - The core ethical line is different: model the full attack path, but execute only bounded, authorized, recoverable proof surrogates and stop before unauthorized access, non-owned data contact, destructive impact, DDoS/resource exhaustion, credential theft, malware, stealth/persistence/evasion, uncontrolled propagation, or report submission.
26: - The prior L0-L5 ladder is now secondary/internal; the preferred planning primitive is `attack path -> proof boundary -> proof surrogate -> stop condition -> evidence packet`.
27: - Multi-agent advantage should be role separation: adversarial planner maximizes realistic hypotheses, boundary engineer converts them into lawful proof plans, implementer/toolsmith builds bounded offline helpers, evidence critic challenges overclaiming, Hermes synthesizes and enforces authorization gates.
28: - Immediate engineering direction: offline/local platform slice first—attack-path candidate packet, proof-boundary/proof-surrogate schema, preview synthesis helper, and A/B matrix validator. This does not authorize live scanning, exploitation, account actions, target-touching automation, or report submission.
29:
30: ## 2026-05-26 <program-name> target selection for first new-process live run
31:
32: Status: selected candidate / pending exact asset-scope confirmation
33: Source: Hermes passive policy/program-metadata intake from Kali VM
34: Date: 2026-05-26
35: Repo truth: `programs/<program-redacted>/notes/program-redacted_target_selection_preview_20260526.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`
36:
37: - Selected `<program-redacted>` / <program-name> as the recommended first target for the new high-hit-rate workflow.
38: - Reason: open bounty program, explicit researcher signup route, <bug-bounty-platform> alias requirement, API docs, customer-ops/team/workspace product shape, and policy interest in cross-company/cross-tenant disclosure plus admin/API permission boundaries.
39: - Deprioritized alternatives for the immediate first run: `hex` requires emailing for a bounty instance and public JSON shows no bounties; `frontegg` is strong but identity-platform-sensitive; `discourse` has temporary bounty suspension; `airtable` is staging/enterprise-request heavy.
40: - Critical blocker: unauthenticated public <bug-bounty-platform> JSON did not expose <program-name>'s structured asset table; exact logged-in <bug-bounty-platform> asset/scope confirmation is required before any `programs/<program-redacted>/scope.json`, `config/scope.txt`, signup/login, or target-touching work.
41: - Boundary: passive <bug-bounty-platform> program JSON/policy intake only; no <program-name> app navigation, signup, account creation, scan/fuzz/exploit, credential handling, customer interaction, or report submission.
42:
43: ## 2026-05-26 tactical-freedom and no-finding learning loop
44:
45: Status: active / template and feedback loop added
46: Source: Hermes synthesis after operator confirmed the improvement direction
47: Date: 2026-05-26
48: Repo truth: `docs/strategy/live_bounty/live_bounty_tactical_preview_template_20260526.md`, `docs/strategy/live_bounty/live_bounty_no_finding_feedback_log.md`, `docs/strategy/live_bounty/live_bounty_account_ab_operator_action_card_20260526.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`
49:
50: - Added the tactical preview template so live-bounty previews expand options before narrowing, list default and adjacent creative lanes, classify risk/prerequisites, and preserve blocked ideas as next-preview seeds.
51: - Added the no-finding feedback log so <program-redacted>/<program-redacted> no-finding and surface-only outcomes update target-selection rules instead of becoming dead history.
52: - Added the Account A/B operator action card with safe reply phrases for Account B, Tenant B, object visibility, and auth/phone/email/CAPTCHA blocks; secrets and raw identifiers stay out of repo/chat.
53: - Boundary: planning/templates/strategy only; no target asset navigation, account creation, scope expansion, scanning/fuzzing/DAST, exploit execution, credential handling, or report submission.
54:
55: ## 2026-05-26 high-hit-rate live investigation selection
56:
57: Status: active / passive OSINT-first selection layer
58: Source: Hermes A0 passive program-directory OSINT and local synthesis
59: Date: 2026-05-26
60: Repo truth: `docs/strategy/live_bounty/live_bounty_high_hit_rate_target_filter_20260526.md`, `docs/strategy/live_bounty/live_bounty_attack_class_matrix_20260526.md`, `docs/strategy/live_bounty/next_live_bounty_shortlist_20260526.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`
61:
62: - The second live/VDP flow achieved the process-familiarity goal, so the next default is no longer another full-flow surface-only practice run.
63: - New high-hit-rate loop: A0 passive OSINT/program scoring -> select one bug class -> confirm A/B or tenant controls -> timebox A2 viability -> run A3 bounded proof only when exact policy/scope and owned controls exist.
64: - Created a reusable target filter, attack-class matrix, and passive shortlist. Initial high-fit candidates for later exact policy intake are `<program-redacted>`, `discourse`, `hex`, `frontegg`, and `airtable`; these are triage leads only, not authorization.
65: - <program-redacted> remains useful only after Account B is ready and a safe owned object exists; otherwise park it as `blocked_no_owned_object` and switch to a better SaaS/workspace/API candidate.
66: - Boundary: passive public program-directory OSINT only; no target asset navigation, account creation, scope expansion, scanner/fuzzer/DAST, exploit, credential handling, or report submission.
67:
68: ## 2026-05-25 <program-redacted> VDP first owned-account surface map
69:
70: Status: complete / no finding / surface_only
71: Source: Hermes noVNC live-bounty first-flow checkpoint
72: Date: 2026-05-25
73: Repo truth: `programs/<program-slug>/notes/tines_automation_vdp_owned_account_surface_map_20260525.md`, `handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_surface_map_20260525.json`, `programs/<program-slug>/lane_state.json`, `handoff/live_bounty_lane_queue.json`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`
74:
75: - Operator completed the <bug-bounty-platform>-alias <program-redacted> signup/login gate locally in Kali/noVNC; no password, OTP, verification link, cookie, token, or raw alias was recorded.
76: - Hermes performed low-speed browser-only observation of the owned <program-redacted> workspace: Stories dashboard/editor, Credentials empty state, Resources empty state, Users/settings count, API Keys empty state, Authentication settings, Workbench, and account menu.
77: - Result: no reportable vulnerability observed; lane state is `NO_FINDING_CLOSEOUT` / `no_finding`, evidence status `surface_only`; local runner now returns `lane_closed_or_parked` / exit `0` for this lane.
78: - Boundaries respected: no scanner/fuzzer/DAST, no workflow publish/run, no Workbench prompt/tool execution, no integration/webhook/callback, no run-script, no API key/credential/resource creation, no invite, no setting mutation, no cross-tenant/non-owned data, no report submission, no <program-redacted> scope expansion beyond browser-only post-login observation.
79: - Next safe action: none by default for <program-redacted>. Any further <program-redacted> work requires a separately approved lane plan.
80:
274: - Hermes reviews artifacts afterward and labels the result honestly as verified/candidate/blocked/deferred.
275:
276: ## 2026-05-23 five tactical questions for each proof wave
277:
278: Status: active methodology
289: 5. Which proof-library capability does this wave add? If it only adds another log with no reusable evidence pattern, downgrade or choose a better lane.
290:
291: Intent: expand tactical attack-path thinking while keeping the project script-first, context-driven, local-lab-only, and evidence-first. This is not a new governance gate.
292:
293: ## 2026-05-23 preview/review process test on deserialization lane
298: Repo truth: `handoff/modern_api_deserialization_preview_review_process_test_20260523.md`, `handoff/claude_review_deser_preview_test_20260523.md`, `handoff/deser_operator_run_card_20260523.md`, `scripts/labs/operator_deser_bounded_marker_run.sh`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`
299:
300: - Tested the new tactical preview / Claude Code review flow once on the current top lane: dedicated modern_vuln_api unsafe deserialization bounded-marker rerun.
301: - Flow completed through: OSS/source recon -> Hermes tactical preview -> bounded execution attempt -> blocker record -> Claude Code read-only review -> Hermes synthesis.
302: - Result: preview/review process worked and stayed tactical/project-value focused, not a new safety gate.
303: - The runtime deserialization rerun itself is still not verified: execution layer returned `BLOCKED: User denied. Do NOT retry`; Hermes did not retry, encode, disguise, split, or move the trigger.
304: - Claude Code review recommended separating `process test passed` from `vulnerability rerun blocked/deferred`, and not borrowing the prior broad historical deserialization bundle to claim this dedicated wave succeeded.
305: - Operator-run path is now prepared: `scripts/labs/operator_deser_bounded_marker_run.sh` with run-card `handoff/deser_operator_run_card_20260523.md`. It has `--precheck-only`, health/control checks, exact human confirmation, one marker-only trigger, `/deser-log` verification, cleanup, and artifact path.
306:
307: ## 2026-05-23 tactical preview / Claude Code review lenses
308:
309: Status: active process update
312: Repo truth: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`, Hermes skill `owasp-single-vuln-lab-wave`
313:
314: - Added two lightweight tactical perspectives to OWASP single-vulnerability local-lab waves; these are explicitly not new safety gates or governance approvals.
315: - New flow: `OSS/source reconnaissance -> Hermes tactical preview -> Kali bounded-script execution -> artifact/evidence pullback -> Claude Code read-only review -> Hermes synthesis / verified-impact / bundle / evidence-packet promotion`.
316: - Rationale: increase tactical visibility and project-value focus without returning to governance-first process.
317: - Hermes owns preview: challenge planned proof path/tool choice/target surface/artifact value before execution.
318: - Claude Code owns post-evidence review by default: from a compact read-only packet, challenge proof value and overclaim risk, then recommend verified/candidate/attempted/blocked/reference-only plus stop/rerun/switch/packetize.
319: - Boundary unchanged: local authorized lab only unless separately scoped; no public target activation, safety-bypass, credential theft, exfiltration, or automatic finding/report promotion. The point is tactical perspective and project value, not more safety process.
320:
321: ## 2026-05-23 SSRF evidence packet consolidation
431: - Future reruns should use `<attacker-vm>`; historical artifact labels that say `<attacker-vm>` are old route metadata, not the current default.
432: - Script hardening: `scripts/labs/dvwa_command_injection_impact_wave1.sh` now supports optional `EXTERNAL_CALLBACK_LOG` so Docker/external listener evidence can be counted in the script summary/observations instead of being orphaned from the runner's local callback path.
433: - No new exploit rerun was performed: read-only VirtualBox check showed both attacker and victim VMs powered off with NIC2/NAT off.
434: - Next best proof lane after this standardization: browser runtime XSS proof pattern, unless the operator wants to rerun the DVWA packet after manually/explicitly starting the lab route.
435:
436: ## 2026-05-23 current navigation cleanup
437:
438: Status: active
439: Source: User + Hermes
440: Date: 2026-05-23
441: Repo truth: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `docs/policy/lab_safety_contract.md`, `handoff/accepted_changes.md`
442:
443: Current project direction:
444:
445: - Default route: `<attacker-vm>` as attacker / target-touching VM; `<victim-vm>` as victim/靶機 route.
446: - Network posture: host-only by default; NAT closed by default and only opened temporarily for installs/pulls/tool recovery, then closed and verified.
447: - Old `<attacker-vm>` is deprecated/forensic archive only.
448: - Active local targets: DVWA, WebGoat, Juice Shop, and `labs/modern_vuln_api/modern_vuln_api.py`.
449: - Current best next lanes:
450:   1. browser runtime XSS proof pattern;
451:   2. file read / path traversal / XXE safe-marker proof pattern;
452:   3. attacker callback proof adaptation using `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md` as the baseline.
453: - Parked for now: public/real bug bounty activation, contract-first/schema-first/importer-first/report-generator-first work, automatic finding promotion/submission, and broad platform integration before proof packets stabilize.
454: - Evidence style: one vulnerability behavior/class per wave; prefer one-vuln max-impact proof packets with route/tool, exact evidence, controls, cleanup, project benefit, and new/changed artifacts.
455: - Memory routing: Hermes global memory remains a compact signpost; repo handoff is engineering truth; this Cybersec Lab note stores strategy/rationale/navigation; raw sensitive evidence, credentials, loot, private scope, exploit dumps, and raw scans stay out of broad memory notes.
456:
457: ## 2026-05-22 workflow / memory routing confirmation
458:
459: Status: active
460: Source: User + Hermes
461: Date: 2026-05-22
462: Repo truth: `.hermes.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`
463:
464: Process changes confirmed for future agents:
465:
466: - Default target-touching attacker route is `<attacker-vm>`; old `<attacker-vm>` is deprecated/forensic archive only.
467: - Lab infrastructure recovery may use a temporary NAT window only for installs/pulls/tool recovery, then NAT must be closed and verified afterward.
468: - `<victim-vm>` remains the victim/靶機 lane; attacker/victim separation should be preserved for local proofs.
469: - Project-specific cybersec workflow state belongs in repo handoff plus this Cybersec Lab Obsidian project note; Hermes global memory should keep only compact cross-project signposts.
470: - Sensitive material still does not belong in Obsidian: no raw targets, scans, credentials, loot, tokens, hashes, private scope, or exploit evidence dumps.
471:
472: ## 2026-05-21 verified exploit-flow wave 1
473:
474: Artifact: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/`.
475:
476: Verified lab flows:
477:
478: - SQLi login bypass to admin lab JWT, then `/api/Users` read with unauth 401 control.
479: - Unauthenticated `/rest/admin/application-configuration` configuration read.
480: - `/ftp/` directory listing plus bounded reads of `legal.md` and `acquisitions.md`.
481: - Unauthenticated Swagger UI/API docs and Prometheus `/metrics` operational counters.
482:
483: Attempted-not-verified: JWT alg-none probe, coupon/business logic probe, XSS execution marker, source-map disclosure, missing host tools for ffuf/nikto/nmap/sqlmap.
484:
485: ## 2026-05-22 attacker route migration
486:
487: Default attacker/target-touching VM is now `<attacker-vm>`.
488:
489: - Cloned from healthy `kali-linux-2026.1-virtualbox-amd64`.
490: - Old `<attacker-vm>` is deprecated/forensic archive only because VirtualBox reports a broken snapshot/differencing disk chain.
491: - New attacker VM config: 4096 MB RAM, 4 CPUs, host-only NIC1 default, NAT NIC2 closed after temporary tool recovery.
492: - Clean snapshot: `clean-attacker-v2-tools-4096m-4cpu-20260522` (`bcee6035-c86d-41f0-8da1-62b3b42ec388`).
493: - Attacker IP evidence: `<lab-ip>`; victim remains `<victim-vm>` / `<lab-ip>`.
494: - Docker/Compose and baseline tools were recovered during operator-approved temporary NAT; no public-target testing was performed during this infrastructure recovery.
495:
496: ## 2026-05-23 WebGoat browser-runtime XSS rerun
497:
498: Status: active lab result / verified local-lab runtime proof rerun
499: Source: Hermes + read-only artifact review
500: Repo truth: `handoff/webgoat_browser_runtime_xss_rerun_20260523.md`, `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/`
501:
502: Reran the WebGoat XSS safe-marker proof on the current default route (`<attacker-vm>` -> `<victim-vm>`). The proof again produced browser runtime DOM mutation with marker `WG_XSS_RUNTIME_webgoat_browser_runtime_xss_20260523T105506Z`, origin/path labels, negative control with no `data-xss`, pre/post WebGoat health 200, and Internet closed on the attacker route. This confirms the project can currently rerun authenticated browser-runtime XSS evidence, not just static reflection checks. Keep it lab-only/reusable-methodology; no public-target or report-ready claim.
503:
504: ## 2026-05-23 Phase 4 closeout direction
505:
506: Status: active strategy / estimate
507: Source: Hermes synthesis
508: Repo truth: `handoff/phase4_exit_assessment_20260523.md`, `handoff/webgoat_browser_runtime_xss_evidence_packet_20260523.md`
509:
510: WebGoat browser-runtime XSS packet hardening is now complete, joining SSRF true-attacker callback and DVWA callback packet standards. Phase 4 no longer needs many more vulnerability waves to justify closing. Recommended close condition: final closeout note + active queue update + validation, then move to Phase 5 as report-readiness / authorized-assessment preparation, not automatic public target testing. If one more technical proof is desired before closeout, pick exactly one bounded lane such as auth/session role separation or file-read/deserialization report packetization.

===== programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md =====
# <program-name> authorized attacker-flow packet — first practical run

Generated: 2026-05-26T11:12:31Z
Skill used: `authorized-attacker-flow`
Program: <program-name> / <bug-bounty-platform> `<program-redacted>`
Scope artifact: `programs/<program-redacted>/scope.json`
Execution mode: manual/noVNC browser-only passive observation + minimal owned-account onboarding choices.

## Authorization / boundary

- Authorization basis: explicit bug bounty scope captured in `programs/<program-redacted>/scope.json` from logged-in <bug-bounty-platform> CSV.
- In-scope current asset: `<in-scope-host>`.
- API reference asset: `<in-scope-host>` / public docs, not exercised in this pass.
- Account state: operator reports first owned account was created successfully; Hermes did not store password, phone, OTP, cookies, tokens, or verification links.
- Current stop-before: external/shared channel connection, invite/team actions, customer/outbound messages, API token creation/storage, webhooks/callbacks/OAST/tunnels, third-party integrations, billing/payment/support/KYC, scanner/fuzzer/DAST, report submission.

## Observed passive surfaces

Evidence screenshots:

- `setting/local/screenshots/program-redacted_live_20260526/post_signup_attacker_flow_start.png`
- `setting/local/screenshots/program-redacted_live_20260526/post_signup_onboarding_after_start.png`
- `setting/local/screenshots/program-redacted_live_20260526/post_signup_onboarding_step_after_team_next.png`
- `setting/local/screenshots/program-redacted_live_20260526/post_signup_onboarding_after_inbox_setup_later.png`
- `setting/local/screenshots/program-redacted_live_20260526/dashboard_channel_connect_gate.png`

Observed UI state, redacted:

- <program-name> post-signup welcome screen reached.
- Setup questionnaire asked for primary team; selected `Customer Support` as low-risk owned-account profile customization.
- Shared inbox onboarding appeared; chose `Set up later` to avoid unnecessary owned-object creation during mapping.
- Dashboard/setup guide reached.
- Visible setup guide surfaces: create shared inbox, connect shared channel, automate workflows/rules, discover topics, invite team.
- The active setup path now asks to connect a first shared channel, with external account/channel options such as Gmail / Office 365 / chat or SMS-style channels. This is a hard stop-before for this pass.
- Left navigation shows inbox/open/drafts/later/done/more, shared/demo inbox labels, settings/help surfaces, setup guide, trial/banner actions.
- A <bug-bounty-platform> assistant panel is visible in a separate window; no interaction needed for target proof.

## Candidate packet

```json
[
  {
    "candidate_id": "<program-name>-channel-connect-oauth-boundary",
    "attacker_objective": "Abuse connected shared channels or OAuth/mailbox authorization to access or route messages beyond intended workspace boundaries.",
    "path_hypothesis": "The onboarding channel connection flow may expose authorization, redirect, mailbox selection, or tenant-boundary assumptions.",
    "impact_potential": 5,
    "surrogate_feasibility": 2,
    "authorization_readiness": 2,
    "proof_boundary": {
      "in_scope_assets": ["<in-scope-host>"],
      "owned_accounts_or_objects": ["one operator-owned <program-name> workspace/account"],
      "allowed_state_changes": ["passive UI mapping only in this pass"],
      "blocked_state_changes": ["Gmail/Office365/channel connection", "OAuth consent", "external messages", "third-party integrations", "token capture/storage"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only; no customer/non-owned mailbox data"
    },
    "proof_surrogate": "Preserve as gated candidate; next proof would require operator-owned mailbox/channel and explicit token/redaction plan before any connection.",
    "stop_before": ["OAuth/login consent", "mailbox/channel connection", "token exposure", "external communication", "non-owned data"],
    "evidence_requirements": ["channel gate screenshot", "program rule reference", "owned mailbox/channel approval if later pursued"],
    "execution_status": "needs_operator_control"
  },
  {
    "candidate_id": "<program-name>-invite-role-boundary",
    "attacker_objective": "Escalate or retain access through teammate invite, role, removal, or downgrade boundary mistakes.",
    "path_hypothesis": "Team invite and role surfaces may reveal whether low-privilege users can access admin-only workspace or shared-inbox functions.",
    "impact_potential": 4,
    "surrogate_feasibility": 4,
    "authorization_readiness": 3,
    "proof_boundary": {
      "in_scope_assets": ["<in-scope-host>"],
      "owned_accounts_or_objects": ["Account A exists", "Account B not yet created/approved"],
      "allowed_state_changes": ["passive navigation to role/invite UI without sending invites"],
      "blocked_state_changes": ["sending invite email", "changing roles without second owned account plan", "accessing non-owned data"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned accounts only"
    },
    "proof_surrogate": "Map role/invite UI and preserve exact Account B requirements; execute only after operator creates/approves a second owned account/address.",
    "stop_before": ["send invite", "accept invite", "role change with real impact", "non-owned data"],
    "evidence_requirements": ["screenshots of role/invite options with emails redacted", "Account A/B ownership statement", "expected vs observed permissions"],
    "execution_status": "needs_operator_control"
  },
  {
    "candidate_id": "<program-name>-shared-inbox-object-permission",
    "attacker_objective": "Access or manipulate shared inbox objects without the required workspace/inbox permission.",
    "path_hypothesis": "Shared inbox creation and rules/topics may create object IDs and permission boundaries that can later be checked with a second user or lower privilege role.",
    "impact_potential": 4,
    "surrogate_feasibility": 3,
    "authorization_readiness": 4,
    "proof_boundary": {
      "in_scope_assets": ["<in-scope-host>"],
      "owned_accounts_or_objects": ["operator-owned workspace", "demo/empty owned setup surfaces"],
      "allowed_state_changes": ["passive map", "optionally create clearly named owned test inbox only after approval"],
      "blocked_state_changes": ["customer messages", "real outbound communication", "scanner/fuzzer", "non-owned data"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned empty/test objects only"
    },
    "proof_surrogate": "Start with UI/object model inventory; defer object creation until a named owned test object plan is approved.",
    "stop_before": ["message send/receive", "external channel connection", "non-owned data", "destructive deletion"],
    "evidence_requirements": ["object/surface inventory", "redacted screenshots", "owned object labels if created later"],
    "execution_status": "needs_multi_agent_review"
  },
  {
    "candidate_id": "<program-name>-workflow-rule-abuse",
    "attacker_objective": "Use workflow/rule automation to trigger unauthorized actions, data exposure, or outbound side effects.",
    "path_hypothesis": "Rule automation may combine conditions/actions across inboxes, channels, or roles in surprising ways.",
    "impact_potential": 4,
    "surrogate_feasibility": 2,
    "authorization_readiness": 2,
    "proof_boundary": {
      "in_scope_assets": ["<in-scope-host>"],
      "owned_accounts_or_objects": ["operator-owned workspace only"],
      "allowed_state_changes": ["passive rule-builder mapping only"],
      "blocked_state_changes": ["activating rules", "sending messages", "external integrations", "webhooks/callbacks"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only"
    },
    "proof_surrogate": "Map available rule conditions/actions without saving or activating rules; choose a local simulation or owned-object proof later.",
    "stop_before": ["save/enable rule", "external action", "message send", "callback/webhook"],
    "evidence_requirements": ["rule-builder option screenshots", "blocked-action list", "no activation confirmation"],
    "execution_status": "blocked_preserve"
  },
  {
    "candidate_id": "<program-name>-api-ui-permission-mismatch",
    "attacker_objective": "Find API endpoints that allow actions the UI/role model should forbid.",
    "path_hypothesis": "Public API (`<in-scope-host>`) and UI features may expose permission mismatches after token handling and role setup exist.",
    "impact_potential": 5,
    "surrogate_feasibility": 3,
    "authorization_readiness": 2,
    "proof_boundary": {
      "in_scope_assets": ["<in-scope-host>", "<in-scope-host>"],
      "owned_accounts_or_objects": ["operator-owned workspace", "second owned role account needed later"],
      "allowed_state_changes": ["public documentation review only in this pass"],
      "blocked_state_changes": ["API token creation/storage", "API calls", "non-owned data", "scanner/fuzzer"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only"
    },
    "proof_surrogate": "Docs-first endpoint/permission inventory; later create redaction-safe API token plan only if operator approves.",
    "stop_before": ["token creation", "API request", "secret storage", "non-owned data"],
    "evidence_requirements": ["docs endpoint inventory", "permission claim references", "token redaction plan if later pursued"],
    "execution_status": "needs_operator_control"
  }
]
```

## Hermes synthesis

Selected lane for next candidate review: `<program-name>-shared-inbox-object-permission` remains passive/manual surface inventory only until the required Claude/Cowork + Codex review packet exists.

Reason: it is the only candidate with comparatively high authorization readiness while staying inside the existing single owned account and no-callback/no-external-communication boundary, but it is non-trivial under the multi-agent rule. Actual object creation, permission checking, second-account use, or any proof beyond passive mapping requires a role-separated Claude/Cowork + Codex review packet and a separate approval point.

Immediate stop reached: the dashboard is prompting for external/shared channel connection. Do not connect Gmail, Office 365, chat, SMS, Slack, WhatsApp, Twilio, <program-name> Chat, webhooks, or any third-party integration in this pass.

Next safe action: continue passive UI mapping through settings/setup-guide/navigation without creating tokens, sending invites/messages, connecting channels, or activating workflows.


===== programs/<program-redacted>/scope.json =====
{
  "schema_version": "1.0",
  "program": {
    "slug": "<program-redacted>",
    "name": "<program-name>",
    "platform": "<bug-bounty-platform>",
    "url": "https://<bug-bounty-platform>.com/<program-redacted>",
    "authorization_reference": "Operator authorized Hermes to open the third live target only within in-scope <program-name> assets on 2026-05-26. Exact assets were confirmed from the logged-in <bug-bounty-platform> Scope CSV downloaded in Kali/noVNC: setting/local/hackerone_scope/<program-redacted>/scopes_for_program-redacted_at_2026-05-26_08_10_14_UTC.csv.",
    "policy_acknowledged_at": "2026-05-26",
    "program_contact": "<bug-bounty-platform> program: <program-redacted>",
    "status": "scope_confirmed_dry_run_pending_front_a2_viability"
  },
  "scope": {
    "in_scope": [
      {
        "type": "domain",
        "value": "<in-scope-host>",
        "asset_type": "URL",
        "eligible_for_bounty": true,
        "eligible_for_submission": true,
        "max_severity": "critical",
        "notes": "Confirmed in logged-in <bug-bounty-platform> Scope CSV. Selected first-contact web app host for manual/noVNC owned-account viability only."
      },
      {
        "type": "domain",
        "value": "<in-scope-host>",
        "asset_type": "URL",
        "eligible_for_bounty": true,
        "eligible_for_submission": true,
        "max_severity": "critical",
        "notes": "Confirmed in logged-in <bug-bounty-platform> Scope CSV. Public API documented at https://dev.frontapp.com/. API testing requires separate bounded A2 plan, owned account/token handling, and redaction; no token storage in repo."
      },
      {
        "type": "apple_store_app_id",
        "value": "com.frontapp.mobile",
        "asset_type": "APPLE_STORE_APP_ID",
        "eligible_for_bounty": true,
        "eligible_for_submission": true,
        "max_severity": "high",
        "notes": "Confirmed in logged-in <bug-bounty-platform> Scope CSV; reference only for current web-first lane."
      },
      {
        "type": "google_play_app_id",
        "value": "com.frontapp.mobile",
        "asset_type": "GOOGLE_PLAY_APP_ID",
        "eligible_for_bounty": true,
        "eligible_for_submission": true,
        "max_severity": "high",
        "notes": "Confirmed in logged-in <bug-bounty-platform> Scope CSV; reference only for current web-first lane."
      },
      {
        "type": "downloadable_executable",
        "value": "<program-name> for Mac",
        "asset_type": "DOWNLOADABLE_EXECUTABLES",
        "eligible_for_bounty": true,
        "eligible_for_submission": true,
        "max_severity": "high",
        "notes": "Download URL listed as https://<program-domain>/download. Reference only; binary/client testing is not selected for first lane."
      },
      {
        "type": "downloadable_executable",
        "value": "<program-name> for Windows",
        "asset_type": "DOWNLOADABLE_EXECUTABLES",
        "eligible_for_bounty": true,
        "eligible_for_submission": true,
        "max_severity": "high",
        "notes": "Download URL listed as https://<program-domain>/download. Reference only; binary/client testing is not selected for first lane."
      }
    ],
    "reference_only": [
      {
        "type": "url",
        "value": "https://dev.frontapp.com/",
        "notes": "Policy/scope instruction references public API documentation; use for documentation review before API lane."
      },
      {
        "type": "url",
        "value": "https://<program-domain>/signup?affiliate=partners",
        "notes": "Policy signup route captured in prior passive intake; only use if still visible/consistent in current policy and after noVNC stop conditions are acknowledged."
      },
      {
        "type": "url",
        "value": "https://<program-domain>/download",
        "notes": "Listed as executable download source for Mac/Windows assets; not selected for current lane."
      }
    ],
    "out_of_scope": [
      {"type": "action", "value": "non_owned_account_or_customer_data_access", "reason": "Policy says only test owned/permitted accounts and do not download/modify customer data or interact with <program-name> customers."},
      {"type": "action", "value": "service_disruption_dos_or_rate_limit_testing", "reason": "Policy says do not disrupt or degrade <program-name> service."},
      {"type": "action", "value": "out_of_asset_testing", "reason": "Policy says do not test websites out of scope or not listed in assets."},
      {"type": "action", "value": "public_disclosure_without_authorization", "reason": "Policy says do not disclose vulnerability information outside <bug-bounty-platform> without written authorization."},
      {"type": "action", "value": "customer_interaction_or_outbound_messages", "reason": "Policy example explicitly warns against interacting with <program-name> customers or posting comments/messages in customer accounts."},
      {"type": "action", "value": "scanner_fuzzer_dast", "reason": "Not selected for first lane; project boundary keeps live work manual/noVNC low-speed unless separately approved."},
      {"type": "action", "value": "external_callbacks_oast_tunnels_integrations", "reason": "Not selected for first lane; requires separate A4 plan and operator approval."}
    ],
    "idn_handling": "punycode_only"
  },
  "techniques": {
    "allowed": [
      "manual_low_speed_research_account_signup_login_when_policy_consistent",
      "owned_account_profile_workspace_surface_mapping",
      "owned_non_sensitive_role_permission_viability_mapping",
      "documentation_review_of_public_api"
    ],
    "conditionally_allowed_later": [
      "owned_account_a_b_role_permission_checks_after_account_b_or_teammate_control_exists",
      "api_ui_permission_mismatch_checks_after_token_handling_and_redaction_plan",
      "two_owned_company_or_tenant_isolation_checks_after_signup_rules_confirm_multi_tenant_creation"
    ],
    "forbidden_or_blocked_for_first_lane": [
      "scanner_fuzzer_dast",
      "dos_ddos_or_rate_limit_testing",
      "non_owned_account_or_customer_data_access",
      "outbound_message_or_customer_interaction",
      "destructive_or_state_changing_actions_beyond_minimal_owned_account_setup",
      "external_callbacks_oast_webhooks_tunnels",
      "third_party_integrations",
      "credential_token_cookie_or_api_key_storage",
      "public_disclosure_or_report_submission_without_operator_final_approval"
    ],
    "automation_permitted": false,
    "automation_notes": "First lane is manual/noVNC/browser-assisted only. Dry-run safety gate may validate scope without target contact."
  },
  "session_layer": {
    "required_account_identity": "Use <bug-bounty-platform> @researcher-alias.example alias email; policy preview says company name should include [Bug Bounty] SomeCompanyName.",
    "required_headers": {},
    "account_rule": "Only interact with operator-owned or explicitly permitted accounts. Operator handles password, CAPTCHA, OTP, email/phone verification, payment, and recovery gates locally. Do not store alias, credentials, cookies, tokens, API keys, or verification links in repo artifacts."
  },
  "rate_limits": {
    "max_concurrency": 1,
    "request_delay_ms": 5000,
    "notes": "Conservative project default. Stop on CAPTCHA, bot warning, account warning, rate limiting, or policy ambiguity."
  },
  "first_lane": {
    "name": "front_owned_account_signup_profile_workspace_surface_map_then_role_permission_viability",
    "selected_assets": [
      "<in-scope-host>"
    ],
    "api_reference_asset": "<in-scope-host>",
    "goal": "Open the third target in Kali/noVNC using only in-scope <program-name> assets, establish owned-account viability, and map non-sensitive workspace/profile/role surfaces without customer interaction or report submission.",
    "blocked_state_changes": [
      "customer messages or comments",
      "third-party integrations",
      "external callbacks/webhooks/OAST/tunnels",
      "API token retention in artifacts",
      "billing/payment",
      "support/customer interaction",
      "scanner/fuzzer/DAST",
      "report submission"
    ]
  },
  "reporting_rules": {
    "one_vulnerability_per_report": true,
    "detailed_reproducible_steps_required": true,
    "report_submission_requires_operator_final_approval": true,
    "impact_focus": "Policy preview emphasizes cross-company/cross-tenant sensitive disclosure and low-privilege users viewing/executing admin-only API/data. Within-company teammate visibility and non-sensitive API data may be expected behavior and must not be overclaimed."
  },
  "expiration": {
    "valid_from": "2026-05-26",
    "valid_until": "2026-06-25",
    "notes": "Re-check <bug-bounty-platform> policy/scope before target-touching work after this date or if <bug-bounty-platform> shows updates."
  }
}


===== programs/<program-redacted>/lane_state.json =====
{
  "schema_version": "1.0",
  "program_slug": "<program-redacted>",
  "lane_id": "owned_account_signup_profile_workspace_surface_map",
  "lane_title": "<program-name> third target first contact: owned-account signup/profile/workspace surface map",
  "autonomy_level": "A2",
  "state": "A2_POST_AUTH_PASSIVE_SURFACE_MAP_STARTED",
  "status": "paused_at_external_channel_connect_gate",
  "authorization": {
    "program_url": "https://<bug-bounty-platform>.com/<program-redacted>",
    "scope_file": "programs/<program-redacted>/scope.json",
    "global_scope_entries": [
      "<in-scope-host>",
      "<in-scope-host>"
    ],
    "dry_run_gate": "passed",
    "out_of_scope_control": "failed_closed"
  },
  "lane_boundary": {
    "allowed_actions": [
      "manual_low_speed_noVNC_navigation_to_in_scope_app_host",
      "owned_account_signup_flow_until_operator_secret_or_phone_gate",
      "post_auth_profile_workspace_empty_state_surface_map_after_operator_completes_auth_gate"
    ],
    "blocked_actions": [
      "scanner_fuzzer_dast",
      "dos_ddos_or_rate_limit_testing",
      "customer_or_non_owned_data_access",
      "customer_messages_or_outbound_communications",
      "third_party_integrations",
      "callbacks_oast_tunnels_webhooks",
      "credential_token_cookie_api_key_storage",
      "billing_payment_support_or_kYC_flows",
      "report_submission_without_operator_final_approval"
    ],
    "identity_strategy": "Use the operator's <bug-bounty-platform> username <researcher-alias> with <bug-bounty-platform> alias plus addressing for project-specific signup, e.g. <researcher-alias-email> if accepted by the target form. Do not write phone numbers, passwords, OTPs, cookies, tokens, API keys, or verification links into repo artifacts. Company name should include the policy-required [Bug Bounty] marker."
  },
  "operator_gates": [
    "work_email_alias",
    "first_name_last_name_or_safe_labels",
    "policy_required_company_name",
    "job_title_industry_company_size",
    "phone_number",
    "password_or_sso_if_present_later",
    "captcha_otp_email_or_phone_verification_if_present_later"
  ],
  "stop_conditions": [
    "<program-name> page requests password OTP CAPTCHA email phone verification payment or KYC",
    "policy or scope ambiguity appears",
    "account warning bot warning rate limit or anti-abuse challenge appears",
    "non_owned_customer_data or real customer interaction appears",
    "outbound message comment invite integration callback API key or token retention is needed",
    "candidate evidence approaches report_ready"
  ],
  "next_autonomous_action": "Passive UI/docs mapping only. Before any proof, object creation, second-account/role action, invite, API token/API call, workflow activation, or external channel connection, run the required Claude/Cowork + Codex <program-name>-specific review packet and update worker_route_status.",
  "next_operator_action": "No immediate operator action unless choosing to approve a second owned account, owned mailbox/channel connection, invite test, or token/API plan later. Do not provide secrets in chat/repo.",
  "artifacts": {
    "dry_run_packet": "programs/<program-redacted>/notes/program-redacted_first_contact_scope_and_signup_gate_20260526.md",
    "evidence_dir": "setting/local/screenshots/program-redacted_live_20260526",
    "latest_evidence": "setting/local/screenshots/program-redacted_live_20260526/dashboard_channel_connect_gate.png",
    "attacker_flow_packet": "programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md"
  },
  "learning": {
    "preview_references": [
      "programs/<program-redacted>/notes/program-redacted_target_selection_preview_20260526.md",
      "docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md"
    ],
    "next_preview_seed": "<program-name> post-signup dashboard reached. Setup guide exposes shared inbox, channel connect, workflow/rules, topics, and invite surfaces. External channel connection is the current hard stop; next bounded lane is passive shared-inbox/object-permission inventory with no external communication.",
    "reusable_capability": "Third-target scope CSV intake plus in-scope app first contact through Kali/noVNC."
  },
  "updated_at": "2026-05-26",
  "worker_route_status": {
    "status": "pending_front_specific_multi_agent_review",
    "applies_to_candidate": "<program-name>-shared-inbox-object-permission",
    "rule_artifact": "docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md",
    "required_before": "any action beyond passive UI/docs mapping",
    "routes_required": [
      {
        "role": "adversarial-planner",
        "route": "claude_or_cowork",
        "state": "pending",
        "artifact": null
      },
      {
        "role": "boundary-engineer",
        "route": "claude_or_cowork",
        "state": "pending",
        "artifact": null
      },
      {
        "role": "evidence-critic",
        "route": "claude_or_cowork",
        "state": "pending",
        "artifact": null
      },
      {
        "role": "deterministic-reviewer",
        "route": "codex",
        "state": "pending",
        "artifact": null
      }
    ],
    "routes_completed": [
      {
        "scope": "workflow_rule_review_only_not_front_proof",
        "route": "claude_code_cli",
        "artifact": "handoff/claude_strict_review_multi_agent_tactical_review_memory_sync_20260526.json",
        "verdict": "REQUEST_CHANGES",
        "note": "Reviewed workflow rule, not enough to advance <program-name> proof."
      },
      {
        "scope": "workflow_rule_review_only_not_front_proof",
        "route": "codex_cli",
        "artifact": "handoff/codex_strict_review_multi_agent_tactical_review_memory_sync_20260526.md",
        "verdict": "PASS",
        "note": "Reviewed workflow rule, not enough to advance <program-name> proof."
      }
    ],
    "passive_only_until_complete": true,
    "updated_at": "2026-05-26"
  }
}


===== config/worker_roles.txt =====
# Canonical worker roles for Hermes multi-agent artifacts.
# One role per line. Blank lines and # comments are ignored.
# This file is a local workflow contract only; it does not authorize target-touching work.
adversarial-planner
boundary-engineer
implementation-worker
deterministic-reviewer
safety-reviewer
evidence-critic
final-synthesizer


===== docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md =====
# Multi-agent tactical review + memory-sync rule

Status: active workflow rule / no target touched
Source: operator correction + Hermes skill update
Date: 2026-05-26
Repo truth: `handoff/active_strategy_queue.md`, `handoff/current_artifact_index.md`, `notes/obsidian_projects/Cybersec Lab.md`, user-local skill `authorized-attacker-flow`

## Operator correction

The role-separated attacker-flow workflow must not be satisfied by Hermes or a single model simply reading an MD file and writing a summary. For non-trivial lanes, the roles must actually invoke suitable independent agents when available, especially Claude Code/Cowork and Codex, so the workflow gets multi-party tactical, boundary, evidence, and deterministic-review perspectives.

## Hard rule

Before a non-trivial candidate lane can move beyond passive UI/docs observation or become `bounded_executable`, Hermes must either:

1. run actual role-separated worker passes and verify their artifacts; or
2. explicitly record that the worker route was unavailable/skipped and keep execution limited to passive observation unless the operator gives a fresh exception.

Post-review tightening: for non-trivial lanes, the default is not merely "suitable workers if available". The lane must have at least one actual Claude Code/Cowork tactical/boundary/safety/evidence review and one actual Codex deterministic/skeptical review before advancing beyond passive mapping. If either route is unavailable, the skipped-route record must include attempted command/tool, blocker, timestamp, fallback decision, and passive-only state.

`Non-trivial` means any candidate or lane that is `bounded_executable`, `needs_operator_control`, or otherwise crosses beyond passive UI/docs mapping toward object creation, second-account action, invite, role change, token/API use, workflow activation, external channel connection, callback/webhook/OAST, scanner/fuzzer/DAST, or report-ready evidence.

## Default worker routing

- Claude Code / Cowork: `adversarial-planner`, `boundary-engineer`, `safety-reviewer`, `evidence-critic`.
- Codex: `deterministic-reviewer` for schema/script/checklist sanity and tactical objections.
- Hermes: final-synthesizer, authorization/scope gate, verification runner, memory-sync owner.

At least two non-Hermes perspectives are expected for non-trivial bounded execution:

- one tactical/strategic review, preferably Claude Code/Cowork;
- one deterministic/skeptical review, preferably Codex.

## Memory-sync packet requirement

Workers must receive current project state, not just the lane MD file. Prompts/artifacts must include or require reading:

- `.hermes.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/current_artifact_index.md`
- `notes/obsidian_projects/Cybersec Lab.md`
- recent `handoff/accepted_changes.md` entries
- active `programs/<slug>/scope.json`
- active `programs/<slug>/lane_state.json`
- current candidate/evidence packet
- exact safety boundary and stop-before list

Secrets, OTPs, passwords, phone numbers, cookies, tokens, API keys, verification links, raw customer data, and loot stay out of worker packets.

## Worker artifact requirements

Each worker output must include:

- Worker identity
- canonical `role:` from `config/worker_roles.txt` when present
- route/tool and visible model/runtime when available
- invocation evidence: command summary, session/run id when available, raw output path, and JSON usage/run artifact path when available
- context read attestation
- role-specific findings
- at least one objection, constraint, evidence gap, or preserved future lane
- validation performed
- verdict

## Verification and sync

After worker outputs are written:

1. Run `scripts/check-worker-attestation.py` when applicable.
2. Run `bash ./bin/hermes review` when project files changed or a lane is about to move state.
3. Hermes manually verifies invocation evidence; shape-only attestation is not sufficient for non-trivial lanes.
4. Hermes synthesis compares disagreements and selects at most one lane.
5. Update lane state/checkpoint with a structured `worker_route_status` or equivalent route-evidence block and append `handoff/accepted_changes.md`.
6. Update `handoff/active_strategy_queue.md` / `handoff/current_artifact_index.md` if navigation changed.
7. Update the Cybersec Lab Obsidian bridge for durable process/methodology decisions.

## <program-name> immediate implication

The existing <program-name> attacker-flow packet is useful as a seed, but it should not be treated as a complete multi-agent review. Before pushing `<program-name>-shared-inbox-object-permission` into any bounded proof beyond passive mapping, run a role-separated review packet with actual Claude Code/Cowork and Codex participation or explicitly record a passive-only exception.


## 2026-05-26 read-only worker review of this rule

Hermes actually invoked both non-Hermes routes for this rule update:

- Claude Code CLI: `handoff/claude_review_multi_agent_tactical_review_memory_sync_20260526.json`
- Codex CLI: `handoff/codex_review_multi_agent_tactical_review_memory_sync_20260526.md`

Both returned `REQUEST_CHANGES`, mainly because the first draft needed less-soft language, concrete invocation evidence, a non-trivial trigger definition, and structured skipped-route evidence. Those changes are incorporated above and in the user-local `authorized-attacker-flow` skill/reference.

Invocation evidence for this workflow-rule review:

- Claude version check: `claude --version` -> `2.1.146 (Claude Code)`.
- Claude command summary: `claude -p "$(cat handoff/multi_agent_tactical_review_memory_sync_strict_attestation_prompt_20260526.md)" --allowedTools "Read,Grep,Glob" --max-turns 10 --output-format json > handoff/claude_strict_review_multi_agent_tactical_review_memory_sync_20260526.json`.
- Claude output artifacts: `handoff/claude_strict_review_multi_agent_tactical_review_memory_sync_20260526.json`, extracted readability copy `handoff/claude_strict_review_multi_agent_tactical_review_memory_sync_20260526.md`.
- Codex version check: `codex --version` -> `codex-cli 0.130.0`.
- Codex session id: `019e6413-c6cf-7471-8282-6d3f189ea21e`.
- Codex command summary: `codex exec --sandbox read-only --output-last-message handoff/codex_strict_review_multi_agent_tactical_review_memory_sync_20260526.md - < handoff/multi_agent_tactical_review_memory_sync_strict_attestation_prompt_20260526.md`.
- Codex output artifact: `handoff/codex_strict_review_multi_agent_tactical_review_memory_sync_20260526.md`.
