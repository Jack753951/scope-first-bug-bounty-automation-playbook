> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# VirtualBox Kali Lab Ops from Git-Bash

Session-derived checklist for managing a Kali VirtualBox lab from a Windows host when the agent terminal is Git-Bash/MSYS.

## Enable bidirectional clipboard / drag-and-drop at runtime

Use the native VBoxManage executable by absolute path; it may not be on PATH in Git-Bash:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' list runningvms
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' clipboard mode bidirectional
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' draganddrop bidirectional
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' showvminfo '<lab-vm>' --machinereadable | grep -E 'clipboard|draganddrop'
```

Expected verification:

```text
clipboard="bidirectional"
draganddrop="bidirectional"
```

If clipboard still does not work inside Kali, start/restart the guest clipboard client or reboot the guest:

```bash
VBoxClient --clipboard
```

## Shared folder permission/remount triage inside Kali

Symptoms:

```text
ls: cannot open directory '/media/sf_hacking': Permission denied
bash: /media/sf_hacking/...: Permission denied
```

Checks/fixes:

```bash
id
sudo usermod -aG vboxsf kali
sudo reboot
```

If the user is already in `vboxsf` but access still fails, remount the shared folder:

```bash
sudo umount /media/sf_hacking
sudo mount -t vboxsf hacking /media/sf_hacking
ls -la /media/sf_hacking
```

If `/media/sf_hacking` remains problematic, mount to a clean path:

```bash
sudo mkdir -p /mnt/hacking
sudo mount -t vboxsf hacking /mnt/hacking
ls -la /mnt/hacking
```

## Kali lab setup script pitfalls

When a setup script needs apt/systemctl/docker operations, run it with sudo rather than answering GUI PolicyKit prompts:

```bash
sudo bash /tmp/phase4a_kali_lab_setup.sh
```

If Kali already provides Docker Compose as `docker compose` / `docker-compose` but `docker-compose-plugin` has no apt candidate, skip that optional plugin install. Avoid partially commenting an if/else block: either replace the entire block with a single log line, or comment the matching `if`, `else`, and `fi` consistently. Validate before execution:

```bash
nl -ba /tmp/phase4a_kali_lab_setup.sh | sed -n '20,45p'
bash -n /tmp/phase4a_kali_lab_setup.sh
```

After a sudo-run setup, verify whether the intended non-root user was added to the docker group. If not:

```bash
sudo usermod -aG docker kali
sudo reboot
id
docker images
```

## VirtualBox `<inaccessible>` VM with snapshot/differencing disk errors

When `VBoxManage list vms` shows a lab VM as `"<inaccessible>" {uuid}`, distinguish a missing VM from a broken snapshot/medium chain before attempting repair.

Read-only triage from Git-Bash/MSYS:

```bash
VBOX='/c/Program Files/Oracle/VirtualBox/VBoxManage.exe'
"$VBOX" list vms
"$VBOX" showvminfo <uuid-or-name> --machinereadable > setting/local/vbox_showvminfo.txt 2>&1 || true
```

Then inspect host-side registry and service logs:

- `C:\Users\<user>\.VirtualBox\VirtualBox.xml` for the `MachineEntry` path.
- `C:\Users\<user>\.VirtualBox\VBoxSVC.log*` for errors around the VM name/UUID.
- The VM `.vbox` file for `currentSnapshot`, `aborted="true"`, `MediaRegistry`, and the currently attached disk image.
- The VM `Logs\VBox.log*` for last states such as `LiveSnapshotting`, `OnlineSnapshotting`, `Saving state`, `aborted`, or power loss.

A durable failure pattern is:

```text
Hard disk '...Snapshots/{parent}.vdi' ... cannot be directly attached ... because it has 1 differencing child hard disks
E_ACCESSDENIED / The object functionality is limited
```

Interpretation: the VM hardware attachment points at a parent differencing disk while VirtualBox still knows that disk has a child. This usually means a live snapshot / save-state / shutdown was interrupted, leaving the snapshot chain inconsistent. Do not treat this as an SSH/IP problem, and do not immediately hand-edit `.vbox`.

Safe handling order:

1. Do not unregister, delete, discard snapshots, or edit XML during initial triage.
2. Record evidence in a handoff file: registry entry, `.vbox` path, disk existence, chain mismatch, and relevant VBoxSVC/VBox.log excerpts.
3. Identify usable alternate VMs with `showvminfo --machinereadable` and `guestproperty enumerate <vm>`; note power state, host-only/NAT NICs, snapshots, and last guest IP evidence.
4. Prefer cloning/renaming a healthy base VM into a replacement attacker/victim VM over repairing the broken VM in place.
5. If recovering the broken VM matters, make an offline copy first, then use VirtualBox GUI/CLI snapshot clone/repair. Manual registry/XML editing is a last resort.

## Clone a healthy Kali attacker replacement

When the broken VM is an attacker box and repo artifacts are already preserved outside the guest, make the new VM the mainline and keep the old one as a forensic archive until the replacement is proven.

Read-only precheck:

```bash
VBOX='/c/Program Files/Oracle/VirtualBox/VBoxManage.exe'
"$VBOX" list vms
"$VBOX" showvminfo 'kali-linux-2026.1-virtualbox-amd64' --machinereadable | grep -E '^(name|VMState|nic[0-9]|cableconnected[0-9]|hostonlyadapter[0-9])='
```

Clone and register, then force a safe default before first boot:

```bash
"$VBOX" clonevm 'kali-linux-2026.1-virtualbox-amd64' --name '<lab-vm>' --register
"$VBOX" modifyvm '<lab-vm>' \
  --nic1 hostonly --hostonlyadapter1 'VirtualBox Host-Only Ethernet Adapter' --cableconnected1 on \
  --nic2 null --cableconnected2 off
"$VBOX" startvm '<lab-vm>' --type headless
```

Verify with host-side guest properties and SSH. Guest properties can show stale values immediately after cloning/boot; wait for a fresh timestamp or confirm with an SSH port probe and an in-guest `ip -brief addr`.

```bash
"$VBOX" guestproperty enumerate '<lab-vm>' | grep -E 'GuestInfo/Net/[0-9]/(Name|Status|V4/IP)|GuestInfo/Net/Count'
ssh -F /dev/null -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no kali@<lab-ip> 'ip -brief addr; ip route'
```

Use `ssh -F /dev/null` or a project-local empty config when the user's Windows OpenSSH config may have a BOM or other parse issue; do not let a host SSH config problem mask a working lab VM.

## Temporary NAT recovery window for lab tools

If the user authorizes NAT to restore tools, open NAT only for setup/downloads, verify internet inside Kali, run the recovery commands, then close NAT and verify no default route/internet remains.

Runtime VirtualBox 7.x NIC operations use `controlvm nicN` and `controlvm setlinkstateN`; `controlvm cableconnectedN` is invalid:

```bash
VBOX='/c/Program Files/Oracle/VirtualBox/VBoxManage.exe'
"$VBOX" controlvm '<lab-vm>' nic2 nat
"$VBOX" controlvm '<lab-vm>' setlinkstate2 on
ssh -F /dev/null kali@<lab-ip> 'ip -brief addr; ip route; timeout 8 curl -Is https://example.com | head -1'
```

Tool-recovery check pattern:

```bash
ssh -F /dev/null kali@<lab-ip> '
for t in docker docker-compose curl wget git jq nmap whatweb nikto python3 ffuf nuclei chromium sqlmap go arjun dalfox xsstrike; do
  printf "%s=" "$t"; command -v "$t" || echo missing
done
sudo -n true >/dev/null 2>&1 && echo sudo_nopasswd=yes || echo sudo_nopasswd=no
'
```

If sudo is not passwordless, do not guess or pipe the password. Write a short setup script into the shared project folder or `/tmp`, ask the user to run it inside Kali with `sudo bash /tmp/<script>.sh`, and resume after they report completion. Prefer installing distro-packaged baseline tools first (`docker.io`, `docker-compose`, `curl`, `wget`, `git`, `jq`, `nmap`, `whatweb`, `nikto`, `python3`, `python3-pip`, `ffuf`, `nuclei`, `chromium`, `sqlmap`, `golang-go`) and make language-specific helpers such as Arjun best-effort unless the next task requires them.

After recovery, close NAT and verify isolation before changing hardware or creating the clean snapshot:

```bash
"$VBOX" controlvm '<lab-vm>' nic2 null
"$VBOX" controlvm '<lab-vm>' setlinkstate2 off || true
ssh -F /dev/null kali@<lab-ip> 'ip route; timeout 5 curl -Is https://example.com >/dev/null 2>&1 && echo internet_open || echo internet_closed_or_blocked'
```

For CPU/RAM changes, power off first; `modifyvm --memory/--cpus` will not reliably apply to a running VM. Prefer a graceful ACPI shutdown, wait for `VMState="poweroff"`, then modify, snapshot, and boot/verify the visible resources:

```bash
"$VBOX" controlvm '<lab-vm>' acpipowerbutton || true
for i in $(seq 1 60); do
  state=$("$VBOX" showvminfo '<lab-vm>' --machinereadable | awk -F= '/^VMState=/{gsub(/"/,"",$2); print $2}')
  [ "$state" = poweroff ] && break
  sleep 5
done

"$VBOX" modifyvm '<lab-vm>' --memory 4096 --cpus 4 \
  --nic1 hostonly --hostonlyadapter1 'VirtualBox Host-Only Ethernet Adapter' --cableconnected1 on \
  --nic2 null --cableconnected2 off

"$VBOX" snapshot '<lab-vm>' take 'clean-attacker-v2-tools-4096m-4cpu-YYYYMMDD' \
  --description 'Host-only attacker baseline after tool recovery; NAT closed; old aggressive VM retained as forensic archive.'

"$VBOX" startvm '<lab-vm>' --type headless
ssh -F /dev/null kali@<lab-ip> 'free -m | head -2; nproc; ip route; timeout 5 curl -Is https://example.com >/dev/null 2>&1 && echo internet_open || echo internet_closed_or_blocked; docker --version; docker compose version || docker-compose --version'
```

Record the route transition in handoff docs: new attacker VM name/UUID/IP, NAT open/close evidence, installed tool summary, CPU/RAM settings, snapshot name/UUID, and that the old `<inaccessible>` VM was not deleted.

## Baseline lab verification pattern

For a local vulnerable-lab baseline, expected evidence includes:

```bash
ls -la ~/phase4a-lab
~/phase4a-lab/verify-setup.sh
docker images
```

Useful success indicators:

- `~/phase4a-lab` contains `run-dvwa.sh`, `run-juice-shop.sh`, `run-webgoat.sh`, `verify-setup.sh`, and `logs/`.
- Images exist for `bkimminich/juice-shop`, `vulnerables/web-dvwa`, and `webgoat/webgoat`.
- Tools resolve: `docker`, `curl`, `wget`, `git`, `jq`, `nmap`, `whatweb`, `nikto`, `python3`.

Security reminder: snapshot after setup, then use only authorized/local lab targets unless the project scope gate explicitly allows more.
