> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Script Inventory — Operator-Facing Map

Status: active / script-first Phase 4B reset
Date: 2026-05-21
Source: `handoff/phase4b_script_first_architecture_reset_20260521.md`

This file is the practical map of scripts. It intentionally starts from "what can I use?" rather than contract/schema/profile structure.

## Working model

```text
preview + recon results
→ choose existing module bundle if one matches
→ if no bundle fits, choose scripts from this inventory
→ run a small situation-specific script combination
→ review results
→ promote useful combination into a reusable module bundle
→ repeat until report-ready
```

## Script locations

| Location | Meaning |
| --- | --- |
| `scripts/*.sh` | Original practical shell script library. |
| `scripts/*.py` | Python helpers, validators, importers, workflow builders. Some are platform scaffolding, some are usable tools. |
| `scripts/labs/*.sh` | Hand-written lab wave runners for Docker/local vulnerable apps. |
| `scripts/lab_modules/*.py` | Current local-lab-safe bounded adapters. |
| `setting/local/*.sh` / `setting/local/*.py` | Generated or local helper scripts used to execute against lab/Kali. |
| `scripts/kali-browser-ops.ps1` | Windows→Kali GUI/browser control wrapper for noVNC-era work: open URL, browser reset, screenshot, xdotool click/type/hotkey, downloads listing, and Chromium CDP tab metadata/visible text. |
| `scripts/kali-passive-browse.ps1` | End-to-end passive browser helper: start Kali if needed, ensure temporary NAT, start noVNC tunnel, open URL, extract sanitized visible text/gate flags, optionally close NAT after. |
| `scripts/passive_target_search.py` | Offline generator for passive target-search URLs and first-bounty triage templates; no network/browser/target contact. |
| `<artifact-output-dir>/<run_id>/` | Actual execution artifacts pulled back from Kali. |

## Primary practical shell scripts

| Script | Category | Current role | Risk / gate | Notes |
| --- | --- | --- | --- | --- |
| `scripts/headers_audit.sh` | headers | Practical baseline audit | low; scope/lab required | Good candidate for a lightweight `headers_baseline` bundle. |
| `scripts/cors_audit.sh` | headers/CORS | CORS behavior clues | low-to-medium; inert origins only unless approved | Needs safe wrapper/notes for origin choices. |
| `scripts/open_redirect.sh` | redirect | Open redirect triage | medium; bounded canaries only | Do not run broad; Wave2 benign adapter is safer current wrapper. |
| `scripts/xss_finder.sh` | XSS/reflection | Reflection/behavior clues | medium/high; no executable payload by default | Needs benign reflection wrapper before routine use. |
| `scripts/sqli_triage.sh` | injection | SQLi triage | high; run card required | Keep out of fast lane unless explicitly bounded. |
| `scripts/lfi_finder.sh` | file/path | LFI/path traversal clues | high; run card required | Must avoid collecting secrets/PII/loot. |
| `scripts/ssrf_finder.sh` | SSRF | OOB SSRF clues | high/blocked by default | Callback/OAST requires explicit approval. |
| `scripts/jwt_inspect.sh` | auth/token | JWT structure/local inspection | low if local/offline | Useful offline helper; never store real secrets. |
| `scripts/subdomain_recon.sh` | recon | Subdomain and HTTP probing | scope required | Real targets need program scope/rules. |
| `scripts/subdomain_takeover.sh` | recon/takeover | Dangling DNS/takeover clues | scope required; manual verification | Triage only; no takeover. |
| `scripts/kali_audit.sh` | local env | Kali tool/environment inventory | local only | Safe for environment checks. |
| `scripts/setup_kali.sh` | local env | Kali setup | changes environment | Review before running. |
| `scripts/gen_report.sh` | report | Offline report generation from existing scan dir | no target touch | Good report-stage helper. |

## Current lab-safe adapters

| Script | Category | Status | Use when | Output |
| --- | --- | --- | --- | --- |
| `scripts/lab_modules/wave1a_metadata.py` | metadata baseline | usable, bounded lab adapter | Need headers/CORS/known-path/tiny discovery lab baseline | JSON plan or generated bash; JSONL observations after execution. |
| `scripts/lab_modules/phase4b_get_only_metadata_probe.py` | metadata/known paths | usable, bounded lab adapter | Need fixed GET-only check of `/`, robots, security.txt, `/ftp/`, `/api-docs/`, canaries | JSON plan or generated bash; JSONL observations. |
| `scripts/lab_modules/ftp_filename_content_class_verifier.py` | directory listing / A02:2025 misconfiguration | usable, bounded lab adapter | `/ftp/` is already a candidate and filenames need content-class triage without file downloads | JSON plan or generated bash; one JSONL observation with filename classes. |
| `scripts/lab_modules/wave2_benign_params.py` | redirect/reflection | usable, bounded lab adapter | Need inert canary checks for reflection/open-redirect negatives/positives | JSON plan or generated bash; JSONL observations. |
| `scripts/lab_modules/owasp_three_class_probe.py` | A01 access-control / A02 crypto metadata / A10 exceptional-conditions trial | pilot only / superseded for final shape | Historical three-class local-lab trial; keep as workflow stress-test, not final module shape | JSON plan or generated bash; JSONL observations with candidate-only signals. |
| `scripts/lab_modules/single_vuln_module_common.py` | shared helper | usable library for single-vulnerability adapters | Shared plan/render/safety logic for one-vuln modules; do not run directly | Imported by single-vuln adapters. |
| `scripts/lab_modules/lab_access_control_unauth_route_metadata.py` | A01 access-control metadata | active, bounded lab adapter | Need fixed unauthenticated route metadata with auth-gate and SPA-fallback controls | JSON plan or generated bash; JSONL observations + possible_vulnerabilities.md. |
| `scripts/lab_modules/lab_crypto_transport_metadata.py` | A02 crypto/transport metadata | active, bounded lab adapter | Need HTTP/cookie/transport metadata without TLS scanner or credentialed flow | JSON plan or generated bash; JSONL observations + possible_vulnerabilities.md. |
| `scripts/lab_modules/lab_exceptional_condition_metadata.py` | A10:2025 exceptional-condition metadata | active, bounded lab adapter | Need fixed benign malformed/unknown-route error-handling metadata | JSON plan or generated bash; JSONL observations + possible_vulnerabilities.md. |
| `scripts/lab_modules/tool_wrapper_common.py` | mature tool wrapper helper | usable library for local-lab tool wrappers | Shared plan/render/parser/safety logic for ffuf/nikto/nmap-style wrappers; do not run directly | Imported by mature-tool wrapper adapters. |
| `scripts/lab_modules/lab_ffuf_sensitive_path_discovery.py` | A05 security misconfiguration / path discovery | active local-lab tool wrapper | Need bounded ffuf sensitive/admin/metadata path discovery on disposable lab | JSON plan or generated bash; tool raw output + normalized JSONL + possible_vulnerabilities.md. |
| `scripts/lab_modules/lab_nikto_server_misconfig.py` | A05 security misconfiguration / server scan | active local-lab tool wrapper | Need Nikto server/header/default-file misconfiguration leads on disposable lab | JSON plan or generated bash; tool raw output + normalized JSONL + possible_vulnerabilities.md. |
| `scripts/lab_modules/lab_nmap_http_fingerprint.py` | A05 security misconfiguration / service fingerprint | active local-lab tool wrapper | Need bounded single-port nmap HTTP fingerprint/header checks | XML raw output + normalized JSONL + possible_vulnerabilities.md. |
| `scripts/lab_modules/lab_service_baseline_targets.py` | Apache/Tomcat/OpenSSL/HAProxy/Envoy/Traefik service baseline | draft-active local-lab service baseline wrapper | Need bounded baseline probes for common web/API infrastructure service surfaces | HTTP path status/header TSV + OpenSSL/nmap metadata + normalized JSONL + possible_vulnerabilities.md. |
| `scripts/lab_modules/web_exposure_common.py` | shared web exposure helper | usable library for bounded Phase 4B exposure bundles | Shared generator/runner for fixed-path GET probes, root-fallback suppression, candidate-only outputs | Imported by API docs, metrics, and source-map triage adapters. |
| `scripts/lab_modules/lab_api_docs_exposure_triage.py` | A05/API docs exposure | draft-active local-lab exposure wrapper | Need bounded Swagger/OpenAPI/API docs exposure triage | JSONL observations + possible_vulnerabilities.md; references ZAP/nuclei/ffuf/dirsearch as mature tools. |
| `scripts/lab_modules/lab_metrics_exposure_triage.py` | A05/observability exposure | draft-active local-lab exposure wrapper | Need bounded `/metrics`/Prometheus/Actuator exposure triage | JSONL observations + possible_vulnerabilities.md; references promtool/nuclei/ffuf/ZAP. |
| `scripts/lab_modules/lab_source_map_disclosure_triage.py` | A05/A06 client artifact exposure | draft-active local-lab exposure wrapper | Need bounded JavaScript `.map` source-map disclosure triage | JSONL observations + possible_vulnerabilities.md; references Retire.js/SecretFinder/trufflehog/LinkFinder. |
| `scripts/lab_modules/lab_auth_surface_no_bruteforce.py` | A07 auth metadata / A01 access-gate controls | draft-active local-lab wrapper | Need authentication-surface mapping without username/password attempts | JSONL observations + possible_vulnerabilities.md; explicitly excludes hydra/brute force. |
| `scripts/lab_modules/lab_component_metadata_triage.py` | A06 vulnerable/outdated components / A08 dependency provenance | draft-active local-lab wrapper | Need package/version/static component clues before Retire.js/npm/OSV-style manual correlation | JSONL observations + possible_vulnerabilities.md; no CVE claim from version string alone. |
| `scripts/lab_modules/lab_integrity_metadata_triage.py` | A08 software/data integrity metadata | draft-active local-lab wrapper | Need security.txt/robots/service-worker/manifest integrity-policy clues | JSONL observations + possible_vulnerabilities.md; no tampering/destructive integrity tests. |
| `scripts/lab_modules/lab_juice_shop_search_sqli_boolean_probe.py` | A03 injection / SQLi boolean differential | active verified-flow local-lab adapter | Need bounded Juice Shop `/rest/products/search?q=` SQLi behavior proof with baseline/positive/negative controls | JSON plan or generated bash; results.json + classification.json + observations.jsonl + possible_vulnerabilities.md; source-driven from Arjun-style parameter discovery. |
| `setting/local/tool_acquisition/wave1_20260521/tools/sqlmap/sqlmap.py` | A03 injection / SQLi | acquired external mature tool, local-only | Need bounded SQLi learning runs against disposable lab endpoints | sqlmap stdout/session output + candidate-only summary; full tool kept git-ignored under `setting/local/`. |

## Generated/local execution scripts

| Script | Role | Notes |
| --- | --- | --- |
| `setting/local/phase4b_wave1a_remote.sh` | Kali-run Wave1A metadata execution | Generated/runtime artifact. |
| `setting/local/phase4b_owasp_lab_probe.sh` | Earlier OWASP local-lab probe | Contains direct probing logic; partially superseded by bounded adapters. |
| `setting/local/phase4b_get_only_metadata_probe_run.sh` | GET-only metadata probe executable | Current fast-lane runnable script. |
| `setting/local/ftp_filename_content_class_verifier_run.sh` | `/ftp/` filename/content-class executable | Generated from bounded adapter; current `lab_directory_listing_triage` runnable script. |
| `setting/local/wave2_benign_params_run.sh` | Wave2 benign params executable | Current fast-lane runnable script. |
| `setting/local/owasp_three_class_probe_run.sh` | Three-class OWASP trial executable | Historical pilot runner from `owasp_three_class_probe.py`; superseded for final one-vulnerability module shape. |
| `setting/local/lab_access_control_unauth_route_metadata_run.sh` | Access-control metadata executable | Generated from single-vulnerability adapter; current bounded runnable. |
| `setting/local/lab_crypto_transport_metadata_run.sh` | Crypto/transport metadata executable | Generated from single-vulnerability adapter; current bounded runnable. |
| `setting/local/lab_exceptional_condition_metadata_run.sh` | Exceptional-condition metadata executable | Generated from single-vulnerability adapter; current bounded runnable. |
| `setting/local/lab_ffuf_sensitive_path_discovery_run.sh` | ffuf sensitive-path discovery executable | Generated from mature-tool wrapper; current local-lab tool runnable. |
| `setting/local/lab_nikto_server_misconfig_run.sh` | Nikto server misconfiguration executable | Generated from mature-tool wrapper; current local-lab tool runnable. |
| `setting/local/lab_nmap_http_fingerprint_run.sh` | nmap HTTP fingerprint executable | Generated from mature-tool wrapper; current local-lab tool runnable. |
| `setting/local/lab_service_baseline_targets_run.sh` | Apache/Tomcat/OpenSSL/HAProxy/Envoy/Traefik baseline executable | Generated from service baseline wrapper; bounded local-lab service metadata runnable. |
| `setting/local/lab_api_docs_exposure_triage_run.sh` | API docs exposure executable | Generated from bounded web exposure wrapper; local-lab candidate-only API docs triage. |
| `setting/local/lab_metrics_exposure_triage_run.sh` | Metrics exposure executable | Generated from bounded web exposure wrapper; local-lab candidate-only metrics triage. |
| `setting/local/lab_source_map_disclosure_triage_run.sh` | Source-map disclosure executable | Generated from bounded web exposure wrapper; local-lab candidate-only source-map triage. |
| `setting/local/lab_auth_surface_no_bruteforce_run.sh` | Auth-surface metadata executable | Generated from bounded web exposure wrapper; local-lab no-bruteforce auth-surface triage. |
| `setting/local/lab_component_metadata_triage_run.sh` | Component metadata executable | Generated from bounded web exposure wrapper; local-lab package/version/static component clue triage. |
| `setting/local/lab_integrity_metadata_triage_run.sh` | Integrity metadata executable | Generated from bounded web exposure wrapper; local-lab security/integrity metadata triage. |
| `scripts/labs/webgoat_docker_wave1.sh` | WebGoat Docker baseline wave | Confirms WebGoat/WebWolf surfaces from aggressive-lab to victim Docker host; valuable target-readiness baseline. |
| `scripts/labs/webgoat_authenticated_wave2.sh` | WebGoat authenticated wave | Registers throwaway users, captures session evidence, enumerates lesson menu, and seeds bounded WebGoat lesson proof work; first manual follow-up verified IDOR. |
| `scripts/labs/webgoat_jwt_wave3.sh` | WebGoat JWT/token wave | Registers throwaway user, fetches JWT lesson/JS, extracts endpoints, verifies bounded JWT decode assignment, and stores offline decoded-token artifacts. |
| `scripts/labs/webgoat_browser_runtime_xss_wave1.sh` | WebGoat browser runtime XSS wave | Registers throwaway user, drives Chromium/CDP via `scripts/labs/cdp_runtime_xss.py`, validates a safe DOM marker in WebGoat origin/path, and preserves positive/control browser artifacts. |
| `scripts/labs/cdp_runtime_xss.py` | Browser/CDP helper | Minimal Chrome DevTools Protocol helper for local-lab runtime XSS marker verification when Playwright is broken/missing; not a standalone scanner. |
| `scripts/labs/webgoat_pathtraversal_file_read_wave1.sh` | WebGoat path traversal retrieval attempt | Attempts WebGoat random-picture safe-marker retrieval with raw/encoded traversal controls; currently valuable attempted-not-verified because Tomcat/app rejected encoded traversal while lesson hash submission succeeded. |
| `scripts/labs/webgoat_pathtraversal_upload_write_wave1.sh` | WebGoat path traversal upload write | Registers throwaway user, posts marker image with traversal in `fullName`, verifies bounded lab file-write lesson completion, and preserves control/traversal evidence. |
| `scripts/labs/webgoat_zipslip_overwrite_wave1.sh` | WebGoat Zip Slip overwrite | Builds a zip with a traversal entry for a throwaway profile image, uploads to WebGoat Zip Slip lesson, verifies bounded overwrite success, and preserves zip/response artifacts. |
| `scripts/labs/modern_api_xxe_safe_marker_wave1.sh` | Modern API XXE safe-marker proof | Dedicated one-vulnerability runner for lab-owned marker XXE/file-entity proof with no-entity and wrong-file controls, pre/post health, and verified-impact lab-only verdict. |
| `scripts/labs/modern_api_path_traversal_file_read_wave1.sh` | Modern API path traversal file-read safe-marker proof | Starts a disposable victim-side `modern_vuln_api` container, verifies public-file and missing-file controls, reads only a lab-owned marker via `../` traversal, records pre/post health, and cleans the target. |
| `scripts/labs/modern_api_auth_role_separation_wave1.sh` | Modern API auth/session role-separation proof | Starts a disposable local `modern_vuln_api` target by default, logs in normal/admin users, verifies unauth/admin/normal-user controls, proves normal-user access to an admin audit marker, and emits `verified_role_separation_bypass_lab_only` only when all role controls pass. |
| `scripts/labs/operator_ssrf_true_callback_run.sh` | Modern API SSRF true attacker callback operator-run proof | Manual Kali-side run script for the safety-layer-denied SSRF trigger. Uses Docker-published listener/target on `0.0.0.0`, health retries, listener precheck, exact human confirmation string, exactly one trigger, diagnostics, and cleanup. Supports `--precheck-only` to verify route without sending the SSRF trigger. |
| `scripts/labs/operator_deser_bounded_marker_run.sh` | Modern API deserialization bounded-marker operator-run proof | Manual Kali-side run script for the safety-layer-denied dedicated pickle marker trigger. Starts the victim target, verifies health, sends an invalid/control request, requires exact human confirmation, sends exactly one marker-only trigger, checks `/deser-log`, cleans up, and supports `--precheck-only` with no positive trigger. |
| `scripts/labs/arcane_global_variables_bootstrap_precheck.sh` | Arcane <specific-ghsa-id> bootstrap posture precheck | Fail-closed precheck/render helper for the Phase 5A Arcane local-bootstrap candidate. Creates artifacts, verifies host-only lab assumptions, rejects default host/user Docker socket posture, and can render a review-only disposable Docker-in-Docker compose template. Does not launch Arcane, mount sockets, create accounts, or send proof requests. |
| `scripts/labs/tmp_path_traversal_safe_marker_wave1.sh` | tmp <specific-ghsa-id> path traversal safe-marker proof | Local-lab runner for npm `tmp@0.2.5` prefix traversal. Requires exact local-lab approval, rejects target-like/live flags, creates control and escaped marker files only under a lab-owned artifact directory, and emits `verified_tmp_path_traversal_arbitrary_file_creation_lab_only` when controls pass. |
| `scripts/labs/dvwa_command_injection_impact_wave1.sh` | DVWA command-injection impact wave | Launches/attacks disposable DVWA from aggressive-lab/v2 to victim-lab; proves `www-data` command execution, lab marker file write/readback, and attacker-side callback when used with Docker-published listener (`CALLBACK_URL_OVERRIDE`, `USE_LOCAL_CALLBACK_LISTENER=0`, optional `EXTERNAL_CALLBACK_LOG` for authoritative external callback counts). |
| `setting/local/verified_lab_flow_juice_shop_search_sqli_boolean_run.sh` | Juice Shop search SQLi boolean executable | Generated from `lab_juice_shop_search_sqli_boolean_probe.py`; bounded local-lab proof for `/rest/products/search?q=` with baseline/normal/boolean true/boolean false controls. |
| `setting/local/phase4a_ftp_meta.py` | Earlier `/ftp/` metadata helper | Candidate source for next `/ftp/` verifier. |

| `setting/local/phase4a_redact_manual_verify.py` | Redaction helper | Useful for evidence hygiene without driving workflow. |
| `setting/local/generated_nuclei_ffuf_lab.sh` | Nuclei/ffuf lab spike script | Do not treat as default; needs bundle-specific gate. |

## Suggested module bundles to create next

### `lab_directory_listing_triage`

Trigger:

- preview/recon shows `/ftp/` or similar directory-listing candidate.

Scripts:

1. `scripts/lab_modules/phase4b_get_only_metadata_probe.py`
2. `scripts/lab_modules/ftp_filename_content_class_verifier.py`
3. optional report/evidence packet helper

Goal:

- classify filenames/content types/sizes;
- no bulk downloads;
- no secrets/loot retention;
- produce candidate evidence packet and report rehearsal input.

### `lab_metadata_baseline`

Trigger:

- new lab target or checkpoint needs passive metadata baseline.

Scripts:

1. `scripts/lab_modules/wave1a_metadata.py`
2. `scripts/headers_audit.sh` or equivalent bounded wrapper
3. optional CORS inert-origin wrapper

Goal:

- produce low-risk metadata observations.

### `lab_headers_cors_baseline`

Status: active learning-stage bundle at `modules/bundles/lab_headers_cors_baseline.md`.

Trigger:

- need a quick hardening metadata baseline for HTTP security headers and inert CORS behavior.

Scripts:

1. `scripts/headers_audit.sh`
2. `scripts/cors_audit.sh`

Latest artifacts:

```text
<artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/
```

Goal:

- record security-header hardening candidates;
- record CORS reflection/credential controls;
- keep missing-header wording candidate-only unless chained with concrete impact.

### `lab_service_baseline_targets`

Status: draft-active bundle at `modules/bundles/lab_service_baseline_targets.md`.

Trigger:

- preview/recon suggests Apache, Tomcat, OpenSSL/TLS, HAProxy, Envoy, or Traefik service surface;
- need a bounded infrastructure/service baseline before deeper app testing.

Scripts/tools:

1. `scripts/lab_modules/lab_service_baseline_targets.py`
2. generated `setting/local/lab_service_baseline_targets_run.sh`
3. mature tools when present: `curl`, `openssl`, `nmap`

Goal:

- safely probe default/status/admin/metrics paths and TLS metadata;
- keep output candidate-only;
- avoid credentials, brute force, config exfiltration, and finding promotion.

### `lab_sqli_acquisition_triage`

Status: active learning-stage bundle at `modules/bundles/lab_sqli_acquisition_triage.md`.

Trigger:

- need SQL injection learning/triage against an authorized disposable lab endpoint.

Scripts/tools:

1. acquired sqlmap at `setting/local/tool_acquisition/wave1_20260521/tools/sqlmap/sqlmap.py`
2. optional acquired SQLi wordlists under `setting/local/tool_acquisition/wave1_20260521/wordlists/`

Latest artifacts:

```text
<artifact-output-dir>/phase4b_sqli_acquisition_learning_20260521T105021Z/
```

Goal:

- use mature SQLi tooling first;
- keep output candidate-only;
- treat HTTP 500s as robustness/error-handling leads unless manual evidence proves SQL injection.

### `benign_reflection_redirect_triage`

Status: active bundle at `modules/bundles/benign_reflection_redirect_triage.md`.

Trigger:

- preview/recon suggests redirect endpoints or query reflection possibilities.

Scripts:

1. `scripts/lab_modules/wave2_benign_params.py`
2. only escalate to original `open_redirect.sh` / `xss_finder.sh` after scoped run-card review.

Goal:

- identify obvious no-candidate/candidate states using inert canaries;
- preserve SPA fallback and error-body echo as false-positive controls;
- avoid executable payloads, redirect following, scanners, callbacks, and finding promotion.

## What is intentionally not primary anymore

These remain useful, but should not be the operator-facing entry point:

- `modules/checks/**/module.json`
- `modules/profiles/*.json`
- `scripts/module_runner.py`
- preview manifest / ledger validators
- candidate review contract chain

They are guardrail/report-integrity layers. The practical workflow starts with context, scripts, and bundles.


## Verified exploit-flow rerun wave 1 — 2026-05-21 UTC

Latest artifact: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/`.

Promoted verified-lab-flow bundles:

- `modules/bundles/verified_lab_flow_sqli_auth_bypass_admin_users_read.md` — SQLi login bypass returned an admin lab JWT and enabled `/api/Users` read where unauthenticated control returned 401.
- `modules/bundles/verified_lab_flow_unauth_admin_config_read.md` — unauthenticated `/rest/admin/application-configuration` returned structured configuration JSON.
- `modules/bundles/verified_lab_flow_directory_listing_file_read.md` — `/ftp/` listing plus bounded reads of `legal.md` and `acquisitions.md`.
- `modules/bundles/verified_lab_flow_api_docs_metrics_exposure.md` — Swagger UI/API docs and Prometheus metrics exposed unauthenticated.

Attempted-not-verified / blockers are centralized in `modules/bundles/attempted_not_verified_flows_wave1.md`: missing host tools (`ffuf`, `nikto`, `nmap`, `sqlmap`), source-map fallback controls, CORS/header metadata-only, JWT oracle invalid, coupon route 401, XSS execution not browser-verified.
