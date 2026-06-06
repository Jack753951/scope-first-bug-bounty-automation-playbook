> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Codex Task — P2-14 preview_manifest/1.0 schema + validator

Implement only the safe offline contract work approved by `handoff/claude_p2_14_direction_review.json`.

Read first:
- `.hermes.md`
- `handoff/review_tiering_policy.md`
- `handoff/oss_recon_gate.md`
- `handoff/claude_p2_14_direction_review.json`
- P2-13 implementation context in `scripts/module_runner.py`, `scripts/test_module_runner.py`, and `handoff/codex_review.md` latest section.

Scope:
- Add a versioned `preview_manifest/1.0` contract and stdlib-only read-only validator for already-persisted preview bundles.
- Keep this phase offline-only and data-only.
- No module execution, no scanner/network/subprocess/process launch, no dynamic import/eval/exec, no callbacks, no target touching, no findings/evidence/report emission, no `config/scope.txt` changes.

Expected files / paths:
- Prefer existing project layout conventions. If unclear, use:
  - `modules/_schema/preview_manifest.schema.json`
  - `scripts/validate_preview_manifest.py`
  - `scripts/test_preview_manifest.py`
  - update `scripts/README.md` with concise safe-use docs
- If you choose different paths, justify in `handoff/codex_review.md`.

Contract requirements:
- `schema_version` exact const: `preview_manifest/1.0`
- closed objects (`additionalProperties: false` where applicable)
- stable producer block for module_runner
- `run_id` using the same safe run-id posture as P2-13
- preview mode flags prove persisted dry-run preview only:
  - `persist_preview_bundle == true`
  - `include_module_io_preview == true`
  - `dry_run == true`
- fixed artifact allowlist only:
  - `run.json`
  - `module_inputs.json`
  - `module_results.json`
  - `bundle_consistency.json`
- artifact fields include relative path, sha256, size_bytes, content_type
- preview_manifest.json itself must NOT be listed as an artifact

Semantic validator requirements:
- stdlib only
- read-only: never create/write/delete/move/repair files
- reject duplicate JSON keys, malformed JSON, trailing data where practical
- reject unknown fields per schema-equivalent checks, even without jsonschema dependency
- reject unsafe run_id/path traversal/absolute paths/backslashes/drive prefixes/raw `//` or `/./` variants where applicable
- reject symlinks in the unresolved parent chain and artifact paths
- require artifact set equals exact allowlist, no extras/missing
- recompute sha256 and size for each artifact
- verify bundle_consistency artifact has status/verdict equivalent allow/ok as supported by the existing bundle validator output; do not invent live semantics
- errors must be structured and redaction-safe
- provide a CLI that emits machine-readable JSON and exits nonzero on denial/invalid manifest

Tests:
- TDD-style focused tests for valid fixture, missing required fields, unknown fields, bad schema_version, unsafe run_id, missing/extra artifact, listing preview_manifest itself, unsafe relative paths, symlink denial where OS supports it, hash mismatch, size mismatch, malformed/duplicate-key JSON, CLI success/failure JSON shape, and static no-network/no-subprocess imports.
- Run focused tests and as much of the relevant scripts suite as practical.

Handoff updates:
- Update `handoff/codex_review.md` with summary, files changed, tests, safety boundary, and validation results.
- Append to `handoff/accepted_changes.md`; do not truncate existing history.
- Preserve the unverified CVE quarantine file if present.

Validation commands to run if possible:
- `python -m py_compile scripts/validate_preview_manifest.py scripts/test_preview_manifest.py`
- focused test command for preview manifest tests
- full or relevant scripts tests
- `USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review`
