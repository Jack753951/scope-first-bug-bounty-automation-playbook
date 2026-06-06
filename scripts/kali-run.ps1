param(
    [string]$Command,
    [string]$HostName,
    [string]$User,
    [int]$Port,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ConfigPath = Join-Path $ProjectRoot "setting\local\kali-ssh.json"

if (-not (Test-Path $ConfigPath)) {
    throw "Missing config: $ConfigPath"
}

$config = Get-Content -Raw -Encoding UTF8 $ConfigPath | ConvertFrom-Json
if (-not $HostName) { $HostName = $config.host }
if (-not $User) { $User = $config.user }
if (-not $Port) { $Port = [int]$config.port }

if (-not $HostName) {
    throw "Kali host is not configured. Edit setting/local/kali-ssh.json or pass -HostName."
}
if (-not $Command) {
    throw "Pass a command, for example: .\scripts\kali-run.ps1 -Command 'whoami && hostname'"
}

$identity = Join-Path $ProjectRoot $config.identityFile
$knownHosts = Join-Path $ProjectRoot $config.knownHostsFile
$remoteOutputDir = $config.remoteOutputDir

if (-not (Test-Path $identity)) {
    throw "Missing SSH identity file: $identity"
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $knownHosts) | Out-Null
$sshConfig = Join-Path (Split-Path -Parent $knownHosts) "empty_ssh_config"
if (-not (Test-Path $sshConfig)) {
    New-Item -ItemType File -Force -Path $sshConfig | Out-Null
}

function ConvertTo-BashSingleQuoted {
    param([string]$Value)
    $singleQuote = [string][char]39
    $replacement = $singleQuote + '"' + $singleQuote + '"' + $singleQuote
    return $singleQuote + $Value.Replace($singleQuote, $replacement) + $singleQuote
}

$remote = "$User@$HostName"
$normalizedOutputDir = $remoteOutputDir
if ($normalizedOutputDir -eq "~") {
    $normalizedOutputDir = "/home/$User"
} elseif ($normalizedOutputDir.StartsWith("~/")) {
    $normalizedOutputDir = "/home/$User/" + $normalizedOutputDir.Substring(2)
}
$normalizedCommand = $Command -replace "`r`n", "`n" -replace "`r", "`n"
$quotedOutputDir = ConvertTo-BashSingleQuoted $normalizedOutputDir
$quotedCommand = ConvertTo-BashSingleQuoted $normalizedCommand
$remoteCommand = "mkdir -p $quotedOutputDir && cd $quotedOutputDir && bash -lc $quotedCommand"
$sshArgs = @(
    "-F", $sshConfig,
    "-i", $identity,
    "-p", "$Port",
    "-o", "UserKnownHostsFile=$knownHosts",
    "-o", "StrictHostKeyChecking=accept-new",
    $remote,
    $remoteCommand
)

if ($DryRun) {
    Write-Host "[DRY RUN] ssh $($sshArgs -join ' ')" -ForegroundColor Yellow
    exit 0
}

& ssh.exe @sshArgs
exit $LASTEXITCODE
