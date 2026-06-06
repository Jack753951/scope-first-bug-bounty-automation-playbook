> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Live bounty preview grounding: <program-slug> / auth_session_profile_empty_state
Date: 2026-05-25
Boundary: local reference generation only
No target request, browser automation, scanner, fuzzer, DAST, callback, exploit, workflow execution, or report submission is authorized by this file.
Do not treat this grounding packet as permission to touch the target. It is a preview/reference checklist for later authorized owned-account work.

## Lane snapshot

- Program: `<program-slug>`
- Lane: `auth_session_profile_empty_state`
- Title: Auth/session/profile/workspace empty-state first flow
- Current lane state: `A2_PENDING_OPERATOR_AUTH`
- Current lane status: `blocked_operator_action`
- Autonomy level: `A2`
- Queue priority: `1`
- Program URL: `https://<bug-bounty-platform>.com/<program-slug>`
- Scope file: `programs/<program-slug>/scope.json`
- Dry-run gate: `passed`
- Out-of-scope control: `failed_closed`

## Reference methodology

- OWASP WSTG — use as reference-only methodology for safe manual test design, not as permission to run tools.
- OWASP ASVS — map controls and expected behavior for authentication, session, authorization, and data protection.
- PortSwigger Web Security Academy — use relevant labs as safe reference-only examples of evidence and controls.
- Public disclosed reports and official docs — compare evidence shapes, but do not copy payloads or aggressive techniques.
- Reference-only scanner/template metadata — read class descriptions and expected evidence; do not run scanner templates by default.
- OWASP WSTG-ATHN/WSTG-SESS categories: login/logout, session lifecycle, account-state boundaries, and credential handling expectations.
- ASVS V2/V3/V4 controls: authentication, session management, and access-control expectations for owned accounts.

## Lane-provided preview references

- OWASP WSTG authentication/session management references
- PortSwigger authentication/session/access-control labs as safe reference-only test cases
- <program-redacted> VDP policy metadata requiring <bug-bounty-platform> alias or X-<bug-bounty-platform>-Research header

## Positive controls

- Use only operator-owned / program-authorized account labels such as Account A and Account B.
- Record normal UI/API provenance for any object identifier before making a claim.
- Keep request budget small and capture sanitized method/path/status summaries only.
- Authenticated Account A can view its own profile/workspace empty state after normal login.
- Logout/session-expiry behavior returns the account to unauthenticated or login-required state without exposing owned data.

## Negative controls

- Do not access non-owned data, tenant data, third-party identities, secrets, tokens, or PII.
- Do not use guessed opaque IDs; mark the lane blocked if normal provenance is unavailable.
- Stop on CAPTCHA, OTP, account warning, rate-limit/bot block, policy ambiguity, or unexpected third-party data.
- Unauthenticated requests should not reveal Account A profile/workspace data.
- Session changes should not be forced, fuzzed, or brute-tested beyond normal UI behavior.

## Allowed actions from lane state

- manual_noVNC_signup_login
- normal_UI_login_logout_observation
- owned_account_surface_map
- owned_workspace_empty_state_inventory
- no_finding_or_candidate_closeout

## Blocked techniques

- scanner
- fuzzer
- DAST
- DoS_or_rate_limit_testing
- callbacks_or_webhooks
- third_party_integrations
- workflow_execution
- run_script_testing
- secrets_or_api_key_storage
- cross_tenant_testing
- non_owned_data_access
- public_disclosure
- report_submission
- broad scanning
- credential brute force or password spraying
- payment/KYC/upload/run-script/integration/cross-tenant tests without separate approval

## Stop conditions

- captcha
- otp_or_email_verification
- account_warning_or_bot_block
- unexpected_third_party_data
- policy_or_scope_ambiguity
- candidate_could_be_report_ready
- stronger_technique_needed
- lane_complete_or_exhausted

## Evidence thresholds

- `no_finding`: allowed lane exhausted with meaningful negative controls and no evidence of unauthorized access or impact.
- `candidate`: owned-account evidence suggests a security boundary may fail, but impact/controls/reproducibility still need review.
- `needs_manual_review`: evidence is ambiguous, policy-sensitive, or could become report_ready after human review.
- `blocked_operator_action`: auth/CAPTCHA/OTP/email/phone/local browser or legal/account gate prevents continuation.
- `report_ready`: only after scope, owned-data boundary, positive/negative controls, impact, redaction, duplicate/policy review, and Hermes synthesis all pass; never auto-submit.

## Next safe local action

- Next autonomous action after required gates: `after_operator_identity_gate_prepare_noVNC_surface_map_and_record_redacted_owned_account_empty_state_evidence`
- Next operator gate: `complete <bug-bounty-platform>-alias signup/login in Kali/noVNC or choose proxy/header strategy before target-touching`
- Operator gates still recorded:
  - choose_or_complete_researcher_identity_strategy
  - complete_HackerOne_alias_signup_login_or_proxy_header_setup
  - handle_CAPTCHA_OTP_email_phone_prompts_locally

## Artifact routing

- dry_run_packet: handoff/tines_automation_vdp_phase5a_dry_run_packet_20260525.md
- evidence_dir: handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state
- latest_evidence: handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_seed_20260525.json

## Classification guardrails

- Use `surface_only`, `blocked_operator_action`, `needs_second_account`, `candidate`, `needs_manual_review`, `no_finding`, or `report_ready` only with the evidence thresholds above.
- Do not use unreviewed promotional labels that imply verified/reportable status before review.
- Redact tokens, cookies, emails, phone numbers, OTPs, and non-owned data before evidence promotion.
