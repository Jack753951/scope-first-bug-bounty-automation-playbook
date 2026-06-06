> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Checkpoint-Waiting Readiness Snapshot Pattern

Use this when a project is between already-scheduled checkpoints and the user says to continue, proceed, or asks for the next phase, but the next meaningful observation window is not mature yet.

## Trigger

- The repo has explicit future observation/checkpoint times.
- The current time is before those checkpoints.
- Advancing early would risk generation, upload, publication, scheduler/OAuth/privacy changes, or strategy overreaction from immature data.
- The user still expects active project work, not a passive “wait”.

## Pattern

1. Load the project-local authority files first: active queue, accepted changes, gate/readout template, or equivalent.
2. Check current time with a live tool; never infer it mentally.
3. Run only read-only/project-safe prechecks such as validation, gate status, status, and scheduler/cron inspection if allowed by the project rules.
4. If checkpoints are not mature, write a named repo-local readiness snapshot instead of forcing a premature action.
5. If a compact routing index / active queue is stale relative to accepted changes or a fresh gate packet, add a short current-status overlay near the top instead of rewriting broad historical sections. The overlay should name the latest authoritative artifact, exact checkpoint time, decision label, and blocked actions.
6. Update the active queue with a short pointer to the snapshot and exact future checkpoints.
7. Prepend/append a compact accepted-changes entry that records the decision, validations, and safety boundary.
8. If scheduler/cron inspection shows stale-looking or past-due jobs but scheduler changes are gated, record the observation in the snapshot and do not pause/remove/update jobs without explicit user approval.
9. Do not store the phase state in global Hermes memory; it is project-local and likely short-lived.

## Snapshot contents

A good readiness snapshot includes:

- Status line: read-only / no generation / no upload / no publication / no scheduler change.
- Why it exists.
- Current phase label from the repo authority file.
- Current local time and checkpoint maturity table.
- Validation/gate/status summaries.
- Relevant cron/scheduler entries without changing them; if entries look past-due/stale, label them as observations only unless the user explicitly authorized scheduler housekeeping.
- Decision, e.g. `WAIT_FOR_MATURE_CHECKPOINTS`.
- Safety boundary listing actions not performed.
- Next safe action with exact times and target templates.

## Routing rule

- Repo handoff: the snapshot, active queue update, and accepted-changes entry.
- Skill: this reusable procedure only.
- Global memory: at most a compact cross-project signpost if the user explicitly wants this pattern reused broadly.

## Pitfall

Do not treat “continue” as permission to start a new generation/upload/scheduling lane when the next accepted phase is an observation checkpoint that has not matured. Active work can be a readiness snapshot and queue alignment, as long as it is useful and verified.
