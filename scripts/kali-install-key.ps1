param(
    [string]$HostName,
    [string]$User = "kali",
    [int]$Port = 22,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ConfigPath = Join-Path $ProjectRoot "setting\local\kali-ssh.json"
$PublicKeyPath = Join-Path $ProjectRoot "setting\local\ssh\kali_codex_ed25519.pub"

if (-not $HostName -and (Test-Path $ConfigPath)) {
    $config = Get-Content -Raw -Encoding UTF8 $ConfigPath | ConvertFrom-Json
    $HostName = $config.host
    if ($config.user) { $User = $config.user }
    if ($config.port) { $Port = [int]$config.port }
}

if (-not $HostName) {
    throw "Pass -HostName or set host in setting/local/kali-ssh.json."
}
if (-not (Test-Path $PublicKeyPath)) {
    throw "Missing public key: $PublicKeyPath"
}

$publicKey = (Get-Content -Raw -Encoding UTF8 $PublicKeyPath).Trim()
$remote = "$User@$HostName"
$remoteCommand = "mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && grep -qxF '$publicKey' ~/.ssh/authorized_keys || echo '$publicKey' >> ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys"

if ($DryRun) {
    Write-Host "[DRY RUN] ssh -p $Port $remote <install public key>" -ForegroundColor Yellow
    exit 0
}

& ssh.exe -p $Port $remote $remoteCommand
exit $LASTEXITCODE
