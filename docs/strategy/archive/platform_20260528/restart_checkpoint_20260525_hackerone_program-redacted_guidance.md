> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Restart Checkpoint — <bug-bounty-platform> <program-redacted> Taiwan Guidance Draft

Status: active checkpoint before Hermes restart
Date: 2026-05-25 17:48:44
Source: User + Hermes VM/noVNC-assisted live-bounty workflow
Repo truth: `.hermes.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/restart_checkpoint_20260525_hackerone_coupang_guidance.md`

## Why this checkpoint exists

The operator is restarting Hermes because the current provider repeatedly returned:

```text
No response from provider for 300s (non-streaming, model: gpt-5.5)
APIConnectionError
Provider: openai-codex
Endpoint: https://chatgpt.com/backend-api/codex
Error: Connection error
```

Interpretation: likely OpenAI Codex / chatgpt.com backend connection instability or long-session/provider timeout. This is not evidence that the Kali VM, <bug-bounty-platform> page, or project files failed.

## Current live-bounty boundary

This is an authorized bug bounty workflow, but no public/live target testing has been performed for this lane.

Binding limits:

- Do not run active scans, fuzzing, exploit attempts, brute force, checkout/payment/KYC/upload/seller/admin flows, or cross-account IDOR/object-ownership tests without explicit program scope/guidance.
- Do not store passwords, OTP, cookies, tokens, phone numbers, or private account data.
- Do not ask <program-redacted> general support or private employees for testing accounts.
- Do not ask anyone to bypass phone verification or anti-abuse controls.
- Do not use SMS rental services.
- Do not click <bug-bounty-platform> `Submit` unless the operator explicitly confirms final submission after review.

## VM / browser state

Use the Kali VM remote UI/noVNC session as the authoritative logged-in browser state.

Known route:

```text
Project root: <private-workspace>
Kali VM control: scripts/kali-vnc-control.ps1
Kali command wrapper: scripts/kali-run.ps1
noVNC endpoint: http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale
```

Important: the assistant/browser tool's separate browser session is not logged into the user's <bug-bounty-platform> account and should not be used to infer <bug-bounty-platform> login state.

## <bug-bounty-platform> / <program-redacted> Taiwan page state

The Kali VM browser is logged into <bug-bounty-platform> and is on the <program-redacted> Taiwan report assistant page:

```text
https://<bug-bounty-platform>.com/hai/report_assistant/158055?2=true
```

A draft report/guidance request exists but has not been submitted.

Current visible draft fields after editing:

- Program: <program-redacted> Taiwan
- Title: `Testing guidance request: two-account IDOR / object ownership testing`
- Asset: `www.tw.<program-redacted>.com (URL)`
- Weakness: `Insecure Direct Object Reference (IDOR) (cwe-639)`
- Description: filled with a pre-testing guidance request asking before any cross-account testing.
- Impact: short version filled:
  `No vulnerability is claimed in this request. This is a testing-guidance request only, asking before any two-account IDOR testing to avoid violating program rules or anti-abuse controls.`

No attachments were added.

## Run checks result

Hermes clicked `Run checks`, not `Submit`.

Hai for Hackers / pre-submission review reported `7 issues` and blocking items, including:

1. `Not a vulnerability report` — it recognized this as a testing guidance request rather than an actual vulnerability report.
2. `Missing required field: Severity` — it asks for a severity rating.

Non-blocking observations included that no PoC/vulnerability claim is present, severity should be `none` if no vulnerability is claimed, and asset/weakness classification may not match a guidance request.

Hermes synthesis: do not submit this draft as-is. The check result confirms that `Submit report` is a poor fit for a guidance request unless the operator knowingly accepts invalid/not-a-vulnerability-report risk.

## Hai for Hackers boundary

Hai for Hackers is not the <program-redacted> program team. It cannot provide test accounts, sandbox/staging access, program authorization, or permission to bypass phone verification/anti-abuse controls.

Acceptable use of Hai:

- ask where the correct program-team contact path is;
- ask how to rewrite a guidance request;
- ask how to avoid misclassifying it as a vulnerability report.

Do not treat Hai's response as authorization.

Suggested safe question to Hai if needed:

```text
Where is the correct <bug-bounty-platform> program-team contact path for a pre-testing guidance request? I am not reporting a vulnerability yet. I want to ask <program-redacted> Taiwan whether they can provide test accounts, sandbox/staging access, or guidance for two-account IDOR/object-ownership testing without violating phone verification or anti-abuse rules.
```

## Recommended resume path after restart

1. Reopen Hermes in the same project directory:

```powershell
cd <private-workspace>
hermes
```

2. If provider errors persist, consider:

```powershell
hermes status --all
hermes login --provider openai-codex
hermes model
```

3. For this task, resume from the Kali VM/noVNC browser, not a separate assistant browser.

4. Next safe action: back out of the current Submit report draft or leave it unsent, then search the <program-redacted> Taiwan <bug-bounty-platform> program page for an official `Contact`, `Ask a question`, or program-team message path.

5. If no official contact path exists, ask the operator before using `Submit report` for the guidance request, because <bug-bounty-platform> checks currently mark it as blocking/not-a-vulnerability-report.

## Last known screenshot artifacts

Local screenshots produced during this session include:

```text
<artifact-output-dir>/vm_screens/hermes_vm_checks_done.png
<artifact-output-dir>/vm_screens/hermes_vm_impact_ctrlv.png
<artifact-output-dir>/vm_screens/hermes_vm_impact_short.png
```

These are operational screenshots only. Review them before continuing if the browser state is unclear.
