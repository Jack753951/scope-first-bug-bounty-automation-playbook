> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Module / Bundle Distinction and Service Scanner Direction 2026-05-21

Status: active decision
Source: User + Hermes synthesis of Codex/Claude evaluations
Date: 2026-05-21
Repo truth: <user-home> <user-home> <user-home>

## Decision

Keep `module` and `bundle` as related but distinct layers:

```text
script/tool -> bundle -> module
```

## Script / tool

Concrete executable capability used to learn, spike, and collect candidate-only lab observations.

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

## Bundle

A bundle is the operator-facing tactical workflow: lightweight, human-readable, context-driven, and script-first.

Bundles live in repo under:

```text
modules/bundles/*.md
```

Each bundle should answer five questions:

1. When should I use it?
2. Which scripts/tools does it run, and in what order?
3. What inputs are required?
4. Where are outputs/artifacts written?
5. How do I distinguish candidate signals from controls, false positives, and missing evidence?

Bundles are the default Phase 4B learning/lab unit. Keep them practical; do not let governance become the main workflow.

## Module

A module is the platform-facing stable capability: machine-readable, schema/policy/runner/report aware, and suitable for formal automation gates.

Modules currently live in repo under:

```text
modules/checks/**/module.json
```

Promote a bundle to a module only when:

- behavior is stable;
- false-positive controls are clear;
- output shape is stable;
- candidate-only semantics are clear;
- importer/bridge/runner/report integration is actually needed;
- or the workflow is being adapted for authorized-assessment / real target use.

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

## Service scanner direction

The operator agreed that adding service scanner bundles is useful. Prioritize six common infrastructure surfaces:

- Apache
- Tomcat
- OpenSSL / TLS
- HAProxy
- Envoy
- Traefik

Initial implementation should be bundle-first, not `module.json`-first.

Implementation update 2026-05-21:

- Repo now has `scripts/lab_modules/lab_service_baseline_targets.py` as a plan-first/gated local-lab adapter covering all six surfaces in one baseline bundle.
- Repo now has `modules/bundles/lab_service_baseline_targets.md` and generated runner path `setting/local/lab_service_baseline_targets_run.sh`.
- Focused test coverage: `scripts/test_service_baseline_targets.py` verifies six service targets, public-target fail-closed behavior, candidate-only semantics, and generated runner contents.
- This is still a bundle-first learning capability, not a promoted formal `module.json`.

Recommended sequence:

1. Seed `command-library/recon.md` and `command-library/web.md` from real lab commands already run.
2. Create lightweight service baseline bundle skeletons.
3. Implement one low-risk bundle first, preferably `lab_openssl_tls_baseline`, because it can support Apache, HAProxy, Envoy, and Traefik.
4. Promote to formal module only after stable repeated use.

## Lane distinction

Use three lanes:

- `local-learning-lab`: authorized disposable local lab; active/aggressive/destructive learning allowed only when recoverable; output candidate-only.
- `authorized-assessment`: real authorized or bug bounty targets; strict scope/rules/rate/evidence gates.
- `offline-research`: CVE, advisory, parser, fixture, schema, report, and knowledge-base work; no target touch.

## Hermes role boundary

Hermes should act as secretary / intelligence / reviewer / synthesis layer, not as the default source of more governance scaffolding.

Preferred Hermes roles:

- organize daily/weekly progress;
- summarize CVE/advisory with primary sources;
- polish reports professionally;
- check scope and candidate-vs-confirmed language;
- consolidate Cowork/Codex/Claude Code handoffs;
- route durable decisions into repo handoff and Obsidian.

Avoid defaulting to new schemas, review tiers, manifests, or process layers unless the operator explicitly asks or the work is being promoted to real-target/platform automation.

## Safety boundary

This note does not authorize public target activation, real bug bounty execution, credential theft, exfiltration, malware, stealth persistence, uncontrolled destructive behavior, automatic finding confirmation, or report submission.

Related:

- [[Phase 4B Script-first Architecture Reset 2026-05-21]]
- [[OWASP Top 10 Release Coverage and Lab Testing Plan]]
