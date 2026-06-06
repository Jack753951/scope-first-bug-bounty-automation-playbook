> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# VirtualBox Kali NAT, Docker, and Attacker Callback Route

Use this reference for the cybersec lab route where Windows Hermes controls VirtualBox Kali VMs over SSH and the operator wants a true attacker-side callback listener.

## Scenario

- Windows Hermes is the control plane.
- `<lab-vm>` is the attacker/tester VM.
- `<lab-vm>` runs Docker-backed vulnerable targets.
- The operator prefers host-only/offline lab mode by default.
- NAT may be temporarily opened only for package/image pulls, then closed and verified.

## Preflight checks

From Windows/Git-Bash, use project-local SSH config/key to avoid broken user SSH config:

```bash
SSHCFG='<user-home>
KEY='<user-home>
KH='<user-home>
ssh -F "$SSHCFG" -i "$KEY" -o UserKnownHostsFile="$KH" kali@<lab-ip> \
  'set +e; hostname; uname -a; ip route; command -v docker || true; docker --version 2>&1 || true; groups; sudo -n true; echo sudo_nopass_exit=$?'
```

Interpretation:

- Docker absent means install is needed.
- `sudo -n true` failing means the user must type the sudo password inside the VM; do not guess or pass secrets through stdin.
- If NAT is off, DNS/curl to package sources will fail until NAT is opened.

## VirtualBox 7 runtime NAT window

Do not use `controlvm <vm> cableconnected2 on`; that is invalid for VirtualBox 7 runtime control. Use `nic2` and `setlinkstate2`:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' nic2 nat
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' setlinkstate2 on
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' showvminfo '<lab-vm>' --machinereadable | grep -E '^(nic2|cableconnected2)='
```

Expected machine-readable state:

```text
nic2="nat"
cableconnected2="on"
```

Inside the guest, NetworkManager may create `eth1` with a NAT address such as `10.0.3.15/24` and default route via `10.0.3.2`. Verify:

```bash
ip -br addr
ip route
ping -c 1 -W 3 1.1.1.1
curl -4 -I --max-time 8 https://download.docker.com
```

Close NAT after installation/pulls:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' nic2 null
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' setlinkstate2 off
```

Then verify no default Internet route remains while host-only SSH/lab connectivity still works.

## Kali Docker install path

On Kali rolling, `docker.io` may be available from Kali apt while `docker-compose-plugin` is not. Check first:

```bash
apt-cache policy docker.io docker-compose-plugin docker-compose
```

A user-run script inside `<lab-vm>` can be:

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
sudo docker --version
printf 'Log out/in or run newgrp docker, then verify: docker ps\n'
```

After group membership changes, the current shell may need:

```bash
newgrp docker
docker ps
docker --version
docker-compose --version
```

## Callback route verification

Before claiming true attacker-side callback:

1. run a disposable listener on `<lab-vm>` with Docker-published port bound to host-only reachability;
2. from `<lab-vm>`, curl the attacker host-only IP and port;
3. from the vulnerable target container, trigger callback;
4. copy listener logs to repo artifacts;
5. require the run marker in listener logs;
6. clean up the listener container;
7. close NAT if it was opened.

A Docker-bridge callback on victim-lab is useful but must be labeled `Docker-bridge local callback`, not true attacker-side callback.
