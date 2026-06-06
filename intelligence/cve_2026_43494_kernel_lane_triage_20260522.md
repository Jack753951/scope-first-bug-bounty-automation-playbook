> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <specific-cve-id> Kernel Lane Triage

Status: partial / candidate likely-applicable; crash/LPE testing deferred
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> VirtualBox snapshot attempt -> SSH to `<victim-vm>` for non-destructive checks
Visible model/runtime: current Hermes session; no Claude/Codex worker usage artifact

## Question answered

With operator-approved snapshot/clone authority, <specific-cve-id> can move into a kernel/local test lane, but only after the VM recovery/snapshot gate is healthy.

Current state:

- Non-destructive triage: completed on `<victim-vm>`.
- Patch/applicability mapping: completed from NVD/kernel.org references.
- Crash/LPE/reproducer testing: **not run**.
- Reason: `<attacker-vm>` live snapshot attempt entered VirtualBox `livesnapshotting` state and SSH became unreachable. The agent is blocked by platform safety rules from issuing VM shutdown/poweroff, so operator manual recovery is required before destructive kernel testing.

## Upstream vulnerability facts

CVE: `<specific-cve-id>`

NVD source:

- Published: `2026-05-21T12:16:19.957`
- Last modified: `2026-05-21T16:16:23.157`
- Source: `kernel.org`

Upstream stable commit:

- `e174929793195e0cd6a4adb0cad731b39f9019b4`
- Subject: `net/rds: reset op_nents when zerocopy page pin fails`
- Author date: `2026-05-05 16:43:36 -0700`
- Committer date: `2026-05-11 17:20:02 -0700`
- Fixes: `0cebaccef3ac ("rds: zerocopy Tx support.")`

Patch essence:

```diff
for (i = 0; i < rm->data.op_nents; i++)
        put_page(sg_page(&rm->data.op_sg[i]));
+rm->data.op_nents = 0;
mmp = &rm->data.op_mmp_znotifier->z_mmp;
```

Bug class:

- RDS zerocopy send error-path cleanup bug.
- If `iov_iter_get_pages2()` fails in `rds_message_zcopy_from_user()`, pages are released but `rm->data.op_nents` remains non-zero.
- Later `rds_message_purge()` cleanup can iterate stale entries and release again.
- Practical impact remains candidate-only locally until a safe reproducer and snapshot/clone recovery path are confirmed.

## Local victim-lab precondition result

Host: `<victim-vm>` / `<lab-ip>`

Kernel:

```text
6.18.12+kali-amd64
Linux kali 6.18.12+kali-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.18.12-1kali1 (2026-02-25) x86_64 GNU/Linux
```

Kernel package:

```text
linux-image-6.18.12+kali-amd64  6.18.12-1kali1
linux-image-amd64               6.18.12-1kali1
```

RDS config:

```text
CONFIG_RDS=m
CONFIG_RDS_RDMA=m
CONFIG_RDS_TCP=m
# CONFIG_RDS_DEBUG is not set
```

RDS module state:

```text
RDS module file exists: yes
RDS loaded: no
```

Module files:

```text
/lib/modules/6.18.12+kali-amd64/kernel/net/rds/rds.ko.xz
/lib/modules/6.18.12+kali-amd64/kernel/net/rds/rds_tcp.ko.xz
/lib/modules/6.18.12+kali-amd64/kernel/net/rds/rds_rdma.ko.xz
```

Installed headers/source did not include full `net/rds/message.c`, so local source-tree patch presence could not be directly verified from `/usr/src/linux-headers-*`.

## Applicability assessment

Assessment: **likely locally relevant but not proven exploitable**.

Reasons:

1. The installed Kali kernel package build date is `2026-02-25`, before the upstream stable fix commit dated `2026-05-11`.
2. RDS is built as a loadable module (`CONFIG_RDS=m`) and module files are present.
3. RDS is not currently loaded, so the vulnerable code path is not exposed until module load/autoload and usable socket/precondition path are confirmed.
4. No crash/LPE reproducer has been run.

Confidence:

- Component presence: high.
- Patch-not-present likelihood: medium-high from dates, but not binary-proven.
- Exploitability: unknown.

## Snapshot/recovery gate status

Attempted live snapshot on `<attacker-vm>`:

- Snapshot name: `pre_CVE-2026-43494_kernel_lane_20260522T062454Z`
- VirtualBox listed the snapshot node, but VM remained in `VMState="livesnapshotting"`.
- SSH to `<lab-ip>:22` timed out after snapshot hang.
- VBox log showed transition to `LiveSnapshotting` / `RUNNING_LS` and guest heartbeat flatline.

Agent limitation:

- The agent's terminal tool blocks shutdown/reboot/poweroff commands, so it cannot recover the stuck VM directly.

Required operator recovery before destructive kernel testing:

```powershell
# Run in Windows PowerShell, not Git-Bash.
VBoxManage showvminfo "<attacker-vm>" --machinereadable | Select-String 'VMState|SnapshotName|SnapshotUUID|CurrentSnapshot'

# If still stuck in livesnapshotting and the GUI cannot recover it, power it off from VirtualBox UI
# or run, only after accepting loss of the live in-memory state:
VBoxManage controlvm "<attacker-vm>" poweroff

# Then start it again:
VBoxManage startvm "<attacker-vm>" --type headless
```

After it boots, verify:

```powershell
# From project directory on Windows PowerShell if using local tools, or let Hermes verify via SSH afterward.
```

## Allowed next kernel-lane steps after recovery

Safe next steps, in order:

1. Recover `<attacker-vm>` from stuck `livesnapshotting`.
2. Prefer powered-off clone or powered-off snapshot for kernel tests, not live snapshot.
3. Verify clone boots and SSH works.
4. On clone only, perform module-load/precondition check:
   - `modprobe rds`
   - confirm `/proc/modules`
   - check whether unprivileged `socket(AF_RDS, SOCK_SEQPACKET, 0)` can trigger/use RDS
5. Only if clone recovery is proven, consider a crash reproducer if a source-reviewed reproducer exists.

Blocked until clone/snapshot recovery is healthy:

- RDS fuzzing.
- Any crash reproducer.
- Any LPE PoC.
- Any attempt to trigger the double-free condition intentionally.

## Artifacts

- `<artifact-output-dir>/cve_2026_43494_kernel_lane_20260522/nvd_cve_2026_43494.json`
- `<artifact-output-dir>/cve_2026_43494_kernel_lane_20260522/kernel_commit_e174929793195e0cd6a4adb0cad731b39f9019b4.html`
- `<artifact-output-dir>/cve_2026_43494_kernel_lane_20260522/e174929793195e0cd6a4adb0cad731b39f9019b4.patch`
- `<artifact-output-dir>/cve_2026_43494_kernel_lane_20260522/victim_rds_precondition_no_module_load.txt`
- `<artifact-output-dir>/cve_2026_43494_kernel_lane_20260522/victim_kernel_source_message_c_check.txt`
