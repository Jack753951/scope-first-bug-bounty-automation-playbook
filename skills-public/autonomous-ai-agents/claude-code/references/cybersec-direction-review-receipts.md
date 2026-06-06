> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec Direction Review Receipts

Use when the user asks to call Claude Code as a direction reviewer, strategy reviewer, capability-vision reviewer, or strong-agent reviewer for a safety-sensitive cybersec repo.

## Required pattern

1. Prepare a compact read-only review packet under `handoff/current/`.
2. Include explicit boundaries:
   - no target contact;
   - no scan/fuzz/exploit/callback/OAST;
   - no credential handling;
   - no account mutation;
   - no report submission;
   - no file edits by the reviewer.
3. Include a required-context-read list, usually:
   - `.hermes.md`
   - `PROJECT_CHARTER.md`
   - `docs/ENGINEERING_INDEX.md`
   - `docs/policy/README.md`
   - current safety / memory / repo-hygiene policies
   - `handoff/INDEX.md`
   - `handoff/current_navigation.md`
   - `handoff/active_strategy_queue.md`
   - `handoff/current_artifact_index.md`
   - active engineering direction
4. Ask Claude Code to return:
   - worker identity;
   - context read attestation;
   - verdict;
   - recommended timeline;
   - essential capabilities;
   - non-goals;
   - risks / hard stops;
   - questions for the operator;
   - explicit disagreements.
5. Run Claude Code in print mode with read-only tools and JSON output so there is a durable receipt:

```bash
claude -p "$(cat handoff/current/direction_review_packet_YYYYMMDD.md)" \
  --allowedTools Read \
  --max-turns 12 \
  --output-format json > handoff/current/claude_code_direction_review_YYYYMMDD.json
```

6. Extract the `result` field into a markdown receipt:

```bash
python - <<'PY'
import json
from pathlib import Path
src = Path('handoff/current/claude_code_direction_review_YYYYMMDD.json')
dst = Path('handoff/current/claude_code_direction_review_YYYYMMDD.md')
data = json.loads(src.read_text(encoding='utf-8'))
dst.write_text(data.get('result', ''), encoding='utf-8')
print(data.get('session_id'), data.get('subtype'), data.get('num_turns'), data.get('total_cost_usd'))
PY
```

7. Hermes must synthesize the review separately and update the repo handoff / accepted-change log.

## Pitfalls

- Do not tell the user that a strong-agent review happened unless there is a saved artifact path or session receipt.
- Do not treat a generic Hermes subagent as equivalent to Claude Code when the user explicitly asked for Claude Code usage.
- Context attestation matters: if the reviewer did not read or receive the required context, label the review provisional instead of pretending it is complete.
- Direction review should usually edit/synthesize into existing active direction files, not create yet another long-lived direction variant.
