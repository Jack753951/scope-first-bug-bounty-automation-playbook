> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Large phased implementation with Claude Code

Use this when the user wants Claude Code to carry more engineering work (for example to conserve Codex/OpenAI tokens) and the task is too large for one print-mode run.

## Pattern

1. Split the implementation into narrow phases with explicit deliverables and tests:
   - Phase A: schema/validation + focused tests.
   - Phase B: one fixture/generator + focused tests.
   - Phase C: renderer/scaffold + focused tests.
   - Phase D: gate/review + focused tests.
2. Write one `handoff/claude_code_task_phase_<x>.md` per phase. Include:
   - files to read first,
   - hard safety constraints,
   - exactly what to implement in this phase,
   - focused validation commands,
   - handoff update requirements.
3. Prefer direct print-mode invocation when project wrappers are too constrained:

```bash
'<user-home> \
  -p "$(cat handoff/claude_code_task_phase_a.md)" \
  --max-turns 25 \
  --allowedTools 'Read,Edit,Write,Bash,Grep,Glob' \
  --output-format text < /dev/null
```

Increase `--max-turns` by phase complexity, but keep phases small enough that reaching max turns is rare.

## After any max-turn exit

Do not rerun blindly. Inspect actual workspace state first:

```bash
git status --short
find handoff tests -iname '*expected-topic*' -maxdepth 3 2>/dev/null
python -m pytest <focused tests> -q
python -m py_compile <touched files>
```

If useful code exists, continue from it: add missing tests, fix focused failures, run verification, and record that Claude Code hit max turns separately from the final verified result.

## Handoff discipline

- Keep `handoff/claude_code_result.md` updated with wrapper failures, actual files changed, tests run, and remaining phases.
- Leave `handoff/codex_review.md` for the later focused Codex review pass.
- If conserving Codex quota, make Codex review only safety boundaries and surgical defects rather than reimplementing the rung.
