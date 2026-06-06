> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# <program-redacted> VDP first-flow no-finding closeout pattern

Session-derived reference for low-pressure SaaS/VDP first-flow runs where the goal is to complete the legal/scope/account/evidence loop, not to force a finding.

## When this applies

Use for a VDP/thanks-only SaaS program after:

```text
policy intake is complete
minimal host is operator-confirmed in config/scope.txt
dry-run gate passed for one in-scope URL and failed for example.org
operator completed HackerOne alias or equivalent researcher identity gate locally
Kali/noVNC/VM browser is logged in to an owned workspace/account
```

## Safe post-login surface-map lane

For an owned SaaS workspace, keep the first lane to normal UI observation:

```text
stories/dashboard/editor inventory
credentials/resources/API-key empty states
users/team count without raw identity retention
authentication/session settings visibility without unlock/change
account/profile menu inventory
AI/workbench/tool surfaces visible but not used
```

Do not click or trigger:

```text
publish/run/play workflow
send email
automation/workbench prompt/tool/MCP execution
integration connection
webhook/callback/OAST
run-script features
API-key/credential/resource creation
user invite/team mutation
authentication setting unlock/change
cross-tenant or non-owned data tests
scanner/fuzzer/DAST/raw probing of generated workspace subdomain
report submission
```

If the program only whitelisted the research/login host globally, treat a generated owned workspace subdomain as browser-only post-login continuation unless the operator explicitly confirms adding it to scope for scripts. Do not promote it to scanner/script scope merely because the browser reached it.

## Evidence and screenshot hygiene

Promoted evidence should be redacted markdown/JSON only:

```text
raw account name/email omitted
password/OTP/verification link/cookie/token/API key not requested or stored
workspace/account identifiers summarized as Account A / owned workspace / 1 owner context
screenshots containing account identifiers remain transient local observation aids
```

If temporary noVNC screenshots were saved under a handoff path, move them to ignored local storage such as:

```text
setting/local/screenshots/<program>_surface_<date>/
```

Then update markdown/JSON evidence to say screenshots were not promoted.

## Closeout state

A completed first-flow no-finding lane should close cleanly instead of remaining blocked on the earlier login gate:

```text
lane_state: NO_FINDING_CLOSEOUT / no_finding
evidence_status: surface_only
queue_status: no_finding
runner_decision: lane_closed_or_parked
runner_target_touching: false
next_autonomous_action: none_lane_closed_as_no_finding_surface_only
report_status: no report packet; no vulnerability observed
```

The runner/checkpoint tooling should treat `no_finding`, `surface_only`, and `parked` as terminal local statuses, not invalid queue states.

## Consolidation checklist

After closeout, update:

```text
programs/<program_slug>/lane_state.json
handoff/live_bounty_lane_queue.json
handoff/live_bounty_evidence/<program>/<lane>/evidence_surface_map_<date>.json
handoff/<program>_owned_account_surface_map_<date>.md
handoff/accepted_changes.md
handoff/current_navigation.md
handoff/active_strategy_queue.md
project Obsidian note
live-bounty bridge/reference if the no-finding teaches a reusable pattern
```

Run focused validation where available, especially redaction checks and runner tests. If a combined validation command exits fail-closed after the lane is otherwise closed, record it as a local validation follow-up, not as a live-target risk or reason to keep probing the target.
