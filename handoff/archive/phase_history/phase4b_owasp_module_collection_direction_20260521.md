> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B Direction — OWASP Top 10 Module Collection and Local-Lab Trials

Date: 2026-05-21
Status: direction accepted for planning/catalog only; runtime execution remains gated per module.

## Operator intent

The operator wants to collect scripts/checks for common OWASP vulnerabilities, trial them on the local victim lab, and modularize the useful checks.

## Hermes interpretation

Proceed, but split into safe phases:

1. Catalog OWASP Top 10 check ideas and OSS design references.
2. Track every official OWASP Top 10 web-application release edition in the planning matrix. OWASP Top 10 is not annual; tracked release years are 2003, 2004, 2007, 2010, 2013, 2017, 2021, and 2025.
3. Create data-only/offline module manifests first.
4. Write one script-specific run card per target-touching module class.
5. Trial only against the local intentionally vulnerable Juice Shop lab after run-card review.
6. Convert outputs into candidate-only packets and lab-only reports.
7. Modularize only the parts that pass safety, false-positive, and evidence-quality gates.

## Current authorization boundary

Authorized runtime target class:

```text
local lab / intentionally vulnerable app only
current observed lab target: http://<lab-ip>:3000/
```

Not authorized:

```text
public targets
real bug bounty targets
client targets
callbacks/OAST/reverse shells
credential attacks/brute force
persistence/stealth/malware
state-changing destructive actions
recursive downloads/loot collection
automatic confirmed-finding promotion
```

## Review classification

Milestone: `Phase 4B — OWASP Top 10 modular lab-check library`

- Current catalog/plan slice: T1/T2, no target interaction.
- Future manifests/profiles/importers: T3 + OSS Recon Gate.
- Future local-lab target-touching scripts: T4 per script, explicit operator approval per run.
- Public/bug-bounty/client activation: not covered.

## Artifacts created for this direction

- `.hermes/plans/owasp-top10-module-collection-and-lab-trial-20260521.md`
- `modules/owasp_top10_lab_module_catalog.json`
- `modules/OWASP_TOP10_LAB_MODULE_CATALOG.md`

## First recommended implementation slice

Create dry-run/offline manifests for the first safe metadata modules:

1. `level1.directory_listing_metadata`
2. `level1.robots_securitytxt_metadata`
3. `level1.api_docs_metadata`
4. `level1.dependency_manifest_metadata`

These must not execute network requests yet. They only declare module identity, risk, tags, output posture, and safety gates.

## First recommended runtime trial after manifests

Use the already successful `/ftp/` workflow as the model:

```text
directory_listing_metadata
→ run card
→ safety review
→ bounded local-lab execution
→ false-positive review
→ candidate packet/report draft
```

## Decision

`APPROVE_PLANNING_AND_CATALOG_ONLY`

Hermes may continue with offline/catalog/manifest work. Hermes may not run a broad OWASP script suite or execute new target-touching modules until each module class has a run card and explicit approval.
