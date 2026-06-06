> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> Account B owned/passive surface map — 2026-05-26

## Reviewer identity

- Reviewer route/tool: Hermes CLI agent + Kali/noVNC screenshot observation
- Visible runtime model: not exposed by tool for vision helper; Hermes active model in session metadata
- Provider / CLI version if visible: not exposed by tool
- Review focus: live-bounty passive owned-account surface mapping and evidence hygiene
- Limitation: browser session cookies/tokens/secrets were not inspected; screenshots are local-only and may contain account/workspace labels.

## Status

- Program: `<program-redacted>` / <program-name>
- Lane: `owned_account_signup_profile_workspace_surface_map`
- Status: `surface_only` / `not_report_ready`
- Timestamp: `2026-05-26T15:36:14Z`
- Evidence JSON: `handoff/live_bounty_evidence/<program-redacted>/owned_account_signup_profile_workspace_surface_map/evidence_surface_map_20260526.json`
- Local screenshot directory: `setting/local/screenshots/program-redacted_live_20260526/`

## Boundary respected

No scanners/fuzzers/DAST, no target-touching scripts, no API token/API call, no OAuth/mailbox/channel connection, no workflow/rule activation, no invite/team membership mutation, no outbound message/comment/discussion, no customer/non-owned data, no credential/OTP/cookie/token/API-key storage, and no report submission.

## Observed sequence

1. Operator completed Account B signup/auth locally without sharing phone/OTP/password/secrets.
2. Hermes observed Account B at <program-name> authenticated onboarding/dashboard state.
3. Low-risk onboarding choices were used only to reach an owned dashboard:
   - primary team: Customer Support;
   - channel/tool survey skipped;
   - recommended shared inboxes created owned labels `Support` and `Support - Priority`;
   - shared email connection skipped/set up later.
4. Current dashboard shows owned shared inbox surfaces and a hard gate to connect the first shared channel.
5. Setup guide confirms `Create your first shared inbox` completed and keeps `Connect your first shared channel`, `Automate workflows... with rules`, `Discover your Topics`, and `Invite your team` as remaining gated tasks.

## Useful candidate families preserved

- Shared inbox membership / recommended inbox default object creation.
- Team/invite boundary.
- Workflow/rule routing boundary.
- Topics dependent on connected channel.
- Channel/OAuth/API/UI mismatch boundary.

## Stop-before list still active

- Stop before Gmail/Office 365/channel/OAuth/mailbox/webhook/integration connection.
- Stop before invite send, role/team mutation, or external recipient contact.
- Stop before saving/activating workflow/rules or Topics if it changes routing/state.
- Stop before API token creation/API calls or token/cookie capture.
- Stop before accessing non-owned/customer data or sending any message/comment/discussion.
- Stop before scanner/fuzzer/DAST or target-touching automation.
- Stop before report-ready evidence promotion or report submission.

## Current next safe action

Passive UI/docs mapping only, or prepare a fresh proof boundary for one owned A/B candidate and ask for explicit operator approval before any state-changing action.
