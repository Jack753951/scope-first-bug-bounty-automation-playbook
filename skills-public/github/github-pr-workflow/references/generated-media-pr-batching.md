> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Generated-media PR batching and reporting

Use this reference when a long-running product/video repo branch contains both durable code/docs changes and many local render or visual-QA artifacts.

## Pattern

1. Treat generated media, visual-QA output folders, playback outputs, and sample render packets as local artifacts unless the user explicitly wants them versioned.
2. Build commits around durable intent, not directory convenience:
   - implementation/runtime safety gates and tests
   - docs/handoff/review records
   - templates/fixtures/spec metadata that are deliberately small and reviewable
3. Stage explicit path sets. Avoid `git add .` on branches with render outputs or QA packet directories.
4. Before committing, verify the staged set with:
   - `git diff --cached --name-status`
   - `git diff --cached --stat`
   - `git diff --cached --check`
   - lightweight staged secret/safety scan
   - project test/review gate
5. If generated assets are deliberately committed, say exactly what kind of assets they are and why they are reviewable. If they are not committed, say so explicitly in the PR update and final report.
6. After pushing, update the existing PR with a temp-file body/comment. Include commit SHAs/messages, test counts or suite result, secret/safety scan result, GitHub check status, and an honest note that the working tree still has untracked/generated local artifacts if true.
7. Delete accidental junk files only when they are clearly syntactically broken or generated leftovers; do not delete operational scripts or handoff artifacts without user confirmation.

## Reporting wording

Prefer explicit distinctions:

- "Committed and pushed: code/tests/spec metadata/review records."
- "Not committed: generated media / visual-QA output folders / local playback outputs."
- "Remaining dirty state is intentionally excluded from the PR; no ahead/behind after push."

This prevents the user from assuming the PR contains large render outputs or local QA evidence when only durable source artifacts were pushed.