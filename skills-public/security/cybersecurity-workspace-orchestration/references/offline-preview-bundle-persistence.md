> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Offline Preview Bundle Persistence

Use this note when adding a persistence/audit layer for an already dry-run-only cybersecurity module runner.

## Contract

Persistence is only for data artifacts that were already produced in memory after all existing gates pass. It must not become a runner, executor, scanner, finding generator, or arbitrary output-path feature.

Recommended CLI shape:

- Add a dedicated opt-in flag such as `--persist-preview-bundle`.
- Require module I/O previews (for example `--include-module-io-preview`).
- Require an explicit repo root (`--discover-root` or `--profile-root`); do not infer from CWD for security-sensitive writes.
- Do not reuse a generic `--output` path for the bundle persistence contract, because generic output often writes deny payloads and may allow arbitrary paths.

Write only fixed filenames under repo-local `runs/<run_id>/preview/`, for example:

- `run.json`
- `module_inputs.json`
- `module_results.json`
- `bundle_consistency.json`
- `preview_manifest.json`

## Required Gates Before Any Write

All must allow before creating preview artifacts:

1. Module manifest validation.
2. Profile validation/selection.
3. Policy allow artifact validation.
4. Run manifest validation.
5. Module input/result preview contract validation.
6. Bundle consistency validation.

Deny/no-write on any validation failure.

## Path and Filesystem Safety

Fail closed on:

- unsafe `run_id` values (path separators, `..`, absolute-ish forms, too-short/malformed IDs);
- symlinked repo root;
- symlinked existing parents in the unresolved/original path chain (not just after `resolve()`), especially `runs`;
- resolved containment escape outside repo-local `runs/`;
- existing preview directory or temp directory;
- bundle validation not `allow`;
- filesystem write failures.

Important pitfall: checking only the resolved path can miss a symlink such as `repo/runs -> repo/real_runs`, because the symlink has already disappeared from the resolved chain. Check the lexical/original parent chain for `Path.is_symlink()` before resolving, then also perform resolved containment checks.

Write atomically enough for the threat model: use a temp directory under the same run directory, write fixed filenames, then rename. On exceptions, remove the temp dir and attempt to remove an empty run dir. Catch persistence exceptions at the runner boundary and return structured deny rather than allowing a CLI traceback.

## Preview Manifest

A minimal `preview_manifest/1.0` should record:

- schema/document type;
- `run_id`, created timestamp, runner name;
- `dry_run=true`, `target_touching=false`, `module_execution=false`, `network_access=false`;
- target/program/profile/policy provenance and hashes;
- module IDs and manifest hashes;
- artifact inventory: relative path, document type, sha256, byte size;
- bundle consistency verdict/path/hash;
- explicit safety boundary fields indicating no module imports, subprocesses, scanner invocation, network clients, findings, or evidence.

If the manifest does not self-hash, document that explicitly or defer self-hash to a later schema.

## Tests

Cover at least:

- happy path writes all fixed files and hashes/sizes match;
- missing module I/O preview denies and writes nothing;
- policy/target mismatch denies and writes nothing;
- unsafe run ID/path escape denies;
- existing preview directory denies;
- symlinked `runs` parent denies, skipped only if OS symlink creation is unavailable;
- simulated filesystem write failure returns deny/no-preview/no-traceback;
- CLI persistence requires explicit repo root;
- static source review or tests proving no subprocess/network/scanner/module execution primitives were added.

## OSS Design Inspirations

- SARIF: adapt run/artifact inventory and hash linkage concepts.
- DefectDojo: treat persisted preview as import candidate/triage material, not confirmed findings.
- Nuclei: keep module/template metadata separate from outputs; reject default-live target touching.
- OpenVEX/SBOM-style integrity: use hash/provenance linkage without implying vulnerability confirmation.
