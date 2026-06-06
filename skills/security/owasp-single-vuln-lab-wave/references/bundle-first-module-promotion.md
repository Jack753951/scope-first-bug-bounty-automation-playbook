> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Bundle-first module promotion pattern

Use this reference when Phase 4B work risks drifting back into contract-first/platform-governance work before the operator has a practical lab workflow.

## Core distinction

Keep these as related but distinct layers:

```text
script/tool -> bundle -> module
```

- **Script/tool**: concrete executable capability used for learning, spikes, mature-tool wrapping, and candidate-only lab observations.
- **Bundle**: operator-facing tactical workflow. Lightweight Markdown under `modules/bundles/`, answering when to use it, what to run, required inputs, artifact paths, and how to separate candidates from controls/false positives/missing evidence.
- **Module**: platform-facing stable capability. Machine-readable `modules/checks/**/module.json` plus schema/policy/runner/report integration.

## Default Phase 4B rule

Do not begin ordinary local-learning-lab work by creating a new `module.json` or schema/profile layer. Start with scripts/tools and mature wrappers, record safe lab artifacts, then promote useful combinations into bundles. Promote a bundle into a formal module only after behavior, output shape, candidate-only semantics, and false-positive controls are stable, or when authorized-assessment/platform integration requires it.

## Bundle shape

A good bundle answers five operator questions:

1. When should I use it?
2. Which scripts/tools does it run, and in what order?
3. What inputs are required?
4. Where are outputs/artifacts written?
5. How do I distinguish candidate signals from controls, false positives, and missing evidence?

## Naming split

Bundle names may be service/operator-specific:

- `lab_apache_httpd_baseline`
- `lab_tomcat_baseline`
- `lab_openssl_tls_baseline`
- `lab_haproxy_baseline`
- `lab_envoy_baseline`
- `lab_traefik_baseline`

Module names should be taxonomy/platform-oriented:

- `level1.http_server_fingerprint`
- `level1.tls_metadata_baseline`
- `level1.reverse_proxy_metadata`
- `level1.management_surface_metadata`

## Lane split

- `local-learning-lab`: authorized disposable lab; active/aggressive/destructive learning allowed only when recoverable; output remains candidate-only.
- `authorized-assessment`: real authorized or bug-bounty targets; strict scope/rules/rate/evidence gates.
- `offline-research`: CVE, advisory, parser, fixture, report, and knowledge-base work only; no target touch.

## Hermes role boundary

For this class of cybersec lab work, Hermes should act mainly as secretary/intelligence/reviewer/synthesis layer: organize handoff, summarize primary-source intel, polish reports, check scope and candidate-vs-confirmed language, and route decisions into repo/Obsidian. Do not default to adding schemas, review tiers, manifests, or process layers unless the operator asks or the work is being promoted to real-target/platform automation.

## Service scanner direction

Service scanner work should start as lightweight bundles and command-library notes before formal module promotion. Prioritize common infrastructure surfaces: Apache, Tomcat, OpenSSL/TLS, HAProxy, Envoy, and Traefik. Prefer mature-tool wrapping and baseline/fingerprint/candidate-only output before exploit-shaped checks.
