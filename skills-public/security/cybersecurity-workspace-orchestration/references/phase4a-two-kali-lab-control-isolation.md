> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A Two-Kali Lab Control/Isolation Notes

Use this when the operator is running a separated VirtualBox lab with one Kali as the red-team/operator VM and another Kali as the intentionally vulnerable lab/victim VM.

## Roles

- Windows host: control plane, Hermes/repo, VirtualBox management.
- Red-team Kali, e.g. `kali-linux-2026.1-virtualbox-amd64`: attacker/operator tooling.
- Victim Kali, e.g. `<lab-vm>`: intentionally vulnerable apps such as Juice Shop, DVWA, WebGoat.

## Setup/control mode

Victim VM can temporarily keep NAT, clipboard/drag-and-drop, and a shared folder while packages/images are being installed. After the vulnerable apps are pulled and a `setup-complete-with-tools` snapshot exists, switch the victim toward isolation before active testing.

Useful VirtualBox inspection commands from Git-Bash on Windows:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' list runningvms
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' showvminfo '<lab-vm>' --machinereadable | grep -E '^(VMState|nic[12]=|cableconnected[12]=|hostonlyadapter1=|natnet2=|clipboard=|clipboard_file_transfers=|draganddrop=|SharedFolderName|SharedFolderPath|CurrentSnapshotName)'
```

## Victim isolation mode

For the victim VM, keep host-only networking but disable external and host-integration channels:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' nic2 null
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' clipboard mode disabled
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' clipboard filetransfers off
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' draganddrop disabled
```

Expected victim posture:

- `nic1=hostonly` remains on so red-team Kali can reach the lab.
- `nic2=null` or otherwise no NAT for the victim.
- `clipboard=disabled`, `clipboard_file_transfers=off`, `draganddrop=disabled`.
- No writable host shared folder. Prefer no shared folder at all for strict testing.

## Host-only IP quirks

If VirtualBox Host-Only DHCP is disabled, a VM can have the host-only NIC attached but no `192.168.56.x` address. This is a configuration issue, not a routing failure. Manually assign a lab IP inside the red-team VM when needed:

```bash
sudo ip addr add <lab-ip>/24 dev eth0
sudo ip link set eth0 up
ping -c 3 <lab-ip>
```

Common addressing pattern:

- Windows host-only adapter: `<lab-ip>/24`
- Victim Kali: `<lab-ip>/24`
- Red-team Kali: `<lab-ip>/24`

## Localhost versus host-only service binding

If the vulnerable app is reachable from the victim as `http://127.0.0.1:3000` but not from red-team Kali as `http://<lab-ip>:3000`, inspect Docker port binding:

```bash
sudo docker ps
sudo ss -ltnp | grep ':3000'
```

A `127.0.0.1:3000->3000/tcp` binding is local-only. Recreate Juice Shop bound to the host-only interface/all interfaces:

```bash
sudo docker ps -q --filter ancestor=bkimminich/juice-shop | xargs -r sudo docker rm -f
sudo docker run -d --name juice-shop-lab -p 0.0.0.0:3000:3000 bkimminich/juice-shop
```

Then test from red-team Kali:

```bash
curl -I http://<lab-ip>:3000
whatweb http://<lab-ip>:3000
```

`curl http://127.0.0.1:3000` on red-team Kali is expected to fail unless the red-team VM itself is running the service.

## Shared-folder mapping caveat

VirtualBox can show both persistent machine mappings and runtime transient mappings. After removing the permanent mapping, check both:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' showvminfo '<lab-vm>' --machinereadable | grep -i 'sharedfolder' || true
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' showvminfo '<lab-vm>' | grep -E 'Shared folders|Name: .+hacking|Host path'
```

If `SharedFolderNameTransientMapping...` remains while the VM is running, `VBoxManage sharedfolder remove --transient` may report `VERR_FILE_NOT_FOUND` even though `showvminfo` still lists the transient share. Treat the safe closeout as:

1. Inside the victim guest, unmount the folder:

```bash
mount | grep hacking
sudo umount /mnt/hacking
# if busy:
cd ~
sudo umount /mnt/hacking
# last resort for this lab state:
sudo umount -l /mnt/hacking
```

2. Power off/restart the victim VM.
3. Re-check that no `SharedFolderNameMachineMapping` or `SharedFolderNameTransientMapping` remains.

A readonly transient share is less risky than a writable share, but strict attack/isolation mode should have no victim shared folder.
