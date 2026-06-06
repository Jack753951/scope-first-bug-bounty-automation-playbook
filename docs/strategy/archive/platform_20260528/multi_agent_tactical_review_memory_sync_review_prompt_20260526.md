> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Read-only worker review: multi-agent tactical review + memory sync rule

You are reviewing a workflow/process rule only. Do not touch live targets, browsers, VMs, accounts, network scanning, credentials, tokens, scope expansion, report submission, or code execution beyond reading local files.

Required context reads:
- `.hermes.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/current_artifact_index.md`
- `notes/obsidian_projects/Cybersec Lab.md`
- recent relevant `handoff/accepted_changes.md` entries
- `docs/policy/multi_agent_tactical_review_memory_sync_rule_20260526.md`
- `programs/<program-redacted>/notes/program-redacted_authorized_attacker_flow_packet_20260526.md` if present
- `programs/<program-redacted>/scope.json` and `programs/<program-redacted>/lane_state.json` if present

Review focus:
1. Does the rule actually force role-separated collaboration to invoke suitable external/independent workers (Claude/Cowork and Codex) rather than a single model reading/writing MD?
2. Does it require memory synchronization/context handoff so workers know current stage and constraints?
3. Does it preserve safety: no worker may authorize target touching; Hermes remains final authorization/scope gate.
4. What is missing before this should be used for the next <program-name> lane?

Return exactly these sections:

Worker identity
- route/tool:
- visible model/runtime if available:
- role: one of config/worker_roles.txt canonical roles

Context read attestation
- Checked files:
- Not checked and why:

Findings
- Role-specific findings:
- Objections:
- Constraints:
- Evidence gaps:
- Preserved future lanes:

Validation
- Commands/checks performed:
- Commands/checks not performed and why:

Verdict
- PASS / REQUEST_CHANGES / BLOCK
- Required next action before <program-name> bounded proof:
