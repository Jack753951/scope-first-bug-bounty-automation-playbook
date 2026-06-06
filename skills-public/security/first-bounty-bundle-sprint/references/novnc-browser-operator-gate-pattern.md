> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# noVNC / Browser Operator-Gate Pattern

Use when the first-bounty workflow involves a Kali/noVNC browser, logged-in H1/Intigriti/Bugcrowd pages, or remote desktop state.

## Durable lesson

Do not ask the operator to open or inspect pages until Hermes has first tried the already-provisioned browser/noVNC route. In this project, live bounty browser work often uses a Kali noVNC Firefox session that may already be logged in.

## Correct sequence

1. Check repo state for noVNC/browser readiness when needed, e.g. `handoff/kali_vm_operations_state.json` or current lane state.
2. Try the noVNC endpoint / browser route yourself before asking the operator.
3. If connected, use passive/logged-in UI observation first to gather policy/scope/freshness information.
4. Only ask the operator when a real gate appears:
   - CAPTCHA / human check.
   - OTP / email code / 2FA.
   - Login expired and credentials cannot be safely filled from approved env bridge.
   - Accept/apply/join terms, scarce claim, or unclear account-impact action.
   - Account creation, free trial, API key, organization/workspace setup, phone/payment/KYC/OAuth/integration.
   - Any live target testing or state-changing proof.
   - Final submission.

## Pitfall from 2026-05-28 session

Hermes incorrectly told the operator to open Intigriti/<program-redacted> policy in Kali/noVNC even though the project already had noVNC/browser setup and Hermes could verify access itself. The correction is to treat operator time as scarce: first test direct noVNC/browser operation, then escalate only if a human gate is actually present.

## Safe wording

Prefer:

```text
I will first try the already-open noVNC/Firefox session myself and stop only if I hit CAPTCHA/OTP/2FA/terms/account-action/live-test gates.
```

Avoid:

```text
Please open noVNC and navigate to X
```

unless Hermes already tried and hit a real gate or cannot reach the browser.

## Boundary

Viewing logged-in platform policy/scope pages through an already-authenticated browser is policy intake. It is still not authorization to test live targets. Keep the split explicit:

```text
policy/scope intake: Hermes may do if the browser is accessible
live target testing: requires scope/policy gate + owned-control proof plan + operator/safe-phrase where applicable
```
