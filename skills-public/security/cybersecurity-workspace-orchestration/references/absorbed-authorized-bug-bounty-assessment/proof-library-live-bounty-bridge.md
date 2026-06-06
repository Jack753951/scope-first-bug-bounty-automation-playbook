> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Proof Library → Live Bounty Bridge Pattern

Use this when a project has local-lab proof bundles and is starting authorized live bug-bounty work. The goal is to convert local proof capability into live-target decision quality without importing lab intensity into real services.

## When to apply

- A local proof library already exists: IDOR/BOLA, auth/session, XSS, SSRF, file-read, upload, exposure, report packets, etc.
- A live bounty lane has begun or is about to begin.
- The current live result may be `no_finding`, `surface_only`, or blocked on an account/scope prerequisite.
- The user asks whether prior bundles/notes helped the live work, or how to make them more useful.

## Bridge artifact shape

Create a repo handoff such as:

```text
handoff/proof_library_live_bounty_bridge_<date>.md
```

Recommended sections:

1. Purpose: convert local proof patterns into live-bounty prerequisites and evidence thresholds.
2. Global live-bounty defaults: manual, low-speed, one lane, owned accounts, redaction, no auto-submit.
3. Decision labels:
   - `surface_only`
   - `needs_second_account`
   - `blocked_state_change`
   - `blocked_sensitive_flow`
   - `gate_fail_closed_needs_fix`
   - `candidate`
   - `report_ready`
4. Local proof pattern bridge table:
   - local proof pattern
   - verified local sources
   - live bounty usable when
   - blocked when
   - minimum live evidence
   - current program status
5. Program-specific target-state map.
6. Before/after account-prerequisite actions.
7. Required authorization-gate fixes before live automation.
8. Future bundle improvement rule.

## Important value framing

A no-finding live dry run can still be valuable if it produces any of:

- validated live safety profile;
- target-specific empty-state/surface map;
- prevented overclaiming by correctly using `surface_only` or `needs_second_account`;
- identified Account A/B or program-guidance prerequisites;
- identified authorization-gate automation blockers before scanner-like execution;
- upgraded local bundles into live-prerequisite proof cards.

Do not judge the dry run only by whether it found a bounty report.

## Local proof pattern → live prerequisite examples

| Pattern | Live usable when | Blocked when | Minimum live evidence |
|---|---|---|---|
| IDOR / BOLA / object ownership | Two owned or program-provided accounts; object IDs from normal UI/API provenance; program allows low-speed account-owned access-control testing | One account only; guessed IDs; payment/order/KYC/support/upload/seller/admin; program forbids multi-account tests | Account A positive, Account B negative, object provenance, redacted request/response, no third-party data |
| Auth/session/member boundary | Normal read-only UI/session/profile pages; no recovery/anti-abuse prompt | CAPTCHA/OTP/account warning; recovery/password reset; secrets would need to be copied | Auth-required vs unauth state, non-sensitive account labels, redacted screenshots/summaries |
| XSS safe marker | Owned field, benign marker, program allows content testing, no third-party viewers | Requires public content, active payload, cookie/token access, stored content not clearly allowed | Owned input provenance, benign marker render, negative/control render, cleanup if state changed |
| File read / XXE / path traversal | Program explicitly allows class; harmless owned marker; no secret paths | Public target default; `/etc/passwd`, metadata, secrets, uploads without plan | Owned marker provenance, positive marker read, negative control, no secret access |
| SSRF/callback | Program explicitly permits callback/OAST or provides approved endpoint | Default live bounty; internal probing, metadata, public listener/tunnel not approved | Approved callback domain, one-shot trigger, listener log, no internal scan/metadata |

## Navigation updates after bridge creation

After writing the bridge, update current project navigation so future workers actually consume it:

- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- project Obsidian or equivalent project note
- `handoff/accepted_changes.md`

Add language that future live-target steps must read the bridge and classify the lane before touching the target.

## Authorization gate lesson

Before moving from manual browser-assisted live work to any script/bundle/scanner-like runner, prove the repository gate works:

- exact in-scope target passes dry-run;
- clearly out-of-scope target fails;
- malformed/missing scope fails;
- override remains dry-run-only or otherwise cannot authorize live execution.

If the gate fails closed due to slug/schema/scope-entry incompatibility, record `gate_fail_closed_needs_fix` and keep live work manual until fixed. Fail-closed is safer than accidental allow, but it is not automation-ready.
