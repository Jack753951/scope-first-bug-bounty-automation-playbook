> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Obsidian Local REST API Integration

Use this when the user wants Obsidian access through the community `Local REST API` plugin instead of direct filesystem-only vault edits.

## Setup pattern

1. In Obsidian: Settings → Community plugins → install and enable `Local REST API`.
2. Keep the service bound to localhost. Prefer the default HTTPS endpoint:

```text
https://127.0.0.1:27124
```

3. Store non-secret and secret config in the Hermes env file, not in chat, not in the repo, and not inside Obsidian notes. Use `OBSIDIAN_REST_API_URL` as the canonical API URL variable; if an older setup used `OBSIDIAN_API_BASE`, migrate it to the canonical name.

```text
OBSIDIAN_VAULT_PATH=<user-home>
OBSIDIAN_REST_API_URL=https://127.0.0.1:27124
OBSIDIAN_API_KEY=<set manually; never print or paste in chat>
```

4. Restart Hermes or run `/reload` after editing `.env`.

## Creating/opening a vault on Windows

A vault is just a folder. If the user cannot find the Obsidian UI button, create the folder first and tell them to open it from Obsidian:

```powershell
New-Item -ItemType Directory -Force "<user-home>"
```

In Obsidian:

- From the startup vault chooser: choose **Open folder as vault**.
- If already inside a vault: click the vault name / vault icon at bottom-left → **Open another vault** or **Manage vaults** → **Open folder as vault**.
- If the button is hard to find: press `Ctrl+P` and search `Open another vault` or `Manage vaults`.

For multi-project knowledge management, use project namespaces inside one vault, e.g. `Projects/YouTubeAgent/`, and only create the requested project tree unless the user asks for all projects.

## Windows/Git-Bash notes

On Windows Hermes often runs terminal commands through Git-Bash/MSYS. Use forward-slash paths such as:

```text
<user-home>
```

A safe way for the user to edit the env file manually:

```bash
notepad "$HOME/AppData/Local/hermes/.env"
```

When invoking PowerShell from the bash-backed terminal, wrap the whole `-Command` body in single quotes so Bash does not expand PowerShell variables like `$vault`, and avoid raw backtick escape sequences in double-quoted bash strings. Example:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -Command '$vault="<user-home>"; New-Item -ItemType Directory -Force -Path $vault | Out-Null; Write-Output "VAULT=$vault"'
```

## Reachability probe

Check whether the service is listening without printing secrets:

```bash
python - <<'PY'
import urllib.request, ssl
url='https://127.0.0.1:27124/'
try:
    ctx=ssl._create_unverified_context()
    with urllib.request.urlopen(url, timeout=2, context=ctx) as r:
        print(f'reachable status={r.status}')
except Exception as e:
    print(f'not_reachable {type(e).__name__}: {e}')
PY
```

## Auth probe pattern

When `OBSIDIAN_API_KEY` is set, use the Authorization header but never echo the key:

```bash
python - <<'PY'
import os, ssl, urllib.request
url=os.environ.get('OBSIDIAN_REST_API_URL','https://127.0.0.1:27124')
key=os.environ.get('OBSIDIAN_API_KEY')
if not key:
    print('OBSIDIAN_API_KEY missing')
    raise SystemExit(1)
req=urllib.request.Request(url.rstrip('/') + '/', headers={'Authorization': 'Bearer ' + key})
ctx=ssl._create_unverified_context()
with urllib.request.urlopen(req, timeout=3, context=ctx) as r:
    print(f'authenticated status={r.status}')
PY
```

## Operating preference

Use API-first when the user requests it or when Obsidian state matters. Keep `OBSIDIAN_VAULT_PATH` as a fallback so notes can still be read/written as markdown when Obsidian is closed or the REST plugin is unavailable.

## Safety

- Never ask the user to paste the API key into chat.
- Never store the key in Obsidian notes.
- Never commit the key to the project repo.
- Do not expose the REST API on `0.0.0.0` for this use case.
