> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A victim-lab host-only Juice Shop control

Use this reference when the operator is setting up or recovering a separate `<lab-vm>` VM that runs an intentionally vulnerable app while the red-team Kali VM performs bounded validation.

## Durable pattern

1. Inspect VirtualBox from the host/control plane first:
   - Confirm both red-team and victim VMs are running.
   - Confirm victim NIC posture: host-only adapter for attack/isolation mode; NAT only for setup/image pulls.
   - Check Host-only adapter address and DHCP state. If DHCP is disabled, expect the guest may have no `192.168.56.x` address.
   - Check the red-team Kali IP before suggesting a victim IP to avoid collisions.

2. If the victim guest shows host-only NIC `UP` but no IP:
   - Ask the operator to run inside the victim guest:
     ```bash
     ip -br addr
     ```
   - If the host-only interface is obvious and DHCP is off, assign a free static IP in the host-only subnet:
     ```bash
     sudo ip addr add <lab-ip>/24 dev eth0
     sudo ip link set eth0 up
     ip -br addr
     ```
   - Replace `eth0` with the actual host-only interface name. Avoid reusing the red-team VM IP.

3. Do not overinterpret failed ping to the Windows host-only address.
   - `ping <lab-ip>` may fail because Windows Firewall blocks ICMP.
   - Verify reachability with the actual service instead: TCP connect or HTTP `curl` from Windows host and red-team Kali.
   - If HTTP/TCP to the victim service succeeds, the host-only lab path is usable even when ICMP to Windows fails.

4. If the vulnerable app image is already present, keep victim isolated and avoid enabling NAT.
   - For OWASP Juice Shop:
     ```bash
     docker images | grep -i juice || true
     docker run --rm -p <lab-ip>:3000:3000 bkimminich/juice-shop
     ```
   - Foreground `--rm` mode is clean for short calibration, but the terminal controls lifecycle.
   - For a longer-lived lab service:
     ```bash
     docker run -d --name juice-shop-lab -p <lab-ip>:3000:3000 bkimminich/juice-shop
     docker ps
     docker logs -f juice-shop-lab
     docker stop juice-shop-lab
     docker rm juice-shop-lab
     ```

5. If the image/package is missing, switch to setup mode rather than improvising downloads through the isolated victim:
   - Keep NIC1 host-only.
   - Temporarily enable NIC2 NAT.
   - Pull images/install packages.
   - Snapshot the VM.
   - Disable NAT again before attack/isolation mode.

6. Verification from the control plane:
   - Windows host:
     ```bash
     curl -I --max-time 5 http://<victim-hostonly-ip>:3000
     ```
   - Red-team Kali via project wrapper when available:
     ```bash
     powershell -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-run.ps1' -Command 'curl -I --max-time 5 http://<victim-hostonly-ip>:3000 | head -20'
     ```
   - Success criterion for baseline setup is a `200 OK` or otherwise expected app response from both control/host and red-team sides.

## Safety notes

- Treat this as local intentionally vulnerable lab scope only.
- Do not run aggressive scanners just because the app is reachable.
- Next safe calibration step is bounded baseline evidence: `curl`, `whatweb`, and single-known-port `nmap -sV -p 3000`, followed by model review and candidate-only evidence handling.
- Do not edit `config/scope.txt`; it is operator-owned. Ask the operator to add the lab target if platform scripts require scope intake.
