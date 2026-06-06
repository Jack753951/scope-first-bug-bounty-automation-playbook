> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Kali VM as Default Tool Lab

Status: active
Source: User + Hermes
Date: 2026-05-20
Repo truth: `.hermes.md`, this handoff note

## Purpose

Use the Kali VM as the default tool lab for cybersecurity tooling and any target-touching or website-touching security work. Windows remains the coordination and repo/handoff surface unless Hermes Agent is deliberately moved into Kali.

## Current known Kali connection

- Kali VM IP: `<lab-ip>`
- SSH user: `kali`
- SSH port: `22`
- Network reachability from Windows: confirmed by ping
- SSH service reachability from Windows: port 22 open
- Authenticated SSH shell: established from Windows/Hermes using the Windows ED25519 key
- Verified tools on Kali: `nmap`, `curl`, `python3`, `git`
- Verified project paths on Kali: `/mnt/hacking` and `/home/kali/projects/cybersec`
- Windows OpenSSH config caveat: `<user-home>\.ssh\config` currently has a UTF-8 BOM parse issue; use `-F <empty config file>` or `-F /dev/null` until fixed

## Default routing rule

Use Kali by default for:

- `nmap`, `nuclei`, `subfinder`, `httpx`, `ffuf`, `gobuster`, `nikto`, `sqlmap`, Burp-related helpers, packet/security tools
- Curling or probing live websites, TryHackMe boxes, HackTheBox boxes, PortSwigger labs, bug-bounty assets, or other target-touching endpoints
- Downloading challenge/lab artifacts from security platforms when analysis tooling is expected to run on Kali
- Any active scan, fuzz, exploit validation, callback, brute force, or payload execution that is authorized and in scope

Keep on Windows by default for:

- Repo edits, handoff files, planning notes, report drafting, and static document work
- Browser screenshots and UI explanation
- Offline analysis that does not need Kali tools
- Coordination between Hermes, Claude/Cowork, Codex, and project handoff files

Authorization gates still apply regardless of environment. Do not run target-touching activity unless scope is local lab, CTF/training, user-owned, written client authorization, or explicit bug-bounty scope.

## Quick connection checks from Windows Git Bash

Use these from `<private-workspace>` or any Windows Git Bash shell.

```bash
ping -n 2 <lab-ip>
```

Check SSH port without relying on broken SSH config:

```bash
timeout 3 bash -c '</dev/tcp/<lab-ip>/22' && echo 'SSH open' || echo 'SSH closed'
```

Try interactive login:

```bash
ssh -F /dev/null kali@<lab-ip>
```

Try one-shot command after password/key works:

```bash
ssh -F /dev/null kali@<lab-ip> 'hostname; whoami; pwd; uname -a; command -v nmap; command -v curl; command -v python3'
```

## Fix Windows SSH config BOM issue

Symptom:

```text
<user-home>/.ssh/config: line 1: Bad configuration option: \357\273\277host
```

Cause: `<user-home>\.ssh\config` starts with a UTF-8 BOM before `Host`.

Safe manual fix options:

1. Open the file in VS Code / Notepad++.
2. Re-save as `UTF-8` without BOM.
3. Ensure the first visible characters of the file are exactly:

```sshconfig
Host lab
```

Temporary workaround until fixed:

```bash
ssh -F /dev/null kali@<lab-ip>
```

Optional alias after fixing config:

```sshconfig
Host kali-vm
    HostName <lab-ip>
    User kali
    Port 22
    StrictHostKeyChecking accept-new
```

Then use:

```bash
ssh kali-vm
ssh kali-vm 'hostname; whoami; uname -a'
```

## Recommended persistent SSH-key setup

Once interactive password login works, set up key-based login so Hermes can run Kali commands non-interactively.

From Windows Git Bash:

```bash
test -f ~/.ssh/id_ed25519.pub || ssh-keygen -t ed25519 -C 'owner-windows-to-kali' -f ~/.ssh/id_ed25519
```

If `ssh-copy-id` exists:

```bash
ssh-copy-id -F /dev/null kali@<lab-ip>
```

If `ssh-copy-id` is not available, manual method:

```bash
PUBKEY="$(cat ~/.ssh/id_ed25519.pub)"
ssh -F /dev/null kali@<lab-ip> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && printf '%s\n' '$PUBKEY' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

Verify non-interactive login:

```bash
ssh -F /dev/null -o BatchMode=yes kali@<lab-ip> 'hostname; whoami; pwd'
```

Expected result should show Kali hostname, user `kali`, and no password prompt.

## Standard Hermes operating pattern

Before target-touching work:

1. Confirm scope/authorization.
2. Confirm Kali is reachable.
3. Run target-touching command through SSH on Kali, not directly on Windows.
4. Save outputs into project-safe locations, avoiding secrets/loot in chat or global memory.
5. Bring back summaries/evidence paths into Windows handoff/report files.

Example pattern:

```bash
ssh -F /dev/null kali@<lab-ip> 'cd /mnt/hacking 2>/dev/null || cd ~/projects/cybersec; pwd; ./recon.sh --help'
```

If `/mnt/hacking` is not mounted in Kali, use a Kali-local project path such as:

```bash
~/projects/cybersec
```

## Future ideal state

Preferred final setup:

- Full Hermes Agent installed directly in Kali VM with a distinct alias such as `hai`
- Repo wrapper `bin/hermes` remains project-local and distinct from full Hermes Agent
- Shared repo mounted in Kali, ideally `/mnt/hacking` or `~/projects/cybersec`
- Website/security interactions default to Kali-side tools
- Windows remains useful for orchestration, screenshots, notes, and handoff review

## Troubleshooting checklist

If Kali is not reachable:

```bash
ping -n 2 <lab-ip>
```

If ping works but SSH fails:

```bash
timeout 3 bash -c '</dev/tcp/<lab-ip>/22' && echo open || echo closed
```

On Kali console, check:

```bash
ip addr
sudo systemctl status ssh
sudo systemctl start ssh
```

If SSH says permission denied:

- Confirm username is `kali`.
- Confirm password works interactively.
- Set up SSH key and verify `authorized_keys` permissions.

If SSH config errors before connecting:

- Use `ssh -F /dev/null ...` temporarily.
- Re-save `<user-home>\.ssh\config` without BOM.
