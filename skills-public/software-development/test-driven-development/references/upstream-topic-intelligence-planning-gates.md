> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Upstream topic-intelligence planning gates

Use this when an upstream topic radar feeds a downstream media generator/publisher and the next step is a human/planning gate rather than runtime generation.

## Pattern

Build gates as small, explicit decision records, not implicit approvals:

1. Candidate/topic packet: public/accountless source metadata only.
2. Main-project handoff: recommends at most one next-gate candidate and blocks runtime actions.
3. Concept/design gate: planning-only review packet for the selected candidate.
4. Human decision record: approve for separate review, request more objects, or reject.
5. Synthetic object specs: define proof-object requirements only; no asset rendering.
6. Specs review decision: approve only a separate downstream concept-review gate, request revision, or reject.
7. Separate downstream concept-review gate: still planning-only unless a later reviewed workflow explicitly authorizes production.
7. Separate downstream concept-review gate: still planning-only unless a later reviewed workflow explicitly authorizes production.
8. Concept-review decision record: approval authorizes only the next named planning packet (for example `user_gated_local_only_concept_packet = YES_SEPARATE_GATE_ONLY`) while script/render/upload/scheduler/OAuth/token/channel-config/competitor-asset actions stay blocked.
9. User-gated local-only concept packet: a planning artifact only, not a script. It can contain originalized premise, hook directions, proof-object requirements, visual beat plan, SFX/pacing direction, missing inputs, no-go checklist, and a `human_approval_required_before_next_gate` flag. Its next action should remain human review of the local concept packet, not automatic script planning.
10. Local concept packet review decision: if used, it should be a separate human decision record before any script-planning gate opens.

## TDD requirements

For each new gate, add RED tests before implementation that prove:

- The source status must match the immediately previous planning-only packet; wrong status fails closed.
- Valid decisions are enumerated; unknown decisions fail closed.
- Approval only authorizes the next named review gate, not script/render/upload/scheduler/OAuth/token/channel-config/competitor-asset actions.
- Request-revision remains local to the current planning layer.
- Reject blocks all downstream actions.
- CLI writes JSON and Markdown artifacts only.
- Generated Markdown repeats the authorization boundary in human-readable form.
- Reviewer metadata fields should label reviewer route/tool and visible model/runtime model when known; if exact runtime model is not exposed, state that limitation rather than inventing it.
- Generated Markdown repeats the authorization boundary in human-readable form.
- User-gated local-only concept packets are explicitly concept directions, not executable scripts: assert there are no `script`, `final_script`, or `voiceover_lines` fields; runtime authorizations remain `NO`; and Markdown says it is NOT a script, NOT a render, NOT an upload approval, and NOT a downstream runtime command.
- Hook/premise transformation is non-verbatim: assert source hook strings are not emitted as hook directions, and add regression checks for risky partial phrase echoes found during review (for example a reused clause such as `not the shadow`). Prefer direction language over final-copy language.
- Concept packets carry synthetic-only proof-object requirements and no-go checklists: synthetic cards only, no real footage/faces/addresses/license plates, no competitor frames/thumbnails/social assets, and human approval required before the next gate.

## Example decisions

For synthetic proof-object specs review:

- `approve_specs_for_separate_concept_review` -> `open_separate_youtube_agent_concept_review_gate`
- `request_spec_revision` -> `revise_synthetic_object_specs_only`
- `reject_specs` -> `return_to_topic_discovery_or_reject_candidate`

For downstream concept-review decisions:

- `approve_for_user_gated_local_only_concept_packet` -> `approve_for_user_gated_local_only_concept_packet`, with only the local concept packet gate set to `YES_SEPARATE_GATE_ONLY`; all runtime/publication authorizations stay `NO`.
- `request_concept_review_revision` -> `revise_youtube_agent_concept_review_gate_only`
- `reject_concept_for_now` -> `return_to_topic_discovery_or_reject_candidate`

For user-gated local-only concept packets:

- `next_allowed_action` should be `human_review_local_concept_packet_only`.
- The packet should include concept directions and review requirements, but must not become a draft script or render order.

Approval should use an authorization value like `YES_SEPARATE_GATE_ONLY` for the specific next review gate and keep every runtime/publication action as `NO`.

## Pitfalls

- Do not treat approval of a planning packet as approval to render, draft, upload, schedule, or touch OAuth/channel config.
- Do not skip the intermediate review artifact just because the candidate looks good; the value is the auditable chain.
- Do not bury safety boundaries only in JSON. Put them in Markdown too so a human reviewer sees them.
- Do not broaden source permissions while adding planning gates. Public/accountless metadata and synthetic specs stay separate from asset generation.
- Do not let a local-only concept packet become stealth script generation. Use `hook_directions`, `visual_beat_plan`, and `sfx_pacing_direction` as planning/review directions only; require a later human decision before any script-planning gate.
- Do not rely only on whole-string non-verbatim checks. Independent review can catch risky partial phrase echoes; convert them into focused RED regressions and regenerate the artifact.
- Do not auto-refresh downstream/main-project state inside a packet builder. Carry a snapshot freshness note and require explicit revalidation before any later runtime-adjacent gate.
