> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# OWASP Top 10 traceability matrix and 2025 migration review

Use this note after the workspace has agreed to cover every official OWASP Top 10 web-application release edition and needs to move from catalog coverage to migration planning without accidentally authorizing runtime tests.

## Trigger

- The user asks for all official OWASP Top 10 releases to be represented in a testing plan.
- A 2025/latest OWASP Top 10 release exists but the current project taxonomy is still 2021-based.
- The next slice is Phase 4B / modular lab-check planning and should remain offline/docs-only.
- The user asks for long-term goal/current phase and the safest next action is methodology or mapping, not target interaction.

## Safe sequence

1. Keep the implemented runtime taxonomy stable, usually `OWASP Top 10 2021`, until migration is reviewed.
2. Build a documentation/catalog-only traceability matrix across official editions:
   - 2003
   - 2004
   - 2007
   - 2010
   - 2013
   - 2017
   - 2021
   - 2025
3. For every category, record:
   - release year
   - category ID/name
   - mapped current taxonomy category
   - mapping confidence: `high`, `medium`, or `low`
   - mapping note
   - module/catalog implication
   - runtime tier or blocked posture
   - implementation status
   - `runtime_authorization: false`
4. Add a human-readable methodology note that explains catalog-vs-runtime status.
5. Update repo handoff / active strategy queue and Obsidian project index if this changes the next active slice.
6. Validate the machine-readable matrix with a parser and a custom invariant check:
   - exact official release years only, no invented annual editions
   - 8 editions × 10 categories
   - all categories include mapping confidence
   - all `runtime_authorization` values are false
   - current runtime taxonomy remains unchanged
   - no wording such as `runtime_active`, `implemented_primary`, or `confirmed` sneaks in.

## 2025 migration review note shape

After the traceability matrix, the next safe slice is usually an offline 2025 migration review note. It should answer:

1. Which 2021 modules can keep behavior and only gain a 2025 alias.
2. Which categories need documentation-only label updates.
3. Which 2025 categories are materially new or changed and require checklist-only planning.
4. Which runtime classes stay blocked until explicit authorization and review, e.g. injection active probes, auth attacks, SSRF callbacks, brute force, DoS/exception abuse, exploit chains.
5. Which actions are explicitly not happening: no target interaction, scanner run, module runner change, scope change, schema promotion, report submission, or finding confirmation.

## Status-answer wording

When summarizing the project, say the long-term goal and phase plainly:

- Long-term goal: build a modular, reviewable, safely gated bug-bounty/testing pipeline that can eventually move from lab calibration to authorized targets.
- Current phase: Phase 4B OWASP Top 10 modular lab-check library, if that is what repo handoff confirms.
- Current state: catalog/methodology coverage and offline mapping, not confirmed vulnerabilities and not live bug-bounty activation.
- Safest next action: an offline 2025 migration review note before any runtime module or Wave 2 active-probe work.

## Pitfalls

- Do not let a taxonomy matrix become implicit execution approval. Every row should be non-authorizing unless a later reviewed runtime gate changes that.
- Do not promote 2025 to the implemented taxonomy just because it is the newest release.
- Do not start Wave 2 probes, scanner runs, or live adapters from a status/methodology question.
- Do not store project-specific matrix contents in global memory or in this skill; keep artifacts in repo handoff/modules and Obsidian project notes.
