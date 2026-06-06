> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Generated-Media Remediation Rungs

Use this reference when a generated video/audio/creative artifact technically renders but fails visual QA, proof-object clarity, subtitle legibility, or brand-safety review.

## Trigger

A controlled/local artifact exists and has a review verdict like `REVISION_REQUIRED`, `DO_NOT_UPLOAD`, or `PRIVATE_LOCAL_LEARNING_ONLY`. The next safe step is not another blind render; it is a remediation plan that converts review blockers into a small TDD implementation rung.

## Required shape

1. Start with scope labels: `PLAN_ONLY`, `NO_RERENDER`, `NO_UPLOAD`, `CODE_NOT_EXECUTED` unless the user explicitly authorized code/runtime work.
2. Cite exact failing artifacts: local media path, metadata/subtitles, contact sheet, ffprobe, review notes.
3. Convert each blocker into an acceptance criterion.
4. Inspect enough code to name exact future files/functions/tests.
5. Split gates:
   - plan/review gate,
   - code implementation gate,
   - rerender gate,
   - upload/canary gate,
   - schedule/publish gate.
6. Use TDD for future code: failing tests first, then minimal implementation, then validation.
7. Run a read-only creative/engineering review (Claude Code or other configured reviewer) on the plan before implementation when the failure is visual/creative and code-adjacent.
8. Record reviewer route/tool and visible runtime model when available.

## Generated video proof-object pattern

For proof-heavy Shorts, do not rely on stock footage to carry the evidence. Plan deterministic synthetic readable cards or overlays with:

- literal synthetic text strings,
- no names, emails, companies, cities, logos, screenshots, or PII-shaped substitutes,
- placement that does not cover subtitles,
- timing windows tied to narration beats,
- contact-sheet-visible text size,
- regression tests that remove placeholders such as `real story detail`.

If stock footage is repetitive, first decide whether readable overlays solve the blocker. Keep stock deduplication as a separate rung unless it is the primary failure.

## Safety reminder

A remediation plan is not permission to rerender or upload. Future implementation and future rerender each need their own explicit approval when the project has privacy, OAuth, scheduler, or publication risks.