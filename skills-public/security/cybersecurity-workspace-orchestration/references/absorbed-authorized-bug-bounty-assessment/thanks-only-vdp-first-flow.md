> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Thanks-only / VDP first complete-flow pattern

Use this reference when the operator wants to practice a full bug-bounty/VDP workflow on a low-pressure program where the likely outcome is thanks/no-finding rather than bounty.

## Goal

Optimize for a complete, legally bounded workflow rather than vulnerability yield:

```text
passive program shortlist
-> selected program policy intake only
-> program-specific scope.json draft
-> operator-confirmed global scope entry
-> dry-run gate: exact in-scope pass + obvious out-of-scope fail
-> account/session run card
-> manual low-speed single-account surface map
-> no-finding/candidate/report-readiness classification
-> post-proof consolidation
```

A no-finding result is acceptable if it validates the workflow, scope gates, account handling, evidence discipline, and stop conditions.

## Passive shortlist criteria

Prefer programs with:

- VDP / thanks / response-only posture;
- public submission open;
- clear account-creation guidance;
- dedicated researcher signup/login paths;
- normal consumer/SaaS account surfaces that can be tested with one owned account;
- policy text that supports owned-account testing.

Avoid first-run programs involving:

- government, finance, health, reservation/payment/state-changing flows;
- CDN/edge/infra or cloud database surfaces;
- device/mobile/firmware/Bluetooth requirements;
- ambiguous third-party ownership;
- workflows requiring external callbacks, webhooks, integrations, publish/share, KYC, payment, or multi-account behavior.

## Policy intake boundaries

Policy intake may query the platform/program page or public program metadata. Do not navigate to target assets yet. In the intake artifact, state explicitly:

```text
policy/metadata read only
no target asset request
no account signup
no scope expansion
no scan/fuzz/exploit
no credential handling
no report submission
```

Create:

```text
programs/<program_slug>/scope.json
handoff/<program_slug>_phase5a_dry_run_packet_<date>.md
```

Mark the scope artifact as pending operator confirmation until the global whitelist is updated.

## <program-redacted> VDP session-derived example

For `tines_automation_vdp`, the policy intake found dedicated research paths:

```text
https://login.<program-redacted>.com/research/signup
https://login.<program-redacted>.com/research/login
```

It also required either a HackerOne email alias or this exact HTTP header:

```text
X-HackerOne-Research: [H1 username]
```

Pitfall: do not silently rename this to `X-HackerOne-Researcher`; preserve the exact policy spelling.

For browser-only first flows, prefer the HackerOne email alias when available because custom headers require proxy/header-injection setup before target-touching requests. If using a non-HackerOne-domain email without the required header, policy may allow account deletion or program exclusion.

Recommended first lane shape:

```text
researcher-account auth/session/profile/workspace empty-state surface map
manual Kali/noVNC browser
low-speed
one owned account
normal UI only
```

Blocked for first lane:

```text
scanner/fuzzer/DAST
DoS/rate-limit testing
external callbacks/OAST/webhooks
third-party integrations
workflow execution
run-script feature testing
secrets/API key creation or storage
cross-tenant access attempts
tenant/team invitations or other-user interaction
public sharing/publishing
non-owned account/data access
```

## Dry-run gate pattern

After the operator confirms adding the minimal host to `config/scope.txt`, run a paired dry-run:

```bash
HACKLAB="$PWD" ./recon.sh --dry-run --program <program_slug> --policy-mode dry-run https://<in-scope-host>/<selected-path>
HACKLAB="$PWD" ./recon.sh --dry-run --program <program_slug> --policy-mode dry-run https://example.org/
```

Expected:

```text
in-scope: pass
example.org: fail out-of-scope
```

This verifies dry-run readiness only. It does not authorize scanners or automation.

## Post-login no-finding closeout

After the operator completes the alias/header identity gate locally and the noVNC/VM browser is logged in, continue within the approved browser-only lane until `lane_complete_or_exhausted`. For SaaS workspaces, observe normal owned-account UI only: dashboard/story/editor inventory, credentials/resources/API-key empty states, users/team count without raw identity retention, authentication/session settings visibility without unlock/change, and account menu/workbench surfaces without execution.

Do not promote generated owned-workspace subdomains into script/scanner scope just because the browser reaches them after login. If only the login/research host is in `config/scope.txt`, keep the generated workspace subdomain as browser-only post-login continuation unless the operator explicitly confirms additional scope.

Temporary noVNC screenshots can help the agent understand the UI, but screenshots containing account identifiers should not remain in `handoff/` or promoted evidence. Move them to ignored local storage and keep official evidence as redacted markdown/JSON.

A clean no-finding closeout should update queue/state from the prior operator gate to terminal status:

```text
lane_state: NO_FINDING_CLOSEOUT / no_finding
evidence_status: surface_only
runner_decision: lane_closed_or_parked
target_touching: false
next_autonomous_action: none_lane_closed_as_no_finding_surface_only
```

See `<program-redacted>-vdp-no-finding-closeout.md` for the session-derived concrete pattern.

## Output classification

Expected first-run outcomes:

```text
no_finding
surface_only
blocked_operator_action
blocked_awaiting_scope
candidate
```

Do not claim cross-tenant/account isolation findings without owned Account B / second tenant / explicit test-account guidance and a separate plan with positive and negative controls.
