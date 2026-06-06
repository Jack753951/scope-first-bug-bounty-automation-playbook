> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Program Scope Intake

`programs/` is the future home for program-specific scope and rules. P1-2 adds an offline validator for these files. It does not change `recon.sh`, does not enable scanning, and does not authorize any real target by itself.

## Layout

```text
programs/
  README.md
  _schema/
    README.md
    scope.schema.json
  _examples/
    public-bounty.example.json
    client-engagement.example.json
    ctf-platform.example.json
    invalid/
      *.example.json
  <program-slug>/
    scope.json
    authorization.txt
    README.md
```

Only `_schema/` and `_examples/` are created in P1-1. Real `programs/<program-slug>/` directories are operator-curated and must not contain secrets, tokens, client data, or private authorization text unless the operator has explicitly decided the repository is the right place for that record.

## Default-Deny Contract

Future program scope loading should deny by default. Missing files, malformed JSON, unknown schema versions, unsupported enum values, expired policy, unsupported IDN mode, empty technique allowlists, automation-disabled policy, or ambiguous scope should stop execution before any target-touching action.

Program scope is an intersection with `config/scope.txt`, not a replacement. A future run should require both:

1. The global operator whitelist in `config/scope.txt` allows the target.
2. The active `programs/<program-slug>/scope.json` allows the target, technique, window, and rate profile.

Either source can veto. Program `out_of_scope` entries should win over broader `in_scope` entries.

## Offline Validator

Use the P1-2 validator before adding or reviewing a future `programs/<program-slug>/scope.json` file:

```bash
python scripts/validate_program_scope.py programs/_examples/public-bounty.example.json
python scripts/validate_program_scope.py --json programs/_examples/public-bounty.example.json
python scripts/validate_program_scope.py --ignore-time programs/_examples/public-bounty.example.json
```

`--json` emits a machine-readable object with `program_slug`, `verdict`, `errors`, and `warnings`. Any JSON load, parse, or semantic validation error returns a non-zero exit code and a deny-like verdict. `--ignore-time` skips only the current-time validity check so examples and tests remain stable; timestamp parsing and ordering are still enforced.

The validator checks the schema-version contract, required blocks, slug/path consistency for `programs/<slug>/scope.json`, expiration ordering, conservative IDN handling, scope entry value formats, technique conflicts, non-authorizable technique placement, testing-window shape, and positive rate-limit values.

## Scope Semantics

Supported placeholder entry types are `domain`, `wildcard`, `cidr`, `ip`, and `url_prefix`. Wildcards preserve the current global default: `*.example.com` includes `example.com` unless a future parser sees `"include_apex": false`.

IDN support is intentionally conservative. Use `punycode_only` or `reject_idn`. Raw Unicode IDN authorization should be converted and reviewed outside this example contract before any future runtime support is considered.

## Operator Responsibilities

Before creating a real program file, the operator must confirm authorization, copy only safe references into the repo, and keep real credentials or sensitive client artifacts elsewhere. Scanner output remains triage only; findings require manual verification and evidence before reporting.

P1-1 examples use only RFC 5737 documentation IP ranges and RFC 2606 or example domains. They are safe examples, not live targets. See `programs/_examples/README.md` for the binding clarification that `_examples/` is never a real program slug namespace and that any `automation_permitted: true` value under `_examples/` is test-only, not live authorization.

## Future Architecture

The schema exposes concepts future modules/plugins can reuse:

- target types and scope precedence
- technique tags such as `http_probe`, `port_scan`, and `vulnerability_scan_passive`
- automation permission
- rate caps that tighten `config/recon.conf`
- testing windows and blackouts
- authorization references and expiration

Future module manifests and finding schemas should consume these same concepts instead of embedding policy in scanner scripts. Unknown modules, unknown technique tags, or missing dry-run support should default-deny.

## P1-2 Non-Runtime Boundary

This phase intentionally does not:

- modify `recon.sh`
- modify `config/scope.txt`
- modify `config/recon.conf`
- wire program scope into scan runtime decisions
- run live scans or touch external assets
- ingest real bounty, client, or CTF data

P1-3 adds an offline policy decision helper. Runtime integration with `recon.sh` remains future P1-4 work after independent review and Hermes acceptance. Until then, this directory is policy data plus offline validation and offline policy decisions only.

## P1-3 Offline Policy Decision Helper

P1-3 adds a reusable offline helper for preflight policy decisions:

```bash
python scripts/program_policy_check.py \
  --program programs/_examples/public-bounty.example.json \
  --global-scope config/scope.txt \
  --target https://example.com/ \
  --technique http_probe \
  --mode dry-run \
  --ignore-time
```

Use `--json` for structured output. The result is a versioned policy decision contract. P1-3.1 emits `schema_version: "policy_decision/1.0"` plus `verdict`, `program_slug`, `target`, `normalized_target`, `target_type`, `technique`, `mode`, `reasons`, `deny_reason_codes`, `errors`, `warnings`, `audit_event`, `program_file_sha256`, `global_scope_sha256`, and `decided_at_utc`.

Consumers must treat this object as a deny-by-default wire contract. Unknown or unsupported decision schemas, missing required fields, unknown fields, unreadable provenance files, or otherwise ambiguous output must be treated as deny-on-uncertainty. Consumers should use `deny_reason_codes` for routing and logging instead of parsing free-text `errors`.

This helper makes a policy decision only. It does not run scans, probes, `curl`, `nmap`, `nuclei`, fuzzers, modules, DNS lookups, or any target-touching behavior. It is not wired into `recon.sh` yet; P1-4 is the future runtime integration phase.

An `allow` verdict means only that offline policy preflight passed for that exact target, technique, mode, program file, global scope file, and decision time. It is not vulnerability verification, proof of exploitability, report evidence, or permission to bypass manual review. Future runtime still needs to record command provenance, respect rate limits, and keep scanner output as triage until manually verified.

Future runtime consumers must never trust cached `allow` decisions. Before any planned or live execution, runtime must recheck policy fresh against the current program file and current `config/scope.txt`. A dry-run `allow` must never be promoted to planned or live execution without rechecking in the stricter requested mode.

The decision is default-deny and requires all of the following:

- the P1-2 program scope validator returns `allow`
- the target syntax normalizes safely as ASCII/punycode-only domain, URL, IPv4, or IPv4 CIDR
- program `scope.in_scope` matches
- program `scope.out_of_scope` does not match
- global `config/scope.txt` also matches
- the technique is present in `techniques.allowed`
- the technique is not present in `techniques.forbidden`
- `planned` and `live` modes require `techniques.automation_permitted=true`
- `planned` and `live` modes must be inside the validated program testing window and outside blackouts

`dry-run` mode is intentionally treated as non-target-touching policy computation. It may be allowed even when automation is disabled or the current time is outside a testing window, provided every scope and technique gate passes. `planned` and `live` remain stricter.

Global scope remains an intersection, not a replacement. Either layer can veto a target, and `out_of_scope` takes precedence over broader `in_scope` entries.
