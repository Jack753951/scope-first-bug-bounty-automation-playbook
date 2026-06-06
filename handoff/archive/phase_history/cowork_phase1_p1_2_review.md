> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Independent Review: Phase 1 P1-2 Program Scope Validator

Generated: 2026-05-15
Reviewer: Claude (Cowork independent review)
Scope under review: offline program scope validator only (`scripts/validate_program_scope.py`, `scripts/test_validate_program_scope.py`, `programs/README.md`, `programs/_schema/README.md`, `programs/_examples/**`).

## Verdict

**ACCEPT.** No blocking issues found.

The validator is genuinely offline and default-deny. Across the supplied invalid fixtures and 20+ additional probes I ran by hand, every malformed or unsafe input produced `verdict: deny` and a non-zero exit. No runtime recon, config, or scope changes are wired in by this phase — confirmed by reading the source, not just the handoff notes.

## What I Checked

- Read in full: `scripts/validate_program_scope.py`, `scripts/test_validate_program_scope.py`, `programs/README.md`, `programs/_schema/README.md`, all three safe examples, all five invalid fixtures, and `handoff/codex_review.md`.
- Ran offline only: `python -m py_compile`, `python -m unittest scripts/test_validate_program_scope.py -v`, validator against each safe example with `--ignore-time`, validator against each invalid fixture with `--json`, plus a 20-case edge-probe battery exercising paths the fixtures do not cover.
- No network calls. No scans. No execution of `recon.sh` or any scanner. No edits to `config/scope.txt`, `config/recon.conf`, or `recon.sh`.

## Validation Results I Reproduced

- PASS: `python -m py_compile scripts/validate_program_scope.py scripts/test_validate_program_scope.py`.
- PASS: `python -m unittest scripts/test_validate_program_scope.py` — 6/6 tests pass on Python 3.12.8.
- PASS: All three safe examples (`public-bounty`, `client-engagement`, `ctf-platform`) return `verdict: allow` with `--ignore-time` and empty errors/warnings.
- PASS: All five invalid fixtures return `verdict: deny`, exit code 1, with a precise first error:
  - `expired-program`: `expiration: program scope is expired`
  - `forbidden-allowed-technique`: `techniques.allowed: non-authorizable techniques cannot be allowed: dos`
  - `overlap-techniques`: `techniques: techniques cannot be both allowed and forbidden: port_scan`
  - `overnight-window`: `testing_windows.allowed[0]: window end must be after start; split overnight windows`
  - `raw-unicode-idn`: `scope.in_scope[0].value: raw Unicode/IDN entries are not allowed`

## Default-Deny Probes (Beyond Provided Fixtures)

All produced `verdict: deny` with appropriate error paths:

| Probe | First error |
|---|---|
| empty object `{}` | `$: missing required keys: expiration, program, rate_limits, schema_version, scope, techniques, testing_windows` |
| malformed JSON file | `$: invalid JSON: Expecting value at line 1, column 1` |
| missing file | `$: file not found` |
| extra unknown top-level key | `$: unknown keys: extra_thing` |
| `schema_version="2.0"` | `schema_version: must equal '1.0'` |
| empty `scope.in_scope` | `scope.in_scope: must contain at least one entry` |
| negative `rate_limits.max_concurrency` | `must be a positive integer` |
| zero `rate_limits.max_concurrency` | `must be a positive integer` |
| empty `rate_limits` object | `rate_limits: must contain at least one safe cap` |
| `testing_windows.always=true` on `<bug-bounty-platform>` platform | `always=true is allowed only for lab, ctf, or self-hosted programs` |
| `idn_handling="allow_idn"` | `unsupported IDN handling 'allow_idn'` |
| `url_prefix` missing path | `url_prefix must include a path prefix` |
| `url_prefix` with userinfo | `url_prefix must not contain userinfo` |
| IPv6 in `cidr` entry | `must be a valid IPv4 CIDR` |
| timestamp `2026-05-15T00:00:00+00:00` (no `Z`) | `must be an ISO-8601 UTC timestamp ending in Z` |
| JSON root is a list | `$: expected object, got list` |
| duplicate `http_probe` in `techniques.allowed` | `duplicate technique 'http_probe'` |
| `True` (bool) where int expected in `rate_limits` | `expected integer, got bool` |
| unknown technique tag `quantum_pwn` | `unknown technique 'quantum_pwn'` |
| `include_apex: "yes"` (string) | `expected boolean` |
| unknown key in scope entry | `unknown keys: wat` |
| blackout `from == to` | `blackout to must be after from` |

The `automation_permitted=false` case correctly returns `allow` at this layer — runtime enforcement of that flag is explicitly a future P1-3 concern, documented in both `programs/README.md` and the handoff. Not a defect.

## Semantic Checks Confirmed in Source

Verified by reading `scripts/validate_program_scope.py`:

- Closed top-level key set with all keys required (`TOP_LEVEL_KEYS == REQUIRED_TOP_LEVEL`, line 75).
- Strict `schema_version == "1.0"` equality (line 615).
- Slug regex `^[a-z0-9][a-z0-9-]{0,63}$` and slug-must-match-path enforcement for `programs/<slug>/scope.json` (lines 284–292, helper at 264–272). Correctly does not apply under `_examples/` or `_schema/`.
- `program.platform` closed enum; `program.url` requires http/https/file scheme and ASCII.
- ISO-8601 UTC timestamps must end in `Z` and be parseable; rejects naive or non-`Z` forms (lines 209–224).
- Wildcard entries require `*.` prefix; remainder validated as domain (lines 340–346).
- Domain values: lowercase ASCII/punycode only, ≤253 chars, no trailing dot, ≥2 labels, no empty labels, ≤63 chars per label, no leading/trailing hyphen, restricted character set (lines 231–250).
- `cidr` is IPv4 only (`ipaddress.IPv4Network`); `ip` is IPv4 only (`IPv4Address`).
- `url_prefix`: rejects non-http(s) scheme, userinfo, missing host, missing path, query, fragment, bad port; host validated as domain.
- Technique vocabulary closed; allowed/forbidden overlap detected; non-authorizable techniques (`dos`, `credential_brute_force`, `social_engineering`, `physical`, `malware`, `callback_payloads`) blocked from `allowed`; duplicates within a list detected (lines 411–443).
- `rate_limits`: closed key set, must be non-empty, each value must be a positive int and explicitly not a bool (line 465 rejects `bool` before `int` check — important since `isinstance(True, int)` is True in Python).
- `testing_windows.always=true` restricted to `{lab, ctf, self-hosted}` only (lines 519–526). When `always=false`, timezone and at least one window are required.
- Window times use `HH:MM` 24-hour format and require `start < end`, which forces operators to split overnight windows.
- `expiration.valid_until > valid_from`; current-time active window enforced unless `--ignore-time`. Warns if validity window > 365 days.
- `--ignore-time` skips only current-time active checks; it does **not** skip ordering or parsing (verified by reading and by behavior — invalid fixtures still deny under `--ignore-time` for non-time reasons).
- `out_of_scope` entries get the same per-entry value validation as `in_scope` (line 399 loop covers both keys).
- `scope.idn_handling` restricted to `punycode_only` / `reject_idn`; raw Unicode scope values rejected independently (defense in depth — even if the enum check were bypassed, the entry validator at line 327 rejects non-ASCII).

## No Runtime / Recon / Config / Scope Changes

Confirmed by reading the validator end-to-end and inspecting the file list:

- The validator only `json.load`s the supplied path and prints to stdout. No invocation of `recon.sh`, no edits to `config/scope.txt` / `config/recon.conf`, no scanner spawning, no network I/O, no subprocess calls at all.
- `scripts/validate_program_scope.py` and the test do not import any project module that touches runtime state.
- README files for `programs/` and `programs/_schema/` repeatedly and accurately describe P1-2 as offline shape/semantic validation, with P1-3 explicitly deferred.
- The `handoff/codex_review.md` P1-2 section accurately reflects what is in the code; no claimed behavior is missing.

## Tests

- 6 unit tests cover: safe-example acceptance, invalid-fixture rejection, JSON output shape, slug/path mismatch via real tmp path under `programs/expected-example/scope.json`, expiration current-time vs. `--ignore-time`, and punycode-allowed vs. raw-Unicode-denied.
- Tests load the module by file path with `importlib.util`, which is the correct pattern for a project without a package install step.
- Coverage is adequate for the P1-2 surface. Suggested (non-blocking) additions for P1-3 or later: a test asserting that `--ignore-time` still denies non-time errors (today implicitly covered via `test_invalid_examples_fail` since the expired fixture also depends on time, but a direct test would lock in the semantic), and a test covering `testing_windows.always=true` on non-safe platforms.

## Extensibility

The design is clean for future expansion:

- Vocabulary sets (`TECHNIQUES`, `NON_AUTHORIZABLE_TECHNIQUES`, `PROGRAM_PLATFORMS`, `SCOPE_ENTRY_TYPES`, `RATE_LIMIT_KEYS`, etc.) are module-level constants — adding a new technique or platform is a one-line change plus a test.
- Each top-level block has its own `_validate_*` helper invoked from `validate_data`. Adding a new block is additive: extend `TOP_LEVEL_KEYS`, add a `_validate_newblock`, call it from `validate_data`. No control-flow refactor required.
- `ValidationResult.as_dict()` provides a stable, machine-consumable shape (`path`, `program_slug`, `verdict`, `errors`, `warnings`) that the future P1-3 runtime loader can consume directly.
- `validate_data` and `validate_file` are both public entry points; importable in-process (as the test demonstrates) without launching the CLI. P1-3 can call `validate_file(...)` and gate on `result.verdict == "allow"` before any global-scope intersection.

## Minor, Non-Blocking Observations

These are not defects and do not affect the verdict. Recording for future iteration:

1. `_validate_program` URL check at line 304 relies on Python precedence (`and` binds tighter than `or`). It is functionally correct but parentheses would aid readers: `if parsed.scheme not in {"http","https","file"} or (not parsed.netloc and parsed.scheme != "file"):`.
2. In `_validate_scope_entry` for `url_prefix`, the clause `or parsed.path == ""` at line 377 is unreachable (empty string never `.startswith("/")`). Cosmetic.
3. `program.url` accepts `file:` scheme. That seems intentional for archived local policy references, but worth a brief mention in `programs/README.md` if operators are expected to use it. Today only http(s) examples exist.
4. `cidr` and `ip` are IPv4-only by design. If a future engagement needs IPv6 scope, a new `cidr6`/`ip6` entry type would be cleanest (don't widen `cidr`).
5. The validator does not check for the same value appearing in both `in_scope` and `out_of_scope` of a single program. The documented semantic ("out_of_scope wins") is a runtime concern, so this is fine for P1-2 — but P1-3 should add an explicit precedence test.
6. Timezone string is validated for IANA-like shape; `ZoneInfo` failure is intentionally swallowed for Windows distributions lacking the IANA DB. The comment in `_validate_testing_windows` already documents this. P1-3/P1-4 runtime evaluation will need to fail closed if the zone is genuinely unknown.

## Recommendation

Accept P1-2 as offline loader/validator. Proceed to P1-3 (`recon.sh` integration) with the understanding that runtime enforcement still needs to be added explicitly: global-scope intersection with `config/scope.txt`, per-target allow/deny, stage technique gates, automation flag enforcement, effective rate computation, current-window/blackout evaluation, and audit-event emission. P1-3 should treat `validate_file()` returning `verdict: allow` as a necessary-but-not-sufficient precondition, never as the sole authorization signal.
