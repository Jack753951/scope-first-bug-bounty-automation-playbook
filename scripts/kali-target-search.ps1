param(
    [Parameter(Mandatory=$true)]
    [string]$Url,
    [string]$ProfileName = "target-search",
    [int]$WaitSeconds = 7,
    [int]$MaxTextChars = 12000,
    [switch]$ResetBrowser,
    [switch]$SkipNatEnable,
    [switch]$CloseNatAfter,
    [switch]$NoScreenshot
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BaseOutDir = Join-Path $ProjectRoot "<artifact-output-dir>\browser_state"

function ConvertTo-SafeName {
    param([string]$Value)
    if (-not $Value) { return "target-search" }
    return ($Value -replace '[^A-Za-z0-9_.-]', '_')
}

function Invoke-RepoPowerShellScript {
    param([string]$ScriptName, [string[]]$ArgsList)
    $scriptPath = Join-Path $PSScriptRoot $ScriptName
    & powershell -NoProfile -ExecutionPolicy Bypass -File $scriptPath @ArgsList
    return $LASTEXITCODE
}

function Write-TextFileUtf8 {
    param([string]$Path, [string[]]$Lines)
    $parent = Split-Path -Parent $Path
    if ($parent) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }
    [System.IO.File]::WriteAllText($Path, ($Lines -join [Environment]::NewLine) + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
}

function Sanitize-VisibleText {
    param([string[]]$Lines)
    $redacted = New-Object System.Collections.Generic.List[string]
    foreach ($line in $Lines) {
        $s = [string]$line
        $s = $s -replace '(?i)(cookie|token|authorization|bearer|password|passwd|secret|otp|verification code)(\s*[:=]\s*)\S+', '$1$2[REDACTED]'
        $s = $s -replace '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[EMAIL_REDACTED]'
        $s = $s -replace '(?<!\d)\+?\d[\d .()\-]{7,}\d(?!\d)', '[PHONE_REDACTED]'
        $redacted.Add($s)
    }
    return $redacted.ToArray()
}

$safeProfile = ConvertTo-SafeName $ProfileName
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ")
$OutDir = Join-Path $BaseOutDir ("${safeProfile}_${timestamp}")
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$transcript = New-Object System.Collections.Generic.List[string]
$manifest = [ordered]@{
    schema_version = "kali_target_search/0.1"
    created_at = $timestamp
    url = $Url
    profile = $safeProfile
    output_dir = $OutDir
    actions = @("open", "wait", "cdp-visible-text", "screenshot", "downloads", "sanitize")
    artifacts = [ordered]@{}
    safety = "Passive browser target-search capture only. No secrets are intentionally captured; visible text is sanitized before durable output."
}

Push-Location $ProjectRoot
try {
    $passiveArgs = @("-Url", $Url, "-ProfileName", $safeProfile, "-MaxTextChars", "$MaxTextChars")
    if ($ResetBrowser) { $passiveArgs += "-ResetBrowser" }
    if ($SkipNatEnable) { $passiveArgs += "-SkipNatEnable" }
    # Keep NAT/session open for follow-up unless caller explicitly asks to close after the full wrapper finishes.

    $transcript.Add("== passive open + cdp-visible-text ==")
    $visibleOutput = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "kali-passive-browse.ps1") @passiveArgs 2>&1
    $visibleExit = $LASTEXITCODE
    $transcript.AddRange([string[]]$visibleOutput)
    Write-TextFileUtf8 -Path (Join-Path $OutDir "cdp-visible-text.raw.txt") -Lines ([string[]]$visibleOutput)
    $sanitized = Sanitize-VisibleText ([string[]]$visibleOutput)
    Write-TextFileUtf8 -Path (Join-Path $OutDir "cdp-visible-text.sanitized.txt") -Lines $sanitized
    $manifest.artifacts["cdp_visible_text_raw"] = "cdp-visible-text.raw.txt"
    $manifest.artifacts["cdp_visible_text_sanitized"] = "cdp-visible-text.sanitized.txt"
    if ($visibleExit -ne 0) { throw "kali-passive-browse.ps1 failed with exit code $visibleExit" }

    if ($WaitSeconds -gt 0) { Start-Sleep -Seconds $WaitSeconds }

    if (-not $NoScreenshot) {
        $transcript.Add("== screenshot ==")
        $shotOutput = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "kali-browser-ops.ps1") -Action screenshot -ProfileName $safeProfile -LocalOutDir $OutDir 2>&1
        $shotExit = $LASTEXITCODE
        $transcript.AddRange([string[]]$shotOutput)
        Write-TextFileUtf8 -Path (Join-Path $OutDir "screenshot.stdout.txt") -Lines ([string[]]$shotOutput)
        $shotLine = ([string[]]$shotOutput | Where-Object { $_ -match '^screenshot_local_path=' } | Select-Object -Last 1)
        if ($shotLine) { $manifest.artifacts["screenshot"] = (Split-Path -Leaf ($shotLine -replace '^screenshot_local_path=', '')) }
        if ($shotExit -ne 0) { $manifest.artifacts["screenshot_error"] = "exit_$shotExit" }
    }

    $transcript.Add("== downloads ==")
    $downloadOutput = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "kali-browser-ops.ps1") -Action downloads -ProfileName $safeProfile 2>&1
    $downloadExit = $LASTEXITCODE
    $transcript.AddRange([string[]]$downloadOutput)
    Write-TextFileUtf8 -Path (Join-Path $OutDir "downloads.txt") -Lines ([string[]]$downloadOutput)
    $manifest.artifacts["downloads_metadata"] = "downloads.txt"
    if ($downloadExit -ne 0) { $manifest.artifacts["downloads_error"] = "exit_$downloadExit" }

    Write-TextFileUtf8 -Path (Join-Path $OutDir "transcript.txt") -Lines $transcript.ToArray()
    $manifest.artifacts["transcript"] = "transcript.txt"
    $manifest.status = "ok"
} catch {
    $manifest.status = "error"
    $manifest.error = $_.Exception.Message
    Write-TextFileUtf8 -Path (Join-Path $OutDir "transcript.txt") -Lines $transcript.ToArray()
    $manifest.artifacts["transcript"] = "transcript.txt"
    throw
} finally {
    $manifestPath = Join-Path $OutDir "manifest.json"
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -Path $manifestPath -Encoding UTF8
    if ($CloseNatAfter) {
        $VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
        if (Test-Path $VBoxManage) {
            & $VBoxManage controlvm "<attacker-vm>" setlinkstate2 off | Out-Null
            & $VBoxManage controlvm "<attacker-vm>" nic2 null | Out-Null
        }
    }
    Pop-Location
}

Write-Output "target_search_output_dir=$OutDir"
Write-Output "manifest=$manifestPath"
