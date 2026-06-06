> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Bug Bounty Submission — <specific-cve-id> (NGINX Rift)

- **Program:** _<program name>_
- **In-scope asset:** _<hostname / asset ID exactly as listed in scope>_
- **Reporter:** _<your handle / contact>_
- **Date:** _<YYYY-MM-DD>_
- **Severity (CVSS v4):** **9.2 — Critical**
- **Weakness class:** CWE-122 Heap-based Buffer Overflow (`ngx_http_rewrite_module`)
- **CVE:** <specific-cve-id> ("NGINX Rift")

---

## 1. Summary

The asset `<host>` is serving traffic from **nginx `<version>`**, which is inside the publicly-disclosed vulnerable range for <specific-cve-id> (nginx OSS **0.6.27 – 1.30.0**, nginx Plus **R32 – R36**). The vulnerability is an unauthenticated, pre-auth heap-based buffer overflow in the rewrite module, reachable with a single crafted HTTP request. It results in a guaranteed worker-process crash (DoS) and, on hosts with ASLR weakened or disabled, can be escalated to remote code execution in the worker user's context.

I confirmed the version via **passive header inspection only**. I did **not** send the trigger payload against your production environment. With written authorization I can validate the bug against a staging host.

## 2. Evidence (passive fingerprint)

```
$ curl -sI https://<host>/
HTTP/1.1 200 OK
Server: nginx/<version>
Date: <RFC1123 date>
...
```

Scanner output:

```
vulnerable      https://<host>/    nginx=<version>    :: nginx <version> is inside the
                                                         <specific-cve-id> vulnerable range (0.6.27 – 1.30.0).
```

(Scanner used: a passive header-fingerprint tool — no exploit payload was sent.)

## 3. Vulnerability detail

<specific-cve-id> is a size/write mismatch inside `ngx_http_rewrite_module`. When a `rewrite` directive uses an unnamed PCRE capture (`$1`, `$2`, …) with a replacement containing a literal `?`, and is followed in the same block by another `rewrite`, `if`, or `set` directive, nginx sizes the destination buffer with one escaping method but writes with a different one. The resulting heap overflow is reachable without authentication and without any non-default modules — the rewrite module is built in by default.

## 4. Impact

- **Confirmed (all hosts in range):** unauthenticated remote denial of service via a single HTTP request — worker process crashes; under load this degrades service availability for all users of the affected listener.
- **Conditional:** unauthenticated remote code execution as the worker user where ASLR is disabled or weakened (`/proc/sys/kernel/randomize_va_space != 2`, statically-linked builds, or hosts that leak suitable pointers via other side channels). Public PoC exists.
- **Blast radius:** every TLS-terminating, reverse-proxy, or API-gateway listener served by this nginx instance.

## 5. Remediation

1. **Patch.** Upgrade nginx OSS to **1.30.1** (stable) or **1.31.0** (mainline). nginx Plus: apply **R36 P4** or **R32 P6**.
2. **Config-level interim mitigation** (until patched): convert any `rewrite` rules that use unnamed PCRE captures plus a `?` in the replacement to named captures, e.g.
   ```nginx
   # vulnerable
   rewrite ^/old/(.*)$ /new/$1?archived=1 last;
   # safe
   rewrite ^/old/(?<path>.*)$ /new/$path?archived=1 last;
   ```
3. **Defence in depth:** confirm `cat /proc/sys/kernel/randomize_va_space` returns `2` on every nginx host so the bug remains a DoS rather than an RCE.

## 6. Reproduction (active validation — only on receipt of written authorization)

Provide a non-production hostname and a written go-ahead; I will:

1. Send the published trigger pattern (single HTTP request) against the staging host.
2. Capture the resulting worker crash from `error.log` (`worker process exited on signal 11`) and provide the timestamps.
3. Stop. No RCE attempt against your infrastructure unless explicitly requested.

## 7. References

- NVD: <https://nvd.nist.gov/vuln/detail/<specific-cve-id>>
- nginx security advisory (vendor)
- Public disclosure: DepthFirstDisclosures — Nginx-Rift
- AlmaLinux advisory: <https://almalinux.org/blog/2026-05-13-nginx-rift-<specific-cve-id>/>

## 8. Disclosure timeline (this report)

| Date | Event |
|---|---|
| <YYYY-MM-DD> | Passive fingerprint shows `<host>` running nginx `<version>` |
| <YYYY-MM-DD> | Report submitted via _<platform>_ |
| | (awaiting program response) |

---

_Submitted in good faith under the program's safe-harbour terms. No active exploitation was performed against production. Happy to coordinate validation on a staging asset on request._
