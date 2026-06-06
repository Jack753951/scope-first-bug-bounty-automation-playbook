> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Codex review checklist for video/render automation agents

Use this reference when a coding task changes Shorts/video rendering, subtitle overlays, topic metadata flowing into render code, or automated media generation pipelines.

## Suggested Codex prompt

```text
Review and, if safe, implement the proposed render/content change. Focus on correctness and safety:

1. Preserve upload/privacy/scheduler defaults unless explicitly requested.
2. Do not expose or modify OAuth tokens, credentials, user runtime databases, or generated final videos.
3. Inspect FFmpeg filtergraph construction for quoting/escaping bugs, especially drawtext text containing commas, colons, backslashes, apostrophes, emoji, and CJK text.
4. Verify wrapping does not silently truncate long unbroken tokens such as URLs/usernames/long English words.
5. Keep function signatures backward compatible where existing callers may omit new metadata.
6. Add or update unit tests plus a lightweight FFmpeg parse/smoke test when FFmpeg is available.
7. Run compile/JSON validation and the project safety validation command.
8. Write a concise handoff note: accepted changes, validation results, and risks intentionally left out of scope.
```

## Failure modes worth asking Codex to hunt

- `drawtext` filters broken by unescaped `'`, `:`, `,`, `%`, `\`, or newline characters.
- Text wrapping that slices `word[:max_chars]` and drops the rest.
- Visual overlays blocking subtitles or important subject area.
- Render features that accidentally require every caller to pass a new metadata object.
- Channel config changes bleeding across unrelated channels.
- Tests that pass Python logic but never exercise FFmpeg parsing.

## Verification pattern

- Parse all channel JSON files as UTF-8.
- Compile changed Python modules.
- Run the targeted unit test suite.
- If FFmpeg is installed, run a tiny generated filtergraph smoke test rather than a full render when speed matters.
- Run the project validation command.
- Confirm lock files are clear and no upload/scheduler/OAuth files changed unexpectedly.
