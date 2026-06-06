> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Periodic Third-Party Strategy / Project Review Process

Date: 2026-05-15
Status: Active operating process

## Goal

The project should periodically be reviewed by third-party models, not only when a single implementation needs QA.

The review should cover:

- current project state
- future strategy
- architecture fit
- extensibility / updateability / modularity
- safety gates and authorization boundaries
- post-scan agent-assisted analysis
- roadmap sequencing
- technical debt and dead-end structures
- recommendations from both Codex and Claude/Cowork

## Cadence

Default cadence: weekly.

The scheduled job should run without live scanning or target interaction. It is an offline project-health and strategy review only.

## Review Flow

1. Hermes gathers a current project snapshot:
   - key files
   - directory layout
   - recent handoff notes
   - current phase status
   - local static review result
   - known constraints

2. Codex reviews from an engineering/systematization angle:
   - implementation architecture
   - code organization
   - testability
   - schema/contracts
   - modularity
   - refactor risks
   - suggested next implementation steps

3. Claude/Cowork reviews from a strategy/product-security angle:
   - roadmap fit
   - security governance
   - scope/safety posture
   - bug bounty workflow quality
   - agent-assisted review quality
   - long-term extensibility

4. Hermes synthesizes both reviews:
   - shared recommendations
   - disagreements
   - immediate next actions
   - defer/avoid list
   - risk notes
   - suggested phase order

## Required Output Files

Each periodic run should create a directory:

```text
handoff/periodic_reviews/YYYY-MM-DD/
```

Expected files:

```text
project_snapshot.md
codex_strategy_review.md
claude_strategy_review.md
hermes_synthesis.md
```

## Safety Boundary

The scheduled review must not:

- run live scans
- touch external targets
- modify `config/scope.txt`
- publish reports
- execute modules against real targets
- add exploit payloads
- store credentials/secrets in output

Any secrets accidentally seen must be written as `[REDACTED]`.

## Review Template

Third-party reviews should include:

```text
1. Current-state assessment
2. What is working well
3. Structural risks / technical debt
4. Extension/systematization opportunities
5. Safety/scope concerns
6. Recommended next phases
7. Non-obvious ideas worth considering
8. Things to avoid
```
