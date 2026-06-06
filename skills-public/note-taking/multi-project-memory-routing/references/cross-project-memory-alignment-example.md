> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cross-Project Memory Alignment Example

This reference captures a reusable pattern from aligning two projects under one Hermes profile. It is an example of process, not a project database.

## Situation

One Hermes profile coordinates multiple projects with different risk profiles, for example:

- A media/content automation project with OAuth, generated media, scheduler, upload, and publication boundaries.
- A cybersecurity lab with authorization gates, scope files, scan artifacts, target details, payloads, and client-sensitive data.

The goal is to share a memory-routing process without leaking project state or sensitive operational details across projects.

## Pattern

1. Treat the more complete existing memory governance document as the baseline only if it is process-oriented.
2. Keep a shared authority order:
   - current explicit user instruction
   - live files/config/validation/current repo state
   - repo handoff engineering truth
   - active Obsidian project notes
   - Hermes durable memory
   - session_search as recall only
3. Put stricter project-specific overrides in each repo policy, not in global memory.
4. Use shared Obsidian notes only for cross-project governance and links to policy notes.
5. Keep project strategy, evidence, scan output, generated media state, OAuth/runtime state, and publication state in project-local locations only.
6. Before creating a new skill, search the skill library. If a class-level umbrella already exists, patch it instead of creating a duplicate.

## Good Skill Capture

A skill should capture:

- layer responsibilities
- decision tree for memory vs handoff vs Obsidian vs skill
- authority order
- periodic review checklist
- sensitive-project storage boundaries
- pitfall: do not turn skills into project logs

## Bad Skill Capture

Do not capture:

- today's completed tasks
- PR/issue/commit IDs
- exact scan outputs or target details
- OAuth/client secret/token paths or values
- generated video runtime state
- private bug bounty scope/rules
- one project's roadmap as if it applied globally

## Review Prompt Additions

For periodic reviews, ask:

- Is global Hermes memory still compact and cross-project-safe?
- Are repo handoff files still the engineering source of truth?
- Are Obsidian project indexes pointing to active policy/strategy notes?
- Did project-specific rules leak into unrelated projects through memory?
- Did we propose a new skill where an existing class-level umbrella should have been patched?
