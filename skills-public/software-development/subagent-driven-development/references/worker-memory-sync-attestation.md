> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Worker memory-sync attestation pattern

Use this when a repo relies on multiple agents or CLI workers (Hermes, delegate_task reviewers, Claude/Cowork, Claude Code Impl, Codex, OpenCode) and needs evidence that each worker read the same project memory and left a useful collaboration artifact.

## Problem

Prompt-level instructions such as "read the handoff files first" are necessary but weak. They do not prove which context the worker used, and review commands can silently pass while rolling worker artifacts are stale, legacy, or missing the fields needed for synthesis.

## Durable pattern

1. Define canonical memory entrypoints in the repo wrapper prompt.
   - Examples: `.hermes.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/current_artifact_index.md`, `handoff/accepted_changes.md`, project Obsidian index.
   - Include artifact/navigation indexes, not only strategy docs, so workers can distinguish active, historical, local-only, and operator-owned files.

2. Require every non-template worker result to include a machine-checkable contract:

```markdown
## Worker identity
- route:
- tool/runtime:
- role:
- task file:
- output artifact:

## Context read attestation
- [x] handoff/current_navigation.md
- [x] handoff/active_strategy_queue.md
- [x] handoff/current_artifact_index.md
- [x] handoff/accepted_changes.md
- [x] notes/obsidian_projects/Cybersec Lab.md
Missing / not read:
- none

## Validation
- Local checks run:
- Files changed/reviewed:
- Safety boundary checked:

## Verdict
PASS / APPROVED / REQUEST_CHANGES / BLOCKED / FAILED / WARNING / SKIP / INCOMPLETE
```

3. Add a static checker rather than relying on human reading.
   - Check required headings.
   - Check required identity fields are present and not placeholders.
   - Check each required context path is on a checked `[x]` line, not merely mentioned.
   - Fail when `Missing / not read:` is absent or not explicitly `none` for a passing artifact.
   - Check validation fields and an explicit verdict inside the Verdict section.
   - Treat missing rolling artifacts as `SKIP` by default when the route may not have run; support a `--require-present` mode for pipeline-specific gates.

4. Wire the checker into the repo review command and worker wrapper as enforcing gates.
   - If a present, non-template worker artifact fails, review must return non-zero.
   - After a worker route runs, validate that route's output immediately with `--require-present --file <artifact>` so a noncompliant result cannot be reported as successful.
   - Advisory-only output is insufficient: it lets unsynchronized or non-attested collaboration pass.
   - Missing artifacts can remain skip/pass for generic review if no route has run yet.

5. When role separation matters, add a narrow canonical role vocabulary instead of a broad orchestration framework.
   - Keep roles in a small local file such as `config/worker_roles.txt` with lowercase hyphenated names.
   - Enforce `role:` against that vocabulary when the file exists, while preserving `other:<reason>` for unusual roles.
   - Add an opt-in `--roles-required` coverage mode for pipeline gates that need one passing artifact per role; do not make generic review fail just because a route has not run.

6. Archive legacy rolling worker artifacts that predate the contract.
   - Do not let stale `cowork_result.md`, `claude_code_result.md`, or `codex_review.md` keep failing forever or appear current.
   - Move them under a rolling archive with a `pre_attestation` marker, then require future rolling outputs to comply.

7. Add regression tests for both prompt injection and checker behavior.
   - Prompt tests: every worker route prompt contains required context entrypoints and output contract headings.
   - Checker tests: good artifact passes; missing context path fails; unchecked `[ ]` paths fail; `Missing / not read: all` fails; missing role/tool/task/output fields fail; missing verdict fails.
   - Review integration tests: repo review fails on a present noncompliant artifact and passes when no route has run yet.

## Pitfalls

- Do not accept path strings alone as proof. Require checked `[x]` boxes on the same lines.
- Do not make the gate fail just because no worker route has run yet; that blocks normal local review before delegation. Use `SKIP` by default and `--require-present` only where a route is mandatory.
- Do not add a broad role-scaffolding framework before there is a concrete consumer. Start with canonical role vocabulary plus opt-in role coverage checks.
- Do not make role coverage mandatory in generic review. It belongs in a pipeline-specific gate, otherwise normal single-route work becomes blocked.
- Do not treat archived legacy artifacts as current evidence. Rolling files are convenience pointers, not immutable history.

## Good completion evidence

A hardening slice is complete when:

- The wrapper prompt contains the required memory entrypoints and worker output contract.
- The checker fails noncompliant present artifacts and passes/skips appropriately.
- The repo review command returns non-zero on attestation failure.
- Tests prove unchecked/not-read, missing identity fields, missing verdict, and review-gate enforcement.
- An independent reviewer verifies that the gate is enforcing, not only reporting.
