> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API Auth/Session Role-Separation Wave 1

Status: completed / verified_role_separation_bypass_lab_only
Date: 2026-05-23
Source: Hermes local disposable-lab run
Route/tool: Windows Hermes control plane running local source-controlled disposable target + bounded curl runner
Artifacts: `<artifact-output-dir>/modern_api_auth_role_separation_20260523T124050Z/`
Script: `scripts/labs/modern_api_auth_role_separation_wave1.sh`
Target fixture: `labs/modern_vuln_api/modern_vuln_api.py`

## Purpose

This is the Phase 4 ability-gap proof wave for real-target-style auth/session role separation. The goal was not to add another generic IDOR count, but to train the project on a bug-bounty-relevant evidence shape:

- two roles/sessions (`alice` normal user and `admin` admin user);
- unauthenticated control;
- normal-user access to an admin-only data surface;
- separate secure admin endpoint as false-positive/control boundary;
- lab-owned marker data only;
- report-readiness wording that does not overclaim beyond the fixture.

## Target change

Added two admin-path surfaces to `labs/modern_vuln_api/modern_vuln_api.py`:

1. `/api/admin/audit-log`
   - Intentional role-separation flaw.
   - Requires authentication but misses the admin-role check.
   - Returns lab-owned marker `ADMIN_AUDIT_MARKER_HERMES_LOCAL_LAB` even to normal user `alice`.

2. `/api/admin/settings`
   - Secure role-control endpoint.
   - Unauthenticated requests get 401.
   - Normal user gets 403.
   - Admin gets 200 with `ADMIN_SETTINGS_CONTROL_HERMES_LOCAL_LAB`.

## Evidence

Final verified run:

```text
<artifact-output-dir>/modern_api_auth_role_separation_20260523T124050Z/
```

`summary_values.json` records:

```json
{
  "admin_audit_marker_found": true,
  "admin_settings_control_marker_found": true,
  "alice_audit_marker_found": true,
  "alice_audit_requested_role": "user",
  "alice_settings_control_error": "admin role required",
  "statuses": {
    "admin_audit": "200",
    "admin_settings_control": "200",
    "alice_audit": "200",
    "alice_me": "200",
    "alice_settings_control": "403",
    "noauth_audit": "401",
    "post_health": "200"
  },
  "verdict": "verified_role_separation_bypass_lab_only"
}
```

Minimum positive/control evidence met:

- pre-health 200;
- `alice` login/token works;
- `admin` login/token works;
- unauthenticated `/api/admin/audit-log` is 401, so the issue is not public unauthenticated exposure;
- `alice` `/api/me` is 200 and role is normal user;
- `alice` `/api/admin/audit-log` is 200 and includes admin audit marker despite `requested_role=user`;
- `admin` `/api/admin/audit-log` is 200 baseline;
- `alice` `/api/admin/settings` is 403, proving not every admin path is globally open;
- `admin` `/api/admin/settings` is 200 with admin-settings control marker;
- post-health 200.

## Classification

`verified_role_separation_bypass_lab_only`.

This verifies a reusable local-lab proof pattern for auth/session role-separation bypass. It is not a public-target finding and should not be used as a bounty report by itself.

## Boundary

Authorized local disposable lab only. Lab-owned marker data only. No public target, brute force, credential theft, sensitive data, persistence, exfiltration, destructive write, callback/OAST, rate testing, or automatic finding/report promotion.

## Tactical preview answers

1. Maximum safe proof: auth-boundary bypass with role-differential evidence and admin-only marker exposure.
2. Current target fit: `modern_vuln_api` can faithfully demonstrate the proof primitive by adding a source-controlled admin audit surface and a secure admin settings control.
3. Minimum evidence: unauth 401, normal-user session 200, normal-user access to admin audit marker 200, admin baseline 200, normal-user denied on a separate admin control 403, admin control 200, post-health 200.
4. Alternate lanes if blocked: WebGoat IDOR/Access Control role lesson; build a second disposable org/tenant fixture; or defer to Phase 5 authorized live target with provided accounts/roles.
5. Proof-library capability added: multi-role session/authorization-boundary proof packet shape for future live-target dry runs.

## 對專案有什麼幫助

- Fills the Phase 4 ability gap closest to real bug bounty work: multi-account / multi-role authorization proof.
- Moves the proof library beyond single-token IDOR toward reportable role-boundary evidence.
- Provides a reusable safe evidence pattern for Phase 5 live-target dry runs: role matrix, positive/control endpoints, unauth control, separate secure admin control, and honest lab-only classification.
- Helps prevent overclaiming: the proof shows a specific admin audit surface bypass, not universal admin access, RCE, data theft, or real-target impact.

## 新增/更新了什麼

- Updated `labs/modern_vuln_api/modern_vuln_api.py` with role-separation fixture endpoints.
- Added `scripts/labs/modern_api_auth_role_separation_wave1.sh`.
- Added artifacts under `<artifact-output-dir>/modern_api_auth_role_separation_20260523T124050Z/`.
- This handoff records the completed Phase 4 ability-gap proof wave.

## Validation

Executed from repo root:

```text
bash -n scripts/labs/modern_api_auth_role_separation_wave1.sh
python -m py_compile labs/modern_vuln_api/modern_vuln_api.py
scripts/labs/modern_api_auth_role_separation_wave1.sh
```

Final runner output:

```text
OUT=<artifact-output-dir>/modern_api_auth_role_separation_20260523T124050Z
VERDICT=verified_role_separation_bypass_lab_only
```
