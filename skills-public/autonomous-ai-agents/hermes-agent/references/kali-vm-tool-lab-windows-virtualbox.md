> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Kali VM Tool Lab from Windows / VirtualBox

Use this reference when the user wants Windows-hosted Hermes to default to a Kali VM for security tooling, lab interaction, or target-touching work.

## Routing rule

- Windows host: orchestration, repo edits, handoff files, screenshots, report drafting, non-target offline analysis.
- Kali VM: security tools and target-touching interaction such as TryHackMe/HTB/PortSwigger labs, bug-bounty probing, `nmap`, `nuclei`, `subfinder`, `httpx`, `ffuf`, `curl` against live targets, exploit validation, and packet/security tooling.
- Authorization/scope gates still apply before any active scan, fuzz, exploit, brute force, callback, or target-touching automation.

## Connectivity checks from Windows Git Bash

```bash
ping -n 2 <KALI_IP>
timeout 3 bash -c '</dev/tcp/<KALI_IP>/22' && echo 'SSH open' || echo 'SSH closed'
ssh -F /dev/null kali@<KALI_IP> 'hostname; whoami; pwd; uname -a'
```

Use `-F /dev/null` when the user's Windows `~/.ssh/config` is malformed or has a UTF-8 BOM.

## PowerShell equivalents

PowerShell 5 does not support bash syntax like `test -f ... || ...`. Use:

```powershell
$EmptySshConfig = "$env:TEMP\empty_ssh_config"
New-Item -ItemType File -Force $EmptySshConfig | Out-Null

if (!(Test-Path "$env:USERPROFILE\.ssh\id_ed25519.pub")) {
    ssh-keygen -t ed25519 -C "owner-windows-to-kali" -f "$env:USERPROFILE\.ssh\id_ed25519"
}

ssh -F "$EmptySshConfig" -o BatchMode=yes -o IdentitiesOnly=yes -i "$env:USERPROFILE\.ssh\id_ed25519" kali@<KALI_IP> "hostname; whoami; pwd"
```

If `$EmptySshConfig` is unset, OpenSSH may report `Can't open user config file -o`; recreate the variable and quote `-F "$EmptySshConfig"`.

## Adding the Windows key to Kali manually

When password login or quoting is troublesome:

1. On Windows PowerShell:

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | Set-Clipboard
```

2. On Kali:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.bak.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
nano ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Append the Windows public key as one complete line. Do not overwrite existing keys.

## VirtualBox shared clipboard

If copy/paste into the Kali VM is needed and VirtualBox is installed on Windows:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' list runningvms
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<VM_NAME>' clipboard mode bidirectional
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<VM_NAME>' draganddrop bidirectional
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' showvminfo '<VM_NAME>' --machinereadable | grep -E 'clipboard|draganddrop'
```

VirtualBox 7 uses `controlvm <vm> clipboard mode bidirectional`; the older-looking `controlvm <vm> clipboard bidirectional` form is invalid.

## Repo handoff, not global memory

For project-specific Kali IPs, usernames, and operating policy, write a repo handoff note and store at most a compact global memory pointer. If the user has asked to use memory-routing discipline, load `multi-project-memory-routing` before saving durable details.
