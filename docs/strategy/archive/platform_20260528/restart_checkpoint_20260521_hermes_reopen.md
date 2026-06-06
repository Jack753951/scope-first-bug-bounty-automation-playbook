> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Restart Checkpoint — Hermes Reopen

Status: active checkpoint before Hermes restart
Date: 2026-05-21
Source: Hermes + operator correction

## Current project direction

Phase 4B remains active, but the architecture direction has been reset.

Accepted direction: `SCRIPT_FIRST_CONTEXT_LOOP`

Correct workflow:

```text
preview + recon result
→ choose context-appropriate module bundle
→ if no usable module exists
→ return to script library
→ choose and execute a situation-specific script combination
→ result + review
→ modularize useful context-driven script combinations
→ return to preview + recon result
→ repeat
→ write pentest report
```

## What changed this session

The prior contract/profile/manifest-heavy architecture was judged too heavy and too limiting. It is no longer the main path.

New positioning:

- Script library is the primary operational surface.
- Module bundles are reusable context-driven script combinations.
- Multi-agent collaboration remains, but as review/implementation support, not the <program-name> gate.
- Safety/scope checks remain guardrails, not the center of the workflow.
- Heavy `modules/checks/**/module.json`, profiles, validators, importers, and readiness gates are retained as optional guardrail/support artifacts, not the primary user-facing workflow.

## Files created/updated for this reset

Primary repo handoff:

- `handoff/phase4b_script_first_architecture_reset_20260521.md`
- `scripts/SCRIPT_INVENTORY.md`
- `modules/bundles/README.md`
- `modules/bundles/lab_directory_listing_triage.md`
- `handoff/active_strategy_queue.md`
- `handoff/accepted_changes.md`

Obsidian:

- `Projects/Cybersec Lab/01_Methodology/Phase 4B Script-first Architecture Reset 2026-05-21.md`
- `Projects/Cybersec Lab/00_Index/Active Projects.md`

## Current next implementation target

Next slice should be practical and script-first:

`lab_directory_listing_triage` bundle

Implement the missing script:

`<private-workspace>/scripts/lab_modules/ftp_filename_content_class_verifier.py`

Purpose:

- Use current `/ftp/` directory-listing candidate from Juice Shop lab.
- List filenames from `/ftp/`.
- Classify extension/content-type/size.
- Avoid bulk download.
- Avoid collecting secrets/credentials/loot/PII.
- Produce result suitable for review/report input.

Do not start by adding more generic contract/profile/schema layers.

## Recent lab evidence

Most recent Wave2 benign-params run:

- Run id: `phase4b_wave2_benign_20260521T054852Z`
- Path: `<artifact-output-dir>/phase4b_wave2_benign_20260521T054852Z/`
- Result: no reflection candidate, no open redirect candidate.
- Health: `200 -> 200`, `requests_sent=5`.

Current strongest candidate remains:

- `/ftp/` directory listing metadata from prior GET-only/lab probe runs.

## Multi-agent collaboration status

Do not delete multi-agent roles. They remain useful:

- Hermes: coordinator, memory, scope guard, result synthesis.
- Cowork/Claude: strategy, report drafting, independent review, architecture guidance.
- Codex: surgical fixes, deterministic tests, validation, script safety.
- Claude Code Impl: larger offline/local implementation when needed, with usage JSON when invoked.

But they should support the script-first loop instead of replacing it with a heavy gate-first process.

## Hermes runtime caveat noticed before restart

Hermes may emit non-fatal Windows logging errors:

```text
PermissionError: [WinError 32] ... agent.log -> agent.log.1
```

Interpretation: Windows log rotation/file-lock issue when another Hermes process/thread/log viewer holds `<user-home>/AppData/Local/hermes/logs/agent.log`. Not a project failure unless the turn actually fails.

## Validation already run after reset

Command:

```bash
git diff --check && HACKLAB=<private-workspace> USER=Owner ./bin/hermes review
```

Result:

- `git diff --check`: OK except existing LF/CRLF warnings.
- `hermes review`: OK.
- Python compile: OK, 102 files.
- Shell scripts: `bash -n` OK.
- Lock: clear.
- Scope entries: 12.

## How to resume after restart

Read these first:

1. `handoff/restart_checkpoint_20260521_hermes_reopen.md`
2. `handoff/active_strategy_queue.md`
3. `handoff/phase4b_script_first_architecture_reset_20260521.md`
4. `scripts/SCRIPT_INVENTORY.md`
5. `modules/bundles/lab_directory_listing_triage.md`

Then continue with the script-first `/ftp/` bundle implementation, unless the operator gives a different instruction.
