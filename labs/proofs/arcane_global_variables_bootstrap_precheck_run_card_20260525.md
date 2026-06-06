> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Arcane <specific-ghsa-id> Bootstrap Precheck Run Card

Status: drafted / precheck-only / no target touched
Date: 2026-05-25
Script: `scripts/labs/arcane_global_variables_bootstrap_precheck.sh`
Related: `handoff/phase5a_arcane_global_variables_feasibility_review_20260525.md`, `handoff/phase5a_arcane_global_variables_bootstrap_plan_20260523.md`, `targets/catalog/arcane_ghsa_jpjh_jm2p_39hh.md`

## Purpose

Prepare a fail-closed local-lab bootstrap gate for Arcane `<specific-ghsa-id>` before any Arcane target is launched.

The script is intentionally not a proof runner. It checks local-lab and Docker posture, creates an artifact directory, and can render a review-only compose template for a disposable Docker-in-Docker posture.

## Boundary

Allowed in this run card:

```text
local file/artifact creation
host-only lab IP sanity check
Docker CLI posture inspection
default host/user Docker socket rejection
review-only compose template rendering
```

Not allowed in this run card:

```text
no public/live target testing
no Arcane launch
no Docker socket mount
no proof/exploit request
no account creation
no global variable write
no real project/secret access
no callbacks/OAST/tunnels
no report submission
```

## Why precheck first

Arcane is a Docker management application. The official examples can mount `/var/run/docker.sock` or proxy a Docker daemon. For this project, that is only acceptable if the daemon is disposable and isolated inside the victim lab. Any ambiguity must fail closed before setup.

## Intended run location

Preferred later location:

```text
<victim-vm> or equivalent disposable victim VM
host-only network
no real projects/secrets
```

This draft was created from the Windows Hermes control plane but is not executed against the lab by default.

## Commands

Precheck only:

```bash
bash scripts/labs/arcane_global_variables_bootstrap_precheck.sh --precheck-only
```

Render a review-only compose template after precheck:

```bash
bash scripts/labs/arcane_global_variables_bootstrap_precheck.sh --render-compose
```

Expected artifact root:

```text
~/<artifact-output-dir>/arcane_global_variables_precheck_<YYYYMMDDTHHMMSSZ>/
```

Expected pass verdict:

```text
precheck_passed_no_target_touched
```

Expected fail behavior:

```text
blocked
```

The script should block if the effective Docker endpoint is the default host/user socket such as `unix:///var/run/docker.sock`.

## Review-only compose template

When `--render-compose` is used, the script writes:

```text
templates/compose.arcane.disposable.template.yaml
templates/next_manual_steps.md
```

The template is not executed. It still requires operator/Hermes review and confirmation that the Docker-in-Docker/proxy endpoint is disposable.

## Next gate after this run card

Do not proceed to launch/proof until all are true:

```text
operator wants to continue this Arcane local-bootstrap lane
disposable Docker daemon/proxy posture is confirmed
NAT/download window is documented if image pulls are needed
NAT is closed/verified before proof execution unless explicitly needed for setup
artifact path is defined
patched/vulnerable comparison plan is chosen
throwaway admin/member account flow is understood
```

## Later proof objective, not part of this script

If separately authorized later, the proof objective remains marker-only role-boundary/config-write evidence:

```text
unauthenticated request denied
admin baseline succeeds
non-admin member writes lab-owned marker variable on v1.19.1
non-admin denied on separate admin-only control
post-health succeeds
cleanup succeeds
patched v1.19.2 comparison denies non-admin if run
```

Do not claim RCE by default. Do not write secrets, commands, or real deployment variables.
