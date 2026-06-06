> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Checkpoint-before-live passive resume pattern

Use this when a cybersec/bug-bounty session was interrupted after broad repo cleanup, artifact migration, or many handoff edits, and the user asks to continue into practical/live work.

## Pattern

1. Re-anchor on current project authority layers before touching the target:
   - current navigation / active queue / artifact index;
   - `config/scope.txt` and active `programs/<slug>/scope.json`;
   - active `programs/<slug>/lane_state.json` and queue state.
2. If the working tree contains broad unrelated cleanup/migration changes, checkpoint it before live work:
   - run the project review command;
   - inspect staged content for accidental runtime/local artifacts (`logs/`, VM logs, screenshots, secrets, cookies, tokens, loot);
   - add ignore rules for accidental local logs if needed;
   - commit the cleanup boundary before creating new live-lane artifacts.
3. Resume live work at the least-active allowed mode:
   - for an already-authorized owned-account lane, prefer passive noVNC observation only;
   - do not turn reachability/noVNC restore into proof authorization;
   - if browser/session is visible, record only screen/state/gate observations, not secrets or customer data.
4. Write a named resume artifact under the program notes path, not a chat-only summary:
   - reviewer identity / route/tool;
   - authorization source and stop-before boundary;
   - local readiness actions performed;
   - passive observation summary;
   - selected next passive step and operator gates for stronger work.
5. Update machine/navigation state:
   - lane state next autonomous action;
   - Kali/noVNC readiness state if present;
   - current navigation / active queue / artifact index;
   - accepted changes and project Obsidian bridge when this changes long-term resumability.
6. Validate before final response:
   - lane state validation;
   - redaction check on new artifacts/state;
   - diff check;
   - project review command.

## Important boundaries

- A scope file plus visible logged-in session authorizes only the specific lane actions already allowed by the lane boundary.
- Passive mapping remains passive: no create/connect/save/invite/send/token/API/activate/import/upload/delete actions.
- Local-only screenshots should stay under ignored local paths and be referenced as pointers, not committed evidence.
- If host-only/NAT posture cannot be verified, do not promote to scanner/scripted/stronger target-touching work; continue only within already-approved manual low-speed passive boundaries or stop.

## Example artifact shape

```markdown
# <Program> practical passive resume — <date>

## Reviewer identity
- Reviewer route/tool: Hermes + Kali/noVNC observation
- Visible runtime model: <if exposed or not exposed>
- Review focus: passive live-bounty resume and evidence hygiene

## Status
- Program / lane / state / mode
- Local-only screenshot pointer if any

## Authorization and stop-before boundary
- Scope artifacts checked
- Allowed passive actions
- Blocked actions

## Local readiness actions performed
- noVNC/tunnel/browser state only

## Passive observation
- screen/gate structure, no secrets/customer data transcribed

## Practical lane decision
- next passive mapping step
- exact operator gates for stronger proof
```
