> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Kali shared-repo mount and dirty-tree hygiene

Use when this user's cybersec lab is controlled from Windows/Git-Bash while Kali is the tool VM and the shared repo or working tree blocks progress.

## Shared-folder mount recovery pattern

Symptoms:
- Windows/VirtualBox shows a shared folder mapping, but Kali cannot `cd /mnt/hacking` or `/media/sf_hacking`.
- Paths appear owned by `root:root` or return permission denied.
- The Kali user is already in `vboxsf`, but the current session/mount still fails.
- `sudo -n` fails, so agent-side noninteractive sudo is unavailable.

Safe sequence:
1. Verify from Windows control plane which VM and mapping are intended. Prefer the project wrapper if present, e.g. `scripts/kali-run.ps1`, for read-only setup checks.
2. If the VM is running/locked, a machine-level persistent VirtualBox mapping may not be editable. A transient mapping can be added for the current running VM, but guest-side mount still needs sudo or reboot/login refresh.
3. Do not guess or pipe a sudo password. Ask the operator to run the minimal guest-side mount commands manually:

```bash
sudo mkdir -p /mnt/hacking
sudo mount -t vboxsf -o uid=$(id -u),gid=$(id -g),umask=002 hacking /mnt/hacking
cd /mnt/hacking
pwd
git status --short | head
```

4. If manual mount works, optionally restore the expected convenience symlink:

```bash
mkdir -p ~/projects
ln -sfn /mnt/hacking ~/projects/cybersec
cd ~/projects/cybersec
pwd
git status --short | head
```

5. Only after the manual mount succeeds, discuss persistence. Avoid duplicate `/etc/fstab` lines:

```bash
grep -n 'hacking /mnt/hacking' /etc/fstab || true
echo 'hacking /mnt/hacking vboxsf uid=1000,gid=1000,umask=002 0 0' | sudo tee -a /etc/fstab
```

6. Re-verify from Windows control plane:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-run.ps1' -Command 'cd /mnt/hacking && pwd && git status --short | head'
```

## Dirty working tree cleanup pattern

When a cybersec lab repo has many modified/untracked artifacts after long multi-agent work, do not use broad cleanup commands.

Safe classification order:
1. `modified` rolling/current files — inspect diff first. Decide restore vs named artifact vs commit.
2. Durable code/tests/fixtures — likely commit candidates if they are project-owned and validated (`modules/**`, `scripts/**`, `tests/**`, `tests/fixtures/**`).
3. Durable handoff/review/report records — preserve unless clearly generated trash; batch commits by milestone/topic.
4. Rolling handoff pointers (`handoff/cowork_task.md`, `handoff/claude_code_task.md`, `handoff/claude_code_result.md`) — if important, copy/archive as named artifacts, then restore or update intentionally.
5. Temp/recon garbage — delete only when clearly disposable and not evidence/sensitive/locked; otherwise use narrow ignore + operator inspection.

Guardrails:
- Never run `git add .` in this workspace during cleanup.
- Never delete `reports/`, `handoff/`, `modules/`, scan outputs, or review artifacts merely to reduce `git status` noise.
- Keep explicit staging lists and small commits: code/tests first, durable handoff/report records second, rolling pointers last.
- Before committing, run a diff review and at least a lightweight secret/sensitive-artifact check appropriate to the changed paths.
- After cleanup, run the project review wrapper from the correct control plane, e.g. `HACKLAB=<user-home> USER=Owner ./bin/hermes review` from Windows/Git-Bash, or the Kali wrapper once `/mnt/hacking` is fixed.

## Operator-facing style

When asking the operator to perform the sudo-only part, give a short diagnosis, then exact copy-paste commands and expected output. Separate what the agent already did from what needs human sudo. Do not bury the required commands under a long narrative.