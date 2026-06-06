> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A Bounded Content-Discovery Rehearsal

Use this reference after an isolated attacker/victim local lab is ready and the operator wants the first tightly bounded aggressive-lab execution slice.

## Pattern

Start with a script-specific run card before any execution. Keep the first rehearsal deliberately small:

- local lab / intentionally vulnerable app only;
- exact attacker VM, victim VM, target URL, and host-only network proof;
- fixed short path list, not a wordlist;
- `HEAD` first when metadata is enough;
- explicit request cap, timeout, delay, and overall command timeout;
- pre-health and post-health checks against `/`;
- candidate-only output with no response bodies by default;
- kill conditions for target health loss, repeated timeouts, off-target redirects, or accidental sensitive output.

A good first cap is about 30 paths plus health checks. This exercises request limits, timeouts, health checks, artifact handling, and output review without immediately crossing into credential attacks, exploit PoCs, callbacks, destructive actions, or recursive crawling.

## Required run-card sections

1. Scope and authorization.
2. Objective.
3. Allowed action class.
4. Explicitly forbidden actions.
5. Request cap / rate / timeout.
6. Fixed path list.
7. Evidence/output artifacts.
8. Kill conditions.
9. Review decision requested.

The safety review should answer whether the run stays in local-lab scope, keeps bounded caps, avoids payloads/destructive behavior, preserves candidate-only output, and is allowed exactly as specified.

## Execution artifact shape

Save a per-run directory under `handoff/`, for example:

```text
handoff/phase4a_1_bounded_content_discovery_run_<date>/
  run_card.md
  pre_health.txt
  observations.jsonl
  execution_exit.txt
  post_health.txt
  summary.md
```

Observation records should be metadata-only, such as:

```json
{
  "schema": "phase4a_content_discovery_observation/1.0",
  "target": "http://<lab-ip>:3000",
  "path": "/robots.txt",
  "method": "HEAD",
  "status_code": 200,
  "content_type": "text/plain",
  "content_length": 28,
  "location": null,
  "candidate_only": true,
  "finding_status": "observation_not_finding",
  "error": null
}
```

## Output-side review gate

After execution, run an output-side review before interpreting results. Require the review to state:

- verdict: candidate-only / revise / block;
- pre-health, execution, and post-health status;
- candidate observations worth manual review;
- false-positive traps;
- what must not be claimed as confirmed;
- allowed next action.

Common false-positive trap for SPAs such as Juice Shop: many arbitrary paths can return `200 text/html` with the same content length as the SPA fallback/index page. Do not claim exposed files/endpoints from status code alone. In particular, `/.git/HEAD`, `/package.json`, `/server-status`, `/swagger.json`, `/admin/`, and `/debug` returning fallback HTML are not evidence of those resources existing.

`500` responses to `HEAD` are candidate anomalies only. They are not confirmed vulnerabilities, crashes, or DoS unless follow-up checks prove impact and post-health shows degradation.

## Manual follow-up slice

A safe next slice is bounded content-class verification for a tiny allowlist, for example:

- `GET /robots.txt`
- `GET /.well-known/security.txt`
- `GET /ftp/`
- `GET /rest/products/search`
- `GET /api-docs/`

Keep it local-lab only, low request count, no recursive download, no exploit payloads, no credential testing, no callbacks/listeners, and store only short redacted snippets or metadata unless separately approved.

## Windows/Kali SSH quoting pitfall

When invoking complex remote Python through the project PowerShell SSH wrapper, here-docs and nested quote-heavy `python -c` payloads can lose quoting before they reach the remote shell. If a future run needs a complex remote script, prefer one of these durable patterns:

1. Use direct `ssh.exe` with the project identity, known_hosts, and empty SSH config, and pass a base64-encoded Python payload:

```bash
ssh.exe -F "$SSH_CONFIG" -i "$KEY" -p 22 \
  -o "UserKnownHostsFile=$KNOWN" \
  -o StrictHostKeyChecking=accept-new \
  kali@<lab-ip> \
  "python3 -c \"import base64; exec(base64.b64decode('$REMOTE_B64'))\""
```

2. Or write a short remote script file through a controlled transfer/setup step, then execute it by path.

Do not encode this as "the wrapper is broken". The reusable lesson is: for nested multi-line code over PowerShell -> SSH -> bash, avoid fragile nested quoting; use base64 payloads or a script file, and keep the artifacts local and git-ignored if they are session helpers.
