> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Program Scope Intake and Validation Pattern

Use this reference when moving a cybersecurity workspace from a global allowlist into per-program bug bounty/client scope files.

## Goal

A bug bounty automation run should be allowed only when both layers pass:

1. Global workspace allowlist, usually `config/scope.txt` and the runtime `safe_target` guard.
2. Active program rules, usually `programs/<program-slug>/scope.json`.

If either layer is missing, ambiguous, malformed, or disallows the target/technique, route to clarification instead of running target-touching automation.

## Suggested `scope.json` shape

Keep the first version boring and explicit:

```json
{
  "program": "example-program",
  "source": "manual-intake",
  "last_reviewed": "YYYY-MM-DD",
  "authorization": {
    "type": "bug_bounty|client|owned_lab|ctf",
    "evidence_ref": "local note or program URL; do not store secrets"
  },
  "in_scope": [
    {"type": "domain", "value": "example.com"},
    {"type": "wildcard_domain", "value": "*.example.com"},
    {"type": "url", "value": "https://app.example.com"},
    {"type": "cidr", "value": "192.0.2.0/24"}
  ],
  "out_of_scope": [
    {"type": "domain", "value": "thirdparty.example"}
  ],
  "allowed_techniques": ["passive_recon", "http_probe", "template_scan_safe"],
  "disallowed_techniques": ["dos", "bruteforce", "social_engineering", "credential_theft"],
  "rate_limits": {
    "requests_per_second": 1,
    "concurrency": 2
  },
  "testing_window": "always|UTC range|manual approval required",
  "reporting": {
    "portal": "program portal name or URL",
    "notes": "triage-only; manual verification required"
  }
}
```

## Validation rules

- Validate JSON syntax and schema before any run.
- Normalize hostnames/URLs before matching. Decide and document wildcard semantics: whether `*.example.com` includes only subdomains or also the apex `example.com`.
- Apply explicit out-of-scope rules before in-scope allows.
- Require the selected technique/module to be present in `allowed_techniques` and absent from `disallowed_techniques`.
- Enforce conservative defaults when rate limits are absent, but do not treat absence as permission for aggressive scanning.
- Revalidate every expansion output through both global scope and the active program file before scan/probe/fuzz/nuclei/notification stages.
- Do not store API keys, private program tokens, session cookies, credentials, or proprietary payload lists in `scope.json`; use redacted notes or local secret stores.

## Handoff expectations

- Cowork should draft the schema, intake checklist, and wording for ambiguous program rules.
- Codex should implement schema validation, dry-run evidence, and negative tests for out-of-scope and disallowed techniques.
- Hermes should verify with synthetic targets only unless the operator has explicitly approved a real lab/client/program target.
