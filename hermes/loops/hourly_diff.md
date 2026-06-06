> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Hourly Diff

Runs every hour (or as cron permits). Differential recon — only checks what changed since last run, bounded by lane scope and the per-program technique profile.

## Scope

Only operates on lanes where `lane_state.json.autonomy_level >= A1` and `lane_state.json.operator_decision != KILL`. Suspended programs are skipped at recon level except for status-flip detection in `daily_sweep`.

Every target-touching action must pass the intersection of:

1. `config/scope.txt`
2. `programs/<slug>/scope.json`
3. `SAFETY.md`
4. the lane's current operator decision / proof boundary

## Technique tiers

### A1_PASSIVE_PUBLIC

Public/feed-only collection: CT logs, CVE/KEV/GHSA feeds, public program policy, disclosed report mining, public docs, source/static review. No target probing.

### A2_LOW_SPEED_ACTIVE_RECON

Default tactical base after exact scope is approved and `scope.json.techniques.allowed` permits the technique. Examples:

- `http_probe`
- `tls_fingerprint`
- `fixed_path_metadata`
- `nuclei_non_intrusive`
- low-count public-doc endpoint existence checks

Default live caps:

```text
max_concurrency: 1-2
max_requests_per_second: 0.2-1.0
request_delay_ms: 1000-5000
max_requests_per_host_per_run: 50
max_runtime_per_host: 5-10 min
retries: 0-1
randomization/evasion: none
```

### A3_BOUNDED_PROOF_ACTIONS

A3 is the single standing lane-approved proof tier. The former A4 controlled class is intentionally folded into A3 so realistic exploit-chain, SSRF/OAST, and API-credential proof work does not require a second classification gate after the lane has approved the capability.

Routine A3 examples after lane/program approval:

- `owned_object_authz_check`
- `owned_object_fuzz`
- `api_token_min_scope_owned_account`
- `small_wordlist_discovery` against allowlisted owned/sandbox routes
- `ssrf_marker_callback` / `oast_marker_callback`
- `exploit_chain_marker_only`
- `exploit_chain_bounded_owned_impact`

A3 credential rules:

- credential is created only in an operator-owned test account/workspace;
- secret value is never written to prompts, memory, repo files, screenshots, shell history, or reports;
- minimum permission/read-only credential preferred;
- credential is used only through a local redacted runner/browser path;
- evidence stores credential label/id suffix/hash only;
- cleanup/revoke is required or explicitly parked for operator decision.

A3 controlled callback rules:

- marker-only callback to an operator-controlled receiver;
- no cloud metadata credential access;
- no internal port scan or private IP enumeration;
- no pivot or customer/non-owned data access;
- request count is capped and evidence is redacted.

A3 bounded exploit-chain rules:

- chain may prove marker/capability proof or recoverable impact on operator-owned objects/state;
- capability record must set `allowed_impact` to `owned_data_only` or `owned_state_change_recoverable`;
- steps and requests are capped;
- cleanup is required;
- stop-before excludes customer/non-owned data, secrets, credential extraction, uncontrolled internal enumeration, persistence, destructive impact outside recoverable owned test state, and final submission.

Still blocked without a separate explicit approval:

- customer/non-owned data access;
- secret/token/cookie/credential extraction;
- uncontrolled internal enumeration;
- cloud metadata credential access;
- persistence, malware, evasion, stealth;
- destructive impact outside recoverable owned test state;
- final report submission.

## Order of steps

1. **Stop-condition gate**
   - Check `stop_conditions.md`. If tripped, exit silently; daily sweep handles inbox surfacing.

2. **Subdomain diff**
   - For each active exact-scope/wildcard lane where `subdomain_enumeration` is allowed:
     - run subfinder/CT-derived expansion within `scope.json.rate_limits`;
     - diff against `programs/<slug>/notes/.subdomains.txt`;
     - write net-new subdomains to `programs/<slug>/notes/<date>T<hour>_new_subdomains.md` and update cache.
   - If `subdomain_enumeration` is not allowed, use apex/exact hosts only.

3. **A2 HTTP/fixed-path probe diff**
   - For newly allowed hosts/endpoints, run only techniques present in `scope.json.techniques.allowed`.
   - Default to `http_probe`, `tls_fingerprint`, and `fixed_path_metadata` when allowed.
   - Diff status/title/headers/tech stack vs last cache.
   - Write changes to `programs/<slug>/notes/<date>T<hour>_http_diff.md`.

4. **A2 non-intrusive nuclei diff**
   - Run only if `nuclei_non_intrusive` is allowed.
   - Keep `dos,intrusive,fuzz` excluded for live targets.
   - Hits are triage only and must not be promoted to findings without proof-boundary review.

5. **A3 capability queueing or execution**
   - Hourly diff may execute A3 only when the lane has a matching standing capability, exact technique allowlist, caps, stop-before list, and cleanup/redaction requirements.
   - If any A3 control is missing, write an operator-inbox/run-card flag with the exact technique, missing capability/cap/cleanup item, and recommended EXECUTE/PARK decision.
   - Former A4 actions are no longer a separate tier; they are controlled A3 capabilities.

6. **Update state**
   - Append per-lane line to `hermes/state/hermes_log.jsonl`.
   - Update `hermes/state/hermes_state.json.last_hourly_diff_at`.

## Bounds

- Per-lane rate caps come from `scope.json.rate_limits`.
- Default live profile is `RECON_PROFILE=live-low-speed` in `config/recon.conf`.
- `--full` is refused under `live-low-speed` unless explicitly enabled and allowed by program scope.
- Per-lane time budget: 10 minutes default.
- Per-hour total Hermes time budget: 30 minutes.

## Failure modes

| Failure | Recovery |
|---|---|
| Tool not installed | Halt the affected technique; daily_sweep flags in digest. |
| Target rate-limits / 429s | Backoff per scope cap; if persistent, skip lane for this hour. |
| Net-new subdomain count > 50 | Flag possible wildcard DNS; do not auto-probe the batch. |
| Technique allowed in docs but denied by validator | Treat validator denial as authoritative; halt affected step and inbox. |
| Redaction or cleanup check fails | Halt proof promotion and write inbox. |

## Boundary

Hourly diff is a notice-board feeder, low-speed scoped recon loop, and A3 controlled proof coordinator. It can make A2 active recon routine and can execute or queue A3 capabilities, including former A4 exploit-chain/SSRF/OAST actions, only when exact scope, technique allowlist, standing capability, caps, stop-before, cleanup, and redaction controls match.
