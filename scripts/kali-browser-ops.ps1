param(
    [ValidateSet("status", "open", "browser-reset", "screenshot", "click", "type", "hotkey", "downloads", "cdp-text", "cdp-visible-text", "cdp-click", "cdp-fill")]
    [string]$Action = "status",
    [string]$Url,
    [string]$Text,
    [string]$Selector,
    [int]$X,
    [int]$Y,
    [string]$Key,
    [string]$ProfileName = "hermes-browser",
    [ValidateSet("chromium", "firefox")]
    [string]$Browser = "chromium",
    [string]$Display = "auto",
    [int]$Width = 1600,
    [int]$Height = 900,
    [string]$LocalOutDir,
    [int]$MaxTextChars = 6000,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ConfigPath = Join-Path $ProjectRoot "setting\local\kali-ssh.json"

if (-not (Test-Path $ConfigPath)) { throw "Missing config: $ConfigPath" }
$config = Get-Content -Raw -Encoding UTF8 $ConfigPath | ConvertFrom-Json
$HostName = $config.host
$User = $config.user
$Port = [int]$config.port
$Identity = Join-Path $ProjectRoot $config.identityFile
$KnownHosts = Join-Path $ProjectRoot $config.knownHostsFile
if (-not $LocalOutDir) { $LocalOutDir = Join-Path $ProjectRoot "<artifact-output-dir>\browser_state" }

if (-not $HostName) { throw "Kali host is not configured. Edit setting/local/kali-ssh.json." }
if (-not (Test-Path $Identity)) { throw "Missing SSH identity file: $Identity" }

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $KnownHosts) | Out-Null
New-Item -ItemType Directory -Force -Path $LocalOutDir | Out-Null
$SshConfig = Join-Path (Split-Path -Parent $KnownHosts) "empty_ssh_config"
if (-not (Test-Path $SshConfig)) { New-Item -ItemType File -Force -Path $SshConfig | Out-Null }

function ConvertTo-BashSingleQuoted {
    param([string]$Value)
    if ($null -eq $Value) { $Value = "" }
    $singleQuote = [string][char]39
    $replacement = $singleQuote + '"' + $singleQuote + '"' + $singleQuote
    return $singleQuote + $Value.Replace($singleQuote, $replacement) + $singleQuote
}

function ConvertTo-SafeName {
    param([string]$Value)
    if (-not $Value) { return "default" }
    return ($Value -replace '[^A-Za-z0-9_.-]', '_')
}

function New-RemotePrelude {
    param([string]$RequestedDisplay)
    $displayLine = "HERMES_REQUESTED_DISPLAY=$(ConvertTo-BashSingleQuoted $RequestedDisplay)"
    return @"
set +u
$displayLine
resolve_display() {
  if [ "x`$HERMES_REQUESTED_DISPLAY" != "x" ] && [ "`$HERMES_REQUESTED_DISPLAY" != "auto" ]; then
    echo "`$HERMES_REQUESTED_DISPLAY"
    return 0
  fi
  for d in "`${DISPLAY:-}" :0 :1; do
    [ -n "`$d" ] || continue
    if command -v xdpyinfo >/dev/null 2>&1; then
      DISPLAY="`$d" xdpyinfo >/dev/null 2>&1 && { echo "`$d"; return 0; }
    else
      echo "`$d"; return 0
    fi
  done
  echo :0
}
D=`$(resolve_display)
export DISPLAY="`$D"
export XAUTHORITY="`$HOME/.Xauthority"
mkdir -p "`$HOME/.cache/hermes-browser-ops"
"@
}

$script:LastKaliExitCode = 0
$script:LastCopyExitCode = 0

function Invoke-KaliCommand {
    param([string]$Command)
    $remote = "$User@$HostName"
    $normalizedCommand = $Command -replace "`r`n", "`n" -replace "`r", "`n"
    $quotedCommand = ConvertTo-BashSingleQuoted $normalizedCommand
    $sshArgs = @(
        "-F", $SshConfig,
        "-i", $Identity,
        "-p", "$Port",
        "-o", "UserKnownHostsFile=$KnownHosts",
        "-o", "StrictHostKeyChecking=accept-new",
        $remote,
        "bash -lc $quotedCommand"
    )
    if ($DryRun) {
        Write-Host "[DRY RUN] ssh $($sshArgs -join ' ')" -ForegroundColor Yellow
        $script:LastKaliExitCode = 0
        return
    }
    & ssh.exe @sshArgs
    $script:LastKaliExitCode = $LASTEXITCODE
}

function Copy-FromKali {
    param([string]$RemotePath)
    $remote = "$User@$HostName`:$RemotePath"
    $scpArgs = @(
        "-F", $SshConfig,
        "-i", $Identity,
        "-P", "$Port",
        "-o", "UserKnownHostsFile=$KnownHosts",
        "-o", "StrictHostKeyChecking=accept-new",
        $remote,
        $LocalOutDir
    )
    if ($DryRun) {
        Write-Host "[DRY RUN] scp $($scpArgs -join ' ')" -ForegroundColor Yellow
        $script:LastCopyExitCode = 0
        return
    }
    & scp.exe @scpArgs
    $script:LastCopyExitCode = $LASTEXITCODE
}

function Copy-ToKali {
    param([string]$LocalPath, [string]$RemotePath)
    $remote = "$User@$HostName`:$RemotePath"
    $scpArgs = @(
        "-F", $SshConfig,
        "-i", $Identity,
        "-P", "$Port",
        "-o", "UserKnownHostsFile=$KnownHosts",
        "-o", "StrictHostKeyChecking=accept-new",
        $LocalPath,
        $remote
    )
    if ($DryRun) {
        Write-Host "[DRY RUN] scp $($scpArgs -join ' ')" -ForegroundColor Yellow
        $script:LastCopyExitCode = 0
        return
    }
    & scp.exe @scpArgs
    $script:LastCopyExitCode = $LASTEXITCODE
}

$safeProfile = ConvertTo-SafeName $ProfileName
$prelude = (New-RemotePrelude $Display) + "`n"

switch ($Action) {
    "status" {
        $cmd = $prelude + @'
echo action=status
echo display=$DISPLAY
for tool in xdotool xdpyinfo gnome-screenshot scrot import chromium chromium-browser google-chrome firefox curl python3 ss; do
  if command -v "$tool" >/dev/null 2>&1; then echo tool_$tool=ok; else echo tool_$tool=missing; fi
done
if ss -ltn 2>/dev/null | grep ':9222 ' >/dev/null 2>&1; then echo cdp_9222=running; else echo cdp_9222=stopped; fi
pgrep -a chromium 2>/dev/null | head -5 || true
pgrep -a firefox 2>/dev/null | head -5 || true
'@
        Invoke-KaliCommand $cmd
        exit $script:LastKaliExitCode
    }
    "open" {
        if (-not $Url) { throw "-Url is required for -Action open" }
        $quotedUrl = ConvertTo-BashSingleQuoted $Url
        $quotedProfile = ConvertTo-BashSingleQuoted $safeProfile
        $browserCommand = if ($Browser -eq "firefox") {
            @"
if command -v firefox >/dev/null 2>&1; then BROWSER_BIN=firefox; else echo firefox_missing; exit 2; fi
PROFILE_DIR="`$HOME/browser-profiles/$safeProfile"
mkdir -p "`$PROFILE_DIR"
nohup "`$BROWSER_BIN" --new-window $quotedUrl >"`$HOME/.cache/hermes-browser-ops/${safeProfile}_firefox.log" 2>&1 &
echo opened_firefox profile=$safeProfile url=$Url display=`$DISPLAY
"@
        } else {
            @"
if command -v chromium >/dev/null 2>&1; then BROWSER_BIN=chromium; elif command -v chromium-browser >/dev/null 2>&1; then BROWSER_BIN=chromium-browser; elif command -v google-chrome >/dev/null 2>&1; then BROWSER_BIN=google-chrome; else echo chromium_missing; exit 2; fi
PROFILE_DIR="`$HOME/browser-profiles/$safeProfile"
mkdir -p "`$PROFILE_DIR"
nohup "`$BROWSER_BIN" --user-data-dir="`$PROFILE_DIR" --no-first-run --disable-session-crashed-bubble --remote-debugging-address=127.0.0.1 --remote-debugging-port=9222 --window-size=$Width,$Height --new-window $quotedUrl >"`$HOME/.cache/hermes-browser-ops/${safeProfile}_chromium.log" 2>&1 &
echo opened_chromium profile=$safeProfile cdp=127.0.0.1:9222 url=$Url display=`$DISPLAY
"@
        }
        Invoke-KaliCommand ($prelude + $browserCommand)
        exit $script:LastKaliExitCode
    }
    "browser-reset" {
        $cmd = $prelude + @"
if ! command -v python3 >/dev/null 2>&1; then echo python3_missing; exit 2; fi
printf %s CmltcG9ydCBvcywgc2lnbmFsLCBzdWJwcm9jZXNzLCBzeXMsIHRpbWUKdHJ5OgogICAgb3V0ID0gc3VicHJvY2Vzcy5jaGVja19vdXRwdXQoWyJwZ3JlcCIsICItYSIsICJjaHJvbWl1bSJdLCB0ZXh0PVRydWUsIHN0ZGVycj1zdWJwcm9jZXNzLkRFVk5VTEwpCmV4Y2VwdCBzdWJwcm9jZXNzLkNhbGxlZFByb2Nlc3NFcnJvcjoKICAgIG91dCA9ICIiCnBpZHMgPSBbXQpmb3IgbGluZSBpbiBvdXQuc3BsaXRsaW5lcygpOgogICAgaWYgInJlbW90ZS1kZWJ1Z2dpbmctcG9ydD05MjIyIiBpbiBsaW5lOgogICAgICAgIHRyeToKICAgICAgICAgICAgcGlkcy5hcHBlbmQoaW50KGxpbmUuc3BsaXQoTm9uZSwgMSlbMF0pKQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgICAgIHBhc3MKZm9yIHBpZCBpbiBwaWRzOgogICAgdHJ5OgogICAgICAgIG9zLmtpbGwocGlkLCBzaWduYWwuU0lHVEVSTSkKICAgIGV4Y2VwdCBQcm9jZXNzTG9va3VwRXJyb3I6CiAgICAgICAgcGFzcwogICAgZXhjZXB0IFBlcm1pc3Npb25FcnJvcjoKICAgICAgICBwcmludChmImNocm9taXVtX3Jlc2V0X3Blcm1pc3Npb25fZGVuaWVkIHBpZD17cGlkfSIpCiAgICAgICAgc3lzLmV4aXQoMikKdGltZS5zbGVlcCgxKQp0cnk6CiAgICBvdXQyID0gc3VicHJvY2Vzcy5jaGVja19vdXRwdXQoWyJwZ3JlcCIsICItYSIsICJjaHJvbWl1bSJdLCB0ZXh0PVRydWUsIHN0ZGVycj1zdWJwcm9jZXNzLkRFVk5VTEwpCmV4Y2VwdCBzdWJwcm9jZXNzLkNhbGxlZFByb2Nlc3NFcnJvcjoKICAgIG91dDIgPSAiIgpyZW1haW5pbmcgPSBbbGluZSBmb3IgbGluZSBpbiBvdXQyLnNwbGl0bGluZXMoKSBpZiAicmVtb3RlLWRlYnVnZ2luZy1wb3J0PTkyMjIiIGluIGxpbmVdCmlmIHJlbWFpbmluZzoKICAgIHByaW50KCJjaHJvbWl1bV9yZXNldF9pbmNvbXBsZXRlIikKICAgIHN5cy5leGl0KDIpCnByaW50KCJjaHJvbWl1bV9yZW1vdGVfZGVidWdnaW5nX3Jlc2V0IikK | base64 -d > /tmp/hermes_browser_reset.py
python3 /tmp/hermes_browser_reset.py
"@
        Invoke-KaliCommand $cmd
        exit $script:LastKaliExitCode
    }
    "screenshot" {
        $remotePath = "`$HOME/codex-output/browser_state/${safeProfile}_$(Get-Date -Format yyyyMMddTHHmmssZ).png"
        $cmd = $prelude + @"
mkdir -p "`$HOME/codex-output/browser_state"
OUT="$remotePath"
if command -v gnome-screenshot >/dev/null 2>&1; then
  gnome-screenshot -f "`$OUT"
elif command -v scrot >/dev/null 2>&1; then
  scrot "`$OUT"
elif command -v import >/dev/null 2>&1; then
  import -window root "`$OUT"
else
  echo screenshot_tool_missing
  exit 2
fi
if [ ! -s "`$OUT" ]; then echo screenshot_empty; exit 3; fi
echo screenshot_remote_path="`$OUT"
"@
        Invoke-KaliCommand $cmd
        if ($script:LastKaliExitCode -ne 0) { exit $script:LastKaliExitCode }
        Copy-FromKali ("~/codex-output/browser_state/" + (Split-Path -Leaf $remotePath))
        if ($script:LastCopyExitCode -eq 0) {
            $localPath = Join-Path $LocalOutDir (Split-Path -Leaf $remotePath)
            Write-Output "screenshot_local_path=$localPath"
        }
        exit $script:LastCopyExitCode
    }
    "click" {
        if ($X -lt 0 -or $Y -lt 0) { throw "-X and -Y are required for -Action click" }
        $cmd = $prelude + @"
command -v xdotool >/dev/null 2>&1 || { echo xdotool_missing; exit 2; }
xdotool mousemove $X $Y click 1
echo clicked x=$X y=$Y display=`$DISPLAY
"@
        Invoke-KaliCommand $cmd
        exit $script:LastKaliExitCode
    }
    "type" {
        if (-not $Text) { throw "-Text is required for -Action type. Do not use this for passwords, OTPs, tokens, cookies, or phone numbers." }
        $quotedText = ConvertTo-BashSingleQuoted $Text
        $cmd = $prelude + @"
command -v xdotool >/dev/null 2>&1 || { echo xdotool_missing; exit 2; }
xdotool type --delay 5 -- $quotedText
echo typed_chars=$($Text.Length) display=`$DISPLAY
"@
        Invoke-KaliCommand $cmd
        exit $script:LastKaliExitCode
    }
    "hotkey" {
        if (-not $Key) { throw "-Key is required for -Action hotkey, e.g. ctrl+l or Return" }
        $quotedKey = ConvertTo-BashSingleQuoted $Key
        $cmd = $prelude + @"
command -v xdotool >/dev/null 2>&1 || { echo xdotool_missing; exit 2; }
xdotool key $quotedKey
echo hotkey=$Key display=`$DISPLAY
"@
        Invoke-KaliCommand $cmd
        exit $script:LastKaliExitCode
    }
    "downloads" {
        $cmd = $prelude + @'
for expanded in "$HOME/Downloads" "$HOME/下載"; do
  if [ -d "$expanded" ]; then
    echo downloads_dir=$expanded
    find "$expanded" -maxdepth 1 -type f -printf '%TY-%Tm-%TdT%TH:%TM:%TSZ\t%s\t%f\n' 2>/dev/null | sort | tail -30
  fi
done
'@
        Invoke-KaliCommand $cmd
        exit $script:LastKaliExitCode
    }
    "cdp-text" {
        $cmd = $prelude + @'
if ! command -v curl >/dev/null 2>&1; then echo curl_missing; exit 2; fi
if ! command -v python3 >/dev/null 2>&1; then echo python3_missing; exit 2; fi
printf %s aW1wb3J0IGpzb24sIHVybGxpYi5yZXF1ZXN0LCBzeXMKdHJ5OgogICAgdGFicyA9IGpzb24ubG9hZCh1cmxsaWIucmVxdWVzdC51cmxvcGVuKCJodHRwOi8vMTI3LjAuMC4xOjkyMjIvanNvbiIsIHRpbWVvdXQ9MikpCmV4Y2VwdCBFeGNlcHRpb24gYXMgZXhjOgogICAgcHJpbnQoImNkcF91bmF2YWlsYWJsZT0iICsgZXhjLl9fY2xhc3NfXy5fX25hbWVfXykKICAgIHN5cy5leGl0KDIpCnBhZ2UgPSBuZXh0KCh0IGZvciB0IGluIHRhYnMgaWYgdC5nZXQoInR5cGUiKSA9PSAicGFnZSIgYW5kIHQuZ2V0KCJ3ZWJTb2NrZXREZWJ1Z2dlclVybCIpKSwgTm9uZSkKaWYgbm90IHBhZ2U6CiAgICBwcmludCgiY2RwX25vX3BhZ2UiKQogICAgc3lzLmV4aXQoMykKcHJpbnQoInRpdGxlPSIgKyBwYWdlLmdldCgidGl0bGUiLCAiIilbOjIwMF0ucmVwbGFjZSgiXG4iLCAiICIpKQpwcmludCgidXJsPSIgKyBwYWdlLmdldCgidXJsIiwgIiIpWzo1MDBdKQpwcmludCgibm90ZT1Gb3IgZnVsbCBET00gZXh0cmFjdGlvbiB1c2UgYSBkZWRpY2F0ZWQgcmV2aWV3ZWQgQ0RQIGhlbHBlcjsgdGhpcyBzdGF0dXMgYWN0aW9uIGF2b2lkcyBwdWxsaW5nIGNvb2tpZXMvdG9rZW5zIG9yIHJlc3BvbnNlIGJvZGllcy4iKQo= | base64 -d > /tmp/hermes_cdp_text.py
python3 /tmp/hermes_cdp_text.py
'@
        Invoke-KaliCommand $cmd
        exit $script:LastKaliExitCode
    }
    "cdp-visible-text" {
        $cmd = $prelude + @"
if ! command -v python3 >/dev/null 2>&1; then echo python3_missing; exit 2; fi
export HERMES_MAX_TEXT_CHARS=$MaxTextChars
printf %s CmltcG9ydCBiYXNlNjQKaW1wb3J0IGpzb24KaW1wb3J0IG9zCmltcG9ydCBzb2NrZXQKaW1wb3J0IHN0cnVjdAppbXBvcnQgc3lzCmltcG9ydCB1cmxsaWIucmVxdWVzdAoKbWF4X2NoYXJzID0gaW50KG9zLmVudmlyb24uZ2V0KCJIRVJNRVNfTUFYX1RFWFRfQ0hBUlMiLCAiNjAwMCIpKQptYXhfY2hhcnMgPSBtYXgoNTAwLCBtaW4obWF4X2NoYXJzLCAyMDAwMCkpCnRyeToKICAgIHRhYnMgPSBqc29uLmxvYWQodXJsbGliLnJlcXVlc3QudXJsb3BlbigiaHR0cDovLzEyNy4wLjAuMTo5MjIyL2pzb24iLCB0aW1lb3V0PTIpKQpleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgIHByaW50KGpzb24uZHVtcHMoeyJvayI6IEZhbHNlLCAiZXJyb3IiOiAiY2RwX3VuYXZhaWxhYmxlIiwgImRldGFpbCI6IGV4Yy5fX2NsYXNzX18uX19uYW1lX199LCBlbnN1cmVfYXNjaWk9RmFsc2UpKQogICAgc3lzLmV4aXQoMikKcGFnZSA9IG5leHQoKHQgZm9yIHQgaW4gdGFicyBpZiB0LmdldCgidHlwZSIpID09ICJwYWdlIiBhbmQgdC5nZXQoIndlYlNvY2tldERlYnVnZ2VyVXJsIiwgIiIpLnN0YXJ0c3dpdGgoIndzOi8vIikpLCBOb25lKQppZiBub3QgcGFnZToKICAgIHByaW50KGpzb24uZHVtcHMoeyJvayI6IEZhbHNlLCAiZXJyb3IiOiAiY2RwX25vX3BhZ2UifSwgZW5zdXJlX2FzY2lpPUZhbHNlKSkKICAgIHN5cy5leGl0KDMpCnJlc3QgPSBwYWdlWyJ3ZWJTb2NrZXREZWJ1Z2dlclVybCJdW2xlbigid3M6Ly8iKTpdCmhvc3Rwb3J0LCBwYXRoID0gcmVzdC5zcGxpdCgiLyIsIDEpCnBhdGggPSAiLyIgKyBwYXRoCmhvc3QsIHBvcnRfcyA9IGhvc3Rwb3J0LnJzcGxpdCgiOiIsIDEpCnBvcnQgPSBpbnQocG9ydF9zKQprZXkgPSBiYXNlNjQuYjY0ZW5jb2RlKG9zLnVyYW5kb20oMTYpKS5kZWNvZGUoKQpyZXEgPSAoZiJHRVQge3BhdGh9IEhUVFAvMS4xXHJcbkhvc3Q6IHtob3N0fTp7cG9ydH1cclxuVXBncmFkZTogd2Vic29ja2V0XHJcbkNvbm5lY3Rpb246IFVwZ3JhZGVcclxuU2VjLVdlYlNvY2tldC1LZXk6IHtrZXl9XHJcblNlYy1XZWJTb2NrZXQtVmVyc2lvbjogMTNcclxuXHJcbiIpCnNvY2sgPSBzb2NrZXQuY3JlYXRlX2Nvbm5lY3Rpb24oKGhvc3QsIHBvcnQpLCB0aW1lb3V0PTMpCnNvY2suc2VuZGFsbChyZXEuZW5jb2RlKCkpCnJlc3AgPSBiIiIKd2hpbGUgYiJcclxuXHJcbiIgbm90IGluIHJlc3A6CiAgICBjaHVuayA9IHNvY2sucmVjdig0MDk2KQogICAgaWYgbm90IGNodW5rOgogICAgICAgIGJyZWFrCiAgICByZXNwICs9IGNodW5rCmlmIGIiIDEwMSAiIG5vdCBpbiByZXNwLnNwbGl0KGIiXHJcbiIsIDEpWzBdOgogICAgcHJpbnQoanNvbi5kdW1wcyh7Im9rIjogRmFsc2UsICJlcnJvciI6ICJ3ZWJzb2NrZXRfdXBncmFkZV9mYWlsZWQifSwgZW5zdXJlX2FzY2lpPUZhbHNlKSkKICAgIHN5cy5leGl0KDUpCgpkZWYgd3Nfc2VuZF90ZXh0KHBheWxvYWQ6IHN0cik6CiAgICBkYXRhID0gcGF5bG9hZC5lbmNvZGUoInV0Zi04IikKICAgIGhlYWRlciA9IGJ5dGVhcnJheShbMHg4MV0pCiAgICBuID0gbGVuKGRhdGEpCiAgICBpZiBuIDwgMTI2OgogICAgICAgIGhlYWRlci5hcHBlbmQoMHg4MCB8IG4pCiAgICBlbGlmIG4gPCA2NTUzNjoKICAgICAgICBoZWFkZXIuYXBwZW5kKDB4ODAgfCAxMjYpOyBoZWFkZXIuZXh0ZW5kKHN0cnVjdC5wYWNrKCIhSCIsIG4pKQogICAgZWxzZToKICAgICAgICBoZWFkZXIuYXBwZW5kKDB4ODAgfCAxMjcpOyBoZWFkZXIuZXh0ZW5kKHN0cnVjdC5wYWNrKCIhUSIsIG4pKQogICAgbWFzayA9IG9zLnVyYW5kb20oNCkKICAgIGhlYWRlci5leHRlbmQobWFzaykKICAgIHNvY2suc2VuZGFsbChoZWFkZXIgKyBieXRlcyhiIF4gbWFza1tpICUgNF0gZm9yIGksIGIgaW4gZW51bWVyYXRlKGRhdGEpKSkKCmRlZiByZWN2X2V4YWN0KG4pOgogICAgYnVmID0gYiIiCiAgICB3aGlsZSBsZW4oYnVmKSA8IG46CiAgICAgICAgY2h1bmsgPSBzb2NrLnJlY3YobiAtIGxlbihidWYpKQogICAgICAgIGlmIG5vdCBjaHVuazoKICAgICAgICAgICAgcmFpc2UgRU9GRXJyb3IoIndlYnNvY2tldCBjbG9zZWQiKQogICAgICAgIGJ1ZiArPSBjaHVuawogICAgcmV0dXJuIGJ1ZgoKZGVmIHdzX3JlY3ZfdGV4dCgpOgogICAgd2hpbGUgVHJ1ZToKICAgICAgICBmaXJzdCA9IHJlY3ZfZXhhY3QoMikKICAgICAgICBvcGNvZGUgPSBmaXJzdFswXSAmIDB4MGYKICAgICAgICBsZW5ndGggPSBmaXJzdFsxXSAmIDB4N2YKICAgICAgICBtYXNrZWQgPSBmaXJzdFsxXSAmIDB4ODAKICAgICAgICBpZiBsZW5ndGggPT0gMTI2OgogICAgICAgICAgICBsZW5ndGggPSBzdHJ1Y3QudW5wYWNrKCIhSCIsIHJlY3ZfZXhhY3QoMikpWzBdCiAgICAgICAgZWxpZiBsZW5ndGggPT0gMTI3OgogICAgICAgICAgICBsZW5ndGggPSBzdHJ1Y3QudW5wYWNrKCIhUSIsIHJlY3ZfZXhhY3QoOCkpWzBdCiAgICAgICAgbWFzayA9IHJlY3ZfZXhhY3QoNCkgaWYgbWFza2VkIGVsc2UgYiIiCiAgICAgICAgZGF0YSA9IHJlY3ZfZXhhY3QobGVuZ3RoKSBpZiBsZW5ndGggZWxzZSBiIiIKICAgICAgICBpZiBtYXNrZWQ6CiAgICAgICAgICAgIGRhdGEgPSBieXRlcyhiIF4gbWFza1tpICUgNF0gZm9yIGksIGIgaW4gZW51bWVyYXRlKGRhdGEpKQogICAgICAgIGlmIG9wY29kZSA9PSAxOgogICAgICAgICAgICByZXR1cm4gZGF0YS5kZWNvZGUoInV0Zi04IiwgInJlcGxhY2UiKQogICAgICAgIGlmIG9wY29kZSA9PSA4OgogICAgICAgICAgICByYWlzZSBFT0ZFcnJvcigid2Vic29ja2V0IGNsb3NlIGZyYW1lIikKCmpzX3RlbXBsYXRlID0gIiIiCigoKSA9PiB7ewogIGNvbnN0IG1heENoYXJzID0ge21heF9jaGFyc307CiAgY29uc3QgdGV4dCA9IChkb2N1bWVudC5ib2R5ICYmIGRvY3VtZW50LmJvZHkuaW5uZXJUZXh0ID8gZG9jdW1lbnQuYm9keS5pbm5lclRleHQgOiAnJykucmVwbGFjZSgvW1xcdCBdKy9nLCAnICcpLnJlcGxhY2UoL1xcbnt7Myx9fS9nLCAnXFxuXFxuJykudHJpbSgpOwogIGNvbnN0IHNhbXBsZUxpbmtzID0gQXJyYXkuZnJvbShkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCdhW2hyZWZdJykpLnNsaWNlKDAsIDgwKS5tYXAoYSA9PiAoe3t0ZXh0OiAoYS5pbm5lclRleHQgfHwgYS5nZXRBdHRyaWJ1dGUoJ2FyaWEtbGFiZWwnKSB8fCAnJykudHJpbSgpLnNsaWNlKDAsMTIwKSwgaHJlZjogYS5ocmVmLnNsaWNlKDAsMzAwKX19KSk7CiAgY29uc3QgY29udHJvbHMgPSBBcnJheS5mcm9tKGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJ2J1dHRvbiwgaW5wdXQsIHRleHRhcmVhLCBzZWxlY3QsIFtyb2xlPSJidXR0b24iXScpKS5zbGljZSgwLCA4MCkubWFwKGVsID0+ICh7e3RhZzogZWwudGFnTmFtZS50b0xvd2VyQ2FzZSgpLCB0eXBlOiAoZWwuZ2V0QXR0cmlidXRlKCd0eXBlJykgfHwgJycpLnNsaWNlKDAsNDApLCBsYWJlbDogKGVsLmlubmVyVGV4dCB8fCBlbC5nZXRBdHRyaWJ1dGUoJ2FyaWEtbGFiZWwnKSB8fCBlbC5nZXRBdHRyaWJ1dGUoJ3BsYWNlaG9sZGVyJykgfHwgZWwuZ2V0QXR0cmlidXRlKCduYW1lJykgfHwgJycpLnRyaW0oKS5zbGljZSgwLDEyMCl9fSkpOwogIGNvbnN0IGxvd2VyID0gKGxvY2F0aW9uLmhyZWYgKyAnXFxuJyArIGRvY3VtZW50LnRpdGxlICsgJ1xcbicgKyB0ZXh0KS50b0xvd2VyQ2FzZSgpOwogIGNvbnN0IGdhdGVQYXR0ZXJucyA9IHt7CiAgICBjYXB0Y2hhOiBbJ2NhcHRjaGEnLCAncmVjYXB0Y2hhJywgJ2hjYXB0Y2hhJywgJ3ZlcmlmeSB5b3UgYXJlIGh1bWFuJywgJ3JvYm90IGNoZWNrJ10sCiAgICBvdHA6IFsnb25lLXRpbWUgY29kZScsICd2ZXJpZmljYXRpb24gY29kZScsICd0d28tZmFjdG9yJywgJzJmYScsICdtdWx0aS1mYWN0b3InLCAnYXV0aGVudGljYXRvciBjb2RlJ10sCiAgICBsb2dpbjogWydsb2cgaW4nLCAnc2lnbiBpbicsICdwYXNzd29yZCcsICdzc28nLCAnc2luZ2xlIHNpZ24tb24nXSwKICAgIHBob25lOiBbJ3Bob25lIG51bWJlcicsICdtb2JpbGUgbnVtYmVyJywgJ3NtcyddLAogICAgcGF5bWVudF9reWM6IFsncGF5bWVudCcsICdjcmVkaXQgY2FyZCcsICdiaWxsaW5nJywgJ2t5YycsICdpZGVudGl0eSB2ZXJpZmljYXRpb24nXSwKICAgIHNjYXJjZV9jbGFpbTogWydjbGFpbSB5b3VyIHNwb3QnLCAnY2xhaW0gaW52aXRhdGlvbicsICcxIHBlciAzMCBkYXlzJywgJ2xpbWl0ZWQgc3BvdCddCiAgfX07CiAgY29uc3QgZ2F0ZUZsYWdzID0ge3t9fTsKICBmb3IgKGNvbnN0IFtuYW1lLCBwYXRzXSBvZiBPYmplY3QuZW50cmllcyhnYXRlUGF0dGVybnMpKSBnYXRlRmxhZ3NbbmFtZV0gPSBwYXRzLnNvbWUocCA9PiBsb3dlci5pbmNsdWRlcyhwKSk7CiAgcmV0dXJuIEpTT04uc3RyaW5naWZ5KHt7b2s6IHRydWUsIHVybDogbG9jYXRpb24uaHJlZiwgdGl0bGU6IGRvY3VtZW50LnRpdGxlLCB0ZXh0X2NoYXJzOiB0ZXh0Lmxlbmd0aCwgdGV4dDogdGV4dC5zbGljZSgwLCBtYXhDaGFycyksIGxpbmtzOiBzYW1wbGVMaW5rcywgY29udHJvbHMsIGdhdGVfZmxhZ3M6IGdhdGVGbGFnc319KTsKfX0pKCkKIiIiCmpzID0ganNfdGVtcGxhdGUuZm9ybWF0KG1heF9jaGFycz1tYXhfY2hhcnMpCmNtZCA9IHsiaWQiOiAxLCAibWV0aG9kIjogIlJ1bnRpbWUuZXZhbHVhdGUiLCAicGFyYW1zIjogeyJleHByZXNzaW9uIjoganMsICJyZXR1cm5CeVZhbHVlIjogVHJ1ZSwgImF3YWl0UHJvbWlzZSI6IFRydWV9fQp3c19zZW5kX3RleHQoanNvbi5kdW1wcyhjbWQpKQp3aGlsZSBUcnVlOgogICAgbXNnID0ganNvbi5sb2Fkcyh3c19yZWN2X3RleHQoKSkKICAgIGlmIG1zZy5nZXQoImlkIikgPT0gMToKICAgICAgICBicmVhawp0cnk6CiAgICB2YWwgPSBtc2dbInJlc3VsdCJdWyJyZXN1bHQiXS5nZXQoInZhbHVlIikKICAgIGRhdGEgPSBqc29uLmxvYWRzKHZhbCkKZXhjZXB0IEV4Y2VwdGlvbiBhcyBleGM6CiAgICBwcmludChqc29uLmR1bXBzKHsib2siOiBGYWxzZSwgImVycm9yIjogInJ1bnRpbWVfZXZhbF9wYXJzZV9mYWlsZWQiLCAiZGV0YWlsIjogc3RyKGV4Yyl9LCBlbnN1cmVfYXNjaWk9RmFsc2UpKQogICAgc3lzLmV4aXQoNikKcHJpbnQoanNvbi5kdW1wcyhkYXRhLCBlbnN1cmVfYXNjaWk9RmFsc2UsIGluZGVudD0yKSkK | base64 -d > /tmp/hermes_cdp_visible_text.py
python3 /tmp/hermes_cdp_visible_text.py
"@
        Invoke-KaliCommand $cmd
        exit $script:LastKaliExitCode
    }
    "cdp-click" {
        if (($Text -and $Selector) -or ((-not $Text) -and (-not $Selector))) { throw "Exactly one of -Text or -Selector is required for -Action cdp-click" }
        $localHelper = Join-Path $PSScriptRoot "cdp_browser_action.py"
        if (-not (Test-Path $localHelper)) { throw "Missing CDP action helper: $localHelper" }
        $helperPath = "/tmp/hermes_cdp_browser_action.py"
        Copy-ToKali $localHelper $helperPath
        if ($script:LastCopyExitCode -ne 0) { exit $script:LastCopyExitCode }
        if ($Text) {
            $encodedText = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Text))
            $argLine = "--text-b64 $encodedText"
        } else {
            $encodedSelector = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Selector))
            $argLine = "--selector-b64 $encodedSelector"
        }
        $cmd = $prelude + @"
if ! command -v python3 >/dev/null 2>&1; then echo python3_missing; exit 2; fi
python3 "$helperPath" $argLine
"@
        Invoke-KaliCommand $cmd
        exit $script:LastKaliExitCode
    }
    "cdp-fill" {
        if ((-not $Text) -or (-not $Selector)) { throw "-Text and -Selector are required for -Action cdp-fill. Do not use this for passwords, OTPs, tokens, cookies, or phone numbers." }
        $localHelper = Join-Path $PSScriptRoot "cdp_browser_action.py"
        if (-not (Test-Path $localHelper)) { throw "Missing CDP action helper: $localHelper" }
        $helperPath = "/tmp/hermes_cdp_browser_action.py"
        Copy-ToKali $localHelper $helperPath
        if ($script:LastCopyExitCode -ne 0) { exit $script:LastCopyExitCode }
        $encodedText = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Text))
        $encodedSelector = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Selector))
        $cmd = $prelude + @"
if ! command -v python3 >/dev/null 2>&1; then echo python3_missing; exit 2; fi
python3 "$helperPath" --selector-b64 $encodedSelector --fill-text-b64 $encodedText
"@
        Invoke-KaliCommand $cmd
        exit $script:LastKaliExitCode
    }
}
