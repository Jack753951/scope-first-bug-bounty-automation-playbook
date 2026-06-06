> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A victim-lab SSH control and static IP pattern

Session-derived pattern for making a Kali victim VM controllable from the Windows/Hermes control plane while preserving host-only lab isolation.

## Situation

- VirtualBox victim VM is intentionally vulnerable lab infrastructure, not a public target.
- VM is on host-only networking, e.g. Windows host `<lab-ip>`, red-team Kali `<lab-ip>`, victim `<lab-ip>`.
- Host-only DHCP may be disabled, so the victim can boot with `eth0 UP` but no `192.168.56.x` address.
- Guest-reported `172.17.0.1` is commonly Docker bridge, not host-only reachability.
- Windows may block ICMP to `<lab-ip>`; failed ping to the host does not prove the lab is broken if TCP/HTTP works.

## Control-plane discovery

From Windows/Git-Bash, prefer VirtualBox plus SSH checks:

```bash
VB='/c/Program Files/Oracle/VirtualBox/VBoxManage.exe'
"$VB" list runningvms
"$VB" showvminfo '<lab-vm>' --machinereadable | sed -n '/^nic[1-4]=/p;/^hostonlyadapter[1-4]=/p;/^clipboard=/p;/^draganddrop=/p'
"$VB" guestproperty enumerate '<lab-vm>' | grep -E 'GuestInfo/Net/[0-9]+/V4/IP|GuestAdd'
ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no -F /dev/null kali@<lab-ip> 'hostname; ip -br addr'
```

Use `curl -I --max-time 5 http://<victim-ip>:3000` or a TCP socket check to validate the lab app; do not rely only on ping.

## One-time static IP setup inside victim

If SSH works after a temporary manual IP assignment, upload a helper and have the operator run it once with sudo in the victim console. Do not guess or pipe the Kali sudo password.

Known-good helper:

```bash
#!/usr/bin/env bash
set -euo pipefail
CONN='eth0'
IP='<lab-ip>/24'
IFACE='eth0'

nmcli -f NAME,UUID,TYPE,DEVICE connection show
sudo nmcli connection modify "$CONN" \
  connection.interface-name "$IFACE" \
  ipv4.method manual \
  ipv4.addresses "$IP" \
  ipv4.gateway '' \
  ipv4.dns '' \
  ipv4.never-default yes \
  ipv6.method disabled \
  connection.autoconnect yes
sudo nmcli connection up "$CONN"
ip -br addr show "$IFACE"
nmcli -f ipv4.method,ipv4.addresses,ipv4.gateway,ipv4.never-default connection show "$CONN"
```

Expected verification:

```text
ipv4.method: manual
ipv4.addresses: <lab-ip>/24
ipv4.gateway: --
ipv4.never-default: yes
```

## Remote service control after static IP

Once the victim has a stable IP and key-based SSH, a repo-local `setting/local/victim-lab-control.sh` helper can safely manage lab services without scanning/exploitation:

- `status`: SSH/IP/container/HTTP readiness checks
- `start`: start `bkimminich/juice-shop` bound to the host-only IP
- `stop`: remove the lab container
- `restart`: restart and verify
- `logs`: tail lab app logs

Keep it under `setting/local/` because it is environment-specific and should remain git-ignored/local.

Example start command on the victim:

```bash
docker rm -f juice-shop-lab >/dev/null 2>&1 || true
docker run -d --name juice-shop-lab -p <lab-ip>:3000:3000 bkimminich/juice-shop
```

Wait a few seconds before declaring HTTP failure: the container can be `Up` before Juice Shop is listening.

## Pitfalls

- When generating a remote shell script from the host, quote heredocs so host-side variables do not expand into empty strings. Prefer creating a local file with `write_file` then `scp` it, or use `cat <<'SH'` carefully.
- On this Windows/Git-Bash setup, `scp /dev/stdin remote:path` may fail because `/dev/stdin` is not treated as a regular file. Use a real local temp/helper file and `scp` that.
- `sudo nmcli` requires operator input unless a very narrow sudoers rule exists. Do not enable broad `NOPASSWD: ALL`; prefer persistent NetworkManager config so no repeated sudo is needed.
- Do not treat Docker bridge IPs as host-only victim IPs.
- Do not add NAT for attack mode. Use NAT only in setup mode for image/package downloads, then snapshot and return to host-only isolation.
