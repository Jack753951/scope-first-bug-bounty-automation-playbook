> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Retired structure notes — 2026-05-27 platform pivot

The project pivoted from a broad cybersecurity expert workbench to an authorized bug bounty automation platform. These root-level structures were retired or downgraded because they encouraged manual/operator-driven workflows instead of platform lanes.

## Retired root shells

- `command-library/` — replaced by script-first platform modules and runbooks. Operators should not manually pick command snippets as the main workflow.
- `exploits/` — verification belongs in `modules/`, `labs/proofs/`, or target-specific evidence packets. A generic root exploit folder is unsafe and ambiguous.
- `recon/` — recon implementation should live under `platform/recon/` or stable scripts until migrated.
- `etc/` — contained LLM scratch/noise and a screenshot; removed.
- `<bug-bounty-platform>/code.txt` — empty stray file; removed.

## Downgraded to supporting notes

- `defense/` -> `notes/defense/`
- root learning roadmap/templates/keywords -> `notes/learning/`
- `CYBERSECURITY_OPERATING_SYSTEM.md` -> historical charter
- `intelligence/cve-watch.md` -> `notes/intelligence/templates/`

## Upgraded platform destinations

- Daily/operator process -> `docs/runbook/`
- CVE brief archive -> `intelligence/cve_briefs/`
- Future automation engine -> `platform/`
