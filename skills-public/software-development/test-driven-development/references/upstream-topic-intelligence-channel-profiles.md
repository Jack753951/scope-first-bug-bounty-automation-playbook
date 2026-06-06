> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Upstream topic-intelligence channel profile abstraction

Use this TDD rung when a topic-radar/upstream intelligence project risks becoming hardcoded to one YouTube channel/lane (for example `redditstories`) but must serve a multi-channel downstream project.

## Trigger

The user asks whether the upstream project can serve a multi-channel architecture, or asks to make it extensible beyond the first supported lane.

## RED tests first

Add focused tests before implementation:

1. Profile loading is data-driven:
   - a config containing at least two channel profiles loads both without code changes;
   - an unknown channel fails closed instead of silently falling back to the first/default lane.
2. Generic scoring uses channel profile vocabulary:
   - non-first-lane profiles return a generic `channel_fit` dimension;
   - the first/legacy lane may keep a compatibility field (for example `redditstories_fit`) only through explicit profile metadata such as `legacy_fit_field`.
3. CLI routing honors explicit channel input:
   - `score --channel <name> --profile-config <path>` uses the requested profile;
   - unknown `--channel` exits/fails closed;
   - generated scores do not leak legacy lane fields into unrelated channels.
4. History/novelty paths are channel-aware:
   - default history path should resolve to `../youtube_agent/data/<channel>/agent.db` when a channel is supplied;
   - explicit `--db` overrides remain supported for local fixtures and migrations.
5. Safety boundary remains metadata-only:
   - profile/routing tests must not touch script generation, render, upload, scheduler, OAuth/token, privacy, destination, or channel config.

## GREEN shape

Implement a narrow data-only abstraction:

- `config/channel_profiles.example.json` with closed profiles and per-channel vocabulary (`fit_terms`, `proof_terms`, `visual_terms`, `risk_terms`, `weights`).
- Loader helpers such as `load_channel_profiles(path)` and `load_channel_profile(channel, path)`.
- Generic scoring helper such as `score_candidate_for_channel(candidate, profile, ...)` returning shared dimensions (`channel_fit`, proof strength, visualizability, policy safety, timeliness, novelty, overall).
- Legacy wrappers/field aliases only where needed for backward compatibility.
- CLI flags for explicit profile use, while keeping old default behavior stable.

## Handoff wording

State maturity honestly:

- Before this rung: source intake/schema may be extensible, but scoring/transform/novelty is probably first-lane-specific.
- After this rung: profile/scoring/novelty routing is multi-channel-ready, but discovery aliases, market-pattern transforms, and creative concepts may still need profile-driven refactors.

## Pitfalls

- Do not claim the project is fully multi-channel just because `channel` exists in the schema.
- Do not let unknown channels quietly use `redditstories` defaults.
- Do not rename/remove legacy score fields without a compatibility path and tests.
- Do not wire profile labels into production actions; profiles are planning metadata until a separate reviewed plan authorizes behavior changes.
