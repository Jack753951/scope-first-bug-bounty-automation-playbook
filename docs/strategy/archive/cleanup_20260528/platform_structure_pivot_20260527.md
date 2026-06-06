> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Platform structure pivot — 2026-05-27

## Decision

Accept the project pivot from broad cybersecurity expert workbench to authorized bug bounty automation platform.

## Implemented in this cleanup batch

- Root charter rewritten as platform charter.
- README rewritten around bug bounty automation and operator inbox model.
- AGENTS routing changed from broad security roles to detection / lane execution / evidence / review / submission / platform.
- Runbooks moved into `docs/runbook/`.
- Original expert charter and operating system moved into `docs/charter/historical/`.
- Empty root shells retired: `command-library/`, `exploits/`, `recon/`.
- LLM scratch/noise removed: `etc/`.
- Defense and learning assets downgraded to `notes/`.
- CVE brief archive moved under `intelligence/cve_briefs/`.
- `platform/` skeleton created for future detector/pipeline/inbox migration.

## Deferred

- Moving active rolling IPC into `handoff/current/` is deferred until scripts such as `bin/hermes` are updated and tested.
- Full migration from root scripts (`cve_watch.py`, `recon.sh`, `recon_pipeline.py`) into `platform/` is deferred to a separate code-path change.
