> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Daily Sweep

Runs once per UTC day. Default cadence: invoked by `hermes daily-sweep` from cron / Task Scheduler at 07:00 UTC.

## Order of steps

Each step is independent. If one fails, the others continue. Failures log to `hermes/state/hermes_log.jsonl` and surface in the digest.

1. **Bootstrap check**
   - Read `SAFETY.md`, `INDEX.md`, `.hermes.md` into context.
   - Verify `hermes/state/hermes_state.json` exists; if missing, initialize.
   - Check all stop conditions in `hermes/policies/stop_conditions.md`. If any tripped, halt the rest of this sweep.

2. **Active lane status refresh**
   - For each lane in `handoff/live_bounty_lane_queue.json`:
     - Fetch program detail page via Playwright (logged in if needed).
     - Compare current `status` / `scope` / `bounty_band` vs cached.
     - On change: update `programs/<slug>/lane_state.json` (passive fields only), write event to log.
     - Notable changes (Suspended ↔ Active, scope add/remove, bounty raise/drop) → flag in digest.

3. **Deadline check**
   - For each lane with `park_expires_at`:
     - If past expiry → write to inbox: recommend KILL or operator extension.
     - If within 48h → write to inbox as upcoming.

4. **Intake scoring**
   - Read `handoff/pending_intake.json`.
   - For each candidate: re-score (signup friendliness × bounty potential × scope size × activity recency × first-bounty fit).
   - Re-fetch program status for top 5 candidates (skip Suspended without flag).
   - Write updated `pending_intake.json`.
   - **Empty-state rule**: if `pending_intake.json.candidates = []` AND `handoff/live_bounty_lane_queue.json.lanes = []` AND `handoff/current_navigation.md` lists recommended programs under "Highest-priority operator action", surface a `pick_target` decision in the inbox (step 8). Do **NOT** auto-promote any recommendation to a lane — operator must explicitly choose.

5. **CVE / KEV diff**
   - Pull latest NVD / KEV / vendor advisories since last sweep.
   - For each new entry: check intersection with active lanes' tech stacks.
   - If intersection: append to lane's `programs/<slug>/notes/<date>_cve_match.md` and flag in digest.
   - Always: write `intelligence/cve_briefs/cve_brief_<date>.md` summary.

6. **CT log diff** (passive recon)
   - For each in-scope wildcard in active lanes' scope.json: query CT log for new certs since last sweep.
   - New subdomains → add to lane's `programs/<slug>/notes/<date>_new_subdomains.md`.
   - Do NOT auto-probe new subdomains. That belongs to hourly_diff.

7. **Drift detection** (weekly only — skip on non-Monday)
   - Run `INDEX.md` § Drift-detection checks.
   - Flag results in digest.

8. **Regenerate operator inbox**
   - Build today's `handoff/operator_inbox_<date>.md` from queue + pending_intake + flagged events.
   - Replaces yesterday's file pointer in handoff.

9. **Write daily digest**
   - `hermes/digests/<date>.md` — summary of what this sweep did, what changed, what needs operator attention.
   - Cross-link to inbox.

10. **Update state**
    - `hermes/state/hermes_state.json` — set `last_daily_sweep_at: <ts>`, `daily_sweep_status: ok|partial|failed`.
    - Append summary line to `hermes/state/hermes_log.jsonl`.

## Boundary

This loop is read-mostly. Only writes Hermes-owned files per `autonomous_actions.md`. No browser interactions beyond reading policy/CT pages. No Claude/Codex calls — those happen on-trigger after Hermes detects a need.

## Failure modes

| Failure | Recovery |
|---|---|
| Intigriti page fetch returns 5xx | Skip lane status for that program; flag in digest. Three consecutive days → halt step 2 for that lane (stop condition #2). |
| Token budget exceeded mid-sweep | Halt remaining steps; write inbox; digest partial. |
| `handoff/live_bounty_lane_queue.json` malformed | Halt step 2; write inbox; do not auto-repair. |
| Drift detected | Step 7 records; sweep continues. Operator decides cleanup. |

## Re-run

Idempotent. Operator can `hermes daily-sweep --force` to re-run mid-day. The inbox file overwrites; the digest appends a "re-run at HH:MM" section.
