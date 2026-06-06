> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Video Project Codex Timeout / Partial Patch Recovery

Use this when a Codex CLI worker times out, emits a huge truncated diff, or exits before writing final handoff notes in a Shorts/video automation repo.

## Recovery checklist

1. Do not assume the timeout means no changes landed. Inspect the workspace state first.
2. Check for expected files from the task prompt, especially generated fixture modules, tests, and handoff reports.
3. If tests import a generated handoff module and it is missing, reconstruct or ask the worker output/diff for the intended module before rerunning the full worker.
4. Run validation from the project's intended Python environment, usually the repo venv on Windows:
   - `./.venv/Scripts/python.exe -m unittest ...` when pytest is unavailable in the venv.
   - `./.venv/Scripts/python.exe -m py_compile ...` for touched modules.
5. Regenerate upload-free fixtures directly with the project venv after repairing missing modules.
6. Run media QA with the tool's actual flags; for this repo `tools/oss_media_qa.py` uses `--out-dir`, not `--output-dir`.
7. Treat media-QA `REVISE` as a lane-specific finding, not a global failure, when the artifact is still internal/upload-free and the structural tests pass. Record the distinction clearly.
8. Update `handoff/codex_review.md` and `handoff/accepted_changes.md` with:
   - worker timeout/partial-patch status,
   - Hermes recovery actions,
   - authoritative local validation results,
   - artifact paths,
   - safety boundaries preserved.

## Safety reminders

For upload-free video/channel spikes, recovery validation must not run upload/create/publish commands, change scheduler state, touch OAuth/token/client-secret files, change privacy defaults, activate disabled channels, or delete runtime user data.
