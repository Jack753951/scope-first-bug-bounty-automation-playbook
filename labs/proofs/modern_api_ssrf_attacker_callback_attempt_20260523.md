> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# modern_vuln_api SSRF True Attacker Callback Attempt — 2026-05-23

Status: blocked/deferred at SSRF trigger step; environment and callback route prepared, no SSRF proof claim
Date: 2026-05-23
Route/tool: Windows Hermes control plane -> `<attacker-vm>` attacker/listener -> `<victim-vm>` Docker-backed disposable target
Visible runtime/model: Hermes current session, exact backend model visible to user as current chat metadata if exposed by CLI
Run ID: `modern_api_ssrf_attacker_callback_20260523T035629Z`
Local artifacts: `<artifact-output-dir>/modern_api_ssrf_attacker_callback_20260523T035629Z/`

## Vulnerability class

- OWASP 2021: A10 Server-Side Request Forgery (SSRF)
- CWE: CWE-918
- Lane: local-learning-lab / active callback proof / not public-target ready

## OSS-first reconnaissance

Decision: `adapt` / `write-custom-bounded-runner deferred`.

References saved under:

- `setting/local/oss_refs/ssrf_callback_20260523/PayloadsAllTheThings_SSRF_README.md`
- `setting/local/oss_refs/ssrf_callback_20260523/SSRFmap_README.md`
- `setting/local/oss_refs/ssrf_callback_20260523/nuclei_generic_ssrf.yaml` was attempted but the fetched file was only 14 bytes and should be treated as invalid/check-later.

Rationale:

- PayloadsAllTheThings and SSRFmap confirm the high-signal pattern: URL-like parameters plus out-of-band/callback evidence.
- `scripts/ssrf_finder.sh` already exists, but its public OAST/interactsh behavior is not ideal for the local-only lab proof.
- The right local-lab adaptation is a host-only attacker callback listener plus a disposable vulnerable target `/fetch?url=...` endpoint.

## Environment work completed

1. Confirmed both VMs were host-only and Internet-closed before tool/target work:
   - attacker `<lab-ip>`, no default Internet route
   - victim `<lab-ip>`, no default Internet route
2. Opened temporary NAT on `<attacker-vm>` to pull `python:3-alpine`, then closed NAT and verified attacker Internet closed.
3. Opened temporary NAT on `<victim-vm>` to pull `python:3-alpine`, then closed NAT and verified victim Internet closed.
4. Copied `labs/modern_vuln_api/modern_vuln_api.py` and helper scripts to victim path `/home/kali/hermes-labs/modern_vuln_api/`.
5. Started Docker-published attacker callback listener container `ssrf-callback-18183` on `<lab-ip>:18183`.
6. Verified victim-to-attacker callback reachability through Docker-published listener. Evidence:
   - `callback/requests.jsonl` contains client `<lab-ip>` path `/ping?marker=modern_api_ssrf_attacker_callback_20260523T035629Z`.
7. Started Docker-published vulnerable target container `modern-api-ssrf-18081` on `<lab-ip>:18081` and observed local Docker log health GET 200.

## Blocker

The actual SSRF trigger command from attacker to victim `/fetch?url=http://<lab-ip>:18183/...` was denied by the local safety layer:

```text
BLOCKED: User denied. Do NOT retry.
```

Per project/skill discipline, I did not retry around that denial and do not claim SSRF true-attacker callback verification for this run.

## Cleanup / recovery

Completed cleanup:

- Removed attacker listener container `ssrf-callback-18183`.
- Removed victim target container `modern-api-ssrf-18081`.
- Verified attacker Internet closed after temporary NAT window.
- Verified victim Internet closed after temporary NAT window.
- Pulled artifacts back to local `<artifact-output-dir>/modern_api_ssrf_attacker_callback_20260523T035629Z/`.

No snapshot restore was needed.

## Evidence status

Verified:

- OSS-first references saved.
- Temporary NAT/image acquisition worked and was closed.
- Docker-published attacker callback listener is reachable from victim.
- Docker-published modern_vuln_api target can run on victim.
- Cleanup completed.

Not verified:

- SSRF `/fetch?url=attacker-callback` trigger was not executed due safety denial.
- No true attacker SSRF callback should be claimed from this attempt.

## Project benefit

- Validated the infrastructure needed for a future true attacker-side SSRF callback: Docker-published listener on attacker plus Docker-published vulnerable target on victim.
- Confirmed that raw host high ports are blocked/unreliable across VMs, while Docker-published ports are the right route for this lab pattern.
- Confirmed the new policy allowing temporary NAT/target changes is useful and recoverable when recorded.
- Preserved a clean blocked/deferred handoff instead of overstating a failed/denied proof.

## Recommended next step

Use this as a setup run. For the next SSRF wave, create a narrowly-scoped reviewed runner that:

1. starts Docker-published listener and target,
2. records pre-health and callback baseline,
3. performs exactly one `/fetch` SSRF request with a unique marker,
4. records positive/control callback logs,
5. cleans both containers,
6. closes/verifies NAT posture,
7. emits only local-lab verified-impact if callback marker appears from the victim target.

If the safety layer still denies the explicit trigger, switch lanes rather than retrying around the denial.
