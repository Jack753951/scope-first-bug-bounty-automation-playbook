> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase Boundary Routing Example

Use this reference when the user gives a project-specific sequencing rule such as "finish this phase before optimizing other areas".

## Pattern

A user may state a strong workflow preference that feels like a global instruction, but is actually scoped to the active project and current phase.

Example shape:

```text
Finish the script modularization closeout before moving to unrelated optimization.
```

## Routing

- Do not store the phase boundary as global Hermes memory unless the user explicitly says it should apply across projects.
- Do not add the phase state to this skill; skills should carry the routing rule, not the project status.
- Record the accepted sequencing decision in repo handoff files when it affects engineering workers.
- If the rationale is strategic or long-lived, summarize it in the project's Obsidian namespace and link back to repo truth.
- If the user preference generalizes into a reusable procedure, update this skill with the procedure only.

## Good handoff entry shape

```text
Current phase boundary: complete <phase name> closeout before starting <deferred work class>. Accepted by user on <date/session>. Applies to this project until changed.
```

## Bad persistent memory shape

```text
Always finish script modularization before optimizing anything else.
```

Why bad: it is project- and phase-specific, becomes stale, and may leak into unrelated projects.

## Verification

Before acting on a phase boundary:

1. Verify the current repo context/handoff still lists the boundary as active.
2. Avoid starting deferred work unless the user explicitly changes priority.
3. If implementing within the phase, keep changes narrow and record validation results in repo handoff.
