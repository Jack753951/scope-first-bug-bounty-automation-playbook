> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Sustained Codex → Claude/Cowork Review Loop

Use this reference for cybersecurity workspaces where Hermes coordinates engineering changes with separate implementation and independent review agents.

## Durable pattern

For non-trivial or high-impact cybersecurity workspace changes, do not stop after the implementation agent reports success. Keep this sustained loop:

1. **Hermes gates and routes** — classify the task and enforce authorization/scope before any target-touching work.
2. **Codex implements** — concrete scripts, validators, templates, dry-run tests, and handoff updates.
3. **Claude/Cowork independently reviews** — fresh-context review of Codex output for scope bypasses, safety regressions, documentation drift, validation gaps, and route-back items.
4. **Hermes verifies and arbitrates** — run local static checks/safe dry-runs, resolve blocking items, update handoff records, and only then proceed to the next phase.

## When independent Claude/Cowork review is required

Run it after Codex when the change touches:

- authorization or scope enforcement
- `safe_target`, `config/scope.txt`, or per-program scope/rules such as `programs/<slug>/scope.json`
- recon automation, scanners, fuzzing, nuclei, notifications, or any target-consuming path
- report integrity, evidence handling, finding templates, or triage/confirmed wording
- worker orchestration, locks, audit logs, validation wrappers, or safety gates

Skip only for trivial documentation-only edits or explicit operator instruction.

## Recommended handoff artifacts

- `handoff/codex_task.md` — constrained implementation prompt with safety limits.
- `handoff/codex_review.md` — Codex summary, validation, limitations, and open risks.
- `handoff/cowork_<phase>_review.md` — independent Claude/Cowork review verdict and route-back list.
- `handoff/accepted_changes.md` — append-only history of accepted changes and review outcomes.
- `handoff/<phase>_validation_evidence.md` — detailed dry-run matrix, audit excerpts, and known limitations.

## Review prompt shape

Ask Claude/Cowork to read the relevant handoff files and changed scripts, run no live scans/network tools, and write a concise review with:

- Verdict
- Evidence/Requirements Matrix
- Safety Review or Security Findings
- Documentation/Validation Issues
- Route Back To Codex
- Recommendation / whether next phase may start

## Hygiene rule

If validation uses temporary lab roots, archive useful local dry-run audit rows into `handoff/` before deleting the temp directories. Do not leave temp validation directories as the only evidence source.
