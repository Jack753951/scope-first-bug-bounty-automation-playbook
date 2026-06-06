> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Worker Max-Turn / Partial Artifact Recovery Routing

Use this pattern when an autonomous worker wrapper exits with a max-turn or similar incomplete-status error but may have written partial or useful repo artifacts.

## Routing rule

- Do not save the failure as Hermes durable memory unless it reveals a stable user preference or cross-project routing principle.
- Treat the failed run as project-local engineering state: logs, partial outputs, usage JSON, and recovery decisions belong in repo handoff / accepted changes / named artifacts.
- Capture only the reusable recovery pattern in this skill.

## Procedure

1. Inspect the wrapper log and any rolling result/archive files before deciding the run failed completely.
2. If a rolling file was overwritten or archived, read both the current rolling pointer and the archived copy.
3. If useful partial output exists, promote the useful content into a named audit artifact for the slice, then keep the rolling pointer as a convenience pointer only.
4. If the wrapper max-turned after making workspace changes, do not report success from the worker alone. Verify live repo state yourself:
   - changed-file boundary against the task;
   - focused tests;
   - broader local validation;
   - safety/forbidden-vocabulary scan when applicable;
   - clean/expected git status.
5. Record the worker status honestly in the named result artifact, including route/tool, visible model/runtime if exposed, max-turn/error status, usage JSON path, and what Hermes fixed or verified afterward.
6. If recovery required changing expectations to match existing runtime behavior, state that explicitly as a deferred assertion or separate follow-up; do not smuggle runtime changes into a locked docs/tests-only slice.
7. Update the active strategy queue only with current lane/next-step implications, not with a long run transcript.
8. Commit/push only after verification passes and the repo handoff explains the recovery.

## Pitfalls

- Do not discard an untracked archive file just because the wrapper exited non-zero; it may contain the last useful worker result.
- Do not treat `error_max_turns` as either automatic failure or automatic success. It is a recovery state requiring local inspection and verification.
- Do not store run IDs, PR comments, timestamps, costs, or commit SHAs in global memory. They belong in the repo handoff or named artifacts.
- Do not turn a transient max-turn incident into a negative durable claim that the worker/tool is broken.

## Good handoff wording

```text
Worker reached max turns after producing workspace changes. Hermes inspected the artifacts, completed local fixup/verification, recorded the named result, and preserved the usage JSON. Boundary remained tests/fixture/handoff only; no runtime or activation files changed.
```
