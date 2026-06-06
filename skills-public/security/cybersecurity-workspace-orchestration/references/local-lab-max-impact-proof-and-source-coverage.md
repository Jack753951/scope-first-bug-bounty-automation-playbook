> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Local Lab Max-Impact Proofs and Source Coverage

Use this reference when the operator asks for offensive/defensive lab work that should prioritize a single vulnerability producing the maximum safe, recoverable impact.

## Operator preference captured

The operator wants recoverable local靶機 testing to emphasize:

- one-vulnerability, maximum-impact proofs;
- control evidence when safe: server-side command execution, execution identity, marker-file write/readback, and callback/control evidence;
- attack-style scripts where appropriate, but bounded to intentionally vulnerable/local lab targets;
- explicit truth-labeling: do not claim callback/control unless an artifact proves it;
- wrap-ups that state project benefit and newly created/changed files.

## Safety boundary for this class of work

Allowed in local/recoverable lab only:

1. marker-only command execution proof, e.g. `id`, `whoami`, and `/tmp/HERMES_*` marker write/readback;
2. disposable container or VM target lanes;
3. isolated callback listeners on host-only/Docker lab networks;
4. destructive-impact drills only against lab-owned marker paths or disposable data, with pre/post/recovery evidence;
5. snapshot/recovery gates before kernel, destructive, or crash-prone tests.

Do not create or normalize real-world malware behavior:

- no credential theft;
- no public-target C2;
- no persistence/backdoors;
- no production data destruction;
- no OS-destruction drills without explicit disposable snapshot/recovery approval.

## Evidence pattern

For a verified max-impact proof, collect and label:

- target and scope: local lab, CTF/training, user-owned, or written authorization;
- route/tool: e.g. Windows Hermes -> SSH/SCP -> aggressive-lab -> victim-lab Docker target;
- vulnerability used: one primary vulnerability per proof;
- execution identity: `id`, `whoami`, process/container context;
- marker file path and value;
- callback listener log, if any;
- cleanup/restore status;
- exact limitation labels, e.g. `Docker-bridge callback, not true attacker-VM callback`.

## Callback truth-labeling

A callback is verified only if a listener artifact contains the run marker.

Label precisely:

- `true attacker-side callback`: listener on the attacker VM receives the marker;
- `Docker-bridge local callback`: target container calls a controlled listener container on the same victim host/bridge;
- `attempted but blocked`: listener was unreachable or no artifact was recorded.

Do not promote `attempted` to `verified`.

## Practical Docker callback route

If the attacker VM only has SSH inbound and no Docker runtime, a Docker-bridge callback on victim-lab can prove outbound behavior but is not a true attacker callback. To upgrade to true attacker-side callback:

1. temporarily enable NAT for package/image pulls;
2. install Docker runtime on the attacker VM (`docker.io` and, on Kali, `docker-compose` if available);
3. run a Docker-published callback listener on the attacker VM, bound to the host-only interface/port;
   - a minimal reusable pattern is `php:8.2-apache` with `callback.php` writing JSONL to `/tmp/requests.jsonl`;
   - bind to the attacker host-only IP (e.g. `-p <lab-ip>:18182:80`), not all interfaces unless explicitly needed;
   - if bound to the host-only IP, `curl 127.0.0.1:<port>` on the attacker may fail; verify from the victim host/IP instead;
4. verify victim-lab can reach `http://<attacker-hostonly-ip>:<port>/...` before rerunning the exploit;
5. rerun the max-impact proof and require a matching marker in listener logs;
   - for runners that also start a built-in listener, add/enable an external-listener mode such as `USE_LOCAL_CALLBACK_LISTENER=0` to avoid port collisions and misleading local callback counts;
6. copy the Docker listener log into the run artifact before cleanup;
7. remove disposable containers;
8. turn NAT back off and verify host-only lab connectivity remains.

## Source-family coverage inventory pattern

When asked whether requested vulnerability sources are covered, inventory by source family and status, not just raw file count:

- OWASP / intentionally vulnerable labs: verified bundles and lab flows;
- CISA KEV: catalog/pattern mapping, usually candidate unless product/version is present;
- NVD / CVE: current records and local applicability notes;
- Exploit-DB: reference acquisition; do not raw-run public exploit scripts by default;
- GitHub security tools/repos: acquired tools/references and any bounded tool use;
- HTB / HackTheBox: concrete machine/challenge runs only count when an artifact exists.

A good inventory labels each row as `verified`, `candidate`, `reference-only`, or `not yet run`, and points to repo handoff/artifact paths.

## CVE kernel-lane handling

Kernel CVEs such as Linux RDS double-free candidates belong in a separate kernel/local lane, not the web-app exploit lane.

First-stage checks should be non-destructive:

- kernel version on each lab VM;
- package version;
- module file presence;
- module loaded/not loaded;
- upstream patch/reference links;
- snapshot/recovery requirement before loading/fuzzing/testing crash or LPE behavior.
