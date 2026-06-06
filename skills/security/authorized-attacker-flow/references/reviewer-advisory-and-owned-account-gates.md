> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Reviewer advisory vs. real execution gates

Use this reference when an authorized bug-bounty lane has Claude/Codex/Cowork review output and the user expects tactical momentum.

## Durable lesson

Role-separated reviewers provide tactical/adversarial/evidence perspective. They do **not** create additional safety gates. A reviewer `BLOCK` or `REQUEST_CHANGES` should be preserved as an objection, evidence gap, or tactical warning, but it should not stop actions that are already allowed by:

- confirmed program scope and rules;
- operator-owned accounts, objects, mailboxes, phones, and test data;
- explicit approval for state-changing or stronger techniques;
- standing project boundaries: no non-owned/customer data, no destructive action, no scanner/fuzzer/DAST without approval, no callbacks/OAST/tunnels without approval, no token/cookie/OTP/phone/password storage, no report submission without operator approval.

If execution pauses, name the concrete blocker, not “reviewer blocked.”

## Correct synthesis pattern

1. Record reviewer objections and useful ideas.
2. Translate each objection into either:
   - a concrete operator/scope/safety blocker; or
   - an evidence gap/tactical caution that can be worked around.
3. Continue all safe in-scope work immediately.
4. Ask the operator only for the specific missing control or approval, e.g. Account B signup, owned object label, phone/OTP handling, token/API approval, channel/OAuth approval, workflow activation approval, scanner approval, or final report approval.

## Second-account signup preparation pattern

When Account B is needed and the operator has authorized signup:

- Open a separate browser profile/window for Account B when practical.
- Fill only non-secret, operator-approved metadata.
- Stop before phone, CAPTCHA, email verification, OTP, password, or final submit if those are operator-handled.
- Save redacted/local screenshot evidence and update lane state to `operator_phone_and_submit` or equivalent.
- Do not store phone numbers, OTPs, passwords, verification links, cookies, or tokens.

## Safe web research / script translation pattern

When the user asks to look for known scripts or proven vulnerability flows:

- Search public sources and distinguish target-specific evidence from broad false positives.
- Prefer converting known SaaS bug classes into owned-data workflows: shared object visibility, comment/draft/message splits, invite/role boundaries, workflow/rule activation, channel/OAuth boundaries, API/UI mismatch.
- Do not run downloaded scripts directly against the live target.
- Convert any future target-touching script into a slow proof surrogate with scope fail-closed checks, dry-run, rate limits, redaction, and explicit operator approval.

## Example wording

Bad: “Reviewer blocked this lane.”

Good: “Reviewer raised evidence gaps. The concrete blocker is Account B is not complete; I prepared Account B signup to the operator phone/submit gate and will continue A/B owned-object mapping after completion.”
