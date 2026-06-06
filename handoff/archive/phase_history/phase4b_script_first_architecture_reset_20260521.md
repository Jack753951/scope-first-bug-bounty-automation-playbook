> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B Architecture Reset — Script-first Context-driven Module Loop

Status: accepted direction reset / design and navigation update
Date: 2026-05-21
Source: operator correction + Hermes synthesis
Repo truth: `scripts/SCRIPT_INVENTORY.md`, `handoff/active_strategy_queue.md`, `.hermes.md`

## Operator correction

The desired workflow is not contract-first and not safety-process-first. The desired loop is:

```text
preview + recon results
→ choose modules based on context
→ if no module fits, use script library
→ choose and execute a script combination for the situation
→ results + review
→ modularize the context-specific script combination
→ preview + recon results
→ choose modules based on context
→ ...
→ penetration test report
```

This is a major architecture correction. Phase 4B should stop growing heavy contract/profile/review scaffolding as the main user-facing path.

## Problem with the current drift

The current repo has useful safety work, but the center of gravity drifted toward:

```text
manifest/schema/profile/preview
→ runner contract
→ adapter
→ importer
→ candidate review chain
```

That structure is useful as a guardrail layer, but it is too heavy as the operator workflow. It also hides the real scripts under `scripts/`, `scripts/lab_modules/`, `setting/local/`, and `<artifact-output-dir>/`, making the practical question "what can I run next?" harder than it should be.

## New architecture principle

Use a script-first, context-driven loop:

```text
Context packet
  = preview + recon results + scope + objective + constraints

Module selection
  = choose existing reusable module bundle if available

Script library fallback
  = if no module fits, pick scripts from indexed script library

Execution bundle
  = a small ordered combination of scripts with caps and notes

Review
  = inspect results, false positives, safety issues, and usefulness

Modularization
  = turn the useful script combination into a named reusable module bundle
```

The safety layer remains, but becomes an execution guard and review checklist, not the primary architecture.

## What becomes lighter

Replace this as the default user-facing path:

```text
module_manifest -> profile -> runner preview -> contract validators -> adapter -> importer -> review chain
```

With this:

```text
context packet -> module bundle match -> script bundle fallback -> execute -> review -> promote bundle
```

Keep the heavier contract system only when it adds value:

- before real public/client/bug-bounty activation;
- when a reusable module bundle is being promoted into a durable platform module;
- when output may influence a report;
- when a script has dangerous capability such as SQLi, LFI, SSRF, brute force, OAST, broad crawling, or destructive behavior.

## Proposed lightweight artifacts

### 1. Context packet

A short file or JSON object containing:

- target/source: lab, CTF, owned asset, bug bounty scope, or offline fixture;
- objective: e.g. metadata triage, directory listing verifier, auth/JWT review, reflection check;
- recon inputs: URLs, paths, status codes, technologies, interesting endpoints;
- constraints: request cap, rate, forbidden behavior, allowed techniques;
- desired output: observation, candidate, evidence packet, report draft.

### 2. Script inventory

Primary location:

```text
scripts/SCRIPT_INVENTORY.md
```

This is the operator-facing map of available scripts. It should answer:

- what script exists;
- category;
- what it does;
- when to use it;
- risk level;
- whether it has a local-lab-safe wrapper;
- whether it needs scope/run-card/review;
- output location/format.

### 3. Script bundle

A script bundle is an ordered recipe such as:

```text
bundle: lab_directory_listing_triage
inputs: preview/recon result showing /ftp/ candidate
steps:
  1. GET-only metadata probe
  2. bounded /ftp/ filename/content-class verifier
  3. candidate evidence packet builder
review:
  - no bulk download
  - no secrets retained
  - classify only
promotion:
  - if useful, save as reusable module bundle
```

### 4. Module bundle

A module should represent a reusable contextual script combination, not just a manifest.

A module bundle should contain:

- purpose;
- trigger conditions from recon/preview;
- script sequence;
- allowed target classes;
- input/output shape;
- review checklist;
- report contribution notes.

The heavy `modules/checks/**/module.json` contract can remain as lower-level metadata, but it should not be the main way the operator finds and runs work.

## Updated Phase 4B target

Phase 4B should now aim to produce:

1. a script inventory and category map;
2. a context-packet format;
3. a module-bundle format;
4. 2-3 real module bundles built from current lab evidence:
   - `lab_directory_listing_triage` from `/ftp/` candidate;
   - `lab_metadata_baseline` from headers/robots/security.txt/api-docs;
   - `benign_reflection_redirect_triage` from Wave2 canary results;
5. a lab-to-report bundle that turns reviewed candidates into a report rehearsal.

## Immediate next implementation slice

Stop adding generic safety scaffolding. Do this instead:

1. Create/update `scripts/SCRIPT_INVENTORY.md`.
2. Create `modules/bundles/README.md` describing script-first module bundles.
3. Create first bundle spec:
   - `modules/bundles/lab_directory_listing_triage.md`
4. Implement only the minimal `/ftp/` bounded verifier needed by that bundle.
5. Use the bundle result to produce/revise a lab report packet.

## Boundaries that still remain

This reset does not authorize public target activation or unsafe testing. The difference is ordering and ergonomics:

- Safety is a guardrail, not the workflow center.
- Scripts are visible and primary.
- Modules are reusable script combinations.
- Contracts exist only where they prevent real risk or preserve report integrity.

Still forbidden without explicit approval:

- public/real bug-bounty target execution;
- broad scanner runs;
- credentials/brute force;
- callback/OAST/reverse shell/listener;
- destructive or DoS behavior;
- loot/secret collection;
- automatic confirmed finding or report submission.

## Decision

Adopt `SCRIPT_FIRST_CONTEXT_LOOP` as the Phase 4B architecture direction.

The next safe work should reorganize around the script library and context-driven bundles, not continue expanding contract-first scaffolding.
