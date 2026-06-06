> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Upstream topic-intelligence demand-signal TDD pattern

Use this when an upstream topic-radar repo needs accountless search/autocomplete/trend demand signals as scoring support, while staying planning-only and not triggering script/render/upload work.

## Durable lesson

Autocomplete/search suggestions are demand indicators, not story sources. They should help identify query families and market interest, but generated packets must not treat them as proof, source narratives, captions, or script text.

## RED tests to add first

- Parser converts a known suggestion payload into a plain list of query suggestions.
- Row builder emits metadata-only rows with an explicit platform/source such as `search_suggest` / `youtube_autocomplete`.
- Suggestion rows use synthetic/reference URLs such as `search://...`, not source-story URLs.
- Topic ranking can use high-fit demand rows as candidate-support signals, but risk flags say the row is not a story source.
- CLI reads seed queries from config and supports an override flag such as `--search-queries` plus a max cap such as `--max-search-queries`.
- CLI writes source counts for demand rows (for example `source_counts.search_seed_queries`).
- Broad or near-duplicate autocomplete phrases should not crowd out concrete story candidates; add RED tests for deduplication/query-family grouping before implementing that rung.
- When live autocomplete contains weak one-token or off-target suggestions (for example generic `email cc`, `boss of boss`, media-title matches like `overtime ost`, or a bare `roommate`), add RED tests before filtering: weak suggestions should remain metadata-only `watchlist`, carry an explicit weak-relevance risk flag, and not appear as headline rollup examples.
- Add RED tests that weak autocomplete rows do not crowd out concrete Reddit/YouTube/public metadata rows under a limited `top_n`; defer weak `search_suggest` topics until after concrete metadata and usable demand rows, only filling empty slots late.
- For demand-family markdown rollups, test and show both quality counts (`usable`, `weak`) and volume counts (`suggestions`, `concrete`) so future agents can see whether a family is actionable or merely diagnostic.
- For the next quality rung, add RED tests that non-search topics can record cross-source autocomplete demand overlap without promoting suggestions into story sources:
  - overlap appears as a separate score field such as `scores.demand_overlap`;
  - matched autocomplete rows are stored under `demand_overlap.supporting_refs`, not appended to `source_refs`;
  - matched query families and meaningful terms are visible for review;
  - risk flags explicitly say overlap is supporting evidence only and not a story source;
  - Markdown digest includes a `Demand overlap:` line only when present.
- Broad or near-duplicate autocomplete phrases should not crowd out concrete story candidates; add RED tests for deduplication/query-family grouping before implementing that rung.
- Cross-source overlap rungs should be tested as support-only evidence: non-search topics may gain `scores.demand_overlap` and `demand_overlap.supporting_refs`, but autocomplete refs must not be mixed into primary `source_refs` or treated as story sources.
- Markdown digest rollups should be tested when demand families exist: include suggestion counts, concrete-story counts, a few example suggestions, and an explicit caveat that autocomplete rollups are demand indicators only.
- Alias/synonym overlap should be tested before implementation: canonicalize durable class-level equivalents such as `manager/supervisor -> boss`, `flatmate -> roommate`, `text/messages -> message`, `screenshots -> screenshot`, and `document(s) -> proof`; require at least two meaningful canonical terms before boosting so one generic alias does not over-promote a topic.
- Autocomplete relevance filtering should be tested before implementation when live suggestions are noisy. Add a RED test for a known off-target suggestion from a proof-object seed (for example a seed like `boss email proof` returning a generic `email cc` suggestion): it should remain `watchlist`, expose a low/zero `scores.demand_relevance`, carry a weak-relevance risk flag, and not be used as the family rollup headline example. Keep counting weak suggestions for diagnostics, but do not let a single attractive token (`email`, `boss`, `overtime`, `roommate`) promote an otherwise generic query to candidate status.
- User-provided Shorts/competitor URL smoke tests should be run through accountless public metadata paths only. Verify `source_counts.youtube_video_urls`, confirm oEmbed/title/channel/thumbnail-reference capture, and keep rows as market-pattern signals unless their public metadata exposes strong safe proof-object/high-conflict terms. Do not treat sensitive hooks (newborn, sexualized/ambiguous “intentions”, credible harm, minors) as production-ready candidates without a safer transformed premise and explicit review.

## Implementation shape
## Implementation shape

- Keep the collector accountless and metadata-only.
- Store rows under existing raw/discovery JSON outputs; do not create scripts, render assets, upload packets, or scheduler jobs.
- In scoring, treat demand rows as supportive ranking signals only. Do not let suggestions become source refs for copied story content.
- Add a conservative relevance score for autocomplete rows when live data quality is noisy. A useful minimum pattern is: require at least two shared seed/query-family terms, at least two meaningful proof/high-conflict terms, or one meaningful term plus a story-format support term (`story`, `storytime`, `reddit`, `shorts`, `aita`) before allowing candidate-level treatment.
- Weak autocomplete rows should be explicit and reviewable: keep them in raw/digest outputs as `watchlist`, add a score field such as `scores.demand_relevance=0`, add a risk flag like `autocomplete suggestion has weak seed/query relevance`, and exclude them from rollup examples.
- During topic selection, defer weak search rows until after concrete Reddit/YouTube metadata and usable search-demand rows so generic autocomplete suggestions do not push competitor/reference metadata out of a small topic inbox.
- Store cross-source matches under a separate support field such as `demand_overlap.supporting_refs`; keep `source_refs` reserved for the actual metadata row/topic source.
- Add clear risk flags such as: `accountless autocomplete demand signal; not a story source` and, for overlap matches, `autocomplete demand overlap is supporting evidence only and not a story source`.
- Add clear risk flags such as: `accountless autocomplete demand signal; not a story source` and, for overlap matches, `autocomplete demand overlap is supporting evidence only; not a story source`.
- Prefer conservative overlap thresholds: require multiple meaningful/proof/high-conflict canonical tokens before applying score boosts, then document when live smoke data has no qualifying overlap despite test coverage.

## Verification


Run focused RED/GREEN tests first, then full project checks, for example:

```bash
python -m compileall src tests scripts
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m trend_radar.cli discover-topics --config config/source_backlog.example.json --date <date> --raw-out data/raw/topic_discovery_<date>.json --topics-out data/topics/top_topics_<date>.json --digest-out handoff/topic_discovery_<date>.md --max-search-queries 4
PYTHONPATH=src python -m trend_radar.cli discover-topics --config config/source_backlog.example.json --date <date> --raw-out data/raw/topic_discovery_<date>_user_shorts.json --topics-out data/topics/top_topics_<date>_user_shorts.json --digest-out handoff/topic_discovery_user_shorts_<date>.md --top 20 --youtube-urls '<comma-separated public Shorts/watch URLs>' --max-search-queries 4
```

After a user-provided Shorts/reference run, inspect the digest ordering: concrete Reddit/YouTube public metadata should appear before weak autocomplete rows; demand rollups should show whether each family is usable or weak.

Update handoff with the stage, count of metadata rows, demand-signal caveat, and next quality rung such as deduplication/query-family labels.
