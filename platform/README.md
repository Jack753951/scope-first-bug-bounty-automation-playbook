> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Platform Core

This directory is the home for the bug bounty automation platform.

Current intended sub-layers:

- `detectors/` — passive/version/exposure detectors for CVEs and product fingerprints.
- `recon/` — target discovery and scope-aware recon pipeline.
- `pipeline/` — daily sweeps, cron/task entrypoints, queue orchestration. Current safe entrypoint: `recurring_substrate_dry_run.py`, which converts offline/passive intel fixtures into operator-inbox candidate JSON without live target contact.
- `bounty/` — lane runner, evidence preview, proof packet assembly.
- `intel/` — CVE/vendor/H1 freshness ingestion and ranking.
- `inbox/` — operator inbox builder and decision summaries. Current safe entrypoint: `operator_inbox_summary.py`, which renders validated dry-run candidate batches into a compact Markdown decision packet.
- `agents/` — multi-agent task prompts, attestations, and review synthesis.

Do not put secrets, cookies, tokens, OTPs, or raw private target data here.
