> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# 2026-05-18 picoCTF workflow validation notes

These notes capture reusable lessons from a CTF workflow validation session. They are not a full transcript; use them as pattern reminders when solving future challenges.

## Workflow corrections from the user

- The purpose of CTF work is not only solving flags; use challenges to validate the agent workflow and improve vulnerability/weakness recognition.
- The user may intentionally omit the challenge category. Perform blind triage from description, files, and behavior.
- External websites, `nc` services, downloads from challenge instances, and security tools should default to Kali. Windows remains the orchestration/repo/Obsidian surface.
- After solving, make an output-side review decision: accept only if verified; escalate if ambiguous, probabilistic, high-impact, or format-weird.

## Case: WASM / C-string embedded NUL trap

Pattern:

- A checker can return success for a prefix if it uses C-string semantics such as `strcmp`/`strlen`.
- Embedded NUL bytes can truncate comparison even when the full flag continues after the NUL.

Pitfall:

- Do not stop at UI success or a short prefix that lacks a normal closing delimiter.
- Inspect the full WASM data segment / memory and verify flag completeness.

Review trigger:

- `strcmp`, `strlen`, embedded NULs, truncated output, missing `}` or other expected terminator.

## Case: Java Script Kiddie — column-shifted PNG/QR

Pattern:

- Client-side JS rebuilt an image from a byte array using a 16-digit key.
- The key controlled per-column shifts of a byte matrix.
- PNG magic bytes and IHDR structure gave constraints for the key.
- Ambiguous columns were resolved by validating PNG chunks/CRC.
- Final QR decode produced the flag.

Reusable method:

1. Read the JavaScript transform.
2. Model the byte arrangement as rows/columns if indexing uses `j * LEN + i`.
3. Use magic bytes such as PNG signature/IHDR to infer shifts.
4. Validate with file parser / CRC before decoding QR/barcode.
5. Treat visual or partial decode as insufficient without structural validation.

## Case: vault-door-8 — Java bit-swap inversion

Pattern:

- Java source checked `scramble(password)` against a constant array.
- `scramble` was a sequence of `switchBits` operations.
- Bit swaps are self-inverse; invert by applying the same swaps in reverse order.

Reusable method:

1. Find the final equality check and expected constants.
2. Extract the transform.
3. Determine if operations are reversible/permutations.
4. Apply inverse order to expected bytes.
5. Verify by reapplying original transform to the candidate.

## Case: Clouds — Nimbus custom cipher differential cryptanalysis

Pattern:

- Provided `clouds.py` implemented a 5-round 64-bit custom block cipher.
- Service exposed a chosen-plaintext encryption oracle and encrypted flag note.
- Round function:

```python
x ^= key
x = bit_reverse_64(x)
x = x * (key | 1) mod 2**64
```

Triage lessons:

- Generic Z3 with 5 x 64-bit key variables and modular multiplication was too slow.
- A public writeup flag was stale/instance-specific and failed verification, so it was not trusted.
- This correctly triggered escalation to research/agent review.

Attack outline:

- Use differential `Δ = 2^63 - 2 = 0x7ffffffffffffffe`.
- `Δ` is bit-palindromic, so bit reversal preserves it.
- Multiplication by odd subkeys preserves this differential with useful probability.
- Generate chosen plaintext pairs `(P, P ^ Δ)` with even endpoints.
- Recover last-round key candidates statistically from pairs passing a condition.
- Partially decrypt and recurse for remaining subkeys.
- Verify recovered keys by re-encrypting oracle plaintext/ciphertext pairs.

Verification rule:

- For probabilistic crypto attacks, never accept decrypted-looking output alone. Verify recovered key material against independent oracle pairs.

## General output-side review triggers observed

Escalate to second review or deeper verification when:

- first answer lacks expected wrapper/terminator;
- candidate depends on UI success only;
- binary/string boundary can truncate content;
- multiple candidates remain after inversion;
- solver result may be underconstrained;
- attack is probabilistic/statistical;
- public writeup answer could be stale;
- external target-touching step beyond minimal CTF interaction is needed.
