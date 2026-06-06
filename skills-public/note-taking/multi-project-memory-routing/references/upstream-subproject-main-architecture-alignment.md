> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Upstream subproject ↔ main-project architecture alignment

Use when a helper/upstream repo is meant to serve a larger main project, especially when the user corrects that the helper must support the main project's multi-channel architecture rather than a single early lane.

## Trigger

- User says to reference the main project architecture before deciding integration shape.
- Helper repo starts with a narrow first lane (for example `redditstories`) but must become extensible across main-project channels.
- You are adding channel/profile/scoring/routing concepts in the helper repo.

## Procedure

1. Inspect the main project's authority files before designing helper abstractions:
   - channel config registry, e.g. `channels/*.json`
   - config/channel model fields, e.g. `config.Channel`
   - engine registries/default mappings, e.g. `script_engines.CHANNEL_DEFAULT_ENGINES`
   - profile/metadata registries, e.g. media/asset/render/QA profile maps
   - data layout conventions, e.g. `data/<channel>/agent.db`
2. Mirror real main-project channel names in the helper repo unless the work is explicitly marked as an experiment.
3. Fail closed for unknown channel/profile names. Do not silently fall back from an unknown channel to the first supported lane.
4. Keep compatibility for the first lane when needed, but use generic fields for new lanes. Example: preserve `redditstories_fit` for legacy consumers while non-legacy channels use `channel_fit`.
5. Add a regression test that the helper's example/profile config covers the active main-project channel names inspected in step 1.
6. Record the inspected main-project files and alignment decision in repo handoff, not global memory. Save only a compact cross-project signpost to Hermes memory if the preference should persist.

## Safety boundary

Architecture alignment is metadata/planning work only. It must not edit main-project channel JSON, OAuth/token files, privacy defaults, scheduler state, upload destinations, or production activation gates unless the user explicitly asks and the project gate allows it.

## Pitfall

Do not invent plausible generic channel names such as `facts` or `scary` as production profiles when the main project currently uses different concrete names such as `psychology`, `chinese`, or `redditscary`. Generic examples are fine only when explicitly labeled as examples/experiments and not mixed into production alignment docs.
