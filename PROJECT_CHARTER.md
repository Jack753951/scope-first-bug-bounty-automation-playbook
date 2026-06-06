> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Project Charter

## Mission

Build a user-owned, authorized bug bounty platform that continuously turns fresh vulnerability intelligence and target surface changes into operator-ready bounty decisions and submission-grade evidence.

This is not a general cybersecurity notebook. North star is a repeatable pipeline:

```
fresh intel / target change → detector or bundle lane → candidate → evidence packet → operator decision → submission
```

## Primary outcomes

- Operator inbox holds high-quality bounded decisions, not raw research.
- Each active lane has an `EXECUTE / PASSIVE_ONLY / PARK / KILL` state with an explicit owner and (for PARK) `park_expires_at`.
- Report candidates carry redacted evidence, controls, scope references, and cleanup notes.
- Operator time is reserved for: auth/OTP/CAPTCHA, phone/payment/KYC, account setup, tactical correction, final submit.

## Operating model

Two roles only:

1. **Operator** — owns scope, owns scarce decisions, completes human gates, approves submissions. Spends minutes per day, not hours.
2. **Driver** — Claude Code in a single session. Reads active state, picks one action, executes inside `/SAFETY.md` boundaries, writes back to active-truth files.

Earlier multi-agent orchestration (Hermes / Cowork / Codex / Claude Impl) retired 2026-05-28. Archived at `archive/hermes_orchestration_20260528/`. Second-opinion models are invoked ad-hoc at decision points (KILL, scope change, submit), not as routine pipeline.

## Safety boundary

See [`/SAFETY.md`](SAFETY.md). Charter does not authorize any target action by itself.

## Decision vocabulary

- `EXECUTE` — preconditions met, bounded proof inside scope/policy/owned-control.
- `PASSIVE_ONLY` — version/exposure/metadata checks only on live targets.
- `PARK` — useful hypothesis, missing controls/scope/operator setup. Must have `park_expires_at`; expired without progress = downgrade or KILL.
- `KILL` — not worth more time.

## Current strategic bias

Prioritize first reportable bounty over broad learning. Active priorities and backlog: `docs/strategy/CURRENT.md`.

Learning assets remain valuable (`modules/bundles/`, `labs/`, `intelligence/cve_briefs/`) but they support the platform; they are not the primary workflow.
