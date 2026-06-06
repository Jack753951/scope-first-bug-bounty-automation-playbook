> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# WebGoat Required Capability Lanes 2026-05-22

Status: active strategy note
Repo handoff: `<user-home>`

## Direction

The cybersec lab should explicitly test these capability lanes instead of avoiding them because they can be high-risk if misused:

- Access Control / IDOR-style lessons
- JWT / token lessons
- Reflected XSS lessons
- Path traversal safe-marker lessons

## Guardrails

- Local authorized lab only.
- One lesson proof per run.
- Pre/post health checks.
- No credential theft.
- No external callbacks.
- No destructive writes.
- No real secret reads.
- No shells/persistence.
- XSS uses harmless DOM marker only.
- Path traversal uses safe marker/training fixtures only.
- JWT and Access Control use throwaway lab users/tokens only.

## Preferred next order

1. WebGoat registration/login with throwaway users.
2. Access Control / IDOR lesson proof.
3. JWT/token lesson proof.
4. Reflected XSS lesson proof.
5. Path traversal safe-marker lesson proof.
