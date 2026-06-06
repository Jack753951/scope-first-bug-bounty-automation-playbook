> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Module / Bundle distinction direction

Status: accepted operator direction
Date: 2026-05-21
Route/tool: Hermes synthesis after operator confirmation
Runtime/model visibility: parent Hermes model visible as gpt-5.5 / openai-codex

## Accepted distinction

The project should keep `module` and `bundle` as related but distinct layers:

```text
script/tool -> bundle -> module
```

## Script / tool

A script or tool is the concrete executable capability.

Examples:

- `scripts/headers_audit.sh`
- `scripts/cors_audit.sh`
- `scripts/lab_modules/lab_nmap_http_fingerprint.py`
- `scripts/lab_modules/lab_nikto_server_misconfig.py`
- `ffuf`
- `nikto`
- `nmap`
- `sqlmap`
- `openssl s_client`
- `testssl.sh`

Use scripts/tools to learn, spike, and collect candidate-only lab observations.

## Bundle

A bundle is the operator-facing tactical workflow: a lightweight, human-readable, context-driven combination of scripts/tools.

Bundles live under:

```text
modules/bundles/*.md
```

Each bundle should answer:

1. When should I use it?
2. Which scripts/tools does it run, and in what order?
3. What inputs are required?
4. Where are outputs/artifacts written?
5. How do I distinguish candidate signals from controls, false positives, and missing evidence?

Bundles are the default Phase 4B learning/lab unit. They should stay short, practical, and script-first.

## Module

A module is the platform-facing stable capability: machine-readable, schema/policy/runner/report aware, and suitable for formal automation gates.

Modules currently live under:

```text
modules/checks/**/module.json
```

A module declares items such as:

- `schema_version`
- `module_id`
- `risk_level`
- `target_types`
- `technique_tags`
- `execution`
- `output_contracts`
- `safety_gates`
- `references`

Promote a bundle to a module only when the bundle has stable behavior, clear false-positive controls, stable output shape, candidate-only semantics, and a real need for runner/policy/report integration or authorized-assessment reuse.

## Naming convention

Bundle names can be operator/service specific:

- `lab_apache_httpd_baseline`
- `lab_tomcat_baseline`
- `lab_openssl_tls_baseline`
- `lab_haproxy_baseline`
- `lab_envoy_baseline`
- `lab_traefik_baseline`

Module names should be taxonomy/platform oriented:

- `level1.http_server_fingerprint`
- `level1.tls_metadata_baseline`
- `level1.reverse_proxy_metadata`
- `level1.management_surface_metadata`
- `level1.security_headers_baseline`

## Operating rule

Do not start new Phase 4B work by creating `module.json` unless the operator explicitly asks for platform promotion or authorized-assessment integration.

Default workflow:

1. run/learn with scripts and mature tools in the authorized local lab;
2. record safe artifacts and candidate-only observations;
3. turn useful combinations into bundles;
4. only later promote stable bundles into formal modules.

## Safety boundary

This direction does not authorize public target activation, real bug-bounty execution, credential theft, exfiltration, malware, stealth persistence, uncontrolled destructive behavior, automatic finding confirmation, or report submission.
