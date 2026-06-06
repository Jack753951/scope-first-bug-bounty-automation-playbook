> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Wave 2 Benign Parameter Probe Run Card

Date: 2026-05-21
Status: draft / not approved for execution
Related direction: `handoff/phase4b_wave2_benign_probe_direction_20260521.md`

## Module class

```text
level2.open_redirect_candidate
level3.xss_reflection_candidate
```

## Purpose

Prepare a tightly bounded local-lab check for benign parameter behavior after Wave 1A metadata checks. This run card is intentionally not an execution approval.

## Target boundary

Allowed target class:

```text
local intentionally vulnerable lab only
```

Current lab target under prior Phase 4B work:

```text
http://<lab-ip>:3000/
```

Blocked targets:

```text
public targets
real bug-bounty targets
client targets
non-private IP/domain targets
credentialed/session flows
```

## Preconditions before execution

Execution must not happen until all are true:

1. A bounded adapter exists and passes tests.
2. Adapter default mode is `plan_only`.
3. Writing executable scripts requires `--lab-approved`.
4. The adapter rejects public/non-private targets.
5. The adapter uses a fixed URL list and fixed payload/canary list.
6. Pre-health and post-health are included.
7. JSONL output vocabulary is candidate-only and non-promotional.
8. Operator explicitly approves the Wave 2 local-lab run.

## Allowed probes for first execution

Open redirect candidate probe:

- one inert `.invalid` URL marker;
- one relative safe marker;
- inspect status and `Location:` header only;
- do not follow redirect chains for exploitation.

XSS reflection candidate probe:

- one inert text canary;
- record whether the canary appears in a short redacted snippet;
- no executable JavaScript payload;
- no context-specific exploit payloads;
- no dalfox/kxss/gau in first run.

## Limits

```text
max_requests: 20
rate_limit: <= 2 req/sec
timeout: <= 5 seconds/request
url_count: <= 5
payload_count: tiny fixed set only
```

## Forbidden actions

- `gau` / crawler URL expansion.
- `dalfox` deep scan.
- `kxss` broad reflection sweep.
- SQLi probes or `sqlmap`.
- LFI/file read.
- SSRF/OAST/callback/blind probes.
- brute force or credential guessing.
- recursive download or loot collection.
- confirmed/exploitable/reportable vocabulary.
- report drafting/submission.

## Required outputs

```text
pre_health.txt
post_health.txt
observations.jsonl
artifact_manifest.txt
```

`observations.jsonl` must remain `scanner_output_only=true`, `manual_verification_required=true`, and `promotes_finding=false`.

## Stop conditions

Stop immediately if:

- pre-health fails;
- post-health differs materially from pre-health;
- target becomes slow/unavailable;
- output contains tokens/cookies/secrets/private data;
- the adapter attempts to use unapproved tools or URLs;
- any observation claims confirmation instead of candidate status.

## Current decision

`DRAFT_ONLY_NOT_EXECUTION_APPROVED`
