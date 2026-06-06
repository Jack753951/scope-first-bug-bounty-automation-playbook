> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent fast local batch review pattern

Session date: 2026-05-22
Project: `<user-home>`

## Durable lesson

For `youtube_agent`, fast local learning batches should stay lightweight, but once a batch is produced, Hermes should still capture enough evidence to rank artifacts and avoid accidentally promoting renderer sanity samples as canary candidates.

Use this when the user asks for faster local learning, local-only draft batches, or post-batch triage for `redditstories` / `redditscary`.

## Pattern

1. Run the local-only draft batch with the requested channel scope.
2. If an automatic Reddit-source run fails a first-sentence / hook gate, treat the gate as useful signal, but do not equate that with render failure. Recovery options:
   - for learning-only renderer/script samples, generate bounded manual-topic drafts with the channel topic engine;
   - do not promote manual-topic recovery drafts as source-grounded Reddit canary candidates;
   - record the pipeline gap if the desired behavior is candidate skip-and-continue instead of aborting the requested count.
3. Extract compact evidence for each artifact:
   - final MP4 path,
   - metadata path,
   - title / hook card / narration summary,
   - duration,
   - script engine,
   - asset/render/QA profile labels,
   - source URL if present,
   - opening and contact sheets.
4. Run project validation after the batch: `run_agent.ps1 validate`; confirm `.agent.lock` clear and `DEFAULT_PRIVACY='private'`.
5. Write one compact review packet under `handoff/visual_qa/<batch_name>/review_packet.md`.
6. Prefer Claude Code read-only creative review for the batch, but avoid broad tool-use wandering when the packet already contains sufficient evidence.

## Claude Code review fallback

A broad `--allowedTools Read --max-turns 3` review may hit `error_max_turns` even when it records useful metadata. If the packet already contains the contact-sheet/Hermes visual notes, immediately fall back to a one-turn no-tools text review rather than rerunning the same broad prompt:

```bash
cat handoff/visual_qa/<batch>/review_packet.md | claude -p 'Read-only creative/visual QA of ONLY the provided packet text. Do not use tools. Do not inspect files. Do not approve upload/private canary/public cadence. Return concise sections: Reviewer route/tool; Visible model/runtime model if exposed; Verdict per artifact (STRONG_INTERNAL_SAMPLE / USABLE_INTERNAL_SAMPLE / WEAK_SAMPLE / BLOCK); Batch-level verdict; Must-fix before private canary; Non-blocking notes; Blocked actions confirmed.' --tools '' --max-turns 1 --output-format json > handoff/visual_qa/<batch>/claude_review_textonly_raw.json
```

Then extract `result`, `session_id`, `modelUsage`, and `total_cost_usd` into a human-readable `claude_review.md`. Record that the broad Read-tools attempt hit `error_max_turns` if applicable.

## Verdict discipline

Use labels that separate internal learning from canary readiness:

- `STRONG_INTERNAL_SAMPLE`: strong local/internal artifact; may be worth exact-artifact canary gate if source-grounded and no hard blocker remains.
- `USABLE_INTERNAL_SAMPLE`: useful for learning/renderer validation, but not enough alone for canary.
- `WEAK_SAMPLE`: keep as negative/learning example only.
- `BLOCK`: do not use; hard visual/audio/provenance/safety issue.

Manual-topic recovery drafts are usually renderer/script samples only, not canary candidates, unless a separate source/provenance gate makes them eligible.

## Common youtube_agent batch blockers to record

- Automatic source pipeline aborts the requested count instead of skipping failed candidates.
- ElevenLabs 402 / paid-plan-required fallback to Edge TTS: not a render blocker, but may make a draft non-canary unless explicitly accepted.
- Missing channel frame/template asset causing fallback visuals.
- Dark horror footage that fits mood but needs mobile luminance/contrast check.
- Generic paperwork/laptop visuals that pass render QA but do not strongly match story-specific proof objects.

## Safety boundary

Fast local batch review does not authorize upload, private canary, public cadence, scheduler edits, OAuth/token/client-secret edits, channel JSON changes, `DEFAULT_PRIVACY` changes, runtime deletion, or DB mutation. Only the selected exact artifact can enter the heavier upload/private/scheduled/public gate after explicit user approval.