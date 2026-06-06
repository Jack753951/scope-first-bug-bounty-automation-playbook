> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Content Artifact Review Gates

Use this reference when subagent-driven work produces visible media/content artifacts (draft videos, thumbnails, HTML previews, MP4 fixtures, scripts, prompt packs, canary candidates) in a repo where strategy/creative quality matters.

## Why

Engineering validation can pass while the artifact is still strategically weak. For example, a draft may render correctly but have a weak hook, low-stakes story, poor first-3-second retention, or no comment-driving dilemma. Do not let code/test PASS become content/canary PASS.

## Gate Shape

Add a lightweight domain-review gate after local artifact validation and before canary/public recommendations:

1. Generate or locate the upload-free artifact.
2. Run local technical validation first (render QA, duration, subtitle checks, schema checks, screenshots/contact sheet as applicable).
3. Send a concise review packet to the domain reviewer (e.g. Claude/Cowork for Shorts/content strategy).
4. Ask for a structured verdict: `CANARY`, `REVISE`, or `REJECT`.
5. Route follow-up by issue type:
   - Strategy/prompt/script issue -> domain reviewer / strategy worker.
   - Implementation/template/render issue -> engineering worker / Codex.
   - Safety/publication issue -> orchestrator/user approval gate.
6. Record only material decisions and reusable learnings in handoff docs.

## Suggested Review Dimensions for Shorts/Media

- Hook strength
- First-3-second retention
- Conflict clarity or value proposition
- Emotional stakes / payoff
- Pacing and escalation
- Comment bait / audience response potential
- Source/story/topic fit
- Visual/subtitle support
- Channel/brand fit
- Safety/rollout concerns

## Verdict Semantics

- `CANARY`: strategically worth a small public test, but not authorization to publish. Still requires orchestrator safety validation and explicit user approval where publishing is sensitive.
- `REVISE`: promising but needs targeted changes before another canary decision.
- `REJECT`: do not spend upload/public attention on this artifact; preserve any reusable lesson for sourcing/scoring/prompting.

## Pitfalls

- Do not balance AI-worker usage by sending low-level engineering changes to a strategy reviewer. Add more frequent strategy checkpoints instead.
- Do not run a full project review for every tiny artifact. Keep artifact reviews lightweight and structured.
- Do not include secrets, OAuth tokens, raw credential files, private API keys, runtime database dumps, or unnecessary user-owned data in review packets.
- Do not treat a domain-review `CANARY` as permission to upload/publish or bypass render/privacy gates.
