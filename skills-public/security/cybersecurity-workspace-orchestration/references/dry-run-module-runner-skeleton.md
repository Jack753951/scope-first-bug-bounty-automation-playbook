> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Dry-run-only Module Runner Skeleton

Use this reference when introducing the first module runner into an authorized cybersecurity platform before any real module execution exists.

## Purpose

The first runner should be an offline planner, not an executor. Its job is to prove contracts and safety boundaries: load module manifests, consume a pre-existing allow policy artifact, and emit a planned run manifest preview. It must not run modules, launch tools, make network requests, generate findings, or touch targets.

## Minimal contract

A safe first skeleton should:

- Require explicit `--dry-run` / dry-run execution state.
- Load and semantically validate `module_manifest/1.0` through the existing manifest validator.
- Load and semantically validate an existing `policy_boundary/1.0` allow artifact.
- Bind the planned `run/1.0` preview to:
  - `run_id`
  - target type and target value
  - requested execution mode
  - program/global scope hashes
  - policy artifact path and hash
  - module manifest path and hash
  - dry-run execution state
  - triage-only review state
- Write or print only deterministic offline planning artifacts.

## Fail-closed policy artifact checks

Do not accept a policy artifact only because it contains `allow`. Re-check at runner consumption time:

- Artifact path is canonical and contained under `runs/<run_id>/policy/<file>`.
- Artifact hash matches the artifact being consumed.
- Boundary schema/version/status are expected.
- Request identity matches runner invocation: `target`, `target_type`, `mode`, stage/technique where applicable.
- Embedded decision fields match boundary/request fields.
- Program/global scope hashes match current source files if the runner is expected to bind current policy state.
- `boundary.errors`, `contract_errors`, `boundary_errors`, and `deny_reason_codes` are empty.
- Helper metadata exists, is well formed, did not time out, and returned zero.
- `decision.errors` and `decision.deny_reason_codes` are empty.

If any check is missing, malformed, contradictory, or ambiguous, deny planning.

## Dry-run module safety checks

For the initial skeleton, allow only modules that are offline and non-target-touching:

- `supports_dry_run` or equivalent must be true.
- `target_touching` must be false.
- `requires_network` must be false.
- `network_access` must be `none`.
- Requested target type must be in the module's supported target types.
- Duplicate module IDs in one plan must fail closed.
- Unknown schema, unsupported technique, or validator failure must fail closed.

This is stricter than a future live runner on purpose. Do not weaken it until the project has explicit execution gates, rate limits, audit logging, evidence handling, and approval workflows.

## TDD / review pattern

Add tests before implementation for:

- Happy-path dry-run planning with one safe offline module.
- Deny / malformed / contradictory policy artifacts.
- Policy target, target type, and mode mismatches.
- Artifact path escape or artifact stored outside `runs/<run_id>/policy/`.
- Non-empty boundary/helper/decision error and deny-code fields.
- Missing or malformed helper object.
- Invalid module manifest and duplicate module ID.
- Module declares target-touching or network access during dry-run.

After Codex implementation, route to independent Cowork/Claude review specifically asking for policy-artifact binding, dry-run non-execution guarantees, fail-closed behavior, and architecture fit. Expect review to catch subtle allow-artifact contradictions; patch blockers before reporting completion.

## Static non-execution sanity checks

In addition to tests, scan the runner source for accidental executor primitives such as subprocess/process launch, socket/network libraries, request clients, dynamic `eval`/`exec`, or plugin imports that could execute untrusted module code. Avoid dynamic import loaders for module content in the first skeleton; read manifests as data.

## Handoff / GitHub notes

For non-trivial runner skeleton work, update handoff artifacts with:

- Offline/live-safety boundary.
- Exact validation commands and results.
- Independent-review verdict and blocker resolution summary.
- PR title/body reflecting the expanded scope.
- Follow-up issue for the first safe Level 1 audit fixture rather than enabling execution immediately.
