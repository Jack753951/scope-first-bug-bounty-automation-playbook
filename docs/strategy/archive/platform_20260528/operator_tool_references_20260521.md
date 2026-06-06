> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Operator Tool References — 2026-05-21

Status: reference
Source: user-provided tool list
Scope: cybersecurity lab workflow support only; not authorization for external target interaction.

## Tools

- VirusTotal upload/home: https://www.virustotal.com/gui/home/upload
  - Use for malware/file/hash reputation workflow only when samples are safe and allowed to upload.
  - Do not upload private client files, secrets, credentials, proprietary binaries, or lab loot without explicit approval.

- IPAddressGuide CIDR calculator: https://www.ipaddressguide.com/cidr
  - Use for quick CIDR/range checking and human verification of scope boundaries.
  - Project automation should still rely on repo-local scope validators, not manual web calculators.

- HexEd.it: https://hexed.it/
  - Use for browser-based hex inspection of non-sensitive local artifacts.
  - Do not upload/open secrets, credentials, loot, private client files, or sensitive samples in browser tools without approval.

- Censys Search: https://search.censys.io/
  - Use for passive internet asset/recon research when program rules allow passive sources.
  - Not authorization for active probing; results must still be checked against `config/scope.txt` and program/client rules before any target-touching step.

## Routing note

These are operator reference tools for manual/support workflows. They are not added as automatic runtime dependencies and do not bypass the repo's authorization, scope, privacy, or evidence-redaction gates.
