> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> post-signup first run — authorized attacker-flow example

Use this reference as a compact example of applying `authorized-attacker-flow` to a live SaaS bug-bounty target after the operator completes account creation/auth gates locally.

## Scenario

- Program: <program-name> / <bug-bounty-platform> `<program-redacted>`.
- Authorization basis: explicit bug-bounty scope already captured in project scope artifacts.
- Initial condition: operator reported the first owned account was created successfully.
- Execution mode: noVNC/Kali browser-only, low-speed, mostly passive observation.
- Secret boundary: do not store phone numbers, passwords, OTPs, cookies, tokens, API keys, verification links, or session material.

## Safe first-run sequence

1. Confirm post-auth dashboard/onboarding state with screenshot evidence.
2. For product-personalization questions, choose the lowest-risk truthful/default option when it only affects owned-account profile state.
   - Example: choosing a primary team such as `Customer Support` was treated as low-risk owned-account customization.
3. Avoid unnecessary object creation during the first mapping pass.
   - Example: at shared-inbox onboarding, choose `Set up later` instead of creating recommended inboxes when the objective is surface mapping.
4. Stop at any external account/channel connection gate.
   - Example: Gmail, Office 365, Slack, WhatsApp, Twilio, <program-name> Chat, webhooks, SMS/chat channels, or channel settings.
5. Convert visible surfaces into candidates rather than executing them immediately.

## Candidate set produced

- `<program-name>-channel-connect-oauth-boundary` — high impact, but requires owned mailbox/channel, OAuth/token redaction plan, and explicit operator control.
- `<program-name>-invite-role-boundary` — needs second owned account before invite/role tests.
- `<program-name>-shared-inbox-object-permission` — best next bounded lane, but start with passive UI/object inventory; object creation needs a named owned-object plan.
- `<program-name>-workflow-rule-abuse` — preserve as blocked until rule builder can be mapped without saving/enabling rules.
- `<program-name>-api-ui-permission-mismatch` — docs-first only until API token handling/redaction plan is approved.

## Hard stop-before signals observed

- External/shared channel connection prompts.
- OAuth or mailbox provider choices.
- Invite/team-send actions.
- API token creation or token display.
- Workflow/rule save or enable action.
- Any outbound message, customer interaction, or third-party integration.

## Evidence pattern

Capture screenshots of gates and surfaces, but redact or avoid collecting sensitive content. The useful evidence for this stage is:

- dashboard/onboarding state;
- setup guide items;
- visible surface labels;
- proof that the workflow stopped before channel connection/invite/token/callback actions;
- candidate packet with proof boundary and execution status.

## Lesson

For SaaS first-contact work, the practical attacker-flow often starts by preserving high-impact paths while selecting only a low-state-change lane for immediate work. A good first run is successful when it reaches a clear external-action gate and produces a ranked candidate packet without crossing that gate.
