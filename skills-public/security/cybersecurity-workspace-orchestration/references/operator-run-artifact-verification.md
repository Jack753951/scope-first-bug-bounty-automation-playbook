> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Operator-run artifact verification for blocked local-lab triggers

Use when a sensitive authorized local-lab trigger was blocked in Hermes (`BLOCKED` / `Do NOT retry`) and the operator later runs a prepared Kali-side script manually.

## Pattern

1. Do not retry or disguise the blocked trigger through Hermes.
2. Prepare or use an operator-run script/run-card with:
   - local-lab scope and fixed target IP/port;
   - `--precheck-only` mode when feasible;
   - exact human confirmation phrase before the sensitive trigger;
   - exactly one positive trigger;
   - baseline/control evidence;
   - post-health, cleanup, diagnostics, and artifact path.
3. After the operator runs it, Hermes may perform artifact verification and read-only posture checks.

## Verification checklist

Pull or inspect artifacts from all relevant VMs/hosts, not just the attacker side, when the script writes remote target-side logs.

Required evidence before upgrading status:

- `summary.md` and `run.log` agree on run id, route, marker, status codes, and verdict.
- Pre-health is successful.
- Negative/control request behaves as expected and does not contain the positive marker.
- Positive response contains the unique marker and expected bounded event type/evidence.
- Server-side log endpoint or target-side artifact confirms the same marker when applicable.
- Post-health is successful.
- Cleanup artifact shows disposable listener/target containers or processes were removed.
- Follow-up read-only checks confirm no leftover disposable container/process when practical.
- Network posture is verified or recorded, especially NAT/Internet closed when that is the lab default.

## Classification discipline

- If all evidence passes, classify narrowly, e.g. `verified_bounded_marker_lab_only` or `verified-impact lab-only`.
- Do not call local-lab proof a public-target finding or bug-bounty report-ready issue by itself.
- Prefer `reusable_methodology / local proof pattern` unless a real authorized scope has separate evidence and reporting authorization.
- If controls or cleanup are missing, keep `attempted-not-verified` or `blocked/deferred` and record the exact missing evidence.

## Record updates

When verified, update the repo truth layers in the same session:

- a dedicated handoff for the verified operator run;
- the relevant reusable bundle;
- vulnerability/proof inventory and current navigation;
- accepted changes;
- project Obsidian note if this workspace uses Obsidian routing.

Keep the update factual and artifact-oriented: route/tool, visible model/runtime if available, artifact root, status, evidence, cleanup/posture, boundary, and next use.