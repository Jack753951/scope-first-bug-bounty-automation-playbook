> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Lab continuation VM/route safety checks

Use this when the operator says to continue testing an existing two-VM local lab. It captures a reusable continuation pattern from a WebGoat/JWT continuation session.

## Trigger

- The previous session already selected a local lab lane, but current VM/runtime state may have drifted.
- Testing should continue from `<lab-vm>`/attacker to `<lab-vm>`/victim or their current concrete VM equivalents.
- The next step might involve scanners, exploit-flow probes, callbacks, or state-changing lab lesson endpoints.

## Continuation checklist

1. Recall current lane and handoff state before touching targets.
   - Confirm the active lab target and the next safe candidate lane.
   - Re-read scope if target-touching work is possible.

2. Resolve actual VM identity before starting anything.
   - Do not assume display names are stable. If the expected clone name is absent, map the operator-facing role (`attacker/aggressive`, `victim`) to the concrete VirtualBox VM names recorded in recent handoff/session state.
   - Report the mapping in the closeout so future continuation is less ambiguous.

3. Start only the needed local VMs and audit networking from inside the guest.
   - VirtualBox settings alone are not enough after saved-state/resume. Check guest `ip -4 -br addr` and `ip route` from the attacker VM.
   - If a NAT/default route is present during a host-only lab wave, close the extra NIC at VirtualBox and re-check from inside the guest.
   - Verify Internet is closed/unreachable before target-touching work resumes.

4. Use the project SSH wrapper pattern, not the user's global SSH config.
   - Prefer the project `kali-run.ps1`/configured SSH identity or an explicit empty SSH config (`ssh -F <project empty_ssh_config> ...`) so a malformed/BOM global `~/.ssh/config` does not derail lab continuation.
   - Treat the lesson as: isolate automation SSH from global user SSH config; do not encode the transient malformed config itself as a durable blocker.

5. Confirm the actual target service is alive before choosing the wave.
   - Ping only proves host-only reachability. Also check the expected service URLs from attacker to victim.
   - If only one target is alive (for example WebGoat up while Juice Shop/DVWA time out), route the wave to the alive target or stop and ask for target startup if that choice changes the task.

6. Respect safety-layer/user denial for exploit-shaped state changes.
   - If a planned next wave is blocked or denied, do not retry or rephrase to bypass. Summarize the low-risk checks already completed and ask for explicit approval/scope for the next bounded lab proof.

## Closeout fields to include

- Route/tool: control plane, VM mapping, attacker IP, victim IP.
- Visible runtime/model and usage artifact path when applicable.
- Safety boundary: local lab only, NAT/default route status, public-target exclusion.
- What was actually tested versus what was deferred/blocked.
- Artifact paths pulled back to the repo.
- `對專案有什麼幫助` and `新增/更新了什麼` sections.
