> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent visionreview routing via Claude Code

Session date: 2026-05-19
Project: `<user-home>`

## Durable lesson

For youtube_agent, treat `visionreview` / visual QA as creative review, not just mechanical engineering QA. When Claude Code is authenticated via Claude Pro/OAuth, non-trivial visual review packets should default to Claude Code first, with Hermes remaining the safety gate and final verifier.

## Applies to

Use this routing for review of:

- rendered Shorts and upload-free MP4 fixtures,
- contact sheets and representative extracted frames,
- screenshots/thumbnails/layout readability,
- first-frame hook strength,
- subtitle/proof-card readability,
- source-to-visual alignment for `redditstories`,
- pre-generation source-fit candidate packets when visual/proof-card fit or creative direction is part of the decision,
- channel-fit creative review for Storytime/Psychology/Reddit visual fixtures.

## Recommended flow

1. Hermes locates or extracts evidence: artifact paths, frames/contact sheet, metadata, channel context, style rubric, blocked actions.
2. Write a compact `handoff/visionreview_*` packet.
3. Run Claude Code print mode first when authenticated:

```bash
claude -p "$(cat handoff/<visionreview_packet>.md)" \
  --allowedTools 'Read' \
  --max-turns 3 \
  --output-format json
```

4. If the CLI cannot inspect pixels directly in the current context, Hermes should supply frame summaries/contact-sheet notes and record the limitation.
5. Hermes reruns/validates any local checks, verifies safety boundaries, and writes the final handoff/GitHub synthesis.
6. Codex/GPT is fallback or focused risk/engineering review, not the default creative visual reviewer.

## Source-fit packet review pattern

For pre-generation candidate selection, the same creative-review policy applies even when there is not yet a rendered video. Treat the packet as a creative artifact when it contains hooks, proof-object ideas, visual beats, brand-risk filters, or channel-fit scoring.

Recommended prompt:

```bash
claude -p "Read-only creative review of handoff/<candidate_packet>.md. Do not modify files. Treat this as source-fit review only, no generation/upload approval. Return concise: Reviewer route/tool; visible model if exposed; Verdict; preferred candidate; blockers; notes; blocked actions confirmed." \
  --allowedTools 'Read' \
  --max-turns 3 \
  --output-format json
```

Record:

- Claude Code session id,
- visible model/runtime model from JSON `modelUsage` if exposed,
- preferred candidate,
- conditions/cautions,
- blocked actions confirmed.

Write a separate review artifact rather than mixing raw Claude output into the source-fit packet, then update the queue/accepted-changes with Hermes synthesis. A `PASS_TO_SCRIPT_PROMPT` or `PASS_WITH_CONDITIONS` is still planning-only.

## Script-prompt planning packet review pattern

When a source-fit candidate has been selected but generation is still user-gated, treat the script-prompt planning packet as a creative artifact too. Claude Code should review the future prompt contract before any `draft`/`create` command is authorized.

Recommended prompt:

```bash
claude -p "Read-only creative prompt review of handoff/<script_prompt_packet>.md. Do not modify files. No generation/upload approval. Review whether this script-prompt packet is ready as a future user-gated controlled generation prompt. Return concise: Reviewer route/tool; visible model if exposed; Verdict; blockers; prompt risks; recommended tweaks; blocked actions confirmed." \
  --allowedTools 'Read' \
  --max-turns 3 \
  --output-format json
```

For `redditstories` proof-object prompts, specifically ask or verify that Claude Code checks:

- the first spoken sentence is not loose enough for the generator to drift away from the selected contradiction,
- duration rules are binding while beat timings are only illustrative,
- title/hook card do not spoil the final reversal,
- proof-object visuals are specific rather than generic mood shots,
- fake numerics, legal windfalls, public doxxing, or revenge escalation are explicitly blocked,
- the causal reversal preserves the selected proof object (for example, manager's own approval emails trigger the overtime correction),
- any media-profile schema/version string is verified against repo code before generation.

After the review, write a separate `handoff/*_claude_review_*.md` artifact, apply only safe planning-text tweaks, update the queue/accepted-changes, and keep generation explicitly user-gated. A `PASS_WITH_CONDITIONS` means "prompt contract ready after tweaks," not permission to generate.

## Required review output shape

Ask Claude Code to return:

```text
Reviewer route/tool: Claude Code CLI
Visible model/runtime model: state if exposed, otherwise "not exposed by CLI output"
Verdict: PASS / PASS_WITH_CONDITIONS / REVISE / BLOCK
Creative fit:
Visual readability:
First-frame/hook strength:
Proof-object clarity:
Pacing / scene variety:
Brand/safety risks:
Must-fix before generation/upload:
Non-blocking notes:
Blocked actions confirmed:
```

## Local draft cron nuance

Fast local-only draft jobs may stay lightweight and do not need to run Claude Code visionreview for every single draft. However, reports for those jobs should explicitly mark `Claude Code visionreview: pending/required before private canary`, and agents must not treat `render QA PASS` or `review-output PASS` as private-canary readiness. Before any batch visual-readiness decision, exact-artifact private canary, or public-cadence decision, route the artifact/contact-sheet packet through Claude Code visionreview first.

## Safety boundary

A Claude Code visionreview verdict is not upload, canary, or publication approval. Do not treat creative review as authorization for:

- `create`, `draft`, `loop`, `remake`, render, or upload commands,
- public/private canary or scheduled publication,
- OAuth/token/client-secret/channel-destination edits,
- `DEFAULT_PRIVACY` changes,
- channel activation or scheduler changes,
- DB/runtime media mutation.

Record in handoff whether Claude Code was used or explicitly skipped and why.