> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Stop Conditions

Hermes halts the affected loop and writes to operator inbox when any condition trips. Distinct from `SAFETY.md` § Hard stops (those gate ACTIONS); these gate Hermes' own behaviour.

## Categories

| Category | Trip | Action |
|---|---|---|
| **Drift** | Output file missing/stale > 2× cadence; same task fails 3× in a row; JSON Hermes wrote does not parse; unexpected file matching `INDEX.md` § Forbidden patterns appears | Halt offending loop |
| **Canon mutated externally** | `SAFETY.md` / `INDEX.md` / `.hermes.md` / `config/scope.txt` changed outside Hermes-orchestrated update | Reload, halt all loops, inbox |
| **Resource** | Token soft cap exceeded; disk < 5%; external API rate-limited > 6h | Halt write loops |
| **Safety** | Claude/Codex returns `Verdict: reject`; agent returns content violating `SAFETY.md`; scope check ambiguous; evidence redaction step fails | Halt task, inbox |
| **Behavioural runaway** | >20 files written in one iteration; daily call cap exceeded; same lane_state rewritten >5× in one day | Halt loop |

## Hard kill (halt ALL loops immediately)

- `SAFETY.md` missing/unreadable
- `INDEX.md` missing/unreadable
- `.hermes.md` missing
- Not a git repo / `.git` missing
- `config/scope.txt` empty AND any A2+ lane exists (deauthorization)
- Hermes running outside expected working directory

## Inbox report shape

```markdown
### Stop condition tripped — <category>

- Condition: <which>
- Affected loop / file: <path>
- Last known good: <timestamp>
- Action: halted <X>, continued <Y>
- Recommended operator action: <inspect | rerun | rollback | escalate>
```

Plus `hermes/state/hermes_log.jsonl` entry: `{"event":"stop_condition", ...}`.

Hermes does not auto-recover. Operator inspects, takes action, runs `bin/hermes` again.
