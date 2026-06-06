> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Kali VM noVNC GUI-control route

Use this reference when the operator wants Hermes/Windows to view or lightly operate a Kali VirtualBox GUI without exposing VNC/noVNC to NAT or the Internet.

## Recommended architecture

- Windows host remains the Hermes/control plane.
- Kali VM runs the browser and GUI tooling.
- Keep the VM's lab/control NIC host-only; add NAT only when live web access is explicitly needed.
- Run VNC/noVNC only on Kali localhost:
  - `x11vnc` on `127.0.0.1:5901`
  - `websockify`/noVNC on `127.0.0.1:6080`
- Windows reaches noVNC through an SSH local tunnel only:
  - `127.0.0.1:6080 -> kali:127.0.0.1:6080`
- The operator opens:
  - `http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale`

## Kali packages

Install manually inside Kali when sudo is required:

```bash
sudo apt update && sudo apt install -y x11vnc novnc websockify
```

Do not pipe guessed sudo passwords through `sudo -S`. If the agent cannot sudo non-interactively, provide the exact command for the operator to run in the VM.

## Service start pattern

Remote Kali-side service pattern:

```bash
mkdir -p "$HOME/.cache/hermes-vnc"
DISPLAY=:0 XAUTHORITY="$HOME/.Xauthority" \
  nohup x11vnc -display :0 -localhost -nopw -forever -shared \
  -rfbport 5901 -o "$HOME/.cache/hermes-vnc/x11vnc.log" \
  >/dev/null 2>&1 &

nohup websockify --web /usr/share/novnc \
  127.0.0.1:6080 127.0.0.1:5901 \
  > "$HOME/.cache/hermes-vnc/websockify.log" 2>&1 &
```

Verify:

```bash
command -v x11vnc
command -v websockify
test -d /usr/share/novnc
ss -ltn | grep 5901
ss -ltn | grep 6080
```

Windows-side tunnel pattern:

```powershell
ssh.exe -N -L 127.0.0.1:6080:127.0.0.1:6080 kali@<host-only-ip>
```

Use the project-local SSH config/identity/known-hosts pattern when available to avoid user SSH config issues.

## Pitfalls

- VirtualBox NAT NIC may be configured but disconnected. Check and enable cable state:
  - `VBoxManage showvminfo <vm> --machinereadable | grep -E 'nic2=|cableconnected2'`
  - `VBoxManage controlvm <vm> setlinkstate2 on`
- `pkill -f x11vnc` or `pkill -f websockify` inside a long SSH `bash -lc` start command can match and kill the SSH command itself, causing unexplained SSH exit 255. Prefer a separate `stop` action, or match only already-running service PIDs carefully. Do not put broad `pkill -f` in the same start payload that contains the service names.
- Avoid exposing VNC/noVNC on `0.0.0.0` for live-web testing. Bind localhost and tunnel.
- noVNC enables GUI viewing and light operation, but credentials, OTP, CAPTCHA, payment, KYC, and other sensitive steps should remain operator-handled.
- For live bug bounty/account-owned workflows, noVNC is a control surface, not authorization to scan, fuzz, brute force, bypass rate limits, or test non-owned data.

## Recommended division of labor

Hermes can:

- Start/stop/check VM control services.
- Open non-sensitive URLs and public pages.
- Capture/analyze screenshots.
- Help map login-state surfaces after the operator logs in.
- Record paths, owned object types, evidence, and reportability notes.

Operator should handle:

- Passwords, OTPs, CAPTCHAs, email/phone verification.
- Payment, order, refund, KYC, seller/admin, or other high-risk flows.
- Final approval for any target-touching escalation beyond manual low-speed owned-account browsing.
