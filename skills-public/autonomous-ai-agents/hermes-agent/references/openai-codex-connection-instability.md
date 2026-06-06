> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# OpenAI Codex backend connection instability

Use this when Hermes shows repeated APIConnectionError / Connection error against:

```text
provider=openai-codex
base_url=https://chatgpt.com/backend-api/codex
model=gpt-5.5
```

## Durable pattern

This is often not a bad repo, git operation, or missing login. The ChatGPT/Codex backend is a streamed OAuth-backed route and can be less stable than regular API-key providers, especially with:

- long sessions and large context windows
- context compression
- background review / curator work
- many tool calls in one session
- repeated auxiliary requests using the same `openai-codex` provider

Common log strings:

```text
APIConnectionError: Connection error
HTTP 503: upstream connect error or disconnect/reset before headers
peer closed connection without sending complete message body (incomplete chunked read)
Codex auxiliary Responses stream exceeded 120.0s total timeout
```

## First triage

Check whether auth is actually present before asking the user to re-login:

```bash
hermes status --all
hermes doctor
```

If `OpenAI Codex auth` is logged in, treat re-login as a secondary diagnostic, not the first fix.

## Preferred fix: move auxiliary compression off openai-codex

If main chat uses `openai-codex` and `auxiliary.compression` also uses `openai-codex`, long conversations can fail during summary/compression. Prefer keeping the main model if desired but moving compression to a stable API provider already configured on the machine.

Example when Anthropic is configured:

```bash
hermes config set auxiliary.compression.provider anthropic
hermes config set auxiliary.compression.model claude-sonnet-4
hermes config set auxiliary.compression.timeout 300
```

Then restart the Hermes session. If the model name is not accepted, use:

```bash
hermes model
```

to confirm the exact configured provider/model names.

## If failures continue

- If only `attempt 1/3` appears and later retry succeeds, explain it as transient retry noise.
- If all retries fail or the UI stalls, switch the main model/provider to a regular API provider via `hermes model`.
- Re-login only after checking status, or when auth is missing/stale:

```bash
hermes login --provider openai-codex
```

## Reporting to user

Be explicit about uncertainty and distinguish:

- confirmed local state (`hermes status`, `hermes doctor`, logs)
- likely root cause (unstable Codex backend / long streaming compression)
- recommended smallest change (move auxiliary compression)
- what is not implicated (repo/git task unless logs point there)
