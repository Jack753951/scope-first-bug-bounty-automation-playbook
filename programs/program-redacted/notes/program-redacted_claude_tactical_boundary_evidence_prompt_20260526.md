> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code <program-name>-specific review — adversarial/boundary/evidence roles

Read-only local review. Do not touch live targets, browser, VM, accounts, network, credentials, tokens, screenshots, or report submission.

Use canonical roles: `adversarial-planner`, `boundary-engineer`, `evidence-critic`. You may combine these roles in one artifact, but separate the findings by role.

Read these files directly:
- `.hermes.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/current_artifact_index.md`
- `handoff/accepted_changes.md` (recent relevant entries are sufficient)
- `notes/obsidian_projects/Cybersec Lab.md`
- `programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md`
- `programs/<program-redacted>/scope.json`
- `programs/<program-redacted>/lane_state.json`
- `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md`
- `config/worker_roles.txt`
- Optional compact packet: `handoff/program-redacted_multi_agent_memory_sync_packet_20260526.md`

Task: test the new multi-agent workflow on the current <program-name> lane. Review the candidate `<program-name>-shared-inbox-object-permission` and decide whether it is ready for anything beyond passive UI/docs mapping. Preserve realistic attacker thinking, but compile into bounded proof surrogate only if safe and authorized. Do not propose scanner/fuzzer/DAST, token/API calls, invites, role changes, object creation, external channel connection, customer/non-owned data, callbacks/OAST, or report submission as immediate actions.

Return exactly this structure:

## Worker identity
- route: claude-code
- tool/runtime: <visible model/runtime/session if available>
- role: adversarial-planner, boundary-engineer, evidence-critic
- task file: handoff/program-redacted_claude_tactical_boundary_evidence_prompt_20260526.md
- output artifact: handoff/claude_program-redacted_tactical_boundary_evidence_review_20260526.json
- invocation evidence: claude -p <this prompt> --allowedTools Read,Grep,Glob --max-turns 12 --output-format json > handoff/claude_program-redacted_tactical_boundary_evidence_review_20260526.json

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
