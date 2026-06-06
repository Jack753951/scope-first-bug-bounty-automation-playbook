> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Hermes + Cowork + Codex Cybersecurity Workflow

This reference captures a reusable project pattern for authorized cybersecurity workspaces.

## Project Context Files To Read First

- `.hermes.md` — mission, roles, security gate, workstreams, safety rules, validation expectations.
- `HERMES_WORKFLOW.md` — default flow, routing table, wrapper commands, scope gate.

If a path lookup fails on Windows Git-Bash, search for the file before concluding it is missing; path normalization can differ between tools.

## Routing Contract

- Hermes: coordinator, scheduler, memory keeper, task router, and quality gate.
- Cowork: strategy, learning plans, documentation cleanup, research synthesis, report wording.
- Codex: implementation, script safety, repo edits, validation, tests, technical review.

## Workstream Mapping

- Add/fix scripts, parsers, dry-run support, repo validation: `build/automation` -> Codex.
- Roadmap, study plan, protocol references, note cleanup: `strategy/knowledge` -> Cowork.
- Current CVE/advisory/exploit status, weekly review: `threat intelligence` -> Hermes primary sources + Cowork synthesis.
- Firewall, hardening, findings, executive summaries, retest language: `defense/reporting` -> Cowork narrative + Codex tooling.
- Live incident or suspected compromise: `incident response` -> preserve evidence, write case note, avoid cleanup-first actions.

## Active Testing Scope Gate

Pause before active scan, exploitation, brute force, callback, or target-touching automation unless one is explicit:

- local lab / intentionally vulnerable app
- CTF / training target
- user-owned asset
- written client authorization
- explicit bug bounty scope

If none is present, ask for scope instead of giving commands.

## Handoff Files

Keep handoffs easy for human/Cowork/Codex readers:

- `handoff/cowork_proposal.md`: proposal, assumptions, scope/safety notes, recommended changes.
- `handoff/codex_review.md`: feasibility, safety review, implementation notes, validation results, open risks.
- `handoff/accepted_changes.md`: accepted proposal items, rejected/deferred items, rationale, final status.

## Safe Validation Bias

Prefer dry-run, local parsing tests, lab-safe examples, static validation, and report generation. Treat generated reports as disposable unless the user says to preserve them. Do not expose secrets from `.env`, credentials, tokens, or runtime data.
