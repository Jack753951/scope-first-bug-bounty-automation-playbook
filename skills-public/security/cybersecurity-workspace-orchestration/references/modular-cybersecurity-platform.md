> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Modular Cybersecurity Platform Architecture

Use this reference when the user wants the cybersecurity lab to become an update-friendly, systematic, extensible platform rather than a pile of one-off scripts.

## Recommended Layering

Prefer separating core execution infrastructure from plugin/module content:

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

Rationale: `scripts/core/` is stable infrastructure; top-level `modules/` is plugin content that can be enabled, reviewed, versioned, and tested independently.

## Module Manifest Contract

Each module declares what it wants to do before it runs:

```yaml
schema_version: "1.0"
id: cors_misconfig
name: CORS Misconfiguration Check
category: web
level: audit                 # audit | triage | verification
risk: medium
requires_auth: false
safe_by_default: true
active_level: passive        # passive | safe_active | intrusive | requires_explicit_approval
requires_network: true
dry_run_supported: true
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

Important required fields for this user's project:

- `schema_version`
- `id`
- `level`
- `active_level`
- `techniques` mapped to program scope allowed techniques
- `target_types`
- `safe_by_default`
- `requires_network`
- `dry_run_supported`
- `output_schema`

## Module Input/Output Contract

Modules should not parse global CLI flags, read `config/scope.txt`, or load `programs/<slug>/scope.json` directly. A runner/policy layer passes a normalized pre-approved input object.

Example input:

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

Example output should be a conservative finding candidate, never confirmed:

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

Allowed automated statuses: `no_observation`, `candidate`, `needs_verification`, `not_applicable`, `error`. Do not let modules emit `confirmed` without agent/human verification.

## Three-Level Module Model

1. **Audit modules** — low-risk baseline checks: headers, TLS metadata, cookies, robots.txt, security.txt, well-known files, CORS baseline observation. Usually `safe_by_default: true` and `active_level: passive`.
2. **Triage modules** — potential vulnerability indicators requiring review: open redirect candidates, JWT weak config hints, reflected input observations, known CVE fingerprinting, GraphQL introspection where allowed. Usually emit `needs_verification`.
3. **Verification modules** — higher-risk proof steps or confirmation workflows. Not auto-run; require explicit operator approval, program scope, strong audit events, and ideally manual/semi-manual flow first.

## Central Safety Gate

Before a module runs, the runner/policy layer must:

1. Validate the program scope file.
2. Check global `config/scope.txt` intersection.
3. Confirm target is in program scope and not in out-of-scope.
4. Confirm module techniques are allowed by program rules.
5. Confirm module active level is allowed by selected profile and mode.
6. Check testing window and blackout.
7. Apply rate/concurrency caps.
8. Emit audit allow/deny reasons.
9. Only then execute the module.

Modules must not bypass or duplicate this gate.

## Agent Review Integration

After module runs:

1. Scripts/modules write structured candidate findings and evidence.
2. Hermes verifies run manifest, policy decisions, and evidence paths.
3. Claude/Cowork reviews false positives, impact, verification steps, report quality, and architecture fit.
4. Codex fixes module/parser/report-generator issues.
5. Hermes records decisions and routes candidates to manual verification, rejection, or report draft.

## Suggested Phase Order

Do not jump straight to vulnerability modules. Build platform contracts first:

- P1-3: program policy decision helper (`allow/deny` for target + technique + mode).
- P1-4: minimal `recon.sh --program` integration using the policy helper.
- P2-1: finding/evidence schemas.
- P2-2: run manifest / execution ledger.
- P2-3: module manifest schema.
- P2-4: module runner skeleton with dry-run only.
- P2-5: first Level 1 audit modules.
- P3: Level 2 triage modules and agent-assisted analysis workflow.
- P4: gated verification workflows.
