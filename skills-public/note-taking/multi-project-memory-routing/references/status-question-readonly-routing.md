> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Status Question Read-Only Routing

Use this pattern when the user asks questions like:

- "目前的長期目標是甚麼還有現在在甚麼階段?"
- "What are we trying to achieve?"
- "Where are we in the plan?"
- "What is the current phase / next gate?"

## Rule

Treat these as read-only orientation requests by default, not as permission to advance the project.

## Procedure

1. Inspect the project-local authority layers first:
   - `.hermes.md` / project context
   - active strategy queue
   - accepted changes / handoff files
   - relevant Obsidian project index if the repo policy points there
   - session_search only as recall, then verify against files
2. Summarize:
   - long-term goal, including any durable goal dimensions the project has explicitly established (for example automation, productionization, launch, research, or safety governance);
   - current phase
   - last completed gate
   - current blockers or safety gates
   - safest next queued action, clearly labeled as not yet executed
3. For automation/scheduler status, do not treat a scheduler `last_run_at` timestamp as success by itself. Read-only status checks should cross-check:
   - scheduler/cron enabled state, `last_status`, `next_run_at`, and delivery errors;
   - gateway/runner health when relevant;
   - local side-effect evidence expected from a successful run, such as DB rows, generated artifacts, handoff readouts, or logs;
   - whether the reported error is only delivery/reporting failure or an actual execution/content-output failure.
   If the evidence is mixed, state the uncertainty explicitly (for example: scheduler fired but production output is not verified) instead of declaring the loop healthy.
4. If the user corrects the summary because a durable goal dimension was omitted, treat that as a project-local navigation update opportunity: verify the authority layers, update the repo/Obsidian active-status surfaces when appropriate, and preserve activation gates. See `automation-goal-status-correction-routing.md`.
4. Treat context-compaction summaries, existing todo state, or earlier queued work as background only. If the latest live user message is an orientation/status question, answer that question read-only; do not resume a prior "continue/proceed" task just because it appears in compacted context or the todo list.
5. Do not run generation, upload, scheduling, publication, implementation, worker pipelines, handoff edits, Obsidian writes, or task-list mutation unless the user explicitly asks to proceed.
6. If a previous task list exists, leave it alone unless the current user asks to manage tasks. A status/orientation reply should not mark stale todos complete or create new execution-state noise.
7. If the project has activation-sensitive steps, restate the gate in the answer.
8. Keep dated run artifacts, commit IDs, and one-off validation snapshots in repo handoff, not global memory or this skill.

## Output shape

Prefer a compact answer in the user's language:

```text
長期目標：...
目前階段：...
已完成：...
現在卡關 / gate：...
下一個安全步驟：...（尚未執行）
```

## Pitfalls

1. Do not interpret an orientation question as "continue". Advancing the repo can hide the answer the user actually wanted and may cross safety or activation boundaries without explicit approval.

2. Do not let a context-compaction handoff or stale todo list change the active request. The current live user message controls: if it asks "what is the goal/phase/status?", give the status answer first and label any next action as proposed/not executed.

3. Do not emit tool-progress artifacts in a status answer unless they are necessary to retrieve current truth. In particular, avoid `todo` updates for read-only orientation questions; they make it look like the agent advanced work when the user only asked for orientation.
