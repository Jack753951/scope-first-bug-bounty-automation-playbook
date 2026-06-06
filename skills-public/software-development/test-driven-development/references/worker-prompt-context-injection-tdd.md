> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Worker Prompt Context Injection TDD

Use this when a repo wrapper launches delegated agents (Claude Code, Codex, Cowork, review workers) and must guarantee they receive compact long-term/current-stage context before the task body.

## Pattern

1. Add a focused RED regression test before changing the wrapper.
2. Use fake worker binaries placed earlier in `PATH` instead of invoking real LLM CLIs.
3. Have fake workers capture the exact prompt to a temp file and return a minimal successful result in the shape the wrapper expects.
4. Run each wrapper mode that builds prompts, for example strategy, implementation, and fallback review workers.
5. Assert prompt order and required content:
   - project context / `.hermes.md` prefix when present
   - required context-read block
   - task heading and task body
   - any safety footer for implementation workers
6. Assert the required context-read block names compact entrypoints, not a full vault dump.
7. Run focused test, syntax check the wrapper, then run the project review command if available.

## Example assertions

The captured prompt should include stable entrypoints such as:

```text
handoff/current_navigation.md
handoff/active_strategy_queue.md
notes/obsidian_projects/<Project>.md
handoff/accepted_changes.md
```

The wording should instruct workers to read those files when present and continue if a file is missing. It should also explicitly avoid dumping the whole Obsidian vault unless a task asks for it.

## Fake worker shape

For `claude -p <prompt>` wrappers:

```bash
#!/usr/bin/env bash
set -euo pipefail
prompt=""
json_out=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    -p) prompt="$2"; shift 2 ;;
    --output-format) json_out=true; shift 2 ;;
    *) shift ;;
  esac
done
printf '%s' "$prompt" > "$CAPTURE_PROMPT"
if $json_out; then
  printf '{"result":"fake","subtype":"success","terminal_reason":"done","session_id":"fake","num_turns":1,"total_cost_usd":0}\n'
else
  printf 'fake result\n'
fi
```

For stdin-based wrappers such as `codex exec ... -`, capture stdin and write the expected output file if the wrapper passes one.

## Pitfalls

- Do not test this by calling real LLM workers; that makes the regression slow, costly, and nondeterministic.
- Do not assert on the entire prompt byte-for-byte; assert on stable required sections and ordering.
- Keep context entrypoints compact. The goal is route/current-stage inheritance, not a full memory or Obsidian dump.
- If the wrapper has a dry-run mode that never builds the real prompt, test the normal execution path through fake binaries instead.
