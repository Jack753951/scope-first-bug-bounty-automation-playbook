> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Role Packet Base Template

Status: template
Boundary: offline/local role artifact only. This template does not authorize live target requests, browser automation, scans/fuzzers/DAST, exploit execution, callbacks/OAST/tunnels, account actions, credential handling, scope edits, evidence deletion, or report submission.

## Worker identity
- route: <cowork | claude-impl | codex | hermes-local | delegate_task | other>
- tool/runtime: <Claude Code CLI | Codex CLI | Hermes delegate_task | Hermes local | other>
- role: <adversarial-planner | boundary-engineer | implementation-worker | deterministic-reviewer | safety-reviewer | evidence-critic | final-synthesizer | other:reason>
- task file: <path>
- output artifact: <path>

## Context read attestation
- [ ] handoff/current_navigation.md
- [ ] handoff/active_strategy_queue.md
- [ ] handoff/current_artifact_index.md
- [ ] handoff/accepted_changes.md
- [ ] notes/obsidian_projects/Cybersec Lab.md
Missing / not read:
- <none or reason>

## Role notes

### Role-specific checklist
- For `adversarial-planner`: 5+ realistic candidates; preserve high-impact blocked ideas; proof surrogate ideas; stop-before list.
- For `boundary-engineer`: scope artifact path; owned controls; callback/OAST/tunnel allowance; state-change boundary; data-contact boundary; destructive-impact boundary.
- For `implementation-worker`: files changed; exact rerun commands; no inline secrets; evidence path under `handoff/live_bounty_evidence/` when applicable.
- For `deterministic-reviewer`: tests/static checks; diff summary; side-effect scan; false-positive controls.
- For `safety-reviewer`: scope artifact verified; forbidden-flow check; operator-gate triggers; PASS/BLOCK/ESCALATE.
- For `evidence-critic`: overclaim check; missing-control check; redaction check; reportability recommendation.
- For `final-synthesizer`: chosen lane or park/preserve; conflict resolution; final decision.

## Validation
- Local checks run:
- Files changed/reviewed:
- Safety boundary checked:

## Verdict
<Use one explicit token: PASS, APPROVED, REQUEST_CHANGES, BLOCKED, FAILED, WARNING, SKIP, or INCOMPLETE.>
