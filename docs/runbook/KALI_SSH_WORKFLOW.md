> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Kali SSH Workflow

This workspace is configured so Hermes and Codex stay on Windows while Kali runs security tools over SSH.

## Local Files

- SSH config: `setting/local/kali-ssh.json`
- Example config: `setting/local/kali-ssh.example.json`
- Private key: `setting/local/ssh/kali_codex_ed25519`
- Public key: `setting/local/ssh/kali_codex_ed25519.pub`
- Local output folder: `<artifact-output-dir>/`

The private key and output folder are ignored by `.gitignore`.

## One-Time Kali Setup

Start Kali, find its IP, and make sure SSH is running:

```bash
ip addr
sudo systemctl enable --now ssh
```

Option A: install the public key from Windows. This asks for the Kali user's password once:

```powershell
.\scripts\kali-install-key.ps1 -HostName KALI_IP -User kali
```

Option B: on Kali, add the public key from Windows to:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Paste the content of `setting/local/ssh/kali_codex_ed25519.pub` as one line.

Then update `setting/local/kali-ssh.json` with the Kali IP.

## Test From Windows

```powershell
.\scripts\kali-run.ps1 -Command "whoami && hostname && command -v nmap"
.\scripts\kali-check-tools.ps1
```

## Run A Tool On Kali

Only run tools against labs, owned assets, or explicitly authorized scope.

```powershell
.\scripts\kali-run.ps1 -Command "nmap --version"
```

For scan outputs, write files under Kali's `~/codex-output`:

```powershell
.\scripts\kali-run.ps1 -Command "nmap -sV 127.0.0.1 -oA local-test"
.\scripts\kali-pull.ps1
```

Pulled files land in `<artifact-output-dir>/`. Review them before moving anything into `reports/` or `notes/`.
