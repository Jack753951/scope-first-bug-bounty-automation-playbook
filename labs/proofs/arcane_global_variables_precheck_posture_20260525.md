> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Arcane bootstrap precheck posture note — 2026-05-25

Status: blocked/fail-closed before setup
Created: 2026-05-25T03:29:35Z
Route: Phase 5A local-bootstrap prep
Candidate: Arcane <specific-ghsa-id>
Script: `scripts/labs/arcane_global_variables_bootstrap_precheck.sh`
Local artifact root: `setting/local/arcane_precheck/arcane_global_variables_precheck_20260525_prep/` (ignored by git)

## What was executed

```bash
bash scripts/labs/arcane_global_variables_bootstrap_precheck.sh --help
RUN_ID=arcane_global_variables_precheck_20260525_prep \
OUT_ROOT="$PWD/setting/local/arcane_precheck" \
PROJECT_ROOT="$PWD" \
bash scripts/labs/arcane_global_variables_bootstrap_precheck.sh --precheck-only
```

## Result

```text
verdict: blocked
block_reason: docker CLI missing on this host/VM
precheck_rc: 1
```

This is the expected safe outcome on the Windows control-plane environment: the helper failed closed before any Arcane launch, account creation, Docker socket mount, or proof request.

## Boundary observed

```text
no Arcane container launched
no proof endpoint request sent
no accounts created
no public/live target touched
no Docker socket mounted
no scope/config authorization changed
```

## Generated local diagnostics

```text
setting/local/arcane_precheck/arcane_global_variables_precheck_20260525_prep/run.log
setting/local/arcane_precheck/arcane_global_variables_precheck_20260525_prep/decision/verdict.txt
setting/local/arcane_precheck/arcane_global_variables_precheck_20260525_prep/decision/block_reason.txt
setting/local/arcane_precheck/arcane_global_variables_precheck_20260525_prep/diagnostics/internet_pre.txt
```

These diagnostics are intentionally under `setting/local/` and ignored by git.

## Next gate

Arcane setup/proof remains blocked until the operator intentionally runs the precheck from the intended disposable victim-lab Docker environment, or Hermes is explicitly routed into the Kali/victim-lab path with a confirmed disposable Docker-in-Docker or isolated daemon/proxy posture.

Do not mount or expose a host/user Docker socket to Arcane.
