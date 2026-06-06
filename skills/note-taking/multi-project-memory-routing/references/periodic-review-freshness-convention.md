> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Periodic Review Freshness Convention

Use this reference when a project has deep-review packets, periodic-review summaries, or multi-agent handoff bundles that may become stale while work continues.

## Problem

Deep review packets are often useful but frozen. If later handoff files, accepted-change logs, or live code change, a future agent may accidentally treat the old packet as current authority and reopen closed work or miss newer constraints.

## Required freshness header

Every periodic/deep review packet should include a compact freshness block near the top:

```markdown
Freshness:
- Packet frozen: YYYY-MM-DD HH:MM TZ, or YYYY-MM-DD if exact time is unavailable.
- Latest handoff inspected: path/to/file.md, dated YYYY-MM-DD.
- Latest accepted-change log inspected: path/to/file.md, dated YYYY-MM-DD.
- Post-packet changes included: yes/no/partial, with one sentence explaining scope.
- Authority if conflict: current explicit user instruction > live project files/validation > active strategy queue / accepted_changes > this frozen packet > session recall.
```

## Review workflow

1. Treat the packet as a snapshot, not a living source of truth.
2. Before using it for action, inspect the project-local active queue, accepted-change log, and relevant live files.
3. If the packet and active handoff disagree, update the handoff or note the packet as stale rather than following it silently.
4. When closing a phase, append a short note to the accepted-change or active-queue file so later workers know whether the packet has been superseded.
5. Do not promote dated packet conclusions into global Hermes memory unless they are stable cross-project preferences or routing rules.

## Example application

For a media automation project with channels, canary candidates, and review packets:

- The packet may discuss a candidate hierarchy or visual QA findings.
- The active strategy queue and accepted changes decide whether that lane is still open.
- If a lane has been closed as strategy/docs-only, future workers should not generate new variants just because an old packet suggested more exploration.
- If new production-learning evidence exists after the packet date, include it as post-packet context or freeze a new packet.

## Common pitfalls

- Calling a review packet "latest" without a frozen date.
- Letting packet recommendations override a newer active strategy queue.
- Re-running old exploratory work after a lane was explicitly closed.
- Copying dated project facts into global memory instead of leaving them in repo handoff or Obsidian.
