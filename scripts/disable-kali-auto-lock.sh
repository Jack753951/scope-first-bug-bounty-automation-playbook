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

# Xfce session: do not lock on suspend/hibernate/shutdown paths.
set_xfconf xfce4-session /shutdown/LockScreen bool false
# Reset lock command if present; harmless if absent.
xfconf-query -c xfce4-session -p /general/LockCommand -r 2>/dev/null || true

# Xfce power manager: disable lock, blanking, DPMS, and display sleep.
set_xfconf xfce4-power-manager /xfce4-power-manager/lock-screen-suspend-hibernate bool false
set_xfconf xfce4-power-manager /xfce4-power-manager/dpms-enabled bool false
set_xfconf xfce4-power-manager /xfce4-power-manager/blank-on-ac int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/blank-on-battery int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/dpms-on-ac-off int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/dpms-on-battery-off int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/sleep-display-ac int 0
set_xfconf xfce4-power-manager /xfce4-power-manager/sleep-display-battery int 0

# Xfce screensaver: disable saver and lock behavior.
set_xfconf xfce4-screensaver /saver/enabled bool false
set_xfconf xfce4-screensaver /lock/enabled bool false
set_xfconf xfce4-screensaver /lock/sleep-activation bool false

# Apply to the currently running X session immediately.
if command -v xset >/dev/null 2>&1; then
  xset s off -dpms s noblank 2>/dev/null || true
fi
pkill -f xfce4-screensaver 2>/dev/null || true

# Persist an X-session fallback for future logins.
cat > "$HOME/.xprofile" <<'XPROFILE'
#!/usr/bin/env sh
xset s off -dpms s noblank 2>/dev/null || true
XPROFILE
chmod +x "$HOME/.xprofile"

echo "Kali auto lock / blank / DPMS disabled for user $(whoami)."
echo "DISPLAY=$DISPLAY"
echo "DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS"
