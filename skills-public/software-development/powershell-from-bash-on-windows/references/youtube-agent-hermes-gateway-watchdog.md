> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Hermes Gateway watchdog for YouTube Agent cron reliability

Use when the YouTube Agent has Hermes cron jobs configured, but scheduled production/report jobs did not fire because the Hermes Gateway/scheduler process was not running. This is a Windows control-plane pattern: Windows Task Scheduler keeps Hermes Gateway alive; Hermes cron remains the source of truth for the actual project jobs.

## Durable lesson

Hermes cron jobs only tick while `hermes gateway run` is alive. A cron job can be correctly configured and still miss its scheduled time if Gateway is not running. On Windows, the robust fix is usually a small Scheduled Task watchdog that periodically starts Gateway if missing, rather than duplicating project production loops in Windows Task Scheduler.

## Diagnostic sequence

1. Check live time and project root so the scheduler timestamps are interpreted correctly.
2. Inspect Hermes status:
   - `hermes gateway status`
   - `hermes cron status`
   - `hermes cron list`
3. If status says Gateway is not running, inspect Hermes logs under the active profile, especially `gateway.log` and `agent.log`, to distinguish missed cron ticks from job failures.
4. Inspect Windows Task Scheduler separately. A disabled stale production-loop task is not a replacement for Hermes cron; do not re-enable it unless the user explicitly authorizes that scheduling model.
5. Check `.agent.lock` by PID before deciding a production job is still running or stuck.

## Watchdog pattern

Create a project script such as `scripts/start_hermes_gateway_if_needed.ps1` that:

- Uses the full path to the active Hermes executable, e.g. `%LOCALAPPDATA%\hermes\hermes-agent\venv\Scripts\hermes.exe`.
- Looks for an existing `hermes gateway run` process and no-ops if found.
- Starts `hermes.exe gateway run --replace` only when missing.
- Writes a small log such as `%LOCALAPPDATA%\hermes\logs\gateway-watchdog.log` with `START`, `OK already running`, and failure lines.
- Does not run YouTube production commands itself.

Register a Windows Scheduled Task that runs every few minutes:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\path\to\repo\scripts\start_hermes_gateway_if_needed.ps1
```

From Git-Bash/MSYS, call registration/verification through `powershell.exe` or `schtasks.exe`; quote PowerShell commands carefully. If a `powershell -Command` contains `{ ... }`, `$variables`, or `Where-Object`, wrap the entire PowerShell command in single quotes or write a temporary `.ps1` file to avoid bash/MSYS mangling.

## Verification checklist

- Scheduled Task exists, is enabled/ready, and last result is `0`.
- Watchdog log shows either Gateway start or `OK gateway already running` on repeated ticks.
- `hermes cron status` reports that Gateway is running and cron jobs will fire automatically.
- Due Hermes cron jobs have `Last run: ... ok` and `Next run` advanced as expected.
- The project artifact expected from the job exists, if the user asked whether the job actually ran.
- Upload/publication jobs remain paused unless the user explicitly authorized publishing changes.
- `DEFAULT_PRIVACY` remains `private` for YouTube Agent unless explicitly changed.
- Run the project validation wrapper and confirm `.agent.lock` is clear before reporting completion.
- Record material scheduler changes and validation outcomes in repo handoff files such as `handoff/accepted_changes.md` and `handoff/codex_review.md`.

## Pitfalls

- Do not say Hermes cron is "scheduled" as proof it will run; verify Gateway is alive.
- Do not enable stale Windows tasks like broad `agent.py loop` jobs just because a run was missed; that duplicates scheduling and can bypass current gates.
- Do not enable upload-gate cron jobs while fixing production-loop reliability unless the user explicitly asked to enable upload/publication.
- A `deliver=origin` warning can affect notification delivery without meaning the cron job failed; verify `Last run` and project artifacts.
- Treat transient provider HTTP 500s as retryable job noise if the final cron result is `ok`; capture the retry pattern, not the one-off failure.
