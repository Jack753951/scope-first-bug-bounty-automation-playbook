> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# picoCTF sice_cream heap-pwn notes

Session context: local/offline CTF pwn analysis of `sice_cream` with provided `libc.so.6` and `ld-2.23.so`, plus optional remote `nc fickle-tempest.picoctf.net 50087`.

## Durable recognition pattern

`sice_cream` is a glibc 2.23 heap exploitation challenge, not a stack smash:

- 64-bit ELF, stripped, non-PIE, Full RELRO, canary, NX.
- `buy` allocates up to `0x58` bytes and reads exactly the requested size.
- `eat` frees `creams[index]` but does not clear the pointer: UAF / double free.
- `reintroduce` reads `0x100` bytes into global `name` at `.bss` and prints it with `%s`.
- `name` and the `creams` pointer table are adjacent in `.bss` (`name` around `0x602040`, `creams` around `0x602140` in the known binary).

## High-level exploit route

For this class of CTF, solve in stages instead of jumping straight to a final one-gadget:

1. Reverse menu behavior and global layout.
2. Confirm size class: `malloc(0x58)` produces a `0x60`-sized fastbin chunk, so fake fastbin size checks must match that class (`0x61` for glibc metadata), not an arbitrary nearby size.
3. Use double free pattern `free(A); free(B); free(A)` to poison the fastbin list.
4. Use a fake fastbin chunk in `.bss` immediately before `creams` to get an allocation overlapping the pointer table.
5. Write `creams[0]` to point at a fake larger/smallbin chunk in `name`.
6. Free that fake chunk with `eat(0)` so unsorted-bin metadata writes a `main_arena` libc pointer into controlled `.bss` memory.
7. Use `reintroduce` / `%s` overread to leak the libc pointer, then compute libc base.
8. For the validated `sice_cream` route, use another fake chunk + fastbin dup to overlap `main_arena` and overwrite the arena `top` pointer so the next top allocation lands near `__malloc_hook - 0x15`.
9. Allocate and write padding plus a one-gadget over `__malloc_hook`.
10. Trigger a glibc error-handling path, such as the double-free diagnostic, which indirectly calls `malloc` in glibc 2.23 and therefore jumps through the overwritten `__malloc_hook`.

This is a useful alternative when direct fastbin poisoning to `__malloc_hook` is awkward because menu allocation sizes are constrained; pivoting through `main_arena.top` can turn a restricted allocator interface into a hook overwrite.

## Pitfalls observed

- `read(size)` blocks until exactly `size` bytes arrive. Helper functions must pad payloads to the requested allocation size; otherwise later menu input is consumed as chunk data and the transcript becomes misleading.
- Do not assume adjacent malloc chunks are spaced by `0x70` just because the user data request is `0x58`. The actual chunk size class for `0x58` is `0x60` (`0x61` metadata), while allocator behavior and intervening bookkeeping can still make printed pointer deltas confusing. Validate fake chunk sizes against glibc fastbin checks.
- For fastbin poisoning, distinguish the address placed in `fd` from the user pointer returned by `malloc`. If you want `malloc` to return user pointer `X`, the fastbin candidate chunk header is at `X-0x10`; glibc validates the size at candidate `+0x8`.
- `%s` leaks stop at NUL and may include punctuation from the format string (`!\n`). Parse only the raw bytes between the controlled marker and the delimiter; do not blindly `u64` the whole tail.
- If pwntools/gdb/strace are missing in the environment, continue with deterministic Python `subprocess` tubes and `readelf`/`objdump`; do not turn missing local tools into a conclusion about the challenge.
- In glibc 2.23 CTFs, a libc diagnostic/error path can be an exploit trigger rather than only a crash. After overwriting `__malloc_hook`, deliberately causing a double-free error may invoke allocator-backed formatting/reporting and hit the hook.
- When allocation size is capped by the menu, do not give up on hook overwrite primitives. Consider corrupting `main_arena.top` so a legal request is served from a chosen address near the hook.

## Minimal helper pattern

When driving this binary without pwntools, implement helpers that always pad writes:

```python
def buy(io, size, payload):
    payload = payload.ljust(size, b'X')[:size]
    menu(io, 1)
    read_until(io, b'> ')
    sendline(io, str(size).encode())
    read_until(io, b'> ')
    send(io, payload)
```

Use this reference as a class example for heap CTFs with `.bss` overlap, fastbin dup, libc leak, and glibc 2.23 FSOP follow-up.
