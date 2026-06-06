> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# WebGoat JWT Wave 3 2026-05-22

Status: completed / verified low-risk JWT decode proof
Repo handoff: `<user-home>`
Bundle: `<user-home>`
Artifacts: `<user-home>`

## Summary

Ran bounded WebGoat JWT/token lesson wave from `<lab-vm>` against Docker-backed WebGoat on `<lab-vm>`.

Verified proof:

- `POST /WebGoat/JWT/decode`
- candidate value `user`
- server returned `lessonCompleted=true`
- assignment: `JWTDecodeEndpoint`

## Important evidence

`jwt_probe/jwt_decode_user.json`:

```json
{
  "lessonCompleted" : true,
  "feedback" : "Congratulations. You have successfully completed the assignment.",
  "assignment" : "JWTDecodeEndpoint",
  "attemptWasMade" : true
}
```

## Candidate-only JWT lanes discovered

- JWT signing / role escalation
- weak key / secret token
- refresh token flow
- JKU misuse
- KID misuse
- voting-token issue/usage flow

## 對專案有什麼幫助

- Gives the project a verified JWT/token lesson flow after the WebGoat IDOR proof.
- Adds endpoint and token-pattern seeds for later JWT sub-waves.
- Improves script reliability by avoiding shell `USER` variable collision.

## 新增/更新了什麼

- New JWT wave script.
- New verified JWT decode bundle.
- New handoff result.
- New local artifacts.
- Active queue and accepted changes updated in repo.

## Next

Recommended next: WebGoat JWT weak-key/signing or refresh-token manipulation, still local-lab only.
