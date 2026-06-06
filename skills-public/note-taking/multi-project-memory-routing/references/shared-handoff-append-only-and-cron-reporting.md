> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Shared handoff append-only and cron reporting pattern

Use this pattern when a project has multiple agents/workers writing shared handoff Markdown files, especially when cron jobs or wrapper scripts may regenerate rolling reports.

## Core rule

Treat durable shared handoff logs as collaboration surfaces, not as single-writer scratch files.

- Append/prepend durable accepted-change logs; do not replace the whole file.
- Re-read the target Markdown file immediately before patching it, especially after worker/subagent runs.
- Put long reviews, run outputs, transcripts, and dense QA detail in named artifacts.
- Add only a short index entry to the accepted-change log with the artifact path and validation status.
- Archive-before-overwrite protects known rolling convenience outputs; it does not make arbitrary shared handoff Markdown safe to rewrite.

## Cron / scheduled-agent reporting

For scheduled local draft or batch jobs:

- Prefer a named per-run report artifact plus a short append-only accepted-change entry.
- Avoid cron prompts that tell the agent to rewrite large shared handoff Markdown files.
- If the run advances only local draft/render state, say so explicitly; do not imply upload/public/scheduling readiness.
- When a separate review gate is required before activation, include a fixed visible line such as: `Claude Code visionreview: pending/required before private canary`.

## Activation boundary example

Render QA PASS is not the same as private-canary-ready. If private canary requires Claude Code visual review, the report must keep that gate visible until the review artifact exists and has been accepted by the project-local handoff process.

## Verification

When encoding this in a repo:

- Add a regression/static test that fails if the policy text disappears from the relevant handoff docs or cron prompt docs.
- Run the project’s local validation after policy edits.
- Check that no lock file or scheduler side effect was left behind.

## Do not store here

- Run-specific output, dates, PRs, issue IDs, or validation transcripts.
- Project-private channel IDs, OAuth data, token paths beyond non-sensitive policy-level examples.
- The full content of named artifacts; store those in the project repo or Obsidian as appropriate.
