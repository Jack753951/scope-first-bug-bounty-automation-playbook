> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent Upload-Free Script Engine Pilot

Use this reference when coordinating youtube_agent phase work involving channel-specific script engines, draft-only experiments, third-party review gates, and visual QA.

## Durable workflow pattern

1. Keep new engines disabled by default until they pass internal review.
2. Trigger/read existing third-party review gates before continuing phase work when the user asks to proceed.
   - Prefer existing scheduled review jobs; resume/run them rather than creating duplicate jobs.
   - Record the job ID, action taken, and safety boundaries in handoff files.
3. Use read-only Claude/Cowork review for creative/strategy/phase-routing decisions.
   - Ask for verdicts such as `ACCEPT_INTERNAL_REVIEW`, `REVISE_INTERNAL`, or `BLOCKED`.
   - Explicitly state that review is not public/canary clearance unless the user separately authorizes publication.
4. Use TDD for engineering changes discovered by review or visual QA.
   - Add a focused regression first.
   - Confirm RED on the blocker.
   - Implement the smallest GREEN change.
5. Generate local-only drafts with `draft --draft-script-engine ...`; do not switch active channel config during pilot validation.
6. Inspect generated metadata and relevance reports, not just final videos.
7. Create a visual QA strip and use vision review before reporting success.
8. Update `handoff/accepted_changes.md`, `handoff/codex_review.md`, and `handoff/codex_task.md` with material decisions, outputs, validation, and next blockers.
9. Run focused tests, py_compile, `run_agent.ps1 validate`, `git diff --check`, and `.agent.lock` check before finalizing.

## Lessons from the Psychology insight engine pilot

- A draft can render successfully while still failing modularity: a new topic may repeat fixture text. Always compare `metadata.json` topic/hook/narration/cards against the requested topic.
- Multi-sample validation matters before channel activation. One passing draft proves render feasibility, not engine stability.
- Stock relevance should be driven by script metadata and recorded in `footage_relevance_report.json`.
- Preserve upload-free posture while evaluating: no upload, no `create`, no scheduler edits beyond explicitly requested existing review-job resume/run, no OAuth/token/client-secret edits, no `DEFAULT_PRIVACY` change, no destination channel ID filling, no default engine switch.
- If Claude/Cowork accepts internal review but notes composition blockers, do separate narrow rungs: typography, then topic diversity, then composition. Do not bundle.
- Before considering a channel-specific engine internally stable, prefer at least three semantically distinct local-only samples when feasible. For the Psychology pilot, the useful spread was default family/Mom, work/Boss, and friend/social; see `references/psychology-three-sample-validation-2026-05-18.md` for the concrete pattern.
- If Claude Code exits with `Error: Reached max turns` after partial implementation, inspect and verify the workspace instead of discarding the work. Complete missing draft/visual-QA/validation steps locally, and record the worker failure separately from the project validation result.

## Useful commands from repo root

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' draft --channel psychology --topic '<topic>' --draft-script-engine psychology_insight_v1 1
./.venv/Scripts/python.exe -m unittest tests.test_hook_overlay_text tests.test_stock_relevance_policy tests.test_agent_draft_script_engine_override tests.test_pipeline_insight_metadata tests.test_psychology_insight_engine tests.test_psychology_visuals tests.test_script_engine_registry
./.venv/Scripts/python.exe -m py_compile agent.py pipeline.py script_engines/__init__.py script_engines/base.py script_engines/psychology_insight.py psychology_visuals.py
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate
git diff --check && test ! -e .agent.lock && echo 'lock clear'
```
