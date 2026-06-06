> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Agent preview and Claude Code review lenses — OWASP single-vulnerability lab waves

Use this reference when inserting lightweight tactical agent perspectives into the script-first local-lab workflow.

## Why this exists

The operator wants more tactical visibility and project-value focus without sliding back into governance-first work. These are not new safety gates, approval layers, or process blockers. They are lightweight perspectives that help choose better proof paths and avoid low-value work:

```text
OSS/source reconnaissance -> agent preview -> Kali bounded script execution -> artifact/evidence -> agent review -> verified-impact/bundle/evidence packet
```

These lenses are not public-target authorization, not report approval, not a new safety process, and not a demand for heavy schemas. They must not add extra safety bureaucracy to local authorized lab work.

## Hermes preview lens

Run after OSS/source reconnaissance and before Kali bounded-script execution. Default owner: Hermes.

Purpose:

- broaden attack-path thinking before execution;
- compare mature tool/wrapper/custom runner choices;
- identify better local target surfaces if the current靶機 is unsuitable;
- catch tactical proof gaps, weak target/tool choices, false-positive risks, and artifact-value gaps;
- preserve local-lab tactical freedom by allowing bolder but recoverable paths when scope-locked.

Default shape:

- Hermes writes the preview by default; do not spawn a separate preview agent unless the operator asks or the lane needs unusual specialist context.
- Preview output should be short and operational, not a broad policy essay.
- Do not use preview to create a new approval/safety gate. Existing scope/recovery boundaries remain, but preview's job is tactical value: stronger proof path, better target, better artifacts, and less wasted execution.

Required preview fields:

```text
Preview owner/tool:
Visible model/runtime if available:
Tactical focus:
Chosen proof path:
Accepted suggestions:
Rejected suggestions:
Missing preconditions:
Execution plan:
Project value:
```

Recommended reviewer prompts:

```text
Tactical preview: Given this one-vulnerability local-lab target, OSS/source notes, and planned bounded runner, identify the strongest proof path, likely false positives, better local target/tool choices, artifact-value gaps, and the one next action with the highest project value. Keep it tactical; do not add new safety process.
```

```text
Project-value preview: Check whether this wave is worth running now versus switching lane/target/tool. State what would make the proof valuable, reusable, and clearly distinguishable from a low-value demo.
```

## Claude Code review lens

Run after execution and artifact pullback, before labeling `verified-impact` or writing/promoting a bundle/evidence packet. Default owner: Claude Code, invoked as a read-only reviewer from a compact evidence packet. Hermes keeps final synthesis.

Purpose:

- challenge whether the artifact actually supports the project-value claim;
- separate verified impact from candidate/control/noise;
- identify missing evidence or weak artifact value before overclaiming;
- decide whether to stop, rerun with controls, switch target/lane, or packetize;
- increase tactical learning by asking whether a stronger safe proof is reachable.

Required review fields:

```text
Reviewer route/tool: Claude Code by default
Visible model/runtime:
Review focus: tactical/project-value evidence review
Evidence inspected:
Claim supported? yes/no/partial
Recommended status: verified-impact | valuable-candidate | attempted-not-verified | blocked/deferred | reference-only
Missing evidence:
False-positive controls:
Tactical next step:
Hermes final decision:
```

Recommended reviewer prompts:

```text
Evidence review: Inspect these artifact summaries/logs and decide whether the exact vulnerability impact claim is supported and useful to the project. Check positive/control artifacts, source labels, marker provenance, and whether the wave should be packetized, rerun once, switched, or parked. Do not add new safety process; do not overclaim.
```

```text
Tactical review: Given the result and artifacts, decide whether the local lab should stop and packetize, rerun with one missing control, switch to a better local target, or retain as candidate. Prioritize one-vulnerability max-impact learning and project value; do not create additional safety gates.
```

## Guardrails

- Do not let preview/review become heavy governance or a new safety process that blocks local learning.
- Do not use these gates to justify public/unknown target testing.
- Do not bypass explicit execution-layer denials; use operator-run scripts or adjacent lanes.
- Do not require multiple agents for trivial metadata-only waves.
- Do record dissent when the reviewer thinks the proof is weak, low-value, or a stronger local-lab path exists.
- Hermes final synthesis decides the project status and records accepted/rejected suggestions in handoff.
