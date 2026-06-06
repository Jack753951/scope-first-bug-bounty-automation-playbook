> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> reviewer advisory correction — no extra safety gate

Timestamp: 2026-05-26T13:10:00Z
Program: <program-name> / <bug-bounty-platform> `<program-redacted>`

## Operator correction

Reviewers are for tactical/adversarial/evidence perspective. They must not add blocking safety gates beyond:

- confirmed in-scope assets and program rules;
- operator-owned accounts, objects, mailboxes, phones, and secrets;
- explicit approval for state-changing or stronger techniques;
- standing project safety rules: no non-owned/customer data, no destructive action, no scanner/fuzzer/DAST without approval, no callbacks/OAST/tunnels without approval, no token/cookie/OTP/phone/password storage, no report submission without operator approval.

## Practical effect

Claude/Codex findings are retained as useful objections and evidence gaps, not as veto authority. If a step is already allowed by scope/operator boundaries, execute it instead of waiting for another reviewer approval. If a step is blocked, record the concrete blocker, not "reviewer blocked".

## Current <program-name> concrete blockers

- Browser/noVNC state: current screenshots show Kali desktop/no visible <program-name> browser; do not kill/reset browser after denied destructive command. A non-destructive restore path or operator-visible browser is needed for more UI mapping.
- Account B / owned teammate absent.
- Second owned tenant/workspace absent.
- Named owned test inbox/object labels and cleanup plan not approved.
- API token/API call plan absent.
- Channel/OAuth/mailbox approval absent.
- Workflow/rule save/activation approval absent.
- Final report approval absent.

## Allowed now

- Passive public-docs inventory.
- Passive UI mapping if the existing browser is visible or can be restored non-destructively.
- Preservation of all useful hypothesis bundles.

## Not a finding

This correction is workflow alignment only. It does not create report-ready evidence and does not authorize out-of-scope or non-owned data access.
