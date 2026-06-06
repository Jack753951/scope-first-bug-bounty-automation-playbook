param(
    [string[]]$Tools = @(
        "nmap",
        "nikto",
        "sqlmap",
        "gobuster",
        "ffuf",
        "nuclei",
        "masscan",
        "msfconsole",
        "hydra",
        "john",
        "hashcat",
        "burpsuite",
        "zaproxy"
    ),
    [string]$HostName,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$KaliRun = Join-Path $ScriptDir "kali-run.ps1"

if (-not (Test-Path $KaliRun)) {
    throw "Missing helper: $KaliRun"
}

$toolList = ($Tools | ForEach-Object { $_.Replace("'", "'\''") }) -join " "
$remoteCommand = @"
set -e
printf 'host: '; hostname
printf 'kernel: '; uname -a
printf 'os: '; (grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null || true)
for t in $toolList; do
  if command -v "`$t" >/dev/null 2>&1; then
    echo "`$t `$(command -v "`$t")"
  else
    echo "`$t missing"
  fi
done
"@

$kaliParams = @{ Command = $remoteCommand }
if ($HostName) { $kaliParams.HostName = $HostName }
if ($DryRun) { $kaliParams.DryRun = $true }

& $KaliRun @kaliParams
exit $LASTEXITCODE
