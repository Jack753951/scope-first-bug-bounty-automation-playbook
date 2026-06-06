> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Multi-agent memory-sync execution rule

Use this reference with `authorized-attacker-flow` whenever a candidate lane is non-trivial or may move beyond passive UI/docs observation.

## Non-negotiable rule

Do not treat role-separated review as complete just because Hermes or a single model read an MD file. The workflow must either:

1. actually invoke suitable independent workers such as Claude Code/Cowork and Codex, then verify their artifacts; or
2. explicitly record that the worker route was unavailable/skipped and keep execution limited to passive observation until the operator approves an exception.

## Required worker mix

Default routing:

- Claude Code / Cowork: adversarial-planner, boundary-engineer, safety-reviewer, evidence-critic, strategy reviewer.
- Codex: deterministic-reviewer, schema/script/checklist reviewer, tactical objection reviewer.
- Hermes: final-synthesizer, authorization gate, scope gate, verification runner, memory-sync owner.

For any non-trivial lane, at least two non-Hermes perspectives are mandatory before the lane moves beyond passive UI/docs mapping:

- one actual Claude Code/Cowork tactical, boundary, safety, evidence, or strategy review;
- one actual Codex deterministic, skeptical, schema, script, or checklist review.

`Non-trivial` means any candidate or lane that is `bounded_executable`, `needs_operator_control`, or otherwise crosses beyond passive UI/docs mapping toward object creation, second-account action, invite, role change, token/API use, workflow activation, external channel connection, callback/webhook/OAST, scanner/fuzzer/DAST, or report-ready evidence.

If either non-Hermes route is unavailable, the synthesis must record the attempted command/tool, blocker, timestamp, and fallback decision, and the lane stays passive-only unless the operator approves the exception.

## Memory-sync packet

Before invoking workers, prepare a compact packet or prompt that includes current project state and requires context read attestation. The packet must include or point to:

- `.hermes.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/current_artifact_index.md`
- `notes/obsidian_projects/Cybersec Lab.md`
- recent `handoff/accepted_changes.md` entries
- active `programs/<slug>/scope.json`
- active `programs/<slug>/lane_state.json`
- the current candidate/evidence packet
- exact safety boundary and stop-before list

Do not include secrets, OTPs, passwords, phone numbers, cookies, bearer tokens, API keys, verification links, raw customer data, loot, or private identifiers.

## Worker output requirements

Each worker artifact must include:

- Worker identity
- canonical `role:` from `config/worker_roles.txt` when present
- route/tool and visible model/runtime when available
- invocation evidence: command summary, session/run id when available, raw output path, and JSON usage/run artifact path when available
- context read attestation with checked files
- role-specific findings
- at least one objection, constraint, evidence gap, or preserved future lane
- validation performed
- verdict

Shape-only attestation is not enough for non-trivial lanes. Hermes must verify that the claimed route/tool actually ran, using CLI output paths, run JSON, session id, or another concrete local artifact.

## Verification

After workers finish:

1. Run `scripts/check-worker-attestation.py` when applicable.
2. Run `bash ./bin/hermes review` when project files changed or a lane is about to move state.
3. Hermes synthesis must compare disagreements and select at most one lane.
4. Update lane state/checkpoint and append `handoff/accepted_changes.md`.
5. Update `handoff/active_strategy_queue.md` / `handoff/current_artifact_index.md` if navigation changed.
6. Update the Cybersec Lab Obsidian bridge for durable process/methodology decisions.

## Failure handling

If Claude Code/Cowork/Codex is unavailable, unauthenticated, blocked by max-turns, or times out:

- record attempted command/tool and blocker;
- inspect any partial artifact if a worker may have written one;
- do not claim multi-agent review passed;
- keep lane status `blocked_preserve`, `needs_operator_control`, or passive-only until a real worker run or explicit operator exception.
