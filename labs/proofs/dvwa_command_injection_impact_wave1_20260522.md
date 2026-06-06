> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# DVWA Command Injection Impact Wave 1

Status: completed / verified command execution + lab marker file proof; callback blocked
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> Docker-backed DVWA on `<victim-vm>`
Visible model/runtime: current Hermes session; no Claude/Codex worker usage artifact

## Target / scope

- Target: `http://<lab-ip>:18080`
- Victim: `<victim-vm>`
- Tester: `<attacker-vm>`
- Container: `vulnerables/web-dvwa:latest`, temporary container `dvwa-impact-lab`
- Vulnerability class: command injection
- Artifact run: `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T052046Z/`

## Verified impact

The single vulnerability was used to execute OS commands in the DVWA container context.

Evidence file:

`<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T052046Z/http/command_injection_response.html`

Verified output excerpt:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data
DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T052046Z
```

This proves:

1. Command execution reached the server-side OS command context.
2. Execution identity was `www-data`.
3. A lab-only marker file was written/read back:
   `/tmp/DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T052046Z.txt`

## Callback result

Callback was attempted in the first run via host-only callback pattern, but not verified:

- Aggressive-lab high port callback: blocked/unreachable from target/container.
- Windows host callback port `<lab-ip>:18182`: blocked/unreachable from aggressive-lab test.

Therefore callback remains a blocker and was not promoted as verified impact.

Next callback lane should use a Docker-published callback container on victim/attacker side, or explicitly open a host-only callback port with operator-approved firewall change.

## Restore / cleanup

- Temporary `dvwa-impact-lab` container was removed after the successful run.
- `juice-shop-lab` was restored and returned HTTP 200 after the earlier port experiment.
- Existing `webgoat-lab` and `juice-shop-lab` were left running.

## Boundaries

- Authorized local lab only.
- Single vulnerability: command injection.
- Lab marker file under `/tmp` only.
- No persistence.
- No credential theft.
- No OS destruction.
- No public/external target.
- No report/finding promotion.

## Project benefit

- Establishes the first lab flow that demonstrates real server-side command execution identity, not just app-layer state change.
- Moves the project closer to the operator's preferred max-impact training model while keeping evidence recoverable and lab-contained.
- Separates verified impact (`id`, `whoami`, marker file) from unverified impact (`callback`) instead of overstating results.
- Shows that Docker-published services bypass the host firewall where host processes do not; future callback/control drills should use Docker-published listener patterns.

## Added / changed

- Added `scripts/labs/dvwa_command_injection_impact_wave1.sh`.
- Added this handoff.
- Added bundle `modules/bundles/verified_lab_flow_dvwa_command_injection_container_control.md`.
- Added Obsidian lab note.
- Updated `accepted_changes.md`, `active_strategy_queue.md`, and `scripts/SCRIPT_INVENTORY.md`.
