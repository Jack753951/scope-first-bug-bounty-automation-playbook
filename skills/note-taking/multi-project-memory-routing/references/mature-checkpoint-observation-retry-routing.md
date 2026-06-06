> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Mature Checkpoint Observation Retry Routing

Use this pattern when a project phase is blocked on a time-gated, read-only checkpoint such as a scheduled publication/canary observation.

## Pattern

1. If the checkpoint is not mature, do not infer performance or start a new lane. Perform only read-only readiness work and, if useful, schedule/launch a narrow one-shot watcher that waits until the mature time.
2. The watcher must be explicitly scoped to read-only checks and named handoff output files. It should not run generation, render, upload, publish, privacy changes, scheduler edits, OAuth setup, channel config changes, DB writes, or data deletion.
3. If the first observation artifact reports an anomaly, classify the source before treating it as a project gate failure:
   - local helper/script bug,
   - import/path/cwd issue,
   - credential/token refresh behavior,
   - actual API/channel/privacy/status inconsistency.
4. When the anomaly is a local helper bug, patch the reusable helper and rerun the same read-only observation once. Mark the first artifact as superseded/import-path anomaly rather than deleting it.
5. If a read-only API helper refreshes an existing token file while performing a normal authenticated read, record that caveat precisely: no auth flow started and no secrets printed, but the token file may have been refreshed. Do not claim “no OAuth/token touch” if the helper output indicates a token save.
6. Put the corrected observation in a new named repo-local handoff artifact and prepend a short accepted-change entry that:
   - points to the corrected artifact,
   - explains what superseded the first anomaly artifact,
   - records the observed status fields,
   - repeats the blocked actions.
7. Update the active strategy queue from “waiting for checkpoint” to “checkpoint observed,” but do not convert low/zero/early engagement into a creative or launch decision unless the project’s explicit gate says so.

## Why

Time-gated observations often combine live API calls, local helper scripts, and scheduled platform state transitions. A local script failure should not be promoted into global memory or project strategy. The reusable lesson is to preserve auditability, retry only after fixing the local cause, and keep activation gates unchanged.
