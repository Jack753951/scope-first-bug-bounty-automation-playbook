> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Target Source Platform Intake

Use this reference when the first-bounty sprint needs fresh target sources from bounty platforms before any target-touching work.

## Recommended platform order for this project class

Primary sources:

1. HackerOne — keep as the main source when an account/workflow already exists; prioritize fresh/private/recently updated/scope-expanded programs over heavily mined public programs.
2. Bugcrowd — strong second source; useful VRT/reward clarity and many web/API/SaaS programs.
3. Intigriti — strong third source; good for European/international B2B SaaS and access-control/API surfaces.
4. YesWeHack — useful backup/diversity source; register when more candidate volume is needed.

Optional / later sources:

- HackenProof — useful mainly if crypto/web3 is in scope; observe before making it a first-bounty main line.
- Immunefi — defer unless deliberately switching to web3/protocol/smart-contract bounty work.
- Synack — long-term/onboarding-heavy; not a fast first-bounty dependency.
- Open Bug Bounty — practice/reputation/source discovery, but not a paid-bounty main line.

Discovery-only sources:

- disclose.io directory — VDP/reward discovery; classify `vdp_only` separately from paid bounty.
- FireBounty — bounty/VDP aggregation.
- ProjectDiscovery Chaos — passive asset/scope discovery only after program authorization is confirmed.
- Public disclosed reports / Hacktivity / CrowdStream / Intigriti disclosures — report-pattern and bundle-learning source, not authorization by itself.

## Intake discipline

Do not immediately test newly found programs. First collect and score candidates.

Minimum useful batch:

```text
5 Bugcrowd programs
5 Intigriti programs
optional: 5 HackerOne / 5 YesWeHack programs
```

For each candidate, record:

```text
platform:
program_name:
program_url:
bounty_or_vdp: bounty / vdp_only / unknown
recently_launched_or_updated: 0-3
self_signup: 0-2
free_plan: 0-2
low_priv_control: 0-3
owned_object: 0-3
scope_clarity: 0-2
operator_cost_low: 0-3
access_control_surface: 0-3
api_or_direct_url_surface: 0-2
total_score: /23
likely_bundle:
decision: EXECUTE / PASSIVE_ONLY / PARK / KILL
operator_gate:
stop_before:
```

Selection rule for first bounty:

- Prefer B2B SaaS with self-serve signup, free/trial access, team/workspace/org model, roles, invite/remove/downgrade lifecycle, owned objects, API/direct URL surface, and clear bounty policy.
- Avoid early payment/KYC/phone gates, sales-demo-only products, unclear scope, reward-disabled programs, VDP-only programs when the goal is paid bounty, and high-friction mobile-only targets unless the signal is unusually strong.
- Do not average effort across platforms. Bias toward the best first-bounty candidate, not equal platform coverage.

## Operator budget nuance

If the operator explicitly says the first-bounty phase can spend several hours of human-gated setup, do not keep applying a strict “5 minutes/day only” assumption. Still score operator cost, but allow higher-cost signup/account-control work when:

- the program has clear paid bounty scope;
- the bundle fit is strong;
- owned A/B controls are feasible;
- the evidence path is likely report-ready;
- the stop-before rule is clear.

High operator budget does not authorize secrets storage, OTP/CAPTCHA handling by the agent, payment/KYC automation, live exploit/fuzz/OAST, or final submission without explicit operator gate.
