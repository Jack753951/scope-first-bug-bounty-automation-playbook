> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Restart Checkpoint — Hermes Reopen 2026-05-21

Status: active checkpoint
Source: Hermes + operator correction
Date: 2026-05-21
Repo truth: `<user-home>`

## Current state

Phase 4B is active, but direction has been reset to script-first/context-driven bundles.

Accepted loop:

```text
preview + recon result
→ choose module bundle
→ if no usable module exists, return to script library
→ choose and execute situation-specific script combination
→ result + review
→ modularize useful script combinations
→ repeat
→ pentest report
```

## Important correction

The previous contract/profile/manifest-heavy structure is too heavy and limiting. It should not remain the main workflow.

New hierarchy:

- Script library = primary operational surface.
- Module bundles = reusable context-driven script combinations.
- Multi-agent collaboration = review/implementation support.
- Safety/scope = guardrails, not the center of the workflow.

## Next practical slice

Implement `lab_directory_listing_triage` by adding:

`<user-home>`

Purpose: verify/classify the `/ftp/` directory-listing candidate without bulk download or collecting secrets/loot.

## Resume pointers

Read:

- `handoff/restart_checkpoint_20260521_hermes_reopen.md`
- `handoff/active_strategy_queue.md`
- `handoff/phase4b_script_first_architecture_reset_20260521.md`
- `scripts/SCRIPT_INVENTORY.md`
- `modules/bundles/lab_directory_listing_triage.md`
