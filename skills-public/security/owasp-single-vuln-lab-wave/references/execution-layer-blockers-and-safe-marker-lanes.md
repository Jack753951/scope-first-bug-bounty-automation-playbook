> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Execution-layer blockers and adjacent safe-marker lanes

Use when an authorized local-lab exploit-flow step is blocked by the agent/tool execution layer, especially for SSRF callback, XXE external callback, command-injection callback, deserialization gadget behavior, or private-IP callback triggers.

## Core rule

A local-lab safety blocker is not the end of capability growth, but it is also not a signal to disguise or retry the same payload. If the tool returns `BLOCKED` / `Do NOT retry`, do not encode, split, rename, hide in another script, or switch clients to execute the same blocked trigger.

Instead, immediately choose one of these routes and record the decision:

1. **Operator-run run-card**: generate exact manual instructions for the human operator to run in the authorized lab, with expected artifacts and cleanup.
2. **Source-level/integration proof**: test the vulnerable behavior inside a controlled fixture or unit/integration harness when that still proves the learning goal.
3. **Equivalent local靶機/lane**: add or modify a recoverable local VM/container/service to prove the same class safely.
4. **Adjacent safe-marker lane**: switch to a neighboring high-value proof type that builds the same evidence skill without bypassing the blocker.

## Session-derived pattern

A SSRF `fetch?url=http://<lab-ip>:18183/...` trigger was blocked by the execution layer even though the lab was local and authorized. The correct handling was:

- keep the SSRF attempt as `blocked/deferred`, not `verified-impact`;
- preserve useful setup artifacts: Docker-published callback listener, victim target, NAT-close verification, and route notes;
- do not retry the same trigger via encoding, Python, shell splitting, or hidden scripts;
- continue capability growth with an adjacent XXE safe-marker proof.

The follow-up XXE wave used a dedicated one-vulnerability runner with:

- OSS-first references: PayloadsAllTheThings XXE and OWASP XXE Prevention Cheat Sheet;
- lab-owned marker file only: `/tmp/hermes_modern_api_xxe_marker.txt`;
- positive XML file-entity request;
- no-entity and wrong-file controls;
- pre/post health;
- cleanup and NAT-closed verification;
- verdict `verified_impact_lab_only`.

## Docker-published route lesson

For this Windows/Hermes + two-Kali-VM lab, raw high-port host listeners may be unreachable between VMs even when the process is listening. Docker-published ports proved more reliable for cross-VM callback/target infrastructure:

- attacker listener: publish `<lab-ip>:<port> -> container:<port>`;
- victim target: publish `<lab-ip>:<port> -> container:<port>`;
- verify attacker-to-victim or victim-to-attacker reachability before claiming a proof;
- still close/verify NAT after image pulls or installs.

Do not generalize this into "host ports never work"; treat it as a route preference for this lab until revalidated.

## Good adjacent lanes after a callback blocker

- XXE safe-marker file entity proof with no-entity/wrong-file controls.
- Path traversal or file-read safe-marker proof.
- Browser-runtime XSS safe DOM marker with positive/control evidence.
- Bounded deserialization in-process marker proof, without shell, persistence, callback, or arbitrary command execution.
- Evidence-packet/report-readiness gate improvements.

## Required wording

When a blocker occurs, closeout must explicitly distinguish:

- `verified-impact`: runtime/impact proof exists and artifacts prove it;
- `blocked/deferred`: setup may be valuable, but the trigger was not executed or not observed;
- `attempted-not-verified`: the attempt ran but did not produce required marker/impact evidence.

Never turn setup success into impact claims.