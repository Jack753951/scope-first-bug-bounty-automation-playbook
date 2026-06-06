> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Command And Technique Library

This directory stores reusable commands by objective. Avoid random dumps; every entry should teach when and why to use the command.

## Entry Template

```text
Goal:
Context:
Authorization:
Command:
Expected output:
Interpretation:
Safety notes:
When not to use:
Related defense:
```

## Suggested Sections

- `recon.md`
- `web.md`
- `network.md`
- `linux.md`
- `windows-ad.md`
- `cloud.md`
- `defense.md`
- `reporting.md`

## Quality Bar

- Commands must be tied to an authorized use case.
- Include what good, bad, and inconclusive output looks like.
- Include a defensive counterpart when possible.
- Prefer lab-safe examples such as `127.0.0.1`, `target.lab`, or intentionally vulnerable platforms.
