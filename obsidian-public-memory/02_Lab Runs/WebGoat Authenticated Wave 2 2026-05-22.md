> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# WebGoat Authenticated Wave 2 2026-05-22

Status: completed / first WebGoat verified lesson proof
Repo handoff: `<user-home>`
Bundle: `<user-home>`
Artifacts: `<user-home>`

## Summary

WebGoat authenticated wave 2 established throwaway-user login/session handling and enumerated the authenticated lesson menu. It confirmed required lanes are present:

- IDOR
- JWT
- CrossSiteScripting
- PathTraversal

It then completed the first verified WebGoat lesson proof for Access Control / IDOR:

- POST `/WebGoat/IDOR/login` with lesson-provided `tom:cat` returned HTTP 200.
- GET `/WebGoat/IDOR/profile` returned Tom Cat profile with `userId=2342384`.
- GET `/WebGoat/IDOR/profile/2342388` returned HTTP 200 and `lessonCompleted: true`, `Well done, you found someone else's profile`.

## Boundary

Local authorized lab only. No brute force, no credential theft, no external callbacks, no destructive writes, no real secret reads. Browser evidence deferred because Kali Playwright driver is broken/missing.

## Next

1. WebGoat JWT/token proof.
2. WebGoat reflected XSS proof after browser runtime tooling is fixed/replaced.
3. WebGoat Path Traversal safe-marker proof.
