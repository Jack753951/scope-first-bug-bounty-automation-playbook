> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# VM Browser GUI Control and Live-Web Routing

Use this reference when moving live-web/browser-assisted assessment work out of the Windows host and into a Kali VM while preserving Hermes as the control plane.

## Recommended default posture

- Windows host stays the control plane: Hermes, handoff files, Obsidian, reports, scope/safety synthesis.
- Kali attacker VM runs the browser, Burp, screenshots, and low-risk manual surface mapping.
- Victim/lab VMs stay for local recoverable targets.
- Do not use the user's daily host browser profile for test sessions.
- Prefer one target/program per dedicated browser profile under the Kali user's home directory.

Example browser profile:

```bash
mkdir -p "$HOME/browser-profiles/<program>-hermes"
chromium \
  --user-data-dir="$HOME/browser-profiles/<program>-hermes" \
  --no-first-run \
  --new-window "https://example.com/"
```

## Network posture

For a Kali attacker VM that normally runs isolated/host-only:

- Keep `nic1=hostonly` for Windows/Hermes <-> Kali control traffic.
- Temporarily enable `nic2=nat` only when the VM needs outbound Internet for live-web browsing or package installs.
- Verify both the adapter type and virtual cable state. A common pitfall is `nic2="nat"` with `cableconnected2="off"`, leaving the guest interface down.

VirtualBox host-side pattern:

```powershell
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm "<vm-name>" nic2 nat
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm "<vm-name>" setlinkstate2 on
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" showvminfo "<vm-name>" --machinereadable
```

Guest-side verification:

```bash
ip -brief addr
ip route
getent hosts <target-host>
```

After the live-web session, close the browser/profile as needed and disable NAT or cable state according to the lab's isolation policy.

## Proxy/Tor defaults

Do not make Tor Browser, onion routing, or `proxychains` the default contact path for normal commercial/live bug-bounty web apps.

Default order:

1. Dedicated Kali Chromium/Firefox profile over normal NAT for low-risk manual browsing.
2. Browser explicitly configured for Burp when interception/evidence is required.
3. `proxychains` for bounded CLI tools only when allowed by scope/rules or in local lab/CTF contexts.
4. Tor Browser only for `.onion` or passive/high-risk OSINT contexts, not as the default login/testing browser for normal live sites.

Rationale: Tor/proxychains can trigger fraud controls, pollute results, violate program rules, or produce incomplete browser coverage due to DNS/QUIC/WebRTC/subprocess behavior.

## noVNC / VNC control route

If the operator prefers C-route GUI control, use a host-only/SSH-tunneled noVNC setup rather than exposing VNC on NAT or bridged networks.

Kali package setup, run manually by the operator if sudo password is required:

```bash
sudo apt update && sudo apt install -y x11vnc novnc websockify
```

Safe binding design:

- `x11vnc` listens only on Kali localhost, e.g. `127.0.0.1:5901`.
- `websockify`/noVNC listens only on Kali localhost, e.g. `127.0.0.1:6080`.
- Windows opens an SSH local tunnel to the Kali localhost noVNC port.
- The operator/agent opens only `http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale` on Windows.

Kali-side service pattern:

```bash
mkdir -p "$HOME/.cache/hermes-vnc"
DISPLAY=:0 XAUTHORITY="$HOME/.Xauthority" \
  nohup x11vnc -display :0 -localhost -nopw -forever -shared \
  -rfbport 5901 -o "$HOME/.cache/hermes-vnc/x11vnc.log" >/dev/null 2>&1 &

nohup websockify --web /usr/share/novnc \
  127.0.0.1:6080 127.0.0.1:5901 \
  > "$HOME/.cache/hermes-vnc/websockify.log" 2>&1 &
```

Windows tunnel pattern:

```powershell
ssh.exe -N \
  -L 127.0.0.1:6080:127.0.0.1:6080 \
  -i <project-ssh-key> \
  -p 22 \
  kali@<host-only-ip>
```

Verification:

```bash
ss -ltn | grep -E '5901|6080'
```

Expected exposure: listeners are Kali-localhost only; Windows access exists only while the SSH tunnel process is running.

## Boundaries for live-web browser sessions

- The operator handles login, password, OTP, CAPTCHA, payment, KYC, and other sensitive fields.
- Hermes may observe screenshots/noVNC state, organize surface maps, write run cards, verify scope, and synthesize evidence.
- Do not store cookies, passwords, OTPs, cards, recovery secrets, or private account material in handoff files or memory.
- Do not escalate from browsing to scanning, fuzzing, exploitation, proxy/VPN/Tor, or cross-account testing unless scope/rules and operator authorization explicitly allow it.
