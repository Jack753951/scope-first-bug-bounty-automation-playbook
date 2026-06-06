> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

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

## Recommended staged migration

1. **Discover current owner first**
   - Run/read `hermes profile list` and identify which profile currently owns the Gateway and cron jobs.
   - If production cron/Gateway is already running in `default`, do not move it silently.
   - Check built-in memory layout before migration: default memory lives under the default Hermes home `memories/`, while named profiles use `profiles/<name>/memories/MEMORY.md` and `USER.md`.

2. **Create project profiles without moving cron first**
   - Prefer names at the project-domain level, e.g. `youtube`, `cybersec`, `research`, not one-off issue names.
   - Use `hermes profile create <name> --clone` when the project should inherit config, `.env`, `SOUL.md`, and skills from the active/default profile.
   - Avoid `--clone-all` during first-stage isolation unless the user explicitly wants all state copied; it risks carrying sessions/runtime state the migration is trying to separate.
   - After creation, verify that new profile Gateway is stopped and the new profile cron list is empty before claiming cron/Gateway stayed in the source profile.

3. **Do first-pass profile-local memory hygiene immediately**
   - Rewrite or patch each new profile's built-in `MEMORY.md` and `USER.md` to keep only that profile's project-domain preferences, routing pointers, safety gates, and stable workflow conventions.
   - Compact the source/default profile memory into cross-project preferences and namespace pointers, not project-specific workflow detail.
   - Rehome still-useful project details into the destination profile memory and project repo/Obsidian before removing them from default/global memory.
   - When modifying another profile's `memories/` files via file tools, treat it as cross-profile state and require explicit user direction; use the tool's cross-profile override only after that direction.

4. **Use explicit profile launch for new sessions**
   - Start future project sessions with `hermes --profile <name>` from the project root, or with the generated profile alias if one was created.
   - Keep `default` as a general coordinator or existing scheduler owner until migration is planned.
   - Do not set a sticky default profile during the transition unless the user specifically chooses that operating mode.

5. **Record the boundary in every affected project**
   - Update the active repo's current navigation / active strategy queue / accepted-change log with the profile name, profile path, launch command, and the fact that cron/Gateway migration is pending.
   - If the migration also creates a profile for another large project, write the same compact profile-boundary note into that project's handoff, not only the current repo.
   - Add an Obsidian/project-note entry when profile isolation changes future reasoning, memory routing, or worker expectations.

6. **Migrate cron/Gateway only with an explicit checklist**
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

- Profile memory: compact preferences, project-domain routing facts, stable workflow conventions, and safety/activation boundaries for that profile.
- Source/default memory: cross-project preferences and short namespace pointers only.
- Repo handoff: exact cron IDs, job status, validation, artifact paths, implementation decisions, and profile-boundary checkpoints.
- Obsidian: long-term project strategy, rationale, research, and decision memory, including why profile isolation changes future reasoning.
- Skills: reusable profile-isolation or scheduler-migration procedures only.

## Verification checklist after first-stage isolation

- [ ] `hermes profile list` shows the new profiles and only the intended source profile has a running Gateway.
- [ ] `hermes --profile <name> cron list` is empty for newly created profiles unless the user explicitly migrated jobs.
- [ ] New profile `MEMORY.md` / `USER.md` are project-scoped and do not contain unrelated large-project details.
- [ ] Source/default memory has been compacted into cross-project preferences and namespace pointers.
- [ ] Affected repo handoff/active queue records the profile name, profile path, launch command, and cron/Gateway migration status.
- [ ] Any second project that received a profile also has its own repo-local boundary note.
- [ ] Validation appropriate to the repos was run, e.g. `git diff --check` and the repo's local review command.

## Pitfalls

- Treating profile creation as cron migration. Creating a profile does not move existing cron jobs or Gateway ownership.
- Running two profiles' Gateways/cron jobs with duplicate production schedules.
- Moving a production cadence without first pausing the old owner.
- Saving project history into global memory just because a new profile exists.
- Setting a sticky default profile too early; explicit `--profile <name>` is safer during transition.
