> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Env-backed Signup Secret Bridge

Use this pattern for live bounty signup or account-control setup when Hermes may fill known operator-approved registration fields, but must avoid printing or persisting secrets.

## Durable pattern

- Keep registration convenience secrets in ignored local storage only, e.g. profile `.env` and/or repo-local `setting/local/*.env` covered by `.gitignore`.
- Use a script that reads secrets by symbolic key (`email`, `password`, `phone-primary`) rather than passing raw secret values through prompts, handoff files, command history, screenshots, or tool-call arguments.
- Prefer a browser-control path that does not expose the secret in agent-visible output:
  - Chrome DevTools Protocol (CDP) to type into the currently focused/selected field.
  - Clipboard/xdotool only as a fallback, with explicit awareness that clipboard state is sensitive.
  - Playwright fallback only if it can target the field without logging the secret.
- Windows control-plane to Kali/noVNC worker is acceptable when the Windows-side wrapper invokes the Kali-side script by symbolic secret name and never echoes the resolved value.
- Stop at CAPTCHA, OTP, email verification, phone verification, OAuth/integration activation, payment/KYC, and final submit gates.

## Minimal verification

Before using on a live target:

1. Confirm the env mirror file is ignored by git.
2. Run a dry-run or compile/syntax check that proves the symbolic key is recognized without printing the value.
3. Fill only the needed field, then visually verify in noVNC/browser.
4. Record only non-secret state in handoff: which symbolic field was filled, where the operator gate occurred, and whether the page advanced.

## Do not capture

- Passwords, phone numbers, OTPs, cookies, tokens, verification links, raw private email inbox contents, or screenshots that expose them.
- One-off target-specific signup narratives unless they affect the next execute/park/kill decision.
