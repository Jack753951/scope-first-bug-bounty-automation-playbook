> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live Target Signup and Account Gate Pattern

Use this reference when a bug bounty first wave requires throwaway account creation or login.

## Durable lesson

For live targets, account creation is part of the safety boundary. If the platform presents CAPTCHA, OTP, email/phone verification, anti-abuse prompts, account warnings, or `Access Denied` to automation, stop and route to operator-local signup instead of retrying or bypassing.

## Recommended sequence

1. Confirm program authorization, exact in-scope signup/login assets, and any required researcher header.
2. Ask for two operator-owned throwaway account emails only if account creation is needed.
3. Record in repo only that operator-owned account inputs were received; do not reprint full email addresses unless explicitly needed.
4. Navigate only official in-scope signup/login pages.
5. If a form loads normally, fill only approved fields and pause for CAPTCHA/OTP/email/phone verification.
6. If browser automation receives `Access Denied` or anti-bot friction, stop. Do not keep retrying, rotate routes, or bypass checks.
7. Ask the operator to create accounts locally through a normal browser/network and return with non-sensitive labels, screenshots, or safe post-login path information.
8. Resume with low-speed account-owned surface mapping: profile/member/review/cart/object ownership; avoid payment/KYC/upload/third-party data.
9. If the operator-local VM/browser locks or returns to an OS lock screen mid-session, treat it like a credential boundary: do not ask for or store the VM password, do not attempt password entry, and do not work around the lock. Save the current artifact state, state the exact blocker, ask the operator to unlock locally, then resume by re-confirming the logged-in page state with a screenshot before any further navigation.
10. Non-sensitive anti-idle hardening is acceptable only after the operator has control of the VM/session, e.g. screen-saver/DPMS disable attempts. Record it as a convenience setting, not as credential handling or a bypass.

## Operator-local interruption pattern

Live bounty browser work often depends on local auth, CAPTCHA, OTP, anti-abuse posture, or a VM/noVNC session the operator controls. When the session is interrupted by a lock screen, timeout, or local auth prompt:

```text
- stop target-touching navigation immediately;
- do not request, reveal, type, save, or infer local passwords/OTP/cookies/tokens;
- preserve any already-created artifacts and screenshots;
- mark status as blocked_operator_action;
- give the operator a minimal local action such as "unlock the VM locally and reply unlocked";
- after unlock, verify the browser is still on the intended logged-in surface before continuing;
- continue from the artifact/checkpoint instead of restarting the assessment.
```

Good status wording:

```text
Current blocker: operator-local VM lock screen. No scans, fuzzing, cross-account tests, payment/order/KYC/upload flows, or credential storage occurred. Waiting for operator to unlock locally; after unlock, Hermes will re-confirm the logged-in browser state before continuing the surface map.
```

## Artifact wording

Use language like:

```text
Operator provided two owned email addresses for Account A and Account B in the active chat. Exact addresses are intentionally not reprinted here. Hermes should use them only for the official in-scope signup flow and should not store passwords/OTP/recovery material.
```

If blocked:

```text
Direct navigation to the official registration page returned Access Denied. No form was filled, no account was created, no password/OTP/phone data was requested or stored, no scan/fuzz/probe was performed. Current recommendation: operator-local signup through normal browser/network.
```

## Why this matters

This keeps the project from turning normal anti-abuse friction into a bypass task, prevents durable storage of account identifiers/secrets, and preserves a clean report narrative for authorized assessment work.
