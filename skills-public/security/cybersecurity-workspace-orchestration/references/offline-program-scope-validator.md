> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Offline Program Scope Validator Pattern

Use this reference when building or reviewing an offline validator for `programs/<slug>/scope.json` before wiring program scope into recon/runtime automation.

## Purpose

The validator is a necessary-but-not-sufficient precondition for future target-touching work. It validates program policy files offline, returns a structured allow/deny verdict, and gives later runtime gates a stable contract to consume. It must not run scans, call external tools, or treat validation success as authorization by itself.

## Recommended CLI Contract

```bash
python scripts/validate_program_scope.py programs/_examples/public-bounty.example.json
python scripts/validate_program_scope.py --json programs/_examples/public-bounty.example.json
python scripts/validate_program_scope.py --ignore-time programs/_examples/public-bounty.example.json
python -m unittest scripts/test_validate_program_scope.py
```

Expected output fields:

```json
{
  "path": "programs/example/scope.json",
  "program_slug": "example",
  "verdict": "allow",
  "errors": [],
  "warnings": []
}
```

Default-deny rule: any load, parse, schema-version, slug/path, expiration, testing-window, technique, scope-entry, IDN, or rate-limit error returns `verdict: deny` and a non-zero exit code.

`--ignore-time` may skip only the current-time active/expired check for examples/tests. It must still parse timestamps and enforce ordering such as `valid_until > valid_from`.

## Semantic Checks To Implement

Beyond raw JSON parsing or JSON Schema inspection, validate:

- required top-level blocks and closed top-level keys;
- exact `schema_version` match;
- `program.slug` syntax and `programs/<slug>/scope.json` path match, while not requiring this for `_examples/*.example.json`;
- `expiration.valid_until > expiration.valid_from` and current-time validity unless `--ignore-time` is set;
- `testing_windows.always=true` only for `lab`, `ctf`, or `self-hosted`;
- `always=false` requires timezone and at least one allowed window;
- testing windows require `start < end`; reject overnight windows unless the policy explicitly splits them;
- `techniques.allowed` and `techniques.forbidden` are disjoint;
- non-authorizable techniques are rejected from `allowed` (`dos`, `credential_brute_force`, `social_engineering`, `physical`, `malware`, `callback_payloads`);
- raw Unicode/IDN scope values are rejected unless a future normalization design is explicitly approved;
- punycode hostnames such as `xn--...` are handled consistently with `idn_handling`;
- `rate_limits` values are positive integers and booleans do not pass as integers;
- URL prefix entries reject userinfo, query strings, fragments, missing hosts, and missing path prefixes.

## Fixture Pattern

Keep safe positive examples under `programs/_examples/` and deliberately-invalid fixtures under `programs/_examples/invalid/`. Invalid fixtures should demonstrate default-deny behavior for cases such as:

- expired program;
- allowed/forbidden technique overlap;
- non-authorizable technique in `allowed`;
- raw Unicode IDN;
- overnight testing window.

Use only RFC 2606 example domains and RFC 5737 documentation IP ranges. Never include real program data, credentials, tokens, or authorization artifacts in fixtures.

## Review Pattern

After Codex implements or changes the validator:

1. Hermes runs the safe examples, invalid fixtures, unit tests, Python compile, and local review wrapper.
2. Claude/Cowork independently reviews source and runs offline-only probes.
3. Handoff records must state no live scans were run and no runtime files (`recon.sh`, `config/scope.txt`, `config/recon.conf`) were modified unless that was the explicit phase.
4. P1-3/runtime integration must treat `validate_file(...).verdict == "allow"` as necessary but not sufficient: still require global scope intersection, per-target allow/deny, stage technique gates, automation flag enforcement, effective rate/window checks, blackout handling, and audit-event emission.

## Common Non-Blocking Follow-Ups

- Document or constrain `file:` policy URLs if accepted for local archived authorization references.
- Keep IPv4-only behavior explicit; add `ip_v6`/`cidr_v6` entry types in a future schema if needed rather than silently widening IPv4 fields.
- Decide how to handle the same value appearing in both `in_scope` and `out_of_scope`; runtime should make `out_of_scope` win and audit the reason.
- On platforms where timezone databases are unavailable, shape validation can be offline-only, but runtime window evaluation should fail closed if a timezone cannot be resolved.
