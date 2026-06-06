> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4B bundle + service-scanner direction

Session signal: the operator reviewed Codex/Claude evaluations and agreed that the lightweight bundle architecture is valuable because it matches the project's practical "module" concept. The correction is that bundles should be the operator-facing workflow layer, while manifests/profiles/schemas remain guardrails for stabilization or real authorized targets.

## Durable workflow lesson

For the disposable local learning lab, prioritize:

1. `scripts/SCRIPT_INVENTORY.md` as the practical entry point.
2. `modules/bundles/` as the reusable script-combination/module layer.
3. Real lab execution notes and command-library pages over new governance/schema layers.
4. Candidate-only observations, manual verification, and report-readiness gates.

Avoid letting Hermes or the platform process expand into more review tiers, schemas, or contracts by default. Hermes should act as secretary/intelligence/reviewer/synthesis support unless the operator explicitly requests architecture work.

## Bundle shape

Each bundle should answer five operator-facing questions:

- When should I use it?
- Which scripts/tools does it run?
- What inputs are required?
- Where are outputs/artifacts written?
- How do I distinguish candidate signals from false positives, controls, and missing evidence?

Promotion path:

- Learning/lab path: `SCRIPT_INVENTORY -> modules/bundles/<bundle>.md -> kali-output artifacts -> possible_vulnerabilities`.
- Stable/real-target path: `bundle -> manifest/profile/schema/policy -> runner/importer/bridge/report gate`.

## Three execution lanes

Use these lanes to avoid over- or under-gating:

1. `local-learning-lab`
   - Disposable local target only.
   - Tools, scanners, fuzzers, and aggressive/destructive tests may be used when recoverable.
   - Output remains candidate-only.

2. `authorized-assessment`
   - Real bug-bounty/client/owned target.
   - Strict scope/rules/rate/evidence gates.
   - No destructive tests, brute force, callbacks, or credential-sensitive behavior unless rules explicitly allow it.

3. `offline-research`
   - CVE/advisory review, parser work, fixtures, schemas, reports, and knowledge-base pages.
   - No target-touching behavior.

## Service scanner bundle backlog

The operator specifically valued adding scanner/baseline bundles for common infrastructure surfaces:

- Apache HTTPD: `lab_apache_httpd_baseline`
- Tomcat: `lab_tomcat_baseline`
- OpenSSL/TLS: `lab_openssl_tls_baseline`
- HAProxy: `lab_haproxy_baseline`
- Envoy: `lab_envoy_baseline`
- Traefik: `lab_traefik_baseline`

Start these as baseline/fingerprint/config-exposure/candidate-only bundles, not exploit scanners. Prefer wrapping mature tools safely before writing custom scanners.

## Recommended next action pattern

Before creating another governance artifact, first ask whether the learning should become:

- a command-library page from real lab commands;
- a lightweight bundle document;
- a bounded adapter under `scripts/lab_modules/`;
- or only later a stable manifest/profile/schema module.

Default to command-library + bundle for Phase 4B learning work.