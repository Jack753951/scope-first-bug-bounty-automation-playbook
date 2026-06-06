# 03 — Memory and Handoff Governance

Status: public methodology

## Layer responsibilities

```text
Global agent memory = compact signposts and durable preferences.
Project handoff = active engineering truth and validation status.
External notes/vault = long-term strategy, rationale, methodology, decisions.
Skills/playbooks = reusable procedures, not project databases.
Session search = recall leads that must be verified against files.
```

## What belongs where

| Information type | Destination |
| --- | --- |
| Stable user/team preference | Global memory, compact and declarative |
| Current lane state | Project handoff / machine-readable JSON |
| Validation output | Project handoff or artifact folder |
| Strategy and rationale | External project notes/vault |
| Reusable workflow | Skill/playbook |
| Secrets, raw target details, cookies, tokens, loot | Nowhere public; keep out of broad memory |

## Authority order

1. Current explicit operator instruction.
2. Live repository state and validation output.
3. Safety contract and scope files.
4. Project handoff/current navigation.
5. External project notes for strategy/rationale.
6. Global memory as compact pointers only.
7. Past sessions as recall, not truth.

## Public-export principle

Do not publish raw handoff, program state, scope, screenshots, scan output, local
VM names, host-only IPs, credential filenames, or dated operational logs. Publish
only hand-cleaned methodology that remains useful when all private nouns are
removed.
