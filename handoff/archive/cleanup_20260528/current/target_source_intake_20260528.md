> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Target Source Intake — 2026-05-28

Status: active target-source intake
Boundary: registration/source tracking only. This file does not authorize live target testing, scanning, exploitation, account mutation, credential handling, or report submission.

## Registered platforms

| Platform | URL | Status | Notes |
|---|---|---|---|
| <bug-bounty-platform> | https://<bug-bounty-platform>.com | existing primary source | Continue as main source. |
| Bugcrowd | https://bugcrowd.com | registered 2026-05-28; login blocked/failed in Kali on 2026-05-28 | Keep as target source, but do not block first-bounty work on Bugcrowd login. Retry via alternate login/support path later. |
| Intigriti | https://www.intigriti.com | registered and logged in via Kali/noVNC on 2026-05-28 | New source for first-bounty target discovery. |
| YesWeHack | https://www.yeswehack.com | not yet confirmed | Optional next registration/source. |

## First-bounty scoring template

Use this for candidate programs before any target-touching work.

| Field | Score / Value |
|---|---|
| platform |  |
| program_name |  |
| program_url |  |
| bounty_or_vdp | bounty / vdp_only / unknown |
| recently_launched_or_updated | 0-3 |
| self_signup | 0-2 |
| free_plan | 0-2 |
| low_priv_control | 0-3 |
| owned_object | 0-3 |
| scope_clarity | 0-2 |
| operator_cost_low | 0-3 |
| access_control_surface | 0-3 |
| api_or_direct_url_surface | 0-2 |
| total_score | /23 |
| likely_bundle | auth-role-separation / removed-downgraded-stale-access / object-ownership-idor / metadata-only-leak / api-ui-permission-mismatch / invite-membership-lifecycle / other |
| decision | EXECUTE / PASSIVE_ONLY / PARK / KILL |
| operator_gate | none / email / OTP / CAPTCHA / phone / payment / KYC / OAuth / account setup / final submit |
| stop_before |  |

## Triage rule

- 15-23: strong candidate; proceed to policy/scope intake and bundle precondition gate.
- 10-14: possible; proceed only if operator cost is low and bundle fit is clear.
- <10: park unless the operator explicitly chooses it.

## Current next action

Collect 5 candidate bounty programs each from Bugcrowd and Intigriti, then score them against this template. Do not run live tests while collecting candidates; only read platform/program policy pages and public scope text.
