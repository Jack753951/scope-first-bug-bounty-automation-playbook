> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B Wave 2 Direction — Benign Parameter Probe Preparation

Date: 2026-05-21
Status: direction / run-card preparation only
Repo truth: `handoff/active_strategy_queue.md`, `handoff/phase4b_owasp_script_collection_and_target_plan_20260521.md`, `handoff/phase4b_wave1a_result_20260521.md`, `scripts/open_redirect.sh`, `scripts/xss_finder.sh`

## Goal

Continue Phase 4B after Wave 1A by preparing the next controlled local-lab wave without executing it yet.

Wave 2 should test only benign parameter-handling candidates in the local intentionally vulnerable lab:

- open redirect candidate behavior;
- XSS reflection candidate behavior;
- fixed allowlisted URLs only;
- no crawlers, broad URL collection, blind/OOB payloads, credentialed flows, destructive payloads, or confirmed-vulnerability promotion.

## Current context

Wave 1A already produced a reusable low-risk metadata path:

1. bounded local-lab execution;
2. output-side review;
3. Level 1 metadata manifests;
4. reusable Wave 1A adapter;
5. offline importer;
6. candidate-review bridge;
7. offline review-chain builder.

Wave 2 is a higher-risk class because it mutates query parameters. It must not reuse the old shell scripts as-is.

## Existing scripts inspected

### `scripts/open_redirect.sh`

Useful ideas:

- redirect-parameter detection;
- canary marker domain;
- `Location:` header inspection;
- no redirect-follow requirement for the main evidence.

Blockers before lab-module use:

- accepts arbitrary target/list input;
- can invoke `gau` URL collection;
- has many bypass payloads, including patterns not needed for first lab pass;
- writes free-form report language including high-confidence wording;
- does not enforce local/private lab URL allowlist;
- does not emit normalized JSONL observations.

### `scripts/xss_finder.sh`

Useful ideas:

- parameterized URL filtering;
- reflection-first posture;
- warning that reflection is not exploitable XSS.

Blockers before lab-module use:

- can invoke `gau`, `kxss`, and `dalfox`;
- dalfox mode may generate/deepen payloads;
- accepts arbitrary target/list input;
- no fixed URL allowlist;
- no local/private lab enforcement;
- report wording includes finding-oriented sections;
- no normalized candidate-only JSONL contract.

## Wave 2 safe implementation direction

Do not execute `open_redirect.sh` or `xss_finder.sh` directly for Wave 2.

First create a new bounded adapter, for example:

```text
scripts/lab_modules/wave2_benign_params.py
scripts/test_wave2_benign_params_lab_module.py
handoff/phase4b_run_cards/wave2_benign_params_run_card.md
```

The adapter should be plan-only by default and require `--lab-approved` before writing an executable script.

## Required gates for Wave 2 adapter

- Reject public/non-private targets.
- Use fixed local-lab URL allowlist, not crawled URLs.
- Disable `gau`, `dalfox`, `kxss`, `sqlmap`, browser automation, and external URL collectors.
- Use a tiny fixed candidate URL list, initially no more than 5 URLs.
- Use a tiny fixed payload/canary set:
  - open redirect: one inert `.invalid` canary URL and one relative safe marker;
  - XSS reflection: one inert text canary, not executable JavaScript.
- Request cap: 20 total requests maximum for the first adapter.
- Timeout: 5 seconds maximum per request.
- Rate limit: <= 2 req/sec.
- Pre/post health required.
- Emit JSONL observations only.
- Use vocabulary such as `redirect_candidate`, `reflection_candidate`, `no_candidate`, `manual_review_required`.
- Forbid vocabulary such as `confirmed`, `verified`, `exploitable`, `reportable`, `ready_for_submission`.
- Do not follow redirect chains beyond header/status observation.
- Do not capture raw bodies except short redacted snippets for reflection context, capped and token-scanned.
- No credentialed/session tests.
- No callbacks/OAST/blind payloads.
- No report drafting or submission.

## Initial fixed URL candidates

Use only local Juice Shop routes already observed in prior lab work. Proposed first list:

```text
/
/search?q=wave2_canary
/rest/products/search?q=wave2_canary
/redirect?to=wave2_canary
/login?redirect=wave2_canary
```

These are candidates for adapter planning only. The executable run must still be reviewed before use because some paths may be SPA routes or non-existent placeholders.

## Output contract sketch

Each JSONL observation should include at minimum:

```json
{
  "schema_version": "wave2_benign_params_observation/0.1-trial",
  "tool": "wave2_benign_params",
  "target_url": "http://<lab-ip>:3000/",
  "module_id": "level2.open_redirect_candidate | level3.xss_reflection_candidate",
  "path": "/search",
  "param": "q",
  "probe_kind": "redirect_header | reflection_text",
  "state": "no_candidate | redirect_candidate | reflection_candidate | needs_manual_review",
  "evidence_summary": "metadata-only summary",
  "manual_verification_required": true,
  "scanner_output_only": true,
  "promotes_finding": false
}
```

## Review tier

- Direction/run-card preparation: T1/T2 documentation, no target interaction.
- Adapter implementation: T3/T4 boundary because it writes target-touching lab scripts, even if plan-only by default.
- Actual Wave 2 lab execution: T4, explicit operator approval required before running.

## Decision

`PREPARE_WAVE2_BENIGN_PARAMS_ADAPTER_ONLY`

Hermes may prepare the run card and adapter plan. Hermes must not execute Wave 2 probes yet.
