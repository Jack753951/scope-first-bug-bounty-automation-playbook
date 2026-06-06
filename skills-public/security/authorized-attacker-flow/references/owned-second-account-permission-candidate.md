> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Owned second-account permission candidate pattern

Use this reference when a SaaS live-bounty lane finds that a second operator-owned account is visible inside the same company/workspace and appears to hold broad permissions.

## Session signal captured

A Front lane found that Account B, an operator-owned alias, appeared in the company teammate list as Active and belonged to high-privilege groups such as Customer Support / Sandbox Admins. Its visible resource permissions included broad teammate, inbox, tag, conversation, shift, and permission-management capabilities.

This is a strong candidate signal, but not automatically reportable.

## Required interpretation gate

Before calling it a vulnerability, prove one of these negative-control facts:

1. Account B was never intentionally invited, approved, or provisioned into the company/workspace, but still self-joined and received access.
2. Account B was intentionally added only as low-privilege/non-admin, but retained or gained admin-like access.
3. Account B was removed/downgraded from the relevant group, but direct URLs/API/UI actions still exposed admin/workspace capabilities.

Without one of those controls, broad Account B permissions may simply be expected workspace membership/admin behavior.

## Safe proof path

- Keep all work inside operator-owned accounts and objects.
- Use browser-only manual checks first; no scanner/fuzzer/DAST.
- Do not store cookies, tokens, OTPs, phone numbers, passwords, invite links, customer data, or raw private scope in artifacts.
- Stop before report submission; operator final-submit gate remains mandatory.

Preferred controls, in order:

1. Admin Account A lowers/removes Account B permissions, then Account B is tested against direct admin/settings URLs and safe owned-object actions.
2. Create/accept a fresh Account C with explicit low-privilege role, then test whether it can access admin/team/permission/inbox surfaces.
3. Operator provides provenance attestation that Account B self-registered and was never invited/approved; then preserve the finding as a report candidate but mark missing technical negative-control if no low-priv check exists.

## Evidence requirements

- Timestamped screenshots/notes showing Account B identity label only, not secrets.
- Account B membership/group/permission view, redacted.
- Expected role/provenance statement: invited/admin vs low-priv vs never invited.
- Negative-control result: low-priv/removed account cannot or can still access admin surface.
- Clear expected vs observed behavior and impact statement.
- List of untested/high-risk actions avoided.

## Common pitfall

Do not overclaim “privilege escalation” merely because a second owned account has broad rights. The reportable claim depends on mismatch between intended/authorized role and observed effective permissions.

Do not let a live UI anomaly create a new ad-hoc investigation lane before mapping it to a practiced bundle. For second-account/admin-like signals, first run the bundle precondition gate: admin positive control, clean low-priv or removed-user negative control, owned object/resource label, expected role matrix, and safe evidence path. If any required control is missing, park the anomaly and move to the next higher-yield bundle instead of spending operator auth/phone/email-verification effort on provenance speculation.