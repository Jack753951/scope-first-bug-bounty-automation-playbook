> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live Target Remote UI Control Pattern

Use when the operator says they are logged into a bug bounty program or target inside the Kali/noVNC/VM browser.

## Lesson

Do not assume the agent's own browser automation session is the same as the operator's VM browser. For live bounty work, the operator may have completed login, CAPTCHA, OTP, or regional/browser state inside Kali/noVNC. That VM browser is the authoritative session for target-touching work.

## Preferred sequence

1. Confirm whether a project remote UI helper exists, such as a VNC/noVNC control script.
2. Check the remote UI service/tunnel status before opening a separate browser session.
3. Inspect the VM browser state through the remote UI or a fresh screenshot.
4. If the VM is logged in, continue from that VM session instead of asking the operator to repeat login.
5. Keep the same side-effect boundary: the agent may navigate, draft, and review; the operator handles passwords, OTP/CAPTCHA/2FA, and final submission/send confirmation.
6. If the tool browser and VM browser disagree, trust the VM browser for login/session state and label the tool browser as a separate unauthenticated session.

## Bug bounty submission boundary

For HackerOne/Bugcrowd-style program pages:

- Drafting a guidance request or report in the logged-in VM UI is acceptable after scope/rules are understood.
- Do not submit/send the final message without explicit operator approval.
- Avoid using platform AI assistant sidebars as if they were program-team contact channels unless the platform clearly states that the message goes to the program team.

## Context-compression / restart gate resumption

When resuming a live bounty lane after context compression, VM restart, or operator "continue" request:

1. Re-read the target lane state/checkpoint artifacts before touching the UI.
2. Verify noVNC/tunnel reachability and inspect the authoritative VM browser with a fresh screenshot.
3. If the UI is still at a signup/identity/phone/OTP/CAPTCHA/password/email/payment/policy gate, do **not** continue or submit. Return a short non-sensitive operator action token list.
4. If a local OS/authentication pop-up blocks the VM desktop, dismiss/cancel it if safe; never enter host/VM passwords unless explicitly authorized.
5. If a fresh browser/profile must be opened, use the documented dedicated profile and official in-scope-app path. Treat marketing-domain signup pages only as official continuation pages reached from the in-scope app flow, not as broadened test scope.
6. After verification, update machine-readable lane state/queue/checkpoint artifacts and run local validation (JSON parse, lane queue/status helper, runner expected blocked exit, diff check/review when available). This is handoff hygiene, not permission to bypass the operator gate.
7. Keep screenshots in ignored/local evidence storage and record only file pointers plus non-sensitive visible field labels.

## Evidence hygiene

Remote screenshots may reveal usernames, notifications, browser tabs, or account state. Use them only for navigation/state verification, avoid copying sensitive values into durable artifacts, and redact before report packets when needed.
