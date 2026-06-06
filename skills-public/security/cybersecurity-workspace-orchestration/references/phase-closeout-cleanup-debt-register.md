> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase Closeout Cleanup / Debt / Deferred Register

Use this reference when a user asks whether a previous phase was really cleaned up before moving to a new cybersecurity-lab phase, especially before lab/live activation.

## Pattern

Do not answer only with a roadmap summary. Produce or update a compact register that separates:

1. **Handled process problems** — workflow, handoff, route/model visibility, review overhead, worker timeout/max-turn caveats, OS/shell quirks.
2. **Technical debt fixed or hardened** — ambiguity removed, tests added, fail-closed behavior verified, drift locks added, direct-read/path/symlink/hash checks strengthened.
3. **Deferred / rejected / parked ideas** — items deliberately not implemented because they would cross a schema/runtime/reporting/target-touching boundary too early.
4. **Activation blockers** — items that must be resolved before any target-touching or lab/live execution.
5. **Small hygiene before release bundle** — local dry-run demo, final review, untracked artifact cleanup/preservation, release notes.

## Recommended document shape

Create a handoff artifact such as:

`handoff/phase<N>_cleanup_debt_deferred_register_<YYYYMMDD>.md`

Include:

- status and scope: documentation synthesis only unless explicitly editing code;
- a direct answer: e.g. “Core cleanup was enough to close Phase N, but not all debt is gone; remaining items are tracked as deferred lanes or blockers.”
- sections for handled process issues, hardened technical debt, deferred ideas, remaining activation blockers, and conclusion;
- explicit safety boundary: no runtime/scope/scanner/module/report/credential/scheduler/target behavior changed.

## Wording guidance

Use precise status language:

- “fixed” only when code/docs/tests were actually updated and verified;
- “hardened” when coverage or fail-closed checks were added;
- “governance-handled” when a problem is controlled by policy/tiering but still requires future discipline;
- “deferred” when a future review trigger is required;
- “blocked” when operator approval and/or T4/T5 review is required before activation.

## Common deferred items before lab/live phases

- schema promotion for trial contracts;
- reviewer-notes / reviewer-answer capture artifacts;
- shared consumer helper extraction that could weaken per-script safety review;
- scanner-output importer/exporter boundaries;
- real evidence locator and redaction gate;
- automated recon-to-runner coupling beyond explicit dry-run/direct-read;
- report drafting/submission adapters;
- scheduler/CI target-touching automation;
- real bug-bounty program activation.

## Pitfall

If the user asks “did we handle the small process problems, technical debt, and dead ideas?”, do not treat it as a request for another high-level phase roadmap. They are asking for a cleanup/debt/deferred inventory and whether it is safe to advance.