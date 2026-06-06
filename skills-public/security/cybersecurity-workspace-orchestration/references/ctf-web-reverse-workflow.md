> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# CTF Web / Reverse Workflow Notes

Use this reference for explicit CTF/training tasks where the user provides a challenge URL, instance, or local source. It captures a lightweight version of the scan-to-verification pipeline without overusing the full multi-agent platform workflow.

## Operating model

- Confirm the target is a CTF/training/local-lab challenge before external interaction.
- For this user's cybersec workspace, prefer Kali for external challenge URLs, downloads, curl/wget, and tooling. Keep Windows as control plane for Obsidian, repo-local artifacts, orchestration, and final notes.
- Use minimal interaction: fetch the page/assets/source needed for the challenge; do not run broad recon, fuzzing, directory brute force, or intrusive scanning unless the challenge explicitly requires it and scope is clear.
- Store downloaded challenge artifacts and throwaway solvers under a git-ignored local workspace such as `setting/local/<challenge-slug>/`; store durable lessons in Obsidian, not memory.

## Lightweight CTF pipeline

1. Scope gate: identify CTF/training platform and explicit instance URL.
2. Kali-first external access: fetch only required page/assets/attachments from Kali.
3. Initial triage: classify Web/JS/WASM/reverse/crypto/forensics/pwn/misc and decide whether a single-agent solve is enough.
4. Solve locally/offline when possible: inspect source, transform assets, reverse client logic, or decode generated media.
5. Candidate verification: verify flag format and the checker/result independently.
6. Output-side review decision: trigger a second review when the answer or checker is ambiguous.
7. Save durable technique notes in Obsidian; keep Hermes memory to a compact trigger only when broadly reusable.

## Output-side review triggers for CTFs

Escalate to a second review (self-review, Claude/Cowork, or Codex depending on task shape) when any of these occur:

- Candidate flag lacks a normal closing delimiter or otherwise violates expected flag format.
- UI says `Correct` but the candidate is malformed or suspicious.
- The checker uses C-string APIs such as `strcmp`, `strlen`, or `strcpy`.
- Binary/WASM data contains embedded NUL bytes before apparent data end.
- Multiple keys/candidates decode to plausible output.
- File reconstruction has ambiguous bytes due repeated header values such as `00`.
- QR/barcode/OCR output is low confidence or visually hard to read.
- The next step would send a payload, scan, fuzz, or otherwise touch the remote target beyond simple asset fetches.

## WASM / C-string pitfall

In WASM/browser checkers, `strcmp`/`strlen` semantics can create a prefix false positive when transformed expected data contains an embedded NUL. Do not stop at the first NUL in a data segment, and do not trust UI `Correct` alone. Inspect the full data segment and validate complete flag format.

Session example: picoCTF `Some Assembly Required 4` had a short prefix accepted by the browser checker, but the full flag continued after an embedded NUL in transformed bytes.

## JavaScript image reconstruction pattern

For JS image reconstruction challenges:

1. Read the JavaScript transformation first instead of guessing input.
2. Identify the file-format magic/header bytes (for PNG: `89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52`).
3. Use fixed header bytes to recover key material or column/row shifts.
4. If repeated bytes create ambiguity, validate candidate files with format-level checks such as PNG chunk CRCs.
5. Decode QR/barcode output with tooling, then verify the final flag format.

Session example: picoCTF `Java Script Kiddie` used a 16-digit key to column-shift PNG bytes. PNG header bytes recovered most candidates; PNG CRC validation selected the only valid key; QR decode yielded the flag.

## When not to use the heavy multi-agent loop

Small CTF/reverse tasks can start as single-agent work after scope gate. However, format anomalies, ambiguous candidates, high-risk remote interaction, or claims of a confirmed vulnerability should trigger output-side review. Reserve the full Hermes → Claude/Cowork → Codex loop for platform changes, new verification scripts, safety boundaries, report schemas, or non-trivial automation that will persist in the repo.
