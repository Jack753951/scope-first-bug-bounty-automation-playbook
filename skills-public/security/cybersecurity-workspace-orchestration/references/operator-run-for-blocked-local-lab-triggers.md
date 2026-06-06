> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Operator-run scripts for blocked local-lab sensitive triggers

Use this reference when an authorized local-lab cybersecurity proof is valuable, but Hermes' execution layer blocks the exact sensitive trigger with a `BLOCKED` / `Do NOT retry` pattern.

## Core rule

Do not retry variants of the same blocked trigger through Hermes tools. Do not encode, split, disguise, relocate, or otherwise transform the trigger just to get it through automation.

Instead, prepare a human operator-run path:

1. A Kali-side script in the repo, usually under `scripts/labs/operator_<lane>_run.sh`.
2. A matching handoff run-card under `handoff/<lane>_operator_run_card_<date>.md`.
3. A precheck mode that proves setup without sending the sensitive trigger.
4. A human confirmation gate before the one sensitive request/action.
5. One-shot trigger behavior, not fuzzing/looping/scanning.
6. Pre/post health, controls, cleanup, diagnostics, and artifact paths.
7. Hermes review after the operator returns the RunId or artifacts.

## Script shape

Required characteristics:

- `--precheck-only` mode that starts/validates route, target, health, listener or marker readiness, and artifact directories, then exits before the sensitive trigger.
- Fixed local-lab scope: attacker/victim host-only IPs, expected VM names, local target path/port.
- Scope assertions in code, e.g. reject non-`<lab-ip>/24` targets for this lab.
- A clear confirmation phrase, e.g. `RUN_<LANE>_ON_LOCAL_LAB`.
- Exactly one positive trigger after confirmation.
- Bounded timeouts and capped requests.
- Negative/control evidence before the positive trigger when possible.
- Post-health and cleanup by default, with explicit `--no-cleanup` only for debugging.
- Diagnostics on failure: docker ps/logs, listening ports, target logs, route/internet posture.
- Summary file that records status, marker, controls, post-health, artifact paths, and verdict.

## Run-card shape

The run-card should include:

- Why this is operator-run: quote or summarize the blocker and state that Hermes did not retry/bypass.
- Scope and hard boundaries.
- Exact commands to run inside Kali and, if useful, artifact pullback commands from Windows PowerShell.
- Expected proof checklist.
- Exact confirmation phrase.
- Cleanup and internet/NAT posture checks.
- What Hermes should verify after artifacts are returned.

## Good examples from Cybersec Lab

- SSRF true-attacker callback operator path:
  - `scripts/labs/operator_ssrf_true_callback_run.sh`
  - `handoff/ssrf_operator_run_card_20260523.md`
  - Pattern: listener precheck, exact `RUN_SSRF_ON_LOCAL_LAB`, one `/fetch?url=attacker-callback` trigger, callback-source verification, cleanup.

- Deserialization bounded-marker operator path:
  - `scripts/labs/operator_deser_bounded_marker_run.sh`
  - `handoff/deser_operator_run_card_20260523.md`
  - Pattern: invalid/control deserialize request, exact `RUN_DESER_MARKER_ON_LOCAL_LAB`, one marker-only `record_deser_marker(marker)` trigger, `/deser-log` verification, cleanup.

## Classification after operator run

Do not promote just because the operator ran the script. Verify artifacts first:

- pre-health and post-health passed;
- negative/control evidence behaved as expected;
- exactly one positive trigger was sent;
- the marker/callback/evidence is unique to the run;
- cleanup and lab network posture are recorded;
- result is labeled honestly: `verified-impact`, `verified_bounded_marker_lab_only`, `attempted-not-verified`, or `blocked/deferred`.

## Pitfalls

- Do not turn the operator-run route into a safety bypass. It is a transparent human-run handoff for local authorized labs after automation refuses a sensitive action.
- Do not skip precheck-only mode; it is what lets the operator distinguish setup failures from trigger behavior.
- Do not claim a dedicated proof from older broad-family artifacts. Historical artifacts can be context, not evidence for the new wave unless rerun-specific controls and markers exist.
- Do not over-narrow the project to only already-proven lanes. If a trigger is blocked, preserve learning breadth by switching to operator-run, source-level inventory, equivalent disposable target, adjacent safe-marker lane, or mature OSS wrapper.