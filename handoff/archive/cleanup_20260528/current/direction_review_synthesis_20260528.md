> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Direction Review Synthesis — 2026-05-28

Status: active review synthesis
Boundary: read-only direction review synthesis; no target contact, no scan/fuzz/exploit/callback/OAST, no credential handling, no account mutation, no report submission.

## Review receipts

- Claude Code review: `handoff/current/claude_code_direction_review_20260528.md`
  - Raw JSON receipt: `handoff/current/claude_code_direction_review_20260528.json`
  - Session: `0120bb1f-6474-4aef-8edf-1ff06fdd021a`
  - Verdict: `APPROVE_WITH_CHANGES`
  - Context: direct read-only file reads completed.
- Codex review: `handoff/current/codex_direction_review_20260528.md`
  - Event log: `handoff/current/codex_direction_review_20260528.events.txt`
  - Initial direct-read attempt failed due Windows sandbox `spawn setup refresh`; Hermes retried with embedded synchronized context packet: `handoff/current/direction_review_codex_embedded_packet_20260528.md`.
  - Verdict after embedded context: `APPROVE_WITH_CHANGES`
  - Context: embedded required-file contents supplied by Hermes; no local tools used by Codex.

## Shared conclusion

Both reviewers agree the product vision is coherent: an authorized bug bounty automation platform/capability library with Hermes as project owner/verifier/safety gate and the operator as scarce-action/final-submit gate.

Both reviewers warn that the next failure mode is not lack of capability; it is substrate-first sprawl: detectors, policies, strategy docs, and agent reviews growing faster than candidate/evidence/report outcomes.

## Main corrections to Hermes proposal

1. Separate engineering deliverables from operator-gated live lane progress.
   - Inbox and dry-run loop are engineering-controlled.
   - <program-redacted>/<program-name>/<program-slug>/<program-redacted>/<program-redacted> lane progress may require operator actions and cannot be promised as pure engineering output.

2. Do not let detector expansion outrun the inbox/evidence consumer.
   - Claude Code suggested `build_operator_inbox.py` immediately.
   - Codex explicitly recommends demoting the large P1 detector list to Tier B until inbox/evidence can consume candidates.

3. Establish one active direction authority.
   - Current candidates: `docs/strategy/platform/engineering_direction_20260527.md`, `handoff/active_strategy_queue.md`, this synthesis.
   - Future action should edit the active engineering direction rather than create another dated direction variant.

4. Add outcome metrics.
   - 30-day success should not be "more infrastructure".
   - Pick one primary metric: first report draft/submission, or stable daily operator inbox. Reviewers prefer tying infrastructure to evidence/report closeout.

## Recommended sequence

### 0–48 hours

- Finish worktree split into reviewable commits.
- Keep active truth minimal: `docs/ENGINEERING_INDEX.md`, policy index, handoff index, current navigation, active queue, artifact index.
- Add/finalize `operator_inbox.md` or a fixed renderer path using current `platform/inbox/operator_inbox_summary.py`.
- Do not add policy/strategy variants.
- Keep all work offline/local unless separately authorized.

### 3–7 days

- Ship operator inbox v0 with 3–5 decisions max.
- Pick one Tier A lane and either:
  - progress it after operator gate, or
  - explicitly PARK/KILL it and move to the next lane.
- If live lane is blocked, run a dry-run/full-loop rehearsal with historical/PARKED lane data rather than expanding detectors.

### 7–14 days

- Complete one loop:
  - scope/policy intake
  - lane state
  - bundle/detector dry-run or passive check
  - evidence/no-finding packet
  - review
  - inbox
  - report draft or closeout
- The live portion remains operator-gated; the engineering portion should not block on live access.

### 14–30 days

- Stabilize 2–3 reusable bundles/detectors only after inbox/evidence can consume their output.
- Add evidence packet builder/redaction/report-draft path.
- Keep scheduler dry-run or local/passive unless program scope/rules/rate/stop-before are machine-checked.

### 30–90 days

- Mature into recurring intel + detector/bundle library + lane state machine + evidence/report pipeline + operator inbox + submission tracking.
- Add metrics: candidate packets/month, submissions/month, redaction violations = 0, stale root handoff files = 0.

## Capability vision questions for the operator

1. Primary 30-day success metric:
   - A. first report-ready draft/submission,
   - B. stable daily operator inbox,
   - C. one complete dry-run/no-finding loop,
   - D. balanced: inbox plus one lane closeout.

2. Tier A live lane for the next week:
   - A. <program-redacted> if human-check can be cleared,
   - B. <program-name> permission/stale-access lane if operator can perform safe account action,
   - C. park both and intake a fresh H1 target,
   - D. avoid live lanes and prove dry-run loop first.

3. Operator budget:
   - How many minutes per day/week can be spent on OTP/CAPTCHA/account setup/safe phrases/final review?

4. Acceptable next-30-day live automation boundary:
   - A. dry-run/local only,
   - B. scoped passive fingerprint only,
   - C. scoped owned-account evidence after explicit safe phrase,
   - D. decide per lane.

5. Report threshold:
   - Are informational/no-finding closeouts valuable, or should the platform optimize only for medium+ impact?

## Operator capability-vision confirmation — 2026-05-28

Operator choices:

1. 30-day primary success metric: `A` — first report-ready draft / submission. Stable inbox matters only insofar as it helps reach the first bounty.
2. Next-week Tier A lane: `D` — first prove the dry-run loop; do not force a live lane until the platform path is clear.
3. Next-30-day live automation boundary: `D` — decide per lane, with dry-run/local and scoped passive as defaults unless explicit safe phrase/operator gate is given.
4. Report threshold: `D` — depends on program bounty policy.
5. Operator budget: early phase can spend several hours if it materially improves the chance of the first bounty.

Implication:

The project should bias toward first-bounty outcome over infrastructure elegance. Inbox, dry-run loop, detector work, and cleanup are support work; they should not displace report-ready evidence or a promising operator-gated bounty lane.

## Hermes recommendation after operator confirmation

Adopt a first-bounty-first plan:

- 48h: commit/clean the repo enough to work safely, but do not over-polish.
- 7d: produce operator inbox v0 and prove the dry-run loop; use it to select the highest-probability first-bounty lane.
- 14d: push one selected lane toward report-ready evidence or explicit closeout.
- 30d: prioritize first report-ready draft/submission over broad detector expansion.

Default next action: fold this confirmed vision into `docs/strategy/platform/engineering_direction_20260527.md` as the active success metric, not as a new strategy variant.
