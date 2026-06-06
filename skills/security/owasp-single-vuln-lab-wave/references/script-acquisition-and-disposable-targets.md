> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Script Acquisition and Disposable Target Expansion

Use this reference when a local OWASP/CVE/KEV-driven lab wave needs modern exploit/tool sources and the current靶機 cannot demonstrate the proof type cleanly.

## Script acquisition pattern

When the operator asks to use modern sources such as Exploit-DB, GitHub PoCs/tooling, HTB patterns, NVD, CISA KEV, OWASP, or CWE:

1. Treat external sources as pattern/tool intake, not proof.
2. Mirror metadata first when useful, then acquire selected scripts/repos into a git-ignored local library such as `setting/local/tool_acquisition/<wave>/`.
3. Record provenance for every acquired item: source URL, category, purpose, fetched time, size/hash when available, and status.
4. Default acquired exploits to `reference-only` until reviewed. Do not run raw third-party exploit code blindly.
5. Prefer extracting safe technique/payload shape into a lab-specific bounded runner.
6. Target-touching execution stays on the tool lab (`<attacker-vm>` for this project) and only against authorized local/CTF/client/scope-approved targets.
7. Preserve a handoff such as `handoff/script_acquisition_waveN_<date>.md` and mention failed/retryable downloads separately.

Useful category buckets:

- path traversal / LFI / file disclosure
- file upload / upload retrieval / execution-boundary
- XSS runtime proof
- auth bypass / IDOR / access control
- SSRF / XXE / deserialization
- wordlists/payload references (bounded subsets only)

## Disposable target expansion pattern

If the current靶機 cannot demonstrate a modern proof type, do not repeatedly force unrelated CVEs onto it. Add or modify a local intentionally vulnerable target when that gives cleaner evidence.

Good reasons to add a disposable local target:

- IDOR needs own-object vs other-object proof.
- Upload was accepted but retrieval/execution boundary cannot be proven.
- SSRF needs an isolated callback log without external OAST.
- XXE needs a real XML parser/input surface.
- Deserialization needs a controlled serialized-object sink.
- XSS needs a reliable runtime/browser proof fixture.

Minimum target requirements:

- local/private/scope-documented host such as `127.0.0.1` or host-only lab IP;
- simple start/stop scripts;
- pre/post health endpoint;
- disposable state or known cleanup path;
- no real secrets, credentials, persistence, or external callbacks;
- artifacts pulled back to repo-local `<artifact-output-dir>/` or equivalent;
- verified and valuable flows written to bundles with exact evidence and boundaries.

If Docker/Compose is unavailable, a small Python/Node stdlib target is acceptable for fast local proof, as long as the session records why a custom target was added and how to stop it.

## Bundle status discipline

Do not require full target control, file read, or RCE for retention. Retain useful work as:

- `verified-impact` — runtime/impact proof exists;
- `valuable-candidate` — reusable workflow, precondition mapping, false-positive handling, or attack-chain step exists;
- `attempted-not-verified` — tried with artifacts but no proof;
- `blocked/deferred` — missing target surface/tool/callback/auth/recovery condition;
- `reference-only` — useful intelligence/tooling but not applicable to the current lab.

## Evidence examples

For IDOR/object ownership:

- low-priv user token;
- own object 200 + own marker;
- other user's object 200 + other marker;
- clear statement that this is object ownership failure, not generic metadata.

For upload retrieval:

- upload response code and returned ID/path;
- retrieved body contains harmless marker;
- boundaries: not RCE, not arbitrary write, not webshell unless explicitly proven.

For SSRF callback:

- fetch endpoint request;
- isolated local callback log count/marker;
- boundaries: no cloud metadata, no external OAST, no internal scan unless separately authorized.

For browser-runtime XSS:

- do not treat reflected payload text as proof;
- use a real browser/headless browser when possible;
- prefer a harmless DOM mutation marker such as `document.body.setAttribute('data-xss','XSS_RUNTIME_MARKER')`;
- verify the dumped DOM or browser artifact contains the mutated marker, not just the original URL/payload;
- boundaries: no credential theft, no external callback, no persistence.

For bounded XXE:

- use a known safe marker file created by the disposable target or test harness;
- assert the response contains only that marker;
- do not read `/etc/passwd`, cloud metadata, SSH keys, tokens, or real secrets for routine lab proof;
- record the marker path, request XML, response JSON, and non-claims.

For bounded unsafe deserialization:

- prove the sink with an in-process marker recorder or other no-shell side effect;
- do not use reverse shells, command execution, persistence, filesystem writes, or external callbacks for the default proof;
- record the payload artifact, response, server-side marker log, and explicit boundaries;
- label the impact as server-side callable/gadget invocation unless command execution is separately authorized and proven in a disposable lab.
