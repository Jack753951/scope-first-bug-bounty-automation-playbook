> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 1 Program Scope System

## Completed design stages

- P1-1: schema/docs/examples
- P1-2: offline validator
- P1-3: offline policy decision helper
- P1-3.1: decision contract hardening
- P1-4: runtime integration design accepted for implementation

## P1-4 implementation sequence

### Task A

- `--program`
- `--policy-mode`
- `--allow-cidr`
- CLI validation
- slug/path restriction
- no-`--program` zero side-effect regression tests

### Task B

- `scripts/program_policy_boundary.py`
- jq-free boundary wrapper
- timeout handling
- schema contract validation
- atomic artifact write
- shell-readable status

### Task C

- per-stage recon integration
- fresh decision per stage/target
- no cached allow decision
