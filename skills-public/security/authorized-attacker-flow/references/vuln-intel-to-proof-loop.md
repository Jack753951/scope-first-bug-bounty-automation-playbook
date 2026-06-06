> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Vuln-intel to proof-pattern loop

Use when the operator asks for automation that starts from latest vulnerabilities and should eventually inform live-target hunting.

Durable lesson: do not stop at a vulnerability-intel coverage diff if the requested workflow is a full loop. The minimum useful offline automation rung is:

```text
latest vuln intel -> proof bundle coverage diff -> local-lab run-card -> proof-pattern draft -> live-target prerequisite map
```

## Correct stage boundaries

1. Latest vuln intake
   - Fetch/consume public advisory metadata only.
   - Classify candidate routing: local bootstrap, bundle update, authorized live target needed, reference only, low signal.
   - No scanner, PoC, browser/noVNC, account action, callback, or target request.

2. Proof-library coverage diff
   - Index local `modules/bundles/*.md` by vuln class, maturity, CVE/GHSA refs, product refs, last verified, and safe proof posture.
   - Emit machine-readable and Markdown delta artifacts.
   - Cap recommendations to avoid backlog sprawl.

3. Local-lab run-card generation
   - Generate a plan-only run-card for a disposable/recoverable local 靶機 or fixture.
   - Require local posture, pre/post health, cleanup/recovery, synthetic data, and explicit operator gate before any execution.
   - Never run against live targets or public IPs/domains from this stage.

4. Proof-pattern draft
   - Create a draft bundle/pattern artifact, but label it `draft / not verified` until local evidence exists.
   - Do not add it to the verified proof library based on metadata alone.

5. Live-target prerequisite map
   - Translate the candidate or local proof idea into future live prerequisites: scope/rules, owned accounts/objects, A/B controls, callback allowance, redaction, stop-before rules.
   - This is not live authorization.

## Pitfall

If the user asks for `latest漏洞 -> 本地靶機測試 -> PROOF PATTERN -> PROOF PATTERN LIBRARY -> LIVE TARGET`, a response that only implements `vuln-intel -> bundle diff` is incomplete. Add the non-executing bridge artifacts even when local execution is not yet authorized.

## Continuation into verified local proof

When the operator explicitly asks to continue from a metadata-only proof loop into a Kali/local 靶機 proof, do not remain stuck on the originally generated run-card if a safer/newer candidate in the same vuln-intel set is a better local-lab fit. It is acceptable to select a different candidate when all of these are true:

- the candidate came from the same latest vuln-intel/delta set;
- it can be verified entirely with synthetic lab-owned data/artifacts;
- it avoids accounts, live targets, public IPs/domains, scanners/fuzzers/DAST, callbacks/OAST, secrets, and privileged host/user Docker sockets;
- the resulting handoff clearly says why this candidate was selected over heavier product-specific items.

For package/dependency vulnerabilities that need temporary Internet access for package acquisition, use a reversible posture:

1. verify attacker/victim VM state and host-only boundary;
2. temporarily enable NAT only long enough to install/pull the vulnerable test dependency;
3. run the proof only against a lab-owned artifact directory or disposable service;
4. disable NAT/cable afterwards and verify `INTERNET_CLOSED_EXPECTED` or equivalent final route/DNS failure;
5. record that temporary NAT was for acquisition only, not live target testing.

A verified local-proof continuation should retain project capability, not just produce a one-off run:

- add or update a tested runner under `scripts/labs/`;
- add a focused regression that rejects target-like/live flags and checks the local approval phrase;
- preserve sanitized evidence under `kali-output/`, `labs/proofs/`, or handoff;
- promote the reusable method into `modules/bundles/` only after local evidence exists;
- update `scripts/SCRIPT_INVENTORY.md`, `handoff/accepted_changes.md`, current navigation/queue/artifact index, and the project Obsidian bridge;
- run focused tests, syntax checks, proof JSON assertions, `git diff --check`, and `hermes review` before calling it complete.

## Safety contract

The automation may be metadata/offline by default. It must fail closed on target/execution-like CLI flags such as `--target`, `--url`, `--host`, `--scope`, `--live`, `--execute`, `--scan`, or `--exploit`. Persistent scheduling/cron activation remains a separate operator-approved gate. Local-lab proof execution is allowed only after explicit operator direction and remains local-lab proof-pattern work, not live-target authorization.
