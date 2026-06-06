> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# preview_manifest/1.0 fixtures

These fixtures are reusable, offline-only examples for consumers of the `preview_manifest/1.0` contract.

- `valid_minimal/` contains a committed golden dry-run preview bundle with the fixed P2-14 artifact set:
  - `run.json`
  - `module_inputs.json`
  - `module_results.json`
  - `bundle_consistency.json`
  - `preview_manifest.json`

The fixture is data-only. It is not a scan result, does not authorize module execution, and must not be used as target-touching input.
