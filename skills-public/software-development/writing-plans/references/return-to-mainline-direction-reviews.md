> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Return-to-Mainline Direction Review Prompts

Use this reference when a project has spent several slices improving an offline UX, fixture, review, or artifact line and the next useful step may be to pause that line and return to the main platform/runtime-policy roadmap.

This is especially useful in safety-gated repositories where adding "just one more" artifact can accidentally trigger schema promotion, new consumers, runtime wiring, or reviewer-note capture before the policy/runtime boundary has been reviewed.

## When to use

Use this pattern when:

- A phase line has produced several coherent offline/local slices and has a natural pause point.
- The next tempting slice would add another artifact, schema, consumer, renderer, report surface, or UX layer.
- A separate mainline exists, such as program-policy gates, dry-run runner integration, or runtime safety validation.
- The next implementation could be T3/T4/T5 depending on whether it touches runtime, scope, policy, module runner, reports, or target-touching behavior.
- The right answer might be "close/pause this line and return to mainline" rather than "implement more here".

## Prompt structure

A good return-to-mainline prompt should include:

1. **Context** — summarize the completed offline/review line and the mainline it might return to.
2. **Current decision point** — state why continuing the current line may be lower value or riskier than returning to mainline.
3. **Small explicit option enum** — force a decision among concrete paths, for example:
   - `CLOSE_CURRENT_LINE_AND_RETURN_TO_MAINLINE`
   - `ADD_OFFLINE_FIXTURE_ONLY`
   - `PLAN_DRY_RUN_STAGE_EXERCISE`
   - `PLAN_DRY_RUN_RUNNER_BRIDGE`
   - `CONTINUE_OFFLINE_REVIEW_LINE`
   - `BLOCK_OR_DEFER`
4. **Review dimensions** — require review tier, milestone boundary, preferred option, safety boundary, OSS/prior-art notes, existing-mainline status check, phase-boundary check, and exact implementation boundary.
5. **Trigger checks** — ask whether the option fires any known refactor/promote/review triggers, such as fifth consumer, third file-reading consumer, schema promotion, helper extraction, scanner-output ingest, report surface, or target-touching boundary.
6. **Hard safety constraints** — explicitly forbid implementation in the review prompt and list runtime/scope/credential/report/platform boundaries that remain locked.
7. **Output contract** — require the reviewer to write a named handoff file plus a final decision block compatible with the repo's review policy.

## Handoff discipline

For repositories that use rolling handoff files:

- Keep a stable named artifact for audit-important prompts, e.g. `handoff/cowork_p3_7_direction_prompt.md`.
- Refresh the rolling pointer, e.g. `handoff/cowork_task.md`, with the same content only after archiving or relying on the repo's handoff archive mechanism.
- Record an append-only accepted-changes entry that names the prompt, the decision options, and the safety boundary.
- When posting PR updates from Git-Bash/MSYS, write Markdown/backtick-heavy comments to a file and use `gh pr comment --body-file` to avoid shell command substitution.

## Safety language to include

Use wording like:

```text
The review is design-only. Do not implement code. Do not run scanners. Do not touch targets. Do not invoke recon stages against real hosts. Do not modify runtime scripts, schemas, configs, scope files, modules, runners, reports, credentials, scheduler, deployment, billing, repo settings, or production settings.
```

Then enumerate forbidden boundary crossings:

- active scan, exploit, fuzz, brute force, callback, OAST, proxy, pivot, tunnel, beacon, relay, reverse listener, or target-touching behavior;
- weakening or bypassing existing scope/policy gates;
- accepting stale/forged/cached allow decisions;
- module/scanner execution or scanner-output ingest;
- report drafting/submission or platform adapters/importers/exporters;
- lifecycle promotion to confirmed/verified/valid/reportable/accepted/resolved;
- new live-target CLI affordances in offline consumers;
- scheduler, CI auto-execution against targets, deployment, billing, OAuth, credentials, secrets, or repo-setting changes.

## Verification after writing the prompt

Run only local/static checks appropriate to the repo:

- diff whitespace check;
- repo local review/static gate;
- prompt structure check for required headings and output file path;
- added-line safety scan for command-shaped scanner invocations or secret material;
- confirm named artifact and rolling pointer match if both are written.

Do not run target-touching validations as part of writing the direction-review prompt.
