> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# hermes/calls/

Records of Hermes' external agent calls (Claude / Codex).

## File naming

`<YYYY-MM-DDTHH-MM>_<target>_<topic>.md` where target is `claude` or `codex`.

Examples:
- `2026-05-29T08-15_claude_hunt_aikido.md`
- `2026-05-29T09-22_codex_review_lane_state_simplification.md`
- `2026-05-29T14-08_claude_policy_parse_coveo.md`

## Content shape

See `hermes/policies/consult_claude.md` and `hermes/policies/consult_codex.md` for required sections:

- `## Task`
- `## Required context reads`
- `## Inputs`
- `## Expected output shape`
- `## Boundary`
- `## Result` (filled after return)
- `## Verdict` (filled after return)
- `## Notes` (Hermes' assessment)

## Retention

Keep all call records in git. They are the only audit trail of what Hermes asked external agents to do, and what came back. Never truncate. Never delete.

If a call record contains output that includes credentials / PII / tokens, do NOT delete the file. Instead, redact in place and add a `## Redaction` section explaining what was removed and why.
