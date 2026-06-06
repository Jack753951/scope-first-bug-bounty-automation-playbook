> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# OWASP Top 10 2003→2025 Traceability Matrix

Status: active
Source: Hermes + pre-session multi-agent review + OWASP official project/repo references
Date: 2026-05-21
Repo truth: <user-home> <user-home> <user-home>
Related: [[OWASP Top 10 Release Coverage and Lab Testing Plan]]

## Summary

The Cybersec Lab now has an offline/catalog-only OWASP Top 10 release traceability matrix.

Tracked official release editions:

- 2003
- 2004
- 2007
- 2010
- 2013
- 2017
- 2021
- 2025

The matrix maps historical/latest category names to the current project taxonomy, which remains OWASP Top 10 2021 until a separate migration review is accepted.

## Why this matters

OWASP Top 10 is not annual. Tracking only official release editions prevents fake yearly lists and avoids confusing historical taxonomy coverage with runtime test approval.

The traceability matrix helps answer:

- which historical risks map to the current 2021 module/checklist vocabulary;
- which mappings are high-confidence vs tentative;
- which risks are renamed, merged, split, retired, or newly emphasized;
- where 2025 migration needs review before changing module labels or runtime plans.

## Safety boundary

This is not a scanner profile, module runner input, evidence source, report gate, or runtime authorization.

Still blocked:

- target interaction;
- scanner/Kali bridge execution;
- public or real bug-bounty target activation;
- exploit payloads;
- credential/brute-force/callback/pivot/destructive/loot workflows;
- automatic confirmed/verified/reportable/accepted promotion;
- replacing the 2021 runtime taxonomy with 2025 without separate review.

## Next explicit step

Recommended next offline slice:

Create a 2025 migration review note that identifies:

- 2021 modules that can keep their behavior with 2025 aliases;
- module/checklist names that need documentation aliases only;
- 2025 categories needing new checklist-only planning entries;
- high-risk runtime classes that remain blocked until script-specific run cards and approval.
