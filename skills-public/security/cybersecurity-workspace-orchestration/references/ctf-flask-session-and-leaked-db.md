> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# CTF Flask Session + Leaked SQLite DB Pattern

Use when a CTF/training web challenge provides a live URL plus leaked application source and a SQLite database.

## Workflow

1. Treat the platform instance as authorized CTF scope, but only touch the explicit URL/host and supplied local files.
2. Inspect source before probing the live service. For Flask apps, check:
   - password verification algorithm and whether hashes are salted/adaptive;
   - whether 2FA/OTP state is stored server-side or in Flask's default client-side session cookie;
   - whether the app uses `session[...]` for sensitive values such as `otp_secret`.
3. Inspect the leaked SQLite DB locally for usernames, password hashes, and 2FA flags.
4. If hashes are unsalted SHA-256/MD5/etc., try common dictionary/crackstation/rockyou-style recovery before any live brute force.
5. If OTP is placed in Flask's default session, remember Flask signs but does not encrypt default cookies. Decode the cookie payload after login and read fields like `otp_secret`; do not brute-force OTP unless decoding is impossible.
6. Verify with minimal live requests: login once, decode cookie locally, submit the recovered OTP once, then fetch the flag.

## Minimal Flask session decode sketch

```python
import base64, json, zlib

cookie = "..."  # value of Flask `session` cookie
compressed = cookie.startswith('.')
payload = cookie.split('.')[1] if compressed else cookie.split('.')[0]
payload += '=' * ((4 - len(payload) % 4) % 4)
raw = base64.urlsafe_b64decode(payload)
if compressed:
    raw = zlib.decompress(raw)
print(json.loads(raw))
```

## Pitfalls

- Do not jump straight to high-volume OTP brute force when source shows OTP is stored in a readable client-side cookie.
- Do not generalize CTF authorization to arbitrary hosts; keep target interaction constrained to the provided challenge URL.
- Flask default session cookies are integrity-protected, not confidential. You generally cannot modify them without the secret key, but you can read their JSON payload.
