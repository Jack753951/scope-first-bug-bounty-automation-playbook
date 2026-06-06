> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Continuous Engineering Substrate for Bug Bounty Platforms

Use this when a broad authorized bug-bounty workspace pivots from strategy cleanup into durable recurring automation. The goal is to build safe, validated substrate without accidentally activating live target contact or scattering operator time across many lanes.

## Core pattern

1. Split execution into two tiers:
   - Tier A / primary live lane: exactly one target-touching live bounty lane by default. Push it to candidate evidence, report draft, PARK, KILL, or an explicit operator-blocked checkpoint before opening another live lane.
   - Tier B / recurring substrate: offline/passive intelligence, detector candidates, path integrity checks, dry-run scheduler harnesses, and operator-inbox summaries. Tier B feeds decisions; it does not hijack the active live lane.
2. Treat latest-CVE/RCE detector work as background substrate unless program policy and operator approval explicitly allow live proof. Prefer lab/passive detector + candidate signal over exploit-shaped live work.
3. Capability-library work is allowed only when it directly supports the active lane, recurring substrate, detector/report/inbox automation, reusable proof bundles, or explicit operator-requested research. Do not let library/index work replace evidence/report progress while a live lane can move.

## Contract alignment sequence

1. Make all active `programs/<slug>/lane_state*.json` files schema-valid before adding scheduler logic.
2. Separate operator-facing and runner-facing vocabulary:
   - `operator_decision`: `EXECUTE`, `PASSIVE_ONLY`, `PARK`, `KILL`.
   - `machine_state`: detailed runner state such as `A2_PENDING_OPERATOR_AUTH`, `CANDIDATE_REVIEW`, `PARKED`, `NO_FINDING_CLOSEOUT`.
   - During migration, keep `machine_state` mirroring legacy `state` until runners consume the alias.
3. Add a regression that scans every active lane state and fails if schema validity, `operator_decision`, or `machine_state` drift.
4. Repair queue/state coherence after state normalization. A lane queue status must match the lane state's `status`; otherwise local runners should fail closed.

## Minimum safe recurring substrate

Build in this order:

1. Candidate schema for operator-inbox batches.
2. Dry-run/no-target substrate harness:
   - reads offline/passive input fixtures;
   - writes candidate JSON;
   - sets `target_touching=false` and `live_activation_allowed=false`;
   - requires a future policy/scope gate before any live action;
   - rejects `--live` or target-like activation flags.
3. Operator inbox renderer:
   - validates candidate batch schema;
   - renders compact Markdown decisions;
   - includes decision, machine state, source, recommended next step, safety boundary, and references;
   - fails closed if the input claims target-touching behavior.
4. Only after an end-to-end dry-run candidate -> inbox packet exists should hourly/daily passive jobs be considered, and only with per-program policy, scope, technique, and rate-budget gates.

## Validation checklist

Run focused tests before broad review:

- lane contract regression over `programs/*/lane_state*.json`;
- dry-run recurring substrate regression;
- operator inbox summary regression;
- existing live-bounty state/redaction tests;
- existing lane runner tests;
- queue runner smoke test returns the expected operator gate / closed state;
- `git diff --check` on touched files;
- project local review (`hermes review`) when available.

## Safety boundaries to state explicitly

Every accepted-change / handoff note for this class should say the work is offline/local contract and dry-run candidate generation/rendering only, with no live recurring job activation, target contact, scanning/fuzzing/DAST, exploit/callback/OAST/tunnel, credential/token/OTP handling, account mutation, report promotion, or submission.
