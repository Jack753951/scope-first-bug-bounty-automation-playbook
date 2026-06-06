> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Run Manifest / Execution Ledger Contract

Use this reference when adding or reviewing a P2-style run manifest for a policy-gated cybersecurity automation platform.

## Purpose

A run manifest is the offline execution ledger that binds a module run envelope to authorization provenance and repository-safe output artifacts. It should make later agent/human review able to answer:

- what run produced this candidate finding/evidence;
- which target and program scope it was authorized under;
- which policy decision artifact/hash allowed it;
- which modules ran;
- where redacted findings/evidence metadata live;
- whether output is still triage-only and needs manual verification.

## Minimal Contract

A versioned `run/1.0` manifest should bind:

- `run_id`
- created/completed UTC timestamps
- run status
- program slug
- active program scope file SHA-256
- active global scope file SHA-256
- target `{type,value}`
- policy mode, decision, decision artifact path, decision SHA-256, checked timestamp
- execution runner/profile, `dry_run`, `target_touching`
- modules with stable `module_id`, manifest hash, status
- artifact references for findings and evidence
- review state with `scanner_output_only=true` and `manual_verification_required=true`

## Safety Rules

- Offline schema/validator work only until an explicit module runner phase exists.
- Policy decision must be `allow` before representing an execution as permitted.
- `policy.mode=dry-run` or `execution.dry_run=true` must imply `target_touching=false`.
- Artifact paths must be local POSIX relative paths under the matching run directory:
  - `runs/<run_id>/policy/`
  - `runs/<run_id>/findings/`
  - `runs/<run_id>/evidence/`
- Reject traversal, absolute paths, URL-like paths, Windows backslashes, wrong run IDs, and unrelated directories such as `loot/`.
- Evidence artifacts must remain redacted and canonical SHA-256 hashed.
- Do not let run/finding/evidence artifacts imply confirmed vulnerabilities; keep them candidate/triage-only until review, evidence, impact, remediation, and retest are complete.

## Semantic Validator Checks

JSON Schema is useful but insufficient for ledger-grade safety. Add a standard-library semantic validator that default-denies ambiguity and cross-checks:

- run schema version and allowed top-level keys;
- canonical hashes and UTC timestamp shapes;
- exact policy decision and dry-run/target-touching constraints;
- path containment under the correct `runs/<run_id>/...` subdirectory;
- duplicate `modules[].module_id` values;
- duplicate `artifacts.findings[].id` and `artifacts.evidence[].id` values;
- finding `source.run_id` equals run `run_id`;
- evidence `source.run_id` equals run `run_id`;
- finding/evidence targets equal run target;
- finding `source.policy_decision_sha256` equals run policy decision hash;
- finding/evidence module IDs are declared in `run.modules`;
- finding/evidence artifact IDs are declared in the run manifest;
- evidence redaction and hashes match artifact declarations.

## Critical Pitfall: Do Not Validate Only the First Finding

When validating a run bundle, it is tempting to call an existing finding/evidence bundle validator once with `findings[0]`. That leaves later findings able to reference missing evidence, mismatched hashes, wrong kinds, or wrong `finding_id` values.

Required pattern:

1. Validate each finding document independently.
2. For each finding, run the finding/evidence cross-document validator against the full evidence set.
3. Validate each evidence document independently.
4. Cross-check every finding/evidence item against the run manifest declarations.

Regression tests should include at least:

- two findings where the second references missing evidence;
- duplicate module IDs;
- duplicate finding artifact IDs;
- duplicate evidence artifact IDs;
- wrong run ID or path containment for a policy/finding/evidence artifact.

## Open-Format Comparison

Before implementing, briefly inspect established formats:

- SARIF: useful for run-level envelopes and tool/result separation.
- Nuclei templates: useful for stable module IDs, metadata, and template execution concepts.
- Project-specific finding/evidence contracts: usually the binding layer for local authorization and redaction rules.

Prefer a project-specific contract when authorization provenance, default-deny policy gates, local redacted evidence, and triage-only review state are first-class requirements.

## Validation Checklist

- [ ] RED tests fail before implementation for missing schema/validator.
- [ ] Negative tests cover traversal/absolute/URL/backslash/wrong-run paths.
- [ ] Negative tests cover dry-run target-touching mismatch.
- [ ] Negative tests cover duplicate IDs.
- [ ] Negative tests cover multi-finding bundle validation, especially a bad second finding.
- [ ] Python compile passes.
- [ ] JSON schemas parse.
- [ ] Relevant pytest suite passes.
- [ ] Project review/preflight wrapper passes.
- [ ] Independent review returns PASS after any blocker fixes.
- [ ] PR/handoff notes state offline/live-safety boundary and next phase.
