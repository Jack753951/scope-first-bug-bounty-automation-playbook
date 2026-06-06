> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: test-driven-development
description: "TDD: enforce RED-GREEN-REFACTOR, tests before code."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [testing, tdd, development, quality, red-green-refactor]
    related_skills: [systematic-debugging, writing-plans, subagent-driven-development]
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (ask the user first):**
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## Media/visual artifact review loop

When TDD is applied to generated-media renderers or visual samples, treat reviewer findings as new RED requirements before patching:

- If a reviewer/user flags a visual rule mismatch (for example, "spec says no boxes but rendered text still has backplates"), add or tighten a test that represents the rule at the renderer/spec level before fixing.
- Use tests for durable invariants: movement must have a story reason, text policy flags must forbid boxes/backplates, review packets must enforce reference-first order, and safety booleans must remain closed.
- Do not overfit tests to one screenshot's pixels unless pixel-level regression is the actual contract; prefer schema/spec invariants plus a fresh contact-sheet or vision review for visual judgment.
- After the fix, rerender the artifact and run the same reviewer/vision recheck so the test does not become a paper-only pass.

## Red-Green-Refactor Discipline

### RED — Write Failing Test

For legacy codebases without pytest, use the existing test runner (`unittest`, project scripts, or wrapper commands) rather than adding a new test framework just to satisfy TDD. The important invariant is still RED-GREEN-REFACTOR: create a focused regression test, run it and watch it fail for the expected reason, then implement the smallest fix.

When an independent review returns `REQUEST_CHANGES`, turn each blocker into a focused RED regression test before patching the code. This is especially important for security-boundary gaps that "almost" pass existing tests, such as a CLI rejecting `--target` but still accepting positional target-like arguments. Run the new test to confirm the blocker is reproduced, patch the smallest behavior, then rerun focused tests plus the adjacent suite. For validators and contract helpers, isolate each fail-closed branch in its own test or subtest: do not let an early metadata/schema mismatch prevent hook-length, narration-length, keyword-count, path, or other later branches from being exercised.

When debugging CLI startup/import problems, a good RED test can assert that importing the CLI entrypoint does not import command-specific heavy modules. Patch `builtins.__import__` in the test to fail if modules like `pipeline`, `youtube_api`, cloud SDK wrappers, or ML/media runtime modules are imported at entrypoint import time; then implement lazy imports inside the commands that actually need them.

Write one minimal test showing what should happen.

**Good test:**
```python
def test_retries_failed_operations_3_times():
    attempts = 0
    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception('fail')
        return 'success'

    result = retry_operation(operation)

    assert result == 'success'
    assert attempts == 3
```
Clear name, tests real behavior, one thing.

**Bad test:**
```python
def test_retry_works():
    mock = MagicMock()
    mock.side_effect = [Exception(), Exception(), 'success']
    result = retry_operation(mock)
    assert result == 'success'  # What about retry count? Timing?
```
Vague name, tests mock not real code.

**Requirements:**
- One behavior per test
- Clear descriptive name ("and" in name? Split it)
- Real code, not mocks (unless truly unavoidable)
- Name describes behavior, not implementation

### Verify RED — Watch It Fail

**MANDATORY. Never skip.**

```bash
# Use terminal tool to run the specific test
pytest tests/test_feature.py::test_specific_behavior -v
```

Confirm:
- Test fails (not errors from typos)
- Failure message is expected
- Fails because the feature is missing

**Test passes immediately?** You're testing existing behavior. Fix the test.

**Test errors?** Fix the error, re-run until it fails correctly.

### GREEN — Minimal Code

Write the simplest code to pass the test. Nothing more.

**Good:**
```python
def add(a, b):
    return a + b  # Nothing extra
```

**Bad:**
```python
def add(a, b):
    result = a + b
    logging.info(f"Adding {a} + {b} = {result}")  # Extra!
    return result
```

Don't add features, refactor other code, or "improve" beyond the test.

**Cheating is OK in GREEN:**
- Hardcode return values
- Copy-paste
- Duplicate code
- Skip edge cases

We'll fix it in REFACTOR.

### Verify GREEN — Watch It Pass

**MANDATORY.**

```bash
# Run the specific test
pytest tests/test_feature.py::test_specific_behavior -v

# Then run ALL tests to check for regressions
pytest tests/ -q
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix the code, not the test.

**Other tests fail?** Fix regressions now.

### REFACTOR — Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers
- Simplify expressions

Keep tests green throughout. Don't add behavior.

**If tests fail during refactor:** Undo immediately. Take smaller steps.

### Repeat

Next failing test for next behavior. One cycle at a time.

## Why Order Matters

**"I'll write tests after to verify it works"**

Tests written after code pass immediately. Passing immediately proves nothing:
- Might test the wrong thing
- Might test implementation, not behavior
- Might miss edge cases you forgot
- You never saw it catch the bug

Test-first forces you to see the test fail, proving it actually tests something.

**"I already manually tested all the edge cases"**

Manual testing is ad-hoc. You think you tested everything but:
- No record of what you tested
- Can't re-run when code changes
- Easy to forget cases under pressure
- "It worked when I tried it" ≠ comprehensive

Automated tests are systematic. They run the same way every time.

**"Deleting X hours of work is wasteful"**

Sunk cost fallacy. The time is already gone. Your choice now:
- Delete and rewrite with TDD (high confidence)
- Keep it and add tests after (low confidence, likely bugs)

The "waste" is keeping code you can't trust.

**"TDD is dogmatic, being pragmatic means adapting"**

TDD IS pragmatic:
- Finds bugs before commit (faster than debugging after)
- Prevents regressions (tests catch breaks immediately)
- Documents behavior (tests show how to use code)
- Enables refactoring (change freely, tests catch breaks)

"Pragmatic" shortcuts = debugging in production = slower.

**"Tests after achieve the same goals — it's spirit not ritual"**

No. Tests-after answer "What does this do?" Tests-first answer "What should this do?"

Tests-after are biased by your implementation. You test what you built, not what's required. Tests-first force edge case discovery before implementing.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to the test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for the code you touch. |

## Red Flags — STOP and Start Over

If you catch yourself doing any of these, delete the code and restart with TDD:

- Code before test
- Test after implementation
- Test passes immediately on first run
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Production-Risk / Upload-Free Integration Pattern

For workflows where the real command could publish, upload, mutate scheduler/OAuth state, switch an active production config, or touch security targets, keep the TDD cycle around a narrow offline/opt-in path before running any expensive/local artifact generation:

1. Write a RED test for the safety boundary first: the override must require an explicit target (for example `--channel`) or committed fixture input, must fail closed when ambiguous, and must not edit persistent config files.
2. Add a RED test that the opt-in value reaches the in-memory object the downstream code actually consumes.
3. For security/offline triage pipelines, prefer a fixture-only end-to-end smoke harness before live/runtime wiring: chain existing pure helpers in memory, assert every stage status is `ok`, summarize cross-stage counts, and assert promoted states/words (for example confirmed/verified/reportable) never appear as JSON string values.
4. Add fail-closed RED tests for upstream stage errors: later-stage artifacts should not be produced after an earlier stage returns `status: error`.
5. Add CLI safety RED tests before implementation: reject positional arguments and live-target flags such as `--target`, `--url`, `--host`, `--scope`, and `--live` with structured JSON and non-zero exit.
6. For generated security/lab wrappers, RED tests should cover both the generator and the safety contract before implementation: plan-only JSON, refusal without explicit lab approval, public-target fail-closed behavior, candidate-only language, generated script `bash -n`, parser output shape, and artifact manifest expectations.
7. Add a regression test for review metadata that future agents need (for example preserving optional cards/provenance into `metadata.json`), not just for the rendered artifact.
7. When a local artifact fails creative review due source/footage fit, test the policy layer rather than the network provider: assert preferred terms, deny terms, dropped terms, and a local provenance report (for example `footage_relevance_report.json`) are produced without depending on real API calls.
8. Only after GREEN should you run the upload-free/local command and then run visual, artifact, or adjacent-chain QA.
9. Record the local artifact path, metadata path, relevance/provenance report path, QA verdict, validation commands, and safety statement in the project handoff files.

Pitfall: if a generated local artifact passes render QA but drops review metadata, future review agents lose the contract/provenance. Add a metadata-preservation test before treating the phase as complete.

Pitfall: do not add network/API-dependent tests for stock-footage quality. Mock failed downloads and verify the local selection plan/report still captures preferred search terms, deny motifs, and selected paths when available.

For security fixture-only cybersec slices, use `references/security-fixture-review-tdd.md`: write RED tests for exact fixture presence, schema validation, synthetic/redacted origin, deterministic offline workflow output, non-promotional status vocabulary, and edge-case survival (for example duplicate candidates with distinct notional sources) before adding fixtures. After independent review, convert any `REQUEST_CHANGES` blocker into a focused regression test before patching.

For live-bounty or authorized-target orchestration substrate work, tests should cover machine-readable state and evidence behavior before implementation: queue entries with missing `state_file` must fail closed, lane state must separate `next_operator_action` from `next_autonomous_action`, evidence schemas must reject unreviewed promotional labels, and redaction tools must redact their own findings output rather than printing raw tokens/cookies/emails/OTP-like lines. After an independent review returns `REQUEST_CHANGES`, convert each blocker into a focused regression before patching; this is especially important for queue coherence and evidence-promotion/redaction hygiene.

For authorized live-target or bug-bounty dry-run gate hardening, use `references/security-live-target-gate-hardening.md`: write RED CLI regressions for exact in-scope dry-run pass, out-of-scope fail, local-lab entries such as `localhost`, malformed/path-like program slugs, `--skip-scope-check` incompatibility with program policy, `--policy-mode dry-run` requiring `--dry-run`, and `--policy-mode` without `--program`. After GREEN, run a lightweight post-proof/post-bundle consolidation checklist so accepted changes, navigation, active queue, project notes, and proof-library/live-bounty bridge indexes are updated without auto-promoting candidates or authorizing live automation.

For cybersecurity lab work where a useful external tool/script has been tried once, use `references/security-external-tool-adapter-rungs.md`: promote valuable one-off lab scripts into committed/tested adapters or runners. Keep execution planning separate from offline output import, require fail-closed RED tests for scope/tool/limit/health gates, and ensure imported tool observations never auto-promote to confirmed/verified/reportable findings. If the user emphasizes project modularization or asks whether a new tool/script was retained, treat that as a workflow requirement: do not stop at a local helper or handoff note; extract the reusable capability into a family-level module, fixtures, tests, and accepted-change documentation.

For follow-on security fixture regression-hardening slices, use `references/security-fixture-terminal-state-matrix.md`: after fixtures already run end-to-end, add a RED test for a missing per-finding expectation matrix, then bind every synthetic finding to exact packet/gap/plan/gate terminal states and required gap-code subsets. Keep this test-only unless a separate direction review authorizes consumer behavior changes.

For offline security dry-run bridge follow-ups, use `references/security-dry-run-bridge-followup.md`: convert review recommendations such as hash-drift/tampered copied artifact coverage or test-only helper comments into RED regressions, keep changes tests/comment/handoff-only, assert fail-closed/no-plan/no-execution-leakage behavior, and update active handoff so completed recommendations do not remain queued.

For existing-artifact upload paths (for example private canary upload of a reviewed local MP4), use the checklist in `references/safety-sensitive-existing-artifact-upload.md`: test lock protection, exact artifact+metadata inputs, no generation calls, explicit approval phrase, destination guard, strict pre-upload QA, private/no-schedule upload arguments, and partial-failure recovery before implementation.

For generated-media readability rungs, turn the visual-review complaint into a focused RED test before rerendering. Examples: a hook-specific cleaner must preserve meaningful punctuation before FFmpeg escaping (`Mom texts: are you mad?` → `Mom texts\: are you mad?` at the drawtext layer), and overlay/card filters should assert concrete readability properties such as scrim opacity, border strength, and font sizes. Render the MP4 and frame strip only after GREEN; visual QA then verifies the artifact, not the implementation guess.

For generated-media subtitle/audio alignment complaints, do not assume matching video/audio duration means captions are aligned. Add RED tests for an opt-in path that preserves the script text while using real word timings/forced-alignment timestamps, then add a second regression that the affected production/main render path actually opts into that behavior. A passing helper or one-off rerender script is not enough if `create_short(...)` or the channel's default pipeline still uses average-distributed captions. Rerender upload-free before any public/private replacement action, and require timing evidence for the exact artifact before upload/schedule. See `references/generated-media-subtitle-alignment.md` for the reusable regression and QA pattern.

For generated-media reference-only template rungs, when the user provides downloaded/competitor/public examples for architecture/template learning, test the boundary before rendering: examples stay internal-reference-only, generated output stays `production_ready=false`, reference files are not ingested, literal frames/captions/audio/SFX/IP/watermarks are forbidden, and the renderer extracts only abstract structure such as duration band, hard-cut beat count, locked title band, sub-caption hierarchy, persona staircase, short pause, and final payoff card. Generate upload-free output only after GREEN, then run media QA plus contact-sheet review and write a decision artifact naming the next safe gate. See `references/generated-media-reference-only-template-rungs.md`.

When a generated-media structural template is accepted but needs original/licensed replacement assets before production, keep TDD on the sourcing gate: create a manifest/checklist step that proves every asset category defaults to `production_ready=false`, candidate packs remain quarantined, license/source/hash/Content-ID fields are required, and `upload_authorized=false` / `channel_activation=false` stay true until a separate explicit gate. See `references/generated-media-replacement-asset-manifest.md`.

For channelized AI prompt / rewrite policy work, test the policy boundary, not only the final artifact. First write RED tests that the channel engine passes an explicit `prompt_policy` / `rewrite_policy` payload into the shared pipeline helper, including family metadata, hook spec, narration spec, and safety/creative rules. Add a direct prompt-capture test for the shared helper to prove those specs/rules are embedded in the LLM prompt. If one channel disables or changes a validator inherited from another channel (for example true-scary stories disabling a drama-style antagonist cold-open repair), add paired tests: the target channel opts out and the original channel still opts in. Keep default helper behavior backward-compatible and tested so legacy/direct callers remain fail-safe.

For modular engine/provider/render contracts, add a versioned metadata rung before relying on downstream QA. Write RED tests that the metadata helper attaches a single-source contract version without mutating input, strict validators require it, fixture validators fail closed on version drift, and final artifact metadata preserves it for reviewers/canary packets. Keep the change narrow: update active fixtures and validators without touching publish/upload/scheduler/OAuth/default-privacy behavior. See `references/metadata-contract-rungs.md` for the reusable checklist.

For media automation profile labels, use staged TDD rungs: closed data-only registry first, optional output-metadata passthrough second, and read-only QA report display third. Labels such as `asset_profile`, `render_profile`, and `qa_profile` are review context only until a later reviewed plan explicitly authorizes behavioral use; they must not affect asset selection, rendering, QA PASS/FAIL, upload/publication, scheduler, OAuth, destination, privacy, or channel config. See `references/media-profile-label-rungs.md` for the reusable pattern.

For generated-media profile labels (asset/render/QA profiles), use phased TDD rungs rather than wiring behavior immediately: (A) add a closed, versioned, data-only registry with fail-closed tests for unknown channels/fields and activation terms such as upload, publish, privacy, scheduler, OAuth, token, and destination; (B) add RED/GREEN tests proving output metadata preserves optional profile labels only when supplied and does not invent them when absent; (C) only then add read-only QA/report display labels. At every rung, verify labels do not drive asset search, renderer behavior, QA pass/fail, canary/publication scoring, upload, scheduler, OAuth, channel config, or runtime media mutation, and update handoff with RED/GREEN evidence plus safety validation.

For upstream YouTube/topic-intelligence repos, avoid making low-risk metadata and planning work as heavy as production upload work. Use TDD to add a medium-gate creative conversion layer before more collectors when the bottleneck is candidate quality: candidate packets -> originalized concept packets with hooks, meme/animal icon staging, proof-card needs, visual beats, and SFX ideas; or YouTube watchlist market patterns -> original, proof-object-seeking candidate hypotheses. When the upstream repo serves a multi-channel main project, add RED tests that helper profile/config examples mirror the main project's real channel registry names, fail closed for unknown channels, preserve legacy first-lane fields only where needed, and expose generic fields for other channels. RED tests should prove source titles/bodies are not copied into generated creative copy, rejects/sensitive watchlist patterns are filtered, CLI writes JSON+Markdown only, and substring classifiers use token matching (for example `release` must not become `lease`, and a legal/mechanic `pay` request must not become workplace/payroll). Keep strict gates for actual script/render/upload/scheduler/OAuth/channel-config workflows. See `references/upstream-topic-intelligence-creative-concepts.md`.

For upstream accountless demand/search-signal rungs, test that autocomplete/search suggestions are metadata-only demand indicators, not story sources. RED tests should cover parser payloads, row shape (`search_suggest` / `youtube_autocomplete`), reference-only `search://...` URLs, explicit risk flags such as `not a story source`, CLI seed-query config/overrides, source counts, and later deduplication/query-family grouping before allowing broad suggestions to crowd out concrete story candidates. See `references/upstream-topic-intelligence-demand-signals.md`.

For upstream topic-intelligence repos that must serve a multi-channel downstream system, add a channel-profile abstraction rung before adding more first-lane-specific transforms. RED tests should prove profile config is data-driven, unknown channels fail closed, non-legacy channels use generic `channel_fit`, legacy lanes preserve compatibility fields only through explicit profile metadata, and novelty/history paths resolve by channel. Keep the change metadata-only: no script/render/upload/scheduler/OAuth/token/privacy/channel-config side effects. See `references/upstream-topic-intelligence-channel-profiles.md`.

For upstream topic-intelligence repos feeding a downstream media generator/publisher, model each human/planning handoff as its own audited decision layer. Use TDD to prove source-status fail-closed behavior, enumerated decisions, JSON+Markdown outputs, and that any approval authorizes only the next named review gate while script/render/upload/scheduler/OAuth/token/channel-config/competitor-asset actions remain blocked. This is especially important for candidate -> concept/design gate -> request-more-objects -> synthetic object specs -> specs-review decision chains. See `references/upstream-topic-intelligence-planning-gates.md`.

For docs/template generators and periodic-review packet builders, test the generated output before implementation. Add RED tests that snapshots/prompts/templates contain freshness/authority metadata, project-specific review tiers, reviewer identity/model fields, and final decision/output-schema blocks; then implement the smallest generator change and smoke-run the real builder. Keep primary and fallback generators aligned. See `references/template-review-packet-tdd.md`.

For delegated-agent wrapper prompt plumbing, test the exact prompt construction path before implementation using fake worker binaries that capture prompts instead of calling real LLM CLIs. RED tests should prove compact current-route/strategy/Obsidian-project/accepted-change entrypoints are injected before task bodies, safety footers remain present where required, and the wrapper does not dump whole vaults by default. See `references/worker-prompt-context-injection-tdd.md`.

For media automation multi-agent learning loops, keep long-horizon review as learning synthesis rather than a new production safety gate. Add repo bridge files so Claude Code/Codex-style workers can read project goals and Obsidian-style notes, split reviewers by role, and TDD the promoted-learning ingestion boundary so production reads only Hermes-synthesized `promoted_rules`-style artifacts. See `references/youtube-agent-multi-agent-learning-loop.md`.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the wished-for API. Write the assertion first. Ask the user. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify the design. |

## Hermes Agent Integration

### Running Tests

Use the `terminal` tool to run tests at each step:

```python
# RED — verify failure
terminal("pytest tests/test_feature.py::test_name -v")

# GREEN — verify pass
terminal("pytest tests/test_feature.py::test_name -v")

# Full suite — verify no regressions
terminal("pytest tests/ -q")
```

### With delegate_task

When dispatching subagents for implementation, enforce TDD in the goal:

```python
delegate_task(
    goal="Implement [feature] using strict TDD",
    context="""
    Follow test-driven-development skill:
    1. Write failing test FIRST
    2. Run test to verify it fails
    3. Write minimal code to pass
    4. Run test to verify it passes
    5. Refactor if needed
    6. Commit

    Project test command: pytest tests/ -q
    Project structure: [describe relevant files]
    """,
    toolsets=['terminal', 'file']
)
```

### With systematic-debugging

Bug found? Write failing test reproducing it. Follow TDD cycle. The test proves the fix and prevents regression.

Never fix bugs without a test.

### Safety-sensitive scheduled uploads

For existing-artifact scheduled upload paths, add RED tests for malformed, timezone-naive, and past `publishAt` values before any DB insert or API side effect. See `references/scheduled-upload-publishat-validation.md`.

## Anti-Patterns

- **Testing mock behavior instead of real behavior** — mocks should verify interactions, not replace the system under test
- **Testing implementation details** — test behavior/results, not internal method calls
- **Happy path only** — always test edge cases, errors, and boundaries
- **Brittle tests** — tests should verify behavior, not structure; refactoring shouldn't break them

## Related references

- `references/security-external-tool-adapter-rungs.md` — use when a cybersecurity lab session turns a useful external recon/scanner script or tool into reusable project capability: TDD safety tests, bounded local-lab runner, offline importer, fixtures, handoff, and non-promotional observation gates.
- `references/security-fixture-review-tdd.md` — use for fixture-only security/cybersec slices that need RED tests, synthetic/redacted fixture guards, deterministic offline workflow checks, and independent-review blocker regression tests.
- `references/security-dry-run-bridge-followup.md` — use for offline security dry-run bridge review follow-ups: tampered copied artifact/hash-drift negative coverage, test-only helper comment regressions, fail-closed/no-plan/no-execution-leakage assertions, and compact handoff closure.
- `references/security-live-target-gate-hardening.md` — use when authorized live-target/bug-bounty dry-runs expose scope/program gate compatibility issues or require post-proof/post-bundle consolidation without authorizing live automation.
- `references/safety-sensitive-existing-artifact-upload.md` — use for private-only existing-artifact uploads.
- `references/template-review-packet-tdd.md` — use for docs/template generators, periodic-review packet builders, prompt generators, and fallback template paths; includes RED tests for generated freshness/authority, review-tier, reviewer-identity, and final-decision blocks.
- `references/worker-prompt-context-injection-tdd.md` — use for delegated-agent wrapper prompt construction: fake worker CLIs capture prompts so RED tests prove compact context-entrypoint injection, task-body order, safety footer preservation, and no full-vault dump by default.
- `references/upstream-topic-intelligence-channel-profiles.md` — use when an upstream topic radar must become multi-channel: data-only channel profiles, fail-closed unknown channels, generic vs legacy score fields, and channel-aware novelty/history routing.
- `references/generated-media-reference-only-template-rungs.md` — use when downloaded/competitor/public examples are allowed only as architecture/template references: RED tests for internal-reference-only policy, no literal reuse, no reference-file ingestion, structure extraction, upload-free generation, media QA, contact-sheet review, and next-gate documentation.
- `references/generated-media-replacement-asset-manifest.md` — use after a generated-media structural template is accepted but production requires original/licensed replacements: manifest/checklist TDD for asset categories, quarantine, license/source/hash/Content-ID fields, and no upload/channel activation.
- `references/media-profile-registry-tdd.md` — use for generated-media asset/render/QA profile registries: data-only closed mappings first, fail-closed side-effect vocabulary, then metadata/report labels in later rungs.
- `references/media-pipeline-proof-card-tdd.md` — use for media pipeline visual/metadata regressions: write deterministic proof-card/metadata tests first, keep code implementation separate from rerender/upload gates, and verify with focused tests plus project validation.

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without the user's explicit permission.
