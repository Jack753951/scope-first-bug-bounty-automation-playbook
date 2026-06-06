> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# VirtualBox Kali Xfce Auto-Lock / Blank Disable

Use this when the user asks to disable automatic screen locking or blanking for the Kali VM while operating from the Windows Hermes control plane.

## Session lesson

In the Cybersec Lab context, if the user says "the auto timed screen lock" shortly after discussing Kali/noVNC/VM work, confirm or infer the likely target is the Kali VM before changing Windows host settings. Host power settings and guest Xfce settings are separate.

## Preferred route

From Git-Bash on Windows, use the project SSH wrapper rather than trying to click the VM UI:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-run.ps1' -Command 'hostname; whoami; pgrep -a xfce4-session || true'
```

For Xfce settings over SSH, export the active display/session bus first:

```bash
export DISPLAY=:0
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
```

## Robust Kali-side script

Run these as the logged-in Kali desktop user (usually `kali`):

```bash
#!/usr/bin/env bash
set -u
USER_ID="${UID:-$(id -u)}"
export DISPLAY="${DISPLAY:-:0}"
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=/run/user/${USER_ID}/bus}"

set_xfconf() {
  local channel="$1"
  local property="$2"
  local type="$3"
  local value="$4"
  xfconf-query -c "$channel" -p "$property" -s "$value" --create -t "$type" 2>/dev/null || \
    xfconf-query -c "$channel" -p "$property" -s "$value" 2>/dev/null || true
}

set_xfconf xfce4-session /shutdown/LockScreen bool false
xfconf-query -c xfce4-session -p /general/LockCommand -r 2>/dev/null || true

set_xfconf xfce4-power-manager /xfce4-power-manager/lock-screen-suspend-hibernate bool false
set_xfconf xfce4-power-manager /xfce4-power-manager/dpms-enabled bool false
set_xfconf xfce4-power-manager /xfce4-power-manager/blank-on-ac int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/blank-on-battery int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/dpms-on-ac-off int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/dpms-on-battery-off int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/sleep-display-ac int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/sleep-display-battery int 0

set_xfconf xfce4-screensaver /saver/enabled bool false
set_xfconf xfce4-screensaver /lock/enabled bool false
set_xfconf xfce4-screensaver /lock/sleep-activation bool false

xset s off -dpms s noblank 2>/dev/null || true
pkill -f xfce4-screensaver 2>/dev/null || true

cat > "$HOME/.xprofile" <<'XPROFILE'
#!/usr/bin/env sh
xset s off -dpms s noblank 2>/dev/null || true
XPROFILE
chmod +x "$HOME/.xprofile"
```

## Verify

```bash
export DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
xfconf-query -c xfce4-session -p /shutdown/LockScreen
xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/lock-screen-suspend-hibernate
xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/dpms-enabled
xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/blank-on-ac
xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/sleep-display-ac
xfconf-query -c xfce4-screensaver -p /saver/enabled
xfconf-query -c xfce4-screensaver -p /lock/enabled
xset q | grep -A2 -E 'Screen Saver|DPMS' || true
pgrep -f xfce4-screensaver || true
```

Expected key values:

```text
LockScreen=false
lock-screen-suspend-hibernate=false
dpms-enabled=false
blank-on-ac=0
sleep-display-ac=0
saver/enabled=false
lock/enabled=false
```

## Pitfalls

- Do not use host Windows `powercfg`/screen-saver registry settings when the request is about the Kali guest.
- `xfconf-query` over SSH may fail with `Unable to open display` unless `DISPLAY` and `DBUS_SESSION_BUS_ADDRESS` are set.
- Quoting complex remote commands through PowerShell -> SSH -> bash is brittle; prefer writing a small Kali-side shell script in the shared repo and invoking it via `kali-run.ps1`.
- `pgrep -x xfce4-screensaver` can warn because the process name is longer than 15 chars; use `pgrep -f` when checking full command lines.
