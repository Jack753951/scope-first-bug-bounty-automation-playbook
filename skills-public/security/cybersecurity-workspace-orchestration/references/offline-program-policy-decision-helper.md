> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Offline Program Policy Decision Helper Pattern

Use this reference after a per-program scope schema/validator exists and before wiring any program policy into live recon/runtime behavior.

## Purpose

Create a standard-library, offline-only helper that answers whether a specific `target + technique + mode` is allowed under both:

1. a validated program/client scope file, and
2. the operator-controlled global allowlist such as `config/scope.txt`.

This is a policy computation layer only. It must not run scans, probes, curl, nmap, nuclei, fuzzers, modules, DNS lookups, or target-touching subprocesses.

## Recommended Files

```text
scripts/core/__init__.py
scripts/core/scope.py        # target normalization + scope matching only
scripts/core/policy.py       # default-deny decision engine
scripts/program_policy_check.py
scripts/test_program_policy_check.py
```

Keep `recon.sh`, `config/scope.txt`, and runtime scanner config unchanged until a later reviewed integration phase.

## Decision Rules

Allow only when all are true:

- the existing program-scope validator returns `allow`
- target syntax is safe and normalized
- target matches program `scope.in_scope`
- target does not match program `scope.out_of_scope`
- target also matches global scope
- technique is in program `techniques.allowed`
- technique is not in program `techniques.forbidden`
- `planned`/`live` modes are compatible with `automation_permitted`
- `planned`/`live` modes are compatible with testing windows / blackouts
- unsupported target/scope types are denied clearly

Treat validator success as necessary but not sufficient.

## Target Matching Baseline

Support enough for early phases without overbuilding:

- domain targets
- wildcard entries such as `*.example.com`
- URL targets matched against domain/wildcard/url_prefix entries
- IPv4 addresses
- IPv4 CIDR
- `url_prefix` entries
- raw Unicode IDN deny
- reviewed punycode ASCII compare
- out_of_scope precedence over in_scope

Avoid DNS resolution or network calls. Matching should be string/IP math only.

## CLI Shape

```bash
python scripts/program_policy_check.py \
  --program programs/<slug>/scope.json \
  --global-scope config/scope.txt \
  --target https://example.com/ \
  --technique http_probe \
  --mode dry-run \
  --json
```

Structured output should be treated as a versioned wire contract. Include at least:

```json
{
  "schema_version": "policy_decision/1.0",
  "verdict": "allow",
  "program_slug": "example",
  "target": "https://example.com/",
  "normalized_target": "example.com",
  "target_type": "url",
  "technique": "http_probe",
  "mode": "dry-run",
  "reasons": ["program in-scope matched", "global scope matched", "technique allowed"],
  "deny_reason_codes": [],
  "errors": [],
  "warnings": [],
  "audit_event": "PROGRAM_POLICY_ALLOW",
  "program_file_sha256": "<lowercase hex or null on read failure>",
  "global_scope_sha256": "<lowercase hex or null on read failure>",
  "decided_at_utc": "2026-05-15T12:34:56Z"
}
```

Consumers should route on `schema_version` and `deny_reason_codes`, not free-text `errors`. Unknown/unsupported schema, missing provenance, unreadable files, or ambiguous output should be deny-on-uncertainty. Use non-zero exit for deny.

## Tests To Pin Before Runtime Integration

- allow only when both program and global scope match
- deny program-only target not in global scope
- deny global-only target not in program scope
- deny when out_of_scope overlaps in_scope
- deny forbidden technique
- deny allowed technique when automation is disabled for `live`/`planned`
- dry-run behavior with automation disabled is explicitly documented and tested
- deny raw Unicode IDN
- wildcard apex/subdomain semantics
- `--json` output shape
- empty/all-comment global scope denies
- malformed global-scope line warns but does not deny if another entry parses
- CIDR target vs CIDR/global scope behavior
- URL port vs `url_prefix` strictness
- explicit IPv6 unsupported-target denial until reviewed support exists
- blackout/window denial path

## Independent Review Expectations

After Codex implements the helper, run Claude/Cowork independent review before acceptance. Ask for:

- blocker verdict (`ACCEPT` / `ROUTE BACK`)
- non-blocking improvements
- strategic architecture recommendations
- safety/scope assessment
- testing assessment
- P1-4 runtime integration advice

Common hardening requirements before runtime wiring:

- single-parse program data to avoid validator/policy double-read TOCTOU, or document the residual risk if deferred
- version the decision object, e.g. `schema_version: policy_decision/1.0`
- add stable uppercase `deny_reason_codes` rather than relying only on free text; cover unsupported mode, validator deny, reload/provenance failure, invalid target, program/global scope parse/miss, forbidden/not-allowed technique, automation disabled, blackout/window failures, and explicit IPv6 unsupported denial if IPv6 is not supported
- avoid double-flagging forbidden techniques: prefer `FORBIDDEN_TECHNIQUE` and do not also emit `TECHNIQUE_NOT_ALLOWED` for the same technique
- populate allow-path `reasons` with matched program/global scope, technique, automation, and window/dry-run conditions
- add provenance fields: `program_file_sha256`, `global_scope_sha256`, `decided_at_utc`; allow `now=` injection or equivalent for deterministic tests
- enforce a no-cache rule: runtime must re-decide per stage, never trust stale allow files; a dry-run allow must never be promoted to planned/live without rechecking in that mode
- decide CIDR fan-out policy before any module consumes CIDR allows

## Acceptance Boundary

Accept this phase only as offline policy computation. Do not claim runtime safety until a later reviewed phase wires the helper into each target-touching stage and preserves the same default-deny/global+program intersection.