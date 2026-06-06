> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

---
name: landing-page-copy
description: "Use whenever the user wants to write, draft, or critique landing page copy, sales page copy, hero sections, headlines, value propositions, calls to action, FAQ sections, or any conversion-focused web copy for a community / SaaS / course / coaching offer / membership / newsletter / digital product. Trigger when the user mentions a specific community or product to promote (e.g. 'AI Profit Boardroom', a Discord, a Skool community, an info product), or asks for help with copywriting frameworks like AIDA, PAS, FAB, or 4Ps. Don't trigger for general marketing strategy that isn't copy, brand-style guides without a conversion target, or technical product documentation."
---

# Landing Page Copy Skill

Helps Claude produce high-converting, structured landing page copy with predictable section quality and a clear voice. Originally seeded from a blueprint for the *AI Profit Boardroom* community; now generalised so it works for any conversion-focused offer.

## Workflow

When asked to draft a landing page, follow this sequence — don't skip the discovery step:

### 1. Discovery (always first)
Before writing copy, gather the inputs that determine quality. Ask the user concisely for whichever are missing — combine into one question rather than serial back-and-forth:

- **Offer / product name** and one-sentence description.
- **Target audience** (who specifically — be narrow).
- **Primary outcome** the buyer gets (the result, not the features).
- **3 biggest objections** they have before buying.
- **Proof** available (testimonials, case studies, numbers, credentials).
- **Tone preference** (authoritative / friendly / contrarian / luxury / playful).
- **Single call to action** (what should they click? what happens next?).
- **Price / commitment level** (so claims match expectations).

If the user has already supplied this in the conversation, don't re-ask — confirm and proceed.

### 2. Drafting
Use the section structure in `references/section_structure.md` and the formulas in `references/copywriting_frameworks.md`. Output the copy as one continuous, ready-to-paste document — not a critique or commentary unless the user asked for that.

### 3. Self-check
Before delivering, verify against `references/quality_checklist.md`. If something fails, fix it silently rather than apologising.

## When the user gives you a brief ad-hoc

If the user just says "write a landing page for X" with no further info — make sensible defaults *but* state them. Example:

> I'm assuming a $97/mo membership for solo founders, friendly-but-authoritative tone, single CTA "Join now". If any of that's off, tell me and I'll rewrite.

This avoids ping-pong while still letting them course-correct.

## Asset files

- `assets/landing_page_template.md` — full filled-in template (the *AI Profit Boardroom* example) showing what a finished page looks like.
- `assets/blank_template.md` — empty version with section labels, ready to be populated for any offer.

## Reference files (read on demand)

- `references/copywriting_frameworks.md` — AIDA, PAS, FAB, BAB, 4Ps, Schwartz awareness levels, headline formulas with worked examples.
- `references/section_structure.md` — the six standard sections (Hero / Sub / Value / Proof / CTA / FAQ) with goals, length targets, and what to avoid.
- `references/quality_checklist.md` — the pass/fail criteria the draft must meet before delivery.

## Output style

- Default to plain Markdown so the user can paste into any builder.
- Hero headline ≤ 12 words, one promise.
- Sub-headline 1–2 sentences, explains *who it's for* and *the mechanism*.
- Bullets are benefit-led: "[outcome] in [timeframe] without [common pain]".
- One CTA, repeated 2–3 times down the page. Not five different CTAs.
- Include FAQ section addressing the 4 objections from discovery.
- Include 1–3 testimonial / proof placeholders if no real proof was given, marked clearly with `[PLACEHOLDER]`.

## Common mistakes to avoid

- Writing features when the user wants benefits ("Prompt vault" → "Cut content prep from 6 hrs/week to 30 minutes").
- Multiple competing CTAs ("Join now" + "Free trial" + "Book a call" — pick one).
- Hero copy that talks about the company instead of the customer.
- Ignoring the discovery step and shipping a generic page.
- Hyperbolic claims that conflict with the offer's price (e.g. "scale to 7 figures" on a $20 ebook).
