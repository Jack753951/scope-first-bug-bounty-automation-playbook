> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# youtube_agent upload-free stock relevance rung

Use this when a YouTube Agent local draft technically renders but Claude/Cowork or visual QA flags generic/off-topic stock footage.

## Pattern

1. Keep the work upload-free and opt-in only.
   - Use `draft`, not `create`.
   - Require explicit `--channel` when overriding a draft engine.
   - Do not edit active `channels/*.json`, destination IDs, scheduler, OAuth/token/client-secret, or `DEFAULT_PRIVACY`.
2. Ask Claude/Cowork for read-only artifact review before choosing the next rung.
   - Provide video path, metadata path, visual strip, render QA result, script summary, and explicit safety boundaries.
   - Treat `REVISE_INTERNAL` as a signal for a narrow local-quality rung, not publication.
3. For footage/source-fit problems, add script-level stock relevance metadata rather than hardcoding channel-wide behavior:
   - preferred search terms, e.g. phone/journaling/breathing terms for a parent-text boundary psychology script.
   - deny terms for low-fit motifs, e.g. macro fruit, food in water, abstract liquid, romantic couple silhouette.
4. Preserve reviewer provenance.
   - Write a local `footage_relevance_report.json` next to `metadata.json` with kept terms, dropped terms, deny terms, and selected paths.
   - Keep tests network-independent by mocking requests and asserting the report is written even when downloads fail.
5. Regenerate an upload-free local draft and visual strip, then visually check for the specific blockers that motivated the rung.
6. Update handoff files (`accepted_changes.md`, `codex_review.md`, `codex_task.md`) with artifact paths, verdict, test status, and safety statement.

## TDD shape

RED examples:

- `build_stock_search_plan(...)` does not exist.
- `download_stock_videos(..., script_meta=...)` rejects script metadata.
- The draft script engine does not emit stock search / deny metadata.
- No `footage_relevance_report.json` is produced.

GREEN examples:

- script-preferred terms are ordered before generic keywords/fallbacks.
- deny motifs are removed from the search plan and recorded in the report.
- downloader writes report without requiring successful network downloads.

## Verification commands

From repo root on Windows via Git-Bash/MSYS:

```bash
./.venv/Scripts/python.exe -m unittest tests.test_stock_relevance_policy tests.test_agent_draft_script_engine_override tests.test_pipeline_insight_metadata tests.test_psychology_insight_engine tests.test_psychology_visuals tests.test_script_engine_registry
./.venv/Scripts/python.exe -m py_compile agent.py pipeline.py script_engines/__init__.py script_engines/base.py script_engines/psychology_insight.py psychology_visuals.py
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate
git diff --check && test ! -e .agent.lock && echo 'lock clear'
```

## Pitfalls

- Do not solve one bad draft by switching active channel config; use a draft-only override.
- Do not add network/API-dependent tests for Pexels candidate quality.
- A render QA PASS is insufficient if visual QA shows off-topic motifs; add a provenance/reporting rung before discussing canary/public.
- Record remaining creative caveats separately from technical PASS, e.g. small card text or punctuation rendering issues.
