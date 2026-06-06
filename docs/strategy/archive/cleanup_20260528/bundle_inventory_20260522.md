> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Bundle Inventory — 已 BUNDLE 化漏洞/能力盤點

Generated: 2026-05-22

Scope: `modules/bundles/*.md`（排除 README）。此盤點是 operator-facing map；所有 target-touching bundle 仍受 lab/scope gate 約束。

## Summary

- Total bundle docs: 42
- verified/proved: 16
- draft-active triage: 17
- active/learning: 4
- candidate/backlog: 5

## Capability counts

- API docs / metrics exposure: 3
- API docs/metrics manual verification checklist: 1
- Access control/auth surface metadata: 2
- Attempted/not-verified flow ledger: 1
- Auth/access-control boundary expansion backlog: 1
- Browser XSS runtime probe backlog: 1
- Command Injection / RCE lab impact proof: 2
- Component/version metadata triage: 1
- Crypto/transport metadata: 2
- Deserialization bounded gadget: 1
- Directory listing / file read: 2
- Exceptional-condition/error metadata: 1
- File upload / retrieval validation: 1
- File upload / unrestricted upload marker proof: 1
- Headers/CORS baseline: 1
- IDOR / object ownership access control: 2
- Infrastructure/service baseline: 1
- Infrastructure/service/tool-wrapper baseline: 4
- Integrity/security metadata triage: 1
- JWT/token inspection: 1
- KEV-inspired path traversal/file-read variants backlog: 1
- SQL Injection: 3
- SSRF isolated callback proof: 1
- Source-map disclosure triage: 1
- Source-reviewed wrapper workflow patterns: 1
- Unauthenticated admin/config read: 1
- Upload/retrieval validation backlog: 1
- XSS/reflection runtime proof: 2
- XXE safe marker proof: 1

## Verified/proved vulnerability flows

| Bundle | Capability | Status/lane | Latest artifacts | File |
| --- | --- | --- | --- | --- |
| `verified_lab_flow_api_docs_metrics_exposure` | API docs / metrics exposure | verified-lab-flow / authorized disposable lab only | `` | `modules/bundles/verified_lab_flow_api_docs_metrics_exposure.md` |
| `verified_lab_flow_directory_listing_file_read` | Directory listing / file read | verified-lab-flow / authorized disposable lab only | `` | `modules/bundles/verified_lab_flow_directory_listing_file_read.md` |
| `verified_lab_flow_dvwa_command_injection_container_control` | Command Injection / RCE lab impact proof | verified-impact / local-lab only | `` | `modules/bundles/verified_lab_flow_dvwa_command_injection_container_control.md` |
| `verified_lab_flow_dvwa_command_injection_true_attacker_callback` | Command Injection / RCE lab impact proof | verified-impact / local-lab only | `` | `modules/bundles/verified_lab_flow_dvwa_command_injection_true_attacker_callback.md` |
| `verified_lab_flow_file_upload_marker_pdf` | File upload / unrestricted upload marker proof | verified-lab-flow / authorized local lab / Kali-side state-change evidence | `` | `modules/bundles/verified_lab_flow_file_upload_marker_pdf.md` |
| `verified_lab_flow_juice_shop_search_sqli_boolean` | SQL Injection | active / verified local-lab flow candidate | `<artifact-output-dir>/juice_q_sqli_bounded_wave_20260522T110815Z/` | `modules/bundles/verified_lab_flow_juice_shop_search_sqli_boolean.md` |
| `verified_lab_flow_modern_api_deserialization_bounded_gadget` | Deserialization bounded gadget | verified-impact / authorized local lab / bounded deserialization gadget proof | `` | `modules/bundles/verified_lab_flow_modern_api_deserialization_bounded_gadget.md` |
| `verified_lab_flow_modern_api_idor_object_ownership` | IDOR / object ownership access control | verified-impact / authorized local lab / disposable target | `` | `modules/bundles/verified_lab_flow_modern_api_idor_object_ownership.md` |
| `verified_lab_flow_modern_api_ssrf_isolated_callback` | SSRF isolated callback proof | verified-impact / authorized local lab / disposable target | `` | `modules/bundles/verified_lab_flow_modern_api_ssrf_isolated_callback.md` |
| `verified_lab_flow_modern_api_upload_retrieval` | File upload / retrieval validation | verified-impact / authorized local lab / disposable target | `` | `modules/bundles/verified_lab_flow_modern_api_upload_retrieval.md` |
| `verified_lab_flow_modern_api_xss_runtime_proof` | XSS/reflection runtime proof | verified-impact / authorized local lab / browser runtime proof | `` | `modules/bundles/verified_lab_flow_modern_api_xss_runtime_proof.md` |
| `verified_lab_flow_modern_api_xxe_safe_marker` | XXE safe marker proof | verified-impact / authorized local lab / bounded XXE-style proof | `` | `modules/bundles/verified_lab_flow_modern_api_xxe_safe_marker.md` |
| `verified_lab_flow_sqli_auth_bypass_admin_users_read` | SQL Injection | verified-lab-flow / authorized disposable lab only | `` | `modules/bundles/verified_lab_flow_sqli_auth_bypass_admin_users_read.md` |
| `verified_lab_flow_unauth_admin_config_read` | Unauthenticated admin/config read | verified-lab-flow / authorized disposable lab only | `` | `modules/bundles/verified_lab_flow_unauth_admin_config_read.md` |
| `verified_lab_flow_webgoat_idor_lesson_access_control` | IDOR / object ownership access control | verified-impact / local-lab only | `` | `modules/bundles/verified_lab_flow_webgoat_idor_lesson_access_control.md` |
| `verified_lab_flow_webgoat_jwt_decode_token_inspection` | JWT/token inspection | verified-impact / local-lab only | `` | `modules/bundles/verified_lab_flow_webgoat_jwt_decode_token_inspection.md` |

## Active triage / reusable local-lab bundles

| Bundle | Capability | Maturity | Status/lane | File |
| --- | --- | --- | --- | --- |
| `attempted_not_verified_flows_wave1` | Attempted/not-verified flow ledger | candidate/backlog | attempted-not-verified / blocked-deferred records | `modules/bundles/attempted_not_verified_flows_wave1.md` |
| `benign_reflection_redirect_triage` | XSS/reflection runtime proof | active/learning | active / local-lab bounded bundle | `modules/bundles/benign_reflection_redirect_triage.md` |
| `lab_access_control_unauth_route_metadata` | Access control/auth surface metadata | draft-active triage | active bundle / local-lab bounded / candidate-only | `modules/bundles/lab_access_control_unauth_route_metadata.md` |
| `lab_api_docs_exposure_triage` | API docs / metrics exposure | draft-active triage | draft-active bundle / local-learning-lab / candidate-only | `modules/bundles/lab_api_docs_exposure_triage.md` |
| `lab_api_docs_metrics_manual_verification` | API docs/metrics manual verification checklist | draft-active triage | mini-bundle / manual-verification checklist / candidate-only | `modules/bundles/lab_api_docs_metrics_manual_verification.md` |
| `lab_auth_surface_no_bruteforce` | Access control/auth surface metadata | draft-active triage | draft-active bundle / local-learning-lab / candidate-only | `modules/bundles/lab_auth_surface_no_bruteforce.md` |
| `lab_component_metadata_triage` | Component/version metadata triage | draft-active triage | draft-active bundle / local-learning-lab / candidate-only | `modules/bundles/lab_component_metadata_triage.md` |
| `lab_crypto_transport_metadata` | Crypto/transport metadata | draft-active triage | active bundle / local-lab bounded / candidate-only | `modules/bundles/lab_crypto_transport_metadata.md` |
| `lab_directory_listing_triage` | Directory listing / file read | draft-active triage | active / local-lab bounded bundle | `modules/bundles/lab_directory_listing_triage.md` |
| `lab_exceptional_condition_metadata` | Exceptional-condition/error metadata | draft-active triage | active bundle / local-lab bounded / candidate-only | `modules/bundles/lab_exceptional_condition_metadata.md` |
| `lab_ffuf_sensitive_path_discovery` | Infrastructure/service/tool-wrapper baseline | draft-active triage | active bundle / local-lab tool wrapper / candidate-only | `modules/bundles/lab_ffuf_sensitive_path_discovery.md` |
| `lab_headers_cors_baseline` | Headers/CORS baseline | draft-active triage | active learning-stage bundle | `modules/bundles/lab_headers_cors_baseline.md` |
| `lab_integrity_metadata_triage` | Integrity/security metadata triage | draft-active triage | draft-active bundle / local-learning-lab / candidate-only | `modules/bundles/lab_integrity_metadata_triage.md` |
| `lab_metrics_exposure_triage` | API docs / metrics exposure | draft-active triage | draft-active bundle / local-learning-lab / candidate-only | `modules/bundles/lab_metrics_exposure_triage.md` |
| `lab_nikto_server_misconfig` | Infrastructure/service/tool-wrapper baseline | draft-active triage | active bundle / local-lab tool wrapper / candidate-only | `modules/bundles/lab_nikto_server_misconfig.md` |
| `lab_nmap_http_fingerprint` | Infrastructure/service/tool-wrapper baseline | draft-active triage | active bundle / local-lab tool wrapper / candidate-only | `modules/bundles/lab_nmap_http_fingerprint.md` |
| `lab_service_baseline_targets` | Infrastructure/service baseline | draft-active triage | draft-active bundle / local-learning-lab service baseline / candidate-only | `modules/bundles/lab_service_baseline_targets.md` |
| `lab_source_map_disclosure_triage` | Source-map disclosure triage | draft-active triage | draft-active bundle / local-learning-lab / candidate-only | `modules/bundles/lab_source_map_disclosure_triage.md` |
| `lab_sqli_acquisition_triage` | SQL Injection | draft-active triage | active learning-stage bundle | `modules/bundles/lab_sqli_acquisition_triage.md` |
| `owasp_three_class_trial` | Crypto/transport metadata | active/learning | active trial bundle / local-lab bounded | `modules/bundles/owasp_three_class_trial.md` |
| `source_reviewed_wrapper_wave1_patterns` | Source-reviewed wrapper workflow patterns | active/learning | valuable-candidate / source-reviewed wrapper workflow / local lab verified subflows | `modules/bundles/source_reviewed_wrapper_wave1_patterns.md` |
| `valuable_candidate_auth_access_boundary_expansion` | Auth/access-control boundary expansion backlog | candidate/backlog | valuable-candidate / partial verified access-control workflow | `modules/bundles/valuable_candidate_auth_access_boundary_expansion.md` |
| `valuable_candidate_browser_xss_runtime_probe` | Browser XSS runtime probe backlog | candidate/backlog | valuable-candidate / attempted-not-verified runtime proof | `modules/bundles/valuable_candidate_browser_xss_runtime_probe.md` |
| `valuable_candidate_kev_path_traversal_file_read_variants` | KEV-inspired path traversal/file-read variants backlog | candidate/backlog | valuable-candidate / partial verified impact / Kali-side intel-driven lab workflow | `modules/bundles/valuable_candidate_kev_path_traversal_file_read_variants.md` |
| `valuable_candidate_upload_retrieval_and_validation` | Upload/retrieval validation backlog | candidate/backlog | valuable-candidate / partial verified state-change | `modules/bundles/valuable_candidate_upload_retrieval_and_validation.md` |
| `webgoat_docker_target_baseline` | Infrastructure/service/tool-wrapper baseline | active/learning | valuable-candidate / target-readiness / Docker-backed local lab | `modules/bundles/webgoat_docker_target_baseline.md` |

## Notes

- `verified_lab_flow_*` bundles are the strongest reusable proof flows currently captured, but they are still local-lab/authorized-scope workflows and not public-target automation.
- `lab_*` bundles are mostly bounded adapters/triage wrappers: useful for repeatable observations, but candidate-only until manual review and report-readiness gates.
- `valuable_candidate_*` and `attempted_not_verified_*` are backlog/learning ledgers, not verified vulnerabilities.
- Auto-generated first pass; capability labels were normalized by filename/status/title, so deep semantic review should still happen before using this as a formal coverage matrix.
