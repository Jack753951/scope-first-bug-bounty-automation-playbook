> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Service baseline scanner runtime lessons

Use this reference when building bundle-first baseline scanners for common web infrastructure surfaces such as Apache, Tomcat, OpenSSL/TLS, HAProxy, Envoy, and Traefik.

## Class-level lesson

Service baseline scanners are useful as low-risk candidate generators, but they are especially prone to false positives on modern single-page apps, reverse proxies, and catch-all routers. A service-specific path returning HTTP 200 is not enough evidence that the service surface exists.

## Recommended pattern

1. Keep the adapter plan-only by default and require explicit lab/authorization approval before rendering a runnable script.
2. Quote every generated path argument in bash runners, including metacharacter paths such as `'/;csv'`.
3. Test the rendered runner itself with `bash -n` and at least one local-lab execution or dry-run path; generator tests alone miss shell quoting and heredoc issues.
4. Record root response fingerprint before probing service paths:
   - fetch `/` or the normalized target root;
   - store a body hash such as `root_body.sha256`;
   - hash each service probe body;
   - if a service path returns 200/3xx but the body hash equals root and there is no service-specific header/location, classify it as `*_generic_root_fallback_control`, not a candidate.
5. For TLS probes, do not treat generic `openssl s_client` output as a candidate if it contains `no peer certificate available` or `Cipher is (NONE)`; classify as TLS unavailable/plaintext/control unless real certificate/session metadata is present.
6. Preserve both candidates and controls in `possible_vulnerabilities.md` so future reviewers can see why noisy 200s were suppressed.

## Candidate language

Acceptable service-baseline candidate wording:

- `candidate-only / needs_manual_review`
- `service_baseline_candidate`
- `access_control_observed`
- `generic_root_fallback_control`
- `tls_metadata_control`

Avoid:

- `confirmed`
- `verified vulnerability`
- `reportable`
- service identity claims based only on a path and status code.

## Minimal artifacts

A practical service-baseline run should emit:

```text
health.txt
http_probe_results.tsv
observations.jsonl
possible_vulnerabilities.md
root_body.sha256
summary.txt
artifact_manifest.txt
```

Tool-specific optional artifacts can include `openssl_s_client.txt`, `tool_raw.xml`, `tool_stdout.txt`, and `tool_stderr.txt`.

## Why this matters

In a local lab run against an SPA target, many Apache/Tomcat/HAProxy/Traefik default paths returned 200, but all matched the root body hash and were correctly downgraded to generic root fallback controls. Only the metrics endpoint remained a candidate requiring manual verification. This is the intended behavior: reduce scanner noise before report or module promotion.
