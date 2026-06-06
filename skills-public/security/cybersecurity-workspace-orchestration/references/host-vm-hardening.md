> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Windows Host + Kali VM Hardening Pattern

Use this reference when the operator asks the agent to directly harden the Windows host / Kali VM lab environment without touching external targets.

## Safe agent-appliable actions

These are setup/hardening actions, not target-touching work:

- Inspect VirtualBox VM state and current settings with `VBoxManage showvminfo <vm> --machinereadable`.
- For a running VirtualBox Kali VM, disable host/guest transfer channels at runtime:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm-name>' clipboard mode disabled
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm-name>' clipboard filetransfers off
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm-name>' draganddrop disabled
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm-name>' nicpromisc1 deny
```

Notes:

- VirtualBox 7.x requires `clipboard mode disabled`; `clipboard disabled` and `clipboard disable` are invalid.
- `draganddrop disabled` is valid.
- `modifyvm` can fail while the VM is running/locked; use `controlvm` for runtime settings and repeat `modifyvm` after shutdown for persistent settings.
- A live snapshot may be possible and useful after runtime hardening; still explain that persistent VM settings should be applied while powered off.

## Windows host hardening checks

Low-risk user-scope setting:

```powershell
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name HideFileExt -Type DWord -Value 0
```

This makes Windows show file extensions, reducing disguised-executable risk.

Admin-dependent checks/settings may include Microsoft Defender PUA protection and Windows Firewall profiles. If the agent process is not elevated, report which settings were verified and provide an elevated PowerShell command for the operator rather than claiming full hardening was completed.

## Kali VM hardening helper pattern

When sudo is required inside Kali and the agent cannot safely provide an interactive password, create a git-ignored local helper script and ask the operator to run it manually in Kali, for example:

```bash
sudo bash /mnt/hacking/setting/local/hardening/apply_kali_hardening.sh
```

A good helper can:

- Install/enable `ufw`.
- Default deny inbound and allow outbound.
- Allow SSH only from the VirtualBox host-only subnet such as `<lab-ip>/24`.
- Add `/etc/ssh/sshd_config.d/99-cybersec-lab-hardening.conf` with key-only SSH, no root login, no X11 forwarding, and `AllowUsers kali`.
- Validate with `sshd -t`, reload SSH, and print `ufw status verbose` plus relevant `sshd -T` values.

Do not pipe guessed/default passwords into `sudo -S`. If the tool blocks `sudo -S`, treat that as a safety boundary and switch to an operator-run script or a pre-approved sudo mechanism.

## Convenience tradeoffs the user may request

The operator may choose convenience when it is bounded and explicit. Prefer the least-open setting that solves the workflow problem:

- If clipboard friction is the issue, set VirtualBox clipboard to `hosttoguest` rather than `bidirectional`:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm-name>' clipboard mode hosttoguest
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm-name>' clipboard filetransfers off
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm-name>' draganddrop disabled
```

Explain that this allows Windows -> Kali command copying while preventing Kali -> Windows clipboard flow, file-transfer clipboard, and drag-and-drop.

- If the user sometimes needs SSH password login, do not reopen root login or broad network exposure. Create an operator-run helper under `setting/local/hardening/` that sets:

```text
PasswordAuthentication yes
KbdInteractiveAuthentication yes
PermitRootLogin no
PubkeyAuthentication yes
X11Forwarding no
AllowUsers kali
```

Pair this with UFW restricted to the VirtualBox host-only subnet, e.g. `22/tcp ALLOW IN <lab-ip>/24`, and ask the operator to run the helper with sudo inside Kali. Verify Windows -> Kali SSH still works after the change. Avoid treating password SSH as ideal; present it as an accepted bounded convenience option for this user's lab.

## Verification summary to report

Report in four buckets:

1. Applied now: settings actually changed by the agent.
2. Verified now: existing Defender/Firewall/VM settings observed.
3. Helper created: local scripts placed under ignored `setting/local/...` paths.
4. Needs operator elevation/password: Kali sudo hardening or admin-only Windows policy changes.
