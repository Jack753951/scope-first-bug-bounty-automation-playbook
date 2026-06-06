> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Script-first context-driven module loop

Use this pattern when a cybersecurity workspace starts over-weighting schemas, profiles, preview contracts, or review gates while the operator's actual goal is a practical modular pentest workflow.

## Trigger

- The operator says the safety structure is too heavy or hides the scripts.
- The desired workflow is based on preview/recon results, contextual module selection, script-library fallback, review, and then modularizing useful script combinations.
- The repo already has many contract/profile/validator artifacts, but the operator asks: "where did the scripts go?" or wants to execute situational script combinations.

## Correct workflow

```text
preview + recon results
→ choose modules based on context
→ if no module fits, use the script library
→ choose and execute a situation-specific script combination
→ review results and false positives
→ modularize the useful script combination into a reusable bundle
→ return to preview + recon results
→ repeat
→ write the pentest report
```

## Architecture correction

Make scripts and bundles the operator-facing layer:

- `scripts/SCRIPT_INVENTORY.md` or equivalent should answer what scripts exist, where they are, what context triggers them, risk/gate notes, and output shape.
- `modules/bundles/` or equivalent should contain reusable context-driven script combinations.
- Existing manifests, profiles, validators, preview manifests, and candidate-review contracts remain useful as guardrails and report-integrity layers, but should not be the main path a human uses to choose work.

## Bundle shape

A bundle is a reusable script combination, not just a manifest:

```text
bundle id
trigger conditions from preview/recon
ordered scripts
inputs and caps
expected outputs
false-positive/manual-review checks
report contribution
promotion/retirement rules
```

## Safety balance

Do not delete scope gates or authorization checks. Reposition them:

- Fast path for local/intentionally vulnerable labs and low-risk bounded checks.
- Heavier review only when crossing into public/client/bug-bounty targets, broad scanners, credentials/brute force, callbacks/OAST, destructive behavior, loot/secret collection, automatic finding promotion, or report submission.
- Treat security as a guardrail, not the workflow center.

## Pitfall

Do not respond to this correction by adding more generic safety scaffolding. The next useful slice should usually be:

1. inventory the scripts;
2. define one concrete bundle from current recon evidence;
3. implement the missing small verifier/helper script;
4. run/review it in the authorized lab;
5. promote the combination into the bundle if useful.
