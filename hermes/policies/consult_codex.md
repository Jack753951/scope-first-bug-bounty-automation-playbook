> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Consult Codex

Load this file before invoking `codex` CLI.

## Call Codex for

- Platform/script/hermes/bin code changes (Hermes does not self-modify directly).
- Test work (new tests, regression, fixtures).
- Surgical fixes / deterministic patches.
- Security review of Hermes' platform changes (secret leakage, scope-bypass risk, validation gaps).
- Second opinion on Claude findings (does evidence actually demonstrate impact? controls present? redaction OK?).
- Diff review before high-stakes commits (optional).

## Do NOT call Codex for

- Browser/recon (Hermes' Playwright handles).
- Strategy/direction (operator + Hermes own).
- Routine state updates (Hermes does).
- Report narrative first pass (Claude is better).
- Design-first refactor (Claude is better).

## Call format

Write `hermes/calls/<YYYY-MM-DDTHH-MM>_codex_<topic>.md` BEFORE invoking:

```
## Task           — one sentence, deterministic, scoped
## Required reads — specific files
## Inputs         — paths, line ranges, diff snippets, evidence
## Expected output — patch + tests + verdict path
## Boundary       — what NOT to touch; validation criteria
```

Invoke:

```bash
codex exec --sandbox workspace-write \
  --output-last-message hermes/calls/<file>.codex_out.md - \
  <<< "Read hermes/calls/<file>.md and execute within Boundary."
```

After return, append `## Result`, `## Verdict`, `## Notes`.

## Verdict handling

- **accept** → integrate; log.
- **partial** → escalate missing part to inbox.
- **reject** → no retry; inbox.

For security-review calls: accept = no concrete blocker. Reject = blocker found → Hermes does not commit; inbox with Codex's reasoning.

## Budget

Single deterministic run per call, no multi-turn loop. Daily cap in `hermes/state/budget.json` (default 12). Codex inherits `SAFETY.md`; Hermes refuses to dispatch a Codex call that would touch `config/scope.txt`, `SAFETY.md`, `INDEX.md`, `.hermes.md`.
