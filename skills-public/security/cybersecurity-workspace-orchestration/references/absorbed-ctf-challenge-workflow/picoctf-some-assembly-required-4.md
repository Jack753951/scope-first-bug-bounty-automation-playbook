> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# picoCTF: Some Assembly Required 4 — WebAssembly validator pattern

Session-specific example for the CTF Challenge Workflow skill's WebAssembly validator section.

## Challenge shape

- Web challenge URL served a simple `index.html` with an input and a `Submit` button.
- HTML loaded an obfuscated JS file, e.g. `rqe4VVml5W.js`.
- JS fetched an extensionless WebAssembly module, e.g. `fetch('./ZoRd23o0wd')`.
- JS copied user input into WASM memory with:

```js
exports.copy_char(input.charCodeAt(i), i);
exports.copy_char(0, input.length);
exports.check_flag() == 1;
```

## Useful findings

WAT conversion exposed:

```wat
(export "memory" (memory $memory))
(export "check_flag" (func $check_flag))
(export "input" (global $input))
(export "copy_char" (func $copy_char))
(data (i32.const 1024) "\18j|a\118i7\1fYyY>\1cVc\0dB\1d~l9\1cZ!]c\11\00...")
```

`copy_char` stored input bytes at memory offset `1072 + index`.

`check_flag` transformed the buffer at offset `1072`, then called:

```wat
i32.const 1072
i32.const 1024
call $strcmp
```

So the challenge compared transformed input against the data segment at offset `1024`.

## Simplified transformation

The validation logic simplified to this forward transform:

```python
for i in range(len(input)):
    y[i] = input[i]
    y[i] ^= 20
    if i > 0:
        y[i] ^= y[i - 1]
    if i > 2:
        y[i] ^= y[i - 3]
    y[i] ^= i % 10
    y[i] ^= 9 if i % 2 == 0 else 8
    y[i] ^= [7, 6, 5][i % 3]

for i in range(0, len(y), 2):
    swap(y[i], y[i + 1])
```

Important detail: the dependencies use already-transformed prior `y` bytes.

## Inversion recipe

1. Extract target bytes from the full data segment, not merely up to the first null terminator.
2. Undo the final adjacent-pair swap.
3. For each byte, reverse XOR operations. Since XOR is self-inverse:

```python
c = enc
if i > 2:
    c ^= y[i - 3]
if i > 0:
    c ^= y[i - 1]
c ^= 7 if i % 3 == 0 else 6 if i % 3 == 1 else 5
c ^= 9 if i % 2 == 0 else 8
c ^= i % 10
c ^= 20
```

Here `y` is the post-transform/pre-swap byte array, not the plaintext.

## Verification lesson

Initial local WASM verification showed this malformed prefix returned success:

```text
picoCTF{1c4abb877272112e3923
```

The page/WASM accepted it because the transformed expected bytes contain an embedded NUL after that prefix and `strcmp` stops comparing there. That was a false positive, not the platform flag.

The full data segment includes bytes after the embedded NUL:

```text
18 6a 7c 61 11 38 69 37 1f 59 79 59 3e 1c 56 63
0d 42 1d 7e 6c 39 1c 5a 21 5d 63 11 00 62 05 49
4b 7e 61 34 1c 57 28 0f 52 00
```

Including those bytes and inverting the same transform produced the real picoCTF-format flag:

```text
picoCTF{1c4abb877272112e39233c05ade7abbb}
```

Durable lesson: `check_flag() == 1` is not enough if the candidate violates the expected platform format. For C-string validators, inspect full data segments past embedded NULs and look for prefix-collision traps.
