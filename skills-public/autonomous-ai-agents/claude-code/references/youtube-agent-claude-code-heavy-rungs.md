> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent — Heavier Claude Code Implementation Rungs

Use this pattern when the user explicitly wants to spend more Claude Code usage in `youtube_agent` while preserving Hermes as verifier and avoiding upload/scheduler side effects.

## Trigger

- User says Claude Code usage is plentiful / asks to use Claude Code more.
- Task is implementation-heavy but bounded and local-only, e.g. media-selection policy, renderer controls, provenance reports, tests, or handoff updates.
- The project has safety boundaries around YouTube upload, OAuth, scheduler, `DEFAULT_PRIVACY`, channel destinations, and runtime data.

## Pattern

1. Write a precise task packet in `handoff/claude_code_task.md`.
   - Include goal, hard no-touch boundaries, files to inspect, required TDD coverage, validation commands, and handoff files to update.
   - Make the packet self-contained so Claude Code does not need chat context.
2. Run direct Claude Code print mode with JSON capture, not only the wrapper, when a larger bounded rung is desired:

```bash
claude -p "$(cat handoff/claude_code_task.md)" \
  --allowedTools 'Read,Edit,Write,Bash,Grep,Glob' \
  --max-turns 35 \
  --output-format json \
  > handoff/claude_code_<rung_name>_<date>.raw.json \
  < /dev/null
```

3. Require Claude Code to update durable repo handoff files:
   - `handoff/accepted_changes.md`
   - `handoff/codex_review.md` (or route/review notes when Codex is not the worker)
   - a concise rung report such as `handoff/<topic>_rung_<date>.md`
4. After Claude Code exits, parse/report visible run metadata from the raw JSON:
   - `subtype`
   - `session_id`
   - `num_turns`
   - `total_cost_usd` if present
   - `modelUsage` keys, if present
5. Hermes must independently verify locally. Do not rely on Claude Code's self-report.
   - Prefer the project venv for Python tests in `youtube_agent`: `./.venv/Scripts/python.exe ...`.
   - A system `python` failure such as missing `anthropic` is usually an environment mismatch; rerun with the project venv before diagnosing a project failure.
6. Run the normal safety checks after code changes:

```bash
./.venv/Scripts/python.exe -m unittest <focused tests> -v
./.venv/Scripts/python.exe -m compileall <changed python files>
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate
```

7. Final status must separate:
   - code/test rung completion,
   - local-only artifact generation (if any),
   - private/public canary readiness,
   - upload/scheduler/OAuth/default-privacy boundaries.

## Example: redditstories selected-asset gate

A successful bounded rung used Claude Code Pro/OAuth to add selected-asset provenance and provider-metadata deny-term rejection to `pipeline.py` and tests, captured raw JSON in `handoff/claude_code_selected_asset_gate_20260521.raw.json`, then Hermes reran venv-based unittests, compileall, and `run_agent.ps1 validate`.

Key lesson: heavier Claude Code usage is safe when the task packet is narrow, the raw JSON is retained for route/model/runtime accounting, and Hermes performs final verification plus local-only/canary boundary labeling.
