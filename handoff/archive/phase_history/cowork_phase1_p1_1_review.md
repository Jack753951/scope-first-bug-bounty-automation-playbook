> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Independent Review: Phase 1 P1-1 Program Scope Schema

Generated: 2026-05-15
Reviewer scope: read-only inspection of the schema, three examples, both READMEs, and the existing codex review. No live tools, no network, no runtime execution.

## Verdict

ACCEPT.

P1-1 ships a schema-and-docs-only contract that is internally consistent, default-deny in posture, parseable by stock JSON readers, and shaped to support future loader work without re-litigating the data model.

## What I Checked

- JSON parse safety of all four JSON files.
- Schema correctness and the strictness of its constraints.
- Default-deny posture at the contract layer (closed enums, required fields, conditional rejections).
- Extensibility: how cleanly P1-2/P1-3 can build on this without breaking the wire format.
- Internal consistency between `programs/README.md`, `programs/_schema/README.md`, the schema, and the three examples.
- Cross-check against the prior `handoff/codex_review.md` claims.

## JSON Parse

All four JSON documents are syntactically valid (balanced braces/brackets, no trailing commas, quoted keys, ASCII content). They will load with stock `JSON.parse`, `json.load`, or `jq`. No BOM, no embedded control characters, no comments. Filenames and slugs match across the files.

## Schema Safety

Strong points:

- Draft 2020-12 with `$id` and `additionalProperties:false` on every object, including nested entry types and `$defs`. This rejects unknown keys at the contract layer.
- `schema_version` is `const:"1.0"` — exact-match pinning so future versions force an explicit consumer upgrade.
- Closed enums for `program.platform`, `techniques.*`, `testing_window.days`, and `scope.idn_handling`. `allow_idn` is intentionally absent.
- Non-authorizable techniques (`dos`, `credential_brute_force`, `social_engineering`, `physical`, `malware`, `callback_payloads`) are rejected from `techniques.allowed` via `not:{contains:{...}}` — defense in depth even if an operator copies a forbidden tag into the wrong list.
- Conditional `allOf`: `testing_windows.always=true` is rejected for any platform that is not `lab`, `ctf`, or `self-hosted` (`then:false`). All three examples respect this (only `ctf` uses `always:true`).
- When `always=false`, `timezone` and `allowed` are required.
- Required top-level blocks: `schema_version`, `program`, `scope`, `techniques`, `rate_limits`, `testing_windows`, `expiration`. Required sub-keys (`policy_version`, `policy_acknowledged_at`, `authorization_reference`, `valid_from`, `valid_until`) are present.
- `scope.in_scope` and `techniques.allowed` carry `minItems:1`, so empty-meaning-allow files cannot be authored by accident.
- Bounded numerics on every rate cap (max ceilings on `max_concurrency`, `max_requests_per_second`, `nuclei_*`, `naabu_rate`, etc.). Bounded string lengths on free-text fields (`authorization_reference`, `notes`, `reason`, `automation_notes`).
- Pattern guards on `program.slug`, `domain_name`, `wildcard`, `cidr` (IPv4), `ipv4`, `url_prefix`, and `time_hhmm`.

Limits the schema cannot express (acknowledged in `programs/_schema/README.md`, called out here for the loader spec):

- No chronological check that `expiration.valid_until > expiration.valid_from`.
- No check that each `testing_window.end > start` (or that overnight windows are split).
- No cross-list check that a tag does not appear in both `techniques.allowed` and `techniques.forbidden`.
- `JSON Schema` `format:"date-time"` is annotation-only by default; loaders must validate explicitly.
- `rate_limits` requires only `minProperties:1`, so a file could legally set just one of the eight caps. The runtime must apply the documented "minimum effective value vs `config/recon.conf`" rule and fall back to safe defaults on unset dimensions.
- `domain_name` and `wildcard` patterns require an alphabetic TLD (`[a-z]{2,63}`). Punycode TLDs (`xn--*`, which contain digits and hyphens) will fail validation. P1-1 examples do not use IDN, so this is dormant — but `idn_handling:"punycode_only"` implies punycode hostnames will eventually appear. The Phase 0.1 evidence in `codex_review.md` already exercised `xn--bcher-kva.example` through the runtime; the schema would reject the same hostname today. Worth fixing in P1-2 (relax TLD pattern to `(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)` or add an explicit `xn--` alternative).
- Minor inconsistency: `entry_common` is referenced by `domain_entry` and `wildcard_entry`, but `cidr_entry`, `ip_entry`, and `url_prefix_entry` inline `notes`/`reason` instead. Functionally identical, just duplicated. Low risk.
- `cidr` and `ip` are IPv4-only. P1-1 README is explicit, so this is a known boundary, not a defect.

None of the above blocks acceptance — they are P1-2 loader work and the contract already documents that runtime must enforce them.

## Default-Deny Posture

The contract reinforces default-deny in the right places:

- `additionalProperties:false` everywhere prevents silent acceptance of typo'd or smuggled fields.
- Pinned `schema_version` forces future readers to opt into a known shape.
- Closed enums force unknown values to fail at the contract boundary.
- `idn_handling:"allow_idn"` is absent — a permissive IDN posture cannot be encoded.
- Non-authorizable techniques cannot be placed in `allowed`.
- The "always-on for non-lab/ctf/self-hosted" combination is unrepresentable.
- Required `expiration.valid_from`/`valid_until` ensure every file carries an explicit lifetime that runtime can refuse outside.

Both READMEs restate the contract: missing/malformed/expired/unknown → deny, program scope intersects (never expands) `config/scope.txt`, `out_of_scope` wins. The wording is consistent across `programs/README.md` and `programs/_schema/README.md`.

## Extensibility

- The `$defs` block factors entry types, technique vocabulary, time/IP/domain primitives, and window/blackout shapes — future schemas can add an entry type or technique tag with a single edit and a version bump.
- Schema versioning is explicit (`const:"1.0"`), so additive changes will need a deliberate `1.1`/`2.0` revision and consumer-side handling — exactly the trade-off P1-1 describes.
- `program.platform` reserves `other` and `self-hosted` so new program kinds can appear without forcing a schema change for every onboarding.
- Optional fields (`operator_contact`, `program_contact`, `automation_notes`, per-tool rate caps, `blackouts`, `notes`, `reason`, `include_apex`) leave room for richer authorship without breaking strict files.
- Future module manifests and finding schemas can `$ref` the same `technique`, `domain_name`, `ipv4`, and `time_hhmm` definitions, which is the stated direction in `programs/README.md`.

## Examples

- `public-bounty.example.json`: `<bug-bounty-platform>` platform, `always:false` with weekday window and a holiday blackout, passive techniques only, intersects schema constraints cleanly.
- `client-engagement.example.json`: `client` platform with RFC 5737 IPv4/CIDR and RFC 2606 domains, `reject_idn`, two testing windows in `America/New_York`, three-month validity. Demonstrates `include_apex:false` with a separate apex entry.
- `ctf-platform.example.json`: `ctf` platform exercising `always:true` (legal for ctf), broader allowed techniques including `vulnerability_scan_active` and `intrusive_fuzz`, abuse categories still forbidden. Validates the platform-conditional rule positively.

All three examples use only documentation/example IPs and domains and are clearly labelled as placeholders. None contain secrets or real authorization text.

## Cross-Check Against `handoff/codex_review.md`

The P1-1 section in `codex_review.md` matches what is on disk: the file inventory is correct, the safety boundaries are accurately summarized, and the open risks (no loader yet, schema cannot express every runtime rule) are flagged. The "LIMITED" notes about Python and Schema validators being unavailable are honest — JSON parse plus schema inspection is a defensible P1-1 acceptance bar.

## Recommendations for P1-2 (non-blocking)

1. Implement loader-side checks for: `valid_until > valid_from`, `testing_window` ordering, and disjoint `allowed`/`forbidden` technique sets.
2. Treat `rate_limits` minimums as a `min(program, recon.conf)` per dimension; supply safe defaults for any unset dimension.
3. Relax `domain_name`/`wildcard` TLD patterns to permit punycode TLDs before the loader has to accept `xn--*` hostnames.
4. Decide IPv6 support posture and either add `cidr_v6`/`ip_v6` $defs or document the IPv4-only boundary in P1-2 release notes.
5. Optional cleanup: have `cidr_entry`, `ip_entry`, and `url_prefix_entry` reference `entry_common` like the other two for consistency.

## Final

ACCEPT — P1-1 lands a strict, default-deny, extensible data contract with safe examples and accurate documentation. The remaining gaps belong to the runtime loader and are already scoped to later phases.
