param(
    [string]$RemotePath,
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
if (-not $RemotePath) { $RemotePath = "$($config.remoteOutputDir)/*" }

if (-not $HostName) {
    throw "Kali host is not configured. Edit setting/local/kali-ssh.json or pass -HostName."
}

$identity = Join-Path $ProjectRoot $config.identityFile
$knownHosts = Join-Path $ProjectRoot $config.knownHostsFile
$localOutputDir = Join-Path $ProjectRoot $config.localOutputDir

if (-not (Test-Path $identity)) {
    throw "Missing SSH identity file: $identity"
}

New-Item -ItemType Directory -Force -Path $localOutputDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $knownHosts) | Out-Null
$sshConfig = Join-Path (Split-Path -Parent $knownHosts) "empty_ssh_config"
if (-not (Test-Path $sshConfig)) {
    New-Item -ItemType File -Force -Path $sshConfig | Out-Null
}

$remote = "$User@$HostName`:$RemotePath"
$scpArgs = @(
    "-F", $sshConfig,
    "-i", $identity,
    "-P", "$Port",
    "-o", "UserKnownHostsFile=$knownHosts",
    "-o", "StrictHostKeyChecking=accept-new",
    "-r",
    $remote,
    $localOutputDir
)

if ($DryRun) {
    Write-Host "[DRY RUN] scp $($scpArgs -join ' ')" -ForegroundColor Yellow
    exit 0
}

& scp.exe @scpArgs
exit $LASTEXITCODE
