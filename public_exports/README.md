> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# public_exports/ — hand-cleaned public editions

This folder is the **only** legitimate source for `stage_public_batch2.ps1`.

## Why this exists

Internal handoff files and Hermes skills contain operational details that should
not be pushed to a public repo: VM names, host-only IPs, specific advisory IDs,
local credential filenames, project-specific paths, channel identifiers, and so
on. Sanity scanning catches some of these but should not be the last line of
defense.

The discipline:

1. **Originals stay private** under `handoff/`, `tools/`, Hermes skill folders.
2. **A human (or this agent under human supervision) hand-cleans a copy** and
   drops it here under the same logical path it should appear in the public repo.
3. **The stager mirrors this folder** into a target (default: a staging folder
   on the Desktop) and runs a fail-closed sanity scan.

## Sanitization rules used here

When producing a `*.public.md` version of an internal doc, replace:

| Private pattern | Public placeholder |
|---|---|
| `<attacker-vm>` / `-v2` | `attacker-tooling-vm` |
| `<victim-vm>` | `victim-lab-vm` |
| `Windows Hermes control plane` | `the orchestration host` |
| `<artifact-output-dir>/...` | `<artifact-output-dir>/...` |
| `192.168.56.x` | `<host-only-lab-subnet>` / `<host-only-lab-ip>` |
| `<private-workspace>` | `<security-research-repo>` |
| `<user-home>\Desktop\youtubestrict\youtube_agent` | `<content-automation-project>` |
| `youtubestrict/youtube_agent` | `<content-automation-project>` |
| `config/scope.txt` | `<authorized-scope-file>` |
| `client_secret.json` | `<provider-credential-file>` |
| `token.json` | `<local-auth-token>` |
| specific GHSA / CVE IDs | `<specific-advisory-id>` (or remove the example) |
| project-specific channel/target names | `<example-target>` / `<format-channel>` |
| internal dates in titles | (remove unless the doc is genuinely about a dated event) |

Keep the methodology language intact. The point is to share the **shape** of
the workflow, not the specific run history.

## Expected folder layout

```
public_exports/
├── README.md                       ← this file
├── docs/
│   ├── LAB_SAFETY_CONTRACT.md
│   ├── MULTI_AGENT_POLICY.md
│   ├── MEMORY_GOVERNANCE.md
│   ├── AI_RESOURCE_ROUTING.md
│   ├── PERIODIC_REVIEW.md
│   └── LONG_HORIZON_LEARNING.md
├── templates/
│   └── AUTHORIZED_LIVE_TARGET_DRY_RUN.md
└── skills/
    └── (later — skill SKILL.md public editions)
```

The stager mirrors this structure into the target repo exactly.

## Adding a new file

1. Copy the private original to the matching path here.
2. Edit out the patterns in the table above.
3. Add a short header noting it is a public edition.
4. Rerun the stager.

If the sanity scan blocks the run, open `PUBLIC_SAFETY_REPORT.md` in the target,
fix the lines it lists by editing the file **here** (not in the target), then
rerun.
