> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec workspace: Claude Code implementation routing

Session learning: a routing policy that merely says "prefer Claude Code" is not enough. If the project wrapper still routes implementation to Codex by default, the user will not see Claude Code usage consumed and will reasonably doubt that coding is being delegated.

Reusable pattern for Hermes-style cybersecurity repos:

1. Keep Hermes as coordinator, safety gate, and verifier.
2. Add an explicit implementation worker command, e.g. `hermes claude-impl`, separate from strategy/review `hermes cowork`.
3. Default implementation-heavy offline/local coding to Claude Code MAX/OAuth, not Codex, while keeping Codex as surgical fallback.
4. Make the route auditable by writing both:
   - a human summary, e.g. `handoff/claude_code_result.md`
   - raw Claude Code JSON, e.g. `handoff/claude_code_impl_run_<timestamp>.json`, including `session_id`, `num_turns`, `total_cost_usd`, `usage`, `modelUsage`, `terminal_reason`, and `subtype`.
5. Ensure `hermes pipeline` default chain visibly uses the Claude Code implementation worker, e.g. `cowork -> review -> claude-impl -> review`.
6. Provide an explicit fallback knob, e.g. `HERMES_IMPL_WORKER=codex`, rather than silently using Codex.
7. Generate a `new-task claude-impl` template with safety boundaries and validation commands.
8. Inject a safety footer into every implementation prompt:
   - offline/local workspace changes only
   - no live scans, exploits, fuzzers, brute force, callbacks, or target-touching automation
   - no changes to scope, loot, credentials, `.env`, tokens, private keys, scheduler/deployment/billing/OAuth settings
   - stop with a blocking note if target interaction or secrets are required
9. Fix multi-stage wrapper locks so one pipeline process can re-enter its own lock while still blocking other processes.
10. Update review output so the next implementation request points to `claude-impl` and the JSON usage artifact, not only Codex.

Verification checklist:

```bash
bash -n bin/hermes
HACKLAB=/path/to/repo ./bin/hermes --dry-run claude-impl
HACKLAB=/path/to/repo ./bin/hermes --dry-run pipeline
HACKLAB=/path/to/repo ./bin/hermes review
git diff --check -- bin/hermes .hermes.md HERMES_WORKFLOW.md handoff/model_usage_routing_policy.md
claude auth status --text
```

Important distinction: dry-run validates routing but does not consume Claude Code usage. A real `claude-impl` run should create the usage JSON artifact.

## Handling max-turn implementation runs

A bounded Claude Code implementation run can end with `subtype: error_max_turns` / `terminal_reason: max_turns` and still produce the desired workspace changes plus a usable JSON usage artifact. In that case, do not classify the project slice as failed just because the wrapper result is non-success.

Recovery pattern:

1. Treat the raw JSON usage artifact as proof of route consumption, not as proof of correctness.
2. Inspect the workspace state and expected changed files from Hermes, not from Claude Code self-report alone.
3. Run focused compile/unit tests for the new slice, then the relevant chain tests, then `hermes review`.
4. If Claude Code missed a small safety/test/handoff detail, let Hermes make the narrow local fix and record that the wrapper hit max turns.
5. Ensure `handoff/claude_code_result.md` exists even after error/max-turn exits so future agents and the user do not have to parse raw JSON first.
6. In Windows Git-Bash / MSYS wrappers, explicitly verify the result-file fallback path after a max-turn run; output/stderr handling can differ from Linux shells.

Example audit fields to report back:

```text
subtype: error_max_turns
terminal_reason: max_turns
session_id: <uuid>
num_turns: <n>
total_cost_usd: <amount>
models: <model list>
```

Safety-sensitive repos still require Hermes verification before saying the slice is done: compile, focused tests, relevant chain tests, `git diff --check`, and the project review gate.