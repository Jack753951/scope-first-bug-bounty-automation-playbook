> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A.1 Bounded Content Discovery Summary

Generated: 2026-05-21T10:26:08

## Gate/result

- Pre-health exit: 0
- Execution exit: 0
- Post-health exit: 0
- Observation records: 29
- Status counts: `{"200": 25, "301": 1, "500": 3}`
- Errors: `[]`

## Interesting metadata-only observations

- `/` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/ftp/` -> 200 type=text/html; charset=utf-8 length=11334 location=None
- `/robots.txt` -> 200 type=text/plain; charset=utf-8 length=28 location=None
- `/sitemap.xml` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/.well-known/security.txt` -> 200 type=text/plain; charset=utf-8 length=475 location=None
- `/rest/products/search` -> 200 type=application/json; charset=utf-8 length=16563 location=None
- `/assets/` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/assets/public/` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/public/` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/uploads/` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/backup/` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/backups/` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/admin/` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/administrator/` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/login` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/register` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/account` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/basket` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/checkout` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/api-docs` -> 301 type=text/html; charset=UTF-8 length=158 location=/api-docs/
- `/swagger.json` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/swagger-ui/` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/debug` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/server-status` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/.git/HEAD` -> 200 type=text/html; charset=UTF-8 length=9903 location=None
- `/package.json` -> 200 type=text/html; charset=UTF-8 length=9903 location=None

## Safety posture

- Candidate-only observations; no response bodies intentionally stored.
- Fixed local-lab target only: `http://<lab-ip>:3000`.
- No brute force, exploit payloads, callbacks, recursive crawling/download, or non-GET/HEAD methods were used.
