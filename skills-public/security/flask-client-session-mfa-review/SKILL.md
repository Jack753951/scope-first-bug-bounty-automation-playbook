> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: flask-client-session-mfa-review
description: Use when reviewing Flask apps, CTF web challenges, or leaked source/database artifacts for MFA bypasses caused by client-side session secrets and weak unsalted password hashes.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, flask, mfa, ctf, code-review, session]
    related_skills: [cybersecurity-workspace-orchestration, obsidian]
---

# Flask Client-Side Session MFA Review

## Overview

Use this workflow when a Flask application, CTF challenge, or authorized code review includes login/MFA logic plus source code, a leaked database, or HTTP cookies. The key lesson: Flask's default session cookie is signed, not encrypted. Users generally cannot modify it without the secret key, but they can read values stored in it.

Therefore, never treat values placed in `session[...]` as confidential if the app uses Flask's default client-side session backend. MFA OTPs, reset tokens, temporary auth bypass flags, internal secrets, and authorization decisions must stay server-side.

## When to Use

- Flask app stores authentication or MFA state in `session[...]`.
- A CTF/web challenge gives source code plus a SQLite/database leak.
- Hints mention no salt, rockyou, 2FA/MFA safety, signed cookies, or Flask sessions.
- A login flow redirects to `/two_fa`, `/mfa`, `/otp`, or similar after password validation.
- You need a low-noise manual verification path instead of brute-forcing OTPs.

Do not use this to attack unauthorized systems. Apply the cybersecurity scope gate first: CTF/training, local lab, owned asset, written client authorization, or explicit bounty scope.

## Review Workflow

1. Confirm authorization/scope.
   - For CTF/training, restrict interaction to the provided instance and artifacts.
   - For bug bounty/client work, verify allowed techniques before any target-touching request.

2. Inspect password verification.
   - Look for raw hashes such as `hashlib.sha256(password.encode()).hexdigest()`.
   - Check whether salts, per-user work factors, bcrypt, Argon2id, scrypt, or PBKDF2 are used.
   - If the DB is provided and hashes are unsalted, test only the relevant authorized account against known/allowed wordlists or offline lookup.

3. Inspect MFA/session state.
   - Search for `session['otp']`, `session['otp_secret']`, `session['mfa']`, `session['2fa']`, `session['logged']`, reset tokens, magic links, role flags, or temporary secrets.
   - Treat these as readable by the user when using default Flask sessions.
   - Check timestamp/expiry and retry/rate-limit logic separately; missing rate limit is a contributing factor, not the only root cause.

4. Decode the Flask session cookie instead of brute-forcing when possible.
   - Flask session payloads are URL-safe base64 JSON, sometimes zlib-compressed and prefixed with `.`.
   - The signature protects integrity, not confidentiality.
   - Decode only cookies from the authorized test instance/session.

5. Verify minimally.
   - Login with the authorized/cracked credential.
   - Decode the returned session cookie.
   - If the OTP or MFA secret is visible, submit that OTP once.
   - Capture only non-sensitive proof needed for the CTF/report; do not store cookies, live secrets, or flags in durable memory/notes.

## Tiny Cookie Decode Helper

Use this only on an authorized test cookie you generated yourself:

```python
import base64, json, zlib

def decode_flask_cookie_payload(cookie):
    compressed = cookie.startswith('.')
    payload = cookie.split('.')[1] if compressed else cookie.split('.')[0]
    payload += '=' * ((4 - len(payload) % 4) % 4)
    raw = base64.urlsafe_b64decode(payload)
    if compressed:
        raw = zlib.decompress(raw)
    return json.loads(raw)
```

If the result contains values such as `otp_secret`, `reset_token`, `mfa_secret`, or authorization flags, record a candidate finding for client-side secret disclosure.

## Candidate Findings to Consider

- Weak password storage: unsalted raw hash or fast hash for passwords.
- Client-side session secret disclosure: OTP/token/secret stored in readable Flask cookie.
- MFA bypass: MFA verifier consumes an OTP that the user can read from their own cookie.
- Missing OTP throttling: no retry counter/rate limit/lockout on OTP submission.
- Auth state confusion: flags such as `logged=false/true` or `username=admin` stored client-side without server-side pending-MFA state.

Keep automation output as `candidate` / `needs_verification` until manual verification, evidence review, impact, remediation, and retest notes exist.

## Reporting Language

Prefer precise root cause language:

- Good: "The application stores the MFA OTP in Flask's client-side session cookie, which is signed but readable by the client. After password login, the attacker can decode their own session cookie, read the OTP, and complete MFA."
- Weak: "2FA can be brute-forced" when the stronger issue is direct OTP disclosure.

Mention contributing factors separately:

- password hashes use a fast unsalted algorithm;
- admin password is dictionary-crackable;
- OTP is short-lived but visible to the client;
- no OTP retry limit/rate limit exists.

## Remediation

- Store MFA OTPs/secrets server-side only: server-side session store, DB, or cache.
- Use Argon2id, bcrypt, scrypt, or PBKDF2 with per-user salt and appropriate work factor for passwords.
- Add OTP retry counters, rate limiting, lockout/backoff, and monitoring.
- Regenerate session IDs after password login and after MFA completion.
- Do not store reset tokens, OTPs, role decisions, or confidential auth state in client-readable cookies.
- Keep Flask `SECRET_KEY` strong and private, but remember it does not encrypt default sessions.

## Common Pitfalls

1. Jumping straight to OTP brute force. First inspect whether OTP is exposed in source, response, or client-readable session state.
2. Assuming signed means secret. Flask's default signed cookie prevents tampering, not reading.
3. Recording challenge secrets in durable memory/Obsidian. Store reusable technique only; keep flags, cookies, live OTPs, hashes, and passwords out of long-term notes.
4. Treating weak hashing as the only bug. In MFA flows, weak credentials may be just the first step; the stronger finding can be MFA secret disclosure.
5. Using this workflow outside scope. CTF authorization does not transfer to arbitrary external Flask apps.

## Verification Checklist

- [ ] Scope/authorization confirmed.
- [ ] Password hashing scheme identified from source.
- [ ] Database/hash artifact handled locally and minimally.
- [ ] Flask session cookie decoded only for the authorized test session.
- [ ] OTP/token/secret disclosure verified, if present.
- [ ] Manual verification used the least number of target requests practical.
- [ ] Notes/report exclude live cookies, OTPs, flags, passwords, and raw sensitive hashes.
- [ ] Remediation distinguishes password storage, client-side secret storage, and rate limiting.
