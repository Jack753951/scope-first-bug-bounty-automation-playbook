> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Single Scheduler Production Ownership Routing

Use this pattern when a project has more than one possible automation owner for the same production action, such as Windows Task Scheduler, Hermes cron, app-internal loops, upload gates, or platform scheduled-publication jobs.

## Trigger

- The user changes which scheduler should own a live or production-affecting loop.
- A loop can be run by both OS scheduling and Hermes cron.
- Separate upload/publication gates could duplicate the same daily production cadence.
- The user asks for status/phase and scheduler state materially affects the answer.

## Procedure

1. Treat scheduler ownership as production-affecting state, not just housekeeping.
2. Verify the current owners before changing or summarizing:
   - OS scheduler/task state if relevant.
   - Hermes cron jobs and pause/resume state.
   - App-internal loop command/channel/scope.
   - Any separate upload/publication gate jobs.
3. Make exactly one owner authoritative for the cadence unless the user explicitly approves multiple lanes.
4. Disable or pause duplicate owners rather than leaving parallel paths active.
5. Preserve hard activation gates: do not infer approval to publish broadly, change OAuth, alter destinations, change default privacy, delete runtime data, or add more schedules.
6. Record the new ownership in repo-local handoff/active queue with:
   - scheduler type and job/task name;
   - enabled/paused/disabled state;
   - command/channel/scope;
   - duplicate gates intentionally paused/disabled;
   - recommended next observation or readout.
7. Keep exact job IDs, timestamps, and command details repo-local. Global memory should contain at most a compact signpost that the project uses repo handoff for scheduler/process truth.

## Reporting

When reporting back, state:

- The single active production owner.
- Which duplicate jobs/tasks were disabled or paused.
- What remains read-only/learning versus upload/publication activation.
- Where the repo-local record was updated.

## Pitfall

Do not say “the loop is paused” merely because an upload gate is paused. Distinguish local generation/learning loops, upload gates, scheduled-publication gates, and analytics/readout jobs. A paused upload gate can coexist with an active local production/learning loop if that is the intended single owner.
