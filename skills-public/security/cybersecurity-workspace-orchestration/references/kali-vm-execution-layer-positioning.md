> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Kali VM execution-layer positioning

Use this when deciding whether Cybersec Lab work should run through Kali/noVNC or stay in the Windows Hermes/repo control plane.

## Durable lesson

The Kali VM layer is valuable, but it should be a specialized execution/isolation layer, not the default control plane for every task.

Recommended split:

```text
Windows Hermes/repo = project owner, control plane, handoff truth, scheduling, inbox, policy/scope gates, source review, bundle writing, report drafting.
Kali VM = isolated Linux execution, noVNC/live browser, Burp/browser-assisted validation, local lab proof runners, Linux/package PoCs, scanner/fuzzer tooling only when authorized.
Victim/lab VM = disposable/recoverable target surface.
Live target = touched only after scope + program rules + operator gate.
```

## Add a Kali necessity gate to run cards

Classify each lane before execution:

```text
KALI_REQUIRED: needs noVNC/logged-in browser, Burp/manual validation, host-only lab, Linux-only PoC, local proof runner, or authorized scanner/fuzzer tooling.
KALI_OPTIONAL: Linux/container semantics are useful but the planning/source/repo work can proceed without Kali.
NO_KALI: passive/source review, policy analysis, candidate scoring, schema/tests, bundle writing, operator inbox, report draft, or handoff cleanup.
```

## Examples

- Live UI lanes such as H1/noVNC, <program-redacted>, <program-redacted>, Front: `KALI_REQUIRED` for browser observation; `NO_KALI` for policy/scope analysis and report drafting.
- Fresh vulnerability source lane: `NO_KALI` for advisory intake and patch diff; `KALI_OPTIONAL` or `KALI_REQUIRED` only for local proof execution.
- `tmp@0.2.5` path traversal bundle: `KALI_REQUIRED` or Linux container required for clean proof execution; `NO_KALI` for bundle writing and live-target matching.

## Pitfalls

- Do not let VM maintenance, SSH wrappers, noVNC canvas friction, or VirtualBox network posture checks consume first-bounty time when the task is passive/source/repo work.
- Do not treat Kali readiness as live-target authorization. Even if SSH/noVNC pass, target-touching work still needs scope, program policy, owned controls, and operator gates.
- Do not remove Kali entirely: it provides isolation, Linux-native tooling, browser state containment, artifact separation, and host-only/NAT posture for local labs.
