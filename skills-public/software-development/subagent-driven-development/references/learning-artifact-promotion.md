> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Learning Artifact Promotion Pattern

Use this when a multi-agent review, daily learning cron, analytics synthesis, or prompt/strategy loop can produce machine-readable guidance that a production generator will consume later.

## Problem

Reviewer prose and early signals are useful for learning, but dangerous if they are written directly into production prompts or channel config. A future production loop should consume only mature, synthesized rules with a stable schema.

## Pattern

1. Keep raw reviewer output in review files only.
   - Accept labels such as `OBSERVE_ONLY`, `EARLY_SIGNAL_ONLY`, `CANDIDATE_FOR_PATTERN_REVIEW`, `NO_SIGNAL_DISTRIBUTION`, and reviewer prose here.
   - Do not let these files be read directly by generation code.

2. Hermes synthesis writes a candidate artifact first.
   - Example path: `handoff/learning/multi_agent_reviews/YYYY-MM-DD/promoted_rules_candidate.json`.
   - The candidate contains only production-consumable mature rules.
   - Include channel scope, action/status, actionable text, confidence, evidence ids, and optional expiry.

3. Validate before promotion.
   - Use a deterministic validator/writer helper when available.
   - Command shape: `python tools/validate_promoted_rules.py <candidate> --promote-to <production-artifact>`.
   - Validation failure must leave the existing production artifact unchanged.
   - Record validator output in the synthesis/readout for follow-up.

4. Production code reads only the promoted artifact fail-soft.
   - Missing/malformed JSON should not block production.
   - Filter to the current channel/scope.
   - Ignore expired rules.
   - Inject only allowed mature actions, e.g. `PROMOTE_TO_NEXT_BATCH_CONSTRAINT`, `PROMOTE_TO_SYSTEM_RULE`, `NEGATIVE_EXEMPLAR`.

5. Preserve the boundary.
   - This is a learning/prompt-ingestion discipline, not a publication approval gate.
   - Do not let the validator authorize upload, publish, schedule, OAuth/token changes, channel JSON rewrites, privacy changes, or runtime-data deletion.

## Reviewer/orchestrator guidance

- The orchestrator owns task splitting. Use delegated reviewers when their second perspective materially improves quality or risk detection; do not delegate ceremonially.
- If a slice is narrow and fully covered by RED/GREEN tests, proceeding `Hermes-local` is acceptable, but label the route and state why delegation would add little signal.
- If a delegated review times out or returns no final report, do not count it as review evidence. Inspect the workspace, run focused checks, and report the incomplete review honestly.

## Minimal test coverage

- Valid candidate promotes/copies to output.
- Unsupported early-learning action is rejected and does not overwrite existing output.
- Missing channel/scope is rejected.
- Missing actionable text is rejected.
- Malformed JSON is rejected.
- Existing production artifact remains valid after a failed candidate.
