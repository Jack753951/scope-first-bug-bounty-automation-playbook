> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_api_docs_metrics_exposure

Status: verified-lab-flow / authorized disposable lab only
Date: 2026-05-21 UTC
Target: http://<lab-ip>:3000/
Run artifact: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/manual/`

## Preconditions

- Scope confirmed by `config/scope.txt`: `<lab-ip>/16` covers the lab target.
- No authentication used.
- Target health before and after wave: HTTP 200.

## Verified exploit-flow

```bash
curl -sS -D api-docs_slash_headers.txt -o api-docs_slash_body.txt \
  http://<lab-ip>:3000/api-docs/
curl -sS -D api_docs_swagger_ui_init_js_headers.txt -o api_docs_swagger_ui_init_js_body.txt \
  http://<lab-ip>:3000/api-docs/swagger-ui-init.js
curl -sS -D metrics_headers.txt -o metrics_body.txt \
  http://<lab-ip>:3000/metrics
```

## Evidence

- API docs:
  - `/api-docs` redirects to `/api-docs/`.
  - `/api-docs/` returned HTTP 200 `text/html` and a Swagger UI page.
  - `/api-docs/swagger-ui-init.js` returned HTTP 200 `application/javascript`, 5457 bytes; evidence markers include `swaggerDoc`, `paths`, `openapi`, and `swagger`.
- Metrics:
  - `/metrics` returned HTTP 200 `text/plain; version=0.0.4`, 26028 bytes.
  - `metrics_evidence.txt` includes Prometheus operational counters such as successful/failed upload counters and HTTP request counters by status code.

## Impact level

Medium in the lab: unauthenticated users can view API documentation and operational metrics. Metrics provide concrete operational data, including request volume and error counters, beyond generic metadata.

## False-positive controls

- The exposure triage rerun separately suppressed root-fallback paths for Swagger/source-map/service probes.
- API docs evidence uses `/api-docs/` and `swagger-ui-init.js`, not just the 301 redirect body.
- Metrics are plain-text Prometheus output with concrete counter names and values.

## Cleanup / recovery

No state change. Post-run health remained HTTP 200.

## Real-target migration limits

Do not classify API docs/metrics as reportable on real targets without checking scope, intended exposure, sensitivity, auth expectations, and concrete impact.
