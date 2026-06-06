> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cross-Project Process Adoption Matrix

Use this reference when the user asks to borrow workflow/review/process improvements from one project for another, or when a periodic/meta review finds a useful pattern that may transfer across projects.

## Principle

Transfer the reusable process, not the source project's domain-specific state or risk language.

Example: a cybersecurity project's review tiers can inspire media-project tiers, but `safe_target`, scanner, exploit, proxy/pivot, and vulnerability-evidence rules should not be copied into a YouTube automation repo. Translate the boundary into that repo's real risks: upload, publication, scheduler, OAuth/token, destination channel, privacy defaults, generated media, asset provenance, render/subtitle QA, and canary gates.

## Workflow

1. Inspect the source project's local context and relevant policy/review docs.
2. Inspect the target project's local policy/handoff/active queue.
3. Extract only class-level process patterns: review tiers, decision blocks, freshness metadata, milestone batching, reviewer role separation, escalation rules.
4. Reject source-domain specifics unless the target project has the same risk class.
5. Write a short project-local adoption note in the target repo handoff.
6. Update the target active queue / accepted changes only with the adopted process and next safe action.
7. If the pattern applies across multiple projects, update this skill or another class-level skill; do not store the target project's detailed state in the skill.
8. Verify with docs/static checks appropriate to the target repo. Do not run unrelated runtime or external-side-effect commands just to record a process adoption.

## Adoption Matrix Template

```text
Source project:
Process improvement:
Reusable principle:
Target projects:
Adopt / adapt / reject:
Project-specific translation:
Safety caveats:
Files to update:
Verification:
```

## Review Decision Block Template

For non-trivial cross-project process adoptions, end the target repo note with:

```text
Decision: PASS / PASS_WITH_CONDITIONS / REQUEST_CHANGES / DEFER / ESCALATE_TO_USER
Target-project tier:
Workstream / milestone:
Hermes authority: direct / conditional / escalation-only
Reviewers consulted:
- route/tool; visible runtime model or limitation
Validation performed:
Blocking findings:
Non-blocking recommendations:
Safety boundary:
User approval required: yes/no; reason:
Next safe action:
```

## Pitfalls

- Do not create a new narrow skill named after the source project or today's adoption note; patch the relevant umbrella skill.
- Do not convert a successful project-specific rule into a global command.
- Do not copy sensitive/domain-specific artifacts across projects.
- Do not overfit the target project with heavy review ceremony; scale the adopted process to the target's risk tier.
- Do not let periodic review packets become stale authority; include frozen date, latest handoff inspected, and conflict-resolution authority.
