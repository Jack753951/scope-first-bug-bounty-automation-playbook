> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 0.1 Validation Evidence

Date: 2026-05-15
Owner: Codex
Scope: Validation evidence only; no live scans, no new recon features, no changes to `config/scope.txt`.

## Method

Used isolated relative temp lab root:

```text
.tmp_phase0_1_validation_20260515_162146_329
```

Each case used its own temp `lab/config/scope.txt`, temp log directory, and temp output directory. All `recon.sh` invocations used `--dry-run`.

## Command Matrix

```bash
./recon.sh --dry-run --scope <temp>/punycode_allowed/lab/config/scope.txt -o <temp>/punycode_allowed/out xn--bcher-kva.example
./recon.sh --dry-run --scope <temp>/unicode_idn_rejected/lab/config/scope.txt -o <temp>/unicode_idn_rejected/out bücher.example
./recon.sh --dry-run --scope <temp>/wildcard_deep_allowed/lab/config/scope.txt -o <temp>/wildcard_deep_allowed/out a.b.example.com
./recon.sh --dry-run --scope <temp>/wildcard_apex_observed/lab/config/scope.txt -o <temp>/wildcard_apex_observed/out example.com
./recon.sh --dry-run --scope <temp>/trailing_dot_rejected/lab/config/scope.txt -o <temp>/trailing_dot_rejected/out example.com.
./recon.sh --dry-run --scope <temp>/scanme_dryrun/lab/config/scope.txt -o <temp>/scanme_dryrun/out --domain scanme.nmap.org
```

## Results

| Case | Temp scope entry | Target | Exit | Result |
|---|---|---|---:|---|
| Punycode allowed | `xn--bcher-kva.example` | `xn--bcher-kva.example` | 0 | Allowed |
| Raw Unicode IDN rejected | `xn--bcher-kva.example` | `bücher.example` | 1 | Rejected as unsupported target syntax |
| Wildcard deep subdomain | `*.example.com` | `a.b.example.com` | 0 | Allowed |
| Wildcard apex observed | `*.example.com` | `example.com` | 0 | Allowed under current semantics |
| Trailing dot rejected | `example.com` | `example.com.` | 1 | Rejected as unsupported target syntax |
| scanme dry-run audit | `scanme.nmap.org` | `scanme.nmap.org` with `--domain` | 0 | Allowed in dry-run temp scope |

## Audit Excerpts

Punycode allowed:

```text
2026-05-15T08:21:47Z | user=Owner | target=xn--bcher-kva.example | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=initial_target: in scope
```

Raw Unicode IDN rejected. The console rendered the non-ASCII character as `?` in this environment:

```text
2026-05-15T08:21:48Z | user=Owner | target=b?cher.example | event=SAFE_TARGET_FAIL | intensity=normal | dry_run=true | reason=initial_target: target is not a supported IP, CIDR, domain, or HTTP(S) URL
```

Wildcard positive:

```text
2026-05-15T08:21:49Z | user=Owner | target=a.b.example.com | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=initial_target: in scope
```

Wildcard apex observed:

```text
2026-05-15T08:21:51Z | user=Owner | target=example.com | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=initial_target: in scope
```

Trailing dot rejected:

```text
2026-05-15T08:21:53Z | user=Owner | target=example.com. | event=SAFE_TARGET_FAIL | intensity=normal | dry_run=true | reason=initial_target: target is not a supported IP, CIDR, domain, or HTTP(S) URL
```

`scanme.nmap.org` dry-run audit:

```text
2026-05-15T08:21:53Z | user=Owner | target=scanme.nmap.org | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=initial_target: in scope
2026-05-15T08:21:53Z | user=Owner | target=scanme.nmap.org | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=domain_expansion: in scope
2026-05-15T08:21:54Z | user=Owner | target=scanme.nmap.org | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=find_live_hosts.input: in scope
2026-05-15T08:21:54Z | user=Owner | target=scanme.nmap.org | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=find_live_hosts.output: in scope
2026-05-15T08:21:54Z | user=Owner | target=scanme.nmap.org | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=port_scan.input: in scope
```

## Required Validation Commands

```bash
bash -n recon.sh
USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review
```

Results:

- `bash -n recon.sh`: exit `0`.
- Hermes review: exit `0`; reported shell scripts `bash -n OK`, runtime lock clear, and non-git workspace status.
- Limitation: the Hermes review invocation emitted sandbox-specific `mkdir: cannot create directory '<user-home>': Permission denied` warnings from Git Bash absolute path handling, but completed successfully.

## Wildcard Semantics

Current Phase 0 behavior: `*.example.com` includes both subdomains such as `a.b.example.com` and the apex `example.com`.

This is already documented in `config/scope.txt` (`*.example.com` matches both subdomains and `example.com` itself). Phase 1 should treat this as a preserve-or-change policy decision for `programs/<slug>/scope.json`: preserve the current rule unless the operator intentionally chooses stricter bug-bounty-style semantics where apex and wildcard entries are distinct.
