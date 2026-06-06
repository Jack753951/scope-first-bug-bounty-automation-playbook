> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# In-scope owned controls: proceed to checkpoint

Use this reference when the operator has already confirmed that a HackerOne/live-bounty target is in scope and the test uses only operator-owned accounts/objects.

## User expectation captured

The user corrected an overly conservative live-bounty flow: do not keep stopping for reviewer-style approval once scope and owned controls are established. The goal is to find the first reportable vulnerability and prepare a submission packet; Hermes should choose the concrete tactic (focused proof lane vs limited reconnaissance) and execute until a real checkpoint.

## Operating rule

If all are true:

- target/asset is explicitly in the program scope and in local scope artifacts;
- actions stay inside operator-owned accounts, tenants, workspaces, objects, aliases, or lab data;
- no customer/non-owned data is accessed;
- no secrets are stored in artifacts;
- technique is not prohibited by program rules;

then proceed without asking for extra approval or reviewer sign-off.

## Ask/stop only for concrete blockers

Ask the operator only when one of these appears:

- password, OTP, CAPTCHA, email/phone verification, payment/KYC, account recovery, or session switching;
- need to handle/store cookies, bearer tokens, API keys, private verification links, phone numbers, or credentials;
- non-owned/customer data would be viewed or changed;
- out-of-scope asset or policy ambiguity appears;
- DoS/rate-limit stress, destructive action, stealth/evasion, malware/persistence, or prohibited tooling would be needed;
- final report submission is ready and needs operator approval.

Reviewer objections are tactical evidence, not extra gates. Translate them into concrete blockers if any; otherwise continue.

## Strategy choice

For SaaS/workspace/team/API platforms, prefer high-yield A/B authorization lanes over broad scanning as the first reportability attempt:

1. Verify Account A and Account B are truly independent sessions.
2. Create or use harmless owned objects only.
3. Establish Account A positive control.
4. Establish Account B negative control through UI.
5. If UI denies access, test direct owned URLs/API/UI parity only when token/secret handling can be avoided or safely redacted.
6. Preserve evidence and stop at report-packet readiness for operator final submission.

Broad scan is a tool choice, not a default. Use it only when program rules, rate limits, and scope support it and it is more likely to produce reportable evidence than an owned-control proof lane.

## Checkpoint quality

A valid checkpoint is one of:

- report packet ready for operator final approval;
- concrete blocker requiring operator action (e.g., Account B identity/session not established);
- scoped no-finding with evidence and learning feedback;
- preserved candidate with exact missing proof control.

Do not stop merely because the next step is beyond passive mapping if it is in-scope and owned-control safe.
