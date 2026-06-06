> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B Lab Fast Lane Policy — Host-only Juice Shop

Status: active local-lab operating policy
Date: 2026-05-21
Authority: operator-approved local/intentionally vulnerable lab use
Scope class: local lab / intentionally vulnerable app only

## Purpose

Use the existing host-only Juice Shop target actively enough to calibrate automation and module behavior without applying the same overhead required for public/client/bug-bounty targets.

This policy is not authorization for public targets. It is a fast lane only for the isolated lab named below.

## Fixed lab boundary

Allowed target:

- `http://<lab-ip>:3000/`
- victim VM: `<victim-vm>`
- attacker VM: `<attacker-vm>`
- network: VirtualBox host-only

Required preserved assumptions:

- no public / real bug-bounty / client target interaction
- no credential harvesting
- no callback / OAST / reverse shell / listener
- no brute force
- no destructive / stress / DoS class actions
- no loot collection or secret exfiltration
- no automatic confirmed / verified / reportable finding promotion

## Fast-lane allowed without fresh heavy review

These can be executed after a quick preflight/health check and artifact path declaration:

- GET-only or HEAD-only baseline checks
- headers/security-header metadata
- CORS metadata with inert Origins only
- `robots.txt`
- `/.well-known/security.txt`
- `/ftp/` directory-listing metadata, filenames/content-class only, no bulk downloads
- `/api-docs/` API-docs metadata
- small fixed known-path metadata list
- tiny benign parameter canaries on fixed URLs
- open-redirect negative/positive canaries that do not follow redirect chains
- inert reflection canary as text only, no executable JavaScript payload
- tiny fixed wordlist content discovery when separately capped and non-recursive

Default fast-lane limits:

- request cap: <= 100 per run
- default adapter cap: <= 40 per run unless the run card says otherwise
- timeout: <= 5 seconds per request by default
- rate: <= 2 requests/second by default
- pre-health and post-health required
- output: JSONL observations plus short summaries
- output vocabulary: `observation`, `candidate`, `needs_manual_review`, `no_candidate`, `blocked`

## Still requires elevated gate / run card

- sqlmap or SQLi time-based payloads
- dalfox/kxss deep scan or executable XSS payloads
- LFI payloads that read `/etc/passwd`, secrets, tokens, keys, app config, or private files
- SSRF callbacks, interactsh, OAST, metadata-service probes
- large ffuf/gobuster wordlists, recursive crawling, or broad spidering
- nuclei templates with intrusive/fuzz/dos/exploit tags
- file upload exploit chains
- auth/session/account-takeover flows
- brute force / password guessing / hydra
- DoS, crash, stress, resource exhaustion
- reverse shell, listener, pivot, tunnel, relay, proxy abuse
- any workflow that collects credentials, tokens, secrets, PII, loot, or proprietary data

## Operating rhythm

For fast-lane Tier 1/Tier 2 lab checks:

1. Confirm target is the fixed host-only lab target.
2. Run pre-health.
3. Execute bounded adapter with fixed target/list and caps.
4. Run post-health.
5. Save artifacts under `<artifact-output-dir>/<run_id>/` and summarize in `handoff/` when meaningful.
6. Perform output-side review after execution.
7. Promote only to candidate/rehearsal artifacts, never confirmed findings.

For Tier 3+ or any uncertain behavior, pause and create a script-specific run card.

## Current next implementation

The reusable GET-only adapter and Wave2 benign parameter adapter are complete and tested against the host-only Juice Shop lab.

Current recommended next fast-lane implementation:

- build a bounded `/ftp/` filename/content-class verifier
- list and classify filenames/content types/sizes only
- do not bulk download files
- do not collect secrets, tokens, credentials, PII, or loot
- keep JSONL candidate-only output and pre/post health gates
- keep public targets blocked
