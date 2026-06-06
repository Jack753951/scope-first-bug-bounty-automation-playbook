> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Realistic SaaS API multi-class local-lab proof — <victim-vm>

Status: verified local-lab methodology
Date: 2026-05-29
Target: `modern-realistic-api` on `<victim-vm>` / `http://<victim-vm>:18080`
Route: Windows Hermes control plane -> `<attacker-vm>` attacker -> `<victim-vm>` Docker target
Artifact root: `<artifact-output-dir>/realistic_saas_api_20260529T063059Z/`

## Boundary

Local lab only. The target is a disposable Docker container running the repo-owned fixture `labs/modern_vuln_api/modern_vuln_api.py` on `<victim-vm>`. All data are synthetic markers. This proof does not authorize live-target testing, report-ready promotion, scanner/fuzzer/DAST use, OAST, credential handling, customer data access, or report submission.

`crAPI` was selected as the closest off-the-shelf real-world API target and most of its images were pulled to the victim VM, but the full compose startup was not reliable in this run. The operational target used for completed proofs is the repo-owned realistic SaaS/API fixture because it gives deterministic owned-data positive/negative controls.

## Installation / runtime

Victim VM:

```text
<victim-vm> <victim-vm>
container: modern-realistic-api
published: <victim-vm>:18080 -> 18080/tcp
health: GET /health -> 200
```

Stop command:

```bash
docker rm -f modern-realistic-api
```

## Verified cases

| Case | Class | Verdict | Evidence |
|---|---|---|---|
| BOLA-001 | BOLA / IDOR object ownership | verified_local | `http/10_bola_own_invoice_control.json`, `http/11_bola_cross_invoice_positive.json` |
| AUTHZ-001 | Broken function-level authorization / role separation | verified_local | `http/20_auth_me_control.json`, `http/21_authz_auditlog_positive.json`, `http/22_authz_admin_settings_negative.json` |
| PATH-001 | Path traversal / arbitrary file read | verified_local | `http/30_path_public_control.json`, `http/31_path_traversal_positive.json` |
| SSRF-001 | SSRF / server-side request primitive | verified_local | `http/42_ssrf_loopback_fetch_positive.json`, `http/43_ssrf_loopback_callback_log.json` |
| XXE-001 | XXE / unsafe XML parser file disclosure | verified_local | `http/50_xxe_positive.json` |
| DESER-001 | Unsafe deserialization / bounded server-side code path | verified_local | `http/60_deser_invalid_control.json`, `http/61_deser_marker_positive.json`, `http/62_deser_log_post.json` |
| UPLOAD-001 | File upload retrieval/content handling | verified_local | `http/70_upload_pdf_control.json`, `http/71_upload_retrieve_positive.json` |
| XSS-001 | Reflected XSS sink discovery | candidate_local | `http/80_xss_reflection_probe.json` |

## Important controls and caveats

- BOLA control: Alice owned invoice `1001` returned normally; Alice also read Bob-owned synthetic invoice `2001` with `BOB_PRIVATE_INVOICE_MARKER`.
- Authz control: Alice could read admin audit metadata, but `/api/admin/settings` still returned 403, proving this was a scoped role-boundary bug shape rather than universal admin bypass.
- Path traversal control: public file read worked; `../hermes_modern_api_file_read_marker.txt` returned only a lab-owned marker.
- SSRF caveat: attacker-host callback to `<attacker-vm>` timed out due lab network posture/firewall. The verified proof uses a safe loopback callback in the target process. Treat this as server-side request primitive evidence, not full external OAST reachability.
- Deserialization proof used a protocol-0 pickle payload that calls the lab-only `record_deser_marker` sink. No shell, persistence, secret read, or arbitrary command was used.
- XSS is sink evidence only; report-ready XSS would require browser-runtime execution proof with safe marker and no cookie/token/keylogging.

## Tactical takeaways

High-value modern bug-bounty lanes should prioritize:

1. BOLA/object ownership across normal user objects before broad scanning.
2. Role-boundary read exposure with a negative control endpoint.
3. File/path handling around imports, uploads, avatars, model files, and export/download routes.
4. Server-side fetch features, webhooks, importers, previewers, and chatbot connectors, with explicit callback/OAST gate before live use.
5. Parser/deserialization/import code paths using marker-only local proofs first.
6. Upload retrieval and public object exposure, especially unauthenticated direct URLs.
7. XSS sink discovery as candidate only until runtime proof exists.

## Live-target prerequisite mapping

Before using any of these tactics on live bounty assets, require exact program scope, owned accounts/objects, allowed request volume, stop-before rules, redacted evidence handling, and operator approval for callbacks/OAST, upload, token, integration, or report-ready steps.

## Validation

- `summary.json` parsed successfully in the runner.
- 7 cases are `verified_local`; 1 case is `candidate_local`.
- `scripts/post-proof-consolidation.sh --type local_lab_verified_proof --artifact labs/proofs/realistic_saas_api_multi_class_kali_victim_20260529.md --dry-run` should be used as the promotion checklist.
