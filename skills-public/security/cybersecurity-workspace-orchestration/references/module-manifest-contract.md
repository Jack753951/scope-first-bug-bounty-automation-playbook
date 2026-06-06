> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Module Manifest Contract Pattern

Use this reference when designing or reviewing a dry-run-first module/plugin manifest for an authorized cybersecurity automation platform.

## Open-format reconnaissance

Before inventing fields, briefly inspect established ecosystems and record what was adapted or rejected:

- Nuclei templates: stable template IDs, severity/tags, request metadata, and template-oriented scanner metadata.
- OWASP ZAP add-ons/extensions: add-on IDs, versioning, dependency/extension metadata, lifecycle compatibility.
- OSCAL/SARIF/OSV/DefectDojo-style concepts as relevant: component provenance, result/evidence schemas, triage/reporting boundaries.

Do not copy external formats blindly. Prefer a project-specific contract when the platform has stronger authorization, dry-run, and triage-only requirements than the source ecosystem.

## Recommended manifest fields

Version all manifests and require explicit declarations for:

- `schema_version` such as `module_manifest/1.0`.
- Stable module `id`, semantic `version`, `name`, and `description`.
- Risk level and supported target types.
- Allowlisted technique tags only; unknown tags fail closed.
- `supports_dry_run=true` as mandatory for early runner phases.
- Network posture (`none`, `dns`, `target-http`, `target-tcp`, etc.) and whether the module is target-touching.
- Destructive, intrusive, OAST/callback, and external-tool declarations.
- Output contracts, e.g. `run/1.0`, `finding/1.0`, `evidence/1.0`.
- Safety gates: policy decision required, scope match required, manual verification required, scanner-output-only, redacted evidence only, no raw secrets, no loot writes, no destructive actions, no callbacks unless explicitly approved in a later phase.

## Default-deny validator semantics

Pair JSON Schema with a stricter semantic validator. Validate both because JSON Schema alone often cannot express all safety relationships cleanly.

Reject by default when:

- Required safety fields are missing or ambiguous.
- `supports_dry_run` is absent or false.
- Technique tags are unknown or duplicated.
- Target types are duplicated.
- Output schema references are unknown.
- Safety gates are missing or weakened.
- A passive-only technique declares `target_touching=true`.
- A known technique is paired with an incompatible `network_access` value.
- Any manifest implies confirmed vulnerabilities instead of candidate/triage-only output.

Maintain an explicit technique-to-posture map. Example constraints:

- `active.http_get` and `active.web_content_check` require `network_access=target-http` and `target_touching=true`.
- `active.tcp_connect` requires `network_access=target-tcp` and `target_touching=true`.
- `active.dns_lookup` requires `network_access=dns` and usually `target_touching=false` unless the project policy explicitly treats DNS as target-touching.
- Passive/research tags require `target_touching=false`.

## Review traps caught in practice

Independent review should try bypass fixtures, not just happy paths. Useful fixtures include:

- Known active technique with the wrong network posture (`active.http_get` + `dns`, `active.tcp_connect` + `target-http`).
- Passive-only technique with `target_touching=true`.
- Python semantic validator rejects an unsafe manifest but JSON Schema still accepts it. Keep schema-only consumers fail-closed where possible, and document any unavoidable semantic-only checks.
- Duplicate IDs/tags that dictionary conversion could silently collapse.

## Validation checklist

- TDD first: invalid fixtures before implementation.
- Compile validator scripts and parse all JSON schemas.
- Run focused manifest tests plus the full relevant schema/policy suite.
- Run the repository review/preflight wrapper.
- Record the external-format comparison, safety boundary, validation commands/results, and independent-review verdict in handoff/PR text.
- Keep the runner offline/dry-run-only until manifest validation, policy decision binding, run ledger, and output contract validation are all enforced.
