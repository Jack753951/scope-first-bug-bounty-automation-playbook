> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_webgoat_idor_lesson_access_control

Status: verified-impact / local-lab only
Date: 2026-05-22
Route/tool: `<attacker-vm>` HTTP/curl -> Docker-backed WebGoat on `<victim-vm>`
Artifacts: `<artifact-output-dir>/webgoat_authenticated_wave2_20260522T040820Z/`
Handoff: `handoff/webgoat_authenticated_wave2_20260522.md`

## When to use

Use this bundle to reproduce and study WebGoat's IDOR lesson as a bounded Access Control / Broken Object Level Authorization training proof.

## Preconditions

- Target is the authorized local WebGoat Docker lab at `<lab-ip>:8080`.
- Execution is from `<attacker-vm>`.
- A throwaway WebGoat session exists.
- No public target, no real user data, no brute force.

## Trigger flow

1. Authenticate to WebGoat with a throwaway lab user.
2. Fetch `/WebGoat/IDOR.lesson` and record the lesson-provided credentials.
3. POST `/WebGoat/IDOR/login` with the lesson-provided `tom:cat` credentials.
4. GET `/WebGoat/IDOR/profile` to retrieve the current user's profile and object identifier.
5. GET `/WebGoat/IDOR/profile/2342388` to retrieve another user's profile.

## Verified evidence

- Own profile returned:
  - name: `Tom Cat`
  - userId: `2342384`
- Alternate object reference returned:
  - HTTP 200
  - `lessonCompleted: true`
  - feedback: `Well done, you found someone else's profile`

## Classification

This is verified-impact inside the training lab because the app itself confirms another profile was accessed through an object-reference change.

It remains lab-only and is not a bug-bounty finding. Real-target use requires program scope/rules, low-rate safe defaults, evidence redaction, manual verification, and report-readiness review.

## Boundaries

- No credential theft; `tom:cat` is lesson-provided.
- No brute force.
- No destructive writes.
- No external callbacks.
- No raw secret/loot retention.
- No automatic report/finding promotion.
