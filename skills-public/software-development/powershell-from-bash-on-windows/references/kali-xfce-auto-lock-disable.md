> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Kali/Xfce Auto-Lock Disable from Windows Git-Bash

Use when a running Kali VirtualBox lab VM locks or blanks the desktop during browser/noVNC/GUI testing and the agent has SSH access through the project wrapper.

## Preconditions

- Target is an authorized/local Kali lab VM, not a production host.
- The VM user is the GUI user (commonly `kali`, UID 1000).
- SSH wrapper exists, e.g. `powershell -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-run.ps1' -Command '<remote bash>'` from the repo root.
- Do not ask for or type the VM password in chat. If the session is already locked, ask the operator to unlock locally once, then apply/persist the settings.

## Remote Bash Pattern

Run from Windows Git-Bash with the project root as `workdir`:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-run.ps1' -Command '
export DISPLAY=:0
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus

set_xfconf() {
  channel="$1"; property="$2"; type="$3"; value="$4"
  xfconf-query -c "$channel" -p "$property" -s "$value" --create -t "$type" 2>/dev/null || \
    xfconf-query -c "$channel" -p "$property" -s "$value" 2>/dev/null || true
}

set_xfconf xfce4-session /shutdown/LockScreen bool false
xfconf-query -c xfce4-session -p /general/LockCommand -r 2>/dev/null || true
set_xfconf xfce4-power-manager /xfce4-power-manager/lock-screen-suspend-hibernate bool false
set_xfconf xfce4-power-manager /xfce4-power-manager/dpms-enabled bool false
set_xfconf xfce4-power-manager /xfce4-power-manager/blank-on-ac int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/blank-on-battery int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/sleep-display-ac int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/sleep-display-battery int 0
set_xfconf xfce4-screensaver /saver/enabled bool false
set_xfconf xfce4-screensaver /lock/enabled bool false
set_xfconf xfce4-screensaver /lock/sleep-activation bool false

xset s off -dpms s noblank 2>/dev/null || true
pkill -f xfce4-screensaver 2>/dev/null || true
cat > "$HOME/.xprofile" <<"XPROFILE"
#!/usr/bin/env sh
xset s off -dpms s noblank 2>/dev/null || true
XPROFILE
chmod +x "$HOME/.xprofile"
'
```

For repeated use, put the remote Bash into a repo script such as `scripts/disable-kali-auto-lock.sh`, validate it with `bash -n`, then run it via `kali-run.ps1`.

## Verification

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-run.ps1' -Command '
export DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
echo session_lock=$(xfconf-query -c xfce4-session -p /shutdown/LockScreen 2>/dev/null || echo missing)
echo pm_lock=$(xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/lock-screen-suspend-hibernate 2>/dev/null || echo missing)
echo dpms_enabled=$(xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/dpms-enabled 2>/dev/null || echo missing)
echo blank_ac=$(xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/blank-on-ac 2>/dev/null || echo missing)
echo saver_enabled=$(xfconf-query -c xfce4-screensaver -p /saver/enabled 2>/dev/null || echo missing)
test -x ~/.xprofile && echo xprofile_present
'
```

Expected durable values: lock/saver false, DPMS false, blank/sleep display 0, and `xprofile_present`.

## Pitfalls

- `ssh` sessions usually have no `DISPLAY`; set `DISPLAY=:0` and `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/<uid>/bus` before `xfconf-query`.
- Avoid shell pipelines containing unescaped `|` inside a PowerShell `-Command` string launched from Bash; quote carefully or split into simpler commands.
- Do not treat a locked GUI as authorization to request or store the VM password. Operator unlocks locally; the agent only applies non-sensitive settings afterward.
- This is a usability setting only. Record that no target-touching action occurred if the task is inside a security-lab repo.
