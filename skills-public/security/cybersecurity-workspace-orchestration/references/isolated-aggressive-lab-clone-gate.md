> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Isolated Aggressive Lab Clone Gate Notes

Use this note when moving from a normal Kali workspace VM to a separate aggressive attacker VM for local-lab testing.

## Durable workflow lessons

1. Full clone requires the source VM to be stopped or saved.
   - VirtualBox may fail `clonevm` on a running VM with `VBOX_E_INVALID_OBJECT_STATE`.
   - Prefer guest/ACPI shutdown first.
   - If ACPI shutdown does not complete and the operator approves preserving state, `controlvm <source> savestate` is safer than hard poweroff.

2. Treat a clone from a saved source as inheriting unsafe runtime state.
   - The clone can start as `VMState="saved"`.
   - Discard the clone saved state before applying isolation controls:
     ```bash
     VBoxManage discardstate '<lab-vm>'
     ```
   - Then apply host-only networking, no NAT, no shared folders, and disabled clipboard/drag-and-drop.

3. Remove inherited shared folders explicitly.
   - Full clones may inherit machine shared folders such as the project repo mapping.
   - Enumerate `SharedFolderNameMachineMapping*` and remove each mapping from the clone before aggressive testing.
   - Do not expose repo secrets or writable workspace folders into the aggressive VM unless separately reviewed.

4. Snapshot order matters.
   - Take the attacker clean snapshot while powered off after isolation settings are applied and before first risky use.
   - Victim running-state snapshots are useful for recovery, but for destructive tests prefer a powered-off clean snapshot or a known setup baseline.

5. Verify runtime isolation from inside the attacker, not only from VBox settings.
   - VBox settings should show host-only only (`nic1=hostonly`, later NICs `none`/disabled), disabled clipboard/drag-and-drop, and no shared folders.
   - From inside the attacker, verify the route table has only the host-only subnet and no default route.
   - Guest properties may temporarily show stale adapter records after clone/start; treat inside-guest `ip route` plus VBox NIC settings as the stronger proof.

6. Watch for host-only IP collisions.
   - A clone can keep the same static/DHCP host-only IP as the source VM.
   - Do not run the normal source Kali and `<lab-vm>` at the same time until one VM's host-only IP is changed.
   - If project SSH config points to the old Kali IP, it may now connect to the clone; label this clearly in handoff status.

## Minimal verification checklist

- Disk free space meets clone/snapshot threshold.
- Source VM saved or powered off; no hard poweroff unless explicitly approved.
- Clone exists and is full clone.
- Clone saved state discarded if inherited.
- Clone settings: host-only only, no NAT/bridged, no shared folders, clipboard disabled, drag-and-drop disabled, clipboard file transfers off at runtime where supported.
- Attacker clean snapshot created.
- Victim recovery/clean snapshot available.
- Attacker route table has no default route.
- Attacker can reach only the lab victim service needed for the run card.
- Handoff gate records IP-collision warning and script-specific review requirement before aggressive execution.
