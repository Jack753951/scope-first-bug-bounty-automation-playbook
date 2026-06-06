> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Automation Goal Status-Correction Routing

Use this pattern when the user corrects a project status/goal summary because it underplays automation, productionization, launch, or another durable goal dimension.

## Trigger

Examples:

- "長期目標是不是缺少了有關自動化的要素"
- "You forgot that the goal is automation, not just review/docs."
- "This is supposed to become a callable platform, not only a checklist."

## Procedure

1. Treat the correction as both a status-answer fix and a project-memory routing event.
2. Verify the project-local authority layers before writing anything:
   - active strategy queue / roadmap handoff;
   - accepted changes or named decision artifacts;
   - Obsidian active project index or methodology note if that project uses Obsidian.
3. Update project-local navigation so future status answers include the corrected durable goal dimension.
   - For cybersec-style projects, phrase automation as policy-gated / scope-gated / review-gated if activation is sensitive.
   - Avoid turning the correction into broad runtime approval.
   - Prefer updating the compact active strategy / roadmap layer and any active Obsidian project index or status-answer preference note, not only a one-off chat answer.
4. Record the navigation correction in the project's accepted-change or decision log when that project uses one.
   - Treat accepted-change logs and shared handoff Markdown as append/prepend-only collaboration surfaces.
   - Re-read the relevant beginning/end anchor before patching and make the smallest possible insertion so the update does not accidentally duplicate or rewrite large historical blocks.
5. If the correction changes a reusable status-answer pattern, patch the relevant class-level skill/reference rather than creating a project-specific skill.
6. Keep sensitive operational details out of global memory. If the user asks whether compaction lost them, point to repo/Obsidian authority files and verify they exist when tools are allowed.

## Output wording pattern

```text
你說得對：我前一版少寫了 <goal dimension>。
我已把 project-local navigation 修正成：<updated one-line goal>。
這不是 activation approval；下一步仍是 <safe gated slice>。
```

## Cybersec example

For a cybersec lab, the corrected long-term goal should preserve automation explicitly while keeping gates closed:

```text
建立可安全轉向授權 bug bounty 的模組化、自動化測試、證據、review、報告 pipeline。
```

Then distinguish:

- allowed now: offline catalog / alias / script-classification planning;
- later with approval: controlled local-lab execution;
- still blocked: real targets, scanner broad runs, exploit chains, callbacks/OAST, brute force, credential/loot workflows, report submission, and automatic confirmed-finding promotion.

## Pitfalls

1. Do not answer only in chat and leave the active project index stale.
2. Do not save the full project state in Hermes global memory.
3. Do not treat "automation is the long-term goal" as approval to run automation now.
4. Do not collapse engineering details into global memory after compaction; preserve pointers and project-local authority instead.
