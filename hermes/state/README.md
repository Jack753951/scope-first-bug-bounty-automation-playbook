> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# hermes/state/

Hermes' runtime state. Hermes owns these files. Do not hand-edit unless recovering.

## Files

- `hermes_state.json` — last-run timestamps and statuses for each loop.
- `hermes_log.jsonl` — append-only event log. One JSON object per line: `{ts, event, loop, slug?, summary, data}`.
- `budget.json` — daily/monthly token and cost caps + current usage counters.

## Initial bootstrap

On first run, Hermes creates:

```json
// hermes_state.json
{
  "schema_version": "1.0",
  "loops": {
    "minute_alerts": {"last_run_at": null, "last_status": null},
    "hourly_diff":   {"last_run_at": null, "last_status": null},
    "daily_sweep":   {"last_run_at": null, "last_status": null}
  },
  "started_at": "<iso ts>"
}
```

```json
// budget.json
{
  "schema_version": "1.0",
  "billing_model": "subscription",
  "daily_token_soft_cap": 500000,
  "claude_call_cap_per_day": 12,
  "codex_call_cap_per_day": 12,
  "current_day": "<YYYY-MM-DD>",
  "tokens_used_today": 0,
  "claude_calls_today": 0,
  "codex_calls_today": 0,
  "notes": "Subscription model (Claude Max + OpenAI Plus / Pro or equivalent). USD-per-day is not the bill — caps here are behavior gates against runaway loops, not billing controls. token_soft_cap is advisory; trip a stop condition if exceeded so the operator can inspect."
}
```

`hermes_log.jsonl` starts empty.

## Retention

- `hermes_log.jsonl` — keep forever. Rotate to `hermes_log_<year>.jsonl` at year boundary.
- `hermes_state.json` — current state only, overwritten on each loop.
- `budget.json` — counters reset daily by daily_sweep step 1 if `current_day` is stale.

## Gitignore considerations

These files contain operational state, not secrets. Keep tracked in git so the operator can inspect history. If they ever start containing tokens / credentials, immediately gitignore and rewrite.
