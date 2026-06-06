> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec Lab Architecture

## Operating model

- Hermes: coordinator, scheduler, memory keeper, security gate
- Codex: implementation, script safety, tests, automation
- Claude/Cowork: strategy, documentation, threat modeling, independent review

## Safety model

Before active scan, exploit, brute force, callback, or target-touching automation, require one of:

- local lab / intentionally vulnerable app
- CTF / training platform
- user-owned asset
- written client authorization
- explicit bug bounty scope

## Source of truth split

- Repo: executable system, schemas, handoff, reports, audit trail
- Obsidian: long-term knowledge, strategy, learning, distilled review notes
- Hermes memory: compact durable preferences and environment facts only
