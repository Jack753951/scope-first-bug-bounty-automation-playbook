> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Project profile isolation routing

Use when the user wants to isolate memory/context for large long-running projects with Hermes profiles.

## Core rule

Hermes profiles are the hard isolation boundary for profile-level durable memory, sessions, skills, plugins, cron jobs, and Gateway/runtime ownership. Repo handoff and Obsidian remain the project truth even after profile isolation.

Use a separate profile when a project is:

- long-running and context-heavy;
- sensitive or safety-boundary-heavy, such as cybersec/bug bounty/lab work;
- production-cadence-heavy, such as media automation with cron jobs;
- likely to pollute unrelated sessions with project-specific priorities.

Do not create a profile for every small repo or one-off task; profile sprawl increases management cost.

## Recommended staged migration

1. **Discover current owner first**
   - Run/read `hermes profile list` and identify which profile currently owns the Gateway and cron jobs.
   - If production cron/Gateway is already running in `default`, do not move it silently.

2. **Create project profiles without moving cron first**
   - Prefer names at the project-domain level, e.g. `youtube`, `cybersec`, `research`, not one-off issue names.
   - Clone config only when useful; avoid blindly cloning active cron jobs into the new profile.

3. **Use explicit profile launch for new sessions**
   - Start future project sessions with `hermes --profile <name>` from the project root.
   - Keep `default` as a general coordinator or existing scheduler owner until migration is planned.

4. **Migrate cron/Gateway only with an explicit checklist**
   - List source-profile cron jobs.
   - Recreate or update equivalent jobs in the target profile.
   - Verify target-profile Gateway/scheduler status.
   - Pause or remove duplicate source-profile production jobs.
   - Dry-run exact scripts where possible.
   - Verify the next scheduled run from repo-local evidence.
   - Record job ownership in repo handoff/Obsidian.

## User-facing recommendation pattern

When asked whether using `default` for an active large project is okay:

- Say short-term is okay if the current session/Gateway/cron already runs there.
- Recommend using a project profile for future sessions to avoid memory/context pollution.
- Do not interrupt a running workflow solely to switch profiles.
- Do not move production cron or Gateway during the same answer unless the user explicitly asks for migration.

## What goes where after profile isolation

- Profile memory: compact preferences and project-domain routing facts for that profile.
- Repo handoff: exact cron IDs, job status, validation, artifact paths, implementation decisions.
- Obsidian: long-term project strategy, rationale, research, and decision memory.
- Skills: reusable profile-isolation or scheduler-migration procedures only.

## Pitfalls

- Treating profile creation as cron migration. Creating a profile does not move existing cron jobs or Gateway ownership.
- Running two profiles' Gateways/cron jobs with duplicate production schedules.
- Moving a production cadence without first pausing the old owner.
- Saving project history into global memory just because a new profile exists.
- Setting a sticky default profile too early; explicit `--profile <name>` is safer during transition.
