> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 0.1 Full Audit Rows

Archived from the temporary validation lab before cleanup. These are local dry-run audit rows only; no live scans were run.

## punycode_allowed

```text
2026-05-15T08:21:47Z | user=Owner | target=xn--bcher-kva.example | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=initial_target: in scope
2026-05-15T08:21:47Z | user=Owner | target=xn--bcher-kva.example | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=find_live_hosts.input: in scope
2026-05-15T08:21:47Z | user=Owner | target=xn--bcher-kva.example | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=find_live_hosts.output: in scope
2026-05-15T08:21:47Z | user=Owner | target=xn--bcher-kva.example | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=port_scan.input: in scope
```

## scanme_dryrun

```text
2026-05-15T08:21:53Z | user=Owner | target=scanme.nmap.org | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=initial_target: in scope
2026-05-15T08:21:53Z | user=Owner | target=scanme.nmap.org | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=domain_expansion: in scope
2026-05-15T08:21:54Z | user=Owner | target=scanme.nmap.org | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=find_live_hosts.input: in scope
2026-05-15T08:21:54Z | user=Owner | target=scanme.nmap.org | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=find_live_hosts.output: in scope
2026-05-15T08:21:54Z | user=Owner | target=scanme.nmap.org | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=port_scan.input: in scope
```

## trailing_dot_rejected

```text
2026-05-15T08:21:53Z | user=Owner | target=example.com. | event=SAFE_TARGET_FAIL | intensity=normal | dry_run=true | reason=initial_target: target is not a supported IP, CIDR, domain, or HTTP(S) URL
```

## unicode_idn_rejected

```text
2026-05-15T08:21:48Z | user=Owner | target=b?cher.example | event=SAFE_TARGET_FAIL | intensity=normal | dry_run=true | reason=initial_target: target is not a supported IP, CIDR, domain, or HTTP(S) URL
```

## wildcard_apex_observed

```text
2026-05-15T08:21:51Z | user=Owner | target=example.com | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=initial_target: in scope
2026-05-15T08:21:51Z | user=Owner | target=example.com | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=find_live_hosts.input: in scope
2026-05-15T08:21:51Z | user=Owner | target=example.com | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=find_live_hosts.output: in scope
2026-05-15T08:21:52Z | user=Owner | target=example.com | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=port_scan.input: in scope
```

## wildcard_deep_allowed

```text
2026-05-15T08:21:49Z | user=Owner | target=a.b.example.com | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=initial_target: in scope
2026-05-15T08:21:49Z | user=Owner | target=a.b.example.com | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=find_live_hosts.input: in scope
2026-05-15T08:21:49Z | user=Owner | target=a.b.example.com | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=find_live_hosts.output: in scope
2026-05-15T08:21:50Z | user=Owner | target=a.b.example.com | event=SAFE_TARGET_OK | intensity=normal | dry_run=true | reason=port_scan.input: in scope
```
