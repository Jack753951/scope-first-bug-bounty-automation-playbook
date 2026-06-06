> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Multi-Agent Cybersecurity Workflow Build History And Reusable Blueprint

Date: 2026-05-15
Status: Reusable process document for other projects
Source project: Cybersecurity Lab / authorized bug bounty platform workspace

## Purpose

This file records how this project evolved from a collection of cybersecurity scripts and notes into a safer, more systematic Hermes + Codex + Claude/Cowork operating workflow.

It is written so other projects can copy the pattern without copying the exact cybersecurity assets.

The core idea:

```text
Hermes = coordinator / safety gate / memory / scheduler / final verifier
Codex = implementation engineer / automation builder / test fixer
Claude/Cowork = strategy reviewer / product-security reviewer / architecture critic
Project files = durable handoff memory and audit trail
```

## What Problem This Workflow Solves

Many personal labs and automation projects fail in predictable ways:

- scripts grow into monoliths
- safety checks are copied inconsistently
- findings/reports are generated from raw scanner output
- AI agents make changes without durable handoff records
- reviews only look for blockers, not long-term architecture fit
- project strategy drifts because nobody periodically reviews the whole system

This workflow addresses those problems by separating roles, keeping durable files, enforcing review gates, and periodically asking third-party models to critique the roadmap.

## Final Operating Model

### Role Split

| Role | Responsibility | Typical Outputs |
| --- | --- | --- |
| Hermes | Coordinator, authorization/scope gate, scheduler, memory keeper, local verifier, final arbitrator | `handoff/accepted_changes.md`, `handoff/latest_check.md`, cron jobs, final summaries |
| Codex | Concrete implementation, schemas, scripts, tests, validation automation | `handoff/codex_task.md`, `handoff/codex_review.md`, code changes |
| Claude/Cowork | Strategy, threat modeling, documentation, independent review, third-party architecture/product-security recommendations | `handoff/cowork_*_review.md`, proposals, strategic recommendations |
| Operator | Owns authorization, target scope, risk appetite, final approval for high-risk actions | scope approvals, program rules, publish/deploy approvals |

### Default Loop

```text
1. Operator states goal.
2. Hermes classifies the request and checks safety/scope.
3. Claude/Cowork proposes strategy if planning is needed.
4. Hermes translates strategy into a constrained Codex task.
5. Codex implements minimal safe changes and records validation.
6. Claude/Cowork independently reviews Codex's result.
7. Hermes verifies locally, arbitrates blocking vs non-blocking items, updates handoff.
8. Project proceeds to next phase only after review and verification.
```

### Review Standard

Claude/Cowork review is not only a blocker check. It must include:

```text
1. Blocking issues
2. Non-blocking improvements
3. Strategic recommendations
4. Architecture fit against long-term goals
5. Safety / scope assessment
6. Testing / validation assessment
7. Recommended next phase
```

## Safety Model

This workflow is especially important for cybersecurity projects, but the pattern applies to any high-risk automation.

Binding rule:

```text
No active scan, exploit, brute force, callback, fuzzing, or target-touching automation runs without explicit authorization/scope.
```

For this project, valid authorization categories are:

- local lab or intentionally vulnerable app
- CTF / training platform
- user-owned asset
- written client authorization
- explicit bug bounty scope

For other projects, replace this section with the project's own risk gates, for example:

- finance: no live trading without paper-trading validation and explicit approval
- publishing: no public publish without preview approval
- infrastructure: no production deployment without rollback plan and approval
- data: no external upload of private data without explicit consent

## Durable Files Created During The Workflow

### Core Project Context

```text
.hermes.md
HERMES_WORKFLOW.md
handoff/sustained_review_loop.md
```

Purpose:

- define roles
- define routing rules
- define safety gates
- document worker commands
- tell future agents how the project should be operated

### Handoff Files

```text
handoff/cowork_proposal.md
handoff/codex_task.md
handoff/codex_review.md
handoff/accepted_changes.md
handoff/latest_check.md
handoff/cowork_<phase>_review.md
```

Purpose:

- make agent work traceable
- avoid losing decisions in chat context
- let future agents resume safely
- preserve append-only accepted history

### Architecture Direction Files

```text
handoff/extensible_architecture_direction.md
handoff/post_scan_agent_review_workflow.md
handoff/module_system_architecture_notes.md
handoff/systematization_extension_plan.md
handoff/periodic_third_party_review_process.md
```

Purpose:

- capture long-term system goals
- prevent one-off script sprawl
- document modularity decisions
- define post-scan agent-assisted analysis
- define periodic third-party review cadence

## Build History Timeline

### Stage 0 — Establish The Coordinator Role

The project first defined Hermes as coordinator and security gate.

Key decisions:

- Hermes does not blindly execute target-touching commands.
- Hermes classifies every request before routing.
- Codex handles implementation.
- Claude/Cowork handles strategy and independent review.
- Durable handoff files are preferred over transient chat-only decisions.

Reusable lesson:

```text
Before adding more automation, define who is allowed to decide, implement, review, and approve.
```

### Stage 1 — Harden Scope And Runtime Safety

The project then hardened `recon.sh` so every target path had to pass a central `safe_target` guard.

What changed conceptually:

- scope checking became mandatory
- `--skip-scope-check` was restricted to dry-run override behavior
- domain expansion output was revalidated before later stages
- out-of-scope expansion results were dropped with audit reasons
- validation used dry-run and synthetic targets, not live unauthorized testing

Reusable lesson:

```text
Centralize high-risk policy decisions. Do not let each script invent its own safety check.
```

### Stage 2 — Add Independent Review After Implementation

After Codex changed scope-related code, Claude/Cowork independently reviewed it.

Review output was stored in task-specific files such as:

```text
handoff/cowork_phase0_review.md
handoff/cowork_phase0_1_review.md
```

Reusable lesson:

```text
For high-impact changes, use a second model as an independent reviewer, then let Hermes arbitrate.
```

### Stage 3 — Define Program-Specific Scope Contracts

The project introduced the idea of `programs/<slug>/scope.json` for bug bounty/client/CTF rules.

Implementation order:

```text
P1-1: schema + docs + safe examples only
P1-2: offline validator only
P1-3: future policy decision helper
P1-4: future runtime integration
```

Important constraint:

```text
Do not wire new policy into runtime until schema and offline validation are reviewed.
```

Reusable lesson:

```text
Build contracts before execution. Schema first, validator second, runtime integration later.
```

### Stage 4 — Expand Review From QA To Strategic Architecture Advice

The operator clarified that Claude/Cowork should not only find blocking defects. Reviews should also judge whether changes advance the long-term goal.

The review prompt was updated to ask for:

- architecture fit
- extensibility
- updateability
- modularity
- safe automation
- agent-assisted analysis
- testing and roadmap alignment

Reusable lesson:

```text
Ask reviewers to assess direction, not only correctness.
```

### Stage 5 — Define Post-Scan Agent-Assisted Review

The project decided that scan/module output should not directly become confirmed findings.

Workflow:

```text
scripts/modules produce structured candidate findings and evidence
Hermes verifies scope/run/audit integrity
Claude/Cowork reviews false positives, impact, verification steps, report quality
Codex fixes automation defects
manual verification upgrades candidate to verified
```

Reusable lesson:

```text
Automation produces candidates. Agent/human review turns evidence into decisions.
```

### Stage 6 — Plan A Modular Vulnerability Platform

Codex and Claude/Cowork both recommended moving from monolithic scripts toward a module system.

Target architecture:

```text
scripts/core/
  scope.py
  policy.py
  runner.py
  evidence.py
  finding.py
  report.py

modules/
  _schema/
    module.schema.json
    finding.schema.json
    evidence.schema.json
  checks/
  triage/
  verify/
  profiles/

runs/<run_id>/
  run.json
  audit.log
  evidence/
  findings/
```

Reusable lesson:

```text
Separate stable execution infrastructure from replaceable check/plugin content.
```

### Stage 7 — Add Periodic Third-Party Strategy Review

The project then added a weekly offline review process.

Each scheduled review should create:

```text
handoff/periodic_reviews/YYYY-MM-DD/project_snapshot.md
handoff/periodic_reviews/YYYY-MM-DD/codex_strategy_review.md
handoff/periodic_reviews/YYYY-MM-DD/claude_strategy_review.md
handoff/periodic_reviews/YYYY-MM-DD/hermes_synthesis.md
```

Codex reviews engineering/systematization.
Claude/Cowork reviews strategy/product-security.
Hermes synthesizes both.

Reusable lesson:

```text
Do not only review patches. Periodically review the whole project direction.
```

## Reusable Implementation Recipe For Another Project

### Step 1 — Create Project Context

Create:

```text
.hermes.md
HERMES_WORKFLOW.md
handoff/
```

Minimum `.hermes.md` content:

```text
Project name:
Goal:
Hermes role:
Codex role:
Claude/Cowork role:
Safety gates:
Validation expectations:
Files that must not be modified without approval:
```

### Step 2 — Define Safety Gates

Write down what actions require approval.

Examples:

```text
Cybersecurity: live scans, exploit attempts, fuzzing, callbacks
Finance: live trades, broker API orders, leverage changes
Publishing: public posting, monetization changes, channel config changes
Infrastructure: production deploys, DNS changes, billing changes
Data: external uploads, private dataset processing, irreversible deletion
```

### Step 3 — Establish Handoff Files

Create:

```text
handoff/cowork_proposal.md
handoff/codex_task.md
handoff/codex_review.md
handoff/accepted_changes.md
handoff/latest_check.md
```

Rules:

- `accepted_changes.md` is append-only.
- `codex_task.md` contains constrained implementation tasks.
- `cowork_*_review.md` contains independent review.
- `latest_check.md` stores local verification results.

### Step 4 — Define The Sustained Review Loop

Use this default:

```text
strategy/spec -> implementation -> independent review -> Hermes verification -> accepted history
```

Do not skip independent review for:

- security gates
- scope/risk logic
- data handling
- report integrity
- production deployment logic
- scheduler/background automation
- financial or irreversible actions

### Step 5 — Prefer Contracts Before Runtime

For any new subsystem, use this order:

```text
1. Architecture note
2. Schema / data contract
3. Offline validator
4. Dry-run helper
5. Limited runtime integration
6. Full automation
```

This avoids building unsafe behavior before the rules are clear.

### Step 6 — Make Review Prompts Strategic

Use this prompt add-on:

```text
Do not limit the review to blocking defects. In addition to ACCEPT/ROUTE-BACK, provide third-party recommendations about architecture, extensibility, maintainability, updateability, modularity, safety gates, agent-assisted analysis, testing, and future roadmap alignment. Separate findings into blocking issues, non-blocking improvements, strategic recommendations, architecture fit, safety/scope assessment, testing assessment, and recommended next phase.
```

### Step 7 — Add Periodic Whole-Project Review

Schedule a recurring offline job that:

```text
1. creates a project snapshot
2. asks Codex for engineering/systematization review
3. asks Claude/Cowork for strategy/product-security review
4. asks Hermes to synthesize next actions
```

Important:

```text
The scheduled review should be offline-only and should not perform high-risk project actions.
```

## Generic Directory Template

```text
project-root/
  .hermes.md
  HERMES_WORKFLOW.md
  handoff/
    accepted_changes.md
    codex_task.md
    codex_review.md
    cowork_proposal.md
    latest_check.md
    sustained_review_loop.md
    periodic_reviews/
  scripts/
    core/
  modules/
    _schema/
    checks/
    triage/
    verify/
    profiles/
  runs/
  reports/
  docs/
```

For non-cybersecurity projects, rename `modules/checks/triage/verify` to match the domain, for example:

```text
finance: signals/strategies/execution_gates
content: ideas/drafts/publish_gates
infra: checks/changes/deploy_gates
data: ingest/transform/export_gates
```

## Prompt Templates

### Codex Implementation Prompt

```text
You are Codex implementing a constrained change in this project.
Read .hermes.md and HERMES_WORKFLOW.md first.
Task: <specific task>
Boundaries:
- do not touch <protected files>
- do not perform <high-risk actions>
- keep changes minimal
- add tests/validation where possible
Update handoff/codex_review.md with files changed, validation, risks, and next steps.
```

### Claude/Cowork Review Prompt

```text
You are Claude/Cowork performing independent review.
Read .hermes.md, HERMES_WORKFLOW.md, handoff/codex_review.md, and relevant changed files.
Do not only look for blocking defects.
Write a review with:
- Verdict: ACCEPT or ROUTE BACK
- Blocking issues
- Non-blocking improvements
- Strategic recommendations
- Architecture fit
- Safety/scope assessment
- Testing/validation assessment
- Recommended next phase
```

### Hermes Synthesis Prompt

```text
Compare Codex's implementation notes and Claude/Cowork's review.
Separate blocking from non-blocking items.
Verify locally with safe commands.
Update accepted_changes.md only after validation.
Summarize what changed, what was verified, what remains risky, and the next phase.
```

## Acceptance Checklist For Porting This Workflow

A project has successfully adopted this workflow when:

- [ ] there is a project context file describing roles and safety gates
- [ ] high-risk actions are explicitly gated
- [ ] Codex tasks are constrained and written to files
- [ ] Claude/Cowork reviews are saved as durable files
- [ ] reviews include strategic recommendations, not only blockers
- [ ] Hermes runs local verification before declaring success
- [ ] accepted history is append-only
- [ ] periodic whole-project reviews are scheduled or manually recurring
- [ ] architecture direction is written before major refactors
- [ ] automation outputs remain candidates until reviewed

## Anti-Patterns To Avoid

- Letting one script become the permanent orchestrator for everything.
- Allowing each module/plugin/script to perform its own inconsistent safety checks.
- Treating scanner/tool output as confirmed findings.
- Asking reviewers only whether a change is broken.
- Keeping important decisions only in chat history.
- Creating empty directories without README files explaining intent.
- Scheduling recurring jobs that can perform high-risk actions without fresh approval.
- Updating memory with stale task progress instead of writing project handoff files.

## Minimal Version For Small Projects

If a project is small, start with only:

```text
.hermes.md
handoff/accepted_changes.md
handoff/codex_task.md
handoff/codex_review.md
handoff/cowork_review.md
```

Then use this loop:

```text
Hermes plans -> Codex changes -> Claude reviews -> Hermes verifies -> accepted_changes updated
```

That is enough to get most of the benefit without building the full module/platform structure.

## Current Project-Specific Status At Time Of Writing

Completed:

- Hermes/Codex/Claude role split
- sustained review loop
- scope-hardening review process
- program scope schema P1-1
- offline program scope validator P1-2
- post-scan agent-assisted review workflow
- modular platform architecture direction
- periodic third-party strategy review job
- empty intent directory README hygiene

Next recommended phases:

```text
P1-3: program policy decision helper
P1-4: minimal recon.sh --program integration
P2-1: finding/evidence schemas
P2-2: run manifest / execution ledger
P2-3: module manifest schema
P2-4: dry-run-only module runner skeleton
P2-5: first Level 1 audit modules
```
