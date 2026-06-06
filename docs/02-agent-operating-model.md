# 02 — Agent Operating Model

Status: public methodology

## Roles

- **Primary orchestrator**: owns task decomposition, scope checks, lane state,
  worker routing, verification, and final safety decisions.
- **Tactical reviewer**: challenges attack-path quality, proof boundary, and
  whether the selected target surface can actually prove the hypothesis.
- **Deterministic reviewer**: checks contracts, schemas, scripts, tests, and
  overclaim risk.
- **Operator**: clears human gates: credentials, OTP/CAPTCHA, signup decisions,
  scope changes, live high-risk techniques, and final submission.

## Required context packet for workers

Before asking a worker to review or implement non-trivial work, provide a compact
context packet with:

1. current project boundary and safety contract;
2. current lane state and blocked/allowed actions;
3. exact files or artifacts to read;
4. expected output shape;
5. stop-before rules;
6. reviewer identity / visible runtime if known;
7. verdict vocabulary: `pass`, `partial`, `request_changes`, `reject`.

Workers do not automatically inherit memory, vault notes, or local context. If it
matters, include it or point to it explicitly.

## Call record shape

```markdown
# Worker Call Record

## Task
<what the worker must decide or produce>

## Required context reads
- <file or summarized packet>

## Inputs
- <artifact list>

## Expected output shape
- verdict
- key risks
- required fixes
- optional suggestions

## Boundary
<what the worker must not do>

## Result
<paste or summarize worker result>

## Verdict
pass | partial | request_changes | reject
```

## Rule of thumb

Use stronger agents for unclear direction, hunt strategy, proof-boundary dissent,
report-readiness review, and code/test review. Do not use them to bypass safety
or to manufacture confidence when evidence is weak.
