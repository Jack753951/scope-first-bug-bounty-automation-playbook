> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# WebGoat JWT/token proof waves

Use this reference when a WebGoat local-lab lane moves from authenticated session setup into JWT/token lessons. It captures reusable lessons from the 2026-05-22 WebGoat JWT wave; keep future JWT work local-lab bounded unless explicit scope/rules authorize more.

## Trigger

- Docker-backed WebGoat is reachable from `<lab-vm>` to the victim host.
- An authenticated WebGoat session is needed for `/WebGoat/JWT.lesson` and related lesson JS/endpoints.
- The goal is to build reusable JWT/token review capability without brute force, cracking, forging, external JWKS hosting, or real-target finding promotion.

## Reusable workflow

1. Register/login with a throwaway user and simple lesson-compatible password.
2. Avoid shell built-in/user environment collisions: do not name the generated username variable `USER`; use `WG_USER` or another explicit name.
3. Fetch the lesson page and lesson JavaScript from authenticated session context.
4. Extract endpoint candidates from the lesson HTML/JS and preserve them as an endpoint map.
5. Decode sample JWTs offline for structure/claims inspection; redact or avoid durable retention of real secrets/tokens outside local artifacts.
6. For a low-risk first proof, prefer the WebGoat decode assignment before signing/role-escalation lanes:
   - POST `/WebGoat/JWT/decode`
   - Try decoded user candidates derived from lesson token payloads (example successful candidate: `user`).
   - Promote only if the server returns `lessonCompleted: true`, feedback, assignment name, and attempt marker.
7. Record later JWT lanes as candidates until individually verified: signing/role escalation, weak key/secret, refresh token flow, JKU misuse, KID misuse, and voting-token issue/usage flows.

## Evidence shape

Keep the following artifacts for the run:

- `summary.md`
- `observations.jsonl`
- `endpoint_extract.txt`
- `jwt_probe/decoded_tokens.jsonl`
- `jwt_probe/jwt_decode_<candidate>.json`
- relevant HTTP headers/status files

Use `verified-impact` only for the exact lesson assignment that returned completion evidence. Keep future JWT techniques as `candidate`, `valuable-candidate`, or `blocked/deferred` until the trigger and impact are reproduced.

## Boundaries

- Local authorized WebGoat lab only.
- No brute force or dictionary cracking by default.
- No JWT forging unless it is the explicit next bounded lesson lane.
- No external callbacks/JWKS hosting unless isolated and explicitly authorized.
- No credential theft, destructive writes, or report/finding promotion.

## Closeout format for this user

Every completed lab/test wave should include two explicit sections in the final user-facing summary:

- `對專案有什麼幫助`: explain how the test improves the project, capability library, evidence quality, automation readiness, false-positive handling, or future bug-bounty/pentest workflow.
- `新增/更新了什麼`: list new/changed scripts, bundles, handoffs, Obsidian notes, artifacts, blockers, and reusable workflow changes.
