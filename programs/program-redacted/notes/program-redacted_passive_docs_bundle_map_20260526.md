> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> passive docs/object-boundary bundle map — BLOCK issue reduction

Status: passive docs/reference mapping only; not proof-ready
Date: 2026-05-26
Program: <program-name> / <bug-bounty-platform> `<program-redacted>`
Candidate focus: `<program-name>-shared-inbox-object-permission`
Boundary: public documentation review and local handoff edits only. No app/browser session, no account action, no object creation, no invite, no role change, no token/API call, no workflow activation, no channel connection, no customer/non-owned data, no scanner/fuzzer/DAST, no report submission.

## Why this exists

This resolves the parts of the previous BLOCK that can be resolved without touching the live app:

- tighten proof-boundary language so object creation is not hidden inside `allowed_state_changes`;
- build an expected object/permission surface matrix from public docs;
- preserve every useful bundle/hypothesis instead of narrowing too early;
- define passive-only next tests and the remaining hard gates.

It does not resolve operator-gated blockers: Account B, second tenant, owned test object approval, token/API handling approval, channel/OAuth approval, or final proof authorization.

## Public docs pass used

Reference-only docs observed from `dev.frontapp.com`:

- `https://dev.frontapp.com/llms.txt` lists markdown/reference pages for <program-name> Platform documentation.
- `add-inbox-access.md`: `POST /inboxes/{inbox_id}/teammates`, gives access to teammates, required scope `inboxes:write`.
- `removes-inbox-access.md`: `DELETE /inboxes/{inbox_id}/teammates`, removes teammate access, required scope `inboxes:write`.
- `list-teammate-inboxes.md`: returns inboxes a teammate has access to, required scope `inboxes:read`.
- `list-team-inboxes.md`: lists inboxes belonging to a team/workspace, required scope `inboxes:read`.
- `list-inbox-conversations.md`: lists conversations in an inbox, required scope `conversations:read`.
- `list-conversation-inboxes.md`: lists inboxes in which a conversation is listed, required scope `inboxes:read`.
- `list-conversation-messages.md`: lists messages in a conversation, required scope `messages:read`.
- `list-conversation-comments.md`: lists comments in a conversation, required scope `comments:read`.
- `list-conversation-drafts.md`: lists drafts in a conversation, required scope `drafts:read`.
- rule references list company/team/teammate rules with required scope `rules:read`.
- teammate group references show non-public inbox linking to groups and automatic linking of public inboxes through teams.
- plugin references: `listInboxes` lists inboxes accessible by current teammate; `listChannels` lists channels accessible by current teammate; `fetchPath` exposes `/inboxes/...` route context; `listMessages` only lists loaded/current-context messages.

## Expected object/permission model to check later

Expected boundary claims to treat as hypotheses, not findings:

| Surface | Expected boundary | Passive evidence now | Later proof gate |
|---|---|---|---|
| teammate -> inbox access | teammate should only see inboxes granted directly, via team/workspace, or via teammate group | docs show list teammate inboxes and add/remove access endpoints | Account B or owned teammate required |
| inbox -> conversations | conversations in an inbox require conversation/inbox access | docs show inbox conversation and conversation inbox endpoints | owned conversation/object required; no customer data |
| conversation -> messages/comments/drafts | message/comment/draft read should require current user's access to that conversation/context | docs show read scopes split across messages/comments/drafts | owned non-sensitive conversation only; no outbound send |
| team/workspace inboxes | team inboxes belong to workspace/team and may be public/non-public | docs show team inbox endpoints and teammate-group linking language | Account B or second workspace needed |
| teammate groups | groups can gain team and non-public inbox access | docs show group-team and group-inbox relations | explicit role/group plan needed |
| channels | accessible channels are per current teammate / inbox context | docs show listChannels and channel API | channel/OAuth approval needed; currently blocked |
| rules/workflows | company/team/teammate rules can reference actions/conditions | docs show rule read endpoints | passive builder/docs mapping only; no save/activation |
| plugin/client context | plugin context may see current loaded conversation/messages and `/inboxes` path | docs show fetchPath/listMessages/listInboxes/listChannels | plugin lane separate; no app install/build now |

## Preserved bundle set — do not exclude useful bundles yet

These are preserved as bundles, not authorized tests. `bundle` here means a related hypothesis family that may later become a bounded proof, local simulation, or parked lane.

1. `BUNDLE-A-inbox-access-membership`
   - Hypothesis: direct teammate access, team/workspace access, and group-derived access can diverge.
   - Future proof need: Account B / owned teammate, named inbox, expected matrix.
   - Current state: passive-only.

2. `BUNDLE-B-non-public-inbox-group-linking`
   - Hypothesis: non-public inboxes linked/unlinked through teammate groups may leak or persist access unexpectedly.
   - Future proof need: teammate group plan, no SCIM-managed group mutation, owned test group/inbox only.
   - Current state: preserve; no group creation/modification now.

3. `BUNDLE-C-conversation-inbox-cross-listing`
   - Hypothesis: a conversation listed in multiple inboxes may expose metadata/messages/comments through one path after access is removed in another.
   - Future proof need: owned conversation created without outbound communication or imported safely under approval.
   - Current state: preserve; no conversation creation/import now.

4. `BUNDLE-D-message-comment-draft-split`
   - Hypothesis: `messages:read`, `comments:read`, and `drafts:read` boundaries may not align with UI permissions or conversation visibility.
   - Future proof need: owned draft/comment/message surrogate and API/token plan; probably separate API/UI lane.
   - Current state: docs-only.

5. `BUNDLE-E-rule-workflow-permission-copy`
   - Hypothesis: rules/workflows may copy, assign, tag, move, or expose conversations across inbox/team boundaries.
   - Future proof need: rule builder passive mapping first; save/activation explicitly blocked.
   - Current state: preserve as `<program-name>-workflow-rule-abuse`.

6. `BUNDLE-F-channel-oauth-shared-inbox`
   - Hypothesis: shared channel/OAuth connection may bind mailbox/channel to wrong workspace, teammate, or inbox boundary.
   - Future proof need: operator-owned mailbox/channel approval and token/redaction plan.
   - Current state: blocked at channel-connect gate.

7. `BUNDLE-G-api-ui-permission-mismatch`
   - Hypothesis: API scopes or object IDs allow reads/writes the UI/role model should forbid.
   - Future proof need: token handling/redaction plan; Account B/role matrix; no raw token storage.
   - Current state: public docs-only.

8. `BUNDLE-H-plugin-client-context-leak`
   - Hypothesis: plugin/client context methods might reveal accessible inbox/channel/message state inconsistent with UI permission boundary.
   - Future proof need: separate plugin/app lane, no installation or code execution in <program-name> now.
   - Current state: preserve; not selected.

9. `BUNDLE-I-archive-delete-remove-access-residue`
   - Hypothesis: archived/deleted/removed-access objects may remain visible through sidebars, routes, searches, drafts, comments, or notifications.
   - Future proof need: owned object lifecycle plan; reversible/non-destructive; no permanent delete by default.
   - Current state: preserve.

10. `BUNDLE-J-metadata-only-leak`
   - Hypothesis: subject/snippet/participants/counts/events may leak even when body/content access is denied.
   - Future proof need: owned non-sensitive labels and negative controls.
   - Current state: preserve.

## Passive-only test queue now allowed

Allowed without further operator approval, if done manually and slowly in noVNC or through public docs only:

1. Map settings/sidebar labels for inboxes, teams/workspaces, roles, groups, rules, topics, views, and audit/log surfaces.
2. Screenshot redacted empty states or navigation menus only.
3. Record whether a screen exists and what gates it presents.
4. Stop before any Save/Create/Invite/Connect/Generate token/Activate/Send/Import/Upload/Delete action.
5. If a screen displays real customer/non-owned data, stop immediately and do not capture it.

## Still-blocking issues

These remain unresolved and deliberately block bounded proof:

- Account B / owned teammate not available.
- No second owned tenant/workspace.
- No approved named test inbox/object labels.
- No positive/negative control data.
- No API token creation/storage/call approval.
- No channel/OAuth/mailbox approval.
- No workflow/rule save/activation approval.
- No report-ready evidence and no operator final submission approval.

## Hermes synthesis update

The previous BLOCK is reduced to: `BLOCK_BOUNDED_PROOF_BUT_PASSIVE_MAPPING_ALLOWED`.

The candidate may move from `front_specific_multi_agent_review_completed_blocked` to `passive_mapping_extended_not_proof_ready`, but must not become `bounded_executable` until hard blockers above are explicitly resolved.

## 2026-05-26T13:02Z passive continuation

Mode: passive noVNC screenshot check plus public documentation inventory only. No app object creation, no invite, no role change, no channel/OAuth connection, no token/API call, no workflow activation, no upload/import/delete, no customer/non-owned data, and no report submission.

Evidence added:

- `setting/local/screenshots/program-redacted_live_20260526/current_passive_resume_20260526.png`
- `setting/local/screenshots/program-redacted_live_20260526/after_open_passive_20260526.png`
- `setting/local/screenshots/program-redacted_live_20260526/ws0_passive_20260526.png` through `ws3_passive_20260526.png`

Result: current visible Kali workspaces show desktop/no visible <program-name> browser. This is useful as a resume-state checkpoint, but not a new target finding. A browser/process reset was not performed after the operator denied the destructive process-kill command.

Latest useful <program-name> UI mapping remains the existing dashboard/setup-guide evidence:

- Setup guide categories: `Get started`, `Basic setup`, `Advanced`, `Discover AI`, `Learn More`, `Product demos`, `Courses`, `Help resources`.
- Basic setup checklist: `Create your first shared inbox`, `Connect your first shared channel`, `Automate workflows for your shared inbox with rules`, `Discover your Topics`, `Invite your team`.
- `Discover your Topics` is gated until a shared channel is connected.
- Channel-connect screen exposes `Gmail Account`, `Office 365 User Mailbox`, and references other channel/settings options such as <program-name> Chat, Slack, WhatsApp, Twilio, and more.
- Inbox/sidebar surfaces visible from prior screenshot: `Inbox`, `Open`, `Drafts`, `Later`, `Done`, `More`, `Shared`, demo/shared inbox labels, setup guide progress, trial/plan/help/download controls.
- Stop-before remains: OAuth/login consent, mailbox/channel connection, send/import/upload, invite, rule save/activation, API token creation/call, customer/non-owned data, and any report submission.

Public docs delta from `https://dev.frontapp.com/llms.txt`:

- Channel surfaces: create/list/validate channels; team and teammate channel listing; application/custom channel docs. Treat all channel creation/validation/OAuth as blocked until operator-owned mailbox/channel approval.
- Contact/account surfaces: account CRUD, contact list/group endpoints, contact-to-account links. Preserve as a future `contact/account metadata boundary` bundle; do not create contacts/accounts now.
- Tag surfaces: company/team/teammate/child tag create/read/delete references. Preserve as `tag namespace and lifecycle boundary`; no tag creation/deletion now.
- Conversation/comment/draft surfaces: message send/reply, comments/replies/mentions, drafts, attachment download references. Preserve as owned-object-only future bundles; no sends, comments, drafts, or attachments now.
- Rule/workflow surfaces: rule read endpoints, rule webhooks, application event triggers. Preserve as workflow/rule bundle; no save/enable/trigger/webhook now.

Additional preserved bundles:

11. `BUNDLE-K-contact-account-metadata-boundary`
    - Hypothesis: account/contact metadata, contact-list/group ownership, and team/teammate scoping can diverge from UI visibility.
    - Future proof need: owned dummy contacts/accounts, no real customer data, explicit create/delete cleanup plan.
    - Current state: docs-only preserve.

12. `BUNDLE-L-tag-namespace-lifecycle-boundary`
    - Hypothesis: company/team/teammate/child tag namespaces or deleted/archived tags may expose cross-scope metadata or stale visibility.
    - Future proof need: named owned tags, reversible lifecycle plan, Account B/role checks.
    - Current state: docs-only preserve.

Synthesis: more passive evidence was preserved, but bounded proof is still blocked. The only safe next autonomous step is further passive docs/UI inventory if the browser is visibly available without process reset; otherwise wait for operator direction or a non-destructive VM/browser restore path.

## 2026-05-26T13:10Z reviewer-advisory correction

Operator correction: reviewer output is tactical/adversarial/evidence perspective only, not an extra safety gate. The <program-name> lane must not be blocked merely because a reviewer said BLOCK/REQUEST_CHANGES. Concrete blockers still apply: scope, operator-owned controls, missing Account B/object labels/token/channel/workflow approvals, non-owned data, destructive/strong techniques, and report approval.

Execution rule going forward: continue safe in-scope passive work immediately; for stronger steps, ask only for the concrete missing operator control/approval rather than another reviewer pass.
