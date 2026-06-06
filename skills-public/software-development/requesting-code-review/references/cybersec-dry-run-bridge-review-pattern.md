> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec Dry-Run Bridge Review Pattern

Use this reference when reviewing or preparing offline cybersec workflow slices that connect two existing components only through test fixtures/harnesses (for example, recon dry-run policy artifacts consumed by a runner preview path).

## Core rule

Do not trade validation fidelity for workflow smoothness. If a high-fidelity review or validation step requires a specific object/input/resource (lab target, program rules, real scope file, sample scanner output, reviewer route, etc.), stop and ask the operator for it. Use synthetic substitutes only when the slice explicitly remains offline/test-only and the loss of fidelity is acceptable for that stage.

## Safe tests-only bridge pattern

For offline bridge coverage:

1. Keep runtime surfaces untouched unless a fresh T3/T4 design review and operator approval authorize them.
2. Run producers only in dry-run mode inside a temporary workspace/HACKLAB.
3. Copy artifacts only inside the test harness, not through a runtime wrapper, CLI flag, auto-discovery path, scheduler, or integration service.
4. Invoke consumers only in preview/dry-run mode.
5. Assert no live target access, scanner execution, module execution, findings/evidence writes, reports/submissions, callbacks/OAST, proxy/pivot/tunnel, credentials/OAuth, deployment, billing, or production changes.
6. Fence real repo mutation with snapshots/hashes for scope/config and output directories (`runs/`, `loot/`, `scans/`, `evidence/`, `reports/`).
7. Add negative cases for target mismatch, path escape/outside-run artifacts, helper returncode mismatch, audit-event mismatch, mode mismatch, and tampered/hash-drifted copied artifacts.
8. Make helper names/comments explicit that path translation is test-only and must not be copied into runtime code.

## Review packet checklist

Independent reviewer should verify:

- Reviewer route/tool and visible model/runtime are stated; if exact runtime is not exposed, say so.
- Diff is scoped to the intended slice and forbidden runtime/config/scope/module/schema surfaces are unchanged.
- Artifact copying is test-harness-only and does not create runtime coupling.
- Validation includes focused tests, adjacent suites when relevant, static review (`git diff --check` / local review), forbidden-surface diff checks, and added-line secret scan.
- Any worker timeout or incomplete TDD/RED transcript is documented as a process caveat; decide whether it is a blocker based on whether runtime code changed.

## When to ask the operator

Ask instead of substituting when the next quality step needs:

- a real lab target or靶機;
- bug bounty program rules or authorized scope;
- real scanner/module output samples;
- explicit permission for target-touching, runtime bridge, activation, scheduler/deployment, credentials/OAuth, reports/submissions, or production-like behavior.

State: what is needed, why synthetic substitutes would reduce quality, exactly how to provide it, and what safe offline work remains possible if they do not provide it yet.
