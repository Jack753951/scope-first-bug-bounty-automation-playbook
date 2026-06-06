> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# First-Bounty Target Source Intake

Use this when the operator is adding bounty platforms or asking where to find targets for the first reportable bounty.

## Platform priority

For this project, favor sources that can feed a first-bounty SaaS/access-control lane quickly:

1. HackerOne — primary existing source.
2. Intigriti — strong secondary source, especially SaaS/B2B/web/API programs.
3. Bugcrowd — valuable source, but do not block first-bounty work if login/onboarding is temporarily blocked.
4. YesWeHack — optional extra source after H1/Intigriti are producing candidates.
5. HackenProof/Immunefi — observe unless intentionally pivoting to web3/crypto.
6. Synack — long-term application/onboarding, not a first-week blocker.

## Registration/onboarding rule

Platform registration is source setup, not target authorization. Recording that a platform is registered does not authorize scanning, exploitation, account mutation, or report submission against any program.

If one platform login is blocked, record the friction and continue with available sources instead of losing the sprint. Example status vocabulary:

```text
registered
logged_in
registered_but_login_blocked
not_yet_confirmed
parked_not_first_bounty_source
```

## Candidate intake shape

Before target-touching work, collect candidate programs and score them:

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

Scoring interpretation:

- 15-23: strong candidate; proceed to policy/scope intake and bundle precondition gate.
- 10-14: possible; proceed only if operator cost is low and bundle fit is clear.
- <10: park unless the operator explicitly chooses it.

## First-bounty target traits

Prefer:

- bounty-paying, not VDP-only, when the explicit goal is first bounty;
- fresh/new/updated/scope-expanded programs;
- mid-sized B2B SaaS, web/API, team/workspace/org products;
- self-serve signup and free plan/trial;
- roles, permissions, invites, removal/downgrade lifecycle;
- owned object creation and direct URL/API surface;
- public API docs, SDK, source-available components, changelog, or advisory surface.

Avoid or park quickly:

- payment/KYC/phone before product access unless signal is already strong;
- sales-demo-only products;
- mobile-only/high setup friction targets;
- huge mined-out public programs with no freshness;
- VDP-only/no-reward programs when first paid bounty is the goal;
- unclear scope or programs that do not reward the intended bug class.

## Operator login gates

The operator handles passwords, OTP, CAPTCHA, 2FA, recovery codes, final submit, and any sensitive signup friction. Do not store or echo these values in memory, repo files, reports, screenshots, logs, or prompts.

If the user asks to open platforms in Kali/noVNC, it is allowed to open login pages only. Treat it as platform source setup, not target testing.

## Practical next step

When H1 and Intigriti are available and Bugcrowd is blocked, continue with H1 + Intigriti. Collect 5 candidate programs from each, score 10, choose top 3, then select one top lane for first-bounty run-card creation.
