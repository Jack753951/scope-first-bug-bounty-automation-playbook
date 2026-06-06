param(
    [ValidateSet("start", "stop", "status")]
    [string]$Action = "start"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ConfigPath = Join-Path $ProjectRoot "setting\local\kali-ssh.json"
$StateDir = Join-Path $ProjectRoot "setting\local\vnc"
$TunnelPidPath = Join-Path $StateDir "kali-vnc-tunnel.pid"

if (-not (Test-Path $ConfigPath)) { throw "Missing config: $ConfigPath" }
$config = Get-Content -Raw -Encoding UTF8 $ConfigPath | ConvertFrom-Json
$HostName = $config.host
$User = $config.user
$Port = [int]$config.port
$Identity = Join-Path $ProjectRoot $config.identityFile
$KnownHosts = Join-Path $ProjectRoot $config.knownHostsFile
$SshConfig = Join-Path (Split-Path -Parent $KnownHosts) "empty_ssh_config"

New-Item -ItemType Directory -Force -Path $StateDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $KnownHosts) | Out-Null
if (-not (Test-Path $SshConfig)) { New-Item -ItemType File -Force -Path $SshConfig | Out-Null }
if (-not (Test-Path $Identity)) { throw "Missing SSH identity file: $Identity" }

function ConvertTo-BashSingleQuoted {
    param([string]$Value)
    $singleQuote = [string][char]39
    $replacement = $singleQuote + '"' + $singleQuote + '"' + $singleQuote
    return $singleQuote + $Value.Replace($singleQuote, $replacement) + $singleQuote
}

$script:LastKaliExitCode = 0
function Invoke-KaliCommand {
    param([string]$Command)
    $remote = "$User@$HostName"
    $quotedCommand = ConvertTo-BashSingleQuoted ($Command -replace "`r`n", "`n" -replace "`r", "`n")
    $sshArgs = @(
        "-F", $SshConfig,
        "-i", $Identity,
        "-p", "$Port",
        "-o", "UserKnownHostsFile=$KnownHosts",
        "-o", "StrictHostKeyChecking=accept-new",
        $remote,
        "bash -lc $quotedCommand"
    )
    & ssh.exe @sshArgs
    $script:LastKaliExitCode = $LASTEXITCODE
}

function Stop-Tunnel {
    if (Test-Path $TunnelPidPath) {
        $pidText = (Get-Content -Raw $TunnelPidPath).Trim()
        if ($pidText) {
            $proc = Get-Process -Id ([int]$pidText) -ErrorAction SilentlyContinue
            if ($proc) { Stop-Process -Id $proc.Id -Force }
        }
        Remove-Item $TunnelPidPath -Force -ErrorAction SilentlyContinue
    }
}

$remoteStatus = @'
set -eu
if command -v x11vnc >/dev/null 2>&1; then echo x11vnc_tool=ok; else echo x11vnc_tool=missing; fi
if command -v websockify >/dev/null 2>&1; then echo websockify_tool=ok; else echo websockify_tool=missing; fi
if [ -d /usr/share/novnc ]; then echo novnc_files=ok; else echo novnc_files=missing; fi
if ss -ltn 2>/dev/null | grep 5901 >/dev/null 2>&1; then echo x11vnc=running; else echo x11vnc=stopped; fi
if ss -ltn 2>/dev/null | grep 6080 >/dev/null 2>&1; then echo websockify=running; else echo websockify=stopped; fi
ss -ltn 2>/dev/null | grep 5901 || true
ss -ltn 2>/dev/null | grep 6080 || true
'@

$remoteStop = @'
pkill -f "websockify.*6080.*5901" 2>/dev/null || true
pkill -f "x11vnc .*5901" 2>/dev/null || true
echo "remote_vnc_stopped"
'@

$remoteStart = @'
set -eu
missing=
command -v x11vnc >/dev/null 2>&1 || missing=${missing}_x11vnc
command -v websockify >/dev/null 2>&1 || missing=${missing}_websockify
[ -d /usr/share/novnc ] || missing=${missing}_novnc
if [ "x$missing" != "x" ]; then
  echo missing_packages:$missing
  echo install_command_manual_in_kali_terminal
  echo sudo_apt_update_then_install_x11vnc_novnc_websockify
  exit 2
fi
# Do not pkill here: the remote SSH shell command line includes the service names and can match itself.
# Use the stop action first if ports are already occupied.
mkdir -p $HOME/.cache/hermes-vnc
DISPLAY=:0 XAUTHORITY=$HOME/.Xauthority nohup x11vnc -display :0 -localhost -nopw -forever -shared -rfbport 5901 -o $HOME/.cache/hermes-vnc/x11vnc.log >/dev/null 2>&1 &
sleep 1
nohup websockify --web /usr/share/novnc 127.0.0.1:6080 127.0.0.1:5901 > $HOME/.cache/hermes-vnc/websockify.log 2>&1 &
sleep 1
if ! ss -ltn 2>/dev/null | grep 5901 >/dev/null 2>&1; then
  echo x11vnc_display0_failed_falling_back_to_xvfb1
  tail -40 $HOME/.cache/hermes-vnc/x11vnc.log 2>/dev/null || true
  for pid in $(pgrep -f '[w]ebsockify.*6080.*5901' 2>/dev/null || true); do kill "$pid" 2>/dev/null || true; done
  for pid in $(pgrep -f '[x]11vnc .*5901' 2>/dev/null || true); do kill "$pid" 2>/dev/null || true; done
  for pid in $(pgrep -f '[X]vfb :1' 2>/dev/null || true); do kill "$pid" 2>/dev/null || true; done
  mkdir -p $HOME/.cache/hermes-vnc
  nohup Xvfb :1 -screen 0 1600x900x24 -ac > $HOME/.cache/hermes-vnc/xvfb.log 2>&1 &
  sleep 1
  DISPLAY=:1 XDG_SESSION_TYPE=x11 nohup dbus-launch --exit-with-session startxfce4 > $HOME/.cache/hermes-vnc/xfce.log 2>&1 &
  sleep 3
  DISPLAY=:1 nohup x11vnc -display :1 -localhost -nopw -forever -shared -rfbport 5901 -o $HOME/.cache/hermes-vnc/x11vnc-xvfb.log >/dev/null 2>&1 &
  sleep 1
fi
if ! ss -ltn 2>/dev/null | grep 5901 >/dev/null 2>&1; then
  echo x11vnc_failed
  tail -80 $HOME/.cache/hermes-vnc/x11vnc-xvfb.log 2>/dev/null || true
  tail -80 $HOME/.cache/hermes-vnc/xvfb.log 2>/dev/null || true
  tail -80 $HOME/.cache/hermes-vnc/xfce.log 2>/dev/null || true
  exit 3
fi
if ! ss -ltn 2>/dev/null | grep 6080 >/dev/null 2>&1; then
  nohup websockify --web /usr/share/novnc 127.0.0.1:6080 127.0.0.1:5901 > $HOME/.cache/hermes-vnc/websockify.log 2>&1 &
  sleep 1
fi
if ! ss -ltn 2>/dev/null | grep 6080 >/dev/null 2>&1; then
  echo websockify_failed
  tail -80 $HOME/.cache/hermes-vnc/websockify.log 2>/dev/null || true
  exit 4
fi
echo remote_vnc_started
echo Remote services are bound to Kali localhost only: 127.0.0.1:5901 and 127.0.0.1:6080
'@

switch ($Action) {
    "status" {
        Invoke-KaliCommand $remoteStatus
        if (Test-Path $TunnelPidPath) {
            $pidText = (Get-Content -Raw $TunnelPidPath).Trim()
            $proc = if ($pidText) { Get-Process -Id ([int]$pidText) -ErrorAction SilentlyContinue } else { $null }
            if ($proc) { "local_tunnel=running pid=$pidText" } else { "local_tunnel=stale_or_stopped" }
        } else {
            "local_tunnel=stopped"
        }
    }
    "stop" {
        Stop-Tunnel
        Invoke-KaliCommand $remoteStop
        "local_tunnel_stopped"
    }
    "start" {
        Invoke-KaliCommand $remoteStart
        $code = $script:LastKaliExitCode
        if ($code -ne 0) { exit $code }
        Stop-Tunnel
        $remote = "$User@$HostName"
        $sshArgs = @(
            "-F", $SshConfig,
            "-i", $Identity,
            "-p", "$Port",
            "-N",
            "-L", "127.0.0.1:6080:127.0.0.1:6080",
            "-o", "ExitOnForwardFailure=yes",
            "-o", "UserKnownHostsFile=$KnownHosts",
            "-o", "StrictHostKeyChecking=accept-new",
            $remote
        )
        $proc = Start-Process -FilePath "ssh.exe" -ArgumentList $sshArgs -WindowStyle Hidden -PassThru
        Set-Content -Encoding ASCII -Path $TunnelPidPath -Value $proc.Id
        Start-Sleep -Seconds 1
        if (-not (Get-Process -Id $proc.Id -ErrorAction SilentlyContinue)) {
            throw "SSH tunnel failed to stay running."
        }
        "local_tunnel_started pid=$($proc.Id)"
        "Open: http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale"
        "Security: x11vnc/noVNC are bound to Kali localhost; Windows reaches them through SSH local tunnel only."
    }
}
