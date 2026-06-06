> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent scheduler sync gate pattern

Use when the YouTube automation repo's handoff state says the project is in observation/gated-learning mode but local Windows Task Scheduler or Hermes cron jobs may still reflect an older production-loop phase.

## Durable lesson

Do not assume scheduler state matches repo handoff. Inspect both:

- Windows Task Scheduler tasks such as `youtube_agent_daily_loop` and `enable_psychology_channel`.
- Hermes cron jobs for read-only canary checks, daily reports, and deep reviews.
- `.agent.lock` and the process id inside it.
- `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`, and `handoff/codex_review.md`.

If a Windows task still runs `agent.py loop --channel ...`, treat it as production automation because `loop` performs fetch + learn + remake + create. If the active queue says generic create/remake/loop is not authorized, disable that task rather than letting old automation continue.

## Safe sequence

1. Read the active queue and latest accepted changes first.
2. Inspect Windows Task Scheduler from bash by invoking PowerShell with single-quoted commands or a temporary `.ps1` script to avoid MSYS `$_.TaskName` path rewriting.
3. If the user explicitly asked to synchronize scheduling, stop and disable stale project tasks that contradict the current gate.
4. Preserve read-only Hermes cron jobs for observation/reporting when they match the queue.
5. If stopping a task leaves `.agent.lock`, verify the PID no longer exists before deleting the lock.
6. Run read-only validation/status commands after sync:
   - `powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate`
   - `powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' gate-status`
7. Record the scheduler sync in `handoff/accepted_changes.md`, `handoff/codex_review.md`, and the active queue/current routing note.

## Pitfalls

- `register_scheduler.ps1` may create a broad daily loop that no longer fits the current gate. Do not re-run it just because a scheduler task exists.
- `Get-ScheduledTask | Where-Object { $_.TaskName ... }` can be mangled by Git-Bash/MSYS if quoted poorly. Prefer single quotes around the PowerShell command or write a small temporary `.ps1` file.
- Disabling old production-loop scheduling is not the same as creating a new video schedule. It is a safety synchronization action, but still requires the user's explicit scheduler-sync request.
- Do not delete `.agent.lock` until the recorded PID is confirmed dead.
- Update cron prompts to say read-only/report-only when the phase is observation; otherwise future scheduled agents may inherit stale production language.
