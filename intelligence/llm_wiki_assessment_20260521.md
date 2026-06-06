> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# LLM Wiki Assessment for Cybersec Lab — 2026-05-21

Source assessed: <https://github.com/nashsu/llm_wiki>
Route/tool: Hermes loaded local `llm-wiki` skill, then fetched GitHub API metadata and README via Python stdlib/terminal.
Visible repo metadata at assessment time: TypeScript/Tauri desktop app, created 2026-04-08, pushed 2026-05-19, ~8.5k stars, ~1.0k forks, GPL-3.0.

## What it is

LLM Wiki is a cross-platform desktop application for building a persistent interlinked markdown knowledge base from documents. It implements the Karpathy-style LLM Wiki pattern with raw sources, generated wiki pages, schema/purpose files, index/log navigation, Obsidian compatibility, graph/search/lint/review features, and optional local HTTP API.

Important features from README:

- Tauri v2 desktop app, React/TypeScript frontend.
- Imports documents and builds wiki pages incrementally.
- Two-step ingest: analysis first, wiki generation second.
- Knowledge graph, source overlap, vector search via LanceDB optional.
- Folder import and source folder auto-watch.
- Deep Research via Tavily/SerpApi/SearXNG.
- Review system for human judgment.
- Chrome web clipper.
- Local `127.0.0.1:19828` token-protected HTTP API for agents.
- Separate `llm_wiki_skill` for Claude Code/Codex-style agents.

## Usefulness for this cybersec project

Verdict: useful, but as a knowledge/research layer, not as a replacement for the repo handoff or security gates.

Good fit:

1. Long-lived learning and methodology memory
   - Bug bounty methodology notes.
   - Tool comparison notes.
   - OWASP/CWE/CVSS references.
   - Program-rule interpretation patterns.
   - Repeated false-positive traps.
   - Lessons from lab reports and reviews.

2. Source-backed knowledge base
   - Save official docs, writeups, references, and internal synthesis as linked pages.
   - Keep provenance to source files instead of relying on chat memory.
   - Use graph/search for cross-project learning.

3. Agent-readable local API
   - Could let Hermes/Claude/Codex query curated knowledge without re-reading everything manually.
   - The `127.0.0.1`-only + token posture is directionally good for local use.

4. Obsidian-friendly workflow
   - Fits the user's existing preference for durable project notes and cross-project memory routing.

## What it should NOT be used for

- Do not store loot, credentials, tokens, private keys, raw vulnerable client data, or sensitive scan bodies.
- Do not treat LLM Wiki content as authorization.
- Do not let it bypass `config/scope.txt`, program rules, or Hermes safety gates.
- Do not auto-ingest raw scanner output containing secrets or large response bodies.
- Do not make it the source of truth for active handoff state; this repo's `handoff/active_strategy_queue.md`, `accepted_changes.md`, and `.hermes.md` remain authoritative for current execution.
- Do not enable web/deep-research auto-ingest into private evidence workflows without redaction and review.

## Recommended adoption pattern

Adopt lightly first:

1. Use it as a read-mostly cybersec knowledge vault.
2. Keep repo handoff as the operational source of truth.
3. Export/summarize only non-sensitive lessons into LLM Wiki.
4. Create pages for:
   - `Bug bounty report readiness`
   - `Directory listing exposure triage`
   - `SPA fallback false positives`
   - `CORS false positive rules`
   - `Nuclei template safety policy`
   - `Evidence redaction rules`
5. If using the API, keep it bound to `127.0.0.1`, token-protected, and read-only for agents by default.
6. Add a project rule: no raw `scans/`, `loot/`, `.env`, cookies, tokens, client materials, or exploit payload captures are ingested.

## Fit score

- For research/learning/reference: high.
- For current cybersec handoff execution: medium-low; repo files are already better because they are versioned, review-gated, and tied to validation.
- For sensitive evidence storage: no.
- For future cross-project methodology memory: high, if kept sanitized and source-backed.

## Bottom line

`nashsu/llm_wiki` is useful as a curated, source-backed cybersec methodology wiki and agent-queryable reference. It should complement Hermes memory + repo handoff, not replace them. The safest first use is to ingest sanitized lessons and public references, not live scan artifacts or bounty evidence.
