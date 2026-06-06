> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Module Bundles — Script-first Context Modules

Status: active design direction
Date: 2026-05-21
Source: `handoff/phase4b_script_first_architecture_reset_20260521.md`

A module bundle is a reusable, context-driven combination of scripts. It is not just a JSON manifest.

## Desired loop

```text
preview + recon results
→ choose module bundle by context
→ if no bundle fits, choose scripts from `scripts/SCRIPT_INVENTORY.md`
→ execute small script combination
→ review result usefulness and false positives
→ promote useful combination into a module bundle
→ repeat
→ report
```

## Bundle shape

Each bundle should answer:

- What context triggers this bundle?
- Which scripts run, in what order?
- What inputs are required?
- What outputs are expected?
- What is explicitly forbidden?
- What review decides whether to promote/report/defer?
- How does it contribute to a pentest report?

## Lightweight bundle template

```markdown
# <bundle_id>

Status: draft | active | retired
Use when: <preview/recon conditions>
Do not use when: <scope/risk exclusions>
Inputs: <URLs, paths, recon summaries, target class>
Scripts:
  1. <script path> — <purpose>
  2. <script path> — <purpose>
Caps: <request/rate/runtime caps if target-touching>
Outputs: <artifact paths/formats>
Review:
  - <false positive check>
  - <manual verification check>
Report contribution: <none | candidate note | evidence packet | report section>
Promotion rule: <when this bundle becomes active/reusable>
```

## Relationship to existing contracts

Existing `modules/checks/**/module.json`, profiles, validators, and preview contracts are guardrails. They may be referenced by a bundle, but they should not hide the practical script workflow.

Use heavy contracts when:

- activating real bug-bounty/public/client targets;
- creating durable report evidence;
- promoting a bundle into platform automation;
- using dangerous script classes such as SQLi, LFI, SSRF, brute force, OAST, broad crawling, or destructive checks.

Otherwise keep bundle specs short and practical.
