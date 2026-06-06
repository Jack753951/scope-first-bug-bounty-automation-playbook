> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Obsidian API Setup

## Goal

Use Obsidian Local REST API instead of direct path-only file access when convenient.

## Current local API URL

```text
https://127.0.0.1:27124
```

## Hermes environment variables

```text
OBSIDIAN_VAULT_PATH=<user-home>
OBSIDIAN_REST_API_URL=https://127.0.0.1:27124
OBSIDIAN_API_KEY=<set manually in Hermes .env; do not paste in chat>
```

Hermes env file:

```text
<user-home>
```

## Safety rules

- Do not paste the API key into chat.
- Do not commit the API key to any repo.
- Do not store the API key in Obsidian notes.
- Keep the API bound to localhost only.
- Prefer HTTPS default port 27124.

## Manual setup steps

1. Open Obsidian.
2. Settings → Community plugins.
3. Turn off Safe mode if needed.
4. Browse and install `Local REST API`.
5. Enable the plugin.
6. Open plugin settings.
7. Confirm it is listening on `https://127.0.0.1:27124`.
8. Copy the API key/token from plugin settings.
9. Open Hermes env file and add:

```text
OBSIDIAN_API_KEY=your_key_here
```

10. Restart Hermes or run `/reload`.

## Test command pattern

Use a request with header:

```text
Authorization: Bearer <OBSIDIAN_API_KEY>
```

Do not print the key in command output.
