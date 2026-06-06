> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: claude-code
description: "Delegate coding to Claude Code CLI (features, PRs)."
version: 2.2.1
author: Hermes Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Claude, Anthropic, Code-Review, Refactoring, PTY, Automation]
    related_skills: [codex, hermes-agent, opencode]
---

# Claude Code — Hermes Orchestration Guide

Reference note: for youtube_agent upload-free script-engine pilots, third-party review gates, visual QA, handoff records, and validation commands, see `references/youtube-agent-upload-free-script-engine-pilot.md`. For the concrete Psychology three-sample semantic validation pattern (family/work/friend) and how to handle Claude Code max-turn partials during that pilot, see `references/psychology-three-sample-validation-2026-05-18.md`.

Reference note: for API-key-aware routing where Claude Code Pro/OAuth is used for build work while preserving `ANTHROPIC_API_KEY` for script/content generation, see `references/api-key-aware-routing.md`.

Reference note: for cybersecurity workspaces that route offline/local implementation to Claude Code Pro/OAuth while keeping Hermes as safety gate/verifier and tracking future-only worker mix, see `references/cybersec-safe-worker-routing.md`. For Hermes-style cybersec repos, do not leave this as documentation-only policy: make the wrapper default visibly call Claude Code implementation and emit usage JSON; see `references/cybersec-claude-impl-default-routing.md`. For CTF-to-platform pattern where offline helpers, verifier metadata fixtures, and a weak read-only linter are trialed before schema/runtime promotion, see `references/cybersec-ctf-offline-metadata-trial.md`. For design-only phase direction/closeout reviews in safety-sensitive cybersec workspaces, including when to defer a tempting core-helper refactor and close a phase via `hermes claude-impl`, see `references/cybersec-phase-closeout-reviews.md`. For governance-only multi-party periodic review alignment — direction review via Claude Code, docs/templates-only implementation, independent review, Hermes synthesis, accepted_changes, and PR tracking while avoiding reviewer-notes artifacts or P2.24 triggers — see `references/cybersec-multi-party-periodic-review-alignment.md`. When the operator explicitly asks to call Claude Code as a direction/vision reviewer, produce a read-only packet, require context-read attestation, save raw JSON + markdown receipts, and synthesize separately; see `references/cybersec-direction-review-receipts.md`. If a cybersec fixture/design review via `hermes claude-impl` hits `error_max_turns` and fails to write the requested review artifact, use the narrow read-only recovery pattern in `references/cybersec-fixture-review-maxturn-fallback.md`. For Cybersec Lab one-vulnerability local-lab waves, Claude Code's role is post-evidence read-only review from a compact packet: assess project value, overclaim risk, and stop/rerun/switch/packetize; do not turn the review into a new safety gate, approval layer, or governance-first process. Hermes owns tactical preview and final synthesis; detailed workflow lives in the `owasp-single-vuln-lab-wave` skill reference `agent-preview-and-review-gates.md`.

Reference note: for Hermes project wrappers that should default `-Mode full` or equivalent build pipelines toward Claude Code while preserving Codex/GPT fallback, see `references/hermes-project-wrapper-routing.md`.

Reference note: for youtube_agent's durable support-layer pattern — repo handoff as engineering source of truth, Obsidian for long-term strategy/decision memory, GitHub for branch/PR/CI/review support, and Hermes as verifier — see `references/youtube-agent-memory-github-support.md`.

Reference note: for youtube_agent `visionreview` / visual QA routing — treat non-trivial visual review and pre-generation creative prompt/source-fit packets as creative review and default compact review packets to Claude Code CLI via Claude Pro/OAuth, with Hermes as evidence extractor/final safety gate and Codex/GPT as fallback — see `references/youtube-agent-visionreview-claude-code-routing.md`.

Reference note: for Storytime local-only creative iteration, do not let upload/licensing caution collapse into placeholder-only drafts. When provided/current meme/GIF-like素材, emotion stickers, SFX, BGM, or VO placeholders exist, use asset-backed local samples so human fun/retention can actually be judged while keeping upload/OAuth/scheduler/channel/default-privacy gates closed; see `references/youtube-agent-storytime-asset-backed-sfx-local-iteration.md`.

Reference note: for youtube_agent fast local learning batches, keep the local loop lightweight but write one compact batch evidence packet, distinguish source-grounded canary candidates from manual-topic renderer samples, and if a broad Claude Code Read-tools batch review hits `error_max_turns`, fall back to a one-turn no-tools text-only review of the packet; see `references/youtube-agent-fast-local-batch-review.md`.

Reference note: when the user wants to spend more Claude Code usage in `youtube_agent`, use a bounded direct print-mode implementation rung with `handoff/claude_code_task.md`, JSON raw-result capture, larger `--max-turns`, explicit no-upload/scheduler/OAuth boundaries, and Hermes venv-based re-verification; see `references/youtube-agent-claude-code-heavy-rungs.md`.

Reference note: for youtube_agent Storytime.exe / generated-media internal samples, use the upload-free evidence-packet + read-only Claude Code visionreview pattern in `references/youtube-agent-storytime-v2-internal-sample.md`; it includes the max-turn resume pattern, artifact checklist, safety gates, and reporting labels (`STRONG_INTERNAL_SAMPLE` but not activation-cleared). For the corrected Storytime cat-meme-theater workflow — default role-separated Claude Code creative + technical reviews, avoid making the user remind you, prefer Claude Code implementation rungs when useful, treat the reference mechanics as mostly static PNG/cutout actors animated by scale/translate/shake/hard cuts rather than GIF-first playback, mark Tenor API as legacy/existing-key-only after the Jan 2026 new-client cutoff, and judge internal samples primarily by human fun/retention rather than technical correctness alone — see `references/youtube-agent-storytime-static-png-transform-and-review-routing.md`. For Storytime reference/material library hygiene — especially quarantining user submissions, separating yt-dlp references from licensed production candidates, and correcting downloaded examples to `YELLOW_INTERNAL_REFERENCE_ONLY` — see `references/youtube-agent-storytime-reference-library.md`. For the newer Storytime SFX-audition pattern — catalog first/classify second, record download dates, build an upload-free MP4 cue-sheet/provenance packet with quarantined sound effects, and ask Claude Code for visual + evidence-based audio review — see `references/youtube-agent-storytime-sfx-audition-review.md`.

Reference note: for youtube_agent exact-artifact uploads/schedules/canary promotion after subtitle/voice sync regressions, use `references/youtube-agent-pre-upload-mp4-review-gate.md`: require Claude Code or timing-capable MP4 review with explicit `APPROVE_FOR_UPLOAD` / `REVISE_BEFORE_UPLOAD` / `BLOCK_UPLOAD` verdict before upload or scheduling. The reference also includes the safe scheduled exact-artifact pattern: contact sheet, metadata verdict, OAuth destination guard, `upload-existing-scheduled` approval phrase, and YouTube API read-back verification.

Reference note: for upstream topic-intelligence / planning-gate work where the user asks to lean harder on Claude Code usage, use Claude Code for two independent read-only reviews (engineering + product/safety) before a bounded TDD implementation, then have Hermes verify tests and artifact contents locally. See `references/upstream-planning-gate-claude-code-review-implementation.md`.

Delegate coding tasks to [Claude Code](https://code.claude.com/docs/en/cli-reference) (Anthropic's autonomous coding agent CLI) via the Hermes terminal. Claude Code v2.x can read files, write code, run shell commands, spawn subagents, and manage git workflows autonomously.

## Prerequisites

- **Install:** `npm install -g @anthropic-ai/claude-code`
- **Auth:** run `claude` once to log in (browser OAuth for Pro/Max, or set `ANTHROPIC_API_KEY`)
- **Console auth:** `claude auth login --console` for API key billing
- **SSO auth:** `claude auth login --sso` for Enterprise
- **Check status:** `claude auth status` (JSON) or `claude auth status --text` (human-readable)
- **Health check:** `claude doctor` — checks auto-updater and installation health
- **Version check:** `claude --version` (requires v2.x+)
- **Update:** `claude update` or `claude upgrade`

## API-Key-Aware Routing

When the user wants to balance GPT/Codex usage but preserve `ANTHROPIC_API_KEY` for a specific application path (for example YouTube script generation), do **not** solve that by moving Hermes/global scheduled agents onto the Anthropic API provider. Prefer Claude Code CLI when it is authenticated through Claude Pro/Max OAuth:

1. Verify auth mode with `claude auth status --text` and avoid printing secrets.
2. If status shows a Pro/Max/OAuth login, route implementation-heavy build work to Claude Code print mode or the project wrapper.
3. Keep Anthropic API-provider usage reserved for the user-designated path.
4. Use Codex/GPT for orchestration, focused independent engineering risk review, OpenAI-specific reasoning, narrow fixes, or fallback when Claude Code is blocked.
5. Hermes must still verify locally; never accept Claude Code self-reported tests without rerunning relevant checks.
6. For cybersecurity repositories, keep the safety gate with Hermes: Claude Code may implement bounded offline/local code, but must not decide scope, run live scans, touch targets, or modify secrets/scope/deployment settings unless a separately reviewed milestone explicitly allows it.
7. If the user questions why Claude Code usage is not moving, inspect the actual wrapper/pipeline route: policy text is insufficient if implementation still defaults to Codex. Add or use an explicit implementation command (for example `hermes claude-impl`) that writes raw Claude Code JSON usage artifacts.
8. Track future-only project worker mix separately from lifetime Hermes token history; Claude Code Pro/OAuth usage may not appear in `hermes insights`.

Use this pattern for project-level routing documents too: record the policy in the repo handoff/context files so future sessions do not regress to API-key-heavy routing. When a project has local worker wrappers, also update those wrappers so the desired ratio is operational rather than just documented: default full/build runs to Claude Code, expose an explicit Codex/GPT fallback flag, increase Claude Code max-turns for bounded build phases, include `Bash` when validation is expected, and write dry-run reports that prove the route.

## Two Orchestration Modes

Hermes interacts with Claude Code in two fundamentally different ways. Choose based on the task.

### Mode 1: Print Mode (`-p`) — Non-Interactive (PREFERRED for most tasks)

Print mode runs a one-shot task, returns the result, and exits. No PTY needed. No interactive prompts. This is the cleanest integration path.

```
terminal(command="claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10", workdir="/path/to/project", timeout=120)
```

**When to use print mode:**
- One-shot coding tasks (fix a bug, add a feature, refactor)
- CI/CD automation and scripting
- Structured data extraction with `--json-schema`
- Piped input processing (`cat file | claude -p "analyze this"`)
- Any task where you don't need multi-turn conversation

**Print mode skips ALL interactive dialogs** — no workspace trust prompt, no permission confirmations. This makes it ideal for automation.

### Mode 2: Interactive PTY via tmux — Multi-Turn Sessions

Interactive mode gives you a full conversational REPL where you can send follow-up prompts, use slash commands, and watch Claude work in real time. **Requires tmux orchestration.**

```
# Start a tmux session
terminal(command="tmux new-session -d -s claude-work -x 140 -y 40")

# Launch Claude Code inside it
terminal(command="tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter")

# Wait for startup, then send your task
# (after ~3-5 seconds for the welcome screen)
terminal(command="sleep 5 && tmux send-keys -t claude-work 'Refactor the auth module to use JWT tokens' Enter")

# Monitor progress by capturing the pane
terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -50")

# Send follow-up tasks
terminal(command="tmux send-keys -t claude-work 'Now add unit tests for the new JWT code' Enter")

# Exit when done
terminal(command="tmux send-keys -t claude-work '/exit' Enter")
```

**When to use interactive mode:**
- Multi-turn iterative work (refactor → review → fix → test cycle)
- Tasks requiring human-in-the-loop decisions
- Exploratory coding sessions
- When you need to use Claude's slash commands (`/compact`, `/review`, `/model`)

## PTY Dialog Handling (CRITICAL for Interactive Mode)

Claude Code presents up to two confirmation dialogs on first launch. You MUST handle these via tmux send-keys:

### Dialog 1: Workspace Trust (first visit to a directory)
```
❯ 1. Yes, I trust this folder    ← DEFAULT (just press Enter)
  2. No, exit
```
**Handling:** `tmux send-keys -t <session> Enter` — default selection is correct.

### Dialog 2: Bypass Permissions Warning (only with --dangerously-skip-permissions)
```
❯ 1. No, exit                    ← DEFAULT (WRONG choice!)
  2. Yes, I accept
```
**Handling:** Must navigate DOWN first, then Enter:
```
tmux send-keys -t <session> Down && sleep 0.3 && tmux send-keys -t <session> Enter
```

### Robust Dialog Handling Pattern
```
# Launch with permissions bypass
terminal(command="tmux send-keys -t claude-work 'claude --dangerously-skip-permissions \"your task\"' Enter")

# Handle trust dialog (Enter for default "Yes")
terminal(command="sleep 4 && tmux send-keys -t claude-work Enter")

# Handle permissions dialog (Down then Enter for "Yes, I accept")
terminal(command="sleep 3 && tmux send-keys -t claude-work Down && sleep 0.3 && tmux send-keys -t claude-work Enter")

# Now wait for Claude to work
terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -60")
```

**Note:** After the first trust acceptance for a directory, the trust dialog won't appear again. Only the permissions dialog recurs each time you use `--dangerously-skip-permissions`.

## CLI Subcommands

| Subcommand | Purpose |
|------------|---------|
| `claude` | Start interactive REPL |
| `claude "query"` | Start REPL with initial prompt |
| `claude -p "query"` | Print mode (non-interactive, exits when done) |
| `cat file \| claude -p "query"` | Pipe content as stdin context |
| `claude -c` | Continue the most recent conversation in this directory |
| `claude -r "id"` | Resume a specific session by ID or name |
| `claude auth login` | Sign in (add `--console` for API billing, `--sso` for Enterprise) |
| `claude auth status` | Check login status (returns JSON; `--text` for human-readable) |
| `claude mcp add <name> -- <cmd>` | Add an MCP server |
| `claude mcp list` | List configured MCP servers |
| `claude mcp remove <name>` | Remove an MCP server |
| `claude agents` | List configured agents |
| `claude doctor` | Run health checks on installation and auto-updater |
| `claude update` / `claude upgrade` | Update Claude Code to latest version |
| `claude remote-control` | Start server to control Claude from claude.ai or mobile app |
| `claude install [target]` | Install native build (stable, latest, or specific version) |
| `claude setup-token` | Set up long-lived auth token (requires subscription) |
| `claude plugin` / `claude plugins` | Manage Claude Code plugins |
| `claude auto-mode` | Inspect auto mode classifier configuration |

## Print Mode Deep Dive

### Structured JSON Output
```
terminal(command="claude -p 'Analyze auth.py for security issues' --output-format json --max-turns 5", workdir="/project", timeout=120)
```

Returns a JSON object with:
```json
{
  "type": "result",
  "subtype": "success",
  "result": "The analysis text...",
  "session_id": "75e2167f-...",
  "num_turns": 3,
  "total_cost_usd": 0.0787,
  "duration_ms": 10276,
  "stop_reason": "end_turn",
  "terminal_reason": "completed",
  "usage": { "input_tokens": 5, "output_tokens": 603, ... },
  "modelUsage": { "claude-sonnet-4-6": { "costUSD": 0.078, "contextWindow": 200000 } }
}
```

**Key fields:** `session_id` for resumption, `num_turns` for agentic loop count, `total_cost_usd` for spend tracking, `subtype` for success/error detection (`success`, `error_max_turns`, `error_budget`).

### Streaming JSON Output
For real-time token streaming, use `stream-json` with `--verbose`:
```
terminal(command="claude -p 'Write a summary' --output-format stream-json --verbose --include-partial-messages", timeout=60)
```

Returns newline-delimited JSON events. Filter with jq for live text:
```
claude -p "Explain X" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Stream events include `system/api_retry` with `attempt`, `max_retries`, and `error` fields (e.g., `rate_limit`, `billing_error`).

### Bidirectional Streaming
For real-time input AND output streaming:
```
claude -p "task" --input-format stream-json --output-format stream-json --replay-user-messages
```
`--replay-user-messages` re-emits user messages on stdout for acknowledgment.

### Piped Input
```
# Pipe a file for analysis
terminal(command="cat src/auth.py | claude -p 'Review this code for bugs' --max-turns 1", timeout=60)

# Pipe multiple files
terminal(command="cat src/*.py | claude -p 'Find all TODO comments' --max-turns 1", timeout=60)

# Pipe command output
terminal(command="git diff HEAD~3 | claude -p 'Summarize these changes' --max-turns 1", timeout=60)
```

### Read-only review packets that avoid max-turn churn
When using Claude Code as an independent reviewer, keep the packet intentionally small and forbid tool use in the prompt. If `git diff | claude -p ... --max-turns 3` returns `Error: Reached max turns`, do not rerun the same broad packet. Build a focused excerpt containing only the touched files/functions/tests and run a one-turn no-tools review:

```
{
  printf '%s\n' '=== src/module.py ==='
  sed -n '120,220p' src/module.py
  printf '%s\n' '=== tests/test_module.py ==='
  sed -n '1,220p' tests/test_module.py
} | claude -p "Read-only review of ONLY the provided excerpts. Do not use tools. Ignore unrelated repo diffs. Return concise: Verdict ACCEPT/REVISE; Blockers; Non-blocking notes; Safety; Validation gaps." --max-turns 1
```

For large working trees, this pattern prevents Claude from wandering into unrelated old diffs and yields a capturable review verdict for handoff logs.

### JSON Schema for Structured Extraction
```
terminal(command="claude -p 'List all functions in src/' --output-format json --json-schema '{\"type\":\"object\",\"properties\":{\"functions\":{\"type\":\"array\",\"items\":{\"type\":\"string\"}}},\"required\":[\"functions\"]}' --max-turns 5", workdir="/project", timeout=90)
```

Parse `structured_output` from the JSON result. Claude validates output against the schema before returning.

### Session Continuation
```
# Start a task
terminal(command="claude -p 'Start refactoring the database layer' --output-format json --max-turns 10 > /tmp/session.json", workdir="/project", timeout=180)

# Resume with session ID
terminal(command="claude -p 'Continue and add connection pooling' --resume $(cat /tmp/session.json | python3 -c 'import json,sys; print(json.load(sys.stdin)[\"session_id\"])') --max-turns 5", workdir="/project", timeout=120)

# Or resume the most recent session in the same directory
terminal(command="claude -p 'What did you do last time?' --continue --max-turns 1", workdir="/project", timeout=30)

# Fork a session (new ID, keeps history)
terminal(command="claude -p 'Try a different approach' --resume <id> --fork-session --max-turns 10", workdir="/project", timeout=120)
```

### Bare Mode for CI/Scripting
```
terminal(command="claude --bare -p 'Run all tests and report failures' --allowedTools 'Read,Bash' --max-turns 10", workdir="/project", timeout=180)
```

`--bare` skips hooks, plugins, MCP discovery, and CLAUDE.md loading. Fastest startup. Requires `ANTHROPIC_API_KEY` (skips OAuth).

To selectively load context in bare mode:
| To load | Flag |
|---------|------|
| System prompt additions | `--append-system-prompt "text"` or `--append-system-prompt-file path` |
| Settings | `--settings <file-or-json>` |
| MCP servers | `--mcp-config <file-or-json>` |
| Custom agents | `--agents '<json>'` |

### Fallback Model for Overload
```
terminal(command="claude -p 'task' --fallback-model haiku --max-turns 5", timeout=90)
```
Automatically falls back to the specified model when the default is overloaded (print mode only).

## Complete CLI Flags Reference

### Session & Environment
| Flag | Effect |
|------|--------|
| `-p, --print` | Non-interactive one-shot mode (exits when done) |
| `-c, --continue` | Resume most recent conversation in current directory |
| `-r, --resume <id>` | Resume specific session by ID or name (interactive picker if no ID) |
| `--fork-session` | When resuming, create new session ID instead of reusing original |
| `--session-id <uuid>` | Use a specific UUID for the conversation |
| `--no-session-persistence` | Don't save session to disk (print mode only) |
| `--add-dir <paths...>` | Grant Claude access to additional working directories |
| `-w, --worktree [name]` | Run in an isolated git worktree at `.claude/worktrees/<name>` |
| `--tmux` | Create a tmux session for the worktree (requires `--worktree`) |
| `--ide` | Auto-connect to a valid IDE on startup |
| `--chrome` / `--no-chrome` | Enable/disable Chrome browser integration for web testing |
| `--from-pr [number]` | Resume session linked to a specific GitHub PR |
| `--file <specs...>` | File resources to download at startup (format: `file_id:relative_path`) |

### Model & Performance
| Flag | Effect |
|------|--------|
| `--model <alias>` | Model selection: `sonnet`, `opus`, `haiku`, or full name like `claude-sonnet-4-6` |
| `--effort <level>` | Reasoning depth: `low`, `medium`, `high`, `max`, `auto` | Both |
| `--max-turns <n>` | Limit agentic loops (print mode only; prevents runaway) |
| `--max-budget-usd <n>` | Cap API spend in dollars (print mode only) |
| `--fallback-model <model>` | Auto-fallback when default model is overloaded (print mode only) |
| `--betas <betas...>` | Beta headers to include in API requests (API key users only) |

### Permission & Safety
| Flag | Effect |
|------|--------|
| `--dangerously-skip-permissions` | Auto-approve ALL tool use (file writes, bash, network, etc.) |
| `--allow-dangerously-skip-permissions` | Enable bypass as an *option* without enabling it by default |
| `--permission-mode <mode>` | `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` |
| `--allowedTools <tools...>` | Whitelist specific tools (comma or space-separated) |
| `--disallowedTools <tools...>` | Blacklist specific tools |
| `--tools <tools...>` | Override built-in tool set (`""` = none, `"default"` = all, or tool names) |

### Output & Input Format
| Flag | Effect |
|------|--------|
| `--output-format <fmt>` | `text` (default), `json` (single result object), `stream-json` (newline-delimited) |
| `--input-format <fmt>` | `text` (default) or `stream-json` (real-time streaming input) |
| `--json-schema <schema>` | Force structured JSON output matching a schema |
| `--verbose` | Full turn-by-turn output |
| `--include-partial-messages` | Include partial message chunks as they arrive (stream-json + print) |
| `--replay-user-messages` | Re-emit user messages on stdout (stream-json bidirectional) |

### System Prompt & Context
| Flag | Effect |
|------|--------|
| `--append-system-prompt <text>` | **Add** to the default system prompt (preserves built-in capabilities) |
| `--append-system-prompt-file <path>` | **Add** file contents to the default system prompt |
| `--system-prompt <text>` | **Replace** the entire system prompt (use --append instead usually) |
| `--system-prompt-file <path>` | **Replace** the system prompt with file contents |
| `--bare` | Skip hooks, plugins, MCP discovery, CLAUDE.md, OAuth (fastest startup) |
| `--agents '<json>'` | Define custom subagents dynamically as JSON |
| `--mcp-config <path>` | Load MCP servers from JSON file (repeatable) |
| `--strict-mcp-config` | Only use MCP servers from `--mcp-config`, ignoring all other MCP configs |
| `--settings <file-or-json>` | Load additional settings from a JSON file or inline JSON |
| `--setting-sources <sources>` | Comma-separated sources to load: `user`, `project`, `local` |
| `--plugin-dir <paths...>` | Load plugins from directories for this session only |
| `--disable-slash-commands` | Disable all skills/slash commands |

### Debugging
| Flag | Effect |
|------|--------|
| `-d, --debug [filter]` | Enable debug logging with optional category filter (e.g., `"api,hooks"`, `"!1p,!file"`) |
| `--debug-file <path>` | Write debug logs to file (implicitly enables debug mode) |

### Agent Teams
| Flag | Effect |
|------|--------|
| `--teammate-mode <mode>` | How agent teams display: `auto`, `in-process`, or `tmux` |
| `--brief` | Enable `SendUserMessage` tool for agent-to-user communication |

### Tool Name Syntax for --allowedTools / --disallowedTools
```
Read                    # All file reading
Edit                    # File editing (existing files)
Write                   # File creation (new files)
Bash                    # All shell commands
Bash(git *)             # Only git commands
Bash(git commit *)      # Only git commit commands
Bash(npm run lint:*)    # Pattern matching with wildcards
WebSearch               # Web search capability
WebFetch                # Web page fetching
mcp__<server>__<tool>   # Specific MCP tool
```

## Settings & Configuration

### Settings Hierarchy (highest to lowest priority)
1. **CLI flags** — override everything
2. **Local project:** `.claude/settings.local.json` (personal, gitignored)
3. **Project:** `.claude/settings.json` (shared, git-tracked)
4. **User:** `~/.claude/settings.json` (global)

### Permissions in Settings
```json
{
  "permissions": {
    "allow": ["Bash(npm run lint:*)", "WebSearch", "Read"],
    "ask": ["Write(*.ts)", "Bash(git push*)"],
    "deny": ["Read(.env)", "Bash(rm -rf *)"]
  }
}
```

### Memory Files (CLAUDE.md) Hierarchy
1. **Global:** `~/.claude/CLAUDE.md` — applies to all projects
2. **Project:** `./CLAUDE.md` — project-specific context (git-tracked)
3. **Local:** `.claude/CLAUDE.local.md` — personal project overrides (gitignored)

Use the `#` prefix in interactive mode to quickly add to memory: `# Always use 2-space indentation`.

## Interactive Session: Slash Commands

### Session & Context
| Command | Purpose |
|---------|---------|
| `/help` | Show all commands (including custom and MCP commands) |
| `/compact [focus]` | Compress context to save tokens; CLAUDE.md survives compaction. E.g., `/compact focus on auth logic` |
| `/clear` | Wipe conversation history for a fresh start |
| `/context` | Visualize context usage as a colored grid with optimization tips |
| `/cost` | View token usage with per-model and cache-hit breakdowns |
| `/resume` | Switch to or resume a different session |
| `/rewind` | Revert to a previous checkpoint in conversation or code |
| `/btw <question>` | Ask a side question without adding to context cost |
| `/status` | Show version, connectivity, and session info |
| `/todos` | List tracked action items from the conversation |
| `/exit` or `Ctrl+D` | End session |

### Development & Review
| Command | Purpose |
|---------|---------|
| `/review` | Request code review of current changes |
| `/security-review` | Perform security analysis of current changes |
| `/plan [description]` | Enter Plan mode with auto-start for task planning |
| `/loop [interval]` | Schedule recurring tasks within the session |
| `/batch` | Auto-create worktrees for large parallel changes (5-30 worktrees) |

### Configuration & Tools
| Command | Purpose |
|---------|---------|
| `/model [model]` | Switch models mid-session (use arrow keys to adjust effort) |
| `/effort [level]` | Set reasoning effort: `low`, `medium`, `high`, `max`, or `auto` |
| `/init` | Create a CLAUDE.md file for project memory |
| `/memory` | Open CLAUDE.md for editing |
| `/config` | Open interactive settings configuration |
| `/permissions` | View/update tool permissions |
| `/agents` | Manage specialized subagents |
| `/mcp` | Interactive UI to manage MCP servers |
| `/add-dir` | Add additional working directories (useful for monorepos) |
| `/usage` | Show plan limits and rate limit status |
| `/voice` | Enable push-to-talk voice mode (20 languages; hold Space to record, release to send) |
| `/release-notes` | Interactive picker for version release notes |

### Custom Slash Commands
Create `.claude/commands/<name>.md` (project-shared) or `~/.claude/commands/<name>.md` (personal):

```markdown
# .claude/commands/deploy.md
Run the deploy pipeline:
1. Run all tests
2. Build the Docker image
3. Push to registry
4. Update the $ARGUMENTS environment (default: staging)
```

Usage: `/deploy production` — `$ARGUMENTS` is replaced with the user's input.

### Skills (Natural Language Invocation)
Unlike slash commands (manually invoked), skills in `.claude/skills/` are markdown guides that Claude invokes automatically via natural language when the task matches:

```markdown
# .claude/skills/database-migration.md
When asked to create or modify database migrations:
1. Use Alembic for migration generation
2. Always create a rollback function
3. Test migrations against a local database copy
```

## Interactive Session: Keyboard Shortcuts

### General Controls
| Key | Action |
|-----|--------|
| `Ctrl+C` | Cancel current input or generation |
| `Ctrl+D` | Exit session |
| `Ctrl+R` | Reverse search command history |
| `Ctrl+B` | Background a running task |
| `Ctrl+V` | Paste image into conversation |
| `Ctrl+O` | Transcript mode — see Claude's thinking process |
| `Ctrl+G` or `Ctrl+X Ctrl+E` | Open prompt in external editor |
| `Esc Esc` | Rewind conversation or code state / summarize |

### Mode Toggles
| Key | Action |
|-----|--------|
| `Shift+Tab` | Cycle permission modes (Normal → Auto-Accept → Plan) |
| `Alt+P` | Switch model |
| `Alt+T` | Toggle thinking mode |
| `Alt+O` | Toggle Fast Mode |

### Multiline Input
| Key | Action |
|-----|--------|
| `\` + `Enter` | Quick newline |
| `Shift+Enter` | Newline (alternative) |
| `Ctrl+J` | Newline (alternative) |

### Input Prefixes
| Prefix | Action |
|--------|--------|
| `!` | Execute bash directly, bypassing AI (e.g., `!npm test`). Use `!` alone to toggle shell mode. |
| `@` | Reference files/directories with autocomplete (e.g., `@./src/api/`) |
| `#` | Quick add to CLAUDE.md memory (e.g., `# Use 2-space indentation`) |
| `/` | Slash commands |

### Pro Tip: "ultrathink"
Use the keyword "ultrathink" in your prompt for maximum reasoning effort on a specific turn. This triggers the deepest thinking mode regardless of the current `/effort` setting.

## PR Review Pattern

### Quick Review (Print Mode)
```
terminal(command="cd /path/to/repo && git diff main...feature-branch | claude -p 'Review this diff for bugs, security issues, and style problems. Be thorough.' --max-turns 1", timeout=60)
```

### Deep Review (Interactive + Worktree)
```
terminal(command="tmux new-session -d -s review -x 140 -y 40")
terminal(command="tmux send-keys -t review 'cd /path/to/repo && claude -w pr-review' Enter")
terminal(command="sleep 5 && tmux send-keys -t review Enter")  # Trust dialog
terminal(command="sleep 2 && tmux send-keys -t review 'Review all changes vs main. Check for bugs, security issues, race conditions, and missing tests.' Enter")
terminal(command="sleep 30 && tmux capture-pane -t review -p -S -60")
```

### PR Review from Number
```
terminal(command="claude -p 'Review this PR thoroughly' --from-pr 42 --max-turns 10", workdir="/path/to/repo", timeout=120)
```

### Claude Worktree with tmux
```
terminal(command="claude -w feature-x --tmux", workdir="/path/to/repo")
```
Creates an isolated git worktree at `.claude/worktrees/feature-x` AND a tmux session for it. Uses iTerm2 native panes when available; add `--tmux=classic` for traditional tmux.

## Parallel Claude Instances

Run multiple independent Claude tasks simultaneously:

```
# Task 1: Fix backend
terminal(command="tmux new-session -d -s task1 -x 140 -y 40 && tmux send-keys -t task1 'cd ~/project && claude -p \"Fix the auth bug in src/auth.py\" --allowedTools \"Read,Edit\" --max-turns 10' Enter")

# Task 2: Write tests
terminal(command="tmux new-session -d -s task2 -x 140 -y 40 && tmux send-keys -t task2 'cd ~/project && claude -p \"Write integration tests for the API endpoints\" --allowedTools \"Read,Write,Bash\" --max-turns 15' Enter")

# Task 3: Update docs
terminal(command="tmux new-session -d -s task3 -x 140 -y 40 && tmux send-keys -t task3 'cd ~/project && claude -p \"Update README.md with the new API endpoints\" --allowedTools \"Read,Edit\" --max-turns 5' Enter")

# Monitor all
terminal(command="sleep 30 && for s in task1 task2 task3; do echo '=== '$s' ==='; tmux capture-pane -t $s -p -S -5 2>/dev/null; done")
```

See `references/large-phased-implementation.md` for the reusable phased-delegation pattern when Claude Code is the primary implementation worker and Codex/OpenAI quota should be conserved.

See `references/safe-periodic-third-party-reviews.md` for the recurring/offline review pattern where Claude Code performs independent strategy/quality review from a safe packet and Hermes writes a separate synthesis before any implementation.

## CLAUDE.md — Project Context File

Claude Code auto-loads `CLAUDE.md` from the project root. Use it to persist project context:

```markdown
# Project: My API

## Architecture
- FastAPI backend with SQLAlchemy ORM
- PostgreSQL database, Redis cache
- pytest for testing with 90% coverage target

## Key Commands
- `make test` — run full test suite
- `make lint` — ruff + mypy
- `make dev` — start dev server on :8000

## Code Standards
- Type hints on all public functions
- Docstrings in Google style
- 2-space indentation for YAML, 4-space for Python
- No wildcard imports
```

**Be specific.** Instead of "Write good code", use "Use 2-space indentation for JS" or "Name test files with `.test.ts` suffix." Specific instructions save correction cycles.

### Rules Directory (Modular CLAUDE.md)
For projects with many rules, use the rules directory instead of one massive CLAUDE.md:
- **Project rules:** `.claude/rules/*.md` — team-shared, git-tracked
- **User rules:** `~/.claude/rules/*.md` — personal, global

Each `.md` file in the rules directory is loaded as additional context. This is cleaner than cramming everything into a single CLAUDE.md.

### Auto-Memory
Claude automatically stores learned project context in `~/.claude/projects/<project>/memory/`.
- **Limit:** 25KB or 200 lines per project
- This is separate from CLAUDE.md — it's Claude's own notes about the project, accumulated across sessions

## Custom Subagents

Define specialized agents in `.claude/agents/` (project), `~/.claude/agents/` (personal), or via `--agents` CLI flag (session):

### Agent Location Priority
1. `.claude/agents/` — project-level, team-shared
2. `--agents` CLI flag — session-specific, dynamic
3. `~/.claude/agents/` — user-level, personal

### Creating an Agent
```markdown
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Security-focused code review
model: opus
tools: [Read, Bash]
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication/authorization flaws
- Secrets in code
- Unsafe deserialization
```

Invoke via: `@security-reviewer review the auth module`

### Dynamic Agents via CLI
```
terminal(command="claude --agents '{\"reviewer\": {\"description\": \"Reviews code\", \"prompt\": \"You are a code reviewer focused on performance\"}}' -p 'Use @reviewer to check auth.py'", timeout=120)
```

Claude can orchestrate multiple agents: "Use @db-expert to optimize queries, then @security to audit the changes."

## Hooks — Automation on Events

Configure in `.claude/settings.json` (project) or `~/.claude/settings.json` (global):

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write(*.py)",
      "hooks": [{"type": "command", "command": "ruff check --fix $CLAUDE_FILE_PATHS"}]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'rm -rf'; then echo 'Blocked!' && exit 2; fi"}]
    }],
    "Stop": [{
      "hooks": [{"type": "command", "command": "echo 'Claude finished a response' >> /tmp/claude-activity.log"}]
    }]
  }
}
```

### All 8 Hook Types
| Hook | When it fires | Common use |
|------|--------------|------------|
| `UserPromptSubmit` | Before Claude processes a user prompt | Input validation, logging |
| `PreToolUse` | Before tool execution | Security gates, block dangerous commands (exit 2 = block) |
| `PostToolUse` | After a tool finishes | Auto-format code, run linters |
| `Notification` | On permission requests or input waits | Desktop notifications, alerts |
| `Stop` | When Claude finishes a response | Completion logging, status updates |
| `SubagentStop` | When a subagent completes | Agent orchestration |
| `PreCompact` | Before context memory is cleared | Backup session transcripts |
| `SessionStart` | When a session begins | Load dev context (e.g., `git status`) |

### Hook Environment Variables
| Variable | Content |
|----------|---------|
| `CLAUDE_PROJECT_DIR` | Current project path |
| `CLAUDE_FILE_PATHS` | Files being modified |
| `CLAUDE_TOOL_INPUT` | Tool parameters as JSON |

### Security Hook Examples
```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{"type": "command", "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf|git push.*--force|:(){ :|:& };:'; then echo 'Dangerous command blocked!' && exit 2; fi"}]
  }]
}
```

## MCP Integration

Add external tool servers for databases, APIs, and services:

```
# GitHub integration
terminal(command="claude mcp add -s user github -- npx @modelcontextprotocol/server-github", timeout=30)

# PostgreSQL queries
terminal(command="claude mcp add -s local postgres -- npx @anthropic-ai/server-postgres --connection-string postgresql://localhost/mydb", timeout=30)

# Puppeteer for web testing
terminal(command="claude mcp add puppeteer -- npx @anthropic-ai/server-puppeteer", timeout=30)
```

### MCP Scopes
| Flag | Scope | Storage |
|------|-------|---------|
| `-s user` | Global (all projects) | `~/.claude.json` |
| `-s local` | This project (personal) | `.claude/settings.local.json` (gitignored) |
| `-s project` | This project (team-shared) | `.claude/settings.json` (git-tracked) |

### MCP in Print/CI Mode
```
terminal(command="claude --bare -p 'Query database' --mcp-config mcp-servers.json --strict-mcp-config", timeout=60)
```
`--strict-mcp-config` ignores all MCP servers except those from `--mcp-config`.

Reference MCP resources in chat: `@github:issue://123`

### MCP Limits & Tuning
- **Tool descriptions:** 2KB cap per server for tool descriptions and server instructions
- **Result size:** Default capped; use `maxResultSizeChars` annotation to allow up to **500K** characters for large outputs
- **Output tokens:** `export MAX_MCP_OUTPUT_TOKENS=50000` — cap output from MCP servers to prevent context flooding
- **Transports:** `stdio` (local process), `http` (remote), `sse` (server-sent events)

## Monitoring Interactive Sessions

### Reading the TUI Status
```
# Periodic capture to check if Claude is still working or waiting for input
terminal(command="tmux capture-pane -t dev -p -S -10")
```

Look for these indicators:
- `❯` at bottom = waiting for your input (Claude is done or asking a question)
- `●` lines = Claude is actively using tools (reading, writing, running commands)
- `⏵⏵ bypass permissions on` = status bar showing permissions mode
- `◐ medium · /effort` = current effort level in status bar
- `ctrl+o to expand` = tool output was truncated (can be expanded interactively)

### Context Window Health
Use `/context` in interactive mode to see a colored grid of context usage. Key thresholds:
- **< 70%** — Normal operation, full precision
- **70-85%** — Precision starts dropping, consider `/compact`
- **> 85%** — Hallucination risk spikes significantly, use `/compact` or `/clear`

## Environment Variables

| Variable | Effect |
|----------|--------|
| `ANTHROPIC_API_KEY` | API key for authentication (alternative to OAuth) |
| `CLAUDE_CODE_EFFORT_LEVEL` | Default effort: `low`, `medium`, `high`, `max`, or `auto` |
| `MAX_THINKING_TOKENS` | Cap thinking tokens (set to `0` to disable thinking entirely) |
| `MAX_MCP_OUTPUT_TOKENS` | Cap output from MCP servers (default varies; set e.g., `50000`) |
| `CLAUDE_CODE_NO_FLICKER=1` | Enable alt-screen rendering to eliminate terminal flicker |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | Strip credentials from sub-processes for security |

## Cost & Performance Tips

0. **Respect API-key reservation policies** — if the user reserves `ANTHROPIC_API_KEY` for another project or a specific application path, do not spend it on routine coding or routine review. Use Claude Code Pro/OAuth for build work instead of switching Hermes cron jobs, global model config, or review workers onto Anthropic API billing. Verify with `claude auth status --text`, record the routing rule in project handoff/context files, and keep Hermes as the local verifier. For Hermes-style projects with worker wrappers, make the routing executable: default full/build pipelines to Claude Code, keep a clear `ImplementationWorker=codex`-style fallback, cap API-backed Claude/Cowork to rare high-value T3+ design/safety/report review (0-3% preferred; 5% ceiling without explicit user approval), and add a status file that tracks the target mix because `hermes insights` may not count Claude Code Pro/OAuth usage.
1. **Lean on Claude Code when conserving GPT/OpenAI quota** — if the user says GPT weekly limits are tight or asks to use Claude more, route review passes, safety audits, and large coding sub-tasks through Claude Code print mode where appropriate, then summarize results back in the main agent.
1. **Split large implementation rungs into small phases before delegating** — if a wrapper or print-mode task hits `Error: Reached max turns`, do not keep rerunning the same monolithic prompt. Inspect partial workspace changes, verify what landed, then delegate the next narrow phase (for example schema+tests, then audio fixture, then renderer, then gate). This conserves both Claude and GPT/Codex budget and avoids losing useful partial work.
2. **Use `--max-turns`** in print mode to prevent runaway loops. Start with 5-10 for most tasks, but raise it deliberately (e.g. 25-35) for contained implementation phases that include tests.
3. **Prefer direct print-mode invocation when a project wrapper is too constrained** — if a wrapper hard-codes too few turns or too few tools for the task, run Claude Code directly with the task file content, e.g. `claude -p "$(cat handoff/phase_task.md)" --max-turns 25 --allowedTools 'Read,Edit,Write,Bash,Grep,Glob' < /dev/null`, then record the result in the project's handoff files.
4. **Use `--max-budget-usd`** for cost caps. Note: minimum ~$0.05 for system prompt cache creation.
5. **Use `--effort low`** for simple tasks (faster, cheaper). `high` or `max` for complex reasoning.
6. **Use `--bare`** for CI/scripting to skip plugin/hook discovery overhead.
7. **Use `--allowedTools`** to restrict to only what's needed (e.g., `Read` only for reviews); include `Bash` when the worker is expected to run tests or inspect generated artifacts.
8. **Use `/compact`** in interactive sessions when context gets large.
9. **Pipe input** instead of having Claude read files when you just need analysis of known content.
10. **Use `--model haiku`** for simple tasks (cheaper) and `--model opus` for complex multi-step work.
11. **Use `--fallback-model haiku`** in print mode to gracefully handle model overload.
10. **Start new sessions for distinct tasks** — sessions last 5 hours; fresh context is more efficient.
11. **Use `--no-session-persistence`** in CI to avoid accumulating saved sessions on disk.
12. **Split large implementation rungs into phase-sized Claude Code tasks** — when conserving GPT/OpenAI/Codex quota, route implementation through Claude Code but keep each print-mode task small enough to finish (schema/tests, fixture generator, renderer, gate, etc.). If a project wrapper hard-codes a low `--max-turns` or narrow tool allowlist, bypass it with a direct `claude -p "$(cat task.md)" --max-turns <larger> --allowedTools 'Read,Edit,Write,Bash,Grep,Glob' < /dev/null` call, then run local verification yourself.

## Pitfalls & Gotchas

0. **Installed is not the same as automation-ready** — wrapper/doctor checks may find `claude.exe` and `claude --version` may succeed, but non-interactive workers can still fail if Claude Code is not authenticated in the execution context. If a project worker or pipeline output says `Not logged in · Please run /login`, inspect the worker result/report (for example `handoff/claude_code_result.md` / `handoff/hermes_run.md` in Hermes-style projects), tell the user to run `claude` interactively and complete `/login`, then rerun the pipeline. Do not keep retrying the same worker just because the doctor check is green.
1. **Interactive mode REQUIRES tmux** — Claude Code is a full TUI app. Using `pty=true` alone in Hermes terminal works but tmux gives you `capture-pane` for monitoring and `send-keys` for input, which is essential for orchestration.
2. **`--dangerously-skip-permissions` dialog defaults to "No, exit"** — you must send Down then Enter to accept. Print mode (`-p`) skips this entirely.
3. **`--max-budget-usd` minimum is ~$0.05** — system prompt cache creation alone costs this much. Setting lower will error immediately.
4. **`--max-turns` is print-mode only** — ignored in interactive sessions.
5. **Claude may use `python` instead of `python3`** — on systems without a `python` symlink, Claude's bash commands will fail on first try but it self-corrects.
6. **Session resumption requires same directory** — `--continue` finds the most recent session for the current working directory.
7. **`--json-schema` needs enough `--max-turns`** — Claude must read files before producing structured output, which takes multiple turns.
8. **Trust dialog only appears once per directory** — first-time only, then cached.
9. **Background tmux sessions persist** — always clean up with `tmux kill-session -t <name>` when done.
10. **Slash commands (like `/commit`) only work in interactive mode** — in `-p` mode, describe the task in natural language instead.
11. **`--bare` skips OAuth** — requires `ANTHROPIC_API_KEY` env var or an `apiKeyHelper` in settings.
13. **Max-turn failures can still leave useful workspace changes** — if Claude Code exits with `Error: Reached max turns`, do not assume nothing happened. Immediately inspect `git status`, search for expected new files/symbols, read changed files, and run focused tests. Continue from the actual workspace state: add missing tests or surgical fixes yourself, then record the wrapper failure separately from the verified project result.
14. **PowerShell wrappers may mishandle print-mode stdin/output** — if a wrapper invokes `claude -p $Prompt` and logs only `Warning: no stdin data received` or truncates at a hard-coded turn limit, use direct CLI invocation from the project shell with `< /dev/null`, explicit `--max-turns`, and an expanded allowlist. Treat the wrapper issue as orchestration friction, not as evidence that Claude Code cannot implement the task.
15. **Plan/account usage is not reliably available from print-mode slash commands** — `claude -p '/usage'` may not show the same plan-limit UI as interactive Claude Code. For account/plan remaining usage, ask the user to check interactive `/usage` or the account UI. For project accounting, parse `--output-format json` run results (`usage`, `modelUsage`, `total_cost_usd`, `terminal_reason`) and record worker route in handoff files.
16. **Claude Code can produce useful implementation before max-turn exit but miss tests/handoff details** — after `error_max_turns`, inspect actual changed files and finish missing tests/verification with Hermes or a narrower follow-up prompt. In safety-sensitive repos, prefer Hermes adding/repairing focused tests over asking Claude Code to continue a broad task blindly. For Hermes-style cybersec wrappers, also make sure the human result file (for example `handoff/claude_code_result.md`) is created even when raw JSON reports `subtype: error_max_turns`; see `references/cybersec-claude-impl-default-routing.md`.

## Rules for Hermes Agents

1. **Prefer print mode (`-p`) for single tasks** — cleaner, no dialog handling, structured output
2. **Use tmux for multi-turn interactive work** — the only reliable way to orchestrate the TUI
3. **Always set `workdir`** — keep Claude focused on the right project directory
4. **Set `--max-turns` in print mode** — prevents infinite loops and runaway costs
5. **Monitor tmux sessions** — use `tmux capture-pane -t <session> -p -S -50` to check progress
6. **Look for the `❯` prompt** — indicates Claude is waiting for input (done or asking a question)
7. **Clean up tmux sessions** — kill them when done to avoid resource leaks
8. **Report results to user** — after completion, summarize what Claude did and what changed
9. **Don't kill slow sessions** — Claude may be doing multi-step work; check progress instead
10. **Use `--allowedTools`** — restrict capabilities to what the task actually needs
