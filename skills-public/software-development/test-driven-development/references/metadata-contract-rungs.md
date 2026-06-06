> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Metadata / Version Contract Rungs

Use this reference when a project is modularizing engines, renderers, providers, or other pluggable components and future reviewers need to know exactly which contract produced an artifact.

## TDD pattern

1. Add RED tests before changing implementation:
   - helper attaches a single-source contract version to returned objects;
   - helper does not mutate the caller's original dict/object;
   - strict validator requires the version when metadata is required;
   - fixture validator fails closed when the fixture version drifts from the constant;
   - output metadata preserves the version for downstream QA/review.
2. Verify the RED failures are about missing contract behavior, not syntax/import errors.
3. Implement the smallest GREEN change:
   - define one constant near the contract helper, e.g. `SCRIPT_CONTRACT_VERSION`;
   - have the attach/enrichment helper write the constant;
   - require/passthrough the field only in paths that explicitly need engine metadata, preserving legacy/backward-compatible callers where appropriate.
4. Update active fixtures to include the version; avoid broad rewrites of unrelated fixture structure.
5. Run focused tests, compile checks, project validate command, and diff whitespace checks.
6. If a CLI worker timed out or hit max-turns after partial implementation, inspect the actual workspace, compare against the RED tests/spec, patch narrow omissions, then rerun validation instead of restarting the entire task.
7. Record accepted contract changes, validation, worker status, and any non-blocking reviewer notes in repo handoff files.

## Review points

- Contract version has one source of truth.
- Fixture validators compare equality to the constant, not just truthiness.
- General validators may allow backward-compatible truthiness only when a stricter fixture/path validator exists.
- Output artifact metadata includes the contract version so later visual QA, canary packets, and reviewer handoffs can trace provenance.
- No publish/upload/scheduler/OAuth/default-privacy gates are touched as part of a metadata-contract rung unless explicitly approved.
