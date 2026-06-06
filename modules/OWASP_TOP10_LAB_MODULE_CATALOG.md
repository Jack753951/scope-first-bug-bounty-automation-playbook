> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# OWASP Top 10 Local-Lab Module Catalog

Status: data-only planning/catalog artifact.
Date: 2026-05-21.
Runtime authorization: none granted by this file.

This catalog supports Phase 4B: collecting OWASP Top 10 check ideas, trialing safe classes against the local OWASP Juice Shop host-only lab, and modularizing useful checks behind scope/policy gates.

## OWASP Top 10 release coverage policy

OWASP Top 10 is not published every calendar year. The test plan tracks every official web-application Top 10 release edition instead of inventing yearly lists for years where OWASP did not publish a new edition.

Currently tracked official release years:

```text
2003, 2004, 2007, 2010, 2013, 2017, 2021, 2025
```

Planning rule:

- latest edition is the primary taxonomy once its local mapping is reviewed;
- 2021 remains the current implemented module taxonomy until migration is reviewed;
- older editions are retained for regression/traceability, renamed/merged-risk mapping, and gap analysis;
- historical coverage does not authorize automatic runtime testing.

## Current authorized runtime scope

Only this class is currently authorized for runtime trials:

```text
local lab / intentionally vulnerable app
current observed target: http://<lab-ip>:3000/
network: VirtualBox host-only lab
```

This catalog does not authorize public, client, or real bug-bounty target execution.

## What "collect scripts" means here

Allowed now:

- collect OWASP/WSTG/ZAP/Nuclei/ProjectDiscovery design patterns;
- record module candidates and manifests;
- build offline fixtures and validators;
- write script-specific local-lab run cards;
- adapt only safe, bounded logic into project-owned modules after review.

Not allowed by default:

- vendoring random exploit scripts;
- running public PoCs;
- executing scanner templates directly;
- credential attacks or brute force;
- OAST/callback/reverse-shell flows;
- recursive download or loot collection;
- confirmed-finding promotion by automation.

## First safe runtime lane

Start with OWASP A05/A06/A02-style metadata modules because they match the successful `/ftp/` rehearsal:

1. `directory_listing_metadata`
2. `robots_securitytxt_metadata`
3. `api_docs_metadata`
4. `dependency_manifest_metadata`
5. `security_headers_baseline`

Each target-touching version requires a T4 script-specific run card and explicit approval before execution.

## Module lifecycle

```text
catalog entry
→ dry-run/offline manifest
→ local-lab run card
→ independent safety review
→ bounded lab trial
→ output-side false-positive review
→ candidate packet
→ lab-only report draft
→ independent report/safety review
```

Automation output remains triage-only until manual/agent verification, impact, remediation, and retest notes exist.

## Catalog file

Machine-readable catalog:

```text
modules/owasp_top10_lab_module_catalog.json
```

## Release traceability matrix

Historical/latest OWASP Top 10 release mapping is kept separate from the runtime module catalog so taxonomy traceability is not confused with execution approval.

```text
modules/owasp_top10_release_traceability_matrix.json
modules/OWASP_TOP10_RELEASE_TRACEABILITY_MATRIX.md
```

The traceability matrix tracks official release editions only: 2003, 2004, 2007, 2010, 2013, 2017, 2021, and 2025. The current implemented runtime taxonomy remains 2021 until a separate migration review is accepted.
