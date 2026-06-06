> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Source-Project Architecture Extraction for a New Product

Use this when the user asks to start or shape a new project by referencing one or more existing local projects and "extract what is valuable" for a different long-term goal.

## Pattern

1. Load/read the target repo first if it exists, then inspect source repo authority layers:
   - README / AGENTS / `.hermes.md`
   - active strategy queue / accepted changes / architecture reset notes
   - not raw runtime data, secrets, tokens, outputs, or sensitive project state.
2. Extract process patterns and architecture principles, not domain-specific nouns.
3. Translate source concepts into the target domain explicitly.
4. Preserve activation gates from the source projects, but rename them into the target risk surface.
5. Create target-local durable artifacts rather than putting project detail in global memory.
6. Save only a compact global signpost if future sessions need to know where target project memory lives.

## Translation examples

Media automation source -> advertising platform target:

- trend/topic radar -> market/audience signal radar
- channel profile -> customer/segment/platform/objective profile
- candidate/concept packet -> campaign concept packet
- private upload gate -> draft/export/canary/spend approval gate
- render QA -> creative + brand + policy + platform-format QA
- fetch analytics / learn -> campaign analytics import + learning report

Cybersecurity workspace source -> advertising platform target:

- context packet -> customer campaign context packet
- scope authorization -> customer data / ad-account / budget authorization
- script inventory -> ad workflow script/template library
- module bundle -> reusable campaign playbook/module
- evidence packet/report integrity -> campaign provenance, approval, and performance report
- review tiering / OSS recon gate -> design review before ad-platform, payment, targeting, or sensitive-category integrations

## Recommended target artifacts

For a new product repo, create a minimal project-local orientation set:

- `README.md` — product goal, borrowed architecture summary, first phase.
- `PROJECT_CHARTER.md` — mission, product thesis, operating loop, non-negotiable boundaries.
- `.hermes.md` — role/routing/gate rules for future agents.
- `docs/architecture.md` — translated target architecture.
- `handoff/source_architecture_extraction_<date>.md` — what was borrowed, what was not, and translation matrix.
- `handoff/active_strategy_queue.md` — current phase, next safe slice, blocked surfaces.

## Pitfalls

- Do not copy source-project secrets, tokens, raw targets, private customer data, or runtime artifacts.
- Do not import source-domain vocabulary as target product truth. Translate it.
- Do not let reference projects override the user's stated target.
- Do not start with production activation, OAuth, billing, scheduler, spend, or public release integrations when the safer first slice is packet/schema/QA design.
- Do not overbuild heavy contracts before proving the target's context-driven loop.

## Memory routing

Project-specific strategy and architecture belong in the target repo handoff/docs and, if used, the target Obsidian namespace. Global Hermes memory should contain only a compact signpost such as: "Project X details live in repo/path/handoff; goal is ...".
