> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, adding wikilinks, and optionally using the Obsidian Local REST API when configured.

Default to filesystem-first access when only `OBSIDIAN_VAULT_PATH` is configured. If `OBSIDIAN_REST_API_URL` and `OBSIDIAN_API_KEY` are configured, the Local REST API may be used for convenience, but remember that it operates on the vault currently open in the Obsidian app — not necessarily the same path named by `OBSIDIAN_VAULT_PATH`.

See `references/local-rest-api-routing.md` for the multi-project API/path routing pattern and verification commands.

## Access modes

Prefer the access mode the user asked for:

1. **Filesystem-first** — read/write markdown directly under `OBSIDIAN_VAULT_PATH`. This is simple and works even when Obsidian is closed.
2. **Local REST API** — use Obsidian's community `Local REST API` plugin when the user wants API-based access or Obsidian app state matters. Keep the API bound to localhost and store `OBSIDIAN_REST_API_URL` plus `OBSIDIAN_API_KEY` in Hermes `.env`; never ask the user to paste the API key into chat. See `references/local-rest-api.md`.

Keep `OBSIDIAN_VAULT_PATH` configured as a fallback even when API-first is enabled. If prior notes or user setup used `OBSIDIAN_API_BASE`, treat it as a legacy alias and migrate/document the canonical `OBSIDIAN_REST_API_URL` name rather than spreading both names.

## Multi-project vaults

When the user has multiple projects, prefer one vault with project namespaces unless they explicitly need hard isolation. Treat each project namespace as the project's long-term memory library for technical notes, vulnerability notes, decisions, review synthesis, and long-term strategy. Keep Hermes global memory project-detail-light; it should store only compact cross-project preferences/signposts and pointers to the right project namespace.

When writing important project-domain notes, maintain the project index (`00_Index/Home.md`, `00_Index/Active Projects.md`, or a dedicated `00_Index/Memory Map.md`) so future agents can find the note and understand its relationship to active work. Use wikilinks and metadata rather than duplicating repo state.

Example:

```text
<vault>/Projects/YouTubeAgent/
<vault>/Projects/CybersecurityWorkspace/
<vault>/Projects/InvestmentAutomation/
<vault>/Shared/
<vault>/Templates/
```

Before writing notes, confirm or infer the target project namespace from the current repo/context. For `youtubestrict/youtube_agent`, write only under `Projects/YouTubeAgent/` unless the user asks for broader setup. For the cybersec lab, durable CTF/security technique lessons, solved challenge writeups, reusable reverse-engineering pitfalls, and methodology notes belong in the Cybersec Lab Obsidian namespace; Hermes memory should keep only a compact trigger/index reminder. Use `00_Index.md` as the project entry note and keep engineering truth in the repo/handoff files; Obsidian stores long-term strategy, research, decisions, experiments, and content rules.

### Cross-project memory governance

When one Hermes profile serves multiple projects, do not let Obsidian become an unstructured second repo or let Hermes global memory accumulate project details. Use this split:

- Hermes durable memory: compact user-wide preferences, stable cross-project rules, and pointers only.
- Repo handoff files: engineering truth, accepted changes, validation, worker outputs, and blocked follow-ups.
- Obsidian project namespace: long-term strategy, research, decision rationale, experiments, and review synthesis.
- Shared Obsidian namespace: cross-project conventions/templates only, not single-project state.
- `session_search`: recall lead only; verify against active notes/files before acting.

When cleaning or compacting Hermes global memory, do not automatically destroy useful project-specific facts. If the user says a global memory entry should be removed because it belongs to a project, rehome the fact into that project's Obsidian namespace with `Status`, `Source`, `Date`, and `Repo truth` metadata, then remove or compact the global memory entry and read back the note to verify.

For durable notes, include `Status`, `Source`, `Date`, and `Repo truth` metadata, and mark old notes `superseded`/`rejected`/`reference` rather than leaving stale strategy active. See `references/cross-project-memory-governance.md` for the full pattern and periodic review checklist.

## Vault path

Use a known or resolved vault path before calling file tools.

For multi-project setups, prefer a routing map outside the repo (for example `~/AppData/Local/hermes/obsidian-projects.json` on Windows) that maps a project key to:

- `api_relative_root` — path inside the currently open API vault, such as `Projects/Cybersec Lab`
- `vault_path` — filesystem fallback path for direct file writes
- `sensitivity` and project-specific no-secrets rules

When a project context makes the target obvious, use the matching route. If the user names a project, use that project key. If API and path disagree about the active vault, do not assume the API is pointing at the intended filesystem root; verify by reading/writing a harmless test note under the intended API-relative folder, or use filesystem fallback.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Local REST API

Use the Obsidian Local REST API when the user wants API-based access or when `OBSIDIAN_REST_API_URL` and `OBSIDIAN_API_KEY` are available and the task benefits from app-aware control of the project memory library.

Prefer the API for:

- verifying the currently open vault before important writes;
- reading the API-visible vault tree;
- maintaining project indexes, wikilinks, backlinks, and memory-map style notes;
- writing and reading back through the same app route;
- confirming that the API-relative project root matches the intended filesystem namespace.

Do not require the API for routine note writes when the vault path is known; filesystem-first Markdown edits are acceptable and often more reliable. If the API connection is refused, treat it as Obsidian/plugin not currently running or enabled, not as a permanent tool limitation; continue filesystem-first unless the user specifically needs API-visible state.

Expected environment variables:

- `OBSIDIAN_REST_API_URL` — commonly `https://127.0.0.1:27124`
- `OBSIDIAN_API_KEY` — secret token from the Local REST API plugin; never print it, store it in notes, or commit it
- `OBSIDIAN_VAULT_PATH` — optional filesystem fallback path

Setup checklist for the user:

1. Open the intended folder as an Obsidian vault (`Open folder as vault`).
2. In that vault, enable Community plugins and install/enable `Local REST API`.
3. Copy the plugin API key into Hermes `.env` as `OBSIDIAN_API_KEY=...`.
4. Set `OBSIDIAN_REST_API_URL=https://127.0.0.1:27124` unless the plugin uses a different port.
5. Reload or restart Hermes.

Verification pattern:

- First check that the key is configured without printing it (print boolean/length only if useful).
- Call `GET /vault/` with `Authorization: Bearer <key>`.
- Write and read back a harmless test note under the intended project root.
- If connection is refused, ask the user to open Obsidian and enable the plugin for the currently open vault; do not conclude the key is wrong until the server is reachable.

Important multi-vault pitfall: the Local REST API follows the vault currently open in Obsidian. A path such as `OBSIDIAN_VAULT_PATH=C:/.../ObsidianProjects` does not force the API to operate there. Validate the API-visible root with `/vault/` and a project-scoped test note before migrating or writing important notes.


## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.
