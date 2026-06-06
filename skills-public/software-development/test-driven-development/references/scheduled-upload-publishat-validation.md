> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Scheduled Upload `publishAt` Validation

Use this for safety-sensitive code paths that schedule an existing artifact for future publication, especially YouTube/Shorts upload flows.

## Durable lesson

A scheduled-upload approval phrase and destination guard are not enough. The timestamp itself must fail closed before DB insert, API upload, or side effects.

## Required RED tests

Add tests that reject all of the following:

- missing `publish_at`
- malformed timestamp strings
- ISO-looking timestamps without timezone information (naive datetimes)
- timestamps in the past

Add a GREEN test that accepts a clearly future timezone-aware ISO 8601 timestamp and verifies the upload call receives:

- `privacy_status="private"`
- exact `publish_at`
- exact existing artifact path
- no generation/remake path

Use far-future timestamps in unit tests (for example year 2099) so tests do not age into failures.

## Implementation notes

- Normalize trailing `Z` to `+00:00` before `datetime.fromisoformat` if the language/runtime needs it.
- Require `tzinfo` and a non-`None` UTC offset.
- Compare against current time in UTC.
- Keep error messages explicit enough to show which gate failed, but do not include secrets or OAuth/token data.
- Validate before DB insert and before upload/API side effects.

## Pitfall

Do not temporarily set broad channel flags (for example a render-fix acknowledgement or production activation flag) just to unblock one scheduled existing-artifact upload. If an exception is needed, encode it in the narrow existing-artifact path and reset/avoid broad activation flags.
