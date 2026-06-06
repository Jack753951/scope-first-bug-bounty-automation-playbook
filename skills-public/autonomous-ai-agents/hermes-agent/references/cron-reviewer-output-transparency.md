> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cron reviewer output transparency

Use this reference when building or revising scheduled Hermes cron jobs that perform delegated multi-party review.

## Trigger

A cron job uses `delegate_task` or otherwise obtains separate reviewer outputs, especially for project-health, gate, safety, governance, or deep-review reports.

## Lesson

Do not deliver only the parent/Hermes synthesis. The user needs the individual reviewer evidence so they can see disagreements, unsupported claims, and stale-evidence caveats.

## Required final report shape

For each reviewer, include a compact but direct summary before Hermes synthesis:

- Reviewer label/role and status.
- Route/tool and whether the route was read-only or mutating.
- Visible model/runtime if exposed; if hidden, say it is not exposed.
- Verdict: PASS / CONTINUE / REVISE / BLOCKED / CONCERN as applicable.
- PASS evidence bullets.
- CONCERN / gap bullets.
- BLOCKED / unsupported bullets.
- Safe next action.
- Artifact or handoff paths read/written.

Then add `Hermes synthesis`:

- State which reviewer constraints were adopted.
- Preserve dissent explicitly; do not smooth a `REVISE` evidence concern into a broad `CONTINUE` consensus.
- Distinguish fresh verification from provided/stale evidence.
- List prohibited actions that remain prohibited.

## Prompt pattern

Add wording like this to the cron prompt:

```text
Final delivery must include Reviewer 1/2/3 individual results before Hermes synthesis. Do not only provide synthesis. For each reviewer include route/tool, visible model/runtime if available, verdict, PASS/CONCERN/BLOCKED bullets, safe next action, and artifact paths. Preserve unsupported/stale-evidence caveats exactly; do not convert them into consensus.
```

## Pitfalls

- `delegate_task` summaries are self-reports; if the task has side effects, verify handles yourself before claiming success.
- If reviewers used only an evidence packet, label the result as packet-based, not freshly verified.
- If one reviewer says a claim is unsupported, final synthesis should either remove that claim or mark it as unsupported/gap.
