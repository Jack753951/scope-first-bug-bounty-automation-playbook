> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B bundle + service-scanner direction note

Status: operator direction captured
Date: 2026-05-21
Route/tool: Hermes synthesis from operator feedback comparing Codex/Claude project evaluations
Runtime/model visibility: parent Hermes model visible as gpt-5.5 / openai-codex; no child model invoked for this note

## Operator signal

The operator agreed that the bundle architecture is valuable and close to the project's existing "module" concept. The operator also highlighted Claude's recommendation to add scanner coverage for six common infrastructure/service surfaces as useful:

- Apache
- Tomcat
- OpenSSL
- HAProxy
- Envoy
- Traefik

## Direction synthesis

The project should keep Phase 4B centered on the script-first context loop:

1. Use `scripts/SCRIPT_INVENTORY.md` as the practical entry point.
2. Use `modules/bundles/` as the reusable script-combination layer.
3. Treat old contracts/profiles/schemas as guardrails for stabilization or real authorized targets, not as the default learning workflow.
4. Keep Hermes in the secretary / intelligence / reviewer / synthesis role rather than letting it expand architecture/process by default.
5. Prioritize practical content growth: command library, service scanner bundles, protocol notes, defense baselines, and candidate-only lab reports.

## Bundle framing

A bundle should answer five operator-facing questions:

1. When should I use it?
2. Which scripts/tools does it run?
3. What inputs are required?
4. Where are outputs/artifacts written?
5. How do I distinguish candidate signals from controls, false positives, or missing evidence?

This should remain lighter than the manifest/profile/schema layer unless the bundle is being promoted into a stable platform module or adapted for an authorized real target.

## Proposed next lane

Recommended next work is a documentation + bounded-wrapper lane, not another governance layer:

1. Create initial `command-library/web.md` and `command-library/recon.md` from the real lab commands already run for ffuf, Nikto, nmap, sqlmap, headers, and CORS.
2. Add or plan six service-specific local-lab scanner bundles:
   - `lab_apache_httpd_baseline`
   - `lab_tomcat_baseline`
   - `lab_openssl_tls_baseline`
   - `lab_haproxy_baseline`
   - `lab_envoy_baseline`
   - `lab_traefik_baseline`
3. For each service bundle, prefer wrapping mature tools safely before custom scanners.
4. Keep output candidate-only and lab/authorized-scope gated.
5. Mark legacy/prototype scanners such as `nginx_rift_scanner.py` unless/until they are routed through the newer scope/policy/bundle pattern.

## Safety boundary

Local-learning-lab can be active/aggressive when recoverable. Authorized-assessment must use strict scope/rules/rate/evidence gates. Offline-research remains parser, fixture, CVE, report, and knowledge-base work only.

No public target activation, credential theft, exfiltration, malware, stealth persistence, automatic finding confirmation, or report submission is authorized by this direction note.
