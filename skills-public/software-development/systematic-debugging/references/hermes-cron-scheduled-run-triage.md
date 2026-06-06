> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Hermes cron scheduled-run triage

Use this when a scheduled Hermes job appears incomplete, skipped, or did not deliver expected artifacts.

## Key lesson

Do not debug the job prompt, delegation path, or worker implementation before proving the scheduler actually fired. A folder containing partial artifacts can come from a smoke/packet-builder/manual check and is not proof that the owning cron run executed.

## Evidence to collect

1. Current local time and working directory.
2. `hermes cron status` and `hermes cron list`.
3. The cron job record in the active profile's `cron/jobs.json`:
   - `last_run_at`
   - `last_success_at` / `last_error_at` when present
   - `next_run_at`
   - schedule expression and grace behavior when visible
4. Gateway/scheduler logs from the active profile, especially around the scheduled time:
   - `logs/gateway.log`
   - `logs/agent.log`
5. Runtime supervision evidence, if the deployment has one:
   - Windows Scheduled Task state / last result for the Gateway watchdog
   - service/container health if running under a service manager
6. The expected output artifact set for the job, not just any folder contents.

## Interpretation pattern

- If `last_run_at` predates the expected scheduled time and `next_run_at` has advanced to a future run, inspect Gateway logs for a missed-run / fast-forward line.
- If Gateway was down during the schedule and restarted after the grace window, classify the incident as scheduler downtime/missed cron, not job logic failure.
- If Gateway was alive and the job fired, but only seed artifacts exist, then debug the cron prompt/delegation/artifact-writing path.
- If partial artifacts exist but role-separated outputs/synthesis are missing, compare against the job's declared completion contract before declaring success.

## Reporting format

Keep the final user-facing answer short and operational:

- Did it run? yes/no/uncertain
- Root cause classification
- Evidence bullets with timestamps
- Current readiness state
- Next verification point
- Path to any repo-local diagnostic note written

## Persistence pattern

For project-owned automation, write a concise repo-local diagnostic note in the handoff/checks area. Include evidence checked, findings, root cause, current risk, and recommended next action. Do not put run-specific timestamps, job IDs, or production state into global memory unless they are durable project signposts.
