> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# One-Vulnerability Evidence Packet Template

Status: template
Source: Hermes Cybersec Lab navigation cleanup / proof-pattern standardization
Date: 2026-05-23
Repo truth: `handoff/current_navigation.md`, `handoff/lab_safety_contract.md`

Use this template for one-vulnerability max-impact local-lab proof waves. Keep it short enough to read, but complete enough to rerun and review.

## Reviewer identity

- Reviewer route/tool: `<Hermes | Claude Code CLI | Codex CLI | local QA script | other>`
- Visible runtime model: `<model if exposed>` or `not exposed by tool`
- Provider / CLI version if visible: `<provider/version>`
- Review focus: `evidence quality / safety / reproducibility / report-readiness`
- Limitation: `<what was not independently verified>`

## Target

- Target name:
- Target URL / service:
- Victim route:
- Attacker/tool route:
- Artifact root:

## Vulnerability class

- Class:
- OWASP / CWE mapping if useful:
- One-vulnerability boundary:
- Why this target demonstrates the class:

## Authorized scope

- Scope basis: `local lab | owned asset | CTF/training | explicit program scope`
- Public/real target involved: `no | yes with scope path`
- Safety lane: `local-learning-lab | authorized-assessment | offline-research`
- Disallowed surfaces avoided:

## Route/tool

- Control plane:
- Tool/attacker plane:
- Victim plane:
- Network posture:
- NAT status:
- Tools/scripts used:

## Preconditions

- VM/container state:
- Snapshot/recovery state:
- Target service health:
- Auth/session setup:
- Callback/listener setup if relevant:

## Exploit/probe path

- Discovery path:
- Exact trigger path:
- Payload/command summary:
- Request caps/timeouts/rate:
- Why this is bounded:

## Evidence

Record only enough evidence to prove the claim and rerun/review it. Avoid unnecessary secrets/raw bodies.

- Primary proof artifact:
- Execution/session/browser/file/callback marker:
- Controls / negative checks:
- Pre-health:
- Post-health:
- Callback/browser/file/session proof if relevant:

## Impact

- Verified impact:
- Maximum safe local-lab impact reached:
- Impact not claimed:
- Why this matters for future authorized assessment:

## Controls / false-positive boundary

- What could have been noisy:
- How it was excluded:
- What remains uncertain:

## Cleanup

- Containers/processes removed:
- Files/markers removed or intentionally left in disposable lab:
- NAT/network restored:
- Snapshot/restore used:
- Remaining cleanup debt:

## Rerun commands

```bash
# exact commands or script invocation
```

## Report-readiness

Choose one:

- `local_learning`
- `reusable_methodology`
- `candidate_needs_manual_review`
- `report_ready_lab_only`
- `not_ready`

Decision:

Reason:

Missing before real bug bounty / pentest use:

## 對專案有什麼幫助

- Capability growth:
- Evidence quality improvement:
- Automation/readiness impact:
- False-positive/precondition lesson:

## 新增/更新了什麼

- Scripts:
- Bundles:
- Handoffs:
- Obsidian notes:
- Artifacts:
- Blockers:
- Reusable workflow updates:
