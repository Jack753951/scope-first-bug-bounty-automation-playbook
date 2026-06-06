> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Windows-to-Kali default tool-lab setup

Use when a Windows-hosted Hermes session should delegate cybersec tooling and target/lab interaction to a Kali VM while Windows remains the orchestration/repo control plane.

## Goal

- Windows/Hermes: chat, repo edits, handoff, Obsidian, screenshots, final synthesis.
- Kali VM: authorized security tooling, CTF/lab target interaction, Linux-native curl/wget/proxy/Burp workflows.
- Scope gate still applies before active scans, exploit validation, fuzzing, brute force, callbacks, or any target-touching automation.

## Connectivity checklist

1. Confirm VM networking from Windows:
   - ping VM IP
   - check TCP 22 with a short `/dev/tcp` or PowerShell `Test-NetConnection`
2. Confirm SSH username with the operator.
3. If normal SSH fails before connecting because Windows `~/.ssh/config` has a UTF-8 BOM or bad config option, do not conclude the VM is unreachable. Bypass user config with an empty config file:
   - PowerShell: create `$env:TEMP\empty_ssh_config` and call `ssh -F "$EmptySshConfig" ...`
   - Git-Bash: call `ssh -F /dev/null ...`
4. Establish key-based auth from Windows to Kali:
   - generate Windows-side ED25519 key if missing
   - append the Windows public key as a new line in Kali `~/.ssh/authorized_keys`
   - set Kali permissions: `chmod 700 ~/.ssh`, `chmod 600 ~/.ssh/authorized_keys`
   - test with `BatchMode=yes`, `IdentitiesOnly=yes`, and explicit `-i`
5. Verify remote lab basics:
   - `hostname`, `whoami`, `pwd`, `uname -a`
   - `command -v nmap curl python3 git`
   - project mount paths if the repo is shared into Kali

## PowerShell pattern

Use PowerShell syntax, not Bash syntax, when the user is in `PS C:\...`:

```powershell
$EmptySshConfig = "$env:TEMP\empty_ssh_config"
New-Item -ItemType File -Force $EmptySshConfig | Out-Null

if (!(Test-Path "$env:USERPROFILE\.ssh\id_ed25519.pub")) {
    ssh-keygen -t ed25519 -C "owner-windows-to-kali" -f "$env:USERPROFILE\.ssh\id_ed25519"
}

ssh -F "$EmptySshConfig" -o BatchMode=yes -o IdentitiesOnly=yes -i "$env:USERPROFILE\.ssh\id_ed25519" kali@<KALI_IP> "hostname; whoami; pwd"
```

Do not give Bash-only `test -f ... || ...` commands to a PowerShell prompt.

## Public-key transfer options

If password-based `ssh-copy-id` is awkward or repeatedly fails:

1. Copy the Windows public key to clipboard:
   ```powershell
   Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | Set-Clipboard
   ```
2. In Kali, edit `~/.ssh/authorized_keys` and append the key as a new line.
3. Preserve existing keys; never overwrite the file unless intentionally rebuilding it.

If the Kali VM is in VirtualBox and the user needs paste support, enable bidirectional clipboard/drag-and-drop with VBoxManage for the running VM, then retry paste. This is a usability step, not a security boundary.

## Verification / default command shape

After setup, run Kali commands through SSH explicitly and change into the shared repo when appropriate:

```bash
ssh -F /dev/null -o BatchMode=yes -o IdentitiesOnly=yes -i "$HOME/.ssh/id_ed25519" kali@<KALI_IP> 'cd /mnt/hacking && hostname; whoami; command -v nmap curl python3 git'
```

If a project wrapper exists, prefer that wrapper, but still verify that it reaches Kali rather than the Windows Git-Bash host.

For offensive/local-lab verified-flow work, make this routing explicit in the task prompt and tool checks, and treat it as a strict default when the user has configured `<lab-vm>`:

```text
Windows/Hermes = control plane for repo edits, handoff, Obsidian, final synthesis
Kali = target-touching tool plane for curl/probing, scanners, browser/runtime checks, exploit-flow attempts, and aggressive/destructive local-lab tests
```

Windows direct target contact is only a quick reachability/emergency fallback. If you use it, label it as an exception and do not let it replace the Kali-side run.

Before marking `ffuf`, `nikto`, `nmap`, `sqlmap`, Chromium, Burp-style workflows, or similar tooling as unavailable, run `command -v` on Kali through the wrapper/SSH path. A synchronous worker inheriting the Windows workdir or PATH is a routing issue, not a durable tool blocker.

## Pitfalls

- A reachable SSH port is not the same as authenticated access.
- Do not store passwords, private keys, or copied public-key material in memory, handoff, or skill files.
- Do not record the full live SSH command with private target/client details in global memory; put project-specific connection facts in repo handoff if needed.
- Do not treat setting up Kali access as approval for target-touching work; scope and authorization are separate gates.
- Do not let Windows-host tool availability drive conclusions for Kali-lab work. Verify tools from Kali first, then pull artifacts back to the repo/handoff layer.
