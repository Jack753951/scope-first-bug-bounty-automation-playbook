> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Proposal — Conditional allowance for low-intensity in-scope discovery

Date: 2026-05-29
Author: Claude (consultant)
Status: **PROPOSAL — operator decision required**. Does not take effect until the operator edits `SAFETY.md`.
Authority note: `SAFETY.md` is operator-approved only (`CLAUDE.md`, `INDEX.md`). This file proposes; it does not change the binding contract.

## Problem

The `SAFETY.md` one-sentence rule lumps `scans/fuzzing/DAST/OAST/SSRF/exploit attempts/high-volume automation` into a single hard stop. That correctly blocks aggressive/DoS-like behavior, but it also blocks **low-intensity, read-only content/parameter discovery** (e.g. wordlist-based directory/endpoint/parameter enumeration with `ffuf`/`dirsearch`).

In the wider ecosystem, low-intensity read-only discovery is routine and commonly allowed **when the program's own policy permits automated tooling and you stay within rate limits**. Blocking it entirely throttles exactly the cheap, safe recon that improves coverage and reduces duplicates, with little safety upside.

## Design principle (unchanged): fail-closed

The relaxation does **not** flip the default. Default remains STOP. The carve-out activates **only** when a set of explicit positive markers all hold simultaneously; any missing/ambiguous precondition fails closed. This preserves the project's "if you can't tell, stop" stance — it just moves the decision into operator-set per-program markers instead of a blanket ban.

## Proposed `SAFETY.md` change

Keep the one-sentence rule **as-is** (everything stays a hard stop by default). Add the following new section after `## Authority`:

---

```markdown
## Conditional allowance — low-intensity in-scope discovery

The hard stop on "scans/fuzzing" is narrowed for ONE action class only, and only
when ALL preconditions below hold at once. If any precondition is missing,
ambiguous, or unverifiable, the action FAILS CLOSED (stop and ask).

1. Action is READ-ONLY discovery: wordlist-based directory / endpoint / parameter
   enumeration. It MUST NOT inject payloads meant to alter state, trigger
   injection/deserialization, fetch external resources (no OAST/SSRF), brute-force
   credentials, upload, or crash/exhaust the service. Anything beyond read-only
   enumeration remains a hard stop.
2. The exact target is inside the `config/scope.txt` x `programs/<slug>/scope.json`
   intersection.
3. That program's `scope.json` carries an operator-set block:
   `"discovery_automation": { "allowed": true, "max_rps": <n>, "wordlist_cap": <n> }`.
   Absent or `allowed: false` => hard stop.
4. The program's PUBLISHED policy explicitly permits automated tooling/scanning.
   If policy is silent, ambiguous, or prohibits it => hard stop.
5. Request volume stays at or below the SMALLER of the program policy's stated
   limit and `max_rps`; the run is reversible, evidence-safe, and logged.
6. No authentication material, secrets, customer/non-owned data, OAST/SSRF, or
   external side effects are involved.

All other scanning / fuzzing / DAST / OAST / SSRF / exploit / high-volume or
mutation/crash-capable automation remains a hard stop under the one-sentence rule.
```

---

## Dependencies (must land with or before the SAFETY.md edit)

- **`programs/_schema/scope.schema.json`** (Codex + operator): add the optional
  `discovery_automation` object (`allowed` bool, `max_rps` int, `wordlist_cap` int).
  Until the schema validates it, no `scope.json` can carry the flag and the
  carve-out is dormant (still fails closed) — acceptable interim state.
- **Per-program `scope.json`** (operator only): the flag must be set deliberately,
  per program, after reading that program's policy. Never default-on.
- Optional: a recon-runner precheck that refuses to run unless it can read
  `discovery_automation.allowed === true` and a `max_rps` for the target slug.

## What this explicitly does NOT change

- No payload-injecting fuzzing, DAST, OAST, SSRF, exploit attempts.
- No high-volume / mutation / crash-capable automation.
- No auth/OTP/CAPTCHA/KYC/payment/integration gates.
- No change to report-ready promotion, disclosure, or submission gates.
- Default for any program without the explicit flag stays STOP.

## Why this is safe to adopt

- Narrow: one named action class, read-only only.
- Fail-closed: four independent positive conditions (scope intersection, per-program
  flag, published policy permission, rate cap) must all hold; any gap => stop.
- Operator-gated: the flag is operator-only per program, so a human still decides
  "this specific program permits this," matching the existing trust model.
- Reversible: remove the section / set `allowed: false` to revert instantly.

## Rollback

Delete the added `SAFETY.md` section, or set every program's
`discovery_automation.allowed` to `false`. Either fully restores the prior blanket
hard stop.

## Operator decision

- [ ] approve as written
- [ ] approve with edits (note below)
- [ ] reject

Notes:
