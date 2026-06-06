> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B OWASP 2025 Migration Review Notes

Status: active / offline migration review
Source: Hermes local synthesis from repo handoff, OWASP traceability matrix, and module catalog
Date: 2026-05-21
Repo truth: `modules/owasp_top10_release_traceability_matrix.json`, `modules/OWASP_TOP10_RELEASE_TRACEABILITY_MATRIX.md`, `modules/owasp_top10_lab_module_catalog.json`, `modules/OWASP_TOP10_LAB_MODULE_CATALOG.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`

## Reviewer identity

- Reviewer route/tool: Hermes local tools
- Visible runtime model: gpt-5.5
- Provider / CLI version if visible: openai-codex route exposed by Hermes session; exact lower-level deployment details not exposed
- Review focus: strategy + safety + modularization planning
- Limitation: this is an offline review artifact. No target requests, scanner execution, Kali bridge execution, or live validation were performed for this note.

## Operator intent captured

The operator clarified that the long-term goal must explicitly include automation: collect recent and historical OWASP Top 10 vulnerability categories, synthesize them into a coherent testing plan, test scripts in a controlled lab, and modularize successful checks so the project can call them on demand later.

This note updates Phase 4B interpretation accordingly:

```text
Phase 4B is building the OWASP Top 10 modular local-lab check library and review workflow that future authorized bug-bounty automation can call safely.
```

## Safety boundary for this slice

Allowed now:

- offline OWASP 2025-to-2021 mapping review;
- module/checklist alias planning;
- script modularization roadmap;
- attack/victim lab engineering-detail preservation check;
- repo handoff and Obsidian navigation updates.

Not authorized by this note:

- target interaction;
- scanner execution;
- Kali bridge execution;
- Juice Shop requests;
- public or real bug-bounty target activation;
- schema/runtime/report promotion;
- exploit chains, brute force, credential attacks, OAST/callbacks, proxy/pivot/tunnel behavior, destructive behavior, loot collection;
- automatic `confirmed`, `verified`, `reportable`, `accepted`, or `submitted` promotion.

## Current source state

The project already tracks all official OWASP Top 10 web-application release editions, not fake annual lists:

```text
2003, 2004, 2007, 2010, 2013, 2017, 2021, 2025
```

The current implemented runtime/module taxonomy remains OWASP Top 10 2021. OWASP Top 10 2025 is the latest observed release and is tracked in the traceability matrix, but runtime migration remains pending until reviewed and implemented as a separate safe slice.

## 2025 migration classification

### 2025 categories that can reuse existing 2021 module behavior with aliases

These can likely keep the same underlying module/checklist behavior while adding 2025 labels and reporting aliases. This is catalog/metadata work first; it does not authorize runtime execution.

| 2025 category | Current 2021 mapping | Recommended treatment |
|---|---|---|
| A01:2025 Broken Access Control | A01:2021 Broken Access Control | Add 2025 alias to `route_auth_matrix` and `idor_manual_checklist`; keep T0/T3 planning first and T4 only for approved local-lab workflows. |
| A02:2025 Security Misconfiguration | A05:2021 Security Misconfiguration | Add 2025 alias to metadata modules: `directory_listing_metadata`, `robots_securitytxt_metadata`, `api_docs_metadata`, `error_page_metadata`, `cors_metadata`, `security_headers_baseline`. |
| A04:2025 Cryptographic Failures | A02:2021 Cryptographic Failures | Add 2025 alias to passive metadata modules: `security_headers_baseline`, `cookie_flag_metadata`, `tls_metadata_if_https`. |
| A05:2025 Injection | A03:2021 Injection | Add 2025 alias only to planned/fixture/benign-marker modules; do not run exploit payload chains. |
| A06:2025 Insecure Design | A04:2021 Insecure Design | Add documentation/checklist alias; mostly report/readiness/threat-model checks. |
| A07:2025 Authentication Failures | A07:2021 Identification and Authentication Failures | Add alias; manual checklist only by default; no brute force or credential stuffing. |
| A08:2025 Software or Data Integrity Failures | A08:2021 Software and Data Integrity Failures | Add alias to `lockfile_metadata`, `integrity_header_metadata`, and checklist-only dependency chain review. |
| A09:2025 Security Logging and Alerting Failures | A09:2021 Security Logging and Monitoring Failures | Add documentation-only label update from monitoring to alerting; keep T0/T1 evidence/logging checklist. |

### 2025 categories that need new checklist-only planning before any module runtime

| 2025 category | Why not direct runtime yet | Safe next artifact |
|---|---|---|
| A03:2025 Software Supply Chain Failures | This is broader than 2021 A06/A08 and can tempt dependency download, SBOM ingestion, registry/API calls, or sensitive artifact collection. | Create a checklist-only supply-chain module plan covering dependency-manifest presence, lockfile hygiene, package-source provenance, update-path notes, and explicit no-download/no-token rules. |
| A10:2025 Mishandling of Exceptional Conditions | Mapping confidence is low and runtime testing can drift toward DoS, forced errors, crash induction, or noisy log/event abuse. | Create a checklist-only exceptional-condition handling review: safe error-page metadata, bounded status-code observation, evidence/logging questions, and explicit DoS/crash/fuzz blocks. |

## Script modularization interpretation

The operator's desired capability is valid, but the safe path is staged:

```text
collect / classify scripts
→ map each script to OWASP category + risk tier
→ create module manifest or checklist stub
→ write bounded local-lab run card
→ independent safety review
→ local-lab execution only when explicitly approved
→ import observations as candidate-only
→ manual verification / review chain
→ modular callable ability behind policy gates
```

Existing Phase 4B Wave 1A already proves this path for low-risk metadata checks:

- `headers_audit.sh`-style behavior becomes `security_headers_baseline` / metadata observation;
- CORS behavior becomes `cors_metadata` and remains candidate/non-finding unless credentials/exploitability are separately verified;
- known-path checks become `directory_listing_metadata`, `robots_securitytxt_metadata`, `api_docs_metadata`, `dependency_manifest_metadata`;
- adapter/importer/review-chain exists for Wave1A and remains observation/candidate-only.

For higher-risk scripts, the correct next state is not direct execution. It is a module candidate plus blocked/runtime-tier label:

| Script / technique class | Likely OWASP mapping | Current treatment |
|---|---|---|
| open redirect / reflected parameter checks | A03:2021 / A05:2025 Injection-adjacent, sometimes design/access-control context | Deferred Wave 2. Requires bounded benign-marker adapter, fixed local-lab URL set, request cap, tests, T3/T4 review, and explicit approval. |
| XSS reflection checks | A03:2021 / A05:2025 Injection | Deferred. Benign inert canaries only; no browser exploit chains or payload libraries. |
| SQLi triage | A03:2021 / A05:2025 Injection | Deferred. Metadata/error-based candidate planning only; no sqlmap or exploit payloads without T4 local-lab run card. |
| LFI checks | A01/A05/A03 depending behavior | Block direct secret-file reads; only checklist/synthetic fixture planning unless a safe lab-specific run card exists. |
| SSRF checks | A10:2021 and possible 2025 exceptional-condition/design links | Block callbacks/OAST/pivot by default; sink inventory/checklist only. |
| Auth checks | A07:2021 / A07:2025 | Manual checklist only; no brute force/credential stuffing. |
| Supply-chain checks | A06/A08:2021 / A03:2025 | Metadata/checklist only; no dependency download or tokenized registry access by default. |

## Attack/victim engineering-detail preservation check

The global Hermes memory compaction did not delete the engineering details. It intentionally moved project-specific operational truth out of global memory and into repo/Obsidian authority layers.

Current verified repo-local locations for attack/victim engineering details:

- `handoff/kali_tool_lab_default.md`
  - Kali default tool-lab rule;
  - Kali VM IP `<lab-ip>`;
  - SSH user `kali`, port `22`;
  - Windows SSH config BOM caveat and `ssh -F /dev/null` workaround;
  - standard pattern: Windows coordinates, Kali runs target-touching security tooling.

- `handoff/phase4a_isolated_aggressive_lab_gate_status_20260521.md`
  - attacker clone `<attacker-vm>`;
  - victim VM `<victim-vm>`;
  - host-only network posture;
  - attacker IP `<lab-ip>` and no default route observed;
  - victim IP `<lab-ip>`;
  - Juice Shop health check `http://<lab-ip>:3000/` returned HTTP 200;
  - attacker snapshot `clean-before-aggressive-tests-20260521-093233`;
  - victim snapshots `setup-complete-with-tools` and `pre-aggressive-current-running-recovery-20260521-093252`;
  - no public/client/bug-bounty targets authorized by that gate.

- `handoff/accepted_changes.md`
  - records the Phase 4A/4B lab setup and Wave 1A execution history;
  - records that `<attacker-vm>` was host-only hardened, shared folder removed, clipboard/drag-and-drop disabled, and local Juice Shop health was checked;
  - records Wave 1A route: Hermes -> `scripts/kali-run.ps1` -> `<attacker-vm>`, output under `<artifact-output-dir>/phase4b_wave1a_20260521T030959Z/`.

- `scripts/kali-run.ps1`, `scripts/kali-check-tools.ps1`, `scripts/kali-install-key.ps1`, `scripts/kali-pull.ps1`
  - operational helper scripts for Kali bridge/workflow.

Conclusion: global long-term memory no longer stores these raw operational details by design, but the details are still present in project-local handoff files. Future agents should consult those repo-local files before touching Kali/victim/lab workflow.

## Decision

Proceed with the automation-oriented Phase 4B path, but keep the next implementation slice offline/catalog-only:

1. Add 2025 alias fields or alias documentation to the OWASP module catalog.
2. Add a script-to-module classification table that marks each script as:
   - callable now only as offline/planning;
   - callable in local lab after run card and approval;
   - blocked until a higher-risk review.
3. Do not execute Wave 2 probes yet.
4. Do not change `config/scope.txt`, schema contracts, report submission surfaces, or real-target automation.

## Next recommended slice

`phase4b_owasp_2025_alias_catalog_and_script_matrix`

Type: T1/T2 documentation + JSON catalog update only.

Expected files:

- update `modules/owasp_top10_lab_module_catalog.json` with 2025 alias metadata;
- update `modules/OWASP_TOP10_LAB_MODULE_CATALOG.md` with a 2025 alias table;
- add or update a script/module matrix artifact, likely under `handoff/phase4b_owasp_script_inventory_20260521.json` or a new Markdown companion;
- update `handoff/active_strategy_queue.md` and Obsidian Active Projects.

Explicitly not included:

- target interaction;
- scanner execution;
- Kali bridge run;
- Wave 2 probe execution;
- schema/runtime/report promotion;
- real bug-bounty activation.
