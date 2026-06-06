> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: codex
description: "Delegate coding to OpenAI Codex CLI (features, PRs)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    related_skills: [claude-code, hermes-agent]
---

# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes terminal. Codex is OpenAI's autonomous coding agent CLI.

## When to use

- Building features
- Refactoring
- PR reviews
- Batch issue fixing

Requires the codex CLI and a git repository.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- Verify install: `codex --version`
- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials
  from the Codex CLI login flow
- First-run login: run `codex` or `codex login` in an interactive terminal and complete the OpenAI auth flow before delegating automated work
- After setup, run an auth smoke test inside the target repo: `codex exec "Reply with exactly: OK"`. A wrapper/doctor command that only finds the `codex` binary does not prove auth is usable.
- If `codex exec` reports `401 Unauthorized`, `Missing bearer or basic authentication`, or websocket auth failures against `/v1/responses`, treat it as missing/invalid Codex auth and run `codex login` or set a valid `OPENAI_API_KEY`; do not debug the repo first.
- Prefer running inside a git repository. If the workspace is intentionally not a git repo (common for local labs or generated workspaces), Codex CLI v0.130+ can run with `--skip-git-repo-check`; use this deliberately and note that git diff/commit validation will be unavailable.
- Use `pty=true` in terminal calls — Codex is an interactive terminal app

For Hermes itself, `model.provider: openai-codex` uses Hermes-managed Codex
OAuth from `~/.hermes/auth.json` after `hermes auth add openai-codex`. For the
standalone Codex CLI, a valid CLI OAuth session may live under
`~/.codex/auth.json`; do not treat a missing `OPENAI_API_KEY` alone as proof
that Codex auth is missing.

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For non-git workspaces where this is intentional:
```
terminal(command="codex exec --sandbox workspace-write --skip-git-repo-check 'Update the handoff report'", workdir="~/project", pty=true)
```
Note in the final validation that git diff/commit checks were unavailable.

## Background Mode (Long Tasks)

```
# Start in background with PTY
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |

## Read-only direction reviews with required context

For direction or architecture reviews where Codex must attest to reading a fixed set of files, use a small review packet and require an explicit context-read attestation. If Codex cannot complete local reads in the execution environment, do not accept a provisional review as final; retry with an embedded synchronized context packet and make the attestation say that embedded context was supplied by Hermes. See `references/embedded-context-review-packet-fallback.md`.

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

For read-only direction reviews that require context attestation, if Codex cannot directly read required repo files due sandbox/PTY friction, do not treat the first result as a formal review. Use the embedded synchronized context fallback in `references/embedded-context-review-fallback.md`, then record the provenance difference in the synthesis.

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Media/render automation review loops

When delegating review or implementation for video-generation/rendering projects, ask Codex to inspect both the feature behavior and the rendering failure modes:

- FFmpeg filtergraph quoting/escaping, especially `drawtext` with commas, colons, backslashes, apostrophes, and dynamic text.
- Text wrapping behavior for long unbroken tokens (URLs, usernames, long English words); do not silently truncate tails. For FFmpeg fixtures using `drawtext=textfile=...`, remember drawtext does not auto-wrap lines: pre-wrap text, use conservative margins, and extract a representative frame to visually confirm no clipping before accepting the fixture.
- Backward compatibility of public/internal function signatures when adding metadata inputs.
- Render smoke tests that parse the generated FFmpeg filtergraph when FFmpeg is available, plus normal unit/compile checks.
- Project safety boundaries: do not change upload privacy, scheduler behavior, OAuth/token files, generated user data, or runtime state unless explicitly requested.
- Handoff files or review notes should distinguish implemented changes from out-of-scope risks.
- If a Codex worker reports validation as blocked by its sandbox/shell environment, do not accept that as the final project verdict until Hermes reruns the same checks directly in the project shell/venv. Record the worker blocker separately from the authoritative local validation result; if the direct rerun passes, update `handoff/codex_review.md` / accepted-change notes from NEEDS_CHANGES to PASS rather than preserving stale worker caveats.
- If a Codex `exec` call times out, do not assume no work was done. Codex may have already written a large patch or generated files before the wrapper timeout. Immediately inspect `git status`, key files, and generated outputs; run the intended validation directly; then continue from the actual workspace state instead of blindly rerunning or discarding the partial result.
- For safety-sensitive direction reviews, require visible receipts and context synchronization. Save `--output-last-message` plus stdout/event logs. If Codex cannot directly read required repo files, do not count the review as complete; retry with a Hermes-built embedded context packet and label the review as based on synchronized embedded context. See `references/cybersec-direction-review-context-sync.md`.
- For Shorts/video projects, recover Codex timeout partial patches with the checklist in `references/video-codex-timeout-recovery.md`: inspect expected handoff modules and artifacts, restore any missing fixture module before test collection, rerun generation with the project venv, use `unittest` if venv pytest is unavailable, use the media-QA tool's actual flags, and update both `handoff/codex_review.md` and `handoff/accepted_changes.md` with Hermes's authoritative local validation.

See `references/video-render-agent-review.md` for a reusable prompt/checklist for Codex reviews of Shorts/video automation agents.

For new content-engine/channel scaffolds that must remain proposal-only or draft-only, use `references/video-channel-scaffold-gates.md`. It covers disabled-channel placement, active-discovery tripwires, OAuth deferral, legal asset placeholders, data-only offline pilot packs, upload-free validation/report runners, deterministic local preview/storyboard layers, upload-free local MP4 fixtures, internal user-viewing gates, and validation expectations before activation.

For the specific rung between upload-free scaffolds and asking the user to watch a local/internal sample, use `references/video-internal-user-viewing-gates.md`. It covers source/template metadata, English joke localization, real visual contact-sheet evidence, safe SFX/audio evidence, disabled-only/runtime-surface checks, local validation after sandbox-blocked worker reviews, and wording that avoids confusing internal viewing with publication approval.

For offline sticker/background/prop asset-pack rungs in video automation projects, use `references/video-offline-asset-pack-pipeline.md`. It covers deterministic local SVG candidates, manifest provenance, semantic preview caption cards, manifest-backed background/prop mapping, visual QA, and production-readiness gates without external asset-site authentication.

For offline meme/sticker/prop/background asset candidates in video automation projects, use `references/video-offline-asset-pack-pipeline.md`. It covers deterministic project-owned SVG placeholder packs, manifest provenance and production-readiness flags, preview integration with fallback, safety-boundary tests, upload-free validation, and handoff notes.

When a Shorts/video automation project can render valid drafts but live source selection is strategically off-target, use `references/video-source-candidate-prescoring.md`. It covers transparent pre-generation scoring labels, negative labels, safe fallback warnings, metadata propagation, word-boundary/phrase matching pitfalls, upload-free draft verification, and review checklist items for source-fit layers.

When a Shorts/video automation project needs a lightweight first-seconds retention signal after render QA, use `references/video-opening-distinctness-qa.md`. It covers upload-free opening-4s frame extraction, cropped-middle-band PPM diffing to reduce subtitle/hook-text noise, handoff-only JSON reports, parameter validation, and review-packet wording that distinguishes a QA signal from publication approval.

When a multi-channel Shorts/video automation project needs deeper per-channel script strategy, use `references/video-script-engine-modularization.md`. It covers behavior-preserving script-engine registries, fail-closed experimental engines, preserving manual-test semantics, TDD coverage, and keeping upload/scheduler/OAuth/privacy behavior out of the registry phase.

When a Shorts/video project has a QA-passing upload-free fixture that must be carried into the normal draft/script pipeline without activating it, use `references/video-disabled-draft-integration-scaffold.md`. It covers disabled-by-default engine/path registration, fixture-parity metadata contracts, legacy downstream script-key compatibility, tests proving active config did not switch, and validation wording that distinguishes upload-free draft experiments from publication/canary approval.

When a Shorts/video project has an already-rendered and reviewed MP4 that may later become a private canary, use `references/video-existing-private-upload-gates.md`. It covers why not to misuse `create`, exact existing-artifact inputs, private-only/publishAt-none enforcement, strict pre-upload render QA, destination guard requirements, DB recording, partial-failure recovery, and handoff wording that separates design/approval packets from actual upload authorization.

## Rules

0. **Conserve Codex/OpenAI quota when requested** — if the user says Codex tokens are draining too fast or prefers Claude quota, do not assign Codex the full implementation by default. In Hermes-style repos, rewrite/keep `handoff/codex_task.md` as a focused review checklist with narrow surgical-fix permission, delegate the main build to Claude Code (`handoff/claude_code_task.md` / `run_hermes_worker.ps1 -Worker claude-code`), then run Codex only after Claude's patch and Hermes local validation need an independent review.
1. **Always use `pty=true`** — Codex is an interactive terminal app and hangs without a PTY
2. **Git repo required** — Codex won't run outside a git directory. Use `mktemp -d && git init` for scratch
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly
4. **`--full-auto` for building** — auto-approves changes within the sandbox
5. **Background for long tasks** — use `background=true` and monitor with `process` tool
6. **Don't interfere** — monitor with `poll`/`log`, be patient with long-running tasks
7. **Parallel is fine** — run multiple Codex processes at once for batch work
