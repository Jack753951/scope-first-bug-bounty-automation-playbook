> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Next.js <specific-cve-id> bounded detector run-card — reference/fallback, not active latest-vuln lane

Artifact: `scripts/nextjs_cve_2025_29927_detector.py`

Purpose: offline-safe, bounded candidate detector for <specific-cve-id> middleware-bypass indicators. It compares a baseline `GET`/`HEAD` response with a probe response that adds:

```text
x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware
```

Safety defaults:

- Plan-only by default; no network requests unless all of `--execute --allow-network --authorized-target` are present.
- Only `GET` and `HEAD` are accepted.
- Timeout is capped at 5 seconds.
- Relative operator-supplied paths only; absolute URLs in path input are ignored.
- Response bodies are not serialized or written; only status, selected headers, and body length are retained.
- Output uses candidate-only language and does not claim confirmation.

Plan-only example:

```bash
python scripts/nextjs_cve_2025_29927_detector.py \
  --base-url http://127.0.0.1:3000 \
  --path /admin \
  --path /dashboard \
  --output /tmp/nextjs_29927_plan.json
```

Network execution is intentionally gated and must only be used against authorized local/disposable lab targets:

```bash
python scripts/nextjs_cve_2025_29927_detector.py \
  --base-url http://127.0.0.1:3000 \
  --path /admin \
  --execute --allow-network --authorized-target \
  --output /tmp/nextjs_29927_candidates.json
```

Validation:

```bash
python -m pytest scripts/test_nextjs_cve_2025_29927_detector.py
```
