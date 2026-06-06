> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> third-target pre-contact readiness checkpoint — 2026-05-26

Status: READY_FOR_OPERATOR_GATE / noVNC reachable / <program-name> signup gate visible in continuation pass
Source: Hermes local engineering + VM/noVNC readiness pass
Repo truth: `programs/<program-redacted>/scope.json`, `programs/<program-redacted>/lane_state.json`, `handoff/restart_checkpoint_20260526_front_signup_phone_gate.md`, `handoff/third_target_contact_checkpoint_20260526.json`, `handoff/current_artifact_index.md`, `handoff/accepted_changes.md`

## Purpose

This checkpoint closes the local engineering/readiness cleanup requested before continuing the third live target lane. It makes the next step actionable without silently contacting the target or handling operator secrets.

## Current decision

```text
READY_FOR_OPERATOR_GATE
```

Meaning:

- <program-name> / `<program-redacted>` scope and lane artifacts already exist.
- The local review/attestation gate is fail-closed and regression-covered.
- The Kali attacker VM is running.
- noVNC is reachable from Windows at the local URL below.
- Earlier readiness pass did not open <program-name>; the latest continuation pass reopened the official path from `<in-scope-host>/signin` to `<program-domain>/signup`.
- The visible signup form still blocks on operator-controlled identity/phone and any later OTP/CAPTCHA/email/password/payment/policy gates.

## Runtime readiness verified in this pass

```text
VirtualBox running VM: <attacker-vm>
Kali SSH: reachable at <lab-ip>:22 using project-local SSH config/key
Remote browser desktop: Xvfb-backed noVNC session on Kali localhost
Windows local noVNC tunnel: listening on 127.0.0.1:6080
noVNC HTTP check: HTTP/1.1 200 OK for /vnc.html
Agent lock: clear
```

Open for operator/visual handoff:

```text
http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale
```

Important caveat: the previous physical `:0` X session was at the LightDM greeter and could not be attached by `x11vnc` as user `kali` due Xauthority. Hermes therefore started a separate Xvfb/Xfce browser desktop and tunneled that to local noVNC. This is sufficient for a fresh browser-only third-target continuation, but it may not show the exact old prefilled signup window from the earlier physical session.

## Scope and authorization checkpoint

Confirmed in prior artifacts:

```text
program: <program-redacted> / <program-name>
in-scope app host: <in-scope-host>
in-scope API host: <in-scope-host>
program scope file: programs/<program-redacted>/scope.json
global scope entries: <in-scope-host>, <in-scope-host>
out-of-scope control: <program-domain> fails closed in safe_target checks
```

`<program-domain>` remains out of global scope. It may only appear as the official signup page reached from the in-scope app sign-in flow; it is not a marketing-site test target.

## Operator gate

Current lane state:

```text
A2_PENDING_OPERATOR_AUTH / blocked_operator_action
```

Operator-only actions:

- enter any phone number locally, if choosing to continue;
- handle CAPTCHA, OTP, email verification, password, SSO, payment/KYC, or policy prompts locally;
- do not paste phone numbers, passwords, OTPs, cookies, tokens, API keys, or verification links into chat/repo.

Expected non-sensitive reply after operator action:

```text
front_signup_complete
blocked_phone
blocked_email_verification
blocked_captcha
blocked_payment
blocked_policy
stop
```

## Next Hermes action after operator gate

Only after `front_signup_complete` or an equivalent non-sensitive success signal:

```text
browser-only, low-speed, owned-account surface map of profile/workspace/roles/non-sensitive empty states
```

Stop before:

```text
scanner/fuzzer/DAST
DoS/rate-limit testing
exploit/callback/OAST/tunnel
customer messages/comments/support chat
non-owned/customer data
third-party integrations
API token creation or retention
credential/cookie/token/password/OTP storage
billing/payment/KYC
report generation/submission without operator final approval
```

## Validation performed for this checkpoint

Runtime/readiness checks:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' startvm '<attacker-vm>' --type headless
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' list runningvms
ssh.exe -F setting/local/ssh/empty_ssh_config -i setting/local/ssh/kali_codex_ed25519 -p 22 kali@<lab-ip> 'echo ssh_ready && hostname'
# started Xvfb :2, Xfce, x11vnc on 5902, websockify on 6081, and local SSH tunnel 6080 -> 6081
curl -I --max-time 5 http://127.0.0.1:6080/vnc.html
```

Engineering checks are recorded in `handoff/accepted_changes.md` and `handoff/latest_check.md`; rerun before final handoff if additional files change.

## Safety boundary for this pass

Latest continuation opened only the normal in-scope-app sign-in path and official signup page; no signup was submitted, no phone/OTP/password was handled, no scanner/fuzzer/DAST/exploit/callback/OAST/tunnel was run, no customer/non-owned data was accessed, no chat/support/integration/API token path was used, and no report was generated/submitted.


## Latest continuation verification — 2026-05-26

Hermes verified the local noVNC tunnel and remote Kali browser desktop, dismissed a local Kali color-management authentication pop-up without entering any password, opened a fresh Chromium profile at:

```text
/home/kali/browser-profiles/<program-redacted>-hermes
```

Then Hermes navigated the official lane path:

```text
https://<in-scope-host>/ -> https://<in-scope-host>/signin -> Try for Free -> https://<program-domain>/signup
```

Visible current state: <program-name> free-trial signup form with non-sensitive field labels for work email, first/last name, company, job title, industry, phone number, and company size. A chat/support widget is visible and remains blocked.

Latest local screenshot pointer, kept under ignored local evidence storage:

```text
setting/local/screenshots/program-redacted_live_20260526/signup_gate.png
```

Current decision remains:

```text
A2_PENDING_OPERATOR_AUTH / blocked_operator_action
```

Hermes must not proceed to submit signup, handle phone/OTP/CAPTCHA/password/email verification, or continue to post-auth surface mapping until the operator completes the gate locally or explicitly authorizes a transient one-time field entry.
