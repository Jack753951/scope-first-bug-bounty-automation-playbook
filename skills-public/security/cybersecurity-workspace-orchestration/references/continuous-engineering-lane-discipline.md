> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Continuous Engineering Lane Discipline

Use this when a cybersecurity/bug-bounty workspace pivots from ad-hoc or learning-oriented work into an automated recurring platform.

## Core lesson

Do not treat "continuous engineering" as permission to immediately enable live recurring scans or to open many live bounty lanes. First make the substrate controllable, machine-readable, and fail-closed.

## Recommended sequencing

1. **Now / closeout rung**
   - Make active `scope.json`, `lane_state.json`, queue, and artifact indexes validator-valid.
   - Update active truth files, not new dated strategy files, when the project direction changes.
   - Add routing discipline before adding automation:
     - Tier A: one primary target-touching live bounty lane.
     - Tier B: recurring platform substrate that feeds candidates/inbox.
   - Preserve hard stop rules for scope, policy, sensitive data, callbacks, fuzzing, exploit proof, and final submission.

2. **Next 1-2 engineering sessions**
   - Build the minimum recurring substrate that produces operator-inbox candidates from offline/passive inputs:
     - CVE/PoC intake.
     - CT/scope-change intake.
     - Detector candidate JSON.
     - Artifact/path integrity checks.
     - Dry-run/no-target scheduler harness.
   - Success criterion: an offline/passive signal becomes a candidate record and operator decision without target-touching side effects.

3. **After first end-to-end inbox signal**
   - Add hourly differential recon and daily passive inventory only for policy-allowed scope.
   - Require per-program policy, scope, technique, rate/budget, and stop-before rules before activation.
   - Keep live jobs fail-closed if policy or scope is missing or ambiguous.

4. **After evidence/report packet is stable**
   - Add weekly deep discovery, disclosed-report mining, and monthly metrics/library cleanup.
   - Do not let deep discovery create a pile of untriaged raw logs before the evidence/report pipeline can close findings.

## Tier A / Tier B routing

- **Tier A — primary live lane**: one target-touching live bounty lane active by default. Push it to candidate evidence, report draft, PARK, KILL, or explicit operator-blocked checkpoint before opening another live lane.
- **Tier B — recurring substrate**: scheduled intel/recon/detector work runs as background infrastructure and feeds the operator inbox. It does not hijack Tier A unless it produces a high-confidence, policy-allowed candidate that passes the same lane gate.

## Capability-library anti-learningization rule

Capability-library work is valid when it directly supports:

- the active live lane;
- recurring substrate;
- detector/report/inbox automation;
- reusable proof bundles;
- explicit operator-requested research.

If a live lane can still move toward evidence/report/PARK/KILL, do not use library/index work as a substitute for lane progress.

## Decision vocabulary pattern

Prefer a two-layer model:

- `operator_decision`: EXECUTE, PASSIVE_ONLY/PASSIVE-ONLY, PARK, KILL.
- `machine_state`: detailed runner state such as POLICY_INTAKE, PENDING_OPERATOR_AUTH, SURFACE_MAP, CANDIDATE_REVIEW, EVIDENCE_PACKET, REPORT_DRAFT, PARKED, NO_FINDING, BLOCKED_LOCAL_TOOLING, BLOCKED_NO_OWNED_CONTROL.

This avoids forcing operational runner states into four human decision words while still keeping the operator inbox concise.
