> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Autonomous Actions

What Hermes does alone. No operator approval, no Claude/Codex consult.

## Reads (any time)

Anywhere in repo per `INDEX.md` directory map. Public web: program policies, vendor docs, CVE/KEV/CT feeds, disclosed reports.

## Writes

| Path | Conditions |
|---|---|
| `programs/<slug>/lane_state.json` | Passive transitions only: status flip detect, deadline recompute, scope-diff note. **Not** decision changes (KILL, autonomy promotion). |
| `programs/<slug>/notes/<date>_*.md` | Recon notes, surface maps, CVE-match notes. |
| `handoff/live_bounty_lane_queue.json` | Register/deregister per operator decisions; never invent lanes. |
| `handoff/pending_intake.json` | Add/score/remove candidates. |
| `handoff/operator_inbox_<date>.md` | Daily regenerate. |
| `hermes/state/{hermes_state.json,hermes_log.jsonl,budget.json}` | Runtime state; log is append-only. |
| `hermes/digests/<date>.md` | Daily digest. |
| `hermes/calls/<ts>_*.md` | Pre + post call records. |
| `intelligence/{cve_briefs,program_briefs}/*` | Per-loop intake. |

## Tools

Filesystem, terminal, HTTP client, Playwright MCP, `claude` CLI, `codex` CLI. All within `SAFETY.md`.

## Decisions Hermes can make alone

- Recommend (write to inbox): lane KILL after deadline, candidate promotion, CVE-match flag, unsuspend detected.
- Execute: passive lane_state update, daily digest, intake score, log event.

## Decisions Hermes CANNOT make alone

See `SAFETY.md` § Hard stops. Includes: lane KILL execution, autonomy/capability promotion (A0→A2→A3), `config/scope.txt` change, scope.json broadening, report submit, modifying `SAFETY.md`/`INDEX.md`/`.hermes.md`, new top-level dir, deleting under `programs/`/`handoff/`/`intelligence/`/`archive/`/`logs/`/`loot/`. Former A4 actions are now controlled A3 capabilities, not a separate autonomy tier.

Default on uncertainty: STOP and write inbox.
