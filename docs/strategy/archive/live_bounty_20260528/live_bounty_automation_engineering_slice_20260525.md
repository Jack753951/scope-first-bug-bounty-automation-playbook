> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Live bounty automation engineering slice

Status: sealed / local-only automation substrate complete
Date: 2026-05-25
Owner: Hermes
Scope: systematic automation, target/lane decomposition, learning-state persistence, and evidence hygiene for authorized live-bounty lanes
Boundary: no new live target requests, no scanner/fuzzer/DAST enablement, no account creation/login, no exploit execution, no report submission, and no new safety approval workflow.
Closeout: `handoff/live_bounty_automation_substrate_closeout_20260525.md` seals this engineering substrate. Do not add more local-only tooling by default before the operator identity/session gate is resolved.

## Why this slice exists

The project had enough policy and handoff structure to run lane-level authorized work, but not enough machine-readable state to resume autonomously after restarts or to let future scripts decide the next safe action. This slice adds the minimal engineering substrate needed for automation and learning:

```text
lane state schema
live evidence schema
machine-readable lane queue
lane status validator/summarizer
redaction precheck for evidence promotion
<program-redacted> seed lane state/evidence checkpoint
focused regression test
```

This is not an extra safety process. It is a systematization layer: it turns the existing project-owner autonomy policy into concrete state files future automation can read.

## Added files

```text
schemas/live_bounty_lane_state.schema.json
schemas/live_bounty_evidence.schema.json
scripts/live-bounty-lane-status.py
scripts/live-bounty-lane-runner.py
scripts/live-bounty-preview-grounding.py
scripts/evidence-redaction-check.py
tests/test_live_bounty_state_and_redaction.sh
tests/test_live_bounty_lane_runner.sh
tests/test_live_bounty_preview_grounding.sh
handoff/live_bounty_lane_queue.json
programs/<program-slug>/lane_state.json
programs/<program-slug>/lane_state_pending_second_account.json
handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_seed_20260525.json
handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md
handoff/live_bounty_preview_grounding_status.json
```

## Machine-readable state model

The lane state schema captures:

```text
program_slug
lane_id
lane_title
autonomy_level
state
status
authorization dry-run status
scope artifacts
allowed/blocked lane actions
operator gates
stop conditions
next_autonomous_action
next_operator_action
artifact pointers
learning preview references / next seed
updated_at
```

Current <program-redacted> state at substrate implementation time, now superseded by the first-flow surface-map closeout:

```text
program: <program-slug>
lane: auth_session_profile_empty_state
autonomy_level: A2
state at implementation time: A2_PENDING_OPERATOR_AUTH
status at implementation time: blocked_operator_action
superseding state: NO_FINDING_CLOSEOUT / no_finding
superseding artifact: programs/<program-slug>/notes/tines_automation_vdp_owned_account_surface_map_20260525.md
next_autonomous_action: none_lane_closed_as_no_finding_surface_only
```

## Evidence model

The evidence schema supports machine-readable, non-promotional live-bounty summaries:

```text
status: no_finding | candidate | needs_manual_review | blocked | blocked_operator_action | blocked_awaiting_scope | surface_only | not_report_ready | report_ready
request_budget planned/used
observations
positive_evidence
negative_controls
redactions
candidate_signals
blocked_states
next_learning_seed
```

The schema intentionally rejects promotional/unreviewed terms such as `verified_reportable`.

## Redaction checker

`scripts/evidence-redaction-check.py` scans local evidence artifacts for common promotion blockers before handoff promotion:

```text
Authorization headers
Set-Cookie headers
Bearer tokens
JWT-shaped values
api_key/secret/token assignments
email addresses
phone-like values
OTP-like lines
```

The checker is local-only and fail-closed. A regression was added so normal ISO dates such as `2026-05-25` do not false-positive as phone numbers. Findings deliberately redact matching line excerpts before printing JSON/stdout so the checker does not re-leak detected token/PII material into logs.

## Lane status helper

`scripts/live-bounty-lane-status.py` validates lane state, optional evidence, and optional queue JSON, then emits a compact JSON summary. It is an orchestration/status helper only; it does not touch targets.

Useful command:

```bash
python scripts/live-bounty-lane-status.py validate \
  --queue handoff/live_bounty_lane_queue.json \
  --state programs/<program-slug>/lane_state.json \
  --evidence handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_seed_20260525.json
```

## Lane runner

`scripts/live-bounty-lane-runner.py` selects the highest-priority queue entry, validates queue/state coherence, and emits the next local orchestration decision as JSON. It is explicitly local-only and does not execute target requests, browser automation, subprocess probes, or scanner-like behavior.

Exit codes:

```text
0  autonomous_local_action_available
10 blocked_operator_action
20 blocked_scope_or_policy
30 invalid_queue_or_state
```

The runner rejects target-like arguments (`--target`, `--url`, `--host`, `--scope`, `--live`) with structured JSON and exit `30`, including bare flags that would otherwise fall through to argparse text. It can also write the same decision JSON to `--status-out` for future schedulers or Hermes wrapper calls.

Useful command:

```bash
python scripts/live-bounty-lane-runner.py \
  --queue handoff/live_bounty_lane_queue.json \
  --status-out handoff/live_bounty_lane_runner_status.json
```

Current queue result is expected to be exit `10` because both active live-bounty lanes are blocked on real operator gates, not because the substrate failed.

## Preview grounding generator

`scripts/live-bounty-preview-grounding.py` reads the same machine queue/state substrate and writes a local-only reference packet under `handoff/references/`. It is designed to improve preview quality and learning without touching targets or importing scanner defaults.

Current <program-redacted> output:

```text
handoff/references/tines_automation_vdp_auth_session_profile_empty_state_grounding_20260525.md
handoff/live_bounty_preview_grounding_status.json
```

The generated packet includes:

```text
OWASP WSTG / ASVS reference-only methodology
PortSwigger Web Security Academy reference-only examples
public report / official-doc comparison guidance
reference-only scanner/template metadata notes, explicitly not execution permission
positive controls
negative controls
blocked techniques
stop conditions
evidence thresholds for no_finding / candidate / needs_manual_review / blocked_operator_action / report_ready
next safe local action and operator gate
```

Target-like arguments (`--target`, `--url`, `--host`, `--scope`, `--live`) fail closed as structured JSON with exit `30`, including bare flags before argparse can emit plain text.

Useful command:

```bash
python scripts/live-bounty-preview-grounding.py \
  --queue handoff/live_bounty_lane_queue.json \
  --output-dir handoff/references \
  --date 2026-05-25 \
  --status-out handoff/live_bounty_preview_grounding_status.json
```

## Validation performed

```bash
bash tests/test_live_bounty_state_and_redaction.sh
bash tests/test_live_bounty_lane_runner.sh
bash tests/test_live_bounty_preview_grounding.sh
python scripts/live-bounty-lane-status.py validate --queue handoff/live_bounty_lane_queue.json --state programs/<program-slug>/lane_state.json --evidence handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_seed_20260525.json
python scripts/evidence-redaction-check.py programs/<program-slug>/lane_state.json handoff/live_bounty_evidence/<program-slug>/auth_session_profile_empty_state/evidence_seed_20260525.json --json
python scripts/live-bounty-lane-runner.py --queue handoff/live_bounty_lane_queue.json --status-out handoff/live_bounty_lane_runner_status.json
python scripts/live-bounty-preview-grounding.py --queue handoff/live_bounty_lane_queue.json --output-dir handoff/references --date 2026-05-25 --status-out handoff/live_bounty_preview_grounding_status.json
```

Observed:

```text
PASS test_live_bounty_state_and_redaction
PASS test_live_bounty_lane_runner
PASS test_live_bounty_preview_grounding
queue status: ok
<program-redacted> lane status: ok
<program-redacted> parked lane status: ok
redaction check: clean
lane runner at substrate implementation time: exit 10 / blocked_operator_action for top queue item (superseded by <program-redacted> closeout; current runner returns lane_closed_or_parked / exit 0)
grounding generator: wrote <program-redacted> reference packet under handoff/references
independent reviewer after fixes: PASS
```

## Independent review loop

A delegated independent reviewer was used after the initial local implementation. The first review returned `REQUEST_CHANGES` with two blockers:

1. The machine queue referenced a missing <program-redacted> state file and queue validation did not fail on missing `state_file` paths.
2. Redaction-check findings printed raw matching excerpts, which could re-leak secrets/PII into logs.

Both blockers were converted into focused regression coverage before fixes. Applied changes:

```text
scripts/live-bounty-lane-status.py now rejects queue entries whose state_file does not exist.
programs/<program-slug>/lane_state_pending_second_account.json now exists for the parked Account A/B lane.
scripts/evidence-redaction-check.py now redacts findings excerpts before output.
tests/test_live_bounty_state_and_redaction.sh asserts both behaviors.
```

A second delegated review returned `PASS` with no remaining blockers.

A later delegated review was used for the lane runner. The first runner review returned `REQUEST_CHANGES` because bare target-like flags such as `--target` would have been rejected by argparse text/exit `2` instead of structured JSON/exit `30`. This was converted into a regression test and fixed by checking target-like args before argparse parsing. The second runner review returned `PASS`.

A delegated review was also used for the preview-grounding generator. It returned `PASS`: no network/process/browser/scanner side-effect APIs were found, target-like bare flags fail closed as structured JSON, generated markdown is explicitly non-authorizing, and the OWASP/ASVS/PortSwigger/reference-only content is useful for safe preview design.

## Next engineering seeds

No further engineering slice is active by default. The substrate is sealed at `handoff/live_bounty_automation_substrate_closeout_20260525.md`.

Reopen only if:

```text
operator explicitly asks for wrapper/promotion tooling
runner/status/grounding test fails
lane schema cannot represent a real new authorized lane
evidence redaction false-positive/false-negative blocks safe promotion
Hermes needs a stable CLI wrapper after repeated manual use
```

Otherwise, no local-only engineering slice is active by default. The <program-redacted> identity/session gate and low-speed owned-account surface map are now complete; any further <program-redacted> work requires a separately approved lane plan rather than more default tooling.
