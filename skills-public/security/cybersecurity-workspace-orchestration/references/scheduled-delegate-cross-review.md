> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Scheduled delegate_task cross-review for cybersec workspace health jobs

Use this reference when a scheduled/cron project-health review asks for multi-party review evidence before final reporting, especially when the job explicitly says not to degrade into a Hermes-only review.

## Pattern

1. Keep the run offline/local-only unless the operator explicitly authorizes target-touching work.
2. Read the required policy/navigation files first: `.hermes.md`, review tiering, multi-party decision policy, OSS Recon Gate when applicable, current navigation/active queue, and recent accepted changes.
3. Collect a concise evidence packet before reviewer delegation:
   - job name/date and workdir/repo/branch/PR
   - required files read
   - local command outputs such as `git status --short --branch`, `git log --oneline -5`, `git remote -v`, `.agent.lock`, and `./bin/hermes review`
   - current phase/current navigation summary
   - safety boundaries and explicit non-actions
4. Call `delegate_task` with three independent role-separated reviewers, preferably batch/parallel:
   - Strategy/Cowork: current phase, goal drift, one-vulnerability/max-impact lane, handoff/Obsidian durability, next-step value.
   - Engineering/Codex: repo/script/test/handoff structure, accepted_changes, verifiable evidence, validation gaps, technical debt; read-only/static checks only.
   - Safety/Authorization: scope gates, target-touching risk, loot/secrets, callbacks/OAST/tunnels/pivots, VM/network/scheduler boundaries.
5. Require each reviewer to return verdict, blocking defects, non-blocking improvements, validation gaps, visible model/runtime if exposed, and safe next action.
6. If `delegate_task` is unavailable, times out, or a role lacks evidence, the final synthesis must explicitly say `三方審查未完整完成` and name the missing reviewer/evidence. Do not claim multi-party review completed from Hermes local validation alone.
7. Hermes synthesis compares the three outputs, resolves disagreements under `handoff/multi_party_review_decision_policy.md`, and issues one decision: `CONTINUE`, `REVISE`, `PAUSE`, `ESCALATE`, or `BLOCKED` plus the repo's Final Decision Block.
8. If artifacts are created, validate before commit/comment:
   - `git diff --check`
   - narrow secret scan over staged review artifacts
   - `HACKLAB=<repo> ./bin/hermes review`
   - stage explicit periodic-review paths only
   - use `gh pr comment --body-file` for Markdown/backtick-safe PR updates.

## Final report shape for Traditional Chinese scheduled reviews

Include these sections:

1. `Route/tool`: state that three-party cross-review used `delegate_task` plus Hermes synthesis.
2. `Reviewer evidence`: one bullet per reviewer with `PASS` / `CONCERN` / `BLOCKED` style status.
3. `Cross-review disagreements or gaps`.
4. `Hermes final decision` with the policy Final Decision Block.
5. `Safe next action`.
6. `Artifact/handoff paths updated or intentionally not updated`.

## Pitfalls

- Do not simulate three reviewers inside Hermes's own response when the job requires real delegated reviewers.
- Do not let scheduled health review run target-touching tools, vulnerability scripts, scanners, or live advisory bootstrap actions.
- Do not commit unrelated dirty worktree changes; commit only explicit periodic review/status artifacts.
- Do not update `accepted_changes.md` for pure periodic-review artifacts unless the job or repo policy specifically treats the review itself as an accepted project change.
- Do not call `send_message` from cron jobs whose delivery is already handled by the scheduler; put the report in the final response.