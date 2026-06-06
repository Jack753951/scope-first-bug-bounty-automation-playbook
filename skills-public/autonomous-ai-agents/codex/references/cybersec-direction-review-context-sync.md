> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Codex Direction Review With Synchronized Context

Use when Codex is asked to act as a direction reviewer, secondary reviewer, or dissenting strategy reviewer for a safety-sensitive repo.

## Required pattern

1. Prepare the same compact review packet used for other strong reviewers.
2. Run Codex in read-only mode first and save both final message and event log:

```bash
codex exec --sandbox read-only --cd . \
  --output-last-message handoff/current/codex_direction_review_YYYYMMDD.md \
  - < handoff/current/direction_review_packet_YYYYMMDD.md \
  > handoff/current/codex_direction_review_YYYYMMDD.events.txt 2>&1
```

3. Require Codex to include:
   - worker identity;
   - context read attestation;
   - verdict;
   - risks and hard stops;
   - disagreements;
   - operator questions.
4. If Codex reports it could not read required files, do not count the review as complete.
5. Retry with an embedded synchronized context packet created by Hermes from the required files. The lesson is the retry pattern, not the transient sandbox failure:

```bash
python - <<'PY'
from pathlib import Path
required = [
    '.hermes.md',
    'PROJECT_CHARTER.md',
    'docs/ENGINEERING_INDEX.md',
    'docs/policy/README.md',
    'docs/policy/repo_hygiene_policy.md',
    'docs/policy/memory_and_strategy_routing.md',
    'handoff/INDEX.md',
    'handoff/current_navigation.md',
    'handoff/active_strategy_queue.md',
    'handoff/current_artifact_index.md',
]
base = Path('handoff/current/direction_review_packet_YYYYMMDD.md').read_text(encoding='utf-8')
parts = [base, '\n# Embedded Context Bundle\nReview based on this synchronized context if direct local reads are unavailable.\n']
for f in required:
    p = Path(f)
    parts.append(f'\n## FILE: {f}\n')
    parts.append(p.read_text(encoding='utf-8', errors='replace')[:30000] if p.exists() else '[MISSING]\n')
Path('handoff/current/direction_review_codex_embedded_packet_YYYYMMDD.md').write_text('\n'.join(parts), encoding='utf-8')
PY
```

Then rerun Codex with the embedded packet as stdin.

## Pitfalls

- Never claim Codex completed memory/context synchronization when its attestation says it could not read the files.
- A failed direct-read attempt can still be useful as evidence of reviewer integrity; preserve the event log, then retry with an embedded packet.
- Keep the retry read-only. Direction review is not permission to modify files.
- Hermes must synthesize Codex and Claude/other reviews into an active handoff or existing direction file; do not leave raw reviews as the only outcome.
