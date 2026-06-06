> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Paused Upload Gate vs Learning Loop Routing

Use this pattern when a user corrects an agent for interpreting a paused upload/scheduled-publication gate as a pause of the entire learning or automation lane.

## Trigger

Examples:

- User says a channel/project should keep collecting data while a new lane is developed.
- User corrects wording like "X should wait" because only the upload/scheduled gate was meant to wait.
- A handoff says a lane is paused, but the surrounding strategy says local-only drafts, read-only observation, or analytics learning should continue.

## Core distinction

Separate these concerns before answering or editing project records:

1. Learning/data loop
   - local-only drafts;
   - local QA / render QA;
   - read-only analytics/canary observation;
   - compact learning logs;
   - batch review after enough artifacts.

2. Activation/upload gate
   - upload/private canary/scheduled upload/publication;
   - OAuth/token/client-secret/destination/channel config;
   - DEFAULT_PRIVACY;
   - OS/Windows Task Scheduler or production cron changes;
   - broad unattended production loops.

A pause of (2) does not automatically pause (1). A desire to continue (1) does not automatically approve (2).

## Procedure

1. Verify authority layers before changing anything:
   - active strategy queue or routing index;
   - accepted changes / decision log;
   - scheduler/cron status if tools are allowed;
   - Obsidian project strategy note if the project uses one.
2. Correct the project-local wording narrowly:
   - name the exact gate that is paused;
   - name the learning activities that remain allowed or desired;
   - preserve the explicit-approval requirement for activation/upload/scheduler/OAuth/privacy changes.
3. If answering "what next?", propose a low-risk loop first:
   - local-only draft or data collection;
   - lightweight QA;
   - Claude/visionreview or batch review when available;
   - compact report to repo-local learning/readout folder;
   - no upload/schedule/publication unless separately approved for an exact artifact.
4. If scheduler state matters, inspect it instead of assuming the old local loop is active.
   - It is common for upload gates to be paused correctly while the intended local-only learning job is absent, disabled, expired, or stale.
   - Report this as an operational gap, not as a change in strategy.
5. Store the correction in repo handoff/active queue and, when strategic, project Obsidian. Keep global memory to a compact signpost only if cross-session routing needs it.

## Output wording pattern

```text
你說得對：這不是整個 <lane> 暫停，而是 <upload/scheduled gate> 暫停。
正確下一步是恢復/確認 local-only learning loop：本地 draft/data -> QA -> visionreview/批次 review -> compact learning log。
這仍然不是 upload、schedule、OAuth、channel config、DEFAULT_PRIVACY 或 broad production loop 的批准。
```

## Pitfalls

1. Do not use vague wording like "the channel is paused" when only upload/scheduled canaries are paused.
2. Do not restart an old broad loop just because the user wants learning to continue; design/restore the narrow local-only loop that matches current gates.
3. Do not treat Storytime/new-lane development, refactoring, or asset intake as replacing the already-approved learning/data cadence unless the user explicitly says so.
4. Do not treat a safe local-only loop as evidence that an exact artifact is upload-ready; promotion still needs the project’s upload/canary gate.
5. Do not save video IDs, cron IDs, artifact paths, or dated run state in this skill; those belong in repo handoff.