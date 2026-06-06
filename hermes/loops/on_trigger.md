> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# On-Trigger Loops

Event-driven, not time-driven. Fire when a specific signal appears.

## Triggers Hermes watches

### 1. Program unsuspend detected

**Source**: daily_sweep step 2 sees `programs/<slug>/lane_state.json.status` flip from `Suspended` to `Active`.

**Actions**:
1. Update lane state: `machine_state: A0_PASSIVE_PARKED` → `A0_READY_FOR_PROMOTION`.
2. Add inbox decision: "Program X unsuspended. Promote lane to A2?" with options EXECUTE_PROMOTE / WAIT / KILL.
3. Do NOT auto-promote. Operator decides.

### 2. Scope diff detected

**Source**: daily_sweep step 2 sees scope.json fields differ from policy fetch.

**Actions**:
1. Write diff to `programs/<slug>/notes/<date>_scope_diff.md` (additions, removals).
2. Update `lane_state.json.policy_drift_detected: true`.
3. Add inbox decision: "Scope changed for X. Re-validate?" with options REVALIDATE / IGNORE_THIS_CYCLE / KILL.
4. If scope shrinks (host removed, out-of-scope expanded): also halt that lane's hourly_diff until operator reviews.

### 3. New candidate scores high

**Source**: daily_sweep step 4 produces a candidate scoring above promotion threshold.

**Actions**:
1. Call Claude with `consult_claude.md` § "Complex policy parsing" task: draft `programs/<slug>/scope.json` first version from the candidate's policy snapshot.
2. Hermes reviews Claude's draft against `SAFETY.md` and policy facts; rejects or accepts.
3. Add inbox decision: "Candidate X enriched. Promote to lane?" with options PROMOTE_TO_LANE / WAIT_FOR_BETTER / KILL_CANDIDATE.

### 4. Operator says "hunt now" on a lane

**Source**: operator writes to inbox or invokes `hermes hunt <slug>`.

**Actions**:
1. Hermes prepares: pull scope, endpoint inventory, owned-org status, previous hunt notes, candidate bundles.
2. Hermes writes `hermes/calls/<ts>_claude_hunt_<slug>.md` with hunt brief.
3. Hermes invokes Claude. Claude drives the session (Playwright + Hermes-prepared inventory).
4. After Claude returns: Hermes integrates findings into `programs/<slug>/findings/<ts>_<finding>.md`.
5. If a candidate finding is flagged: Hermes calls Codex (per `consult_codex.md` § "Second opinion on Claude findings") for deterministic verification.
6. Result lands in inbox with options DRAFT_REPORT / KEEP_INVESTIGATING / DROP.

### 5. Stop condition tripped

**Source**: any loop detects a condition from `stop_conditions.md`.

**Actions**:
1. Halt affected loop.
2. Write to inbox per stop_conditions.md § "How Hermes reports".
3. Log event.
4. Do not auto-recover.

### 6. CVE matches active lane

**Source**: minute_alerts catches a CVE in an active lane's tech stack.

**Actions**:
1. Write match to `programs/<slug>/notes/<date>_cve_match_<cve_id>.md` with: CVE summary, affected product, version constraint, KEV status, public PoC links if any.
2. Daily digest highlights the match.
3. Do not auto-test. Operator / hunt session evaluates.

### 7. Candidate finding flagged for redaction

**Source**: any agent (Hermes / Claude / Codex) detects a draft finding contains unredacted credentials / PII / tokens.

**Actions**:
1. Halt the writing step.
2. Log event.
3. Inbox: "Redaction required on finding X" with the path; do NOT auto-redact (may obscure forensic data).

## Trigger handling order

If multiple triggers fire in one sweep cycle, Hermes processes them in this priority:

1. Stop conditions (always first).
2. Scope shrink (#2 when scope removed).
3. Redaction failure (#7).
4. Unsuspend (#1).
5. CVE match (#6).
6. Scope grow (#2 when scope added).
7. New high-scoring candidate (#3).
8. Operator hunt request (#4) — these are usually interactive and the operator is waiting.

## Boundary

Triggers add inbox decisions and prepare context. They do not execute lane mutations beyond passive state-machine updates. Active state changes (PROMOTE, KILL, SUBMIT) wait for operator.
