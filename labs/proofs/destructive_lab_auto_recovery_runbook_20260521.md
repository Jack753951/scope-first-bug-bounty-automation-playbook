> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Destructive Lab Auto-Recovery Runbook

Status: active gate / local靶機 only
Date: 2026-05-21
Skill: `owasp-single-vuln-lab-wave`

## Scope

This runbook applies only to the disposable VirtualBox host-only lab:

```text
attacker VM: <attacker-vm> / <lab-ip>
victim VM: <victim-vm> / <lab-ip>
target URL: http://<lab-ip>:3000/
```

No public, client, or real bug-bounty target is covered by this runbook.

## Verified preconditions in this session

VirtualBox executable found:

```text
/c/Program Files/Oracle/VirtualBox/VBoxManage.exe
```

VMs found:

```text
kali-linux-2026.1-virtualbox-amd64
<victim-vm>
<attacker-vm>
```

Running VMs found:

```text
<victim-vm>
<attacker-vm>
```

Victim snapshots found:

```text
setup-complete-with-tools
pre-aggressive-current-running-recovery-20260521-093252
```

Attacker snapshot found:

```text
clean-before-aggressive-tests-20260521-093233
```

Attacker-to-victim health observed:

```text
HTTP/1.1 200 OK
```

Attacker route boundary observed:

```text
<lab-ip>/24 dev eth0 ...
no default route
```

## Destructive wave gate

Before any destructive/aggressive OWASP wave:

1. Write a wave-specific plan with:
   - target URL;
   - one OWASP class only;
   - expected impact;
   - kill condition;
   - request/rate/time caps;
   - pre/post health check;
   - artifact directory;
   - recovery command;
   - post-restore health check.
2. Confirm `VBoxManage.exe snapshot <victim-vm> list --machinereadable` still shows a recovery snapshot.
3. Confirm `curl -I http://<lab-ip>:3000/` from attacker still returns HTTP 200 before the run.
4. Run the wave.
5. If health degrades, planned damage occurs, or the script exits non-zero in a way that indicates target breakage:
   - record the breakage in the wave result;
   - restore victim snapshot;
   - restart victim if needed;
   - verify health returns to HTTP 200.

## Recovery command template

Use Git-Bash quoting from the Windows host:

```bash
VBOX='/c/Program Files/Oracle/VirtualBox/VBoxManage.exe'
"$VBOX" controlvm <victim-vm> poweroff || true
"$VBOX" snapshot <victim-vm> restore pre-aggressive-current-running-recovery-20260521-093252
"$VBOX" startvm <victim-vm> --type headless
```

Then verify from attacker VM:

```bash
MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/kali-run.ps1 -Command 'curl -sS -I --max-time 10 http://<lab-ip>:3000/ | head -n 1'
```

Expected:

```text
HTTP/1.1 200 OK
```

## Important limitation

Snapshot restore is intentionally not executed merely to prove the command during a normal planning turn because it disrupts the running lab. The destructive wave itself must treat restore as the automatic fallback after breakage. If strict proof is required before the first destructive run, create/restore a fresh throwaway victim snapshot in a separate setup slice first.

## Still prohibited

Even in destructive-lab mode:

- public/real bug-bounty/client targets;
- malware, stealth, persistence, evasion;
- credential theft or real secret exfiltration;
- uncontrolled DoS or propagation;
- callbacks/OAST/reverse shells unless a separate isolated callback lab is explicitly built;
- retention of raw secrets/loot;
- automatic confirmed/reportable finding promotion.
