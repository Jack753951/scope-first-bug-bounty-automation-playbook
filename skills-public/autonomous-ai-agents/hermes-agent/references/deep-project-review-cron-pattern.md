> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Deep project-review cron pattern

Use this when a Hermes cron job is responsible for recurring third-party or project-health review of an automation/code/content project.

## Durable lesson

A recurring review job should not be only a narrow content or bug check. The cron prompt should define the review as a system-health review and explicitly require the reviewer to inspect:

- workflow drift: whether the agent/worker/reviewer split still improves delivery or has become fragmented busywork.
- memory and handoff durability: whether decisions, validation results, blockers, and review conclusions are written to durable files rather than living only in chat.
- goal drift: whether current work still advances the original project objective, or whether side quests are consuming effort.
- project-structure drift: whether modules, configs, channels, tests, generated artifacts, and handoff docs are becoming clearer or more tangled.
- constructive recommendations: what to continue, pause, consolidate, stop, and do next.

## Prompt shape

For each scheduled review job, make the prompt self-contained. Include:

1. Target repo/workdir and expected output path, usually `handoff/periodic_reviews/YYYY-MM-DD/`.
2. Role split: e.g. Codex/GPT for engineering risk, Claude/Cowork for strategy/creative/process review, Hermes for synthesis/gating. If the job title or purpose says `third-party review`, `deep system review`, or otherwise implies multi-party review, the prompt must require a real `delegate_task` call with separate reviewer tasks and the cron job must enable the `delegation` toolset; single-answer role-play is not sufficient.
3. Required sections such as Executive Verdict, Workflow/Memory Review, Goal-Drift Review, Project Structure Review, Safety Review, Immediate Actions, Defer/Avoid, and Decision for Next Phase.
4. Explicit read-only/offline boundaries for automation projects: no publish/upload/deploy, no generation runs unless requested, no OAuth/token/client-secret changes, no default privacy or scheduler mutations, and no runtime-data deletion.
5. Validation expectations: inspect generated prompt packets, compile/check scripts that build packets, and run whitespace/diff checks when files are edited.

## Handoff context to include when safe

A useful packet usually includes not just recent diffs but the governance files future reviewers need to judge drift:

- multi-agent collaboration policy
- accepted changes / decision log
- active proposal/review inboxes
- blocked follow-ups
- canary or candidate lists
- open-source/recon logs when relevant
- channel or project configuration summaries with secrets excluded

## Pitfall

Do not let a recurring review decay into a checklist that only asks "is the latest artifact good?" The value of the schedule is catching slow systemic drift before it becomes expensive: handoff rot, unclear ownership, duplicated modules, unsafe automation creep, and work that no longer serves the original goal.
