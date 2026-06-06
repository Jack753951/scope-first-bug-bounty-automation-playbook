> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Workflow / Process Change Governance Routing

Use this pattern when the user corrects how a project should be operated, reviewed, routed between agents, or remembered across future sessions.

## Trigger

- The user says a workflow/process change should be remembered, adopted, or applied going forward.
- The change affects future Hermes / Claude Code / Codex behavior for a project.
- The change is not merely a one-off run artifact or today's task progress.

## Routing

1. Classify the correction before saving anything.
2. If it is a reusable cross-project routing rule, update this skill or another class-level skill.
3. If it is a stable user-wide preference, save only a compact declarative Hermes memory signpost.
4. If it governs one project's future operations, write it to that project's repo governance/handoff file.
5. If it changes long-term project reasoning, decision rationale, or future review behavior, also write it into the project's Obsidian namespace with metadata:

```markdown
Status: active | superseded | rejected | experiment | reference
Source: User | Hermes | Claude | Codex | Mixed
Date: YYYY-MM-DD
Repo truth: path/to/handoff-or-code-file, if applicable
```

## Verification

- Read back or otherwise verify both repo-local and Obsidian project notes after editing.
- Report the storage layers separately so the user can see the routing decision.
- Do not run unrelated implementation tests merely to record a governance/process note.

## Pitfall

Do not treat a workflow/process correction as chat-only memory. If future agents or reviewers need it, durable project-local governance must be updated. Do not over-promote exact project facts into global Hermes memory; keep global memory as a compact pointer.