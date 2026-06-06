> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# OWASP Top 10 Release Coverage and Lab Testing Plan

Status: active
Source: Hermes + OWASP official project/repo lookup
Date: 2026-05-21
Repo truth: <user-home> <user-home> <user-home> <user-home>

## Decision

OWASP Top 10 is not published every calendar year. The Cybersec Lab test plan should track every official OWASP Top 10 Web Application release edition, not invent yearly Top 10 lists for years without an official release.

Official release editions currently tracked:

- 2003
- 2004
- 2007
- 2010
- 2013
- 2017
- 2021
- 2025

## Project interpretation

- 2021 remains the currently implemented module taxonomy for the local lab pipeline until migration is reviewed.
- 2025 is the latest release edition and should be mapped offline before being used as the primary taxonomy.
- 2003-2017 are retained for historical traceability, renamed/merged-risk mapping, regression thinking, and missed-class gap analysis.
- Historical release coverage does not authorize new runtime tests by itself.

## Safety boundary

This note is methodology/strategy only.

It does not authorize:

- target-touching execution;
- public or real bug bounty target testing;
- scanner/template execution;
- exploit payloads;
- credential/brute-force/callback/pivot/destructive/loot workflows;
- automatic confirmed-finding promotion.

Any local-lab target-touching module still needs a run card, safety review, explicit approval, bounded request plan, pre/post health, redaction, recovery, and candidate-only output semantics.

## Next safe offline task

Create an OWASP Top 10 2003→2025 traceability matrix:

- release edition;
- category name;
- current equivalent or merged category;
- mapped Cybersec Lab module/checklist;
- runtime tier;
- status: planned / fixture-only / metadata module / local-lab run-carded / blocked.

This task should be offline/catalog-only first.
