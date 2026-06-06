> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code Task — P3.9 Direction Review

Status: READY_FOR_CLAUDE_IMPL
Date: 2026-05-19
Prepared by: Hermes

Run a T3 design-only direction review using the prompt in:

`handoff/cowork_p3_9_direction_prompt.md`

Write the full review to:

`handoff/cowork_p3_9_direction_review.md`

Write/update the concise worker result to:

`handoff/claude_code_result.md`

Hard constraints:

- Design-only/read-only except the two output files above and normal Hermes worker metadata/rolling archives.
- Do not implement the bridge.
- Do not run live targets or scans.
- Do not touch `config/scope.txt`.
- Do not change runtime code, schemas, modules, reports, scheduler, credentials/OAuth, deployment, billing, or production settings.
- Apply OSS Recon Gate before recommending implementation.
