> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Result — Role-separated workflow hardening smoke test (2026-05-26)

## Worker identity
- route: cowork
- tool/runtime: Claude Code CLI
- role: adversarial planner / workflow critic
- task file: handoff/cowork_task.md
- output artifact: handoff/cowork_result.md

## Context read attestation
- [x] handoff/current_navigation.md
- [x] handoff/active_strategy_queue.md
- [x] handoff/current_artifact_index.md
- [x] handoff/accepted_changes.md
- [x] notes/obsidian_projects/Cybersec Lab.md
Missing / not read:
- none

Additional task-specific reads (informational; not part of the required-context contract):
- handoff/multi_agent_bug_hunting_operating_model_20260526.md (full)
- handoff/multi_agent_bug_hunting_engineering_plan_20260526.md (full)
- scripts/check-worker-attestation.py (full)
- tests/test_worker_context_attestation.sh (full)

## Validation
- Local checks run: static-only review against the four task-specific files; no execution, no test invocation, no target touch, no scope change.
- Files changed/reviewed: scripts/check-worker-attestation.py, tests/test_worker_context_attestation.sh, handoff/multi_agent_bug_hunting_operating_model_20260526.md, handoff/multi_agent_bug_hunting_engineering_plan_20260526.md, handoff/current_artifact_index.md, handoff/active_strategy_queue.md, handoff/current_navigation.md, notes/obsidian_projects/Cybersec Lab.md, handoff/accepted_changes.md (most recent entries).
- Safety boundary checked: offline/local design review only; no browse, scan, fuzz, exploit, account action, scope edit, credential handling, evidence deletion, or report submission proposed.

## Critique of the proposed slice

### 1. Is `role-separated workflow scaffolding v1` the right next step after worker context attestation?

**Not as currently framed.** I am pushing back on the slice in its broad form. Three concrete reasons:

1. **Role separation is already encoded for the most concrete consumer.** The recent `scripts/live-bounty-preview-synthesize.py` + `schemas/attack_path_candidate.schema.json` + `templates/live_bounty_attack_path_candidate_packet.md` already accept 2–3 role-separated companion packets (adversarial planner / boundary engineer / evidence critic style) and synthesize one Hermes decision. There is one proven consumer; there is not yet a second consumer asking for generic scaffolding.
2. **`scripts/check-worker-attestation.py` already enforces a `role` field per artifact** as part of `Worker identity`. The route+role vocabulary is free-form but listed in `.hermes.md`. The missing pieces are *canonicalization* and *cross-artifact decision gating*, not a new scaffolding layer.
3. **Operator standing preference disfavors contract-first / schema-first / governance-first work** (see `handoff/active_strategy_queue.md` parked lanes and `handoff/current_navigation.md` parked lanes). A broad "role-separated workflow scaffolding v1" without an immediate bug-hunting consumer is exactly that pattern. The engineering plan also says explicitly: *"Do not build everything at once."* and recommends Task 1 (A/B matrix template) → Task 2 (validator) → Task 3 (run-card generator) as the next three slices.

**Stronger candidates for the next slice:**

- **A. (Recommended) Engineering-plan Milestone 1 Task 1+2:** `templates/live_bounty_ab_matrix_template.md`, `schemas/live_bounty_ab_matrix.schema.json`, `scripts/live-bounty-ab-matrix-validate.py`, tests. Concrete consumer (<program-redacted> Account B once Account B exists; any future owned-object lane). Directly raises bug-hunting capability rather than meta-process.
- **B. Narrow role-vocabulary tightening to the attestation contract:** ship only the smallest piece of "role-separated workflow scaffolding" that pays for itself today — a canonical role vocabulary file + tightened `role:` validation in the existing attestation checker + an optional `--roles-required` flag. No new framework, no new directory tree, no new helper class.

If the operator wants the role-separated scaffolding direction *now*, do option B, not the broad proposal. If the operator wants the most project value now, do option A.

### 2. Minimal concrete files to create/change (if the slice goes ahead in narrow form — option B)

The smallest defensible version of "role-separated workflow scaffolding v1":

| Action | Path | Purpose |
|---|---|---|
| create | `config/worker_roles.txt` | canonical role vocabulary list (one role per line, lowercase-hyphen). Initial set: `adversarial-planner`, `boundary-engineer`, `implementation-worker`, `deterministic-reviewer`, `safety-reviewer`, `evidence-critic`, `final-synthesizer`. Operator-owned; never auto-rewritten. |
| edit | `scripts/check-worker-attestation.py` | when `config/worker_roles.txt` exists, the `role:` field in `Worker identity` must match exactly one canonical role (or use `other:<freeform>` with reason). No silent role drift. Backwards-compatible: missing file = current free-form behavior. |
| edit | `scripts/check-worker-attestation.py` | add `--roles-required adversarial-planner,boundary-engineer,evidence-critic,final-synthesizer` (repeatable / comma-list) so a pipeline gate can require that one artifact exists per listed role across the supplied `--file` set. Default behavior unchanged. |
| create | `templates/role_packet_base.md` | single shared markdown sub-template that already complies with the attestation contract: `Worker identity` / `Context read attestation` / `Validation` / `Verdict` plus a per-role `## Role notes` section. No new top-level contract. |
| create | `tests/test_worker_roles_vocabulary.sh` | RED→GREEN: free-form role still passes when `config/worker_roles.txt` is absent; unknown role fails when it is present; `--roles-required` flags missing roles; `other:<freeform>` accepted. |
| edit | `handoff/current_artifact_index.md` | add `config/worker_roles.txt` as `operator-owned` and the role packet template + test as `active-engineering`. |
| edit | `.hermes.md` | reflect that role vocabulary is now canonical when the file is present; no new authority and no new safety claim. |
| edit | `handoff/accepted_changes.md` | prepend a compact entry describing the change, validation commands, and the explicit "no new authority" line. |

Do **not** in this slice:
- create a new `roles/` directory tree;
- add a new orchestrator/state machine for multi-agent decisions;
- introduce a JSON schema for "multi-agent decision packet";
- wire `--roles-required` into `bin/hermes review` by default (keep it pipeline-gate opt-in);
- touch `bin/hermes` worker invocation surface beyond what is strictly needed for the role vocabulary check.

### 3. Required roles and fields per role artifact

If `config/worker_roles.txt` is shipped, each role artifact MUST already be a valid attestation artifact (no change to that contract) and SHOULD include one role-specific `## Role notes` section. Minimum per-role expectations below — these are template-level expectations, **not** new gate fields, to avoid premature schema growth.

| Role | Role notes expected to contain |
|---|---|
| `adversarial-planner` | 5+ attack-path candidates; explicit "high-impact-but-blocked candidates preserved as parked, not deleted"; mapping to `proof_surrogate` ideas; `stop_before` list. |
| `boundary-engineer` | one concrete `proof_boundary`: scope artifact path, owned controls, callback/OAST/tunnel allowance, state-change boundary, data-contact boundary, destructive-impact boundary. |
| `implementation-worker` | files changed, exact rerun commands, no inline secrets, evidence path under `handoff/live_bounty_evidence/` when applicable. |
| `deterministic-reviewer` | tests/static checks executed, diff summary, false-positive controls considered. |
| `safety-reviewer` | scope artifact verified, forbidden-flow check, operator-gate triggers, PASS/BLOCK/ESCALATE. |
| `evidence-critic` | overclaim check, missing-control check, redaction check, recommendation: `report_ready` / `candidate_needs_control` / `no_finding` / `parked`. |
| `final-synthesizer` | Hermes synthesis: chosen lane or `park/preserve`; explicit cross-role conflict resolution; final verdict. |

These are template expectations checked at review time by humans, not new machine-enforced fields. The only machine-enforced additions are: (i) role string is canonical when the vocabulary file exists, (ii) `--roles-required` flags missing role artifacts.

### 4. Safety boundary and stop-before rules

This slice is offline/local workflow hardening only. It MUST NOT:

- create or modify any target-touching authority, automation, or runner;
- add or modify `config/scope.txt`, `programs/<slug>/scope.json`, or any per-program scope artifact;
- send requests to any target, browser-automate, signup, login, store credentials/OTP/cookies/tokens/phone/email/PII, or interact with customer support;
- run scanners, fuzzers, DAST, callbacks/OAST/tunnels, exploitation, brute force, account creation, workflow execution, run-script, integrations, or webhooks;
- introduce stealth/persistence/evasion, malware, DDoS/resource exhaustion, credential theft, or destructive impact patterns;
- weaken `.gitignore`, exfiltrate evidence, delete `<artifact-output-dir>/`, `scans/`, `logs/`, `loot/`, browser profiles, or any evidence directory;
- promote candidate/no-finding state, mark lanes report-ready, or submit reports;
- bypass or rewrite the existing attestation contract — extend it backwards-compatibly only;
- become a new approval-heavy governance layer (operator preference: tactical perspective, not governance-first gates).

Stop-before rules during implementation: if the role vocabulary file would force any existing legitimate worker artifact to fail attestation, stop and either (a) add the missing role to vocabulary, or (b) widen `other:<freeform>` handling — do not retroactively reject historical artifacts.

### 5. What deterministic reviewer / Codex should check afterward

If the slice is implemented (either option A or option B), the deterministic reviewer / Codex run should verify:

1. `python -m py_compile scripts/check-worker-attestation.py` succeeds.
2. `bash tests/test_worker_context_attestation.sh` still passes unchanged.
3. New `bash tests/test_worker_roles_vocabulary.sh` passes (or, for option A, new A/B matrix tests pass).
4. `bash ./bin/hermes review` still passes on a clean tree.
5. `git diff --stat` shows no edits outside the listed files; in particular no edits to `config/scope.txt`, `programs/*/scope.json`, `bin/hermes` worker invocation surface (beyond the minimal documented change), `recon.sh`, or any evidence/lane state file.
6. Grep the diff for forbidden tokens introduced by the change: `curl`, `requests.`, `subprocess.*kali`, `webdriver`, `selenium`, `playwright`, `nuclei`, `nmap`, `ffuf`, `feroxbuster`, `burp`, `callback`, `OAST`, `tunnel`, raw target hostnames. Any hit = REQUEST_CHANGES.
7. The change introduces no new external-network capability and no new file write outside `handoff/`, `templates/`, `scripts/`, `tests/`, `config/`, `.hermes.md`.
8. The attestation contract remains backwards-compatible: at least one existing accepted worker artifact (e.g., the good fixture in `tests/test_worker_context_attestation.sh`) still passes.
9. The new role vocabulary file is operator-owned and listed in `handoff/current_artifact_index.md`.
10. `handoff/accepted_changes.md` prepends a compact entry that explicitly states "no new target-touching authority and no new approval-heavy process."

If the operator chooses option A (A/B matrix template + validator) instead, add: (a) the validator rejects cookie/token/session/authorization headers, OTP-like labels, phone-like values, raw emails; (b) the validator rejects evidence paths outside `handoff/live_bounty_evidence/`; (c) the validator requires `["Account A","Account B"]` labels and rejects raw account identifiers.

### 6. Verdict

REQUEST_CHANGES

Rationale: the slice as named ("role-separated workflow scaffolding v1") is broader than the current evidence justifies and risks the parked "contract-first / schema-first / governance-first" pattern. Before shipping a generic role-scaffolding framework, either (a) ship the next plan-aligned tactical slice (A/B matrix template + validator + run-card) which has an immediate <program-redacted>/owned-object consumer, or (b) ship only the narrow role-vocabulary tightening described in section 2 as the smallest backwards-compatible extension to the existing attestation contract. Both options preserve the multi-agent direction without committing to scaffolding ahead of demand.

## Verdict

REQUEST_CHANGES
