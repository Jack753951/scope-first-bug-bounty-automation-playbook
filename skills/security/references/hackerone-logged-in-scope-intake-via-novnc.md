> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <bug-bounty-platform> logged-in scope intake via Kali/noVNC

Use this when the operator has already logged into <bug-bounty-platform> in the Kali/noVNC browser and explicitly authorizes work only inside the program's in-scope assets.

## Lesson

Do not ask the operator to manually copy a <bug-bounty-platform> asset table when Hermes can use the authorized remote UI session to read it. The operator's correction in this session was: if Kali/noVNC mastery is part of the platform goal and the H1 account is already logged in, Hermes should self-serve scope intake through the remote UI, not bounce the work back to the user.

## Safe workflow

1. Confirm authorization boundary in the chat:
   - public/known bug bounty or written authorization;
   - operator says only in-scope assets;
   - no secrets, OTPs, cookies, tokens, passwords, raw email aliases, or phone numbers should be pasted into chat or repo.
2. Use Kali/noVNC, not a separate browser session, when the user's logged-in <bug-bounty-platform> session is already there.
3. Navigate to the program scope/policy page and prefer official export/download when available:
   - typical page: `https://<bug-bounty-platform>.com/<program>/policy_scopes`;
   - download the Scope CSV if available;
   - store raw downloads under ignored/local evidence such as `setting/local/hackerone_scope/<program>/`.
4. Convert only confirmed in-scope assets into repo authorization artifacts:
   - create `programs/<program>/scope.json` with asset type, eligibility, max severity, and source evidence pointer;
   - add only selected host assets to `config/scope.txt`; do not add wildcards or marketing domains unless the official scope explicitly lists them;
   - keep mobile/binary/API lanes as reference-only unless they are the selected lane.
5. Run fail-closed dry-run checks before live contact:
   - in-scope asset should PASS through `recon.sh --dry-run --program <program> --policy-mode dry-run <url>`;
   - a nearby out-of-scope control should FAIL closed.
6. First contact stays low-speed/manual/noVNC:
   - open the selected in-scope app/login host;
   - screenshots and notes are local operational evidence, not report evidence;
   - do not run scanners/fuzzers/DAST or callbacks/OAST/tunnels.
7. Stop at operator gates:
   - email alias, phone number, password, CAPTCHA, OTP, verification link, payment, KYC, cookies, tokens, API keys;
   - the operator may have multiple phone numbers available, but record only non-sensitive gate capacity/status, never the actual numbers.
8. Record a machine-readable lane state:
   - `programs/<program>/lane_state.json` with current state like `A2_PENDING_OPERATOR_AUTH`;
   - handoff packet summarizing confirmed scope, dry-run gate, first-contact state, next operator action, and stop conditions.

## Pitfalls

- Do not treat a signup page reached via an in-scope app as a general authorization to test the parent marketing domain. If the parent domain is not in the official scope, keep it out of `config/scope.txt` and describe the signup page as a narrow official auth gate only.
- Do not store operator identity details. It is acceptable to note `operator-owned phone available` or `H1 alias ready`; never store the actual phone number, alias, OTP, password, token, cookie, or verification link.
- Do not let `scope confirmed` imply `automation allowed`. First live contact should remain manual/browser-only unless a separate bounded plan authorizes automation.

## Minimal artifact checklist

```text
setting/local/hackerone_scope/<program>/<official-scope-csv>
programs/<program>/scope.json
programs/<program>/lane_state.json
handoff/<program>_first_contact_scope_and_signup_gate_<date>.md
config/scope.txt  # selected confirmed host assets only
```

## Suggested status vocabulary

```text
scope_confirmed_dry_run_pending
formal_contact_started_operator_signup_gate
A2_PENDING_OPERATOR_AUTH
blocked_phone
blocked_email_verification
blocked_captcha
front_signup_complete  # replace prefix with program slug where useful
stop
```
