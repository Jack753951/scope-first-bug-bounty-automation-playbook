> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Level 1 Audit Module Fixtures

Use this reference when adding the first safe module fixtures after module manifests, run ledgers, and a dry-run-only runner exist.

## Purpose

A Level 1 audit fixture is committed module metadata that proves discovery/validation/planning contracts without enabling execution. It is a bridge between schema-only work and future runnable modules.

## Recommended layout

Use a repository-local module tree such as:

```text
modules/checks/<level-or-category>/<module_id>/module.json
```

Example first fixture:

```text
modules/checks/level1/policy_decision_metadata_audit/module.json
```

Keep fixture content as data only. Do not add runnable scanner code, imports, subprocess calls, network clients, callbacks, or target-touching behavior in the same phase.

## Safe first fixture posture

For the first Level 1 fixture, prefer an offline metadata/audit fixture that declares:

- `supports_dry_run=true`
- `requires_network=false`
- `network_access=none`
- `target_touching=false`
- `destructive=false`
- `intrusive=false`
- `output_contracts.emits_findings=false`
- `output_contracts.emits_evidence=false`
- safety gates require policy decision, scope match, manual verification, scanner-output-only, redacted evidence only
- safety gates forbid raw secrets, loot writes, destructive actions, and OAST callbacks

This fixture exists to validate the manifest contract and runner planning path; it should not imply a confirmed finding or any observation about the target.

## TDD pattern

1. Add RED tests that reference the committed fixture path and fail because the fixture is missing.
2. Assert the fixture validates with the existing module manifest validator.
3. Assert direct safety posture fields, not only validator verdict:
   - dry-run support
   - no network / target touching
   - no destructive or intrusive behavior
   - no findings/evidence emission
   - no raw secrets / loot / destructive / OAST gates
4. Assert the dry-run runner can plan the fixture and records:
   - module id
   - manifest SHA-256
   - `status=planned`
   - `execution.dry_run=true`
   - `execution.target_touching=false`
   - empty findings/evidence arrays
5. Keep existing tests that target-touching or network-requiring manifests default-deny.

## Documentation and review

Update module README/examples to use the chosen layout or concrete fixture path, not only a stale placeholder such as `modules/<module_id>/module.json`.

Independent review should check:

- the fixture is truly offline/dry-run-plannable;
- tests cover committed fixture validation and runner planning;
- no execution, target touching, network, findings/evidence, callbacks, or scanner behavior is introduced;
- docs match the actual layout;
- roadmap fit: next phase should be offline discovery/profile selection, not live execution.

## Validation checklist

- Fixture validator returns allow with no errors/warnings.
- Focused manifest/runner tests pass.
- Full relevant test suite passes.
- Python compile and JSON parse pass.
- Project review/preflight passes.
- `git diff --check` has no functional issues; line-ending warnings alone are non-blocking.
- Handoff/PR text records safety boundary, validation results, independent-review verdict, and next follow-up phase.
