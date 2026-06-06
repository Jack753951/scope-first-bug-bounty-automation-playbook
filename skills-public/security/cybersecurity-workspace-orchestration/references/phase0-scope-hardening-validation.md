> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 0 Recon Scope-Hardening Validation Pattern

Use this reference when hardening a cybersecurity workspace recon pipeline before any authorized active testing.

## Durable lessons

- Treat scope logic as a runtime guard, not just an entrypoint check. A single `safe_target`-style function should normalize host/URL input, reject malformed/ambiguous targets, check authorization scope, and emit a concrete pass/fail reason.
- Revalidate expansion outputs before later stages touch them. Subdomain enumeration, CT log output, http probe output, port-scan output, and URL construction can all introduce new host/URL strings that need the same guard.
- Preserve CLI compatibility flags cautiously. A legacy `--skip-scope-check` can remain only if it is impossible to produce network egress: require matching per-session override variables and force dry-run semantics.
- Refuse config-level scope disabling (`REQUIRE_SCOPE_CHECK=false`) as a hard error in offensive/bug-bounty automation workspaces.
- Scanner output remains triage only; generated summaries should repeat manual verification/evidence/remediation/retest expectations.

## Local validation recipe

Run validation only with synthetic/local scope and fake tools unless the operator has approved a lab/scope target.

1. Syntax:
   ```bash
   bash -n recon.sh
   bash -n bin/hermes
   ```
2. Unauthorized target should fail even in dry-run:
   ```bash
   tmp=$(mktemp -d)
   printf 'authorized.example\n*.authorized.example\n' > "$tmp/scope.txt"
   HACKLAB=/path/to/project USER=${USER:-Owner} bash recon.sh --dry-run --scope "$tmp/scope.txt" unauthorized.example
   # expect non-zero
   ```
3. Authorized target should pass in dry-run with synthetic scope.
4. Config disabling should fail by using a temp `HACKLAB` containing `config/recon.conf` with `REQUIRE_SCOPE_CHECK=false` and a temp `config/scope.txt`.
5. Scope override should fail without matching env vars and pass only as forced dry-run with:
   ```bash
   SCOPE_OVERRIDE_TOKEN=abc SCOPE_OVERRIDE_CONFIRM=abc bash recon.sh --skip-scope-check unauthorized.example
   ```
7. Close validation-evidence gaps before moving phases when an independent reviewer flags them. Useful Phase 0.1 rows include:
   - punycode allowed (`xn--bcher-kva.example`) with matching temp scope
   - raw Unicode IDN rejected against punycode-only scope
   - wildcard positive (`a.b.example.com` under `*.example.com`)
   - trailing-dot rejection (`example.com.`)
   - dry-run audit evidence for a scope-listed public test hostname such as `scanme.nmap.org`, using an isolated temp lab root and `--dry-run` only
8. Document wildcard semantics explicitly. If `*.example.com` currently includes the apex `example.com`, record whether Phase 1 should preserve that rule or intentionally migrate to stricter bug-bounty-style semantics.
9. Archive useful temp-lab audit rows into `handoff/` before deleting temp validation directories, so evidence survives cleanup.

## Windows/Git-Bash pitfall

Project review wrappers may call `python3`, but on some Git-Bash/MSYS hosts `python3` exists and exits with a launcher/setup code while Windows `python` works. If a wrapper reports Python compile failure but direct Windows `python -m py_compile ...` succeeds, patch the wrapper to select a runnable candidate (`python3` or `python`) before compiling.
