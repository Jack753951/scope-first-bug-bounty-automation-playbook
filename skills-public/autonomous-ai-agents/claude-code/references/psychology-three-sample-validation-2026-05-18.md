> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Psychology Insight Three-Sample Validation Pattern (2026-05-18)

Use this as a concrete example for future youtube_agent upload-free script-engine pilots where one local draft is not enough to prove modularity.

## Situation

The Psychology insight engine needed proof that topic-specific branches did not silently reuse fixture scenarios. Earlier validation had a default family/Mom sample and a work/Boss sample. A corrected work-message sample received read-only Claude Code / Claude-Cowork style review with verdict `ACCEPT_INTERNAL_REVIEW`, but that still only proved two topic families.

## Pattern that worked

1. Re-review the corrected blocked sample first, read-only, before expanding scope.
   - Expected verdict vocabulary: `ACCEPT_INTERNAL_REVIEW`, `REVISE_INTERNAL`, `BLOCKED`.
   - Treat acceptance as internal only, not public/canary/upload clearance.
2. Add a third distinct local-only topic family that is neither the default nor the previous correction target.
   - Example topic: `friend text replay anxiety pause`.
   - Goal: prove the engine does not fall back to Mom/family or Boss/work text.
3. Use TDD around semantic specificity, not just render success.
   - Assert hook/narration/cards/keywords contain friend/social signals.
   - Assert they do not contain Mom or Boss fallback hooks.
   - Preserve deny-term safety checks.
4. Generate with draft-only override, not active config switching:
   - `powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' draft --channel psychology --topic 'friend text replay anxiety pause' --draft-script-engine psychology_insight_v1 1`
5. Verify both machine and visual outputs:
   - focused tests for the engine and registry path
   - py_compile of touched modules
   - `run_agent.ps1 validate`
   - `git diff --check`
   - `.agent.lock` clear
   - metadata/relevance report inspection
   - frame-strip visual QA
6. Record material decisions and outputs in handoff files.

## Acceptance bar

A multi-sample pilot is internally stronger when it has at least three distinct scenario families that all pass local-only validation. For the Psychology insight engine, the useful set was:

1. default family/Mom
2. work/Boss
3. friend/social

Each sample should have topic-specific hook, persistent card/header language, narration, stock terms, and comment prompt. Rendering successfully is insufficient if metadata repeats an old scenario.

## Caveat handling

If visual QA finds non-blocking composition issues such as light split-screen panel text or overly large panel spacing, do not block semantic modularity acceptance. Defer them into a separate composition-only rung with no upload, no active config switch, and no scheduler/OAuth/privacy changes.

## Claude Code max-turn caveat

If Claude Code hits `Error: Reached max turns` after making partial changes, preserve useful work rather than restarting the phase. Inspect the workspace, complete the missing draft/QA/validation steps locally, and distinguish `worker max-turn exit` from `project validation result` in the handoff.