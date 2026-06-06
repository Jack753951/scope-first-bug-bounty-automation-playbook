> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-redacted> VDP owned-account surface map

Status: surface_only / no finding
Date: 2026-05-25
Owner: Hermes
Program: <program-redacted> VDP (`<program-slug>`)
Lane: `auth_session_profile_empty_state`
Boundary: low-speed browser-assisted owned-account observation only. No scanners, fuzzers, DAST, callbacks, webhooks, workflow execution, run-script testing, integrations, cross-tenant tests, non-owned data access, credential/API-key storage, report submission, or setting changes.

## Authorization and identity gate

- Authorization source: <bug-bounty-platform> <program-redacted> VDP policy captured in `programs/<program-slug>/scope.json`.
- Identity strategy used: <bug-bounty-platform> researcher alias email handled locally by the operator.
- Operator-local gate completed: email verification/signup/login completed in Kali/noVNC before Hermes continued.
- No password, OTP, verification link, cookie, token, or raw email address was recorded in this artifact.

## Route and request posture

- Tool/route: Kali VM Chromium via noVNC, single tab/profile for <program-redacted> (`/home/kali/browser-profiles/<program-redacted>-hermes`).
- Speed: manual/low-speed observation.
- Workspace: post-signup generated owned workspace under a <program-redacted> tenant subdomain. The exact tenant slug is visible in the browser but not promoted into global scope config in this pass.
- Global scope config still only includes `login.<program-redacted>.com` for <program-redacted>; this pass treated the generated workspace as a normal post-login owned-account continuation, not as authorization for scanner/script automation.

## Observed surfaces

| Surface | Observation | Status |
|---|---|---|
| Research signup/login | Operator completed alias-based signup/login and browser reached the <program-redacted> app. | identity gate complete |
| Stories dashboard | Dashboard visible with one onboarding story titled `Your first story`, table filters/search, `New` story control, and right-side onboarding/help panels. | surface_only |
| Story editor | Existing onboarding story visible with sample nodes for `Simple Weather API` and `Send Email`; `Publish` control visible. | blocked_state_change; no execution |
| Credentials | Credentials page visible; empty state says no credentials; `New`/plus controls visible. | no_finding; secrets flow blocked |
| Resources | Resources page visible; empty state says no resources; `New`/plus controls visible. | no_finding; creation blocked |
| Users/settings | Users settings visible with one tenant owner and invite/new controls. Raw account identity was not recorded. | surface_only; invite blocked |
| API keys | API Keys settings visible; empty state says no API keys; `New`/plus controls visible. | no_finding; key creation blocked |
| Authentication settings | Session timeout, recovery-code, SSO, and user-provisioning settings visible; sensitive changes require unlock. | no_finding; mutation blocked |
| Workbench | Workbench visible with templates/stories/MCP tabs, many not-connected integrations/templates, chat input, model selector, and new-chat controls. | surface_only; AI/tool execution blocked |
| Account menu | Account menu visible with Profile, favorites/recent stories, UI theme/help/support, and logout options. | surface_only; profile details not opened |

## Positive evidence

- Login/session persisted after navigating from signup/login into the generated owned workspace.
- Workspace and settings pages load for the owned account.
- Empty states for credentials, resources, and API keys are clear and do not expose pre-existing secrets.
- Users page showed only the operator-owned account context in this newly created tenant; no third-party user data was pursued or retained.
- Authentication/security settings appear gated for changes; Hermes did not click unlock or mutate values.
- Workflow/story execution and publishing controls are visible but were not used.

## Negative controls and stop conditions respected

- Did not click `Publish`, play/run story, execute workflow, send email, connect integrations, create credentials/resources/API keys, invite users, alter authentication settings, or use Workbench chat/tool execution.
- Did not perform raw HTTP probing against the generated workspace subdomain because it is not mirrored into `config/scope.txt` and this lane remained browser-only.
- Did not retain password, OTP, verification link, cookies, tokens, API keys, raw alias email, or screenshots containing account identifiers as promoted evidence. Temporary noVNC screenshots were moved out of `handoff/` into ignored local storage under `setting/local/screenshots/tines_surface_20260525/`; markdown/JSON evidence remains redacted.
- Stopped at `lane_complete_or_exhausted` for the first owned-account empty-state map.

## Candidate/reportability status

Status: `surface_only` / `no_finding`.

No reportable vulnerability was observed in this first conservative pass. The run still has project value because it proves the <program-redacted> identity gate, validates the low-speed noVNC route, identifies sensitive first-lane surfaces, and records which controls must stay blocked for any later deeper test.

## Next safe action

Default: close this first <program-redacted> lane as `no_finding` unless the operator wants a second, separately approved plan.

Possible later lanes, each requiring an explicit new plan before execution:

1. Read-only profile/account page review with strict no-PII retention.
2. API documentation/policy review for whether any owned-account API checks are allowed.
3. Owned-account access-control checks only if a second owned account or sanctioned test account exists.
4. Workbench/MCP/template behavior review without executing tools, only if policy permits and a no-execution observation plan is written.

Do not proceed to integrations, webhooks, run-script, workflow execution, callbacks, or cross-tenant testing without separate operator approval and controls.
