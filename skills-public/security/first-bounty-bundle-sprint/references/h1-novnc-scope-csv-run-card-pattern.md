> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# H1 noVNC + Scope CSV Run-Card Pattern

Use this when the first-bounty lane involves a logged-in HackerOne browser, noVNC/Kali, and H1 scope metadata.

## Durable technique

1. Before asking the operator to navigate a logged-in browser, try the existing Kali/noVNC route yourself.
2. If noVNC canvas interaction is clumsy, use the already-authorized Kali SSH path plus desktop tools to control Firefox:
   - `xdotool` for focus, URL navigation, clicks, keys.
   - X11 screenshot tools such as `import -window root` for ground truth screenshots.
   - Base64 over SSH for pulling screenshots/files back when scp path conversion is awkward.
3. Treat this as browser operation, not target testing, while you are only reading platform policy/scope pages.
4. Stop only at real gates: CAPTCHA/OTP/2FA/login failure, accept/apply/join terms, scarce claim/slot consumption, account/trial/API setup, live target contact, safe phrase, or final submit.

## H1 Opportunity Discovery gates

- `Claim your spot`, private invitations, or language like `up to 1 per 30 days` is a scarce operator-resource gate. Do not consume it without explicit operator approval unless a separate active instruction in the current session explicitly authorizes consuming that slot.
- Before asking, summarize competing choices and give a recommendation.
- Non-scarce public/collaboration program policy pages can be opened and read autonomously when already logged in.

## Scope CSV discipline

When H1 offers a scope CSV:

1. Download it from the policy/scope page.
2. Parse it locally for:
   - identifier
   - asset_type
   - eligible_for_bounty
   - eligible_for_submission
   - max_severity
   - updated_at
3. Compare URL identifiers against repo `config/scope.txt` before any live target action.
4. If H1 scope has more assets than repo whitelist, live execution is limited to the intersection. Do not silently expand `config/scope.txt`; it is operator-owned in this project.
5. Write the mismatch into the run card as a hard precondition, including currently whitelisted hosts and parked H1-only assets.

## First-bounty run-card conversion

Convert policy/scope metadata into a run card before touching target hosts:

```text
Program:
Scope source:
Repo whitelist intersection:
Bundle:
Report title if true:
Positive control:
Negative control:
Owned object/resource:
Allowed actions:
Blocked actions:
Operator cost:
Kill criteria:
Evidence required:
Decision: PREPARED_NOT_EXECUTED / EXECUTE / PARK / KILL
```

## Pitfalls

- Do not ask the operator to use noVNC when the browser route is already available and you have not tried it.
- Do not treat a platform-visible in-scope asset as live-authorized in this repo until it also passes `config/scope.txt`.
- Do not click scarce private-opportunity claims while merely doing autonomous triage.
- Do not let a suspended program remain in the first-bounty execution lane; keep it only as passive research/reference.
