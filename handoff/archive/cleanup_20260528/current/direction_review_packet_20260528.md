> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Direction Review Packet — 2026-05-28

Status: read-only direction review request
Boundary: no target contact; no scan/fuzz/exploit/callback/OAST; no credential handling; no account mutation; no report submission; no file edits by reviewers.

## Review goal

The operator asks for Codex and Claude Code to act as direction reviewers and advise on the project capability vision and timeline.

Question to answer:

1. Is the current project vision coherent?
2. What should the platform be capable of in 48h / 7d / 14d / 30d / 90d?
3. Which capabilities are essential versus distracting?
4. What should be explicitly out of scope for the next 30 days?
5. What hard engineering/policy risks could make the repo chaotic again?
6. What should Hermes ask the operator to confirm about the capability vision?

## Project summary

This repository is an authorized bug bounty automation platform and capability library, not a general cybersecurity notebook.

Desired operating loop:

```text
fresh intel / scope change / target freshness
  -> detector or proof bundle lane
  -> candidate + controls
  -> evidence packet or no-finding closeout
  -> operator inbox decision
  -> report draft / final operator submit gate
```

Hermes role: project owner, scheduler, worker router, verifier, safety gate, and repo truth maintainer.

Operator role: auth/OTP/CAPTCHA/phone/payment/KYC, scarce account setup, safe phrases, final tactical corrections, and final submission approval.

## Required context reads

Read these files before giving advice and include an attestation listing which were read:

- `.hermes.md`
- `PROJECT_CHARTER.md`
- `docs/ENGINEERING_INDEX.md`
- `docs/policy/README.md`
- `docs/policy/repo_hygiene_policy.md`
- `docs/policy/memory_and_strategy_routing.md`
- `handoff/INDEX.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/current_artifact_index.md`
- `docs/strategy/platform/engineering_direction_20260527.md`
- `handoff/current/worktree_cleanup_index_20260528.md`

If a file is missing, say so.

## Current Hermes proposal to review

### 0–48 hours

- Clean worktree into reviewable commits.
- Keep active truth minimal: `docs/ENGINEERING_INDEX.md`, policy index, handoff index, current navigation/queue/artifact index.
- Stop adding policy variants.
- Verify with local tests and `hermes review`.

### 3–7 days

- Produce a compact operator inbox with 3–5 decisions.
- Push at least one live lane to candidate evidence, no-finding closeout, or explicit PARK/KILL.

### 7–14 days

- Run one complete loop: scope intake -> lane state -> bundle/detector -> evidence/no-finding -> review -> inbox -> report draft or closeout.

### 14–30 days

- Turn recurring substrate into daily dry-run/local job.
- Add scoped passive checks only after policy/scope gates.
- Stabilize 2–3 reusable bundles/detectors.

### 30–90 days

- Mature into a bug bounty operating system with recurring intel, detector/bundle library, lane state machine, evidence redaction, operator inbox, report draft pipeline, and clean repo discipline.

## Expected response format

Use Traditional Chinese.

Return:

1. Worker identity
2. Context read attestation
3. Verdict: APPROVE / APPROVE_WITH_CHANGES / REVISE
4. 48h / 7d / 14d / 30d / 90d recommended sequence
5. Essential capabilities
6. Non-goals for the next 30 days
7. Risks and hard stops
8. Questions Hermes should ask the operator to confirm capability vision
9. Any disagreement with Hermes proposal

Do not modify files. This is a read-only direction review.
