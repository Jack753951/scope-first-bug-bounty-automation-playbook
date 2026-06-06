> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Prompt For Codex

When Cowork updates `handoff/cowork_proposal.md`, give Codex this task:

```text
Please review handoff/cowork_proposal.md with multiple agents.

First classify the proposal under handoff/review_tiering_policy.md:
- Review tier: T0/T1/T2/T3/T4/T5
- Milestone boundary:
- OSS Recon Gate required: yes/no and why
- Escalation triggers present:

Split the review across:
1. Strategy/prompt/product intent.
2. Code and operational risk.
3. Tests/docs/workflow consistency.

Keep the format easy for Cowork and Hermes to understand. Implement only safe changes. If the diff crosses into a higher-risk tier, route back instead of broadening scope silently. Run available validation checks. Update handoff/codex_review.md and handoff/accepted_changes.md only after Hermes accepts the change.
```
