> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Video disabled draft integration scaffold

Use this when a Shorts/video automation project has a passing upload-free fixture or visual QA artifact, but the behavior is not yet integrated with the normal draft/script pipeline.

## Pattern

1. Treat fixture parity as the contract, not the final product.
   - Preserve the exact strings/metadata that passed visual QA unless a new QA pass is planned.
   - Carry scenario/hook/motion evidence forward into code-level metadata.
2. Add an opt-in engine/path, disabled by default.
   - Register the new engine/path so tests can select it explicitly.
   - Do not switch active channel JSON/config in the same rung.
   - Do not add upload destination IDs, scheduler changes, OAuth/token edits, or privacy changes.
3. Keep downstream compatibility.
   - Script engines should still emit legacy keys expected by existing render/upload code, e.g. `title`, `hook_question`, `narration`, `keywords`, `hashtags`.
   - Add experimental metadata as additional fields such as `insight_cards`, not as a replacement for legacy fields.
4. Use strict TDD.
   - RED: assert the new engine/path is unknown or unavailable first.
   - GREEN: minimally register and implement the explicit opt-in path.
   - Add tests proving active/default channel config did not switch.
5. Validate locally after worker/sandbox reports.
   - Focused tests for the new engine/path and existing renderer helpers.
   - `py_compile` on touched modules.
   - Project safety validation (`run_agent.ps1 validate` in youtube_agent-style repos).
   - `.agent.lock` clear and `git diff --check` clean except harmless line-ending warnings.

## Useful test assertions

- `get_script_engine("new_engine_v1")` returns an engine.
- Active channel config does not resolve to the new engine unless explicitly configured in a local test object.
- New output passes the existing fixture/metadata validator.
- Post-polish QA contract fields are present, for example scenario metadata and motion cues.
- Legacy downstream script keys remain non-empty.

## Acceptance wording

Record that the lane is ready only for a later upload-free draft experiment, not publication or active config switching, unless the user explicitly approves the higher-risk gate.
