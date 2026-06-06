> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat Authenticated Wave 2

Status: completed / authenticated readiness + first verified IDOR lesson proof
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> `<attacker-vm>` -> Docker-backed WebGoat on `<victim-vm>`
Target: `http://<lab-ip>:8080/WebGoat`
Artifacts: `<artifact-output-dir>/webgoat_authenticated_wave2_20260522T040820Z/`
Runner: `scripts/labs/webgoat_authenticated_wave2.sh`

## Scope and boundaries

- Authorized local lab only.
- No public or third-party targets.
- No brute force; used WebGoat lesson-provided credentials only.
- No credential theft, no external callback, no destructive write, no shell/persistence, no real secret read.
- Browser evidence deferred because Kali Playwright driver is currently broken/missing; HTTP/session evidence is preserved.

## Results

- Throwaway WebGoat users registered successfully after switching to the lesson-compatible password `webgoat`.
- Session cookies were captured for two throwaway users.
- Authenticated `/start.mvc` and `/service/lessonmenu.mvc` returned HTTP 200.
- Lesson menu exposed required next lanes:
  - `#lesson/IDOR.lesson`
  - `#lesson/JWT.lesson`
  - `#lesson/CrossSiteScripting.lesson`
  - `#lesson/PathTraversal.lesson`
- Direct lesson content URLs were confirmed:
  - `/WebGoat/IDOR.lesson`
  - `/WebGoat/JWT.lesson`
  - `/WebGoat/CrossSiteScripting.lesson`
  - `/WebGoat/PathTraversal.lesson`

## Verified IDOR proof

Using the lesson-provided credentials from `IDOR.lesson.html`:

- POST `/WebGoat/IDOR/login` with `tom:cat` returned HTTP 200.
- GET `/WebGoat/IDOR/profile` returned Tom Cat's own profile with `userId=2342384`.
- GET `/WebGoat/IDOR/profile/2342388` returned HTTP 200 and WebGoat feedback `lessonCompleted: true`, `Well done, you found someone else's profile`.

This is a verified local-lab Access Control / IDOR proof. It demonstrates horizontal object reference access in the training app. It does not imply reportability outside the lab.

## Evidence files

- `summary.md`
- `authenticated_gets.csv`
- `observations.jsonl`
- `lessons/IDOR.lesson.html`
- `lessons/JWT.lesson.html`
- `lessons/CrossSiteScripting.lesson.html`
- `lessons/PathTraversal.lesson.html`
- `idor_probe/idor_login.json`
- `idor_probe/profile.json`
- `idor_probe/profile_2342388.json`

## Next lanes

1. Convert the manual IDOR proof into a reusable script subroutine or dedicated bundle runner.
2. Continue WebGoat JWT/token proof.
3. Continue reflected XSS runtime proof after fixing or replacing the broken Kali Playwright driver.
4. Continue Path Traversal safe-marker lesson proof.
