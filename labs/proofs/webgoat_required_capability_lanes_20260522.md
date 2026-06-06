> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat Required Capability Lanes

Status: active strategy note
Date: 2026-05-22
Scope: local authorized cybersec lab only

## Operator direction

The lab should not avoid higher-risk vulnerability classes entirely. To improve project capability, WebGoat and future Docker-backed targets should include explicit tests for:

- Access Control / IDOR-style lessons
- JWT / token lessons
- Reflected XSS lessons
- Path traversal safe-marker lessons

## Execution constraints

These lanes are required, but they must be executed as bounded lab exercises:

- local authorized lab only
- one lesson / vulnerability proof per run
- pre-health and post-health checks
- save request, response, cookies/session metadata, screenshots/DOM where relevant
- no credential theft
- no external callbacks
- no real secret reads
- no destructive writes
- no persistence or shells
- path traversal must use safe marker files or training-app-provided fixtures only
- XSS must prove runtime execution with harmless DOM marker, not credential/session exfiltration
- JWT tests must use throwaway lab users/tokens only
- Access Control/IDOR tests must compare throwaway users and lab-only lesson objects

## Preferred next order

1. WebGoat registration/login with throwaway users.
2. Access Control / IDOR lesson proof.
3. JWT/token lesson proof.
4. Reflected XSS lesson proof.
5. Path traversal safe-marker lesson proof.

## Classification rule

A lesson proof becomes `verified-impact` only when evidence shows the intended security boundary was crossed or the intended exploit condition was met in the local lab. Otherwise retain as `valuable-candidate` or `attempted-not-verified` with blockers and next conditions.
