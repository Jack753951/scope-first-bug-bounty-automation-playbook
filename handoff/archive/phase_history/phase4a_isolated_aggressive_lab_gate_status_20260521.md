> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A Isolated Aggressive Lab — Hermes Gate Status 2026-05-21

Updated: 2026-05-21 09:35:20 local

Status: SETUP_SLICE_READY_FOR_SCRIPT_SPECIFIC_REVIEW

## Authorization / scope posture

- Scope class: local lab / intentionally vulnerable app only.
- Target observed for this gate: `<victim-vm>` on host-only network, Juice Shop reachable at `http://<lab-ip>:3000/`.
- No public / bug-bounty / client targets are authorized by this gate.
- This gate does not authorize callbacks/OAST/reverse shells, credential attacks, persistence, stealth, malware, or external target interaction.

## Disk gate

Disk blocker is cleared:

```text
C: size 953G, used 776G, available 177G, use 82%
```

This satisfied the previous minimum (`80 GB`) and preferred (`150+ GB`) free-space gate for a full clone plus snapshots.

## VM actions completed by Hermes

### Source / normal Kali

- Source VM: `kali-linux-2026.1-virtualbox-amd64`.
- ACPI shutdown was requested but did not complete within the wait window.
- To avoid hard poweroff/data loss, Hermes used VirtualBox `savestate` on the source VM.
- Source VM is intentionally not running now, to avoid host-only IP collision with the cloned attacker.

### Attacker clone

Created full clone:

```text
<attacker-vm>
```

Clone settings verified:

```text
VMState=running
nic1=hostonly
hostonlyadapter1=VirtualBox Host-Only Ethernet Adapter
nic2=none
nic3=none
nic4=none
clipboard=disabled
draganddrop=disabled
no machine shared folder mapping shown after inherited `hacking` mapping was removed
```

Runtime sharing controls applied after start:

```text
clipboard mode disabled
clipboard filetransfers off
 draganddrop disabled
```

Attacker host-only identity observed via VirtualBox guest properties and SSH:

```text
attacker VM: <attacker-vm>
attacker IP: <lab-ip>
attacker hostname: kali
attacker route table: <lab-ip>/24 only; no default route observed
```

### Victim VM

Victim settings verified:

```text
VM: <victim-vm>
VMState=running
nic1=hostonly
hostonlyadapter1=VirtualBox Host-Only Ethernet Adapter
nic2=null
nic3=none
nic4=none
clipboard=disabled
draganddrop=disabled
```

Victim host-only identity observed:

```text
victim IP: <lab-ip>
```

Minimal lab health check from attacker to victim:

```text
curl -I http://<lab-ip>:3000/
HTTP/1.1 200 OK
```

## Snapshots

Attacker clone clean snapshot created while powered off before first boot:

```text
VM: <attacker-vm>
snapshot: clean-before-aggressive-tests-20260521-093233
purpose: clean attacker baseline; host-only only; no NAT; no shared folders; clipboard/drag-and-drop disabled
```

Victim recovery snapshots available:

```text
VM: <victim-vm>
existing setup snapshot: setup-complete-with-tools
new running-state recovery snapshot: pre-aggressive-current-running-recovery-20260521-093252
```

Note: the new victim snapshot was captured while the victim VM was running. For the strictest clean-room cycle before destructive tests, prefer reverting to `setup-complete-with-tools` or taking a powered-off victim snapshot after explicit operator approval.

## Current gate decision

Environment setup slice is complete.

Allowed next:

1. Select exactly one bounded aggressive lab script/class for the first test.
2. Write a script-specific run card with:
   - allowed request class;
   - rate cap;
   - timeout;
   - kill condition;
   - health check before/after;
   - evidence redaction/minimization;
   - recovery plan;
   - expected candidate-only output.
3. Run model/safety review of that specific run card.
4. Execute only if the script-specific review passes.

Not allowed yet:

- high-volume fuzzing without a request cap;
- brute force/credential spraying;
- callbacks/OAST/reverse shell/listener behavior;
- persistence/evasion/stealth;
- recursive download or loot collection;
- real bug-bounty/client/public targets;
- using the normal Kali VM as the aggressive attacker while the clone exists.

## Operational warning

`<attacker-vm>` currently uses the same host-only IP that the normal source Kali previously used (`<lab-ip>`). Do not run `kali-linux-2026.1-virtualbox-amd64` at the same time unless one VM's host-only IP is changed first.

## Suggested next slice

Recommended first script-specific slice:

```text
Phase 4A.1 — bounded local-lab content-discovery / path-enumeration rehearsal
```

Reason: it exercises aggressive-run gates such as request caps, timeout, health checks, and candidate-only output without immediately crossing into credential attacks, callbacks, exploit PoCs, or destructive state changes.
