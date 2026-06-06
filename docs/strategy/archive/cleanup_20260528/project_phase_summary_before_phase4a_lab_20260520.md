> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Project Phase Summary Before Phase 4A Lab Work

Status: current roadmap summary / pre-lab gate
Date: 2026-05-20
Prepared by: Hermes
Scope: documentation and target-selection gate only; no target-touching action authorized by this file

## Long-term goal

Build an authorized bug-bounty platform that can safely move from scoped reconnaissance to candidate findings, evidence review, manual verification, report readiness, and eventually first legitimate bounty submission.

The platform direction is:

1. authorization and scope gates first;
2. dry-run and offline contracts before execution;
3. candidate-only output before confirmed findings;
4. human-in-loop verification before reports;
5. controlled lab calibration before any real bug-bounty target;
6. one-program private beta before production-like multi-program automation.

## Current phase

Current state: Phase 3 is closed as an offline/dry-run local MVP checkpoint.

Decision source: `handoff/phase3_dry_run_local_mvp_closeout_20260520.md`
Decision: `PASS_WITH_CONDITIONS / CLOSE_PHASE_3_OFFLINE_MVP`

Next phase: Phase 4A — Controlled Lab Semi-Automated Calibration / 授權靶場半自動流程校準.

This means the project is ready to prepare for a lab target, but not to touch any target until the lab target and scope are explicitly selected and recorded.

## Phase-by-phase summary

### Phase 0 / baseline — workspace, safety, and recon foundation

What was established:

- Cybersecurity lab repository and Hermes/Cowork/Codex workflow.
- Authorization-first operating model.
- `config/scope.txt` global scope whitelist concept.
- `recon.sh` and local tooling foundation.
- Rule that scanner output is triage only, never automatic confirmation.

Safety boundary:

- No unauthorized scans.
- No stealth, persistence, credential theft, malware, destructive actions, evasion, or out-of-scope target interaction.

### Phase 1 — program scope and policy gates

What was established:

- Per-program scope/rule direction.
- Offline validators and policy decision helper concepts.
- Default-deny interpretation of program/global scope.
- Program-policy runtime hardening direction.
- Synthetic `_examples/` fixtures clarified as test-only, never real authorization.

Important outcome:

- Scope and policy became reusable platform contracts, not ad-hoc CLI checks.

Remaining limitation:

- Real bug-bounty program scope/rules still need operator-provided program details and manual review before use.

### Phase 2 — offline contracts, module runner, and candidate review workflow

What was established:

- Finding/evidence contract layer.
- Run manifest / preview / ledger concepts.
- Dry-run-only module runner preview.
- Module manifest/profile contracts.
- Level 1 offline audit modules.
- Module I/O preview contracts and bundle consistency checks.
- Candidate review workflow:
  - candidate review packet;
  - gap/action review;
  - verification plan/checklist;
  - report-readiness gate;
  - offline end-to-end fixture.

Important outcome:

- The project can reason about candidate findings and report-readiness without touching real targets or submitting reports.

Remaining limitation:

- Current workflow remains trial/offline. It does not import real scanner output, execute modules, draft final reports, or submit anything externally.

### Phase 3 — offline hardening, governance, and dry-run/local MVP closeout

What was established:

- Curated synthetic bug-bounty-shaped fixtures.
- Terminal-state matrix for candidate workflow expectations.
- Two-module discovery and runner-indifference coverage.
- Data-only report-readiness reviewer prompt catalog.
- Multi-party review templates and decision-gate governance.
- Memory/strategy routing and active strategy queue.
- Program-policy dry-run regression coverage.
- Recon-to-runner policy artifact coverage in dry-run / direct-read / test-harness-only form.
- SOC evidence-bucket and reviewer-gap catalog as static calibration companions.
- Active-testing risk-tier policy.
- Manifest/profile policy crosswalk; formal field promotion deferred.
- Phase 3 closeout as offline/dry-run local MVP.

Important outcome:

- The project is coherent enough to stop adding Phase 3 micro-slices by default.
- The next safe milestone is not a real bug-bounty run; it is controlled lab calibration.

Remaining limitation:

- No lab target is selected yet.
- No live-ish activation is approved yet.
- No scanner/module execution is approved yet.

## Phase 4A — what starts now

Phase 4A purpose:

Use one explicitly authorized lab target to calibrate the workflow before any real bug-bounty private beta.

Allowed target classes after explicit selection:

- local lab controlled by the operator;
- intentionally vulnerable local app;
- explicit CTF/training platform instance;
- user-owned asset explicitly designated for lab testing.

Good first choices:

1. OWASP Juice Shop local instance — recommended first web-app lab for bug-bounty workflow calibration.
2. DVWA local instance — simpler classic web vulns, useful for basic scanner/evidence loop.
3. WebGoat local instance — structured training style.
4. PortSwigger Web Security Academy lab — explicit training target, but external web interaction must stay limited to the selected lab.
5. HackTheBox / TryHackMe machine — acceptable only after explicit machine/scope selection.

## Pre-lab activation gate

Before touching any target, even a lab, Hermes needs the operator to provide:

1. Target class: local app / CTF-training / user-owned asset.
2. Exact target: URL, IP, hostname, or platform machine name.
3. Authorization statement: confirm it is your lab, intentionally vulnerable app, CTF/training instance, user-owned asset, or otherwise authorized.
4. Allowed actions for this session:
   - passive browse only;
   - service discovery;
   - light web enumeration;
   - vulnerability verification;
   - exploit proof-of-concept;
   - no brute force / no fuzzing / no callbacks unless explicitly approved.
5. Rate/impact limits:
   - request rate or scan intensity;
   - stop conditions;
   - whether credentials are involved;
   - whether screenshots/evidence can be saved.

Without these details, only planning and local documentation are allowed.

## Recommended first lab run shape

For the first target-touching Phase 4A session, prefer conservative manual-assisted calibration:

1. Confirm authorization and exact scope.
2. Record lab scope artifact under handoff/local notes.
3. Start with low-noise reachability and service identification.
4. Collect minimal evidence: headers, landing page, service versions, app type.
5. Run only explicitly allowed low-risk checks.
6. Convert observations into candidate findings, not confirmed findings.
7. Review false positives and evidence quality.
8. Update manual verification checklist.
9. Stop before report submission or real bug-bounty claims.

Default forbidden unless separately approved:

- brute force;
- heavy fuzzing;
- exploit chaining;
- callbacks/OAST;
- proxy/pivot/tunnel behavior;
- credential theft or loot collection;
- persistence;
- destructive tests;
- public target testing;
- report submission.

## Current safest next action

Ask the operator to choose the first Phase 4A target and scope.

Recommended default if the operator has no preference:

- OWASP Juice Shop running locally or inside the Kali/lab network.

If the operator wants HTB/THM/PortSwigger instead, the next step is to record the exact platform machine/lab URL and keep interaction limited to that lab.

## Operator prompt for next step

Please provide one of these:

Option A — local vulnerable app:

```text
Target class: local intentionally vulnerable app
App: OWASP Juice Shop / DVWA / WebGoat / other
URL or IP:
Authorization: I own/control this lab and approve Phase 4A low-risk calibration
Allowed actions: passive browse + light enumeration only / include vulnerability verification / other
Limits: no brute force, no heavy fuzzing, no callbacks, stop if auth/secret/loot appears
```

Option B — CTF/training platform:

```text
Target class: CTF/training platform
Platform: HTB / THM / PortSwigger / other
Machine or lab name:
URL/IP:
Authorization: this is an explicit training target assigned to me
Allowed actions:
Limits:
```

Option C — user-owned asset:

```text
Target class: user-owned asset
Asset:
Scope:
Authorization: I own/control this asset and approve this specific test
Allowed actions:
Limits:
```

## Safety boundary

This summary does not authorize target-touching by itself.

No live scans, probes, scanner/module execution, target interaction, fuzzing, brute force, exploit attempts, callbacks/OAST, proxy/pivot/tunnel/transport behavior, credentials, loot-class collection, report submission, scheduler/CI target-touching automation, `config/scope.txt` changes, or real bug-bounty program activation were introduced.
