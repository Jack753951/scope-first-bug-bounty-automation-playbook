> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P2-16 Triage Draft Cadence

These markdown files are workflow-validation drafts only. They are not findings, not evidence, not reports, and not published artifacts.

Cadence:

1. The offline fixture produces deterministic candidate finding JSON.
2. A Claude/Cowork or human reviewer reads the candidate IDs and this draft language.
3. The reviewer decides whether the candidate should be manually verified.
4. Only after manual verification and approval may language be copied into a report draft.

Boundaries:

- Do not add host names, URLs, IP addresses, raw header values, environment values, secrets, or client data.
- Do not treat scanner output as confirmed.
- Do not write anything to `runs/`, `evidence/`, `loot/`, or `reports/` from this triage step.
- Do not promote these drafts automatically.
