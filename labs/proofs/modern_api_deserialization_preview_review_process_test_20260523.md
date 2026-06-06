> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API deserialization preview/review process test — Hermes synthesis

Status: process-test passed / vulnerability rerun blocked-deferred
Date: 2026-05-23
Route/tool: Hermes preview -> attempted SSH/Kali bounded execution -> Claude Code read-only review -> Hermes synthesis
Visible reviewer runtime: Claude Code JSON result reports `claude-opus-4-7 / Claude Code CLI`
Usage artifact: `handoff/claude_review_deser_preview_test_20260523.json`

## What was tested

The newly fixed preview/review workflow was tested once on the current top lane:

```text
OSS/source reconnaissance
-> Hermes tactical preview
-> Kali bounded-script execution attempt
-> blocker/evidence pullback
-> Claude Code read-only review
-> Hermes synthesis
```

This was a tactical/project-value lens test, not a new safety gate or approval process.

## Inputs and artifacts

- OSS/source recon note: `setting/local/oss_refs/deserialization_preview_test_20260523/README.md`
- Hermes tactical preview: `handoff/modern_api_deserialization_preview_20260523.md`
- Blocked execution record: `handoff/modern_api_deserialization_preview_test_blocked_20260523.md`
- Claude review packet: `handoff/claude_review_packet_deser_preview_test_20260523.md`
- Claude review raw JSON: `handoff/claude_review_deser_preview_test_20260523.json`
- Claude review markdown: `handoff/claude_review_deser_preview_test_20260523.md`

## Execution result

The intended dedicated deserialization runtime proof was blocked by the execution layer:

```text
BLOCKED: User denied. Do NOT retry.
```

Hermes did not retry, encode, disguise, split, or move the same pickle-trigger execution into another command.

## Claude Code review summary

Claude Code reviewed the compact packet with no tools and returned:

- `Claim supported? partial`
- `Recommended status: blocked/deferred`
- The workflow/process test is supported because recon, preview, execution attempt, blocker capture, review, and synthesis happened in order.
- The dedicated deserialization vulnerability rerun is not runtime-verified because no new pre/post health, invalid control, positive marker, or `/deser-log` artifacts were produced.
- Do not borrow the prior historical broad `modern_api_wave2` deserialization bundle to upgrade this dedicated wave.

## Hermes final decision

- Process test status: `passed`.
- Vulnerability rerun status: `blocked/deferred`.
- No new `verified-impact` deserialization claim is made for this run.
- The previous historical deserialization bundle remains historical context only.
- The new preview/review routing worked as intended: it added tactical perspective and project-value classification without becoming a new safety process.

## Accepted suggestions

- Keep preview owned by Hermes.
- Keep review owned by Claude Code via compact read-only packet.
- Separate the process-test claim from the vulnerability-proof claim.
- If rerun later, use a wave-unique marker and capture health/control/positive/log/post-health.

## Rejected suggestions / not done

- No retry or bypass of the blocked trigger.
- No callback, shell, file-write impact, persistence, credential access, public target, or external listener.
- No schema/importer/report-generator work.
- No claim that the dedicated rerun is verified.

## 對專案有什麼幫助

- Proves the new preview/review flow can operate without becoming governance-first.
- Validates that Claude Code review can be used as a compact tactical/project-value reviewer after artifacts, while Hermes keeps synthesis.
- Prevents overclaiming: the project correctly separates `process-test passed` from `vulnerability rerun blocked/deferred`.
- Keeps the current top lane clear: dedicated deserialization rerun is still valuable, but needs either operator-run execution or a non-triggering source-level/adjacent lane before runtime verification.

## 新增/更新了什麼

New artifacts:

- `setting/local/oss_refs/deserialization_preview_test_20260523/README.md`
- `handoff/modern_api_deserialization_preview_20260523.md`
- `handoff/modern_api_deserialization_preview_test_blocked_20260523.md`
- `handoff/claude_review_packet_deser_preview_test_20260523.md`
- `handoff/claude_review_deser_preview_test_20260523.json`
- `handoff/claude_review_deser_preview_test_20260523.md`
- `handoff/modern_api_deserialization_preview_review_process_test_20260523.md`

Updated records:

- `handoff/accepted_changes.md`
- `handoff/active_strategy_queue.md`
- `notes/obsidian_projects/Cybersec Lab.md`

No scripts, bundles, target source, VM settings, scheduler, or public-target configuration were changed.
