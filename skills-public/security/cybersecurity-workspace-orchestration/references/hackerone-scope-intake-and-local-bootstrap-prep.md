> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# HackerOne scope intake + local bootstrap prep pattern

Use this when a cybersec lab session is transitioning from local/offline preparation toward an authorized public bug bounty or a local vulnerable-app bootstrap candidate.

## Pattern

1. Treat the public/live-target lane as blocked until the operator supplies the program policy URL, in-scope assets, out-of-scope assets/actions, allowed/forbidden techniques, automation/rate limits, testing windows, test-account availability, callback/OAST/tunnel rules, and report-submission rules.
2. Create a repo handoff intake file for the operator to fill, with status such as `blocked-awaiting-operator-scope`. Do not add targets to `config/scope.txt` or generate `programs/<program-slug>/scope.json` from guesses.
3. After the operator supplies scope, convert it into the repo's program scope schema first, validate it against the global whitelist/safety policy, then ask before any target-touching dry run.
4. For public bug-bounty programs that require logged-in testing, prefer operator-created throwaway accounts over agent-created accounts. The operator should handle CAPTCHA, email, OTP, phone, recovery, and any personal/financial verification locally; do not ask them to paste long-lived passwords/OTPs into handoff. If the operator explicitly authorizes Hermes to create accounts, constrain it to the official in-scope signup flow, at most the approved number of throwaway accounts, no anti-abuse bypass, no non-owned email/phone, no stored credentials in repo, and stop for any CAPTCHA/OTP/phone/payment/KYC gate.
5. When a program mandates researcher-identification headers (for example `X-HackerOne-Researcher: <h1-username>`), record the exact username in the program scope artifact and dry-run packet, but still keep target-touching blocked until selected assets are explicitly added to the global scope whitelist and the operator approves the single-lane plan.
6. Keep local vulnerable-app/bootstrap candidates separate from public-scope intake. Run only posture/precheck commands unless the correct disposable victim-lab/Docker posture is confirmed.
5. If a local bootstrap/precheck blocks because prerequisites are absent on the control plane, record the blocking posture as a safe fail-closed result, but do not encode the missing prerequisite as a durable limitation.
6. Quarantine unverified CVE/live-scan notes into ignored local storage if they contain target-touching suggestions or unverified claims; commit only cleaned methodology/templates.
7. Update navigation/handoff/Obsidian pointers so the active lanes are explicit: first authorized-scope intake, then live-target dry-run readiness, then vuln-intel refresh/local lab candidates as separately gated lanes.

## Final response shape for this user

- State branch/commit/push only if actually verified.
- Summarize benefits and changed files.
- Label blocked gates explicitly.
- Provide the exact next human input list for scope intake.
- Reassure that no live/public target or exploit/proof was touched if the session stayed in prep/precheck mode.
