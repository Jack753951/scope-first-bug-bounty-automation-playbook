> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# WebAssembly CTF / Web Validator Reversing

Use this reference when a CTF/lab web challenge loads a `.wasm` or extensionless WebAssembly module, especially when the page exposes an input field and JS calls exports such as `check_flag`, `copy_char`, `strcmp`, `memory`, or similar validator functions.

## Safety / scope

1. Confirm the target is a CTF/training/lab instance or otherwise authorized before touching it.
2. Prefer passive/static retrieval of challenge assets (`index.html`, JS, WASM) over active probing.
3. Do not run scanners or fuzzers for simple WASM validator challenges; the flag is usually client-side.

## Workflow

1. Fetch the page and JS assets.
   - Inspect `<script src=...>` and obfuscated JS arrays.
   - Look for `fetch(...)`, `WebAssembly.instantiate(...)`, and export calls.
2. Download the WASM module.
   - Extensionless paths are common, e.g. `fetch('./ZoRd23o0wd')`.
   - Verify it is a WebAssembly binary with `file` or by magic bytes `00 61 73 6d`.
3. Read the JS-WASM boundary.
   - Identify input copy functions such as `copy_char(charCode, index)`.
   - Identify validation calls such as `check_flag()`.
   - Note whether JS appends a null terminator via `copy_char(0, input.length)`.
4. Convert WASM to WAT.
   - Use `wasm2wat`/`wasm-objdump` if installed.
   - If not installed and Node is available, use the `wabt` npm package locally for conversion.
5. Find key WASM artifacts.
   - Exports: `memory`, `check_flag`, `copy_char`, globals such as `input`.
   - Data segments: `(data (i32.const OFFSET) "...")` usually contain encrypted or transformed expected bytes.
   - Input buffer offset: often revealed by `copy_char` storing at `index + OFFSET`.
   - Comparison offset: `strcmp(expected_offset, transformed_input_offset)`.
6. Simplify `check_flag` into pseudocode.
   - Collapse verbose locals into operations on `buf[i]`.
   - Track operation order exactly.
   - Watch for signed-byte idioms: `i32.shl 24` then `i32.shr_s 24` means signed 8-bit extension.
7. Invert the transformation.
   - XOR transforms are self-inverse, but dependencies matter.
   - If the validator mutates `buf[i]` based on earlier transformed bytes, invert using the same already-recovered transformed bytes, not necessarily the plaintext bytes.
   - Undo final swaps/permutations before per-byte inversion.
8. Verify against the original WASM, then sanity-check the flag format.
   - Instantiate the WASM locally in Node/Python if possible.
   - Feed the recovered candidate with `copy_char` plus null terminator.
   - Confirm `check_flag() == 1`, but do not treat UI/WASM success as the only truth.
   - If the candidate is malformed for the platform format, inspect the full data segment past embedded `\x00` bytes before finalizing.

## Node + wabt conversion fallback

If `wasm2wat` is unavailable but `node`/`npm` exist:

```bash
mkdir -p setting/local/<challenge>
npm --prefix setting/local/<challenge> init -y >/dev/null
npm --prefix setting/local/<challenge> install wabt --silent
node - <<'NODE'
const fs = require('fs');
require('./setting/local/<challenge>/node_modules/wabt')().then(wabt => {
  const buf = new Uint8Array(fs.readFileSync('setting/local/<challenge>/module.wasm'));
  const mod = wabt.readWasm(buf, { readDebugNames: true });
  mod.generateNames();
  mod.applyNames();
  fs.writeFileSync('setting/local/<challenge>/module.wat', mod.toText({ foldExprs: false, inlineExport: false }));
});
NODE
```

Important: pass a `Uint8Array` to `wabt.readWasm`; passing a Node `Buffer` can fail in some environments.

## Local WASM verification pattern

```js
const fs = require('fs');
const wasm = fs.readFileSync('module.wasm');
(async () => {
  const { instance } = await WebAssembly.instantiate(wasm, {});
  const e = instance.exports;
  const candidate = 'picoCTF{...';
  for (let i = 0; i < candidate.length; i++) e.copy_char(candidate.charCodeAt(i), i);
  e.copy_char(0, candidate.length);
  console.log(e.check_flag());
})();
```

## Pitfalls

- Do not trust expected flag punctuation or the page's `Correct!` by itself. Verify the exact string accepted by the WASM and the platform's normal flag format.
- Embedded NUL bytes in transformed target data can create `strcmp` / `strlen` prefix false positives: a short malformed candidate may pass the browser checker because comparison stops at `\x00`, while the real flag continues in later data bytes.
- Do not extract only up to the first null terminator until you have checked whether later bytes decode to the rest of a valid flag.
- Do not stop at `strings`; WebAssembly data segments often hold non-printable transformed bytes.
- Obfuscated JS is usually only a loader. The validator logic is usually in WASM.
- Pair swaps/permutations often happen after per-byte transforms; invert in reverse order.
- `strcmp` requires null-terminated transformed input; if the candidate has an extra byte, validation can fail even when the visible prefix is correct.
