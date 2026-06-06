> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Direction Review Prompt — P3.13 Module Risk-Tier / Active-Testing Policy Follow-up

Status: ready for Cowork direction review
Date: 2026-05-20
Prepared by: Hermes
Source checkpoint: `handoff/p3_12_closeout_current_thread_pause_20260520.md`
Source policy: `handoff/active_testing_policy.md`

## Context

The project is an authorized bug-bounty / cybersec automation platform. Current near-term work is still offline/dry-run/local-first. P3.11 and P3.12 captured SOC simulator lessons as synthetic fixture/catalog artifacts only, and the SOC calibration thread is now paused.

The next mainline platform step is to refine module risk-tier / active-testing policy before future module manifests, module profiles, runner validators, or scanner bridges add explicit risk-tier fields or live-capable behavior.

This is a direction review only. Do not implement code. Do not change schemas, manifests, runners, validators, scanner wrappers, `config/scope.txt`, program scopes, modules, report generators, scheduler/CI, credentials, deployment, billing, OAuth, or production settings.

## Requested review

Review `handoff/active_testing_policy.md` and recommend a narrow P3.13 policy/docs-only follow-up.

Please answer:

1. Is the current risk-tier vocabulary good enough for the next offline platform phase, or should it be split/renamed before future manifest/profile fields exist?
2. What minimal policy/doc update, if any, should happen now as P3.13?
3. Which future module manifest/profile fields should be candidates later, but not implemented in this slice?
4. How should risk tier map to:
   - execution mode (`offline`, `dry-run`, `planned`, `live`);
   - review tier (T0-T5);
   - global/program scope requirements;
   - program-rule allow/deny semantics;
   - operator approval;
   - human-in-loop verification;
   - evidence minimization and audit logging?
5. Which technique classes need explicit fail-closed wording now?
   Examples: passive observation, benign probing, discovery, template checks, fuzzing, brute force/password guessing, exploit-shaped verification, SSRF/OAST callbacks, authentication/session/account-boundary testing, credential-sensitive testing, proxy/pivot/transport behavior.
6. What remains blocked until fresh T3/T4/T5 review or explicit operator approval?
7. Should P3.13 produce only a policy clarification, or should it also produce a future-field candidate table that is explicitly non-contractual?

## Review tier and authority assumptions

Proposed current slice tier: T1 planning/policy-doc direction.

Escalate to T3+ if the recommendation would introduce or materially change a platform contract, schema, module manifest/profile, runner boundary, finding/evidence/report lifecycle, importer/exporter, scanner integration, or module I/O contract.

Hermes authority: direct for a policy/docs-only clarification if the safety boundary remains intact. Conditional or escalation-only for anything that proposes future contracts, runner behavior, target-touching behavior, or live activation.

## OSS Recon Gate posture

For the current policy-doc-only direction review, OSS Recon Gate may be treated as lightweight/not required unless you recommend future contract/schema/runner/module-manifest changes.

If you recommend future manifest/profile fields or runner-validator changes, include a brief design-only OSS comparison using 2-5 relevant references from `handoff/oss_recon_gate.md`, such as:

- Nuclei template metadata / tags / severity / classification;
- ProjectDiscovery tool output and recon pipeline boundaries;
- OWASP ZAP alert risk/confidence model;
- Semgrep rule metadata and fixture discipline;
- SARIF run/rule/result/artifact structure;
- DefectDojo vulnerability lifecycle;
- MITRE ATT&CK / D3FEND tags.

Do not copy unsafe defaults. Specifically reject any pattern that assumes scanner output is confirmed, auto-enables target-touching behavior, auto-discovers targets, bypasses scope/rule gates, or chains callbacks/proxies/pivots without explicit authorization.

## Safety boundary for this review

Allowed:

- read local policy/handoff files;
- recommend policy/docs-only edits;
- recommend future field candidates as non-contractual notes;
- identify required future tests/safety assertions.

Forbidden:

- live scans, probes, exploitation, brute force, fuzzing, callbacks/OAST, proxy/pivot/tunnel/transport behavior, scanner/module execution, target-touching automation;
- `config/scope.txt` or real program scope/rule changes;
- schema promotion or new schema/manifest/runner implementation;
- module/scanner adapter implementation;
- report drafting/submission or platform adapter work;
- credentials, OAuth, tokens, private keys, loot, scheduler/CI, deployment, billing, production settings.

## Expected output format

Please write a direction review with:

```text
Review tier:
Milestone:
Decision: APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK
Safety boundary:
OSS Recon Gate: not applicable / lightweight / required before implementation
Recommended P3.13 scope:
Blocking issues:
Non-blocking improvements:
Future field candidates, if any:
Required tests/safety assertions for any future implementation:
Out-of-scope/deferred items:
Operator approval required: yes/no; reason:
```

Decision guidance:

- `APPROVE`: current policy is good enough; only minor note update needed.
- `APPROVE_WITH_CHANGES`: P3.13 should make a narrow policy/doc update before future module fields.
- `DEFER`: no policy follow-up is useful until a concrete module/runner design is ready.
- `BLOCK`: current policy is unsafe or misleading enough that it must be fixed before more platform work.
