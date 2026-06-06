> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Security live-target gate hardening via TDD

Use this reference when a cybersecurity lab workflow moves from local proof bundles toward authorized live-target or bug-bounty dry-runs. The goal is to prove safety gates before any scanner-like automation, not to authorize live testing.

## Trigger

Apply after any of these events:

- A new program/scope artifact is introduced, e.g. `programs/<slug>/scope.json`.
- A dry-run gate rejects an intended in-scope authorized target for compatibility reasons.
- A global scope file contains local-lab entries such as `localhost` alongside live authorized domains.
- The user asks whether new proof/bundle/live-surface work will be archived or consolidated.
- A first live-target manual session discovers workflow/gate gaps before automation.

## RED tests to add first

Write focused shell/CLI regressions before changing production scripts:

1. In-scope program dry-run passes for the exact authorized URL.
2. Out-of-scope public target fails closed.
3. Local-lab tokens such as `localhost` do not poison unrelated global scope validation.
4. Malformed or non-lowercase program slugs fail before target processing.
5. Path-like slugs (`../x`, slash/backslash, dot-prefix, dash-prefix, whitespace/control chars) fail closed.
6. `--skip-scope-check` cannot combine with program policy mode.
7. `--policy-mode dry-run` requires `--dry-run`.
8. `--policy-mode` without `--program` is rejected.

Prefer tests that assert both exit status and diagnostic text, plus a negative assertion that no target processing or dry-run plan leaked after a guard failure.

## Minimal GREEN fixes

Only patch the narrow compatibility issue exposed by the failing tests. Examples:

- Allow lowercase underscores in program slugs only if the repository's program directories already use them.
- Treat `localhost` as an explicit local-lab scope/target type, not as a malformed domain.
- Keep path-like, uppercase, reserved, or traversal-like values rejected.

A dry-run pass is only readiness evidence. It is not permission for live scanner-like automation.

## Post-proof consolidation step

After GREEN, run the project’s post-proof/post-bundle checklist if present, or create a lightweight one that prints required updates without changing live state. It should remind the agent to update:

- append-only accepted changes
- current navigation / active strategy queue
- project note / Obsidian entrypoint
- proof-library index or live-bounty bridge
- focused regression tests and validation commands

The checklist must not auto-promote `surface_only`, `candidate`, or `needs_second_account` observations to `verified` or `report_ready`.

## Validation

Run focused tests, shell syntax checks, whitespace checks, and the project review command. In the final response, separate:

- Benefit
- Changes
- Validation
- Next safe action

Explicitly state that dry-run gate readiness does not authorize scanning, fuzzing, exploitation, cross-account testing, callbacks, scope expansion, or report submission without a separate operator-approved plan.
