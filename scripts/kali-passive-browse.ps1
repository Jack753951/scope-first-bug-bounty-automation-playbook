param(
    [Parameter(Mandatory=$true)]
    [string]$Url,
    [string]$ProfileName = "passive-browse",
    [int]$MaxTextChars = 6000,
    [switch]$ResetBrowser,
    [switch]$SkipNatEnable,
    [switch]$CloseNatAfter
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
$VmName = "<attacker-vm>"

$script:LastRepoScriptExitCode = 0
function Invoke-RepoPowerShellScript {
    param([string]$ScriptName, [string[]]$ArgsList)
    $scriptPath = Join-Path $PSScriptRoot $ScriptName
    & powershell -NoProfile -ExecutionPolicy Bypass -File $scriptPath @ArgsList
    $script:LastRepoScriptExitCode = $LASTEXITCODE
}

function Test-KaliSsh {
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "kali-run.ps1") -Command 'echo ssh_ready && hostname' | Out-Host
    return ($LASTEXITCODE -eq 0)
}

function Ensure-KaliVm {
    if (-not (Test-KaliSsh)) {
        if (-not (Test-Path $VBoxManage)) { throw "Kali SSH failed and VBoxManage not found at $VBoxManage" }
        $running = & $VBoxManage list runningvms
        if ($running -notmatch [regex]::Escape($VmName)) {
            & $VBoxManage startvm $VmName --type headless | Out-Host
        }
        $ready = $false
        for ($i = 1; $i -le 30; $i++) {
            Start-Sleep -Seconds 5
            if (Test-KaliSsh) { $ready = $true; break }
        }
        if (-not $ready) { throw "Kali SSH did not become ready after VM start." }
    }
}

function Ensure-TemporaryNat {
    if ($SkipNatEnable) { return }
    if (-not (Test-Path $VBoxManage)) { return }
    $net = & $VBoxManage showvminfo $VmName --machinereadable
    if ($net -notmatch 'nic2="nat"' -or $net -notmatch 'cableconnected2="on"') {
        & $VBoxManage controlvm $VmName nic2 nat | Out-Null
        & $VBoxManage controlvm $VmName setlinkstate2 on | Out-Null
        Start-Sleep -Seconds 3
    }
}

function Close-TemporaryNat {
    if (-not (Test-Path $VBoxManage)) { return }
    & $VBoxManage controlvm $VmName setlinkstate2 off | Out-Null
    & $VBoxManage controlvm $VmName nic2 null | Out-Null
    $net = & $VBoxManage showvminfo $VmName --machinereadable
    $net | Select-String -Pattern 'nic2=|cableconnected2='
}

function Ensure-KaliInternetRoute {
    $probe = @'
ip route | grep '^default ' >/dev/null 2>&1 && curl -I --max-time 8 https://example.org >/dev/null 2>&1
'@
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "kali-run.ps1") -Command $probe | Out-Null
    if ($LASTEXITCODE -ne 0 -and -not $SkipNatEnable) {
        Ensure-TemporaryNat
        Start-Sleep -Seconds 3
        & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "kali-run.ps1") -Command $probe | Out-Null
    }
}

Push-Location $ProjectRoot
try {
    Ensure-KaliVm
    Ensure-KaliInternetRoute
    Invoke-RepoPowerShellScript "kali-vnc-control.ps1" @("-Action", "start") | Out-Null
    Invoke-RepoPowerShellScript "kali-browser-ops.ps1" @("-Action", "status")
    if ($ResetBrowser) {
        Invoke-RepoPowerShellScript "kali-browser-ops.ps1" @("-Action", "browser-reset")
    }
    Invoke-RepoPowerShellScript "kali-browser-ops.ps1" @("-Action", "open", "-Url", $Url, "-ProfileName", $ProfileName)
    Start-Sleep -Seconds 5
    Invoke-RepoPowerShellScript "kali-browser-ops.ps1" @("-Action", "cdp-visible-text", "-MaxTextChars", "$MaxTextChars")
    exit $script:LastRepoScriptExitCode
} finally {
    if ($CloseNatAfter) { Close-TemporaryNat }
    Pop-Location
}
