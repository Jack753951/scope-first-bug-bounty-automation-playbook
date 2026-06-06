> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P2-1 Independent Review — Finding/Evidence Schemas

Date: 2026-05-16
Issue: https://github.com/Jack753951/cybersec-lab/issues/5
PR: https://github.com/Jack753951/cybersec-lab/pull/1

## Scope reviewed

P2-1 adds a contract layer for future policy-gated modules:

- `modules/_schema/finding.schema.json`
- `modules/_schema/evidence.schema.json`
- `modules/_schema/README.md`
- `scripts/validate_finding_evidence.py`
- `scripts/test_finding_evidence_schema.py`

The implementation is offline/schema/validator work only. It does not run scans, touch external targets, modify `config/scope.txt`, or publish reports.

## Open-source references considered

Before implementation, GitHub/open-source references were checked for reusable ideas:

- Bug bounty scope repositories/tools were mostly scope-data collection/validation and not suitable to copy into this policy-gated architecture.
- ProjectDiscovery Nuclei template metadata influenced future module-manifest concepts (`id`, severity, tags, metadata, classification/CWE/CVSS/reference style fields).
- OSV/SARIF/DefectDojo concepts informed conservative finding fields such as severity/confidence, references, evidence, and verification state.

Decision: implement a project-specific conservative schema/validator rather than copy an external format, because this workspace requires authorization gates, triage-only semantics, and repository-safe redacted evidence handling.

## Review timeline

### Review 1 — BLOCKED

Blocking findings:

1. `storage.path` allowed traversal such as `runs/x/../../config/scope.txt`.
2. `triage.scanner_output_only` was boolean but not forced to `true`.
3. `metadata` was unconstrained and could carry raw secrets/unredacted data.

Fixes applied:

- `storage.path` is validated with `PurePosixPath` and must be a local POSIX relative path under `runs/<run_id>/evidence/`; traversal, backslashes, absolute paths, URL-like paths, non-evidence layouts, and run-id mismatches are denied.
- `triage.scanner_output_only` must be `true` in both schema and validator.
- Metadata is constrained and covered by regression tests.

### Review 2 — BLOCKED

Remaining blocker:

- Sensitive metadata values could still be stored under innocuous keys, for example `metadata.notes = "Authorization: Bearer ..."`.
- JSON Schema and Python validator diverged for nested metadata sensitivity.

Fixes applied:

- Metadata is now flat only: no nested objects or lists.
- Metadata values must be repository-safe scalar values and strings are bounded to 500 chars.
- Sensitive-looking keys and values are denied.

### Review 3 — BLOCKED

Remaining blocker:

- JSON Schema regexes were case-sensitive while the Python validator was case-insensitive. A consumer using only schema validation could allow `Authorization`, `HEADER`, lowercase `authorization:`, or lowercase `bearer` variants.

Fixes applied:

- Added optional `jsonschema` regression coverage for case-variant sensitive metadata.
- Updated `evidence.schema.json` regexes to use ECMA-compatible explicit case-character patterns.

### Final review — PASS

Final independent verdict: PASS.

The reviewer confirmed:

- Original blockers are resolved.
- Schema and validator reject case-variant sensitive metadata keys/values consistently.
- Evidence storage remains constrained to redacted local artifacts under `runs/<run_id>/evidence/`.
- README storage-path drift was fixed.
- No live scans or `config/scope.txt` changes were observed.

## Validation

Latest validation passed:

- `python -m py_compile scripts/validate_finding_evidence.py scripts/test_finding_evidence_schema.py`
- JSON parse for `modules/_schema/*.json`
- `env -u PYTHONIOENCODING -u PYTHONUTF8 python -m pytest scripts/test_validate_program_scope.py scripts/test_program_policy_check.py scripts/test_program_policy_boundary.py scripts/test_recon_program_cli.py scripts/test_finding_evidence_schema.py -q`
  - `65 passed, 2 skipped, 51 subtests passed`
- `USER=${USER:-Owner} HACKLAB="$PWD" ./bin/hermes review`
- `git diff --check`
- static added-line safety scan

## Safety boundary

- No live scans were run.
- No external targets were touched.
- No `config/scope.txt` changes.
- No credentials, loot, reports, scheduler, deployment, billing, or production settings changed.
- Automated findings remain candidate/needs-verification only; confirmed findings still require manual/agent verification.

## Non-blocking follow-up

- P2-2 should add a run manifest / execution ledger so findings/evidence can point to a run envelope and policy decision artifact.
- P2-3 should add `module.schema.json` and module manifest validation using the same technique/mode vocabulary as program policy.
- P2-4 should introduce a dry-run-only module runner skeleton that consumes these contracts without target-touching behavior by default.
