> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Finding / Evidence Schema Contract Pattern

Use when building module output contracts for an authorized cybersecurity lab, bug bounty platform, or defensive automation workspace.

## Reusable lesson

Before inventing a finding/evidence schema, quickly inspect established formats and projects, then make an explicit adapt-vs-build decision. Useful reference families:

- ProjectDiscovery Nuclei templates: `id`, `severity`, `tags`, `metadata`, `classification`, CWE/CVSS/references, and declarative module metadata ideas.
- SARIF/OSV/DefectDojo-style concepts: stable finding identity, severity/confidence, references, evidence links, remediation, and verification state.
- Bug bounty scope/tool repos: useful for scope vocabulary but usually not enough for policy-gated evidence contracts.

For this workspace, prefer project-specific contracts when the platform needs authorization gates, default-deny semantics, triage-only candidate findings, redacted repo-safe evidence metadata, and future agent-assisted review.

## Contract shape

Candidate findings emitted by automation should be explicitly triage-only:

- Allow statuses such as `candidate` / `needs_verification`.
- Reject `confirmed` or equivalent final-verdict statuses from automated modules.
- Require `scanner_output_only: true` or an equivalent field that prevents scripts from implying human confirmation.
- Require source/run linkage so every finding/evidence item belongs to a concrete run envelope.
- Reserve confirmation for a later human/agent review step with evidence, impact, remediation, and retest notes.

Evidence metadata should be safe to commit and route to reviewers:

- Evidence paths must be repository-relative under `runs/<run_id>/evidence/`.
- Reject path traversal, absolute paths, URLs, backslash Windows paths, mismatched `run_id`, and non-canonical paths.
- Require canonical SHA-256 for file integrity.
- Require an explicit redaction marker/boolean.
- Keep metadata flat and scalar when possible.
- Block sensitive keys and values case-insensitively: authorization, bearer, cookie, set-cookie, token, secret, password, api_key, raw/body/request/response/header, etc.

## TDD/review sequence

1. Write failing tests for expected valid examples and for unsafe examples before creating schemas/validators.
2. Implement JSON Schema plus a stricter standard-library validator for semantic checks JSON Schema cannot express reliably.
3. Run schema-only tests and validator tests; ensure both reject the same sensitive key/value variants.
4. Send the result to independent Cowork/Claude review, asking specifically for bypasses in path handling, status semantics, metadata leakage, and schema-vs-validator mismatches.
5. When review finds a bypass, add a regression test first, then patch both schema and validator as needed.
6. Record the contract in `modules/_schema/README.md` and handoff notes; do not treat module output as confirmed findings.

## Common bypasses to test

- `../` traversal and encoded/doubled traversal segments.
- Absolute paths such as `/tmp/x`, `C:\x`, or URL-like `https://...`.
- Backslash path separators in otherwise relative paths.
- `source.run_id` not matching the evidence path prefix.
- Upper/lower/mixed-case sensitive keys (`Authorization`, `HEADER`, `Set-Cookie`).
- Sensitive values hidden in benign keys (`notes: "Authorization: Bearer redacted"`).
- Non-canonical SHA-256 strings.
- Metadata objects/arrays used to smuggle raw request/response material.

## Validation expectation

A complete pass should include Python compile, JSON parsing, focused tests, the project review wrapper, static diff/safety scan, and independent review marked PASS or non-blocking before PR/issue/Obsidian updates.