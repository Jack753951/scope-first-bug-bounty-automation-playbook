> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code <program-name>-specific review — compact retry

Read-only local review. Do not touch live targets, browser, VM, accounts, network, credentials, tokens, screenshots, or report submission.

Use canonical roles: `adversarial-planner`, `boundary-engineer`, `evidence-critic`.

Read only these focused files/sections:
- `.hermes.md` security gate + worker context sections
- `handoff/current_navigation.md` lines mentioning <program-name>/<program-redacted> and worker context only
- `handoff/active_strategy_queue.md` lines mentioning <program-name>/<program-redacted> and multi-agent only
- `handoff/current_artifact_index.md` lines mentioning <program-name>/<program-redacted> and multi-agent only
- `handoff/accepted_changes.md` recent entries mentioning <program-name>/<program-redacted>/multi-agent only
- `notes/obsidian_projects/Cybersec Lab.md` top 80 lines only
- `programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md`
- `programs/<program-redacted>/scope.json`
- `programs/<program-redacted>/lane_state.json`
- `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md`
- `config/worker_roles.txt`

Task: Review `<program-name>-shared-inbox-object-permission` for practical next-step readiness. Decide if anything beyond passive UI/docs mapping is allowed. Keep output concise.

Return exactly:

## Worker identity
- route: claude-code
- tool/runtime: Claude Code CLI
- role: adversarial-planner, boundary-engineer, evidence-critic
- task file: handoff/program-redacted_claude_tactical_boundary_evidence_prompt_retry_20260526.md
- output artifact: handoff/claude_program-redacted_tactical_boundary_evidence_review_20260526.json
- invocation evidence: claude compact retry, output json path above

## Context read attestation
- checked reads:
  - .hermes.md
  - handoff/current_navigation.md
  - handoff/active_strategy_queue.md
  - handoff/current_artifact_index.md
  - handoff/accepted_changes.md
  - notes/obsidian_projects/Cybersec Lab.md
  - programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md
  - programs/<program-redacted>/scope.json
  - programs/<program-redacted>/lane_state.json
  - docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md
  - config/worker_roles.txt
- missing / not read:
  - none

## Findings
- role-specific findings:
- objections:
- constraints:
- evidence gaps:
- preserved future lanes:

## Validation
- local checks run:
- files changed/reviewed:
- safety boundary checked:

## Verdict
- PASS / REQUEST_CHANGES / BLOCK:
- required next action before <program-name> bounded proof:
