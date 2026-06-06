> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Obsidian Local REST API routing

Use this reference when a user wants Hermes to access Obsidian through the Local REST API, especially with multiple projects or vaults.

## Key facts

- The Obsidian Local REST API plugin is enabled per vault.
- The API operates on the vault currently open in Obsidian, not necessarily the path stored in `OBSIDIAN_VAULT_PATH`.
- `OBSIDIAN_API_KEY` is a secret. Never print, store in Obsidian, commit, or save it to memory.
- Keep the API bound to localhost (`https://127.0.0.1:27124` by default).
- Keep a filesystem fallback path for each project so notes can be written safely if API context is ambiguous.

## Recommended environment

```text
OBSIDIAN_REST_API_URL=https://127.0.0.1:27124
OBSIDIAN_API_KEY=<manual secret in Hermes .env>
OBSIDIAN_VAULT_PATH=<optional fallback path>
```

## Multi-project routing map

Store non-secret routing outside the repo, for example:

```text
<user-home>
```

Example:

```json
{
  "default_project": "cybersec",
  "api_url_env": "OBSIDIAN_REST_API_URL",
  "api_key_env": "OBSIDIAN_API_KEY",
  "projects": {
    "cybersec": {
      "display_name": "Cybersec Lab",
      "api_relative_root": "Projects/Cybersec Lab",
      "vault_path": "<user-home> Lab",
      "sensitivity": "restricted",
      "rules": ["No secrets, credentials, loot, hashes, or client-sensitive data."]
    }
  }
}
```

## Verification recipe

Use a script that reads Hermes `.env`, checks for key presence without printing the key, then calls API endpoints.

```python
from pathlib import Path
import os, ssl, urllib.request, urllib.parse

vals = {}
env_path = Path.home() / 'AppData' / 'Local' / 'hermes' / '.env'
for raw in env_path.read_text(encoding='utf-8', errors='replace').splitlines():
    line = raw.strip()
    if line and not line.startswith('#') and '=' in line:
        k, v = line.split('=', 1)
        vals[k.strip()] = v.strip().strip('"').strip("'")

url = vals.get('OBSIDIAN_REST_API_URL', 'https://127.0.0.1:27124').rstrip('/')
key = vals.get('OBSIDIAN_API_KEY')
print('obsidian_api_key_configured=' + str(bool(key)).lower())
if not key:
    raise SystemExit(0)

ctx = ssl._create_unverified_context()
headers = {'Authorization': 'Bearer ' + key}

def api_path(rel):
    return '/vault/' + urllib.parse.quote(rel, safe='/')

def request(method, path, data=None, content_type=None):
    h = dict(headers)
    if content_type:
        h['Content-Type'] = content_type
    req = urllib.request.Request(url + path, method=method, headers=h, data=data)
    with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
        return resp.status, resp.read(10000)

status, body = request('GET', '/vault/')
print('vault_list_status=' + str(status))

rel = 'Projects/Cybersec Lab/00_Index/Hermes API Test.md'
content = '# Hermes API Test\n\nAPI connectivity works. No secrets stored here.\n'
status, _ = request('PUT', api_path(rel), content.encode('utf-8'), 'text/markdown; charset=utf-8')
print('write_status=' + str(status))
status, body = request('GET', api_path(rel))
print('read_back_ok=' + str(b'API connectivity works' in body).lower())
```

## Troubleshooting

- `WinError 10061` / connection refused: Obsidian is closed, the plugin is disabled, or the currently open vault does not have the plugin running. Open Obsidian, enable Local REST API in that vault, then retry.
- `401`/`403`: key/header issue; ensure `Authorization: Bearer <key>` is used and reload Hermes after editing `.env`.
- `404` for an existing filesystem note: the API is probably pointed at a different currently open vault. Use `/vault/` to inspect the API-visible root and either switch vaults or use filesystem fallback.

## Migration rule

When moving notes from a standalone vault into a multi-project API vault, copy rather than delete first. Verify with both filesystem counts and API read-back before treating the migration as complete.
