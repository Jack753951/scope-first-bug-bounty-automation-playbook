> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent upload-free modular script rungs

Use this when continuing `youtubestrict/youtube_agent` script-engine modularization or Shorts draft QA from Git-Bash/Hermes on Windows.

## Durable workflow pattern

1. Keep new script engines disabled-by-default until they pass multiple local drafts and read-only creative review.
2. Use draft-only overrides for safe testing:
   ```bash
   powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' draft --channel psychology --topic 'boundary pause relationship text' --draft-script-engine psychology_insight_v1 1
   ```
3. For each rung, isolate one variable only. Examples that worked:
   - stock relevance policy only,
   - hook punctuation/card readability only,
   - microtext sizing only.
4. Before implementation, get/read Claude-Cowork review when available and convert the highest-impact blocker into the next smallest engineering rung.
5. Use TDD against deterministic surfaces first:
   - CLI/config behavior tests for draft-only overrides,
   - metadata preservation tests for script-engine outputs,
   - FFmpeg filter-string tests for visual typography/scrim changes,
   - stock-search plan tests with network disabled/mocked.
6. Generate a new local-only draft, then a frame strip for visual QA:
   ```bash
   ffmpeg -y -i data/psychology/output/<job>/final_short.mp4 -vf "fps=1/3,scale=270:-1,tile=3x3" -frames:v 1 -update 1 handoff/visual_qa/<name>_strip.jpg
   ```
7. Record results in the project handoff files:
   - `handoff/accepted_changes.md`
   - `handoff/codex_review.md`
   - `handoff/codex_task.md`
   - review request/response files under `handoff/`

## Gates used in this session

- `ACCEPT_INTERNAL_REVIEW` means local artifact viewing only; it is not canary/public authorization.
- Do not switch `channels/<channel>.json` to a new engine after one good draft.
- Require at least one additional distinct local-only draft after an internal acceptance to establish consistency.
- Public/canary remains gated behind multi-draft review plus explicit user authorization.

## Safety invariants

Do not upload/publish, call `create`, change scheduler behavior, touch OAuth/token/client-secret files, change `DEFAULT_PRIVACY`, fill destination channel IDs, enable Storytime.exe, or delete runtime state while doing upload-free modularization rungs.

## Verification bundle

Run from repo root after code/prompt changes:

```bash
./.venv/Scripts/python.exe -m unittest tests.test_hook_overlay_text tests.test_stock_relevance_policy tests.test_agent_draft_script_engine_override tests.test_pipeline_insight_metadata tests.test_psychology_insight_engine tests.test_psychology_visuals tests.test_script_engine_registry
./.venv/Scripts/python.exe -m py_compile agent.py pipeline.py script_engines/__init__.py script_engines/base.py script_engines/psychology_insight.py psychology_visuals.py
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate
git diff --check && test ! -e .agent.lock && echo 'lock clear'
```
