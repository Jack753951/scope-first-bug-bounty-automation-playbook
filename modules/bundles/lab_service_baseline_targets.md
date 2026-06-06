> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_service_baseline_targets

Status: draft-active bundle / local-learning-lab service baseline / candidate-only
Date: 2026-05-21
Adapter: `scripts/lab_modules/lab_service_baseline_targets.py`
Generated runner: `setting/local/lab_service_baseline_targets_run.sh`

## Scope

This bundle adds bounded baseline probes for six common web/API infrastructure surfaces:

- Apache httpd
- Tomcat
- OpenSSL / TLS
- HAProxy
- Envoy
- Traefik

Primary behavior:

```text
A05:2021 Security Misconfiguration — service/admin/default/status/metrics surface metadata
A02:2021 Cryptographic Failures — TLS/certificate/protocol metadata
A06:2021 Vulnerable and Outdated Components — version/outdatedness leads only
```

This is not an exploit scanner and does not attempt credentials, brute force, config exfiltration, callbacks, or finding promotion.

## OSS/tooling decision

Decision: `wrap`

Considered:

- `curl` for bounded status/header/path probes
- `openssl s_client` for TLS handshake/certificate metadata
- `nmap` HTTP/TLS NSE scripts for service metadata
- `testssl.sh`, `sslyze`, `whatweb`, `nikto`, and allowlisted `nuclei` templates as later bundle-specific improvements

Reason:

The first retained capability should be a low-impact service baseline that uses mature tools already common on Kali and produces candidate-only observations. Deeper service-specific scanners can be split into separate bundles after this baseline is useful.

## Use when

Use this bundle when preview/recon suggests one of these infrastructure/service layers may be present, or when a local lab target needs service baseline coverage before deeper app testing.

Examples:

- `Server` header hints Apache, Tomcat, Envoy, Traefik, or HAProxy.
- A reverse proxy/load balancer/ingress may sit in <program-name> of the app.
- TLS/certificate/protocol metadata should be captured as candidate-only crypto posture context.
- A lab target may expose default/status/metrics/admin surfaces.

## Do not use when

Do not use this bundle for public or third-party targets without separate scope/rules approval. Do not use it to brute force Tomcat manager, dump Envoy config from real systems, retain secrets, or auto-promote scanner output.

## Inputs

Required:

```text
--target <private/local lab URL>
```

Optional:

```text
--output-dir <remote/local artifact dir>
--out-script <generated runner path>
--tool-timeout <10..300 seconds>
--health-timeout <1..15 seconds>
--lab-approved
```

Plan-only example:

```bash
python scripts/lab_modules/lab_service_baseline_targets.py --target http://<lab-ip>:3000/
```

Generate runner example:

```bash
python scripts/lab_modules/lab_service_baseline_targets.py \
  --target http://<lab-ip>:3000/ \
  --lab-approved \
  --out-script setting/local/lab_service_baseline_targets_run.sh \
  --output-dir /tmp/lab_service_baseline_targets
```

## Scripts/tools

1. `scripts/lab_modules/lab_service_baseline_targets.py` — approval-gated generator and plan.
2. Generated bash runner — fixed safe HTTP path probes plus bounded `openssl s_client` and `nmap` metadata runs.
3. Mature tools used when present: `curl`, `openssl`, `nmap`.

## Service probe set

Apache:

```text
/server-status
/server-info
/icons/
/manual/
```

Tomcat:

```text
/manager/html
/host-manager/html
/docs/
/examples/
```

OpenSSL / TLS:

```text
openssl s_client -connect <host>:<port> -servername <host> -showcerts
nmap --script ssl-cert,ssl-enum-ciphers
```

HAProxy:

```text
/haproxy?stats
/haproxy_stats
/stats
/;csv
```

Envoy:

```text
:9901/server_info
:9901/config_dump
:9901/stats
/stats/prometheus
```

Traefik:

```text
/dashboard/
/api/rawdata
/api/http/routers
/metrics
```

## Outputs

Expected artifacts:

```text
observations.jsonl
possible_vulnerabilities.md
health.txt
summary.txt
http_probe_results.tsv
root_body.sha256
openssl_s_client.txt
tool_stdout.txt
tool_stderr.txt
tool_raw.xml
artifact_manifest.txt
```

## Review

Candidate signals:

- management/status/default/metrics/dashboard path returns 200/204/redirect;
- TLS/certificate/protocol metadata exists and needs crypto review;
- server/proxy/app-server metadata appears in headers or nmap scripts.

Controls / likely non-findings:

- 404 on service-specific paths;
- 401/403 indicating access control exists, unless the mere exposed surface matters in context;
- generic SPA/router fallback where a service-specific path returns the same body hash as `/`;
- generic SPA fallback;
- plaintext HTTP port producing OpenSSL `no peer certificate available` / `Cipher is (NONE)`;
- service not detected by this baseline is not proof the service is absent.

Missing evidence before finding language:

- manual verification that the surface belongs to the suspected service;
- redacted reproduction/evidence packet;
- version/outdatedness confirmation from primary sources;
- impact analysis beyond scanner wording;
- report-readiness gate.

## Promotion rule

Keep this as a bundle-first local-learning capability until repeated runs show stable outputs. Promote individual service families into formal modules only when needed, for example:

- `level1.tls_metadata_baseline`
- `level1.http_server_fingerprint`
- `level1.reverse_proxy_metadata`
- `level1.management_surface_metadata`

## Safety semantics

Output remains:

```text
candidate-only / needs_manual_review
```

No public target activation, credential attempts, secret retention, confirmed finding promotion, or report submission is authorized by this bundle.
