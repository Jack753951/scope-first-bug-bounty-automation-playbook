> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Program Scope Schema / Intake Pattern

Use this reference when implementing Phase-1-style program/client/bug-bounty scope intake for an authorized cybersecurity lab.

## Goals

Create a versioned, default-deny data contract under `programs/<slug>/scope.json` that narrows global `config/scope.txt` and can later be reused by module manifests, finding schemas, and post-scan agent review.

## Recommended Layout

```text
programs/
  _schema/
    scope.schema.json
    README.md
  _examples/
    public-bounty.example.json
    client-engagement.example.json
    ctf-platform.example.json
  <program-slug>/
    scope.json
    README.md
    authorization.txt
```

Examples must use safe placeholder domains/IPs only, such as RFC 2606 example domains and RFC 5737 documentation IPv4 ranges.

## Required Top-Level Fields

```text
schema_version
program
scope
techniques
rate_limits
testing_windows
expiration
```

Recommended contract properties:

- Draft 2020-12 JSON Schema.
- `schema_version` pinned exactly (for example `"1.0"`).
- `additionalProperties:false` on all objects.
- Closed enums for platforms, scope entry types, IDN handling, techniques, day names.
- Required authorization reference and policy/version timestamps.
- Explicit expiration window.

## Scope Semantics

- Runtime permission is intersection, not union: both global `config/scope.txt` and active program scope must allow a target.
- Program `out_of_scope` always wins over `in_scope`.
- Wildcard entries should be explicit about apex behavior; for this workspace, preserve the documented current behavior unless changed by operator: `*.example.com` includes `example.com` itself unless an `include_apex:false` policy is intentionally introduced.
- Prefer `punycode_only` or `reject_idn`; do not accept raw IDN unless a future phase explicitly designs normalization.
- URL prefix entries should not silently allow the whole host; the host must also be in scope and the path prefix must match.

## Techniques

Non-authorizable or abuse-oriented tags should not be allowed in `techniques.allowed`:

```text
dos
credential_brute_force
social_engineering
physical
malware
callback_payloads
```

Use technique tags that future module manifests can reuse, for example:

```text
subdomain_enumeration
http_probe
port_scan
service_fingerprint
directory_bruteforce
vulnerability_scan_passive
vulnerability_scan_active
intrusive_fuzz
```

## Loader Checks That JSON Schema Cannot Fully Enforce

When implementing the loader (for example P1-2), add explicit default-deny checks for:

- `valid_until > valid_from`.
- `testing_window.end > start` or explicit overnight-window handling.
- `techniques.allowed` and `techniques.forbidden` are disjoint.
- slug matches `programs/<slug>/scope.json` and CLI/env selection.
- program is not expired and not before `valid_from`.
- current time falls within testing windows and outside blackouts.
- `automation_permitted:false` blocks non-dry-run automation.
- per-tool rate caps tighten, never loosen, base config.
- punycode TLDs and labels are accepted or rejected consistently with `idn_handling`.
- IPv6 posture is explicit: unsupported with default-deny, or supported through separate `ip_v6`/`cidr_v6` entry types.

## Validation Pattern

- Parse every JSON file under `programs/` with the stock runtime JSON parser.
- Validate examples against the schema when `jsonschema`, `ajv`, or similar is available.
- Run the project local review wrapper.
- Do not modify runtime scanners during schema-only scaffolding.
- Run independent Claude/Cowork review before accepting schema changes that affect future authorization behavior.
