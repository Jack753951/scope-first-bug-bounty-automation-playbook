> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> authorized attacker-flow packet — first practical run

Generated: 2026-05-26T11:12:31Z
Skill used: `authorized-attacker-flow`
Program: <program-name> / <bug-bounty-platform> `<program-redacted>`
Scope artifact: `programs/<program-redacted>/scope.json`
Execution mode: manual/noVNC browser-only passive observation + minimal owned-account onboarding choices.

## Authorization / boundary

- Authorization basis: explicit bug bounty scope captured in `programs/<program-redacted>/scope.json` from logged-in <bug-bounty-platform> CSV.
- In-scope current asset: `<in-scope-host>`.
- API reference asset: `<in-scope-host>` / public docs, not exercised in this pass.
- Account state: operator reports first owned account was created successfully; Hermes did not store password, phone, OTP, cookies, tokens, or verification links.
- Current stop-before: external/shared channel connection, invite/team actions, customer/outbound messages, API token creation/storage, webhooks/callbacks/OAST/tunnels, third-party integrations, billing/payment/support/KYC, scanner/fuzzer/DAST, report submission.

## Observed passive surfaces

Evidence screenshots:

- `setting/local/screenshots/program-redacted_live_20260526/post_signup_attacker_flow_start.png`
- `setting/local/screenshots/program-redacted_live_20260526/post_signup_onboarding_after_start.png`
- `setting/local/screenshots/program-redacted_live_20260526/post_signup_onboarding_step_after_team_next.png`
- `setting/local/screenshots/program-redacted_live_20260526/post_signup_onboarding_after_inbox_setup_later.png`
- `setting/local/screenshots/program-redacted_live_20260526/dashboard_channel_connect_gate.png`

Observed UI state, redacted:

- <program-name> post-signup welcome screen reached.
- Setup questionnaire asked for primary team; selected `Customer Support` as low-risk owned-account profile customization.
- Shared inbox onboarding appeared; chose `Set up later` to avoid unnecessary owned-object creation during mapping.
- Dashboard/setup guide reached.
- Visible setup guide surfaces: create shared inbox, connect shared channel, automate workflows/rules, discover topics, invite team.
- The active setup path now asks to connect a first shared channel, with external account/channel options such as Gmail / Office 365 / chat or SMS-style channels. This is a hard stop-before for this pass.
- Left navigation shows inbox/open/drafts/later/done/more, shared/demo inbox labels, settings/help surfaces, setup guide, trial/banner actions.
- A <bug-bounty-platform> assistant panel is visible in a separate window; no interaction needed for target proof.

## Candidate packet

```json
[
  {
    "candidate_id": "<program-name>-channel-connect-oauth-boundary",
    "attacker_objective": "Abuse connected shared channels or OAuth/mailbox authorization to access or route messages beyond intended workspace boundaries.",
    "path_hypothesis": "The onboarding channel connection flow may expose authorization, redirect, mailbox selection, or tenant-boundary assumptions.",
    "impact_potential": 5,
    "surrogate_feasibility": 2,
    "authorization_readiness": 2,
    "proof_boundary": {
      "in_scope_assets": ["<in-scope-host>"],
      "owned_accounts_or_objects": ["one operator-owned <program-name> workspace/account"],
      "allowed_state_changes": ["passive UI mapping only in this pass"],
      "blocked_state_changes": ["Gmail/Office365/channel connection", "OAuth consent", "external messages", "third-party integrations", "token capture/storage"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only; no customer/non-owned mailbox data"
    },
    "proof_surrogate": "Preserve as gated candidate; next proof would require operator-owned mailbox/channel and explicit token/redaction plan before any connection.",
    "stop_before": ["OAuth/login consent", "mailbox/channel connection", "token exposure", "external communication", "non-owned data"],
    "evidence_requirements": ["channel gate screenshot", "program rule reference", "owned mailbox/channel approval if later pursued"],
    "execution_status": "needs_operator_control"
  },
  {
    "candidate_id": "<program-name>-invite-role-boundary",
    "attacker_objective": "Escalate or retain access through teammate invite, role, removal, or downgrade boundary mistakes.",
    "path_hypothesis": "Team invite and role surfaces may reveal whether low-privilege users can access admin-only workspace or shared-inbox functions.",
    "impact_potential": 4,
    "surrogate_feasibility": 4,
    "authorization_readiness": 3,
    "proof_boundary": {
      "in_scope_assets": ["<in-scope-host>"],
      "owned_accounts_or_objects": ["Account A exists", "Account B not yet created/approved"],
      "allowed_state_changes": ["passive navigation to role/invite UI without sending invites"],
      "blocked_state_changes": ["sending invite email", "changing roles without second owned account plan", "accessing non-owned data"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned accounts only"
    },
    "proof_surrogate": "Map role/invite UI and preserve exact Account B requirements; execute only after operator creates/approves a second owned account/address.",
    "stop_before": ["send invite", "accept invite", "role change with real impact", "non-owned data"],
    "evidence_requirements": ["screenshots of role/invite options with emails redacted", "Account A/B ownership statement", "expected vs observed permissions"],
    "execution_status": "needs_operator_control"
  },
  {
    "candidate_id": "<program-name>-shared-inbox-object-permission",
    "attacker_objective": "Access or manipulate shared inbox objects without the required workspace/inbox permission.",
    "path_hypothesis": "Shared inbox creation and rules/topics may create object IDs and permission boundaries that can later be checked with a second user or lower privilege role.",
    "impact_potential": 4,
    "surrogate_feasibility": 3,
    "authorization_readiness": 4,
    "proof_boundary": {
      "in_scope_assets": ["<in-scope-host>"],
      "owned_accounts_or_objects": ["operator-owned workspace", "demo/empty owned setup surfaces"],
      "allowed_state_changes": ["passive map only", "redacted screenshot of empty/navigation/settings surfaces only"],
      "operator_gated_state_changes": ["create a clearly named owned test inbox only after explicit operator approval naming label, purpose, redaction plan, and cleanup plan"],
      "blocked_state_changes": ["customer messages", "real outbound communication", "scanner/fuzzer", "non-owned data", "invite/team role mutation", "token/API calls", "workflow save/activation", "OAuth/channel connection", "attachment upload", "shareable-link generation", "comment/message posting", "billing/payment/KYC"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned empty/test objects only"
    },
    "proof_surrogate": "Start with UI/object model inventory and public docs matrix only; object creation is a separate operator-gated proof plan, not part of the current allowed state.",
    "stop_before": ["message send/receive", "external channel connection", "non-owned data", "destructive deletion", "OAuth consent", "shareable-link generation", "attachment upload", "comment posting", "third-party connect", "billing/trial flows", "token/API call", "workflow save/activation"],
    "evidence_requirements": ["object/surface inventory", "redacted screenshots", "expected role/permission matrix", "named owned object labels before any later creation", "positive/negative control plan before any later proof"],
    "execution_status": "needs_multi_agent_review"
  },
  {
    "candidate_id": "<program-name>-workflow-rule-abuse",
    "attacker_objective": "Use workflow/rule automation to trigger unauthorized actions, data exposure, or outbound side effects.",
    "path_hypothesis": "Rule automation may combine conditions/actions across inboxes, channels, or roles in surprising ways.",
    "impact_potential": 4,
    "surrogate_feasibility": 2,
    "authorization_readiness": 2,
    "proof_boundary": {
      "in_scope_assets": ["<in-scope-host>"],
      "owned_accounts_or_objects": ["operator-owned workspace only"],
      "allowed_state_changes": ["passive rule-builder mapping only"],
      "blocked_state_changes": ["activating rules", "sending messages", "external integrations", "webhooks/callbacks"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only"
    },
    "proof_surrogate": "Map available rule conditions/actions without saving or activating rules; choose a local simulation or owned-object proof later.",
    "stop_before": ["save/enable rule", "external action", "message send", "callback/webhook"],
    "evidence_requirements": ["rule-builder option screenshots", "blocked-action list", "no activation confirmation"],
    "execution_status": "blocked_preserve"
  },
  {
    "candidate_id": "<program-name>-api-ui-permission-mismatch",
    "attacker_objective": "Find API endpoints that allow actions the UI/role model should forbid.",
    "path_hypothesis": "Public API (`<in-scope-host>`) and UI features may expose permission mismatches after token handling and role setup exist.",
    "impact_potential": 5,
    "surrogate_feasibility": 3,
    "authorization_readiness": 2,
    "proof_boundary": {
      "in_scope_assets": ["<in-scope-host>", "<in-scope-host>"],
      "owned_accounts_or_objects": ["operator-owned workspace", "second owned role account needed later"],
      "allowed_state_changes": ["public documentation review only in this pass"],
      "blocked_state_changes": ["API token creation/storage", "API calls", "non-owned data", "scanner/fuzzer"],
      "callback_oast_tunnel_allowance": "none",
      "data_contact_boundary": "owned-data-only"
    },
    "proof_surrogate": "Docs-first endpoint/permission inventory; later create redaction-safe API token plan only if operator approves.",
    "stop_before": ["token creation", "API request", "secret storage", "non-owned data"],
    "evidence_requirements": ["docs endpoint inventory", "permission claim references", "token redaction plan if later pursued"],
    "execution_status": "needs_operator_control"
  }
]
```

## Hermes synthesis

Selected lane for continued safe testing: `<program-name>-shared-inbox-object-permission` remains passive/manual UI/docs surface inventory only. <program-name>-specific Claude/Cowork + Codex review has now run and returned REQUEST_CHANGES/BLOCK, so the lane is allowed only as passive mapping, not proof execution.

Reason: it is the only candidate with comparatively high authorization readiness while staying inside the existing single owned account and no-callback/no-external-communication boundary, but multi-agent review found unresolved proof blockers. Actual object creation, permission checking, second-account use, API/token use, channel connection, workflow activation, or any proof beyond passive mapping requires explicit operator approval plus a separate proof boundary update.

Immediate stop reached: the dashboard is prompting for external/shared channel connection. Do not connect Gmail, Office 365, chat, SMS, Slack, WhatsApp, Twilio, <program-name> Chat, webhooks, or any third-party integration in this pass.

Next safe action: continue passive UI mapping through settings/setup-guide/navigation without creating tokens, sending invites/messages, connecting channels, or activating workflows.


## 2026-05-26 BLOCK issue reduction / bundle preservation update

- Added passive docs/object-boundary matrix and preserved bundle set: `programs/<program-redacted>/notes/program-redacted_passive_docs_bundle_map_20260526.md`.
- Tightened `<program-name>-shared-inbox-object-permission`: object creation is no longer listed under allowed state changes; it is an explicit operator-gated future action.
- Preserved all useful bundles instead of narrowing prematurely: inbox membership, non-public group linking, conversation cross-listing, message/comment/draft splits, workflow copy/routing, channel/OAuth boundary, API/UI mismatch, plugin context, archive/delete residue, and metadata-only leak.
- Current state: `BLOCK_BOUNDED_PROOF_BUT_PASSIVE_MAPPING_ALLOWED`; continue only with passive UI/docs mapping unless operator explicitly approves a later bounded proof plan.
