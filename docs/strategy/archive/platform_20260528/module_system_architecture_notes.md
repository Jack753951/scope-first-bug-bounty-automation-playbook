> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Module System Architecture Notes

Date: 2026-05-15
Status: Architecture direction for future phases after Phase 1 program policy gates
Source: operator-provided Codex architecture suggestion, adapted for this workspace

## Verdict

The proposed direction is good and aligned with the project goal: update-friendly, systematic, extensible authorized testing with unified scope gates, structured evidence, standardized findings, and agent-assisted review.

However, implementation should be staged. Do not build vulnerability modules before the policy gate and finding/evidence contracts are stable.

Recommended order:

1. Program policy gate / target decision helper.
2. Finding and evidence schemas.
3. Module manifest schema.
4. Module runner skeleton.
5. Safe passive audit modules.
6. Triage modules.
7. Verification modules only with explicit approval gates.

## Proposed Layout

The suggested layout is useful, but should be separated slightly so core contracts are not mixed with ad-hoc scripts:

```text
scripts/
  core/
    scope.py              # global + program authorization checks
    policy.py             # target/technique/mode decision engine
    runner.py             # safe command runner / Kali SSH bridge wrapper
    evidence.py           # evidence capture, hashing, redaction metadata
    finding.py            # finding schema helpers
    report.py             # Markdown / JSON draft output

modules/
  _schema/
    module.schema.json
    finding.schema.json
    evidence.schema.json
  checks/
    web/
      headers/
        module.yaml
        check.py
        tests/
      cors/
        module.yaml
        check.py
        tests/
      jwt/
        module.yaml
        check.py
        tests/
      open_redirect/
        module.yaml
        check.py
        tests/
      xss_reflection/
        module.yaml
        check.py
        tests/
  profiles/
    audit-baseline.yaml
    web-passive.yaml
    lab-active.yaml

runs/
  <run_id>/
    run.json
    audit.log
    evidence/
    findings/
```

Key adjustment: `modules/` should be top-level, not under `scripts/`, because modules are content/plugins while `scripts/core/` is execution infrastructure.

## Core Contracts

### Module Manifest

Each module declares what it wants to do before it runs:

```yaml
schema_version: "1.0"
id: cors_misconfig
name: CORS Misconfiguration Check
category: web
level: audit
risk: medium
requires_auth: false
safe_by_default: true
active_level: passive
techniques:
  - http_probe
  - vulnerability_scan_passive
target_types:
  - url
tools:
  - curl
outputs:
  - finding_json
  - markdown_summary
owasp:
  - A05 Security Misconfiguration
cwe:
  - CWE-942
```

Important required fields for this project:

- `schema_version`
- `id`
- `level`: `audit`, `triage`, or `verification`
- `active_level`: `passive`, `safe_active`, `intrusive`, `requires_explicit_approval`
- `techniques`: must map to program scope allowed techniques
- `target_types`
- `safe_by_default`
- `requires_network`
- `dry_run_supported`
- `output_schema`

### Module Input

Modules should not parse global CLI flags or scope files directly. The runner passes a normalized input object:

```json
{
  "run_id": "20260515T180000Z_public-bounty-example",
  "program": "public-bounty-example",
  "target": "https://example.com",
  "mode": "dry-run",
  "module": "cors_misconfig",
  "policy_decision": {
    "verdict": "allow",
    "reasons": ["global_scope_allowed", "program_scope_allowed", "technique_allowed"]
  },
  "output_dir": "runs/.../modules/cors_misconfig/"
}
```

### Module Output / Finding Candidate

Modules output standardized candidate findings only:

```json
{
  "schema_version": "1.0",
  "module": "cors_misconfig",
  "target": "https://example.com",
  "status": "needs_verification",
  "severity_hint": "medium",
  "confidence": "low",
  "evidence": [],
  "summary": "Potential permissive CORS behavior observed.",
  "remediation": "Restrict allowed origins and avoid reflecting arbitrary Origin headers."
}
```

Allowed automated statuses should stay conservative:

- `no_observation`
- `candidate`
- `needs_verification`
- `not_applicable`
- `error`

A module should not emit `confirmed` by itself.

## Three-Level Module Model

### Level 1: Audit Modules

Low-risk baseline checks, mostly passive or single-request observations.

Examples:

- headers
- TLS
- cookies
- robots.txt
- well-known files
- CORS baseline observation
- security.txt

Default posture:

- `safe_by_default: true`
- `active_level: passive`
- good first module-runner test targets

### Level 2: Triage Modules

Potential vulnerability indicators that require agent/human analysis before reporting.

Examples:

- open redirect candidate
- JWT weak configuration hints
- reflected input observations
- known CVE fingerprinting
- GraphQL introspection check where allowed

Default posture:

- `status: needs_verification`
- evidence required
- Claude/Cowork review required before report draft

### Level 3: Verification Modules

Higher-risk proof steps or confirmation workflows.

Examples:

- vulnerability-specific confirmation
- auth-sensitive flows
- anything that might mutate state
- anything needing a callback/OOB endpoint

Default posture:

- not auto-run
- `requires_explicit_approval`
- only after program scope and operator approval
- strong audit events
- preferably manual or semi-manual first

## Safety Gate Model

Module execution must be centrally gated:

1. Validate program scope file.
2. Check global `config/scope.txt` intersection.
3. Check target is in program scope and not out-of-scope.
4. Check module technique tags are allowed by program scope.
5. Check module active level is allowed by selected profile and mode.
6. Check testing window and blackout.
7. Check rate limits and concurrency profile.
8. Emit audit decision.
9. Only then run module.

Modules must never call `safe_target`, read program scope, or override policy directly. They receive a pre-approved input object from the runner.

## Agent Review Integration

After modules run:

1. Scripts/modules write structured candidate findings and evidence.
2. Hermes validates run manifest, policy decisions, and evidence paths.
3. Claude/Cowork reviews candidate findings for false positives, impact, verification steps, and report quality.
4. Codex fixes module/parser/report-generator issues.
5. Hermes updates handoff and decides whether findings remain candidates, need manual verification, or become report drafts.

## Phase Placement

Do not jump directly to full modules yet.

Suggested future phases:

- P1-3: program policy decision helper (`allow/deny` target + technique + mode).
- P1-4: minimal `recon.sh --program` integration using the policy helper.
- P2-1: finding/evidence schema.
- P2-2: run manifest / execution ledger.
- P2-3: module manifest schema.
- P2-4: module runner skeleton with dry-run only.
- P2-5: first Level 1 audit modules (`headers`, `cors`, `jwt`, `security.txt`, basic TLS metadata if safe).
- P3: Level 2 triage modules and agent-assisted analysis workflow.
- P4: gated verification workflows.

Claude/Cowork's systematization review adds one important directory split: organize future modules by risk level, not only by technology:

```text
modules/
  checks/    # lowest-risk passive/baseline observations
  triage/    # candidate-generating probes needing agent/human review
  verify/    # explicit-approval verification helpers only
```

This layout lets policy code enforce stronger defaults from the path/category before reading module details. `verify/` must never run without explicit program allowance and operator approval.

## Acceptance Criteria For The Future Module System

Before real modules run against any target:

- module manifest validates
- program scope validates
- global scope intersects
- technique allowed
- selected profile allows module level
- dry-run mode works
- output validates against finding schema
- evidence paths are under run directory
- no secrets in report output
- Claude/Cowork can review candidate findings from structured output
- Hermes audit log explains every allow/deny decision
