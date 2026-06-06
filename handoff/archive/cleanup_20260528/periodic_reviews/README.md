> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Periodic Reviews

This directory houses periodic project-health and direction-review artifacts for the cybersec lab. Reviews are informational quality checks, not mandatory approval gates.

The review cadence is informational only. Scheduler or cron configuration is managed outside this directory and must not be inferred from any Markdown file here.

Template lineage: `handoff/periodic_reviews/2026-05-18/` and other dated folders are frozen historical snapshots. `review_template_v0.md` is the current growth-first template; future dated review folders should copy the current template at the time the review is written rather than editing older dated snapshots.

No periodic review artifact carries a `*/0.1-trial` schema header, none is machine-parsed by any candidate-chain consumer, and none is required to be parseable by tools. Periodic reviews are governance and synthesis documents, not candidate workflow contracts.

Authoritative current policy and navigation sources:

- `docs/policy/multi_party_review_decision_policy.md`
- `docs/policy/review_tiering_policy.md`
- `docs/policy/oss_recon_gate.md`
- `docs/policy/memory_and_strategy_routing.md`
- `handoff/active_strategy_queue.md`

Freshness rule: dated periodic-review folders are frozen snapshots. If a frozen packet conflicts with current explicit operator instruction, live repo state, `handoff/accepted_changes.md`, or `handoff/active_strategy_queue.md`, use the live/current source and record the conflict in the next review.
