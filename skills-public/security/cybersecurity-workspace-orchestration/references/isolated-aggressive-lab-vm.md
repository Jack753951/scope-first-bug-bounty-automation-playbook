> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Isolated Aggressive Lab VM Pattern

Use this reference when the user wants to test more aggressive security scripts than ordinary low-risk lab browsing/enumeration.

## Recommendation

For low-risk Juice Shop / DVWA calibration, an existing Kali VM plus a local lab can be acceptable.

For aggressive scripts, create a separate isolated lab environment:

```text
Windows Host
├── Kali-main              # normal workspace / Hermes / repo / notes
├── <lab-vm>    # cloned attacker VM for risky scripts
└── Victim VM              # intentionally vulnerable target
```

Do not run aggressive testing from the normal work VM when the script may fuzz, brute force, exploit, write files, open listeners, pivot/proxy, invoke callbacks, or damage state.

## What counts as aggressive

Use an isolated VM/snapshot when testing:

- fuzzing or high-volume request generation;
- brute force / credential spraying patterns;
- exploit PoCs;
- RCE / command injection checks;
- file upload, path traversal, LFI/RFI checks;
- SSRF, webhook, callback, or OAST behavior;
- destructive or state-changing tests;
- proxy/pivot/tunnel/reverse-shell/listener flows;
- scripts that create users, alter configs, persist files, or collect loot-like data.

## VirtualBox setup shape

Preferred network choices:

1. Most isolated: `Internal Network` shared only by attacker and victim VMs.
2. Practical lab mode: `Host-only Adapter` shared by attacker and victim VMs.
3. NAT only for temporary updates; disable it during risky tests when possible.
4. Avoid bridged mode for victim VMs unless there is a specific reviewed reason.

Hardening defaults:

- Full Clone rather than Linked Clone.
- Generate new MAC addresses.
- Disable shared clipboard.
- Disable drag-and-drop.
- Disable clipboard file transfers on VirtualBox 7.x.
- Avoid shared folders; if needed, make them read-only and never expose secrets.
- Take a clean snapshot before aggressive tests.
- Revert snapshot between risky test cycles.

## VirtualBox CLI commands from Git-Bash/MSYS

Use the native VBoxManage path on this Windows/Git-Bash host:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' list vms
```

Clone an existing Kali VM as a full clone:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' clonevm 'SOURCE_VM_NAME' \
  --name '<lab-vm>' \
  --mode all \
  --register
```

After cloning, set fresh MAC and safer networking:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' modifyvm '<lab-vm>' --macaddress1 auto
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' modifyvm '<lab-vm>' \
  --nic1 hostonly \
  --hostonlyadapter1 'VirtualBox Host-Only Ethernet Adapter'
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' modifyvm '<lab-vm>' --nic2 none
```

Disable sharing features persistently while powered off:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' modifyvm '<lab-vm>' \
  --clipboard disabled \
  --draganddrop disabled
```

For a running VM on VirtualBox 7.x, runtime controls are:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' clipboard mode disabled
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' clipboard filetransfers off
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' controlvm '<lab-vm>' draganddrop disabled
```

Create a clean snapshot:

```bash
'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe' snapshot '<lab-vm>' take 'clean-before-aggressive-tests'
```

## Phase 4A gate wording

Before running aggressive scripts, record:

- exact attacker VM;
- exact victim VM / target URL/IP;
- network mode and proof it is lab-only;
- allowed action classes;
- explicitly forbidden classes;
- rate limits, timeouts, kill switch, and stop conditions;
- snapshot name;
- evidence minimization/redaction rules.

Keep outputs candidate-only. Aggressive lab success is measured by workflow calibration and safety controls, not by exploit count.

## Pitfalls

- Do not confuse VM isolation with authorization. Scope gate still applies.
- Do not put the victim VM on bridged LAN/public network for convenience.
- Do not store real credentials or personal files in victim VMs.
- Do not share the project repo or secrets into the aggressive VM unless read-only and explicitly needed.
- Do not test callbacks/OAST/reverse-shell behavior without a separate explicit review and lab-only routing plan.