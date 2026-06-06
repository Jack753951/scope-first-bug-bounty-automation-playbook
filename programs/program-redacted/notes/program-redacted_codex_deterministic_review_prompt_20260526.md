> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Codex <program-name>-specific deterministic review

Read-only local review. Do not touch live targets, browser, VM, accounts, network, credentials, tokens, screenshots, or report submission. Do not execute target-touching commands. Local file reads only; local JSON/static checks are okay if sandbox permits.

Use canonical role: `deterministic-reviewer`.

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

Task: test the new multi-agent workflow on the current <program-name> lane. Deterministically review whether `<program-name>-shared-inbox-object-permission` is ready for anything beyond passive UI/docs mapping. Check consistency of candidate status, lane_state worker_route_status, scope/safety boundary, and missing evidence. Do not grant authorization; Hermes remains final gate.

Return exactly this structure:

## Worker identity
- route: codex
- tool/runtime: <visible runtime/model/session if available>
- role: deterministic-reviewer
- task file: handoff/program-redacted_codex_deterministic_review_prompt_20260526.md
- output artifact: handoff/codex_program-redacted_deterministic_review_20260526.md
- invocation evidence: codex exec --sandbox read-only --output-last-message handoff/codex_program-redacted_deterministic_review_20260526.md - < handoff/program-redacted_codex_deterministic_review_prompt_20260526.md

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
