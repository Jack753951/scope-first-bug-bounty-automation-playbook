> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Multi-agent tactical review + memory-sync guidance

Status: active simplified guidance / no target touched
Source: operator correction 2026-05-27: remove unnecessary growth-blocking gates
Repo truth: `handoff/active_strategy_queue.md`, `handoff/current_navigation.md`, `docs/policy/multi_party_review_decision_policy.md`, `notes/obsidian_projects/Cybersec Lab.md`

## Current Rule

Multi-agent review is a quality amplifier, not a mandatory approval gate.

Hermes may proceed without Claude/Cowork/Codex review when the lane is already inside scope, uses owned/local controls, and does not cross a hard stop. This includes local-lab proof iteration, capability-library work, passive mapping, and established in-scope owned-account browser/manual checkpoints.

Use external workers when they are likely to improve tactical coverage, architecture, evidence quality, or dissent. Do not block project growth merely because a worker route is unavailable, slow, unauthenticated, or not yet invoked.

## Hard Stops Still Override

Stop or ask the operator for:

- ambiguous/missing scope or authorization;
- live target scanners/fuzzers/DAST/exploits/callbacks/OAST/tunnels/proxies/pivots outside explicit approval;
- OAuth/integration/webhook/channel/mailbox/API-token/billing/payment/KYC/scheduler/deployment/publishing/report-submission activation;
- secrets, credentials, cookies, tokens, OTPs, passwords, phone numbers, verification links, loot, or customer/non-owned data;
- destructive, persistent, stealthy, evasive, brute-force, resource-exhaustive, malware-like, or uncontrolled behavior;
- report-ready promotion or final submission.

## When Review Is Useful

Prefer actual Claude/Cowork/Codex review for:

- complex live-bounty candidate synthesis where multiple attack paths should be preserved;
- state-changing owned-account proof boundaries;
- report-readiness or final disclosure drafts;
- new reusable runner/module/evidence/report contracts where design mistakes would compound;
- periodic system-health review.

When review is skipped for speed, record only a short note if the skip affects future interpretation. Do not force passive-only state solely because a reviewer did not run.

## Memory-Sync Packet When Workers Are Used

Workers should receive or be instructed to read:

- `.hermes.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/current_artifact_index.md`
- `notes/obsidian_projects/Cybersec Lab.md`
- recent `handoff/accepted_changes.md` entries
- active `programs/<slug>/scope.json` and `programs/<slug>/lane_state.json` when target-specific
- current candidate/evidence packet
- exact safety boundary and stop-before list

Secrets, OTPs, passwords, phone numbers, cookies, tokens, API keys, verification links, raw customer data, and loot stay out of worker packets.

## Compact Worker Artifact Shape

```text
Worker identity / route:
Context read:
Concrete blockers:
Advisory improvements:
Preserved hypotheses / dissent:
Validation checked:
Verdict:
```

A reviewer finding blocks only when it maps to a hard stop, failing validation, malformed consumed contract, or data/capability-loss risk. Generic caution is not a blocker.

## Verification and Sync

After meaningful worker outputs:

1. Run `scripts/check-worker-attestation.py` only when the artifact claims formal worker evidence.
2. Run `bash ./bin/hermes review` when shared contracts, runner-facing JSON, lane state, or broad repo state changed.
3. Preserve concrete dissent and useful hypotheses.
4. Update lane state, current navigation, artifact index, accepted changes, or Obsidian only when the durable route actually changes.

## <program-name> Implication

<program-name> should no longer be kept passive-only solely because a multi-agent review was not freshly run. It remains blocked only by concrete operator/safety gates, currently the independent Account B/session identity issue and the standing hard stops for non-owned data, secrets, external connections, destructive actions, and final submission.
