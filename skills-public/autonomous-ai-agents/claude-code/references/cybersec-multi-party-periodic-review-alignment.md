> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec multi-party periodic review alignment via Claude Code

Use this reference when a Hermes-style cybersecurity workspace needs to operationalize governance/review policy without adding runtime, schema, target-touching, or candidate-chain surfaces.

## Pattern

1. Treat the direction review as T3 if it decides a workflow/artifact boundary, even when the implementation slice is only T1 Markdown/templates.
2. Route the design-only direction review through the project Claude Code MAX/OAuth wrapper (for this repo: `HACKLAB=<user-home> ./bin/hermes claude-impl`) so usage JSON, worker result, turn count, and model/runtime evidence are recorded.
3. Keep the Claude Code task file explicit:
   - read `.hermes.md` and the relevant governance policy files;
   - write exactly one review artifact;
   - no code/runtime/schema/scope/test/template changes unless the task is the later implementation slice;
   - no scanners, targets, credentials, scheduler, deployment, billing, or production settings.
4. If the approved implementation is governance-only, prefer a periodic/milestone review template under `handoff/periodic_reviews/` over adding a candidate-chain reviewer-notes artifact.
5. Preserve dated review folders as frozen historical snapshots. Add a current reusable template such as `handoff/periodic_reviews/review_template_v0.md` instead of editing older dated review artifacts.
6. Add a README in the periodic review directory stating that these artifacts are Markdown governance documents, not `*/0.1-trial` schemas and not machine-parsed by candidate-chain consumers.
7. Obtain an independent implementation review after the template/docs changes. If a broad Claude Code review hits max turns, use a small no-tools packet with only the diff/status and ask for a concise PASS/ROUTE_BACK/BLOCK verdict.
8. Hermes must synthesize separately: final decision block, reviewer route/tool/model evidence, validation commands, accepted_changes update, and GitHub/PR tracking comment if available.
9. When the operator says to continue with the accepted slice, complete the local-to-GitHub loop: inspect staged scope, run staged diff safety checks, run the project review gate, commit with a conventional message, push the branch, verify the PR head SHA/status checks, and post a PR tracking update.
10. Treat `handoff/claude_code_task.md` and `handoff/claude_code_result.md` as rolling artifacts that may be overwritten by later worker runs. For important phase/direction slices, also preserve named artifacts (`handoff/cowork_pX_Y_*`, `handoff/hermes_pX_Y_synthesis.md`, timestamped usage JSON) before committing so historical review evidence is not only in the rolling files.
11. Post GitHub PR comments from a body file, not inline shell `--body`, whenever the text contains Markdown backticks or `$` variables. On bash/MSYS, unescaped backticks in `gh pr comment --body "..."` are command substitution and can silently corrupt the comment; if it happens, delete the malformed comment via `gh api -X DELETE repos/OWNER/REPO/issues/comments/COMMENT_ID` and repost with `--body-file`.

## Safety assertions to verify

- No reviewer-notes artifact file, reviewer-notes consumer, reviewer-notes schema, reviewer-notes fixture, or chain wiring was created.
- No P2.24 helper-extraction trigger fired: no fifth stdin consumer, no shared `LIVE_TARGET_FLAGS`, no `_compact_emit`, no `_error_payload`, no `_argv_errors`, and no new chain import path.
- Frozen periodic review snapshot has no diff, e.g. `git diff --name-only -- handoff/periodic_reviews/2026-05-18` returns empty.
- Only `handoff/**` governance/docs artifacts changed unless the operator explicitly approved a wider implementation.
- `git diff --check` and the project local review command pass.
- Focused forbidden-surface scan finds no secrets and no runtime/config/module/schema/test/report/scan/loot/run changes.

## Useful final decision shape

```text
Decision: PASS_WITH_CONDITIONS
Tier: T3 direction review; T1 implementation slice
Hermes authority: conditional; conditions satisfied by independent review plus local validation
Reviewers consulted:
- Direction: Claude Code MAX/OAuth via project wrapper; visible model/runtime: <self-reported or not exposed>
- Implementation review: Claude Code read-only packet; visible model/runtime: <self-reported or not exposed>
- Hermes local validation: terminal/local checks
Validation performed: git diff --check; focused forbidden-surface scan; frozen snapshot diff check; project review command
Blocking findings: none
Safety boundary: docs/templates only; no target-touching/runtime/schema/consumer/scanner/report-submission/credential/scheduler/deployment/billing/production/scope changes
OSS Recon Gate: not applicable for Markdown template/docs only; required before future reviewer-notes artifact or consumer
User approval required: no for docs/templates-only; yes if deferred runtime/schema/live/scheduler/production items are pulled into scope
Accepted changes updated: yes
Next action: GitHub tracking updated if available; wait for operator direction before next Phase slice
```
