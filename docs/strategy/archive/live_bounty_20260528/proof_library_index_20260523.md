> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersec Lab Proof Library Index — 2026-05-23

Status: active navigation / proof-pattern index
Source: Hermes synthesis from bundles, handoffs, accepted changes, and latest SSRF/XXE/WebGoat/DVWA runs
Date: 2026-05-23
Repo truth: `handoff/current_navigation.md`, `handoff/vulnerability_test_inventory_20260523.md`, `modules/bundles/`, `scripts/SCRIPT_INVENTORY.md`, `notes/obsidian_projects/Cybersec Lab.md`
Reviewer route/tool: Hermes local repo synthesis
Visible runtime model: `gpt-5.5 / openai-codex`
Review focus: navigation, evidence quality, next-lane routing

## Purpose

This file is the short proof-library map for the Cybersec Lab. Use it before starting a new vulnerability wave so the next agent/operator can answer:

- Which proof patterns already exist?
- Which bundle/script/handoff should be reused?
- What evidence shape makes the proof credible?
- Which lanes are still candidates or attempted-not-verified?
- What is the next best local-lab learning slice?

This is documentation/navigation only. It does not authorize public targets, new exploitation, scanner runs, VM network changes, credential handling, report submission, or automatic finding promotion.

## Current default route and boundary

- Windows repo root: `<private-workspace>`
- Attacker/tool VM: `<attacker-vm>` / latest host-only evidence `<lab-ip>`
- Victim/target VM: `<victim-vm>` / latest host-only evidence `<lab-ip>`
- Default network posture: host-only; NAT closed except deliberate temporary install/pull windows, followed by close/verify.
- Current learning mode: local authorized recoverable lab only.
- Hard exclusions: public/unknown targets, malware, stealth/persistence/evasion, real credential theft, real exfiltration/loot retention, uncontrolled propagation/DoS outside the lab, metadata endpoint probing unless explicitly scoped, public OAST/tunnels, and automatic report/finding submission.

## Reusable proof patterns — use these first

### 0. Unsafe deserialization bounded marker proof

Use when: a deserialization lane needs a safe local-lab proof of server-side callable invocation without shell, persistence, callback, secrets, or public target behavior.

| Pattern | Status | Target | Bundle / handoff | Artifact root |
|---|---|---|---|---|
| Modern API unsafe deserialization bounded marker | verified-impact lab-only / operator-confirmed dedicated trigger | `modern_vuln_api` on victim Docker | `modules/bundles/verified_lab_flow_modern_api_deserialization_bounded_gadget.md`, `handoff/modern_api_deserialization_bounded_marker_operator_verified_20260523.md`, `handoff/deser_operator_run_card_20260523.md` | `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/` |

Minimum evidence shape:

```text
pre-health 200
invalid/control deserialize request -> 400
unique marker-only payload
positive deserialize request -> 200
/deser-log contains marker and bounded gadget type
post-health 200
cleanup + network posture
```

### 1. True attacker callback evidence

Use when: SSRF, command injection callback, deserialization callback, or any callback-dependent proof needs truthful attacker-side evidence.

Primary verified patterns:

| Pattern | Status | Target | Bundle / handoff | Artifact root |
|---|---|---|---|---|
| SSRF true attacker callback | verified-impact lab-only / operator-confirmed trigger / evidence packet complete | `modern_vuln_api` on victim Docker | `modules/bundles/verified_lab_flow_modern_api_ssrf_isolated_callback.md`, `handoff/modern_api_ssrf_true_attacker_callback_verified_20260523.md`, `handoff/modern_api_ssrf_true_attacker_callback_evidence_packet_20260523.md` | `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/` |
| Command injection true attacker callback | verified-impact lab-only | DVWA | `modules/bundles/verified_lab_flow_dvwa_command_injection_true_attacker_callback.md`, `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md` | `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/` |

Minimum evidence shape:

```text
pre-health 200
unique marker
listener log with marker
truthful callback source/context label
trigger response / status
post-health 200
cleanup + network posture
```

Key lesson:

- If the execution layer blocks the sensitive trigger, do not bypass/retry. Use an operator-run script/run-card with `--precheck-only`, diagnostics, exact confirmation gate, exactly one trigger, and cleanup.

### 2. Browser runtime XSS safe-marker proof

Use when: reflected text or JSON output needs to be upgraded into browser/runtime evidence.

| Pattern | Status | Target | Bundle / handoff | Artifact root |
|---|---|---|---|---|
| WebGoat browser runtime safe-marker | verified local proof pattern / evidence packet complete | WebGoat | `modules/bundles/verified_lab_flow_webgoat_browser_runtime_xss_safe_marker.md`, `handoff/webgoat_browser_runtime_xss_wave1_20260523.md`, `handoff/webgoat_browser_runtime_xss_rerun_20260523.md`, `handoff/webgoat_browser_runtime_xss_evidence_packet_20260523.md` | `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/` |
| modern_vuln_api XSS runtime proof | verified-impact lab-only | `modern_vuln_api` | `modules/bundles/verified_lab_flow_modern_api_xss_runtime_proof.md` | `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/` |

Minimum evidence shape:

```text
origin/path/session label
safe marker payload
browser DOM/console marker evidence
positive artifact
negative/control artifact
screenshot or saved DOM when useful
no cookie/token theft or exfiltration
```

### 3. File read / path traversal / XXE safe-marker proof

Use when: proving file read/write/overwrite without developing bad habits around `/etc/passwd`, secrets, or loot.

| Pattern | Status | Target | Bundle / handoff | Artifact root |
|---|---|---|---|---|
| XXE lab-owned marker read | verified-impact lab-only | `modern_vuln_api` | `modules/bundles/verified_lab_flow_modern_api_xxe_safe_marker.md`, `handoff/modern_api_xxe_safe_marker_wave1_20260523.md` | `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/` |
| Path traversal lab-owned marker read | verified file-read safe-marker lab-only | `modern_vuln_api` | `modules/bundles/verified_lab_flow_modern_api_path_traversal_file_read.md`, `handoff/modern_api_path_traversal_file_read_wave1_20260523.md` | `<artifact-output-dir>/modern_api_path_traversal_file_read_20260523T094352Z/` |
| Path traversal upload write | verified local destructive-lab bounded file write | WebGoat | `modules/bundles/verified_lab_flow_webgoat_pathtraversal_upload_write.md`, `handoff/webgoat_pathtraversal_upload_write_20260523.md` | `<artifact-output-dir>/webgoat_pathtraversal_upload_write_20260523T033108Z/` |
| Zip Slip profile overwrite | verified local destructive-lab bounded overwrite | WebGoat | `modules/bundles/verified_lab_flow_webgoat_zipslip_profile_overwrite.md`, `handoff/webgoat_zipslip_overwrite_20260523.md` | `<artifact-output-dir>/webgoat_zipslip_overwrite_20260523T033158Z/` |
| File listing/read metadata | verified/candidate | Juice Shop | `modules/bundles/verified_lab_flow_directory_listing_file_read.md`, `modules/bundles/valuable_candidate_kev_path_traversal_file_read_variants.md` | see bundle |

Minimum evidence shape:

```text
lab-owned marker provenance
exact request/path/payload summary
positive response or state proof
wrong-path/no-entity/control evidence
post-health
cleanup/recovery
```

### 4. Auth/session/JWT/access-control proof patterns

Use when: the target requires throwaway accounts, lesson/session state, token decoding, or role separation before proof.

| Pattern | Status | Target | Bundle / handoff | Artifact root |
|---|---|---|---|---|
| WebGoat IDOR lesson access control | verified-impact lab-only | WebGoat | `modules/bundles/verified_lab_flow_webgoat_idor_lesson_access_control.md`, `handoff/webgoat_authenticated_wave2_20260522.md` | `<artifact-output-dir>/webgoat_authenticated_wave2_20260522T040820Z/` |
| WebGoat JWT decode/token inspection | verified low-risk proof | WebGoat | `modules/bundles/verified_lab_flow_webgoat_jwt_decode_token_inspection.md`, `handoff/webgoat_jwt_wave3_20260522.md` | see handoff/bundle |
| modern_vuln_api IDOR/object ownership | verified-impact lab-only | `modern_vuln_api` | `modules/bundles/verified_lab_flow_modern_api_idor_object_ownership.md` | `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/` |
| modern_vuln_api auth/session role separation | verified role-separation bypass lab-only | `modern_vuln_api` | `modules/bundles/verified_lab_flow_modern_api_auth_role_separation.md`, `handoff/modern_api_auth_role_separation_wave1_20260523.md` | `<artifact-output-dir>/modern_api_auth_role_separation_20260523T124050Z/` |

Minimum evidence shape:

```text
throwaway users only
session/login artifacts
role/user separation
positive access proof
negative/control user proof
separate secure-role control when claiming role-separation bypass
no credential theft or reuse beyond lab fixtures
```

### 5. Injection and server-side execution proof patterns

| Pattern | Status | Target | Bundle / handoff | Artifact root |
|---|---|---|---|---|
| SQLi boolean/search behavior | verified/candidate methodology | Juice Shop | `modules/bundles/verified_lab_flow_juice_shop_search_sqli_boolean.md`, `handoff/juice_q_sqli_bounded_wave_20260522.md` | see handoff/bundle |
| SQLi auth bypass/admin users read | verified lab flow | Juice Shop | `modules/bundles/verified_lab_flow_sqli_auth_bypass_admin_users_read.md` | see bundle |
| Command injection container control | verified-impact lab-only | DVWA | `modules/bundles/verified_lab_flow_dvwa_command_injection_container_control.md` | see bundle |
| Unsafe deserialization bounded gadget | verified-impact lab-only | `modern_vuln_api` | `modules/bundles/verified_lab_flow_modern_api_deserialization_bounded_gadget.md` | `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/` |

Minimum evidence shape:

```text
baseline/positive/negative controls
bounded target and payload
identity or marker evidence for impact claims
post-health
no shell/persistence/secret access unless specifically local-lab bounded and recorded
```

### 6. Upload and exposure triage patterns

| Pattern | Status | Target | Bundle / handoff | Artifact root |
|---|---|---|---|---|
| Upload marker PDF / accepted state-change | verified lab flow / candidate | Juice Shop | `modules/bundles/verified_lab_flow_file_upload_marker_pdf.md`, `modules/bundles/valuable_candidate_upload_retrieval_and_validation.md` | `<artifact-output-dir>/kali_verified_flow_wave2b_20260522T001740Z/` / `<artifact-output-dir>/kali_intel_wave3_20260522T005554Z/` |
| modern_vuln_api upload retrieval | verified-impact lab-only | `modern_vuln_api` | `modules/bundles/verified_lab_flow_modern_api_upload_retrieval.md` | `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/` |
| API docs / metrics exposure | verified/candidate exposure | Juice Shop | `modules/bundles/verified_lab_flow_api_docs_metrics_exposure.md`, `modules/bundles/lab_api_docs_exposure_triage.md`, `modules/bundles/lab_metrics_exposure_triage.md` | see bundles |
| Headers/CORS/service baseline | candidate/hardening metadata | Juice Shop/WebGoat | `modules/bundles/lab_headers_cors_baseline.md`, `lab_ffuf_sensitive_path_discovery.md`, `lab_nikto_server_misconfig.md`, `lab_nmap_http_fingerprint.md`, `lab_service_baseline_targets.md` | see bundles |

Minimum evidence shape:

```text
accepted upload/exposure path
content/type/filename controls
root-body/SPA fallback suppression when applicable
candidate-only wording until impact proof
no raw secrets/bulk downloads
```

## Candidate / attempted-not-verified shelves

Keep these useful, but do not cite them as confirmed impact without fresh verification:

- `modules/bundles/attempted_not_verified_flows_wave1.md`
- `modules/bundles/valuable_candidate_auth_access_boundary_expansion.md`
- `modules/bundles/valuable_candidate_browser_xss_runtime_probe.md`
- `modules/bundles/valuable_candidate_kev_path_traversal_file_read_variants.md`
- `modules/bundles/valuable_candidate_upload_retrieval_and_validation.md`

Use them as source/context for the next wave only after rechecking the current target and adding positive/negative controls.

## Current top next lanes after this cleanup

1. **Dedicated deserialization bounded-marker rerun**
   - Existing modern_vuln_api deserialization is verified, but still lives in a broader `modern_api_wave2` artifact family.
   - Best next proof-quality improvement: create a dedicated one-vulnerability runner with baseline/positive/negative controls, no shell, no persistence, and optional callback only if operator-run gated.

2. **Second safe-marker file-read/path traversal target**
   - Extend the XXE safe-marker pattern to a different local target or a clearer source-controlled path traversal/LFI fixture.
   - Avoid sensitive system files; use lab-owned marker only.

3. **Auth/session role-separation or report-readiness rehearsal**
   - Browser-runtime XSS packet hardening is now complete for WebGoat.
   - Next best proof-quality slice: rehearse report-readiness across SSRF/DVWA/XSS/file-read packets, or run one bounded auth/session role-separation proof if more local evidence is desired.

Completed consolidation:

- SSRF true-attacker callback evidence packet: `handoff/modern_api_ssrf_true_attacker_callback_evidence_packet_20260523.md`.
- DVWA command-injection callback evidence packet standard: `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md`.
- WebGoat browser-runtime XSS evidence packet: `handoff/webgoat_browser_runtime_xss_evidence_packet_20260523.md`.

## Use order for future agents

Before choosing a new proof wave:

1. Read `handoff/current_navigation.md`.
2. Read this file.
3. Check the matching bundle in `modules/bundles/`.
4. Check `scripts/SCRIPT_INVENTORY.md` for existing runner/script.
5. Check latest `handoff/accepted_changes.md` for freshness.
6. If new script or meaningful bundle optimization is needed, perform OSS/tooling/source reconnaissance first and record `adopt`, `wrap`, `adapt`, `reference-only`, or `write-custom`.
7. Keep target-touching work on `<attacker-vm>`; Windows/Hermes is the control plane.

## What not to do next

- Do not jump to public bug bounty/public targets just because SSRF/XXE/XSS/path traversal are now locally verified.
- Do not add schema/importer/governance work unless it directly improves a proof packet or operator navigation.
- Do not rerun broad scanners when a dedicated proof packet or evidence-quality cleanup is the higher-value next slice.
- Do not turn candidate bundles into confirmed findings without fresh positive/control evidence.
