> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_unauth_admin_config_read

Status: verified-lab-flow / authorized disposable lab only
Date: 2026-05-21 UTC
Target: http://<lab-ip>:3000/
Run artifact: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/manual/`

## Preconditions

- Scope confirmed by `config/scope.txt`: `<lab-ip>/16` covers the lab target.
- No authentication cookie, token, or credentials used.
- Target health before and after wave: HTTP 200 on `/`.

## Verified exploit-flow

```bash
curl -sS -D admin_config_headers.txt -o admin_config_body.json \
  http://<lab-ip>:3000/rest/admin/application-configuration
```

## Evidence

- `admin_config_status.txt`: HTTP 200 `application/json`, 23513 bytes.
- `admin_config_evidence.txt`: SHA-256 `eb1bb4f3c404ff4ddfaa6ebc207b22f0dd78c2e7911a53eda17af3eb00894ef5`; JSON top-level key `config`; nested keys include `server`, `application`, `challenges`, `hackingInstructor`, `products`, `memories`, `ctf`.
- The retained snippet shows application/server configuration metadata, not just an SPA fallback.

## Impact level

Medium in the lab: unauthenticated route exposes detailed application configuration and challenge metadata. It is a concrete unauthorized data read, not merely route metadata.

## False-positive controls

- Direct request without auth returned structured JSON and a large non-root body.
- Evidence records body hash, byte count, and parsed keys.
- No lab secrets or real credentials were exfiltrated; snippet is bounded and local.

## Cleanup / recovery

No state change. Post-run health remained HTTP 200.

## Real-target migration limits

Public/real target use is not authorized from this bundle. A real assessment would require explicit scope/rules and data-minimization/redaction before retaining configuration evidence.
