> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Inactive Project Global Memory Removal

Use this pattern when the user says a project is paused, inactive, not currently enabled, or asks to remove a project signpost from global Hermes memory.

## Rule

Treat this as a global-memory scope correction, not as deletion of the project itself and not as a request to modify the repo, Obsidian, scheduler, auth, or runtime state.

## Procedure

1. Identify the exact global-memory entry or compact signpost that names the inactive project.
2. Remove or compact only that global-memory entry.
3. Do not delete repo handoff files, Obsidian notes, local project directories, credentials, scheduled tasks, or runtime data unless the user explicitly asks for that specific destructive action.
4. In the reply, state plainly that the global memory signpost was removed and that this does not by itself change the project files or runtime state.
5. If the user asks later about the paused project, use session_search or project files only if they explicitly want to revisit it.

## Why

A paused project may still have useful local records, but keeping its route in always-injected global memory can distract future sessions and make the agent over-prioritize a project the user does not currently want active.

## Pitfalls

- Do not rehome every detail before removal unless the user wants preservation work. If the user merely wants the global signpost gone because the project is inactive, remove the global signpost and stop.
- Do not convert "暫時不啟用" into a permanent ban. It means the global memory should not foreground that project now; it does not mean the project can never be resumed.
- Do not treat memory removal as approval to edit schedulers, OAuth, channels, or repo configuration.
