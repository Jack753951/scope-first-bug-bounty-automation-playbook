> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Minute Alerts

Runs every minute (or as cron permits). Lightweight feed intake. No LLM calls.

## Sources

- CT log streams (Certstream / crt.sh polling / Censys CT) — filter by in-scope apex from active lanes' scope.json.
- Disclosed-report RSS feeds — public <bug-bounty-platform> / Intigriti disclosed feeds.
- CVE feeds — NVD recent-modified API, KEV recent additions, GitHub Security Advisories.
- Vendor security advisories — for stacks Hermes knows lanes use.

## Behaviour

Each source is polled. New entries are filtered for relevance:

- CT log entry where the cert's domain matches an in-scope wildcard in any active lane.
- CVE where the affected product is in any active lane's tech stack inventory.
- Disclosed report where the reported program is on Hermes' watch list.

Relevant new entries are written to:

- CT new cert → `programs/<slug>/notes/.ct_new.jsonl` (append, deduped).
- CVE match → `intelligence/cve_briefs/.pending_<date>.jsonl` for the next daily brief.
- Disclosed report relevant → `intelligence/disclosed_relevant_<date>.jsonl` for the next weekly mining step.

## What this loop does NOT do

- No probe / no GET against discovered hosts (that's hourly_diff).
- No Claude / Codex calls.
- No inbox writes (daily_sweep aggregates).
- No state machine changes.

## Cost

Should be near-zero in tokens. Pure ETL.

## Failure modes

| Failure | Recovery |
|---|---|
| External feed 5xx | Backoff; if >1h continuous failure, log and skip until next hour. |
| Feed payload schema changed | Log raw payload, skip processing; daily digest flags for operator. |
| Disk write fails | Halt loop, daily_sweep will surface in next inbox. |

## Boundary

Pure passive intake. Cannot trigger any active behaviour. Feeds the daily / hourly loops with fresh material to consider.
