> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A Kali VM lab setup pattern

Use this when preparing an isolated Kali/VirtualBox lab for controlled Phase 4A calibration or more aggressive script testing.

## Class-level lesson

Do not treat lab hardening as a one-way "turn everything off immediately" step. Split the VM lifecycle into two modes:

1. Setup mode
   - NAT may stay enabled so the guest can run `apt update`, install Docker/tools, and pull vulnerable-app images.
   - Host-only/Internal networking may also be enabled for later attacker/victim traffic.
   - Shared folders should be minimized; if present, prefer read-only and avoid mounting the main repo into a VM that will run destructive/RCE tests.
   - Clipboard, drag-and-drop, and file-transfer clipboard should normally stay disabled unless the operator explicitly asks for a short-lived setup/control convenience state.

2. Setup-control mode
   - Use when the operator needs to control or configure the victim/lab VM interactively: copy commands, repair scripts, mount shared folders, or start vulnerable apps.
   - NAT may remain enabled, host-only should remain enabled, and a known snapshot such as `setup-complete-with-tools` should exist.
   - It is acceptable to temporarily enable bidirectional clipboard and drag-and-drop for setup convenience, but keep clipboard file transfer off and state clearly that this is not aggressive/isolated attack mode.
   - Before moving to aggressive testing, disable NAT if not required, remove or narrow writable shared folders, and turn clipboard/drag-and-drop back off.

3. Attack/aggressive-test mode
   - Disable NAT or other internet egress unless the lab scope explicitly requires it.
   - Use host-only or internal networks between attacker and victim VMs.
   - Remove shared folders or keep a narrow read-only exchange folder only.
   - Take/revert snapshots around tests.

The user may correctly object if you recommend disabling NAT before tool downloads; acknowledge setup mode first, then switch to isolated mode after the tool/image snapshot.

## Recommended VirtualBox sequence

1. Clone or create the lab VM.
2. Verify VM state and network:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' list runningvms
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' showvminfo '<vm>' --machinereadable | grep -E '^(VMState=|nic[0-9]=|hostonlyadapter[0-9]=|natnet[0-9]=|clipboard=|draganddrop=|SharedFolderNameMachineMapping[0-9]=|SharedFolderPathMachineMapping[0-9]=)'
```

3. Set convenience channels according to mode.

Default safer setup/attack posture:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm>' clipboard mode disabled
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm>' clipboard filetransfers off
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm>' draganddrop disabled
```

Temporary setup-control posture when the operator explicitly wants to paste commands/control the lab VM:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm>' clipboard mode bidirectional
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm>' clipboard filetransfers off
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<vm>' draganddrop bidirectional
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' showvminfo '<vm>' --machinereadable | grep -E '^(VMState|clipboard=|clipboard_file_transfers=|draganddrop=|nic[0-9]=|cableconnected[0-9]=|hostonlyadapter[0-9]=|natnet[0-9]=|SharedFolderNameMachineMapping[0-9]=|SharedFolderPathMachineMapping[0-9]=|CurrentSnapshotName)'
```

For persistent settings while powered off, use `modifyvm`; if the VM is running/locked, use `controlvm` for runtime changes and repeat persistent hardening after shutdown:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' modifyvm '<vm>' --clipboard disabled --draganddrop disabled
```

4. In setup or setup-control mode, keep NAT enabled while installing tools and pulling images.
5. Take a snapshot such as `setup-complete-with-tools`.
6. For aggressive mode, power off and disable NAT:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' modifyvm '<vm>' --nic2 none
```

7. Take a pre-test snapshot such as `pre-aggressive-test`.

## Direct-control pitfall

Before telling the user you can install inside the VM, verify an actual control channel:

- SSH on host-only IP or explicit NAT port forward with a working SSH service and credentials; or
- VirtualBox Guest Additions `guestcontrol` with a known guest username/password.

VirtualBox showing the VM as running is not enough. `guestcontrol` can fail if credentials differ, and NAT guest properties may only show a `10.0.3.x` address while host-only IP is absent. If no control channel exists, create a setup script under a git-ignored local path and ask the user to run it inside the guest via shared folder or console.

## Setup script pattern

Create a local helper such as `setting/local/phase4a_kali_lab_setup.sh` that:

- runs `apt-get update`;
- installs baseline lab tools (`curl`, `wget`, `git`, `jq`, `nmap`, `whatweb`, `nikto`, `python3`, `pipx`, `docker.io`, Docker Compose if available);
- treats Docker Compose installation as a compatibility preflight, not a hard blocker: check `docker compose version` and `docker-compose --version` first, install `docker-compose`/`docker.io` when needed, and make any `docker-compose-plugin` attempt non-fatal because some Kali/Debian package sources provide Compose under a different package name;
- enables Docker;
- pulls local vulnerable-app images such as Juice Shop, DVWA, and WebGoat;
- creates small run wrappers under `~/phase4a-lab/` binding services to `127.0.0.1` by default;
- prints a reminder to snapshot before switching to isolated attack mode.

Keep the helper clearly bounded: setup/download only, no scans, no target interaction beyond pulling public images, and no exploit logic.

### Shared-folder execution troubleshooting

When a Kali console screenshot shows `~/phase4a-lab/verify-setup.sh: no such file or directory`, do not treat that as the root failure. It usually means the setup helper has not successfully run yet. Diagnose the helper path/mount first.

Use this sequence in the guest:

```bash
ls -la /media
ls -la /media/sf_hacking
ls -la /media/sf_hacking/setting
ls -la /media/sf_hacking/setting/local
sudo find /media -name 'phase4a_kali_lab_setup.sh' 2>/dev/null
```

Interpretation:

- `Permission denied` when running `bash /media/sf_hacking/.../phase4a_kali_lab_setup.sh` points to VirtualBox shared-folder membership/permissions or a stale/bad shared-folder mount. First check `id` for `vboxsf`; if the user is missing it, use `sudo usermod -aG vboxsf kali` and logout/reboot. If `id` already shows `vboxsf` but `ls -la /media/sf_hacking` still says permission denied, treat the mount as suspect and remount the shared folder before diagnosing the script.
- `No such file or directory` after adding `sudo` means the path is wrong, the shared folder is not mounted at that name, or the file was not copied to the expected location. Do not keep retrying the same path; list `/media` and use `find` to discover the actual path.
- If the shared folder exists but cannot be read despite correct group membership, remount it using the VirtualBox share name, then re-list it:

```bash
sudo umount /media/sf_hacking 2>/dev/null || true
sudo mkdir -p /media/sf_hacking
sudo mount -t vboxsf hacking /media/sf_hacking
ls -la /media/sf_hacking
```

If the share name is different, list `/media`/VirtualBox settings and substitute the correct name.

- If the file is visible only to root or shared-folder execution is unreliable, copy it to a guest-local temp path before running:

```bash
sudo cp /media/sf_hacking/setting/local/phase4a_kali_lab_setup.sh /tmp/phase4a_kali_lab_setup.sh
sudo chmod +x /tmp/phase4a_kali_lab_setup.sh
sudo bash /tmp/phase4a_kali_lab_setup.sh
```

If a copied helper still aborts on `docker-compose-plugin`, first prove Compose is already usable:

```bash
docker --version
docker compose version
docker-compose --version
```

When Compose is already present, patch the guest-local copy so the plugin install cannot abort the whole setup. Prefer targeting every plugin line, then inspect the result before re-running:

```bash
grep -n -C 3 'docker-compose-plugin' /tmp/phase4a_kali_lab_setup.sh
sed -i '/docker-compose-plugin/s/^/# skipped: /' /tmp/phase4a_kali_lab_setup.sh
grep -n -C 3 'docker-compose-plugin' /tmp/phase4a_kali_lab_setup.sh
bash /tmp/phase4a_kali_lab_setup.sh
```

If the plugin command is embedded in a more complex line and still runs, make that install non-fatal rather than continuing to retry the same failing package:

```bash
perl -0pi -e 's/(apt(-get)?\s+install[^\n]*docker-compose-plugin[^\n]*)/$1 || true/g' /tmp/phase4a_kali_lab_setup.sh
bash /tmp/phase4a_kali_lab_setup.sh
```

After the setup helper completes, then verify:

```bash
~/phase4a-lab/verify-setup.sh
```

### Bash patching pitfall: do not leave dangling `else`/`fi`

When skipping a Kali-incompatible `docker-compose-plugin` block manually, do not comment only the `if` and install lines. If the script has an `if ... then ... else ... fi` block, partial line comments can leave an orphaned `else` or `fi`, causing `bash -n` errors such as `syntax error near unexpected token 'else'`.

Inspect the block with line numbers before and after editing:

```bash
nl -ba /tmp/phase4a_kali_lab_setup.sh | sed -n '20,45p'
bash -n /tmp/phase4a_kali_lab_setup.sh
```

If the block is already partially commented and shows a bare `else`/`fi`, comment the matching control-flow remnants or replace the whole block with one log line:

```bash
sed -i '31s/^/# skipped: /;33s/^/# skipped: /' /tmp/phase4a_kali_lab_setup.sh
bash -n /tmp/phase4a_kali_lab_setup.sh
```

Prefer a future helper implementation that checks Compose availability first and avoids a plugin-install `if/else` block entirely.

### Privilege pitfall: run setup helpers with sudo

If a setup helper prints apt lock errors such as `Could not open lock file /var/lib/apt/lists/lock` or a PolicyKit popup says authentication is required to reload systemd state, cancel the GUI prompt and rerun the whole helper with sudo:

```bash
sudo bash /tmp/phase4a_kali_lab_setup.sh
```

Do not keep accepting piecemeal GUI authentication prompts; apt, Docker service enablement, and group changes need a consistent root context.

## Dual-Kali attacker/victim topology

For controlled lab calibration, use two VMs when possible:

- Attacker/red-team Kali: runs browsers, curl, Burp/security tools, and calibration scans only against explicit local lab targets.
- Victim/lab Kali: runs intentionally vulnerable containers such as Juice Shop, DVWA, and WebGoat.
- Windows host: remains the control plane for VirtualBox, Hermes, repo files, and snapshots.

It is safe to run both Kali VMs simultaneously if host CPU/RAM is sufficient, but verify roles and IPs every session:

```bash
ip -br addr
```

Typical addresses:

- Windows host-only adapter: `<lab-ip>`
- Victim Kali host-only: e.g. `<lab-ip>`
- Attacker Kali host-only: e.g. `<lab-ip>`
- NAT adapters: often `10.0.3.x`
- Docker bridge inside victim: `172.17.0.1/16`

If the attacker Kali has NAT but no `192.168.56.x` address, check VirtualBox host-only DHCP. Some labs have host-only DHCP disabled, so assign a temporary static host-only IP inside the attacker guest:

```bash
sudo ip addr add <lab-ip>/24 dev eth0
sudo ip link set eth0 up
ping -c 3 <lab-ip>
```

If ping works but HTTP to the vulnerable app fails, separate network reachability from service binding:

- `ping` success means L3 host-only path works.
- `curl http://<victim-hostonly-ip>:3000` failure often means the Docker container is bound only to victim-local `127.0.0.1`.

On the victim Kali, inspect the published port:

```bash
sudo docker ps
sudo ss -ltnp | grep ':3000'
```

If `PORTS` or `ss` shows `127.0.0.1:3000`, restart Juice Shop bound to all victim interfaces for red-team access over host-only:

```bash
sudo docker ps -q --filter ancestor=bkimminich/juice-shop | xargs -r sudo docker rm -f
sudo docker run -d --name juice-shop-lab -p 0.0.0.0:3000:3000 bkimminich/juice-shop
curl -I http://127.0.0.1:3000
curl -I http://<lab-ip>:3000
```

Then test from attacker Kali:

```bash
curl -I http://<lab-ip>:3000
```

Keep this limited to local intentionally vulnerable apps. Before aggressive testing, switch from setup-control mode to isolated attack mode: disable NAT if not required, remove or narrow shared folders, and turn off clipboard/drag-and-drop.

## Suggested first lab images

- `bkimminich/juice-shop:latest` for modern bug-bounty-like web flow calibration.
- `vulnerables/web-dvwa:latest` for basic web vulnerability loops.
- `webgoat/webgoat:latest` for structured training.

## Safety wording

For Phase 4A, frame this as lab calibration rather than real bug-bounty activation. Automation output remains candidate-only, and aggressive behaviors such as fuzzing, brute force, callbacks/OAST, RCE validation, reverse shells, destructive changes, proxy/pivot/tunnel behavior, or credential/loot handling still require explicit lab scope and operator approval.
