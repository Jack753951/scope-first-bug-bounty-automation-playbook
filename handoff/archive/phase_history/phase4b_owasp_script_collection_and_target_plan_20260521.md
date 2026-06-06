> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B — OWASP Script Collection and Local-Lab Target Plan

Date: 2026-05-21
Target class: local intentionally vulnerable lab only
Current target: `http://<lab-ip>:3000/`
Attacker lab: `<attacker-vm>` / Kali tool bridge
Status: execution plan drafted; broad execution not yet started

## Operator intent

Collect scripts/checks for common OWASP vulnerability classes, use the OWASP Juice Shop victim VM as the target, and modularize useful scripts/checks into the platform.

## Hermes execution interpretation

Use the target aggressively enough to learn, but still in controlled lab waves:

1. Inventory available scripts/tools.
2. Classify each check by OWASP Top 10 and active-testing risk tier.
3. Run low-risk metadata/content-discovery waves first.
4. Refactor existing high-risk scripts before use so they become bounded local-lab modules.
5. Execute one class per run with health checks, request caps, output redaction, and candidate-only semantics.
6. Convert useful outputs into module manifests, run cards, candidate packets, and lab reports.

## Tool/script inventory collected

### Existing project scripts

| Script | OWASP mapping | Current posture | Use decision |
|---|---:|---|---|
| `scripts/headers_audit.sh` | A02/A05 | Low-risk header observation, target-touching via `curl -I` | USE WAVE 1 after local target hard-code/run dir wrapper |
| `scripts/cors_audit.sh` | A05 | Low-risk crafted Origin header checks; CORS `*` is not automatically vuln | USE WAVE 1 with candidate-only language |
| `scripts/open_redirect.sh` | A01/A05 | Sends redirect payloads; benign marker but target-touching | USE WAVE 2 after URL-list allowlist and cap |
| `scripts/xss_finder.sh` | A03 | Injects XSS probes; may invoke dalfox/kxss | REFIT before use; benign canary-only first |
| `scripts/sqli_triage.sh` | A03 | Sends SQLi/time-based probes and optional sqlmap | REFIT before use; disable time payload/sqlmap in first wave |
| `scripts/lfi_finder.sh` | A01/A05 | Attempts file-read payloads and recommends secret reads | DO NOT RUN AS-IS; rewrite to non-secret marker/metadata-only lab module |
| `scripts/ssrf_finder.sh` | A10 | OOB/interactsh callback workflow | DO NOT RUN in current lab phase; callbacks/OAST not authorized |
| `scripts/jwt_inspect.sh` | A02/A07 | likely local token inspection | USE only with synthetic/local tokens; no token harvesting |
| `scripts/nginx_config_audit.sh` | A05 | local config audit | USE only on owned/local config files, not target web probing |
| `scripts/subdomain_recon.sh` | A05/A06 asset recon | public/external enumeration risk | NOT FOR JUICE SHOP lab; defer |
| `scripts/subdomain_takeover.sh` | A05 | public asset takeover checks | NOT FOR JUICE SHOP lab; defer |
| `recon.sh` | multi | guarded recon pipeline | Use only with scope gate and lab-safe intensity |

### Kali tool bridge inventory

Collected by:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-check-tools.ps1'
```

Observed installed tools:

```text
nmap
nikto
sqlmap
gobuster
ffuf
nuclei
masscan
msfconsole
hydra
john
hashcat
burpsuite
```

Observed missing:

```text
zaproxy
```

Use decision:

| Tool | Use in Phase 4B? | Decision |
|---|---:|---|
| `curl` | yes | baseline health, fixed metadata requests |
| `ffuf` | yes | tiny wordlist, low rate, max time, local lab only |
| `gobuster` | yes | alternative tiny directory wordlist only |
| `nuclei` | yes | local custom info/low templates only; no intrusive/fuzz/dos/exploit tags |
| `nikto` | maybe | bounded local lab only, short timeout; output as observation only |
| `nmap` | yes, limited | single known host/port validation only; no broad sweep |
| `sqlmap` | not first | only after T4 run card; risk 1/level 1 max; no dump; no os-shell |
| `burpsuite` | manual assist | human-in-loop verification, not automated attack |
| `masscan` | no | unnecessary/high-volume for one lab host |
| `msfconsole` | no | exploit framework; not needed for OWASP flow now |
| `hydra` | no | brute force prohibited |
| `john`/`hashcat` | no | credential/hash cracking not in web lab flow |
| `zaproxy` | missing | do not install until a separate adapter plan exists |

## Execution waves

### Wave 0 — preflight / target health

Purpose: verify the victim is alive and record baseline.

Allowed actions:

- `GET /` or `HEAD /`
- no recursion
- no payloads

Command pattern:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-run.ps1' -Command 'curl -sS -I --max-time 5 http://<lab-ip>:3000/ | sed -n "1,12p"'
```

Exit gate:

- HTTP 200/3xx acceptable.
- If down/timeout: stop and recover victim before further tests.

### Wave 1 — A05/A02 metadata baseline

Purpose: run low-risk checks that map to the already successful `/ftp/` pattern.

Modules/scripts:

1. `headers_audit.sh`
2. `cors_audit.sh`
3. tiny `ffuf`/`gobuster` content discovery
4. custom local nuclei info template
5. known path metadata list: `/robots.txt`, `/.well-known/security.txt`, `/ftp/`, `/api-docs/`, `/rest/products/search`

Limits:

- max 50 total requests per tool run;
- rate <= 2 req/sec;
- timeout <= 5 seconds;
- no recursive crawling;
- no raw body capture except short redacted snippets;
- no downloads from `/ftp/`.

Expected output:

- JSONL/Markdown observation files under `scans/phase4b_wave1_<timestamp>/`.
- candidate-only states.

### Wave 2 — parameterized benign probes

Purpose: test low-impact parameter handling without exploit chains.

Modules/scripts after refit:

1. `open_redirect.sh` with local marker only and fixed URL list.
2. `xss_finder.sh` in benign reflection-only mode; no dalfox deep payload mode at first.
3. parameter inventory from known Juice Shop routes only.

Limits:

- fixed allowlist URLs only;
- no crawler/gau collection;
- no blind/OOB payloads;
- no credentialed/session tests;
- no payload escalation;
- output says `reflection_candidate` or `redirect_candidate`, not confirmed vuln.

### Wave 3 — controlled injection triage

Purpose: safely calibrate SQLi/injection tooling without service disruption.

Scripts:

- refactored `sqli_triage.sh` variant only.

Changes required before use:

- disable time-based sleep payloads in first run;
- disable `--confirm` / sqlmap;
- use benign syntax-error/differential checks only;
- max 10 candidate URLs;
- no data extraction;
- no dump/table/schema enumeration;
- pre/post health mandatory.

`sqlmap` is deferred until a separate T4 run card explicitly approves a narrow lab-only command such as risk 1/level 1/no dump/no os-shell/no file-read.

### Wave 4 — high-risk classes kept planned/manual

Do not execute these automatically in current Phase 4B:

- SSRF with OAST/interactsh/callbacks.
- LFI attempts that read `/etc/passwd`, source code, private keys, env vars, or config files.
- brute force/auth guessing.
- RCE/deserialization/file upload exploit chains.
- masscan/metasploit/hydra/hash cracking.

For Juice Shop learning, these may become manual walkthrough/checklist items, but not automated target-touching modules yet.

## Modularization plan

Each useful script becomes:

```text
modules/checks/<level>/<module_id>/module.json     # manifest
scripts/lab_modules/<module_id>.py                 # bounded local-lab adapter, if approved
scripts/test_lab_module_<module_id>.py             # tests
handoff/phase4b_run_cards/<module_id>_run_card.md  # script-specific run card
scans/phase4b_<module_id>_<timestamp>/             # runtime output
```

Initial module IDs:

```text
level1.security_headers_baseline       # already exists as offline fixture
level1.directory_listing_metadata
level1.robots_securitytxt_metadata
level1.api_docs_metadata
level1.dependency_manifest_metadata
level1.cors_metadata
level2.open_redirect_candidate
level3.xss_reflection_candidate
level3.sqli_error_candidate
```

## Refactor requirements for old shell scripts

Before existing scripts become modules:

1. Add `--lab-approved` for any target-touching run.
2. Reject targets outside `http://<lab-ip>:3000/` unless a future scope artifact explicitly allows them.
3. Disable external URL collectors like `gau` by default in lab mode.
4. Add request cap and timeout.
5. Write JSONL observations with stable fields.
6. Remove or gate dangerous recommendations such as reading private keys/env files or chaining to RCE.
7. Remove automatic `confirmed` language.
8. Add pre/post health.
9. Add unit tests for unauthorized target rejection and request cap behavior.

## Concrete first run plan

Recommended first executable run after this plan:

```text
Wave 1A: headers + CORS + known-path metadata
```

Execution bundle:

1. pre-health: `curl -I /`
2. run `headers_audit.sh` against root only
3. run `cors_audit.sh` against root and `/rest/products/search` only
4. run bounded known-path metadata script for 5 known paths
5. post-health: `curl -I /`
6. output-side review
7. candidate packet only if evidence warrants it

No XSS/SQLi/LFI/SSRF in first run.

## Run approval boundary

This plan prepares execution but does not by itself authorize every wave. The operator has authorized using the local lab target; Hermes should still execute in waves and stop after each wave for output review before moving to higher-risk classes.

Decision: `READY_FOR_WAVE_1A_LOCAL_LAB_EXECUTION_PLAN`
