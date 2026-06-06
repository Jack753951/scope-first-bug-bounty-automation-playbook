> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Engineering Direction (CURRENT)

Status: active
Updated: 2026-05-28 (restructure)
Authority: this file is the active engineering direction. Edit in place; do not create dated variants.

## Why this file exists

Earlier phases produced 380+ handoff files / 20 policy variants / 30+ proof bundles and **0 bounty submissions**. Root cause: substrate (docs, policy, multi-agent ceremony) grew faster than outcome (candidate evidence, lane closeout). Restructure 2026-05-28 collapsed the substrate; this file keeps the direction honest going forward.

## North Star

```
30 days: first report-ready draft / submission candidate.
```

All inbox / dry-run / detector / cleanup / scheduler work serves this. Do not add infrastructure that doesn't connect to a current candidate or lane.

Execution stance: model the full attacker path, execute only bounded authorized proof, stop before unauthorized access / non-owned data / destructive impact / DDoS / credential theft / persistence / submission. (Full version in `/SAFETY.md`.)

## High-value zones

1. **Latest vulnerabilities × latest targets** — fresh CVE/advisory/PoC × newly-launched/updated/scope-expanded program. This is the first-bounty intersection.
2. If no intersection ready: run `fresh_vuln_lane` (CVE → local proof → scoped match) and `fresh_target_lane` (new program → access-control bundle → owned-control proof) in parallel.

Do not let latest-vuln work become detector sprawl. Do not let latest-target work become signup drift.

## Active priorities (in execution order)

### P0 — Operator inbox v0 (Batch 7)

`scripts/build_operator_inbox.py` reads lane states + freshness candidates, emits `handoff/operator_inbox_<date>.md` with ≤5 decisions, each `situation + 3 options + default`. Acceptance: produces a markdown file when run; user can act on it in <5 minutes.

### P1 — <program-redacted> Public Bug Bounty policy review (operator)

Highest-leverage move. Operator does the logged-in Intigriti policy read; driver creates `programs/<program-slug>/scope.json` + `lane_state.json` from those facts. Until then no <program-redacted> lane exists.

### P2 — Move one Tier A lane (Batch 8)

Either <program-redacted> human-check or <program-redacted> TW second-account. Both `park_expires_at: 2026-06-04`. By that date, either lane has progressed to A2_SURFACE_MAP / CANDIDATE_REVIEW or it's KILL'd.

### P3 — Daily sweep (deferred until P0 ships)

Detector backlog (haproxy/apache/tomcat/openssl version fingerprints, daily_sweep chainer) waits until the inbox has a consumer path. Detectors that emit candidates nobody reads = substrate.

### P4 — Continuous monitoring (deferred until P3 ships)

disclose.io diff, chaos JSON diff, CVE PoC GitHub diff. Same rule — only after inbox+detector chain produces operator-actionable items.

## Standing rules

**Must do:**
- Every target-touching action verified by `safe_target` against `config/scope.txt` × `programs/<slug>/scope.json`.
- Every new script: brief OSS check first (OWASP / PortSwigger / PayloadsAllTheThings / project source). Record `adopt|wrap|adapt|reference-only|write-custom` in commit or note.
- Every evidence packet runs `scripts/evidence-redaction-check.py` before promotion.
- Every commit batched by intent (structure / policy / code / tests / lane state / archive).

**Must NOT do:**
- No new policy/strategy `.md` without driver advisory.
- No dated navigation/queue variants. Edit the active file.
- No worker handoff in `handoff/` root — new working notes go in `handoff/current/` (which itself gets archived after each batch).
- No account state mutation without operator safe-phrase.
- No `git reset --hard`, `git clean -fdx`, mass-delete on lane state / scope / evidence / governance.
- No silent overwrite of `handoff/accepted_changes.md`.

## Backlog (claimable, ≤4h each)

| # | Task | Path | Status |
|---|---|---|---|
| 1 | `build_operator_inbox.py` | `scripts/build_operator_inbox.py` | **next (Batch 7)** |
| 2 | HAProxy <specific-cve-id> fingerprint | `scripts/detectors/haproxy_cve_2026_33555.py` | deferred until P3 |
| 3 | Apache httpd batch fingerprint | `scripts/detectors/apache_httpd_latest_batch.py` | deferred |
| 4 | Tomcat 11.0.21 fingerprint | `scripts/detectors/tomcat_11_0_21_batch.py` | deferred |
| 5 | OpenSSL 3.0.18 fingerprint | `scripts/detectors/openssl_3_0_18_batch.py` | deferred |
| 6 | `daily_sweep.py` chainer | `scripts/daily_sweep.py` | deferred |
| 7 | `disclose.io` diff | `scripts/disclose_io_diff.py` | deferred |
| 8 | Chaos JSON diff | `scripts/chaos_bugbounty_diff.py` | deferred |
| 9 | CVE PoC GitHub diff | `scripts/cve_poc_github_diff.py` | deferred |
| 10 | Bundle metadata index | `tools/bundle_index.py` | deferred |
| 11 | vuln-intel → bundle coverage diff | `tools/vuln_intel_to_bundle_index.py` | deferred |
| 12 | Bugcrowd / Intigriti / YesWeHack intake template | merged into operator_inbox v0 | deferred |

## What NOT to build next

- New multi-party review / governance policy variants.
- New schema/contract unless an existing module is about to use it.
- New OSS recon ceremony or review-tier doc.
- Anything that adds an abstraction layer before P0 ships.

If tempted to write one of the above: stop, add the idea to the backlog table, decide after P0–P2 closeout.

## Acceptance / review cadence

- Weekly (Sundays): one lane state change or KILL. No exceptions. If none happened, document why in `accepted_changes.md` and adjust priorities.
- Monthly: file-count review. If repo crosses 200 active (non-archive) files without proportional submission output, re-evaluate.

## How to update this file

Edit in place. If direction changes materially: rename current version to `docs/strategy/archive/CURRENT_<date>.md` and rewrite under the same name. No `_v2`, no dated variants in active path.
