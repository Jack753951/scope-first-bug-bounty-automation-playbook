> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Second-account provenance chain-of-custody for SaaS permission candidates

Use this reference when a live-bounty SaaS lane tests tenant/workspace/team/role boundaries with Account A/B/C.

## Session lesson

A Front lane found a strong candidate signal: an operator-owned second account appeared as an active teammate with broad/admin-like permissions. The evidence showed the permission state, but the proof was weakened because the session did not preserve the full Account B provenance path: whether B self-registered, used the same company name, accepted an invite, was admin-approved, or was later added to groups.

The user correctly pushed back: for this class of finding, the agent should remember and record the provenance as it happens rather than ask the operator to reconstruct it later.

## Required provenance log before and during A/B/C testing

For every owned secondary account, record a redacted chain-of-custody table in the lane checkpoint:

| Field | Record without secrets |
| --- | --- |
| Account label | A/B/C only; no full email |
| Browser profile | path/display/window label |
| Signup source | self-signup, invite accept, SSO, existing session, unknown |
| Company/workspace label relation | same-as-A, different-from-A, unknown; do not store sensitive exact names unless already safe |
| Invite state | no invite sent, invite sent not accepted, accepted, unknown |
| Admin approval/addition | none, performed by operator, system-suggested, unknown |
| Group/role assignment | default, manually assigned, automatically assigned, unknown |
| First post-auth screen | new workspace onboarding, existing workspace dashboard, invite acceptance, other |
| Operator secret gates | phone/OTP/password/email verification handled by operator; no values stored |
| Evidence pointers | redacted screenshots/notes only |

If any row is unknown, mark it immediately as an evidence gap. Do not let the lane silently advance to a privilege-escalation claim.

## Clean repro rule

If provenance is missing or contaminated, prefer a fresh Account C clean repro over asking the operator to remember details:

1. Open/stage a dedicated browser profile for Account C.
2. Navigate to the official signup path and stop at the form/secret gate.
3. Ask the operator only for fields the agent cannot handle or must not record: email alias, phone, password, OTP, verification link.
4. Instruct the operator not to accept invites and not to approve/add C from Account A/admin.
5. If testing company-name auto-join, ask them to use the same company/workspace label as Account A, but still avoid storing sensitive exact values.
6. After the operator completes signup/auth, verify whether C reached a new workspace or unexpectedly joined A's company; then check teammate list, groups, permissions, and direct admin/settings URLs.

## Evidence discipline

- Do not store full emails, phone numbers, OTPs, passwords, cookies, tokens, verification links, or customer data.
- Do not overclaim broad rights as privilege escalation unless the expected role/provenance contradicts the observed permissions.
- Preserve both positive and negative controls: admin Account A, low-priv/never-invited Account C, and any downgraded/removed-account state if available.

## Reportability gate

A reportable finding requires at least one of:

1. Self-signup/never-invited account joins existing company/workspace and receives access.
2. Explicitly low-priv account receives or retains admin-like access.
3. Removed/downgraded account still accesses admin/resource surfaces through UI/API/direct URLs.

Without one of these, classify the result as an unresolved candidate or expected membership behavior.