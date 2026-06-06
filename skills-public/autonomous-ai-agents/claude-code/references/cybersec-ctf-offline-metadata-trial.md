> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec CTF offline workflow trial pattern

Use this reference when a Hermes-controlled cybersecurity workspace turns CTF lessons into offline/local workflow artifacts before promoting any schema, registry, runner, or target-touching behavior.

## Pattern that worked

1. Treat CTF results as workflow-calibration data, not as confirmed findings.
2. Keep the first slice offline/local and fixture-driven:
   - artifact preparation helper
   - review-decision helper
   - non-binding metadata template
   - committed fixtures and expected-output pairs
3. Route direction review and implementation to Claude Code Pro/OAuth when the user has Claude Max/Pro capacity and wants to preserve `ANTHROPIC_API_KEY`.
4. Keep Hermes as verifier and acceptance gate; use Codex/GPT only for surgical fallback.
5. Defer schema/registry/runtime promotion until at least two realistic trial descriptors consume the vocabulary.

## P2.17-style skeleton

Useful first deliverables:

- `scripts/ctf_prepare_challenge.py` — offline artifact preparation / classification helper.
- `scripts/ctf_review_decision.py` — classifies candidate evidence into statuses such as candidate/verified/needs-second-review without promoting to report/finding contracts.
- `templates/ctf_verifier_metadata.yaml` — explicitly non-binding, unversioned, trial-only template.
- `tests/fixtures/...` — deterministic inputs plus pinned expected JSON outputs.

Acceptance checks:

- `python -m py_compile` on new scripts/tests.
- Focused tests for each helper.
- Full `python -m unittest discover -s scripts -p 'test_*.py'`.
- Static check that implementation scripts do not import or invoke network/socket/scanner/subprocess paths.
- `git diff --check` and repo-local review command.

## P2.18-style metadata trial

Before schema promotion, add trial consumers under `tests/fixtures/`, not runtime or template dirs:

- `tests/fixtures/ctf_verifier_metadata/source_transform_inversion.yaml`
- `tests/fixtures/ctf_verifier_metadata/parser_validation_checksum.yaml`
- optional `oracle_replay_kali.yaml` to prove active-service/oracle descriptors require Kali but remain non-executable from the host.

A small linter can be worthwhile, but it must stay weaker than a schema:

- standard-library only if possible
- read-only, deterministic JSON output
- no network, sockets, subprocess, scanner/module imports, or runtime writes
- no registry, runner, recon, CI, hook, scheduler, or `bin/hermes` wiring
- deny unknown top-level fields during the trial so vocabulary drift is visible
- deny target/scope/execution/callback/payload/finding-promotion/credential fields
- enforce real booleans, not quoted boolean strings
- require `kali_required: true` whenever `mode: active-service`, `uses_external_service: true`, or `oracle_required: true`
- keep `modules/_schema/` untouched until a separate P2.19+ review

Recommended linter test cases:

- valid offline fixtures pass
- optional active-service/oracle Kali fixture passes only with `kali_required: true`
- `destructive: true` denied
- active-service without `kali_required: true` denied
- active-service with `command`, `cmd`, `exec`, or callback fields denied
- unknown second-review trigger denied
- unknown top-level fields denied
- string booleans denied
- invalid mode/category denied
- each forbidden field denied
- deterministic output across repeated and multi-file runs
- missing required keys denied
- unsafe YAML/object/anchor syntax rejected or unsupported
- no `modules/_schema/*ctf*` files are created

## OSS Recon Gate notes

Use OSS only for design comparison, not unsafe defaults:

- Adapt Nuclei-style flat metadata/tag shapes, but do not adopt severity/CVSS for verifier descriptors.
- Adapt SARIF's separation of status/kind/level as a reminder to keep finding severity separate from verifier metadata.
- Adapt Semgrep confidence ideas only as advisory descriptor metadata; runtime confidence should remain in the review-decision helper.
- Ignore DefectDojo finding-state vocabulary for verifier descriptors; it belongs to findings, not verifiers.
- Ignore ZAP add-on manifest coupling for this trial; it implies plugin/runtime registration too early.

## Claude Code max-turn handling

Claude Code may hit `error_max_turns` after producing most implementation files. In this pattern, do not discard the work:

1. Inspect `git status` and expected files.
2. Read the linter/test files for boundary violations.
3. Run focused tests and full discovery.
4. Add missing tests/fixtures/handoff entries locally if small and safety-sensitive.
5. Record the Claude Code run JSON path and note that Hermes completed verification.

This is especially useful when the user wants Claude Code plan capacity used for coding while preserving API-backed Claude for other projects.
