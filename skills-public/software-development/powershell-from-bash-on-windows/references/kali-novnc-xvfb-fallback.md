> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Kali noVNC Xvfb fallback from Windows/Git-Bash

Use this when a live-target or lab workflow should use the project Kali/noVNC browser, but the physical display `:0` is unavailable or stuck at LightDM and `x11vnc` cannot attach as user `kali` due Xauthority/MIT-MAGIC-COOKIE errors.

## Trigger symptoms

- `scripts/kali-vnc-control.ps1 -Action start` reaches Kali by SSH but `x11vnc -display :0` fails.
- Logs include `Invalid MIT-MAGIC-COOKIE-1 key`, `XOpenDisplay(":0") failed`, or the only visible user on `who` is `lightdm seat0 (:0)`.
- `sudo -n true` is not available, so attaching to the display-manager auth cookie as root is not appropriate for an unattended agent step.

## Safe fallback pattern

Start an isolated browser desktop instead of trying to take over the physical greeter session:

```bash
# From the Windows project root, through Git-Bash/MSYS terminal.
ssh.exe -F setting/local/ssh/empty_ssh_config \
  -i setting/local/ssh/kali_codex_ed25519 \
  -p 22 \
  -o ConnectTimeout=5 \
  -o UserKnownHostsFile=setting/local/ssh/known_hosts \
  -o StrictHostKeyChecking=accept-new \
  kali@<lab-ip> '
mkdir -p ~/.cache/hermes-vnc
nohup Xvfb :2 -screen 0 1600x900x24 -ac > ~/.cache/hermes-vnc/xvfb2.log 2>&1 &
sleep 1
DISPLAY=:2 XDG_SESSION_TYPE=x11 nohup dbus-launch --exit-with-session startxfce4 > ~/.cache/hermes-vnc/xfce2.log 2>&1 &
sleep 3
DISPLAY=:2 nohup x11vnc -display :2 -localhost -nopw -forever -shared -rfbport 5902 -o ~/.cache/hermes-vnc/x11vnc-xvfb2.log >/dev/null 2>&1 &
sleep 1
nohup websockify --web /usr/share/novnc 127.0.0.1:6081 127.0.0.1:5902 > ~/.cache/hermes-vnc/websockify2.log 2>&1 &
sleep 1
ss -ltn | grep -E "5902|6081"
'
```

Then create a local Windows tunnel. This is a long-lived process, so use background tracking rather than a shell-level `&` wrapper:

```bash
ssh.exe -F setting/local/ssh/empty_ssh_config \
  -i setting/local/ssh/kali_codex_ed25519 \
  -p 22 \
  -N \
  -L 127.0.0.1:6080:127.0.0.1:6081 \
  -o ExitOnForwardFailure=yes \
  -o UserKnownHostsFile=setting/local/ssh/known_hosts \
  -o StrictHostKeyChecking=accept-new \
  kali@<lab-ip>
```

Verify locally:

```bash
curl -I --max-time 5 http://127.0.0.1:6080/vnc.html
```

Expected success includes:

```text
HTTP/1.1 200 OK
Server: WebSockify
```

Operator URL:

```text
http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale
```

## Pitfalls

- Do not claim the old physical browser session was preserved. Xvfb is a fresh desktop; it is readiness for a new browser-only continuation, not proof that a previous prefilled form is still visible.
- Avoid `pkill -f "pattern"` inside a remote command whose own command line contains the same pattern; it can kill the SSH shell running the cleanup. Use bracketed patterns or PID lists that do not match themselves, e.g. `pgrep -f '[w]ebsockify.*6081.*5902'`.
- Keep `websockify` and `x11vnc` bound to Kali localhost and expose them to Windows only through the project SSH tunnel.
- For live bounty work, starting noVNC is not target authorization. Scope/lane artifacts and operator gates still control whether a page may be opened.

## Checkpoint wording

For a pre-contact checkpoint, record the distinction explicitly:

```text
noVNC reachable / local VM readiness passed / target page not opened in this pass / operator auth gate remains blocking
```
