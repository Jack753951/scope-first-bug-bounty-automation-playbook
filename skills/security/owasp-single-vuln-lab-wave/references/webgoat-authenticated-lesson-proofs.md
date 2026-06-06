> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat authenticated lesson proofs

Session-derived reference for Docker-backed WebGoat/WebWolf local lab work.

## Lab route

- Windows Hermes remains the control plane.
- `<attacker-vm>` is the tester/attacker VM.
- `<victim-vm>` is the Docker target host.
- WebGoat target used in this session: `http://<lab-ip>:8080/WebGoat`.
- WebWolf target used in this session: `http://<lab-ip>:9090/WebWolf`.
- Keep both VMs host-only for target-touching execution; NAT may be used only for bounded install/update windows, then closed and verified from inside the VMs.

## Authenticated wave pattern

Use a two-stage WebGoat wave before individual lesson proof attempts:

1. Register short throwaway users.
2. Use a WebGoat-compatible simple lab password such as `webgoat` when registration rejects stronger/special-character passwords.
3. POST login and confirm a `JSESSIONID`/session cookie exists.
4. Fetch authenticated `/start.mvc` and `/service/lessonmenu.mvc`.
5. Confirm required lesson links exist in the menu before probing direct content URLs.
6. Fetch direct lesson content at paths such as:
   - `/WebGoat/IDOR.lesson`
   - `/WebGoat/JWT.lesson`
   - `/WebGoat/CrossSiteScripting.lesson`
   - `/WebGoat/PathTraversal.lesson`
7. Preserve request/response headers, cookies, lesson HTML, observations JSONL, summary, and post-health.

## IDOR proof pattern verified in session

The WebGoat IDOR lesson provides credentials in the lesson HTML:

- username: `tom`
- password: `cat`

Bounded proof steps:

1. POST `/WebGoat/IDOR/login` with `tom:cat` using the authenticated WebGoat lab session.
2. GET `/WebGoat/IDOR/profile` and capture the own profile.
3. Record `userId=2342384` for `Tom Cat` as own-object evidence.
4. GET `/WebGoat/IDOR/profile/2342388`.
5. Verified success evidence is a JSON response containing:
   - `lessonCompleted: true`
   - `feedback: Well done, you found someone else's profile`
   - `output` containing `Buffalo Bill` and `userId=2342388`

Classification: `verified-impact / local-lab only`. This proves the training-app IDOR flow, not a real-target reportable finding.

## Evidence and artifact convention

For each WebGoat lesson wave, write:

- `<artifact-output-dir>/<run_id>/summary.md`
- `<artifact-output-dir>/<run_id>/observations.jsonl`
- `<artifact-output-dir>/<run_id>/authenticated_gets.csv`
- `<artifact-output-dir>/<run_id>/lessons/<Lesson>.lesson.html`
- per-lesson proof directory, e.g. `idor_probe/`
- repo handoff under `handoff/`
- bundle under `modules/bundles/`
- Obsidian project note when the run changes strategy/progress
- `handoff/accepted_changes.md`
- `handoff/active_strategy_queue.md`
- `scripts/SCRIPT_INVENTORY.md` for reusable runners

## Boundaries

- Local authorized lab only.
- No public target.
- No brute force.
- No credential theft; lesson-provided credentials are allowed as training fixture input.
- No external callbacks unless using an explicitly isolated callback lab.
- No destructive writes unless the lesson explicitly requires a recoverable local-lab state change and recovery is documented.
- No shell/persistence.
- No real secret/loot retention.
- No automatic report/finding promotion.

## Pitfalls

- WebGoat registration may reject generated usernames/passwords; prefer short throwaway usernames and the simple lab password `webgoat` before treating registration as broken.
- Hash-style lesson links in `/service/lessonmenu.mvc` (`#lesson/IDOR.lesson`) are client routes; direct lesson content is available at `/WebGoat/IDOR.lesson`, not `/WebGoat/lesson/IDOR.lesson`.
- Browser evidence may be deferred or rerouted when the browser driver setup is transiently broken. Do not encode this as a permanent limitation; preserve HTTP/session evidence and continue with non-browser proof types such as JWT/IDOR first.
- For reflected XSS runtime proof, require a working browser/runtime route or explicitly record the browser blocker and move to JWT/path traversal first.

## Next preferred WebGoat order after baseline

1. Authenticated session and lesson menu enumeration.
2. Access Control / IDOR proof.
3. JWT/token proof.
4. Reflected XSS runtime proof once browser runtime tooling is available.
5. Path Traversal safe-marker proof.
