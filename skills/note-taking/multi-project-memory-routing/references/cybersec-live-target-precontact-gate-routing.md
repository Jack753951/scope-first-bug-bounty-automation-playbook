> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersec live-target pre-contact gate routing

Use this pattern when a cybersecurity workspace has prepared a next live/bug-bounty/CTF target, but the next step crosses from offline/readiness work into target contact or account signup.

## Trigger

- The repo has scope/authorization evidence for selected hosts, but the agent has not yet touched the live target in the current pass.
- The next action involves official signup/login, phone/OTP/email verification, CAPTCHA, payment/KYC, workspace creation, browser profile state, cookies, API tokens, integrations, callbacks, or report submission.
- The user asks for status such as "remember what we were doing?", "are we ready?", or "continue" near a live-target boundary.

## Routing rule

Do not store target-specific scope, hostnames, program names, verification results, cookies, tokens, phone numbers, OTPs, or artifacts in global Hermes memory or in this skill. Keep them in repo-local handoff / artifact index / active strategy queue / Obsidian project notes according to the project's security policy.

The reusable skill-level lesson is the gate shape:

1. Separate `scope_authorized_for_selected_hosts` from `autonomous_target_touching_allowed`.
2. If scope is authorized but signup/auth/operator-owned gates remain, write a named repo-local checkpoint that explicitly says target contact has not happened in this pass.
3. Mark the next step as an operator gate, not an agent action, whenever it requires secrets, OTPs, CAPTCHA, phone numbers, payment/KYC, or policy acceptance.
4. Give the user a small finite set of non-sensitive status replies, e.g. `signup_complete`, `blocked_phone`, `blocked_email_verification`, `blocked_captcha`, `blocked_payment`, `blocked_policy`, `stop`.
5. After the user reports success, resume only the authorized low-risk surface/account mapping lane and stop before invite/customer data, API token creation/retention, integrations/callbacks/OAST/tunnels, billing/payment/KYC, support/customer messages, or report submission unless explicitly approved and in-scope.

## Operator-gate preparation pattern

If the user explicitly authorizes opening the target/signup flow but a gate requires operator-owned data, use a narrow "prepare but do not submit" pattern:

1. Use the project-approved environment/browser lane (for this workspace, normally VM/noVNC rather than a separate browser session) and keep target contact within the already authorized signup/account-mapping surface.
2. Fill only non-sensitive, non-secret fields that are necessary to reach the operator gate and are consistent with the program rules.
3. Stop before submitting or advancing any gate that needs phone numbers, OTPs, CAPTCHA, email verification, password decisions, policy acceptance, payment/KYC, or report/customer/support messages unless the user is locally present and explicitly directs the next action.
4. Leave the UI in a safe handoff state when practical: cursor in the operator-only field, no automatic submit, and no stored OTP/phone/password in repo artifacts or chat.
5. Record a repo-local checkpoint with: browser/VM pointer, screenshot path if non-sensitive, fields completed at a coarse level, exact blocked gate category, and a small set of non-sensitive status tokens for the user to reply with.
6. Validate only the local artifacts you changed (for example JSON formatting and whitespace/diff checks); do not run unrelated scans or probes just to close the checkpoint.

## Repo-local artifacts to prefer

- `handoff/<program>_pre_contact_ready_checkpoint_<date>.md`
- `handoff/<program>_pre_contact_verification_summary_<date>.md`
- `handoff/third_target_contact_checkpoint_<date>.json` or equivalent machine-readable gate state
- `programs/<program>/lane_state.json` or equivalent program-local lane state
- `setting/local/screenshots/<program>_live_<date>/...` for non-sensitive VM/noVNC screenshots that support handoff
- `handoff/current_artifact_index.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- append-only `handoff/accepted_changes.md`

## Verification before saying ready

- Scope file / program rules checked for the selected hosts.
- Local browser/noVNC or VM access verified if the workflow depends on it.
- Dirty tree classified so readiness artifacts are not confused with historical noise.
- Focused validation / project review passes for changed scripts or handoff contracts.
- Secret scan or manual redaction check confirms no secrets/OTP/cookies/tokens were written.

## Chat response style

When reporting the checkpoint, be concise and gate-explicit:

- State `READY_FOR_OPERATOR_GATE` or equivalent.
- State what is authorized and what is still blocked.
- State that the agent did not perform live target contact in this pass if true.
- Provide the exact operator URL/path only if it is already in project-local scope and non-sensitive.
- Ask for only non-sensitive status tokens, never credentials or verification material.
