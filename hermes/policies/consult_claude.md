> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Consult Claude

Load this file before invoking `claude` CLI.

## Call Claude for

- Hunt sessions (owned-account A/B IDOR/BOLA/role-mismatch exploration).
- Complex policy parsing (multi-page, mixed prose+JSON, custom severity).
- Report drafting (first pass: evidence → CVSS-justified markdown).
- OSS source review of a target's tech stack.
- Multi-file design-first refactors.

## Do NOT call Claude for

- Routine browser tasks (Hermes has Playwright).
- Single-file scope.json edits, daily digest, lane state passive updates, intake scoring, CVE digest. Hermes does these.
- Anything a deterministic script can do.

## Call format

Write `hermes/calls/<YYYY-MM-DDTHH-MM>_claude_<topic>.md` BEFORE invoking, with sections:

```
## Task           — one sentence
## Required reads — file paths Claude must read
## Inputs         — concrete paths/evidence/hypothesis
## Expected output — file path + format + length bound
## Boundary       — what NOT to touch; daily limits; stop conditions
```

Invoke:

```bash
claude -p "Read hermes/calls/<file>.md and execute within Boundary." \
  --max-turns 20 \
  --allowedTools "Read,Edit,Write,Grep,Glob,Bash,mcp__playwright__*"
```

After return, append to the same call file:

```
## Result    — what Claude wrote
## Verdict   — accept | partial | reject
## Notes     — Hermes' assessment
```

## Verdict handling

- **accept** → integrate; log.
- **partial** → Hermes does the remainder if autonomous; else inbox.
- **reject** → no retry; inbox with reason.

## Budget

Per-call cap 20 turns. Daily cap in `hermes/state/budget.json` (default 12). Exceed → stop calling, inbox. Claude inherits `SAFETY.md`; if call needs operator-gated action, Hermes pauses and writes inbox first.
