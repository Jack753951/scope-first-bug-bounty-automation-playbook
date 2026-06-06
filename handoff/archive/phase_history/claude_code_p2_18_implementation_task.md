> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code Implementation Task — P2.18 CTF Verifier Metadata Trial Consumers

Date: 2026-05-18
Worker route: Claude Code MAX/OAuth implementation
Verifier: Hermes
Fallback: Codex/GPT surgical fix only if needed
Tier: T3
Boundary: offline/local only; no runtime wiring

## Read First

- `handoff/cowork_p2_18_direction_review.md`
- `handoff/model_usage_routing_policy.md`
- `templates/ctf_verifier_metadata.yaml`
- `scripts/ctf_review_decision.py`
- `scripts/ctf_prepare_challenge.py`

## Goal

Implement the accepted P2.18 offline/local trial for CTF verifier metadata descriptors.

This is a trial before schema promotion. Do not create JSON Schema, registry entries, runner wiring, CI hooks, or runtime consumers.

## Required Deliverables

1. Add fixture descriptors:

```text
tests/fixtures/ctf_verifier_metadata/source_transform_inversion.yaml
tests/fixtures/ctf_verifier_metadata/parser_validation_checksum.yaml
```

Recommended optional third fixture if helpful:

```text
tests/fixtures/ctf_verifier_metadata/oracle_replay_kali.yaml
```

2. Add standalone read-only linter:

```text
scripts/lint_ctf_verifier_metadata.py
```

Constraints:

- standard library only
- no PyYAML dependency unless already present; prefer a minimal flat YAML parser
- no network, no subprocess, no sockets, no scanner/module imports
- deterministic JSON output
- reads one or more `--input` paths
- exit 0 only if all inputs pass
- output shape per file: `{file, status, errors[], warnings[]}` or equivalent deterministic JSON
- header comment: TRIAL ONLY, non-binding, no runtime consumers, schema promotion deferred to P2.19+

3. Add focused tests:

```text
scripts/test_ctf_verifier_metadata.py
```

Must cover the acceptance tests from `handoff/cowork_p2_18_direction_review.md`, especially:

- two valid fixture descriptors pass
- optional active-service/oracle Kali descriptor accepted only with `kali_required: true`
- `destructive: true` denied
- active-service without `kali_required: true` denied
- active-service with command/host execution field denied
- unknown second-review trigger denied
- unknown top-level field denied
- boolean strings denied
- invalid mode/category denied
- forbidden fields denied
- deterministic output
- missing required keys denied
- YAML unsafe/object syntax rejected or unsupported
- no `modules/_schema/ctf_verifier_metadata*` created

4. Update template:

```text
templates/ctf_verifier_metadata.yaml
```

Add explicit `kali_required: false` and comments explaining it must be true for active-service/external/oracle descriptors. Keep template NON-BINDING, UNVERSIONED. No `$schema`, no `schema_hint`.

5. Update docs:

```text
scripts/README.md
```

Add entry for the linter and its trial-only status.

## Forbidden Changes

- No live scans, HTTP, sockets, callbacks, exploit attempts, fuzzing, brute force, OAST, or target-touching behavior.
- No imports from `scripts/module_runner.py`, `scripts/validate_module_io_bundle.py`, `scripts/validate_module_io_contract.py`, `scripts/program_policy_boundary.py`, `recon.sh`, or scanner/module runtime paths.
- No JSON Schema under `modules/_schema/`.
- No registry entry, runner wiring, recon wiring, CI/hook/scheduler/pre-commit wiring, `bin/hermes` integration, or `.github/` workflow changes.
- No promotion of fields to finding/evidence/run contracts.
- No changes to `config/scope.txt`, `loot/`, `.env`, credentials, tokens, OAuth, scheduler, deployment, billing, or production settings.
- No use of ANTHROPIC_API_KEY. Use Claude Code MAX/OAuth only.

## Validation to Run

Run and report:

```bash
python -m py_compile scripts/lint_ctf_verifier_metadata.py scripts/test_ctf_verifier_metadata.py
python scripts/test_ctf_verifier_metadata.py
python -m unittest discover -s scripts -p 'test_*.py'
```

If tests fail, fix them within the same boundary. If the task appears to require target interaction, schema promotion, secrets, or runtime wiring, stop and write a blocking note instead.

## Output

Update `handoff/accepted_changes.md` with concrete worker route and validation results, or leave a clear note for Hermes if you do not update it.
