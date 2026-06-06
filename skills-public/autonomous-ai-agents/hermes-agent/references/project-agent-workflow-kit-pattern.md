> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Project Agent Workflow Kit Pattern

Use this reference when adapting Hermes Agent to coordinate external agents across multiple long-lived projects.

## Source pattern

A durable multi-agent project kit emerged from comparing three mature local projects:

- Cybersecurity lab project: strong gates, route policy, recoverable one-vulnerability modules, explicit strategy queue.
- YouTube automation project: private-first workflow, upload/publish gates, multi-agent collaboration policy, active strategy queue.
- AD platform project: source architecture extraction, campaign/creative/analytics gates, handoff-first architecture notes.

The common reusable pattern is not “add more agents.” It is a coordinator-owned workflow skeleton that prevents state drift and role confusion.

## Recommended project kit files

At project root, install or maintain:

- `.hermes.md` — compact project operating contract and activation gates.
- `agent_workflow.json` — machine-readable worker routing, authority order, review tiers, and blocked actions.
- `handoff/active_strategy_queue.md` — current phase, next action, route map, blocked actions, approval gates.
- `handoff/hermes_workflow.md` — human-readable workflow discipline.
- `handoff/claude_code_task.md` — bounded implementation prompt for Claude Code or equivalent implementation worker.
- `handoff/hermes_run.md` — latest convenience run report; archive before overwrite.
- `handoff/archive/rolling/` — old rolling files, not the source of truth.

## Authority and role split

Default authority order:

1. User explicit instruction and project safety gates.
2. Project `.hermes.md` / `agent_workflow.json` / active strategy queue.
3. Domain handoff files and project memory.
4. Worker output.
5. Hermes final verification.

Default roles:

- Hermes: coordinator, safety gate, final verifier, memory/router hygiene owner.
- Cowork/Claude strategy worker: strategy, architecture, creative alternatives, independent review.
- Claude Code implementation worker: larger bounded implementation tasks.
- Codex/GPT worker: focused engineering review, narrow fix, tests, fallback implementation.

Keep strategy workers and implementation workers separate. Do not let one rolling `cowork_result.md` become both strategy, implementation, and accepted history.

## Standard workflow

1. Read `.hermes.md`, `agent_workflow.json`, and `handoff/active_strategy_queue.md` first.
2. Identify the phase, gate, allowed routes, and blocked actions before spawning workers.
3. For strategy/spec work, ask a strategy/review worker for options or critique.
4. For implementation-heavy work, create a bounded implementation task file and send it to Claude Code if available; otherwise use Codex/GPT fallback.
5. Run independent review after implementation.
6. Hermes performs final verification, resolves disagreement, and updates durable handoff/state.
7. Archive rolling outputs before overwriting them.

## Review requirements

A final review artifact should label:

- route/tool used;
- visible model/runtime when available, or explicit uncertainty when hidden;
- input artifact path;
- changed files / output artifacts;
- verification commands or checks;
- final decision: accept, revise, block, or ask human;
- blocked actions and any approval gate still required.

## Pitfalls

- Do not treat rolling files as durable truth. They are convenience pointers only.
- Do not blur Cowork/Claude strategy output with Claude Code implementation output.
- Do not claim a multi-party/tiered review happened unless the evidence exists.
- Do not move from private/local to publish/deploy/upload/attack execution without the project-specific gate.
- Do not save raw project targets, secrets, credentials, scans, or private artifacts into global memory; route them to repo handoff or project-scoped notes.

## Smoke-test pattern for a workflow kit

When safe, validate the kit by installing it into a temporary project and running doctor/dry-run modes only. On Windows from a bash-backed Hermes terminal, invoke PowerShell scripts with forward-slash paths or quoted `./script.ps1` paths.

Example manual test shape:

```powershell
$TempProject = Join-Path $env:TEMP "hermes-kit-test"
Remove-Item -Recurse -Force $TempProject -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $TempProject | Out-Null

powershell -NoProfile -ExecutionPolicy Bypass -File "<user-home>" -ProjectPath $TempProject -ProjectName "Kit Test" -Preset generic
powershell -NoProfile -ExecutionPolicy Bypass -File "$TempProject/run_agent_worker.ps1" -Doctor
powershell -NoProfile -ExecutionPolicy Bypass -File "$TempProject/run_agent_pipeline.ps1" -Mode status -DryRun
```

If the terminal approval layer blocks a smoke test and says not to retry, record the unverified step in the report instead of retrying.