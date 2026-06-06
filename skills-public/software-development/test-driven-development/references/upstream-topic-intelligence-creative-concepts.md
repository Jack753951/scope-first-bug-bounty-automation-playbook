> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Upstream topic-intelligence -> creative concept TDD pattern

Use this when an upstream YouTube/topic-radar repo is producing candidate packets that later feed a media generator, but the current slice should stay planning-only.

## Durable lesson

Do not treat every upstream metadata or planning step like a production upload. Use stage-appropriate gates:

1. Fast lane: public metadata collection, scoring, candidate JSON, list/schema validation.
2. Medium lane: candidate -> originalized creative concept or script-outline packets.
3. Strict lane: only real generator/render/upload/scheduler/OAuth/channel-config workflows.

This preserves safety without letting safety paperwork crowd out creative progress.

## RED tests to add first

For candidate -> concept packets:

- Candidate -> concept packet includes a clear planning-only stage, e.g. `CREATIVE_CONCEPT_ONLY_NO_SCRIPT_NO_RENDER_NO_UPLOAD`.
- Concept packet has originalized creative fields: premise, hooks, character setup, visual beats, SFX ideas, needed synthetic objects, and next gate.
- Source title/body is not copied into premise/hooks or the concept packet as generated copy.
- Reject candidates do not become concept packets.
- CLI writes both JSON and Markdown artifacts without invoking generation/render/upload code.
- Substring classifiers use token-level matching for category/proof inference; add regressions for false positives like `release` being treated as `lease`, or `pay` in a legal/mechanic title being treated as workplace/payroll.

For YouTube watchlist market-pattern -> candidate packets:

- Watchlist-only YouTube metadata can be transformed into an original candidate hypothesis, but the generated premise/hooks/proof object must not copy the source title phrase.
- The packet uses a distinct planning-only stage such as `MARKET_PATTERN_CANDIDATE_ONLY_NO_SCRIPT_NO_RENDER_NO_UPLOAD` and writes schema-valid candidate JSON plus a Markdown digest only.
- The transform should add a concrete synthetic proof object (lawyer email, signed letter, bank statement, family text-message card, receipt chain, etc.) instead of preserving a vague shock title.
- Sensitive or ambiguous title patterns are skipped or kept as watchlist-only: minors/high school, newborns, ambiguous stay-over/intentions framing, celebrity dating/exposure, and other topics that would need a separate policy review before creative expansion.
- CLI tests should prove the command accepts topic JSON and writes candidate packets without calling script/render/upload code.

## Implementation shape

- Keep generated concept JSON under a gitignored generated-data directory such as `data/concepts/`; commit only `.gitkeep` and human-readable handoff if appropriate.
- Concept packets should be strong enough for a human or later agent to choose 1-2 items for script-outline review, but not be scripts.
- If a concept needs a specific synthetic proof object, say so explicitly; do not silently downgrade to generic B-roll or vague material.

## Verification

Run focused RED/GREEN tests, then full project validation, for example:

```bash
python -m compileall src tests scripts
PYTHONPATH=src python -m trend_radar.cli validate-list data/candidates/<file>.json
PYTHONPATH=src python -m pytest -q
```

Update handoff with the current stage and the next medium gate rather than repeating long high-risk upload prohibitions for every upstream step.
