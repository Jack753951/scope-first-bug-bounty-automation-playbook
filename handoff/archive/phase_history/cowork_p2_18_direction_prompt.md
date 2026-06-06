> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Direction Prompt — P2.18 CTF Verifier Metadata Trial Consumers

Date: 2026-05-18
Proposed tier: T3 design review
Worker route preference: Claude Code MAX/OAuth read-only review first; use API-backed Claude/Cowork only if explicitly justified.
Boundary: offline/local only; no runtime scanner/module wiring.

## Context

P2.17 added offline/local CTF workflow scaffolding:

- `scripts/ctf_prepare_challenge.py`
- `scripts/ctf_review_decision.py`
- `templates/ctf_verifier_metadata.yaml` as NON-BINDING, UNVERSIONED template
- deterministic input+expected-output fixtures under `tests/fixtures/ctf_review_decision/`

P2.17 intentionally deferred schema-ification, verifier registration, and integration with module runner / program policy / preview ledgers.

## Proposed P2.18 Objective

Trial the verifier metadata template with two offline-only, non-runtime sample verifier descriptors before considering any schema/registry promotion.

This is not a runtime integration. The goal is to test whether the template vocabulary is sufficient for real CTF lessons without creating platform coupling.

## Candidate Deliverables

1. Add two sample metadata files under a clearly non-runtime path, for example:

```text
tests/fixtures/ctf_verifier_metadata/source_transform_inversion.yaml
tests/fixtures/ctf_verifier_metadata/parser_validation_checksum.yaml
```

2. Add a small standard-library validator/linter, if useful:

```text
scripts/lint_ctf_verifier_metadata.py
```

The linter should be read-only, offline-only, and intentionally weaker than a schema. It should check only:

- required flat keys exist
- boolean fields are booleans
- `mode` is one of `offline|oracle|active-service|reconstruction`
- `destructive` is false for all P2.18 fixtures
- `second_review_triggers` contains only the P2.17 trigger vocabulary
- no fields imply live target execution, scanner invocation, findings/evidence/report promotion, or scope bypass

3. Add focused tests:

```text
scripts/test_ctf_verifier_metadata.py
```

Minimum cases:

- two valid sample descriptors pass
- `destructive: true` denied
- `mode: active-service` with `uses_external_service: true` is marked as requiring Kali / not host execution
- unknown second-review trigger denied
- target URL / scope override / command fields denied or ignored, depending on review decision

4. Update `scripts/README.md` and `handoff/accepted_changes.md`.

## OSS Recon Gate Questions

Compare this slice against 2-5 mature references, design-only:

- Nuclei template metadata
- SARIF result kind/level separation
- Semgrep rule metadata/confidence
- DefectDojo finding-state vocabulary
- OWASP ZAP add-on or alert metadata if useful

For each reference, state adopt/adapt/ignore and why.

## Required Review Questions

1. Should P2.18 add a linter now, or only sample descriptors?
2. Should sample descriptors live under `tests/fixtures/` rather than `templates/` or runtime dirs?
3. Should `mode: active-service` be allowed in examples if it is clearly marked as Kali-required and not host-executable?
4. Should unknown fields be denied in the linter, or should the template stay open for forward compatibility?
5. What are the exact forbidden fields for this slice?
6. What acceptance tests are mandatory before implementation?

## Forbidden Changes

- No live scans, HTTP calls, sockets, callbacks, exploit attempts, fuzzing, brute force, or target-touching automation.
- No imports from scanner/module runner runtime paths.
- No changes to `config/scope.txt`, credentials, `.env`, tokens, `loot/`, scheduler, deployment, billing, OAuth, or production settings.
- No schema promotion under `modules/_schema/`.
- No registry entry, runner wiring, recon wiring, CI/hook/scheduler wiring, or report/finding/evidence promotion.
- No use of ANTHROPIC_API_KEY-backed Claude unless explicitly justified; prefer Claude Code MAX/OAuth read-only review.

## Expected Output

Write review to:

```text
handoff/cowork_p2_18_direction_review.md
```

Return:

- Decision: ACCEPT_FOR_IMPLEMENTATION / ACCEPT_WITH_CHANGES / DEFER / BLOCK
- Tier and boundary confirmation
- OSS references considered
- Adopt/adapt/ignore decisions
- Recommended deliverables
- Required tests
- Forbidden changes
- Suggested worker route
