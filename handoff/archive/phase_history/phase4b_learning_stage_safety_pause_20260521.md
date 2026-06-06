> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B learning-stage safety-control pause

Status: active operator directive / local learning stage only
Date: 2026-05-21
Owner: Operator directive recorded by Hermes

## Operator directive

The operator requested that, during the current learning stage, project-internal safety controls should be paused rather than split into another detailed tier/profile system.

Plain-language directive:

```text
先不要分層，學習階段先暫停安全管制。
```

## Hermes interpretation

This does **not** remove the external/legal/abuse boundary. It pauses the project's over-broad internal brakes that were blocking normal learning-lab use of offensive/security tooling.

In practice, while this directive is active:

- Do not require new risk-tier reviews before using mature tools in the authorized local lab.
- Do not category-ban broad scanners, fuzzers, Burp workflows, TLS scanners, nuclei/ZAP/Nikto/ffuf/gobuster/wfuzz/nmap, or exploit-shaped/destructive lab scripts against the disposable local靶機.
- Do not force contract-first/profile-first/schema-first work before learning-lab execution.
- Do not make Hermes retreat to dry-run/offline planning when the operator asks to use the built靶機.
- Prefer script-first learning loops: run tool/script -> observe -> recover if needed -> summarize -> modularize useful parts.
- NAT may be enabled temporarily for tool/package/template downloads, then disabled after setup where feasible.

## Non-paused red lines

The following are not project-process controls; they remain binding:

- no public/real/unknown target interaction without explicit authorization/scope;
- no malware;
- no stealth persistence;
- no real credential theft;
- no real exfiltration of secrets/tokens/PII/proprietary data;
- no unauthorized pivoting/relay infrastructure;
- no evasion of legitimate controls;
- no automatic report submission;
- no automatic promotion from scanner/tool output to confirmed finding.

## Learning-stage defaults

For the current authorized local lab / intentionally vulnerable app:

```text
broad scanner: allowed
fuzzer: allowed
Burp/session workflow: allowed
TLS scanner: allowed
intrusive scanner templates: allowed
exploit-shaped script: allowed
destructive script: allowed if the lab is intended to be recoverable
```

Expected but lightweight practice:

```text
know target IP/URL
know attacker/victim VM role
keep artifacts local
record what ran
recover/reset if the app breaks
summarize possible vulnerabilities as candidate-only
```

Do not stop learning-lab execution just because a heavy policy artifact, review tier, profile, manifest, or contract is missing.

## Output semantics still strict

Execution may be aggressive in the learning lab, but conclusions stay conservative:

```text
tool output -> observation
observation -> possible vulnerability / candidate
candidate -> manual review needed
manual verification + evidence + impact -> confirmed/report-ready only after separate human/operator decision
```

## Scope of this pause

This pause applies only to the current learning stage and the authorized disposable local lab / intentionally vulnerable app environment.

It does not authorize:

- public bug bounty target activation;
- client target activation;
- production/third-party assets;
- scanning the internet;
- credential attacks against real accounts;
- retaining loot/secrets;
- automated submission or publication.

## Next operating rule

If the target is the local learning靶機, Hermes should default to acting, not over-governing:

```text
Use the tool, cap obvious runaway behavior, keep artifacts local, recover if needed, and record candidate-only lessons.
```

If the target is not clearly the local learning lab or otherwise authorized, Hermes must stop and ask for scope/authorization.
