> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Review Route and Model Labeling

Use this reference for any project review, independent review, code review, creative review, safety gate, or third-party review when the user wants transparency about who/what reviewed the work.

## Required review identity block

Include a compact block near the top of the review:

```md
## Reviewer identity

- Reviewer route/tool: <Hermes subagent | Claude Code CLI | Codex CLI | local Hermes tools | other>
- Visible runtime model: `<model if exposed>` OR `not exposed by tool`
- Provider/runtime: `<provider if exposed>` OR `not exposed by tool`
- Tool/version visible: `<CLI version if relevant/available>`
- Limitation: <what cannot be verified about the underlying model>
- Review focus: <engineering | creative | safety | subtitle/audio QA | visual QA | publication gate>
```

## Important distinction

Do not imply that “third-party review” automatically means a different underlying model. Be explicit:

- Hermes subagent reviews usually run in a fresh context and may report a visible runtime model.
- Claude Code / Codex CLI may expose a CLI version but not the exact underlying model.
- A route was chosen for the task focus; the actual model is only known when the tool reports it.

## When to use

Use this in:

- code reviews,
- creative or strategy reviews,
- generated-media QA,
- subtitle/audio alignment review,
- upload/publication/scheduler/OAuth safety gates,
- cross-agent handoff summaries.

## Handoff wording

When exact model is not exposed, write that plainly instead of guessing:

- `Visible runtime model: not exposed by tool`
- `Limitation: CLI/provider did not reveal the exact underlying model; only route and visible version are known.`

## Safety-sensitive reviews

For public/upload/scheduler/OAuth/default-privacy decisions, the review identity block does not replace explicit user approval. Keep reviewer/model transparency separate from action authorization.
