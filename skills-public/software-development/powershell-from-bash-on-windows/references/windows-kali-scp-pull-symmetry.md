> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Windows-to-Kali SCP Pull Symmetry

Use this when a Windows/Git-Bash Hermes control plane pulls artifacts from a Kali VM with `scp.exe` after a Kali-side run.

## Lesson

If `ssh.exe` wrappers use a project-local empty SSH config (`-F <empty_ssh_config>`) to avoid a BOM-broken or otherwise invalid user `%USERPROFILE%\.ssh\config`, the matching `scp.exe` pull wrapper must use the same `-F` argument. It is not enough to harden only the run/SSH wrapper; artifact pulls can fail later even though the remote command executed successfully.

## Symmetric wrapper pattern

1. Create/locate the project-local known-hosts directory.
2. Ensure `empty_ssh_config` exists beside the known-hosts file.
3. Pass `-F $sshConfig` to both `ssh.exe` and `scp.exe`.
4. Keep identity, port, known-hosts, and strict-host-key options explicit.
5. Verify by pulling a small known artifact after a successful run.

PowerShell sketch:

```powershell
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $knownHosts) | Out-Null
$sshConfig = Join-Path (Split-Path -Parent $knownHosts) "empty_ssh_config"
if (-not (Test-Path $sshConfig)) {
    New-Item -ItemType File -Force -Path $sshConfig | Out-Null
}

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
& scp.exe @scpArgs
exit $LASTEXITCODE
```

## Pitfall

A failure like this during artifact pull is a wrapper-hardening issue, not proof the Kali run failed:

```text
Bad configuration option: \357\273\277host
terminating, 1 bad configuration options
scp: Connection closed
```

Patch the pull wrapper, re-pull the specific run directory, then continue with result review.
