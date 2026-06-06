> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# OWASP Top 10 Release Traceability Matrix

Status: catalog-only / offline traceability artifact
Date: 2026-05-21
Runtime authorization: none granted by this file
Machine-readable matrix: `modules/owasp_top10_release_traceability_matrix.json`

## Purpose

This artifact tracks OWASP Top 10 Web Application release editions across time so the Cybersec Lab can map older and newer category names to the current project module/checklist vocabulary without confusing taxonomy coverage with runtime authorization.

OWASP Top 10 is not an annual publication. This project tracks official release editions, not calendar years.

Tracked official release editions:

```text
2003, 2004, 2007, 2010, 2013, 2017, 2021, 2025
```

## Current project interpretation

- Current implemented project taxonomy remains `OWASP Top 10 2021`.
- `OWASP Top 10 2025` is tracked as the latest observed official release, but this slice does not migrate the runtime taxonomy.
- Historical releases are used for traceability, renamed/merged/split-risk analysis, regression thinking, and coverage gap analysis.
- Category mappings are planning aids; they may be many-to-one, split, merged, retired, or tentative.
- Mapping a historical category to a current category does not mean the project has a finding, an implemented module, or runtime approval.

## Source policy

Primary references:

- OWASP Top 10 project: `https://owasp.org/www-project-top-ten/`
- OWASP Top10 repository: `https://github.com/OWASP/Top10`
- OWASP 2021-2003 comparison artifact: `https://github.com/OWASP/Top10/tree/master/2021-2003_Comparison`
- OWASP 2021 docs: `https://github.com/OWASP/Top10/tree/master/2021/docs/en`
- OWASP 2025 docs: `https://github.com/OWASP/Top10/tree/master/2025/docs/en`

Uncertainty note: historical category lineage can be non-exact. The matrix records `mapping_confidence` and `mapping_note`; medium/low confidence rows require human review before they influence module design.

## Safety boundary

Allowed by this artifact:

- offline taxonomy traceability;
- module/checklist planning;
- gap analysis;
- 2025 migration planning notes;
- Obsidian/repo documentation updates.

Not authorized by this artifact:

- target interaction;
- scanner execution;
- Kali bridge execution;
- Juice Shop requests;
- public or real bug-bounty target activation;
- exploit payloads;
- credential attacks or brute force;
- callbacks/OAST, proxy, pivot, tunnel, reverse listener, or destructive behavior;
- recursive download or loot collection;
- report submission;
- automatic `confirmed` / `verified` / `reportable` / `accepted` promotion;
- replacing the 2021 runtime taxonomy with 2025 without a separate reviewed migration slice.

## How to use it

Use the JSON matrix to answer:

- Which official OWASP Top 10 editions are tracked?
- Which historical category maps to the current 2021 taxonomy?
- Which project module/checklist might be relevant?
- Which mappings are high-confidence versus tentative?
- Which historical categories should remain blocked or manual-only?

Do not use the matrix as a scanner profile, module runner input, report gate, or evidence source.

## Next safe step

After this catalog slice, the next safe offline task is a 2025 migration review note:

- identify which 2021 modules can keep their names;
- identify which docs/module labels need 2025 aliases;
- identify which 2025 categories need new checklist-only entries;
- keep runtime activation blocked until each module class has its own run card and approval.
