> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Tool acquisition wave 1 — learning-stage scripts and wordlists

Status: completed / local git-ignored acquisition
Date: 2026-05-21
Storage root: `setting/local/tool_acquisition/wave1_20260521/`

## Purpose

First learning-stage acquisition of mature external scripts, templates, references, and wordlists for OWASP local-lab module development.

This acquisition does not commit third-party payload lists or tool repos into the project. The full downloads live under git-ignored `setting/local/`; the repo records only this summary and downstream bundle/handoff notes.

## Sources acquired

| Source | Local path | Commit | Role |
|---|---|---|---|
| SecLists | `setting/local/tool_acquisition/wave1_20260521/repos/SecLists` | `f73a46d35bdab4a1da0999e3b4f781becb377348` | web discovery, LFI, SQLi, XSS wordlists |
| PayloadsAllTheThings | `setting/local/tool_acquisition/wave1_20260521/repos/PayloadsAllTheThings` | `e961fef231d8327bae83b563fab50aec2e6b77c0` | SQLi/LFI/XSS/SSRF/open-redirect reference payload notes |
| nuclei-templates | `setting/local/tool_acquisition/wave1_20260521/repos/nuclei-templates` | `ac27507912e11827db5652ce05891c198413c4f5` | exposure/misconfiguration/default-login/technology templates for review/wrapping |
| sqlmap | `setting/local/tool_acquisition/wave1_20260521/tools/sqlmap` | `e6595430483f0cf57ad36539ffc61fc4a6060df5` | mature SQLi tool for local-lab bounded runs |

## Curated local wordlists

```text
setting/local/tool_acquisition/wave1_20260521/wordlists/web_common.txt
setting/local/tool_acquisition/wave1_20260521/wordlists/raft_small_directories.txt
setting/local/tool_acquisition/wave1_20260521/wordlists/raft_small_files.txt
setting/local/tool_acquisition/wave1_20260521/wordlists/lfi_jhaddix.txt
setting/local/tool_acquisition/wave1_20260521/wordlists/sqli_generic.txt
setting/local/tool_acquisition/wave1_20260521/wordlists/sqli_quick.txt
setting/local/tool_acquisition/wave1_20260521/wordlists/sqli_low_risk_boolean_blind.txt
setting/local/tool_acquisition/wave1_20260521/wordlists/xss_brutelogic.txt
```

## Notes

- Initial SecLists sparse paths for SQLi/XSS were wrong; corrected to `Fuzzing/Databases/SQLi/...` and `Fuzzing/XSS/robot-friendly/...`.
- No newly downloaded exploit script was run against public/unknown targets.
- The only execution from this acquisition was sqlmap against the authorized local learning靶機, recorded separately in `handoff/phase4b_sqli_acquisition_learning_result_20260521.md`.
- Keep full third-party repos out of git. Commit only summaries, wrappers, local-lab result notes, and project-owned adapters.

## Reuse rule

For the current learning stage:

```text
Use these assets on the authorized local lab first, keep artifacts local, and preserve candidate-only output.
```

For public/real bug bounty/client targets, re-enable scope/program rules before using any acquired payload list, scanner template, or tool.
