> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent Multi-Agent Learning Loop TDD Pattern

Use this reference when adding a learning/review layer to a media automation project where production loops already create/upload private artifacts and a later review stage promotes learnings.

## Durable pattern

1. Keep production and learning layers separate.
   - Morning/daily production loops should continue creating/uploading according to existing behavior.
   - Long-horizon review runs later as a learning synthesis layer.
   - Do not add a new publication/safety gate unless the user explicitly asks for one.

2. Make reviewer context explicit for external agents.
   - Claude Code, Codex, or other CLI workers do not automatically receive Hermes private memory.
   - Add repo bridge files such as `CLAUDE.md`, `AGENTS.md`, and repo-local Obsidian/project-index notes.
   - Evidence packets should include paths to active strategy, accepted changes, memory-governance docs, and project-index notes rather than dumping whole vaults.

3. Split review roles rather than asking several agents to do the same review.
   - Creative/channel-fit reviewer: hook, title, channel fit, story arc, viewer curiosity.
   - Technical MP4 QA reviewer: playability, duration/resolution/audio, subtitles/readability, first seconds, evidence artifacts.
   - Learning/strategy integrity reviewer: data maturity, distribution noise, sample size, whether a pattern deserves promotion.
   - Engineering/pipeline reviewer only when systematic implementation defects are suspected.

4. Treat raw review output as evidence, not production input.
   - Raw reviewer notes should land under `handoff/learning/multi_agent_reviews/YYYY-MM-DD/`.
   - Hermes synthesis may promote only mature conclusions into a machine-readable artifact such as `handoff/learning/promoted_rules.json`.
   - Production strategy hints should read only the promoted artifact, not reviewer raw Markdown.

5. Use TDD for the ingestion boundary.
   - RED tests should prove missing/malformed promoted rules fail soft.
   - RED tests should prove only current-channel rules are injected.
   - RED tests should prove `OBSERVE_ONLY` / `EARLY_SIGNAL_ONLY` and raw reviewer text do not enter production prompts.
   - RED tests should prove expired rules are skipped and supported promoted actions are included.

6. Recommended eligible actions for production prompt injection:
   - `PROMOTE_TO_NEXT_BATCH_CONSTRAINT`
   - `PROMOTE_TO_SYSTEM_RULE`
   - `NEGATIVE_EXEMPLAR`

7. Recommended non-production labels:
   - `OBSERVE_ONLY`
   - `EARLY_SIGNAL_ONLY`
   - `CANDIDATE_FOR_PATTERN_REVIEW`
   - `NO_SIGNAL_DISTRIBUTION`

## Validation checklist

- Focused tests pass for promoted-rule ingestion.
- Compile checks pass for touched Python files.
- Project validation passes.
- `.agent.lock` is clear.
- Default privacy remains private if the project has publication behavior.
- No upload/publish/schedule/OAuth/token/channel-config/runtime-data changes occurred unless explicitly requested.
- Handoff files record route/tool, visible model/runtime, validation commands, and boundaries.

## Notes

This is a learning loop pattern, not a safety gate pattern. The key invariant is: production consumes only Hermes-synthesized promoted learning, never raw multi-agent reviewer opinions.
