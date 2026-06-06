> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Local tool acquisition and review hygiene

Use this reference when a lab workflow downloads mature third-party tools, payload lists, templates, or wordlists for local learning.

## Pattern

- Put full third-party repos, payload archives, and raw runtime outputs under git-ignored local paths such as `setting/local/...` and `kali-output/...`.
- Commit only project-owned summaries, manifests, wrapper code, bundle docs, and candidate-only result notes.
- Record upstream source, local path, commit/version, license if known, and intended role in a handoff manifest.
- Preserve candidate-only language for tool/scanner output until manual verification, evidence review, impact, remediation, and retest steps exist.
- When a project-owned review wrapper recursively validates files, exclude git-ignored runtime/vendor acquisition dirs from static compile/lint checks. The gate should validate project-owned code, not arbitrary third-party payload archives.

## Example artifacts

```text
setting/local/tool_acquisition/<wave>/         # git-ignored full downloads
kali-output/<run>/                             # git-ignored runtime outputs
handoff/tool_acquisition_<wave>.md             # committed summary/manifest
modules/bundles/<bundle>.md                    # committed reusable local-lab bundle
handoff/<run>_result.md                        # committed candidate-only result note
```

## Review-wrapper exclusion example

For a bash wrapper that scans JSON/Python/shell files with `find`, add path exclusions like:

```bash
! -path '*/setting/local/*' ! -path '*/kali-output/*'
```

Apply this to JSON validation, Python compile, and shell syntax checks if those checks recurse through the whole repository.

## Pitfall

Do not save a durable rule that a downloaded tool or wordlist is “broken” because it failed a project static check. The durable lesson is to keep vendor/runtime acquisitions out of project-owned static review gates and record only the acquisition manifest plus wrappers/results that belong to the project.
