> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# OWASP Top 10 release coverage planning

Use this note when the operator asks whether OWASP Top 10 is annual, asks to include every year in a testing plan, or wants OWASP coverage status for the cybersec/bug-bounty lab.

## Key correction

OWASP Top 10 Web Application Security Risks is not published every calendar year. Do not invent annual Top 10 lists for missing years.

Track every official release edition instead:

- 2003
- 2004
- 2007
- 2010
- 2013
- 2017
- 2021
- 2025

## Planning policy

- Coverage target: every official OWASP Top 10 web-application release edition, not every calendar year.
- Latest edition should become the primary taxonomy only after a local mapping/migration review.
- Keep the currently implemented taxonomy stable until migration is reviewed; in this workspace, the implemented module taxonomy may remain 2021-based while 2025/latest is added as a planning/mapping target.
- Use older editions for historical traceability, renamed/merged-risk mapping, regression coverage, and gap analysis.
- Historical release coverage does not authorize new runtime tests.

## Safe artifact update pattern

For catalog/planning-only updates:

1. Update the machine-readable catalog with a release coverage block, e.g. `official_release_years: [2003, 2004, 2007, 2010, 2013, 2017, 2021, 2025]` and a note that OWASP is not annual.
2. Update the human-readable catalog/plan to state release-edition coverage and the current implemented taxonomy.
3. Update the direction/handoff note to clarify this is planning/catalog only.
4. Append to `handoff/accepted_changes.md` with explicit non-authorization language.
5. Validate JSON with `python -m json.tool` and, if editing repo files, run whitespace/diff checks.

## Wording to use in status answers

Short answer:

"OWASP Top 10 is not annual. The correct coverage unit is each official release edition: 2003, 2004, 2007, 2010, 2013, 2017, 2021, 2025. The test plan should include all of those editions for traceability, while runtime modules remain separately gated by scope, safety tier, and run cards."

When explaining implementation status, distinguish:

- `catalog/planning coverage`: official editions and categories are represented in the plan;
- `implemented reusable pipeline coverage`: module manifests/importers/adapters/review-chain coverage that has tests;
- `runtime authorization`: target-touching execution, which still requires scope, run card, approval, and candidate-only outputs.

## Pitfalls

- Do not say "every year is covered" unless the user explicitly means calendar-year project activity; for OWASP taxonomy, that wording is wrong.
- Do not treat adding 2025/latest coverage as permission to rename existing A01-A10 modules or run new tests immediately.
- Do not turn historical categories into scanner payloads. Map first, then review, then implement only safe candidate-only modules.
