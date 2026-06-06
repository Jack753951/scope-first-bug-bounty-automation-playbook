> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# 2026-05-21 single-vulnerability split run

Session learning from converting an earlier three-class OWASP pilot into three class-level, one-vulnerability modules.

## Operator correction

The durable module shape is:

```text
one vulnerability behavior / one OWASP class capability / one runnable module
```

A multi-class runner can be useful as a workflow pilot or stress test, but should not become the final module shape. Shared helper code is fine; runnable entrypoints, bundle docs, tracker state, importer/bridge, and possible-vulnerability summaries should remain per vulnerability behavior.

## Completed split pattern

The three-class pilot was split into:

- `lab_access_control_unauth_route_metadata`
  - candidate: `/rest/admin/application-configuration` returned 200 JSON unauthenticated
  - controls: `/api/Users` 401 auth gate; `/administration` SPA fallback control
- `lab_crypto_transport_metadata`
  - metadata-only: `/`, `/rest/user/whoami`, `/api/SecurityQuestions`
  - no candidate from bounded run
- `lab_exceptional_condition_metadata`
  - candidate: `/rest/does-not-exist` returned 500 with error title
  - controls: benign malformed search queries returned stable 200

Each module emitted:

- `observations.jsonl`
- `possible_vulnerabilities.md`
- `health.txt`
- `summary.txt`
- `artifact_manifest.txt`

## Useful implementation pattern

A shared helper can render approval-gated bash runners while module files contain only the fixed path/spec definitions. Tests should assert:

- plan-only behavior before approval;
- public-target rejection;
- no broad/high-risk tools (`sqlmap`, `hydra`, scanner/fuzzer defaults);
- no confirmed/reportable/submission language;
- generated script has pre/post health, request caps, manifest, JSONL, and `possible_vulnerabilities.md`;
- per-module class isolation (do not mix access-control, crypto, and exception probes into one module).

## Windows/MSYS/Kali execution pitfall

When generating scripts on Git Bash/MSYS for remote Linux paths such as `/home/kali/...`, set:

```bash
MSYS2_ARG_CONV_EXCL='*'
```

Otherwise MSYS may rewrite `/home/kali/...` into a Windows path like `C:/Program Files/Git/home/kali/...`, causing artifacts to land in the wrong place or the runner to fail remotely.

## Generated bash heredoc pitfall

When Python renders bash containing a nested Python heredoc, escape handling can corrupt newline literals. Use a raw f-string (or equivalent explicit escaping) for generated bash templates, then verify the generated script directly with `bash -n` and at least one lab execution/dry-run path. Do not rely only on generator unit tests.

## Reporting language

Every module should emit a human-readable possible-vulnerability summary with:

- `possible_manual_review_candidates`
- `non_findings_or_controls`
- `missing_evidence_to_confirm`

Keep language candidate-only. Lab output should not auto-promote to confirmed, verified, reportable, accepted, or ready-for-submission.

## No new OSS download by default

OSS/tooling recon is mandatory before writing a new adapter, but recon does not imply downloading tools. In this session, mature tools were checked conceptually (ZAP/Autorize/AuthMatrix, testssl.sh/SSLyze/Observatory, ZAP/ffuf/nuclei), but the bounded local-lab need justified `write-custom` without downloading new scripts.
