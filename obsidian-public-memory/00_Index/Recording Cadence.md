> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Recording Cadence

## Default rule

Record to Obsidian when the note will still be useful after 7 days.

## Cadence

### Work-unit session note

Create a short note after completing a meaningful unit of work, such as:

- phase/task completed
- Codex review completed
- Claude/Cowork review completed
- important design decision made
- safety boundary changed or clarified
- non-trivial blocker discovered/resolved

Keep it short: outcome, decision, next step, risks.

### Daily note

Create or update a daily note only on days with substantive progress.

Include:

- completed work
- decisions
- blockers
- next actions
- safety notes

Skip daily notes for trivial chats or no material progress.

### Weekly strategy review

Create a weekly review once per week or after a major phase completes.

Include:

- roadmap fit
- architecture/security recommendations
- Codex/Claude/Hermes review synthesis
- immediate next actions
- defer/avoid items
- unresolved risks

## Do not record

- API keys, tokens, cookies, credentials
- loot, hashes, private exploit details, client-sensitive data
- every terminal command
- temporary TODOs
- commit SHAs unless they are part of a durable release note
- raw scanner output unless sanitized and intentionally summarized

## Storage split

- Repo: source of truth for code, schemas, handoff, audit artifacts
- Obsidian: long-term knowledge, decisions, strategy, learning notes
- Hermes memory: compact durable preferences/environment facts
- Skills: reusable workflows and procedures
