> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: writing-plans
description: "Write implementation plans: bite-sized tasks, paths, code."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [planning, design, implementation, workflow, documentation]
    related_skills: [subagent-driven-development, test-driven-development, requesting-code-review]
---

# Writing Implementation Plans

## Overview

Write comprehensive implementation plans assuming the implementer has zero context for the codebase and questionable taste. Document everything they need: which files to touch, complete code, testing commands, docs to check, how to verify. Give them bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume the implementer is a skilled developer but knows almost nothing about the toolset or problem domain. Assume they don't know good test design very well.

**Core principle:** A good plan makes implementation obvious. If someone has to guess, the plan is incomplete.

## When to Use

**Always use before:**
- Implementing multi-step features
- Breaking down complex requirements
- Delegating to subagents via subagent-driven-development

**Also use for direction-review prompts before implementation when:**
- The next step could expand safety, runtime, platform, schema, or production boundaries
- A refactor seems tempting but may be premature
- The right answer may be "defer and close out the phase" rather than "write code"
- A reviewer must choose among explicit verdicts before any implementation begins

See `references/safety-gated-direction-review-prompts.md` for a reusable prompt pattern.
See `references/return-to-mainline-direction-reviews.md` for the pattern where a long offline/review/UX line should pause and ask whether to return to the main platform/runtime-policy line before adding another artifact.
See `references/safety-gated-no-runtime-code-rung-plans.md` for the pattern where a design-only/project-phase artifact should become an actionable TDD plan while implementation remains unexecuted until the user explicitly chooses the code rung.
See `references/phase-closeout-milestone-checkpoints.md` for the pattern where a long offline/design/review phase should be closed as a checkpoint while explicitly preserving higher-risk activation gates.
See `references/source-fit-planning-rungs.md` for generated-media/content projects where the next safest action is a no-generation candidate scorecard rather than another render or implementation rung.
See `references/generated-media-remediation-rungs.md` for generated-media projects where a controlled local artifact renders but fails visual QA/proof-object review and needs a plan-only remediation rung before code, rerender, or upload.

**Don't skip when:**
- Feature seems simple (assumptions cause bugs)
- You plan to implement it yourself (future you needs guidance)
- Working alone (documentation matters)

## Bite-Sized Task Granularity

**Each task = 2-5 minutes of focused work.**

Every step is one action:
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

**Too big:**
```markdown
### Task 1: Build authentication system
[50 lines of code across 5 files]
```

**Right size:**
```markdown
### Task 1: Create User model with email field
[10 lines, 1 file]

### Task 2: Add password hash field to User
[8 lines, 1 file]

### Task 3: Create password hashing utility
[15 lines, 1 file]
```

## Plan Document Structure

### Header (Required)

Every plan MUST start with:

```markdown
# [Feature Name] Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

### Task Structure

Each task follows this format:

````markdown
### Task N: [Descriptive Name]

**Objective:** What this task accomplishes (one sentence)

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:45-67` (line numbers if known)
- Test: `tests/path/to/test_file.py`

**Step 1: Write failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify failure**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: FAIL — "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify pass**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Writing Process

### Step 1: Understand Requirements

Read and understand:
- Feature requirements
- Design documents or user description
- Acceptance criteria
- Constraints

### Step 2: Explore the Codebase

Use Hermes tools to understand the project:

```python
# Understand project structure
search_files("*.py", target="files", path="src/")

# Look at similar features
search_files("similar_pattern", path="src/", file_glob="*.py")

# Check existing tests
search_files("*.py", target="files", path="tests/")

# Read key files
read_file("src/app.py")
```

### Step 3: Design Approach

Decide:
- Architecture pattern
- File organization
- Dependencies needed
- Testing strategy

### Step 4: Write Tasks

Create tasks in order:
1. Setup/infrastructure
2. Core functionality (TDD for each)
3. Edge cases
4. Integration
5. Cleanup/documentation

### Step 5: Add Complete Details

For each task, include:
- **Exact file paths** (not "the config file" but `src/config/settings.py`)
- **Complete code examples** (not "add validation" but the actual code)
- **Exact commands** with expected output
- **Verification steps** that prove the task works

### Step 6: Review the Plan

Check:
- [ ] Tasks are sequential and logical
- [ ] Each task is bite-sized (2-5 min)
- [ ] File paths are exact
- [ ] Code examples are complete (copy-pasteable)
- [ ] Commands are exact with expected output
- [ ] No missing context
- [ ] DRY, YAGNI, TDD principles applied

### Step 7: Save the Plan

```bash
mkdir -p docs/plans
# Save plan to docs/plans/YYYY-MM-DD-feature-name.md
git add docs/plans/
git commit -m "docs: add implementation plan for [feature]"
```

## Principles

### DRY (Don't Repeat Yourself)

**Bad:** Copy-paste validation in 3 places
**Good:** Extract validation function, use everywhere

### YAGNI (You Aren't Gonna Need It)

**Bad:** Add "flexibility" for future requirements
**Good:** Implement only what's needed now

```python
# Bad — YAGNI violation
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.preferences = {}  # Not needed yet!
        self.metadata = {}     # Not needed yet!

# Good — YAGNI
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

### TDD (Test-Driven Development)

Every task that produces code should include the full TDD cycle:
1. Write failing test
2. Run to verify failure
3. Write minimal code
4. Run to verify pass

See `test-driven-development` skill for details.

### Frequent Commits

Commit after every task:
```bash
git add [files]
git commit -m "type: description"
```

### Safety-Gated No-Runtime Plans

When the safest next step is an implementation plan rather than implementation, make that boundary explicit:

- state that the artifact is a plan and code/runtime behavior remains unexecuted;
- list activation surfaces that remain forbidden without fresh explicit approval;
- inspect enough code to name exact future files/functions/tests;
- include RED/GREEN TDD steps for the future code rung;
- update project handoff so future agents know the plan exists but is not approval to execute it.

Use this especially for projects with upload, scheduler, OAuth, privacy, external-side-effect, or production activation gates. See `references/safety-gated-no-runtime-code-rung-plans.md`.

#### Continuous-engineering sequencing pitfall

For recurring/scheduled platform work, do not plan "full automation" as the first rung. First plan a controllable substrate:

1. Make state contracts validator-valid and fail-closed.
2. Produce offline/passive candidate records and operator-inbox decisions in dry-run/no-target mode.
3. Only after an end-to-end inbox signal works, add hourly/daily recurring jobs with explicit policy, scope, technique, rate/budget, and stop-before gates.
4. Keep live target-touching work single-lane by default; background detectors should feed the inbox, not hijack the active lane.
5. Treat capability-library work as support for active lanes or recurring substrate, not as a substitute for evidence/report progress.

This is the planning pattern for avoiding "continuous engineering" turning into multi-lane automation drift.

### Source-Fit Planning Rungs

When the previous phase closed an engineering/review loop and the safest next move is better candidate selection, write a source-fit planning rung instead of generating another artifact. The plan should define a scoring packet, hook/readiness criteria, brand-risk blockers, visual/proof-object feasibility, and a `PASS_TO_SCRIPT_PROMPT / HOLD_FOR_REVIEW / BLOCK` decision. It must also say that a pass is not generation/upload approval and that future generation still needs explicit user authorization. See `references/source-fit-planning-rungs.md`.

### Generated-Media Remediation Rungs

When a local/controlled media artifact renders but fails visual QA, proof-object clarity, subtitle legibility, or brand-safety review, do not blindly rerender. Write a plan-only remediation rung first: cite exact artifacts, map blockers to acceptance criteria, inspect code enough to name future files/functions/tests, split plan/code/rerender/upload gates, and use a read-only creative/engineering review before implementation when the issue is visual and code-adjacent. See `references/generated-media-remediation-rungs.md`.

## Common Mistakes

### Vague Tasks

**Bad:** "Add authentication"
**Good:** "Create User model with email and password_hash fields"

### Incomplete Code

**Bad:** "Step 1: Add validation function"
**Good:** "Step 1: Add validation function" followed by the complete function code

### Missing Verification

**Bad:** "Step 3: Test it works"
**Good:** "Step 3: Run `pytest tests/test_auth.py -v`, expected: 3 passed"

### Missing File Paths

**Bad:** "Create the model file"
**Good:** "Create: `src/models/user.py`"

## Execution Handoff

After saving the plan, offer the execution approach:

**"Plan complete and saved. Ready to execute using subagent-driven-development — I'll dispatch a fresh subagent per task with two-stage review (spec compliance then code quality). Shall I proceed?"**

When executing, use the `subagent-driven-development` skill:
- Fresh `delegate_task` per task with full context
- Spec compliance review after each task
- Code quality review after spec passes
- Proceed only when both reviews approve

## Remember

```
Bite-sized tasks (2-5 min each)
Exact file paths
Complete code (copy-pasteable)
Exact commands with expected output
Verification steps
DRY, YAGNI, TDD
Frequent commits
```

**A good plan makes implementation obvious.**
