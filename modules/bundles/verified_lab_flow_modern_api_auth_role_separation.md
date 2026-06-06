> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified Lab Flow: Modern API Auth/Session Role-Separation Bypass

Status: active / verified local-lab methodology
Date: 2026-05-23
Handoff: `handoff/modern_api_auth_role_separation_wave1_20260523.md`
Latest artifacts: `<artifact-output-dir>/modern_api_auth_role_separation_20260523T124050Z/`
Runner: `scripts/labs/modern_api_auth_role_separation_wave1.sh`
Target fixture: `labs/modern_vuln_api/modern_vuln_api.py`

## When to use

Use this bundle when the project needs a bug-bounty-relevant authorization proof shape, especially:

- multi-account / multi-role testing;
- normal user vs admin user differential;
- admin-only data exposure;
- false-positive controls showing not every admin endpoint is open;
- Phase 5 live-target dry-run preparation.

Do not use it to claim real-target impact. It is a local-lab methodology bundle.

## Capability added

This bundle proves an auth/session role-separation bypass with:

- unauthenticated control: `/api/admin/audit-log` returns 401 without a token;
- normal-user session: `alice` can authenticate and `/api/me` confirms role `user`;
- vulnerable positive: `alice` can read `/api/admin/audit-log` and receive `ADMIN_AUDIT_MARKER_HERMES_LOCAL_LAB`;
- admin baseline: `admin` can also read `/api/admin/audit-log`;
- secure-control endpoint: `alice` gets 403 for `/api/admin/settings`;
- admin secure-control baseline: `admin` gets 200 with `ADMIN_SETTINGS_CONTROL_HERMES_LOCAL_LAB`;
- post-health stays 200.

## Run

From repo root:

```bash
bash -n scripts/labs/modern_api_auth_role_separation_wave1.sh
python -m py_compile labs/modern_vuln_api/modern_vuln_api.py
scripts/labs/modern_api_auth_role_separation_wave1.sh
```

Default mode starts the disposable target locally on `127.0.0.1:18084` and writes artifacts to:

```text
<artifact-output-dir>/modern_api_auth_role_separation_<timestamp>/
```

To run against an already-started target:

```bash
START_LOCAL=0 TARGET=http://<authorized-lab-target>:<port> scripts/labs/modern_api_auth_role_separation_wave1.sh
```

## Evidence minimum

The verdict may be `verified_role_separation_bypass_lab_only` only if all are true:

```text
noauth_audit = 401
alice_me = 200
alice_audit = 200
alice_audit_marker_found = true
alice_audit_requested_role = user
admin_audit = 200
admin_audit_marker_found = true
alice_settings_control = 403
admin_settings_control = 200
admin_settings_control_marker_found = true
post_health = 200
```

Otherwise classify as `attempted_not_verified`.

## Report-readiness boundary

This is `reusable_methodology`, not a real finding. For an authorized live target, convert it into a report packet only after collecting:

- program/scope authorization;
- two or more legitimate test accounts/roles;
- role/account matrix;
- exact affected endpoint/action;
- normal-user positive access to data/action reserved for another role/tenant;
- negative/secure controls;
- redacted evidence only;
- program-compliant request volume and timing;
- submit/not-submit decision.

## Safety boundary

Authorized local lab only by default. No public target, brute force, credential theft, sensitive data retention, destructive writes, persistence, callbacks/OAST, or automatic finding/report promotion.
