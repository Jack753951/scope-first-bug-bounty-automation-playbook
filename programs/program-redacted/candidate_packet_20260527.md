> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-slug> candidate packet — 2026-05-27

Status: NEEDS_OPERATOR_CONTROL before proof execution
Lane: syfe_signup_api_precondition_review

## Authorization / scope basis

<bug-bounty-platform> <program-slug> BBP private opportunity was claimed/opened. H1 lists 9 in-scope, bounty-eligible assets with max severity Critical. See `programs/<program-slug>/scope.json`.

Rules that matter for this packet:
- Use owned accounts/objects only.
- Production signup must use `@researcher-alias.example` address.
- Production requests should include `X-<bug-bounty-platform>-Research: [H1 username]`.
- UAT findings need production reproducibility to be eligible.
- No production brute force/automation/DoS; no customer/non-owned data; no support/social-engineering; no report submission without operator approval.

## Passive precondition observations

1. Production signup page: `https://www.<program-slug>.com/create-account?utm_source=bug_bounty&medium=bug_bounty`
   - Fields/buttons observed: Email, Password, marketing checkbox, SIGN UP, Google signup, Apple signup, login link.
   - No form submission performed.

2. UAT signup page: `https://uat-bugbounty.nonprod.<program-slug>.com/create-account`
   - Same high-level signup surface: Email, Password, marketing checkbox, SIGN UP, Google signup, Apple signup, login link.
   - No form submission performed.

3. UAT frontend static config:
   - `NEXT_PUBLIC_BASEAPI_URL=https://api-uat-bugbounty.nonprod.<program-slug>.com`
   - Signup flow references `/auth/signup` and reCAPTCHA Enterprise `signup` action.
   - Auth flow references MFA/email OTP endpoints.
   - This is routing/precondition evidence only, not a vuln.

4. Minimal fixed-path API root checks:
   - `https://api-uat-bugbounty.nonprod.<program-slug>.com/` -> JSON 404 `Requested resource not found`.
   - `https://mark8.<program-slug>.com/` -> JSON 401 `Unauthorized`.
   - `https://api.<program-slug>.com/` -> Cloudflare challenge 403.
   - No fuzzing/scanning/auth/customer data.

## Candidate paths

```json
[
  {
    "candidate_id": "syfe_owned_object_idor",
    "attacker_objective": "Read or modify another user's investment/trading/account object by changing an object identifier.",
    "path_hypothesis": "After owned signup, <program-slug> web or API may expose portfolio/account/order/profile objects with stable IDs; Account B should not access Account A's object by direct API/URL.",
    "impact_potential": 5,
    "surrogate_feasibility": 3,
    "authorization_readiness": 2,
    "proof_boundary": {
      "in_scope_assets": ["www.<program-slug>.com", "api.<program-slug>.com", "uat-bugbounty.nonprod.<program-slug>.com", "api-uat-bugbounty.nonprod.<program-slug>.com"],
      "owned_accounts_or_objects": ["Account A/B only after operator auth gate", "owned empty/test objects only"],
      "allowed_state_changes": ["normal signup/login", "owned profile/object creation if no phone/KYC/payment gate", "manual low-speed owned-object read checks"],
      "blocked_state_changes": ["non-owned/customer object access completion", "financial transaction", "KYC/payment/phone without explicit operator decision", "bruteforce/enumeration"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only"
    },
    "proof_surrogate": "Create/read Account A owned object, confirm Account B/unauth cannot read same object. Use redacted snippets only.",
    "stop_before": ["OTP/CAPTCHA/phone/payment/KYC", "tokens/cookies storage", "customer data", "rate-limit or enumeration", "transactional/financial action"],
    "evidence_requirements": ["scope reference", "A/B role/object matrix", "redacted request/response status", "expected vs observed"],
    "execution_status": "needs_operator_control"
  },
  {
    "candidate_id": "syfe_api_ui_permission_mismatch",
    "attacker_objective": "Perform an API action that UI/account state should deny.",
    "path_hypothesis": "Onboarding or verification state may hide UI capabilities while backend endpoints still accept actions for unverified/non-KYC accounts.",
    "impact_potential": 4,
    "surrogate_feasibility": 3,
    "authorization_readiness": 2,
    "proof_boundary": {
      "in_scope_assets": ["www.<program-slug>.com", "api.<program-slug>.com", "uat-bugbounty.nonprod.<program-slug>.com", "api-uat-bugbounty.nonprod.<program-slug>.com"],
      "owned_accounts_or_objects": ["owned account only after operator auth gate"],
      "allowed_state_changes": ["manual UI/API comparison on owned account", "read-only or harmless owned-account actions"],
      "blocked_state_changes": ["financial orders/transfers", "KYC bypass completion", "response manipulation only", "production automation"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only"
    },
    "proof_surrogate": "Compare UI-denied owned state vs backend denial on same owned account without completing financial/KYC actions.",
    "stop_before": ["financial impact", "KYC/payment/phone", "credential/token capture", "policy-listed UI-only response manipulation"],
    "evidence_requirements": ["UI denied screenshot", "API denied/allowed redacted snippet", "actual backend effect if any, without financial action"],
    "execution_status": "needs_operator_control"
  },
  {
    "candidate_id": "syfe_signup_verification_lifecycle",
    "attacker_objective": "Bypass or confuse email/mobile/MFA verification state during signup/onboarding.",
    "path_hypothesis": "Frontend references email verification and OTP/MFA flows; lifecycle edges may expose stale sessions or state mismatch.",
    "impact_potential": 4,
    "surrogate_feasibility": 2,
    "authorization_readiness": 2,
    "proof_boundary": {
      "in_scope_assets": ["www.<program-slug>.com", "api.<program-slug>.com", "uat-bugbounty.nonprod.<program-slug>.com", "api-uat-bugbounty.nonprod.<program-slug>.com"],
      "owned_accounts_or_objects": ["operator-owned email/account only"],
      "allowed_state_changes": ["normal verification steps performed by operator", "manual observation of owned verification state"],
      "blocked_state_changes": ["OTP guessing", "brute force", "phone abuse", "support contact", "verification link storage"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only"
    },
    "proof_surrogate": "Record redacted state transitions only after operator completes OTP/email gates; do not store OTP or verification links.",
    "stop_before": ["OTP/CAPTCHA/phone gate", "retry/rate-limit testing", "verification-link capture", "support contact"],
    "evidence_requirements": ["state transition notes", "redacted UI states", "no secret/link storage statement"],
    "execution_status": "needs_operator_control"
  },
  {
    "candidate_id": "syfe_market_api_auth_boundary",
    "attacker_objective": "Access market/trading API data or functions without proper auth or entitlement.",
    "path_hypothesis": "mark8 and alfred APIs are separate in-scope services; unauth root currently returns 401/closed, but authenticated/entitlement boundaries may have role/object mismatch after owned login.",
    "impact_potential": 4,
    "surrogate_feasibility": 2,
    "authorization_readiness": 2,
    "proof_boundary": {
      "in_scope_assets": ["mark8.<program-slug>.com", "alfred.<program-slug>.com", "alfred-uat-31.nonprod.<program-slug>.com"],
      "owned_accounts_or_objects": ["owned account/session only after operator auth gate"],
      "allowed_state_changes": ["single fixed-path status checks", "manual owned-session entitlement checks if exposed by UI"],
      "blocked_state_changes": ["endpoint fuzzing", "order/trade placement", "non-owned data", "token storage"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only"
    },
    "proof_surrogate": "Use only UI-discovered endpoints from owned session; verify denial for unauth/other owned account without enumerating.",
    "stop_before": ["trading action", "fuzzing", "non-owned data", "token/cookie storage"],
    "evidence_requirements": ["UI-discovered endpoint provenance", "redacted status-only snippets", "owned-session boundary matrix"],
    "execution_status": "needs_operator_control"
  },
  {
    "candidate_id": "syfe_mobile_static_dynamic_bridge",
    "attacker_objective": "Find mobile/API mismatch exploitable against production backend.",
    "path_hypothesis": "Mobile apps and alfred UAT APK may expose routes/flows useful for web/API proof, but static-only issues are non-qualifying unless validated against production build/backend.",
    "impact_potential": 3,
    "surrogate_feasibility": 3,
    "authorization_readiness": 3,
    "proof_boundary": {
      "in_scope_assets": ["com.<program-slug>", "iOS App Store id 1497156434", "alfred-uat-31.nonprod.<program-slug>.com"],
      "owned_accounts_or_objects": ["none for offline static review", "owned account required for dynamic backend proof"],
      "allowed_state_changes": ["offline/static review", "no target-touching dynamic requests until separately gated"],
      "blocked_state_changes": ["root/jailbreak/SSL pinning bypass only", "hardcoded secret report without PoC", "production dynamic automation"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only"
    },
    "proof_surrogate": "Use mobile/static findings only as route discovery for later owned-account backend proof.",
    "stop_before": ["dynamic mobile API testing", "token/API-key storage", "production automation"],
    "evidence_requirements": ["static route provenance", "production-build validation plan", "owned-data backend proof if any"],
    "execution_status": "blocked_preserve"
  }
]
```

## Synthesis

Best next lane after operator gate: `syfe_owned_object_idor`, falling back to `syfe_api_ui_permission_mismatch` if the product exposes UI-denied/account-state actions but no cross-account object.

Current blocker is not scope; it is owned-account/control setup. No proof lane should execute until an owned account exists and no phone/payment/KYC gate blocks a safe object/control surface.
