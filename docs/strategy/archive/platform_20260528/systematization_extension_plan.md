> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Systematization / Extensibility Plan

Date: 2026-05-15
Status: Architecture decision and staged implementation plan
Source: Claude/Cowork third-party recommendation, adopted by Hermes after local inspection

## Current-State Verification

Hermes verified locally:

- `recon.sh` is 986 lines, confirming monolithic-script risk.
- Empty intent directories currently exist: `exploits/`, `cves/`, `recon/`, `tools/`.
- Future architecture directories are not implemented yet: `modules/`, `scripts/core/`, `runs/`.
- Candidate first-pass audit/triage scripts exist under `scripts/`: `headers_audit.sh`, `cors_audit.sh`, `jwt_inspect.sh`, `open_redirect.sh`, `xss_finder.sh`, etc.

## Decision

Adopt Claude/Cowork's recommendation with two safety constraints:

1. Do not start by writing vulnerability modules. First build the contracts and core helpers that prevent modules from bypassing scope, audit, evidence, and finding rules.
2. Before adding or changing a major platform contract/schema/module/runner/reporting/tool boundary, run the OSS Recon Gate in `docs/policy/oss_recon_gate.md` so the design learns from mature open-source projects/formats without inheriting unsafe target-touching defaults.

## Target Architecture

```text
scripts/
  core/
    scope.py              # global + program scope intersection helpers
    policy.py             # target/technique/mode decision engine
    runner.py             # safe subprocess and Kali SSH bridge wrapper
    evidence.py           # evidence capture, hashing, redaction metadata
    finding.py            # finding schema helpers
    report.py             # Markdown/JSON draft helpers

modules/
  _schema/
    module.schema.json
    finding.schema.json
    evidence.schema.json
  checks/
    web/headers/
    web/cors/
    web/jwt/
    network/tls/
  triage/
    web/open_redirect/
    web/xss_reflection/
    web/lfi_probe/
  verify/
    web/sqli_confirm/
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

## Key Design Rules

1. Modules do not read scope files directly.
2. Modules do not call subprocess directly.
3. Modules do not write arbitrary files directly.
4. Modules receive normalized input from the runner.
5. Modules emit standardized candidate findings only.
6. Modules cannot mark findings as `confirmed`.
7. Policy decisions happen in `scripts/core/policy.py` before module execution.
8. Evidence is stored under `runs/<run_id>/evidence/` with hashes/redaction metadata.
9. Findings are stored under `runs/<run_id>/findings/` and validated against schema.
10. Claude/Cowork reviews candidate findings before report drafting.

## Recommended Phase Order

### P1-3: Program Policy Decision Helper

Create `scripts/core/policy.py` or `scripts/program_policy_check.py` to answer:

```json
{
  "program_scope": "programs/<slug>/scope.json",
  "target": "https://example.com/path",
  "technique": "http_probe",
  "mode": "dry-run"
}
```

Output:

```json
{
  "verdict": "allow",
  "reasons": ["program_scope_valid", "target_in_scope", "technique_allowed"],
  "audit_event": "PROGRAM_POLICY_ALLOW"
}
```

Boundary: no scanning, no module execution, no `recon.sh` wiring yet.

### P1-4: Minimal Runtime Integration

After independent review, wire the policy helper into `recon.sh --program <slug>` for dry-run and limited preflight decisions only.

Required gates:

- validated program scope
- global `config/scope.txt` intersection
- target allow/deny
- technique allow/deny
- automation flag
- testing window / blackout
- audit event

### P2-1: Finding / Evidence Schemas

Create:

- `modules/_schema/finding.schema.json`
- `modules/_schema/evidence.schema.json`
- `scripts/core/finding.py`
- `scripts/core/evidence.py`

Findings remain `candidate` / `needs_verification` until agent/human review.

### P2-2: Run Manifest / Execution Ledger

Create:

- `runs/README.md`
- `scripts/core/run_manifest.py` or equivalent helper

Each execution gets:

- `run.json`
- `audit.log`
- `evidence/`
- `findings/`

### P2-3: Module Manifest Schema

Create:

- `modules/_schema/module.schema.json`
- `modules/profiles/*.yaml`

Manifest must include:

- `schema_version`
- `id`
- `level`: `audit`, `triage`, `verification`
- `active_level`: `passive`, `safe_active`, `intrusive`, `requires_explicit_approval`
- `techniques`
- `target_types`
- `safe_by_default`
- `requires_network`
- `dry_run_supported`
- `defense_ref`
- `output_schema`

### P2-4: Module Runner Skeleton

Create dry-run-only runner that:

- validates module manifest
- validates program policy decision
- creates run directory
- passes normalized input to module
- collects standardized output
- validates finding/evidence schema
- emits audit events

No real target execution until reviewed.

### P2-5: First Level 1 Audit Modules

Migrate safest existing scripts first:

- `scripts/headers_audit.sh` -> `modules/checks/web/headers/check.py`
- `scripts/cors_audit.sh` -> `modules/checks/web/cors/check.py`
- `scripts/jwt_inspect.sh` -> `modules/checks/web/jwt/check.py`

These should begin in dry-run/sample-fixture mode, then lab-only, then authorized program mode.

## Empty Directory Hygiene

Existing empty directories should not remain ambiguous. Add README files explaining whether they are reserved or deprecated:

- `exploits/` should clearly state that exploit code is not accepted by default and requires explicit authorization and safety review.
- `cves/` should state it is for advisory/intelligence archives, not exploit payloads.
- `recon/` should state whether it will hold future recon modules or remain reserved.
- `tools/` should state it is for safe wrappers/helpers, not arbitrary offensive tooling.

## Acceptance Criteria For This Architecture Direction

- Future Codex tasks prefer `scripts/core/` helpers and versioned schemas over adding logic to `recon.sh`.
- Claude/Cowork reviews architecture fit, not only blocker defects.
- No module can bypass policy/scope gates.
- Findings and evidence are structured before report generation.
- Empty directories are documented or removed.
- `recon.sh` is gradually reduced to a thin orchestrator or retired after equivalent modules exist.
