> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Project Cleanup Migration Plan — 2026-05-27

Status: active migration plan
Source: Hermes directory/policy cleanup
Boundary: file organization / documentation only. No target-touching, scanner, exploit, VM, scope authorization, credential, token, cookie, OTP, phone, or report-submission action is authorized by this cleanup.

## Goal

Reduce `handoff/` from a catch-all history/policy/target/log store into a compact collaboration surface:

- keep current worker IPC, compact navigation, current lane queue/state pointers, and accepted-change log in `handoff/`;
- move binding/process policies to `docs/policy/`;
- move target-specific notes to `programs/<slug>/notes/`;
- move lab proof summaries/run-cards to `labs/proofs/`;
- move worker run receipts to `logs/runs/`;
- move old phase/review history to `handoff/archive/phase_history/`;
- move strategy/reference planning docs to `docs/strategy/`;
- keep sensitive/operator-owned files untouched (`config/scope.txt`, `loot/`, browser profiles, raw local screenshots, secrets).

## Keep in handoff root

- `accepted_changes.md`
- `active_strategy_queue.md`
- `current_navigation.md`
- `current_artifact_index.md`
- rolling worker files when present/non-empty: `cowork_task.md`, `cowork_result.md`, `cowork_proposal.md`, `claude_code_task.md`, `claude_code_result.md`, `codex_task.md`, `codex_review.md` (result files may be absent after archival or route-not-run; generic attestation review treats absent routes as SKIP)
- active machine-state files: `live_bounty_lane_queue.json`, `live_bounty_lane_runner_status.json`, `live_bounty_learning_seeds.jsonl`, `kali_vm_operations_state.json`
- `latest_check.md`, `hermes_workflow.md`, `INDEX.md`

## New destinations

| Destination | Meaning |
|---|---|
| `docs/policy/` | Binding or semi-binding process/policy/contract/routing docs. |
| `docs/strategy/` | Current or historical strategic planning/reference docs. |
| `programs/<program-redacted>/notes/` | <program-name> target/lane notes, review packets, prompts, passive maps. |
| `programs/<program-slug>/notes/` | <program-redacted> target/lane notes and learning seed. |
| `programs/<program-slug>/notes/` | <program-redacted> target/lane notes. |
| `labs/proofs/` | Local lab proof packets/run-cards/summaries. |
| `logs/runs/` | Claude/Codex/worker run JSON/TXT receipts. |
| `intelligence/` | CVE / KEV / vulnerability-intel reference notes. |
| `handoff/archive/phase_history/` | P0-P4/P2/P3/old worker review chains and superseded rolling named artifacts. |
| `handoff/archive/nav_snapshots/` | Full pre-cleanup copies of current navigation/index files. |

## Validation

After migration:

```bash
git status --short
python scripts/live-bounty-lane-status.py validate --state programs/<program-redacted>/lane_state.json --evidence handoff/live_bounty_evidence/<program-redacted>/owned_account_signup_profile_workspace_surface_map/evidence_surface_map_20260526.json --queue handoff/live_bounty_lane_queue.json
python scripts/live-bounty-lane-status.py queue --queue handoff/live_bounty_lane_queue.json
bash ./bin/hermes status
bash ./bin/hermes review
```

If `hermes review` fails only because historical artifacts moved, fix active path references or leave compatibility pointers; do not restore handoff sprawl.

## Rollback

Use git to inspect/restore moved paths:

```bash
git status --short
git diff --stat
# For a mistaken move before commit:
git restore --source=HEAD -- <path>
```

For untracked moved artifacts, use the generated manifest `handoff/project_cleanup_migration_manifest_20260527.json` to move them back.
