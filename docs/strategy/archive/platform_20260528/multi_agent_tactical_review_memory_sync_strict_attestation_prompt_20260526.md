> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Strict attestation review: multi-agent tactical review + memory sync rule

Read-only local workflow review. Do not touch live targets, browsers, VMs, accounts, network, credentials, tokens, screenshots, or report submission.

You MUST read these files and then output exactly the Markdown headings/field labels below:
- `.hermes.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/current_artifact_index.md`
- `handoff/accepted_changes.md` (recent relevant section is sufficient; still list the file as checked)
- `notes/obsidian_projects/Cybersec Lab.md`
- `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md`
- `programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md`
- `programs/<program-redacted>/scope.json`
- `programs/<program-redacted>/lane_state.json`
- `config/worker_roles.txt`

Review focus: Does the current rule now enforce actual Claude/Cowork + Codex execution, memory-sync context, Hermes final authorization, invocation evidence, and passive-only fallback for unavailable routes? What remains missing before <program-name> bounded proof?

Output EXACTLY this structure:

## Worker identity
- route: <route>
- tool/runtime: <tool/runtime/model if visible>
- role: deterministic-reviewer
- task file: handoff/multi_agent_tactical_review_memory_sync_strict_attestation_prompt_20260526.md
- output artifact: <your output artifact path>

## Context read attestation
- checked reads:
  - .hermes.md
  - handoff/current_navigation.md
  - handoff/active_strategy_queue.md
  - handoff/current_artifact_index.md
  - handoff/accepted_changes.md
  - notes/obsidian_projects/Cybersec Lab.md
  - docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md
  - programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md
  - programs/<program-redacted>/scope.json
  - programs/<program-redacted>/lane_state.json
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
- REQUEST_CHANGES or PASS:
- required next action before <program-name> bounded proof:
