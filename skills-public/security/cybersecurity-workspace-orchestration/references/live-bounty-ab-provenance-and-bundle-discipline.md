> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live bounty A/B provenance + bundle discipline

## Trigger

Use this note when doing authorized live-bounty work with owned accounts, especially A/B/C teammate, tenant, workspace, role, permission, invite, signup, or UI/API mismatch testing.

## Durable lesson

A candidate access-control signal is not enough. The proof lives in the chain-of-custody for how each owned account reached its state.

If an owned Account B is observed as an active teammate, group member, or admin-like user, record the provenance immediately. Do not rely on later operator memory.

## Minimum provenance record for each A/B/C account

For every account transition, write a redacted checkpoint that answers:

1. Which browser profile/session was active? Use labels only, not raw email.
2. Which identity was visible in the profile menu? Store only alias labels/fragments if needed.
3. Was the account created by signup, invitation acceptance, admin add, approval, SSO/domain join, or unknown path?
4. Was the company/workspace name typed? Was it intentionally the same as an existing workspace?
5. Was any invite email sent or accepted? Do not store invite links.
6. Did an admin manually approve/add/downgrade/change groups?
7. Which groups/roles/permission sets were assigned before and after the step?
8. What was expected vs observed?
9. What negative control exists? If none, state that the finding is not report-ready.

## Candidate classification rule

If provenance is missing, classify the result as:

`unresolved owned-account membership/permission candidate — not report-ready`

Do not describe it as a confirmed vulnerability. The safe next step is a fresh clean control, usually Account C, rather than asking the operator to reconstruct old details from memory.

## Clean repro pattern

For suspected self-join / same-company-name / same-domain tenant-join bugs:

1. Account A: admin/owner positive control.
2. Account C: fresh owned alias, separate browser profile.
3. Do not send or accept any invite for C.
4. Do not approve/add C from A.
5. If testing company-name matching, intentionally type the same company/workspace label and record that fact redacted.
6. Stop after first successful login/onboarding state and record the workspace/teammate/group state.
7. Only then compare A's teammate list and C's direct URL/settings access.

A reportable path needs proof that C joined or gained permissions without invite/approval/domain verification or other legitimate authorization.

## Bundle discipline in live bounty

Keep three states distinct in handoff and replies:

- Preserved hypothesis bundle: an idea family parked for later bounded proof.
- Bounded proof card: a concrete approved procedure with owned controls, stop-before rules, and expected artifacts.
- Executed bundle: an actual run with artifacts, such as `kali-output/<run_id>/...` or equivalent evidence.

If no bundle was executed, say so explicitly. Do not let a manual noVNC/UI validation session sound like a bundle-first靶機 run. When the user asks why no bundle artifact exists, the correct answer is usually workflow drift or a deliberate gate, not a display problem.
