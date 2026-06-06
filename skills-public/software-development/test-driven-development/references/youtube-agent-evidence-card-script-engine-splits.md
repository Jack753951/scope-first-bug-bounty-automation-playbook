> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent Evidence Cards and Script-Engine Split Fixes

Use this reference when debugging youtube_agent regressions around Reddit evidence cards, script-engine overrides, and generated/scheduled artifacts.

## Durable lessons from the session

- Treat local draft, uploaded private, scheduled, and public/audience-test states as distinct status classes. Do not report a scheduled/uploaded success until a YouTube video id and publishAt/privacy state are verified.
- Evidence cards must be source-provenance overlays, not invented proof. If a script lacks Reddit source metadata, skip the Reddit evidence card rather than using placeholder text. If only `source_subreddit` is known, showing `r/<subreddit>` is acceptable; do not invent a URL.
- When adding a split/divergent script version, verify the engine actually reaches the generated artifact metadata. A CLI override can be silently defeated by channel/story-source default routing.
- Add a regression test that `resolve_script_engine_name(channel, topic=None)` respects explicit non-default engine overrides before generating a real draft.
- QA generated artifacts by reading `metadata.json` and `footage_relevance_report.json`, not just by trusting CLI logs. Confirm `script_engine`, `script_family`, `opening_asset_bucket`, `opening_diversity_rule`, render profile labels, and stock deny/selected asset provenance.
- For redditstories cold-open gates, distinguish true soft setup from boundary/intrusion conflict language such as `wanted to bring` or `insisted on bringing`; add narrow regression tests for accepted conflict openings.

## Practical TDD loop

1. Write focused failing tests for the contract:
   - no placeholder evidence cards without source metadata;
   - subreddit-only source cards do not invent URLs;
   - explicit split-engine override survives Reddit auto-source routing;
   - split engine writes distinct family/visual-policy metadata;
   - cold-open gate accepts realistic boundary/intrusion conflict wording.
2. Patch the smallest production functions involved:
   - evidence-card builder;
   - script engine registration/routing;
   - split-engine class metadata/policy;
   - visual policy enrichment;
   - cold-open term list or classifier.
3. Run targeted unittest modules first, then generate one real draft with the split engine.
4. Inspect generated metadata/relevance report/subtitles and render QA output.
5. Only after artifact verification proceed to upload/schedule gates, OAuth channel confirmation, handoff updates, and final validation.

## Pitfalls

- Do not let the default Reddit auto-source engine mask a requested split version.
- Do not publish or schedule based only on a successful local draft; upload/schedule is a separate side-effect with separate verification.
- Do not preserve placeholder evidence-card text for generic stories; it creates fake provenance.
- Do not treat transient ElevenLabs paid-plan failures as blockers when the project falls back to Edge TTS successfully.
