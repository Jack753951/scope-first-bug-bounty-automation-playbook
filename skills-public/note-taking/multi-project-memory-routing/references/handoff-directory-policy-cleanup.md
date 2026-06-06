> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Handoff Directory / Policy Cleanup Pattern

Use when a project-local `handoff/` directory has become a catch-all for rolling IPC, navigation, policies, target notes, lab proof packets, worker receipts, and old phase history.

## Trigger

- `handoff/` has hundreds of root files or workers cannot tell which files are current.
- Navigation files have become long historical narratives instead of short route maps.
- Policy files are duplicated as dated variants rather than patched in place.
- Target/lab/run artifacts crowd the same root used for active worker IPC.

## Cleanup principle

`handoff/` should be current working memory, not the whole project database.

Keep in `handoff/`:

- compact current navigation / queue / artifact index;
- accepted-change log;
- rolling worker IPC files;
- current machine-state pointers and lane queues;
- a short `INDEX.md`;
- archive directories and migration manifests.

Move out of `handoff/`:

- policies/contracts -> `docs/policy/`;
- strategy/reference planning -> `docs/strategy/`;
- target-specific notes -> `programs/<slug>/notes/`;
- lab proof packets and run-cards -> `labs/proofs/`;
- worker run receipts / usage JSON -> `logs/runs/`;
- old phase/review chains -> `handoff/archive/phase_history/`;
- full pre-cleanup navigation snapshots -> `handoff/archive/nav_snapshots/`.

## Safe sequence

1. Inventory first: count root files, classify by role, and identify operator-owned or sensitive paths.
2. Write a migration plan and manifest path before moving files.
3. Archive full copies of long active navigation files before compacting them.
4. Move files by category; do not touch `config/scope.txt`, secrets, loot, raw browser profiles, cookies, OTPs, phone numbers, or private scope data.
5. Add or update indexes: `handoff/INDEX.md`, `docs/policy/README.md`, `docs/strategy/README.md`, and compact current navigation files.
6. Update active machine-readable pointers, especially `programs/<slug>/lane_state.json`, when artifact paths move.
7. Patch only active context/policy references; avoid rewriting every historical archived artifact just to update old path text.
8. Update wrappers if they write run receipts into the old root path, e.g. worker usage JSON should go to `logs/runs/`.
9. Run focused validation: shell syntax for wrappers, JSON validation for lane/queue/manifest files, lane-status helpers, and the project review command.
10. Report the move as filesystem/documentation cleanup only; explicitly state it does not authorize target-touching work.

## Policy hygiene rule

Do not create a new dated policy file for a correction to an existing policy topic. Patch the active policy file and rely on git/history/archive for previous versions. Dated files are appropriate for event records, checkpoints, evidence packets, and migration manifests, not for successive policy rewrites of the same rule.

## Verification examples

```bash
bash -n ./bin/hermes
python -m json.tool programs/<slug>/lane_state.json >/dev/null
python -m json.tool handoff/live_bounty_lane_queue.json >/dev/null
python -m json.tool handoff/project_cleanup_migration_manifest_<date>.json >/dev/null
python scripts/live-bounty-lane-status.py validate --state programs/<slug>/lane_state.json --queue handoff/live_bounty_lane_queue.json
bash ./bin/hermes review
```

## Pitfalls

- Do not mistake a large git status after moves for data loss; verify manifest and destinations.
- Do not put worker logs/receipts back into `handoff/` just because wrapper code used that path historically.
- Do not move operator-owned authorization files automatically.
- Do not let cleanup become another governance expansion; the goal is fewer active files and clearer current truth.
- Do not treat cleanup as approval to run scans, proofs, callbacks, API calls, or live target actions.
