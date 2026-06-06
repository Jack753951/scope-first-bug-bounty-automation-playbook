> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Periodic Third-Party Strategy / Project Review

Use when a cybersecurity workspace should be periodically reviewed by independent models, not only when a single patch needs QA.

## Purpose

Run an offline project-health and roadmap review on a cadence (weekly by default) so the project does not drift into one-off scripts, monolithic tooling, weak safety gates, or stale strategy.

The review should ask both:

- **Codex** for engineering/systematization review: code organization, modularity, schemas/contracts, tests, maintainability, technical debt, and next implementation steps.
- **Claude/Cowork** for strategy/product-security review: roadmap fit, safety governance, scope posture, bug bounty workflow quality, agent-assisted review, long-term extensibility, and sequencing.

Hermes then synthesizes both into prioritized actions.

## Safety Boundary

Periodic reviews are offline project review only. They must not:

- run live scans, probes, fuzzers, exploit tools, or modules against targets
- modify `config/scope.txt`
- publish reports
- transmit loot, credentials, or secrets
- add exploit payloads or weaponized PoC code

If secrets are encountered in files or logs, write `[REDACTED]` in review output.

## Recommended Output Layout

Each run creates:

```text
handoff/periodic_reviews/YYYY-MM-DD/
  project_snapshot.md
  codex_strategy_review.md
  claude_strategy_review.md
  hermes_synthesis.md
```

## Project Snapshot Contents

Include safe, local-only facts:

- current phase/status
- key context/handoff files
- recent accepted changes
- `recon.sh` line count or equivalent monolith indicators
- directory layout summary
- presence/status of `modules/`, `scripts/core/`, `runs/`
- status of empty intent directories and README hygiene
- current schemas/validators/tests
- local static review result
- known constraints and non-blocking review items

## Third-Party Review Template

Prompts for Codex and Claude/Cowork should request:

1. Current-state assessment
2. What is working well
3. Structural risks / technical debt
4. Extension/systematization opportunities
5. Safety/scope concerns
6. Recommended next phases
7. Non-obvious ideas worth considering
8. Things to avoid

Also require the review to distinguish:

- blocking issues
- non-blocking improvements
- strategic recommendations
- architecture fit against extensibility, updateability, modularity, safe automation, agent-assisted analysis, testing, and roadmap alignment

## Hermes Synthesis Template

`hermes_synthesis.md` should include:

```text
# Periodic Review Synthesis — YYYY-MM-DD

## Executive Summary
## Shared Recommendations
## Codex-Specific Recommendations
## Claude/Cowork-Specific Recommendations
## Disagreements / Tradeoffs
## Immediate Next Actions
## Defer / Avoid
## Safety Notes
## Suggested Phase Order
## Review Coverage / Gaps
```

## Scheduling Pattern

If Hermes Agent cron is available, create a weekly job by default, or use the operator's requested cadence when specified. Examples:

```text
# weekly Monday 09:00
schedule: 0 9 * * 1

# every two days at 09:00
schedule: 0 9 */2 * *

workdir: <cybersec project root>
delivery: origin
skills: cybersecurity-workspace-orchestration
```

The job prompt should instruct Hermes to collect the snapshot, invoke Codex and Claude/Cowork if available, synthesize results, update handoff records, and continue even if one reviewer CLI is unavailable by recording the failure as a review gap. When the user asks to change cadence, update the existing cron job rather than creating a duplicate.

## Pitfalls

- Do not confuse periodic strategy review with implementation review. Periodic review is broader and should produce roadmap/systematization advice, not just blocker checks.
- Do not let scheduled reviews interact with targets. They are for local files, docs, schema, tests, and handoff state only.
- Do not treat one model's suggestion as automatically accepted. Hermes should reconcile Codex/Claude recommendations against scope, safety, and the project roadmap before turning them into tasks.
- Prefer contract/schema/core-helper work before migrating many vulnerability modules; otherwise module code may duplicate scope, evidence, and output logic.