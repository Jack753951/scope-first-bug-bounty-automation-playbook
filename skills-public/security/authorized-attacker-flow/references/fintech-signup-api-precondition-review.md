> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Fintech signup/API precondition review pattern

Session lesson from a Syfe-like HackerOne fintech target: before spending operator auth cost, do a compact passive precondition review that determines whether the target has a plausible owned-object/API bundle and where the hard human gates begin.

Use when:

- H1 scope lists web + API + mobile assets for a fintech/investment/trading product.
- Program allows owned-account testing but has likely phone/KYC/payment/friction.
- The goal is first-bounty access-control/object-boundary proof, not broad recon.

Low-side-effect sequence:

1. Capture H1 scope/policy metadata into repo-local artifacts: allowed assets, production/signup identity rules, headers, non-qualifying issues, disqualifiers, and UAT/prod reproducibility requirements.
2. Visit only the program-provided signup/login URLs and map visible fields/buttons. Do not submit forms.
3. If a UAT/test environment exists, visit its landing/signup page and map whether it mirrors production.
4. Passively inspect already-loaded public frontend bundles for environment config and route names, especially base API host, signup endpoint names, OTP/MFA/email-verification references, and CAPTCHA indicators. Treat this as routing/precondition evidence only.
5. Optional: perform tiny fixed-path root/status checks only on explicitly in-scope API roots, with the required bounty header when production is touched. Do not enumerate endpoints or fuzz.
6. Build candidate packets for owned-object IDOR, API/UI permission mismatch, verification lifecycle, entitlement/API auth boundary, and mobile/static-to-backend bridge.
7. Stop at the first auth/OTP/CAPTCHA/phone/payment/KYC/credential gate. Ask the operator to complete auth or park if phone/KYC/payment appears before a strong owned-object surface exists.

Safety boundaries:

- No scanner/fuzzer/DAST/endpoint brute force.
- No signup submission by the agent when secrets or human verification may appear.
- No token/cookie/password/OTP/verification-link/API-key storage.
- No customer/non-owned data.
- No financial transaction, KYC bypass completion, trading/order action, or support contact.

Useful artifact set:

- `programs/<slug>/run_card.md`
- `programs/<slug>/scope.json`
- `programs/<slug>/lane_state.json`
- `programs/<slug>/evidence_index.json`
- `programs/<slug>/candidate_packet_<date>.md`

Decision rule:

```text
EXECUTE_PRECONDITION_REVIEW -> NEEDS_OPERATOR if account/control setup is required.
PARK if phone/KYC/payment/support contact appears before an owned-object/API boundary is visible.
After auth, prefer object-ownership-idor; fallback to api-ui-permission-mismatch.
```
