> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Source-fit planning rungs for generated-media projects

Use this when the safest next action is choosing better creative/source candidates, not generating another artifact.

## Purpose

A source-fit planning rung converts prior creative QA/review lessons into a reusable pre-generation packet. It should help future runs decide whether a candidate is ready for script prompting while preserving all generation/upload gates.

## Required safety boundary

State explicitly that the artifact does not authorize:

- create/draft/loop/remake commands;
- rendering, upload, publication, scheduling, or privacy changes;
- OAuth/token/client-secret/channel-destination edits;
- channel JSON mutation;
- database/runtime-media mutation;
- copying competitor assets/audio/frames.

A source-fit pass is only a planning signal; it is not upload or generation approval.

## Scorecard sections

### 1. Core source fit

Use a small scoring scale, e.g. `2 = strong`, `1 = weak`, `0 = missing`, `BLOCK = hard risk`.

Typical generated-media criteria:

- clear relationship or power imbalance;
- concrete unfair action or conflict;
- one proof object or visual anchor;
- plausible consequence or reversal;
- side-taking/comment-prompt potential.

### 2. Hook readiness

Require a proposed first sentence before generation. Check:

- short enough for the target format;
- contains a relationship/role noun;
- contains an unfair action/demand/conflict verb;
- hints proof/contradiction;
- avoids generic setup.

### 3. Brand/safety risk filters

Define blockers for the lane. For story/reaction content, common blockers include:

- sustained gross-out or bodily-fluid retaliation;
- cruelty to children or animals;
- graphic violence;
- sex/assault detail;
- doxxing or real named private workplaces/schools/cities;
- revenge more harmful than the original action;
- humiliation/contamination as the only appeal.

### 4. Visual/proof readiness

Check that the opening can communicate the conflict visually without unsafe or copied assets:

- two distinct visual beats in the first few seconds;
- synthetic or project-owned proof object;
- visual motif reinforces the exact injustice rather than generic mood;
- first frame can be understood without long text;
- fit with the lane’s current asset/render/review profile.

## Candidate packet template

```text
Candidate title/theme:
Source type:
Safety status: PASS / BLOCK / NEEDS_REVIEW

One-sentence source summary:

A. Source-fit scores
- Relationship/power imbalance: 0/1/2 — evidence:
- Concrete unfair action: 0/1/2 — evidence:
- Proof object / visual anchor: 0/1/2 — evidence:
- Plausible consequence: 0/1/2 — evidence:
- Side-taking potential: 0/1/2 — evidence:
Total A: __ / 10

B. Hook readiness
- Proposed first sentence:
- Role noun: 0/1/2 — evidence:
- Conflict verb/action: 0/1/2 — evidence:
- Proof/contradiction hint: 0/1/2 — evidence:
- Format length fit: 0/1/2 — count:
- Avoids generic setup: 0/1/2 — evidence:
Total B: __ / 10

C. Brand-risk filters
- Hard blocker present? yes/no
- If yes, blocker:

D. Visual/proof readiness
- Two-beat opening idea:
- Proof object representation:
- Synthetic/safe asset plan:
- Profile fit: yes/no + reason
Total D: __ / 10

Decision: PASS_TO_SCRIPT_PROMPT / HOLD_FOR_REVIEW / BLOCK
Reason:
Next safe action:
```

## Creative-review routing for non-trivial candidate scoring

If a source-fit packet chooses among multiple candidate themes, treats visual/proof-card fit as a deciding factor, or the user frames the task as creative review, add an independent creative review pass before promoting a candidate to the next planning rung.

Preferred pattern when Claude Code is available/authenticated:

```bash
claude -p "Read-only creative review of handoff/<candidate_packet>.md. Do not modify files. Treat this as source-fit review only, no generation/upload approval. Return concise: Reviewer route/tool; visible model if exposed; Verdict; preferred candidate; blockers; notes; blocked actions confirmed." \
  --allowedTools 'Read' \
  --max-turns 3 \
  --output-format json
```

Record the visible model/runtime model from JSON `modelUsage` when exposed. Write a separate review artifact, e.g. `handoff/<candidate_packet>_claude_review_<date>.md`, then update the candidate packet and queue with Hermes synthesis.

The Claude Code review may confirm a `PASS_TO_SCRIPT_PROMPT` planning target, but it is still not generation/render/upload approval.

## Handoff update

After writing a source-fit rung, update the project queue/accepted-changes files with:

- artifact path;
- no-generation/no-upload boundary;
- threshold for moving to script prompt;
- reviewer route/tool and visible model/runtime model when a Claude Code review was used;
- explicit statement that future generation still needs fresh user approval.

## Common pitfall

Do not let a planning pass become implicit permission to generate. If the user later says “continue,” choose another safe planning/scoring step unless they explicitly authorize generation/render/upload.
