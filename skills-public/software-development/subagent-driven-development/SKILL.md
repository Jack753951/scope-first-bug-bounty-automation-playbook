> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: subagent-driven-development
description: "Execute plans via delegate_task subagents (2-stage review)."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, subagent, implementation, workflow, parallel]
    related_skills: [writing-plans, requesting-code-review, test-driven-development]
---

# Subagent-Driven Development

## Overview

Execute implementation plans by dispatching fresh subagents per task with systematic two-stage review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

## When to Use

Use this skill when:
- You have an implementation plan (from writing-plans skill or user requirements)
- Tasks are mostly independent
- Quality and spec compliance are important
- You want automated review between tasks

For project-orchestrator work, the agent owns task splitting and delegation decisions. Do not ask the user to decide every time whether Claude Code, Codex, or another reviewer should be involved. Decide based on whether another agent materially improves quality, catches risk, adds creative/strategy judgment, or creates a useful usage artifact. If you choose to keep a nontrivial slice Hermes-local, label it explicitly and state why delegation would add little value.

Do not overclaim multi-agent participation. In final summaries and handoff artifacts, distinguish Hermes-local work, Hermes `delegate_task` subagents, Claude/Cowork, Claude Code Impl, Codex, and other reviewers as separate routes. If Claude Code or Codex did not run, say so plainly. For users who care about auditability, list route/tool, visible model/runtime if exposed, output artifacts, and which role each route actually performed. `delegate_task` reviewers are useful for fast role-separated review, but they are not equivalent to repo-wrapper Claude Code/Codex runs with usage/result artifacts. When `delegate_task` subagents are used as formal third-party/periodic review evidence, persist each review into a named repo artifact with reviewer identity, context-read attestation, validation, and verdict; otherwise chat-only delegate summaries are not covered by repo-level worker-attestation gates and must be reported as un-gated advisory input.

When a repo relies on multiple agents across sessions, harden memory sync as an engineering contract rather than a prompt convention. Add canonical context entrypoints to worker prompts, require each worker result to attest checked `[x]` reads, worker identity, validation, and verdict, and wire a static checker into the repo review command so present noncompliant artifacts fail review. See `references/worker-memory-sync-attestation.md` for the full pattern and pitfalls.

When the project is primarily an agent-operated research/workflow platform, optimize structure for Hermes/agent capability rather than human-reader presentation. Do not add broad documentation/governance layers just to make the repo look organized; add narrow, machine-checkable substrates with concrete consumers: readiness state, role synthesis, learning seeds, validators, and review gates. For cybersec/live-target workflows, keep engineering readiness distinct from target authorization. See `references/agent-operable-capability-substrate.md` for the pattern.

**vs. manual execution:**
- Fresh context per task (no confusion from accumulated state)
- Automated review process catches issues early
- Consistent quality checks across all tasks
- Subagents can ask questions before starting work

## The Process

### 1. Read and Parse Plan

Read the plan file. Extract ALL tasks with their full text and context upfront. Create a todo list:

```python
# Read the plan
read_file("docs/plans/feature-plan.md")

# Create todo list with all tasks
todo([
    {"id": "task-1", "content": "Create User model with email field", "status": "pending"},
    {"id": "task-2", "content": "Add password hashing utility", "status": "pending"},
    {"id": "task-3", "content": "Create login endpoint", "status": "pending"},
])
```

**Key:** Read the plan ONCE. Extract everything. Don't make subagents read the plan file — provide the full task text directly in context.

### 2. Per-Task Workflow

For EACH task in the plan:

#### Step 1: Dispatch Implementer Subagent

Use `delegate_task` with complete context:

```python
delegate_task(
    goal="Implement Task 1: Create User model with email and password_hash fields",
    context="""
    TASK FROM PLAN:
    - Create: src/models/user.py
    - Add User class with email (str) and password_hash (str) fields
    - Use bcrypt for password hashing
    - Include __repr__ for debugging

    FOLLOW TDD:
    1. Write failing test in tests/models/test_user.py
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)
    3. Write minimal implementation
    4. Run: pytest tests/models/test_user.py -v (verify PASS)
    5. Run: pytest tests/ -q (verify no regressions)
    6. Commit: git add -A && git commit -m "feat: add User model with password hashing"

    PROJECT CONTEXT:
    - Python 3.11, Flask app in src/app.py
    - Existing models in src/models/
    - Tests use pytest, run from project root
    - bcrypt already in requirements.txt
    """,
    toolsets=['terminal', 'file']
)
```

#### Step 2: Dispatch Spec Compliance Reviewer

After the implementer completes, verify against the original spec:

```python
delegate_task(
    goal="Review if implementation matches the spec from the plan",
    context="""
    ORIGINAL TASK SPEC:
    - Create src/models/user.py with User class
    - Fields: email (str), password_hash (str)
    - Use bcrypt for password hashing
    - Include __repr__

    CHECK:
    - [ ] All requirements from spec implemented?
    - [ ] File paths match spec?
    - [ ] Function signatures match spec?
    - [ ] Behavior matches expected?
    - [ ] Nothing extra added (no scope creep)?

    OUTPUT: PASS or list of specific spec gaps to fix.
    """,
    toolsets=['file']
)
```

**If spec issues found:** Fix gaps, then re-run spec review. Continue only when spec-compliant.

#### Step 3: Dispatch Code Quality Reviewer

After spec compliance passes:

```python
delegate_task(
    goal="Review code quality for Task 1 implementation",
    context="""
    FILES TO REVIEW:
    - src/models/user.py
    - tests/models/test_user.py

    CHECK:
    - [ ] Follows project conventions and style?
    - [ ] Proper error handling?
    - [ ] Clear variable/function names?
    - [ ] Adequate test coverage?
    - [ ] No obvious bugs or missed edge cases?
    - [ ] No security issues?

    OUTPUT FORMAT:
    - Critical Issues: [must fix before proceeding]
    - Important Issues: [should fix]
    - Minor Issues: [optional]
    - Verdict: APPROVED or REQUEST_CHANGES
    """,
    toolsets=['file']
)
```

**If quality issues found:** Fix issues, re-review. Continue only when approved.

#### Step 4: Mark Complete

```python
todo([{"id": "task-1", "content": "Create User model with email field", "status": "completed"}], merge=True)
```

### 3. Final Review

After ALL tasks are complete, dispatch a final integration reviewer:

```python
delegate_task(
    goal="Review the entire implementation for consistency and integration issues",
    context="""
    All tasks from the plan are complete. Review the full implementation:
    - Do all components work together?
    - Any inconsistencies between tasks?
    - All tests passing?
    - Ready for merge?
    """,
    toolsets=['terminal', 'file']
)
```

### 4. Verify and Commit

```bash
# Run full test suite
pytest tests/ -q

# Review all changes
git diff --stat

# Final commit if needed
git add -A && git commit -m "feat: complete [feature name] implementation"
```

## Task Granularity

**Each task = 2-5 minutes of focused work.**

Prefer system-level, extensible increments over one-off fixes when operating in product-line automation repos. A good task should add a reusable layer, fixture, schema, validator, gate, or review artifact that future channels/features can reuse. If the immediate request is narrow, still frame the implementation as a small rung in a coherent ladder rather than a disposable script.

**Too big:**
- "Implement user authentication system"

**Too narrow / one-off:**
- "Make this one generated file look OK by hardcoding today's case"

**Right size:**
- "Create User model with email and password fields"
- "Add password hashing function"
- "Create login endpoint"
- "Add JWT token generation"
- "Create registration endpoint"
- "Add a deterministic local preview fixture layer for disabled video-channel pilots"

## Side-Effect-Sensitive Repos

When subagents work in repos that publish content, run schedulers, touch credentials, or perform external actions, add an explicit safety envelope to every implementer/reviewer context:
When subagents work in repos that publish content, run schedulers, touch credentials, or perform external actions, add an explicit safety envelope to every implementer/reviewer context:

- Read the repo's orchestrator docs first (for example `.hermes.md`, `handoff/*workflow*.md`, or equivalent) and quote the relevant safety boundaries in the task context.
- Separate proposal/review work from implementation. If the project uses handoff files, require subagents to update the expected handoff artifacts rather than ad-hoc notes.
- Keep active scheduler, publishing/upload, OAuth/token, credential, and default-visibility changes out of scope unless the user explicitly approved that exact gate.
- Prefer upload-free/local validation for render or pipeline QA; if upstream generation credentials are missing and the target is only downstream rendering, use a deterministic fixture/helper outside active production paths instead of changing privacy or upload behavior.
- Reviewers should flag out-of-scope side effects separately from code quality, even if tests pass.
- For a narrow side-effect-sensitive CLI/path review after local implementation, dispatch a focused safety reviewer with explicit allowed actions: read files, run compile/unit/validate checks only, do not run publish/upload/create/auth/scheduler/OAuth/token/client-secret commands, do not delete runtime data, and return `PASS` or `REQUEST_CHANGES` with concrete blockers only. Verify any claimed PASS yourself with local validation before reporting completion.
- If a delegated reviewer times out or returns no final report, do not treat that as review evidence. Inspect the workspace for partial changes, run the focused checks yourself, report the incomplete review honestly, and decide whether to retry with a narrower reviewer or proceed with a Hermes-local justification.
- For learning-loop or prompt-ingestion work, prefer a second engineering/strategy reviewer when the change affects future generation behavior. However, delegation is not ceremonial: if the slice is small, fully covered by RED/GREEN tests, and the reviewer would add little signal, proceed locally but record the route as `Hermes-local` and explain the decision.
- When multi-agent review or analytics synthesis can feed future production prompts, use a candidate-first promotion artifact: raw reviewer notes stay in review files, Hermes writes a candidate JSON, a deterministic validator promotes it only on success, and production reads only the promoted artifact fail-soft. See `references/learning-artifact-promotion.md`.
- For adversarial/security planning, separate reviewer roles by responsibility instead of asking every reviewer to fill the same generic table. A good split is: adversarial planner proposes realistic paths; boundary engineer compiles proof boundaries and stop-before rules; evidence critic rejects weak/sensitive evidence; Hermes synthesizes disagreements and grants no execution authority without scope/operator gates. If a reviewer returns `REQUEST_CHANGES`, fix the concrete blocker and rerun/replace that review before calling the slice complete.
- For cybersec platform changes that affect schemas/contracts, scheduler or recurring substrates, live-lane boundaries, evidence/report promotion, operator gates, safety policy, or target-execution routing, do not treat strong-agent review as optional polish. Use role-separated review before implementation when feasible, or immediately after the first local slice if the change started Hermes-local: at minimum architecture/spec plus safety/boundary reviewers. If this review was skipped initially, say so plainly, run the missing review, patch concrete blockers, rerun validation, and only then call the slice complete. Safety reviewer `REQUEST_CHANGES` is a blocker until fixed and revalidated.
- For agent-operable cybersec/lab platforms, prioritize capability substrates over human-readable project cleanup: role-conflict synthesis, Kali/noVNC readiness state, and no-finding learning seeds. Treat these as local/offline decision inputs only; readiness is not authorization, learning seeds are not evidence promotion, and third-target/live contact remains blocked until explicit operator scope facts are converted into checked program scope/config artifacts.

### Generated Content / Media Artifact Gates

When a task produces visible artifacts such as draft videos, thumbnails, HTML previews, MP4 fixtures, scripts, prompt packs, or canary candidates, add a lightweight domain-review gate after local technical validation and before public/canary recommendations.

- Keep engineering review with the engineering worker; do not route low-level code correctness to a strategy reviewer just to balance model usage.
- Increase strategy/creative reviewer usage by adding focused artifact checkpoints: hook quality, first-3-second retention, pacing, conflict clarity, comment bait, source/story fit, visual/subtitle support, and channel/brand fit.
- When a media/content review can influence future implementation or phase direction, include an `OSS opportunities` add-on: directly useful tools, worthwhile spikes, unsafe patterns to avoid, and the next safe upload-free experiment. Prefer optional QA tools (OCR/readability, ASR/subtitle alignment, scene/static detection) before renderer rewrites; treat the section as recommendation-only, not authorization to install dependencies or change upload/scheduler/OAuth behavior.
- Use explicit verdicts such as `CANARY`, `REVISE`, or `REJECT`; `CANARY` is never publication permission by itself.
- Route follow-up by issue type: strategy/prompt/script to the domain reviewer, implementation/template/render to engineering, and publication/safety to the orchestrator/user approval gate.
- For upload-free media fixture generators, add path-boundary guardrails in code, not only in docs/manifests: custom `out_dir`, `report_path`, or equivalent write targets must resolve under the approved handoff/artifact root, and tests should prove outside paths are rejected. Independent safety reviewers should treat arbitrary artifact-output paths as a blocker in side-effect-sensitive repos.
- When stock/search assets are selected by policy, inspect the machine-readable provenance/relevance report before visual QA. If accepted assets already include a policy blocker, stop promotion, add a regression test for the exact slipped asset/URL/id, patch the deny/scoring rule, re-run targeted tests/validate, and re-render exactly one local-only artifact to prove the asset is now rejected.
- When a contact sheet or storyboard reveals caption clipping, label overflow, or asset-thumbnail overflow, fix before finalizing and re-run browser/visual QA. Common fixes: reduce MP4 overlay font size, add SVG/HTML word wrapping for long captions, add `flex-wrap`/smaller thumbnails for asset rows, regenerate artifacts, and verify no broken images or layout blockers remain.
- For disabled-only/upload-free artifact tests, avoid importing broad runtime config modules solely to inspect constants when those imports can create runtime directories or touch adjacent state. Prefer static AST/literal parsing for invariants like default privacy, and keep artifact tests free of scheduler/upload/OAuth/runtime-path imports.
- If generated ffprobe JSON or similar probe output includes absolute local filenames, scrub or relativize those fields before writing handoff artifacts so reports are portable and do not leak unnecessary machine paths.
- See `references/content-artifact-review-gates.md` for a reusable checklist and verdict semantics.
- See `references/upload-free-media-rungs.md` for the preferred pattern when a visible media/channel artifact must advance through offline-only rungs with creative review, TDD artifact contracts, safety manifests, browser visual QA, and handoff/Obsidian recording.
- See `references/media-fixture-polish-patterns.md` for the TDD + visual-QA polish loop for upload-free MP4 fixtures: safe-area linters, concrete scenario hooks, deterministic motion evidence, FFmpeg contact strips, footer/caption clipping fixes, and safety-boundary reminders.
- See `references/media-provenance-gate-rungs.md` for local-only stock/search asset provenance gates: inspect accepted/rejected asset evidence before visual QA, turn real false negatives into TDD policy fixes, and re-render one post-fix artifact before promotion.

## Red Flags — Never Do These

- Start implementation without a plan
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed critical/important issues
- Dispatch multiple implementation subagents for tasks that touch the same files
- Make subagent read the plan file (provide full text in context instead)
- Skip scene-setting context (subagent needs to understand where the task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance
- Skip review loops (reviewer found issues → implementer fixes → review again)
- Let implementer self-review replace actual review (both are needed)
- **Start code quality review before spec compliance is PASS** (wrong order)
- Move to next task while either review has open issues

## Handling Issues

### If Subagent Asks Questions

- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

### If Reviewer Finds Issues

- Implementer subagent (or a new one) fixes them
- Reviewer reviews again
- Repeat until approved
- Don't skip the re-review

### If Subagent or CLI Worker Fails, Times Out, or Lacks a Final Report

- Do not assume no work happened. A timed-out subagent or external CLI worker may have already modified files, generated artifacts, or partially updated docs.
- Immediately inspect the workspace for changed/new files and generated outputs before dispatching another implementer.
- Compare partial changes against the original bounded task/spec before editing or widening scope.
- Run the relevant targeted tests/compile checks yourself if the worker timed out after likely implementation work.
- Dispatch a focused reviewer subagent for critical issues (spec, safety, and obvious quality) when partial work appears complete.
- If review finds a narrow issue, patch that issue directly or dispatch a narrow fix subagent; do not restart the whole task unless the workspace is inconsistent.
- In side-effect-sensitive repos, constrain recovery/review actions to safe local inspection, targeted tests, compile checks, repo validate commands, and handoff updates unless the user explicitly authorizes publish/upload/scheduler/auth/credential gates.
- Document the worker command/status, accepted partial changes, Hermes/manual fixes, validation results, and blocked follow-ups in the repo's handoff files.
- Document that the first subagent timed out only as session context; do not encode it as a durable claim that the tool is unreliable.
- Keep worker budget changes local to the run when possible. If a fixture/test/handoff-heavy slice hits a max-turn or timeout boundary, prefer a temporary per-run max-turn/step override or split the slice into smaller rungs before raising repo/global defaults.
- For catalog/schema/fixture compatibility work, reviewers should reject one-way drift checks. Require either a declared single source of truth or exact bidirectional/equality coverage so additions on either side fail until the peer artifact is updated.
- See `references/cli-worker-partial-completion.md` for the full recovery checklist for Claude Code/Codex/OpenCode/repo-wrapper runs.
- See `references/cli-worker-budget-and-drift-locks.md` for turn-budget discipline and static/offline symmetric drift-lock test patterns.

## Efficiency Notes

**Why fresh subagent per task:**
- Prevents context pollution from accumulated state
- Each subagent gets clean, focused context
- No confusion from prior tasks' code or reasoning

**Why two-stage review:**
- Spec review catches under/over-building early
- Quality review ensures the implementation is well-built
- Catches issues before they compound across tasks

**Cost trade-off:**
- More subagent invocations (implementer + 2 reviewers per task)
- But catches issues early (cheaper than debugging compounded problems later)

## Integration with Other Skills

### With writing-plans

This skill EXECUTES plans created by the writing-plans skill:
1. User requirements → writing-plans → implementation plan
2. Implementation plan → subagent-driven-development → working code

### With test-driven-development

Implementer subagents should follow TDD:
1. Write failing test first
2. Implement minimal code
3. Verify test passes
4. Commit

Include TDD instructions in every implementer context.

### With requesting-code-review

The two-stage review process IS the code review. For final integration review, use the requesting-code-review skill's review dimensions.

### With systematic-debugging

If a subagent encounters bugs during implementation:
1. Follow systematic-debugging process
2. Find root cause before fixing
3. Write regression test
4. Resume implementation

## Example Workflow

```
[Read plan: docs/plans/auth-feature.md]
[Create todo list with 5 tasks]

--- Task 1: Create User model ---
[Dispatch implementer subagent]
  Implementer: "Should email be unique?"
  You: "Yes, email must be unique"
  Implementer: Implemented, 3/3 tests passing, committed.

[Dispatch spec reviewer]
  Spec reviewer: ✅ PASS — all requirements met

[Dispatch quality reviewer]
  Quality reviewer: ✅ APPROVED — clean code, good tests

[Mark Task 1 complete]

--- Task 2: Password hashing ---
[Dispatch implementer subagent]
  Implementer: No questions, implemented, 5/5 tests passing.

[Dispatch spec reviewer]
  Spec reviewer: ❌ Missing: password strength validation (spec says "min 8 chars")

[Implementer fixes]
  Implementer: Added validation, 7/7 tests passing.

[Dispatch spec reviewer again]
  Spec reviewer: ✅ PASS

[Dispatch quality reviewer]
  Quality reviewer: Important: Magic number 8, extract to constant
  Implementer: Extracted MIN_PASSWORD_LENGTH constant
  Quality reviewer: ✅ APPROVED

[Mark Task 2 complete]

... (continue for all tasks)

[After all tasks: dispatch final integration reviewer]
[Run full test suite: all passing]
[Done!]
```

## Remember

```
Fresh subagent per task
Two-stage review every time
Spec compliance FIRST
Code quality SECOND
Never skip reviews
Catch issues early
```

**Quality is not an accident. It's the result of systematic process.**

## Scheduled review / cron usage

When a scheduled Hermes cron job claims to perform third-party, deep, or multi-party review, do not let it become single-agent role-play. The cron prompt should explicitly require `delegate_task` with separate reviewer tasks, and the job must have the `delegation` toolset enabled. A good scheduled review packet gives each reviewer the same concise evidence bundle, separates strategy/engineering/safety roles, and requires Hermes to synthesize disagreements into `CONTINUE`, `REVISE`, `PAUSE`, `ESCALATE`, or `BLOCKED`. If delegation is unavailable or reviewer evidence is missing, the final report must say the multi-party review was incomplete rather than over-claiming.

## Further reading (load when relevant)

When the orchestration involves significant context usage, long review loops, or complex validation checkpoints, load these references for the specific discipline:

- **`references/agent-operable-capability-substrate.md`** — Pattern for projects whose primary audience is Hermes/agents rather than human readers: use narrow machine-checkable role synthesis, Kali/noVNC readiness state, and no-finding learning seed substrates; avoid documentation/governance reshuffles that do not improve agent capability. Load when a repo is being hardened toward live-target/security workflow checkpoints.
- **`references/worker-memory-sync-attestation.md`** — Repo-level hardening pattern for multi-agent memory sync: required context entrypoints, checked read attestations, worker identity/validation/verdict contracts, enforcing review gates, legacy artifact archival, and regression tests. Load when a project wants Claude/Codex/Cowork/Hermes collaboration to be auditable across sessions.
- **`references/role-separated-adversarial-planning.md`** — Role split for adversarial/security planning reviews: adversarial planner, boundary engineer, evidence critic, and Hermes synthesis with explicit forbidden side effects and REQUEST_CHANGES handling.
- **`references/learning-artifact-promotion.md`** — Candidate-first schema/validator pattern for learning-loop or multi-review synthesis outputs that later feed production prompts. Load when reviewer/analytics output can become machine-readable generation guidance.
- **`references/context-budget-discipline.md`** — Four-tier context degradation model (PEAK / GOOD / DEGRADING / POOR), read-depth rules that scale with context window size, and early warning signs of silent degradation. Load when a run will clearly consume significant context (multi-phase plans, many subagents, large artifacts).
- **`references/gates-taxonomy.md`** — The four canonical gate types (Pre-flight, Revision, Escalation, Abort) with behavior, recovery, and examples. Load when designing or reviewing any workflow that has validation checkpoints — use the vocabulary explicitly so each gate has defined entry, failure behavior, and resumption rules.
- **`references/cli-worker-partial-completion.md`** — Recovery checklist for external CLI worker runs (Claude Code, Codex CLI, OpenCode, repo wrapper scripts) that time out, hit max turns, or leave partial changes without a final report. Load before restarting a worker so useful partial changes are not overwritten.
- **`references/cli-worker-budget-and-drift-locks.md`** — Per-run worker budget discipline plus symmetric drift-lock patterns for schema/catalog/fixture vocabulary compatibility. Load when a rich offline slice hits max turns, or when reviewers need to prove two artifacts cannot silently drift.

References adapted from gsd-build/get-shit-done where noted (MIT © 2025 Lex Christopherson); CLI-worker notes are Hermes-local.
