> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: ctf-challenge-workflow
description: Blind triage and solve workflow for CTF/training challenges, emphasizing Kali-first external interaction, output-side review, reusable lesson capture, and escalation to second review/multi-agent when ambiguity or advanced crypto/reversing appears.
---

# CTF Challenge Workflow

Use this skill when the user gives a CTF/training challenge name, description, URL/host/port, or local attachment and wants it solved or used to validate the cybersec workflow. This is class-level: web, crypto, reverse, forensics, misc, and source-code puzzles all start here unless a more specific skill clearly applies.

## Core intent

The user's goal is not only getting flags. Treat each challenge as a way to:

- validate the scan/triage/verification pipeline;
- improve weakness-pattern recognition;
- practice selecting safe tools and probes;
- decide when output requires second review;
- preserve reusable technical lessons in Obsidian or skill references.

## Default workflow

0. Declare solving mode and source transparency.
   - Before starting, label the run as `blind training` or `assisted solve`.
   - In `blind training`, do not use search engines, writeups, browser-based hints, public exploit scripts, or solution pages. Allowed sources are the challenge prompt, provided artifacts, local tools, man pages, language/library docs, libc/source docs, and official platform connection details.
   - In `assisted solve`, external hints/writeups are allowed, but the final report must clearly separate: what came from external hints, what was independently reasoned, what was rebuilt locally, and what was actually verified against the local/remote challenge.
   - If the mode changes mid-session, say so explicitly; do not let an assisted result read like a blind solve.

1. Scope gate first.
   - Confirm it is CTF/training/lab/authorized.
   - For picoCTF/HTB/TryHackMe/PortSwigger Labs, minimal challenge interaction is allowed.
   - Do not use recon/fuzz/brute force unless the challenge clearly requires it and the scope is explicit.

2. Kali-first for external interaction and security tooling.
   - If touching an external website, `nc` service, remote host/port, downloading challenge resources, or running security tools, prefer Kali.
   - Windows host is fine for orchestration, repo files, Obsidian notes, local source review, and local deterministic scripts.
   - Offline local attachments can be analyzed on Windows if no external target/tool interaction is needed.

3. Blind triage.
   - Do not rely on the user to tell the category.
   - Infer type from description, files, protocol behavior, source language, magic bytes, UI, endpoints, crypto structure, binary format, etc.
   - Record hypotheses and the minimal next probe.

4. Minimal probe / artifact capture.
   - Prefer low-noise, deterministic interactions: fetch provided files, read source, single HTTP request, limited `nc` transcript, file metadata.
   - Store transient scripts/artifacts under `setting/local/<challenge-slug>/` or Kali `~/codex-output/<challenge-slug>/` as appropriate.

5. Solve with verification built in.
   - Do not trust the first candidate just because a UI says “Correct”, a checker returns true, or a public writeup contains a flag.
   - Re-run the original transform/checker when possible.
   - For generated files/images, validate file format invariants, checksums/CRC, parser acceptance, and decoded content.
   - For crypto/key recovery, verify recovered keys by re-encrypting known plaintext/ciphertext pairs before decrypting the flag.

6. Output-side review decision.
   - Accept without second review only when the candidate is deterministic, verified, and format-consistent.
   - Trigger second review or multi-agent escalation when:
     - flag format is abnormal or missing expected wrapper/terminator;
     - checker logic involves C strings, `strcmp`, `strlen`, embedded NULs, or binary/string boundary ambiguity;
     - multiple candidate outputs exist;
     - the result comes from probabilistic/statistical crypto;
     - generic solver/SMT times out or gives underconstrained output;
     - a public writeup answer may be stale or instance-specific;
     - the next action would require stronger target-touching probes.

7. Lesson capture and bug-bounty mapping.
   - Put full technical notes in Obsidian or repo-local notes.
   - Keep Hermes memory short: only durable trigger phrases.
   - Add durable class-level patterns to this skill or `references/` when a non-trivial method emerges.
   - Because this user's CTF work is primarily bug-bounty workflow calibration, close each meaningful challenge with a mapping section, not just a flag:
     - `challenge_result`: blind/assisted, solved/partial/blocked, local verification, remote verification.
     - `technical_pattern`: vulnerability class, root cause, exploit/verification conditions, false-positive traps.
     - `bug_bounty_mapping`: analogous real-world weakness class, candidate-finding evidence needed, manual verification steps, impact questions, report-readiness blockers.
     - `platform_improvement`: whether to update a checklist, candidate finding/evidence schema, reviewer prompt, scope/policy gate, module manifest field, or report-readiness classifier.
   - Do not let CTF solving become the main roadmap; use it to improve authorized bug-bounty candidate → review → verification → report workflow.

## Common CTF patterns from validated sessions

### C-string / WASM false positives

If validation uses `strcmp`/`strlen` or binary data may contain embedded NUL bytes, a prefix can pass while the real flag continues after `\0`. Inspect the full data segment, not just UI success.

### JavaScript image reconstruction

For client-side puzzles that rebuild an image from byte arrays:

- read the transformation rather than guessing inputs;
- use file magic bytes (PNG/JPEG/GIF/ZIP/PDF) to constrain keys;
- use checksums/CRC/parser acceptance to remove ambiguity;
- decode QR/barcode only after the file validates structurally.

### Source-code reverse with bit permutations

For “vault door” style source challenges:

- ignore obfuscating presentation and find the final equality check;
- isolate the transform and expected constants;
- check if the transform is a permutation or self-inverse operation;
- invert in reverse order;
- verify by reapplying the original transform byte-for-byte.

### Custom crypto with chosen-plaintext oracle

For custom block ciphers:

- identify block size, padding, oracle capabilities, and per-block independence;
- avoid relying solely on generic SMT when modular multiplication or many bit-vector variables appear;
- search for structural differentials/invariants;
- if using recovered keys, verify by re-encrypting oracle pairs before decrypting the flag.

### Hash-selected generated-code checkers

For reverse/crypto-ish password checkers that hash salted input chunks, select digest bytes, then compare or execute the result:

- reverse the exact input chunking, salts/constants, hash windows, output byte ordering, and register state at the decision point;
- search for the shortest useful code/check effect rather than a full obvious shellcode, because bytes after an early `jmp`/`ret` may be arbitrary;
- if a success/check function pointer is already passed in a register, consider jumping into its success path instead of materializing the full expected argument;
- treat selected digest windows as partial-preimage constraints and brute force independent chunks locally;
- for binary passwords, record hex and submit via script rather than an interactive terminal;
- verify by reimplementing the transform and confirming generated bytes before the final remote submission.

See `references/picoctf-rolling-my-own-md5-shellcode.md` for the concrete Rolling My Own pattern.

### Threat hunting / SIEM simulator timelines

For TryHackMe-style SOC/threat-hunting simulators where the user must validate a hypothesis from SIEM logs and fill timeline stages:

- Treat the run as authorized training/log analysis, not a live target or bug-bounty asset.
- Broad-search explicit IOCs first, then build a raw chronological evidence table before selecting MITRE tactic/technique values.
- Do not over-split every telemetry event into separate stages before seeing the simulator's expected IOC buckets. Some platforms expect consolidated stages such as: package/initial access, PowerShell execution + decoded command, registry persistence, then only verified follow-on activity.
- If feedback names missed IOC classes, align stages to those buckets. Example: `PowerShell Command` and `Decoded Command` usually belong in the execution stage; `Registry Path` and `Registry Value Name` belong in the registry persistence stage.
- If a tactic/technique is marked wrong despite being MITRE-plausible, inspect the platform dropdown/feedback instead of defending the generic mapping; choose the option matching the grader's evidence class.
- When feedback says `investigation incomplete` / `trail went cold`, search for follow-on results: payload file creation, payload process execution, outbound network activity, internal access to named infrastructure, or same IOCs on additional hosts.
- Use company context to prioritize impact and follow-up hunts, but do not turn business impact into an attacker stage unless the form supports non-attacker-activity notes.

See `references/threat-hunting-simulator-timeline.md` for a reusable timeline/reporting pattern and pitfalls.

### Threat hunting / SOC simulator timelines

For TryHackMe/SOC simulator tasks where the challenge gives company context, employees, logs, hypotheses, or IOC feedback:

- Treat it as `blind training` unless external writeups are explicitly allowed.
- Do not over-split every log event into separate timeline stages before understanding the grader's expected evidence categories.
- Build an evidence-first chain from broad IOC searches, then map stages to core artifacts: initial package/source, execution command, decoded command, system change, payload execution/network/lateral activity.
- When grader feedback lists missed IOCs by stage, rewrite the timeline around those stage numbers. Example: PowerShell Command + Decoded Command in Stage 2; Registry Path + Registry Value Name in Stage 3.
- Each stage must state findings and implications, not only a tactic label. Include exact timestamp, host, user, raw command/artifact, decoded behavior, and follow-up result.
- Business context matters: map host to employee/role and use important servers/subnets as follow-up hunt pivots, but do not invent impact without log evidence.

See `references/threat-hunting-simulator-timelines.md` for the reusable form-filling and feedback-interpretation pattern.

### Threat-hunting / SIEM simulator timeline tasks

For TryHackMe-style SOC simulators, attack-chain builders, and SIEM timeline forms:

- Treat the task as authorized training, but avoid active scanning unless the room explicitly requires it.
- First search broad IOCs and reconstruct the event chain before filling MITRE fields.
- Do not over-split every log artifact into separate stages when the simulator expects coarse stages. A common expected shape is: initial package/vector → command/script execution with decoded payload → registry/file/system change → network/payload staging → impact/scope follow-up.
- Put IOCs in the stage where the platform expects them, not only where they were discovered. Example pattern from npm supply-chain labs: NPM package in Stage 1; PowerShell command and decoded command in Stage 2; registry path and registry value name in Stage 3.
- When platform feedback says the investigation is incomplete, look for missing follow-up evidence: whether the script executed, what the decoded command did, whether a payload was written/executed, what system changes occurred, and whether additional hosts or important internal assets were touched.
- For ransomware simulator prompts, do not stop at the first encrypted host. Pivot on the encryption extension, ransomware process, credential-tool activity, and remote-session user context across all hosts, especially when the prompt says "two machines" or "another developer".
- Split late-stage activity when the form supports it: credential access (for example Mimikatz), lateral movement / alternate credentials (for example pass-the-hash or WinRM), and impact (ransomware encryption) are separate evidence questions even if they occur in one narrative.
- If tactic/technique feedback marks a theoretically valid MITRE mapping wrong, adapt to the platform's expected taxonomy and ask for/dropdown screenshots before guessing.
- Prefer specific ATT&CK sub-techniques in graded forms; parent techniques are often rejected even when the narrative is correct.
- Descriptions should include both finding and implication: what happened, what evidence proves it, why it matters for mitigation/reporting, and what follow-on result it caused.

See `references/threat-hunting-ransomware-simulator.md` for ransomware-specific SIEM timeline staging, MITRE mapping hints, and second-host scope pitfalls.

If the simulator expects a long timeline (around 20 stages), use `references/trygovme-ransomware-20-stage.md` for the expanded stage taxonomy, second-host pivot workflow, child-technique mapping pitfalls, timestamp/asset correction heuristics, and Kibana console-proxy query pattern.

### Web CTF source-first vulnerability solving

For Web category CTFs, picoCTF/PortSwigger/HTB/TryHackMe labs, and intentionally vulnerable apps:

1. Confirm the challenge/lab scope, then inventory source files, Docker/compose, package manifests, database seeds, environment variables, and exposed endpoints before live probing.
2. Map trust boundaries: forms, JSON bodies, headers, cookies, uploads, path/query params; state such as sessions/tokens/roles; sinks such as SQL/NoSQL, templates, filesystem, shell, URL fetchers, JWT/session signing, and redirects.
3. Form the smallest exploit hypothesis: read, write, auth bypass, role pivot, path read, SSRF, template eval, deserialization, etc.
4. Validate locally when possible and use the live instance only for server-only secrets or final flag retrieval.
5. Report more than the flag: root cause, exploit sequence, payload shape, why it worked, remediation, and the reusable recognition pattern.

SQLi review reminder: inspect `INSERT`, `UPDATE`, and `DELETE` sinks, not only `SELECT`. In CTFs, a write-context SQL injection against token/session/user/role tables can be a cleaner auth pivot than broad data dumping. See `references/web-ctf-sqli-token-pivot.md`.

### Heap pwn with global pointer tables

For pwn challenges with menu actions like allocate/free/rename and adjacent `.bss` globals:

- inventory exact global addresses, pointer tables, and allocator size classes before choosing fake chunk sizes;
- remember `read(size)` often consumes exactly `size` bytes, so local drivers must pad chunk payloads or later menu commands are swallowed as data;
- with glibc fastbin poisoning, distinguish the poisoned `fd` candidate chunk header from the user pointer returned by `malloc`; glibc validates size at candidate `+0x8`;
- when `%s` overreads are used for leaks, parse around controlled markers and delimiters because NUL bytes and format-string punctuation can truncate or pollute the leak;
- for glibc 2.23 challenges with Full RELRO/NX/canary/no PIE, expect staged exploitation: fastbin dup into `.bss` pointer table → fake small/unsorted-bin libc leak → House of Orange/FSOP, `main_arena.top` corruption into `__malloc_hook`, or another libc-2.23 control-flow technique.
- if menu allocation sizes block a direct hook-sized fastbin attack, check whether a controlled arena/top-pointer overwrite can make a legal request land near `__malloc_hook - 0x15`.
- after a hook overwrite, glibc 2.23 diagnostic/error handling such as deliberate double-free detection can be a valid trigger because it may allocate while printing/reporting the error.

See `references/picoctf-sice-cream-heap-pwn.md` for a concrete `sice_cream` pattern and pitfalls.

### WebAssembly-backed web validators

For web challenges that load `.wasm` or extensionless WebAssembly modules:

1. Fetch HTML/JS/WASM assets statically; find `WebAssembly.instantiate`, `fetch(...)`, exported `memory`, `check_flag`, `copy_char`, `strcmp`, or similar functions.
2. Verify WASM magic bytes, convert to WAT with `wasm2wat`/`wasm-objdump`, or use local Node `wabt` as a fallback.
3. Identify input buffer offsets, expected data segments, transform loops, signed-byte idioms, comparison calls, and any null terminator behavior.
4. Invert transformations in exact reverse order. For dependencies on prior transformed bytes, use the transformed prior bytes, not guessed plaintext.
5. Verify recovered candidates against the original WASM, but do not trust `check_flag() == 1` alone when C-string functions or embedded NULs are present; inspect full data segments past `\0` and confirm platform flag format.

See `references/wasm-validator-reversing.md` for the reusable workflow and `references/picoctf-some-assembly-required-4.md` for a concrete prefix-false-positive example.

## Authoring local practice drills

When the user asks for a quick CTF practice and no external challenge is specified, prefer a completely offline/local drill under `setting/local/<challenge-slug>/` so no target-scope or network action is needed. Include a README, checker/challenge file, and optional hint file; do not reveal the flag in the final user-facing message unless the user asks to solve/review it. Before presenting the drill, verify the checker with the intended solution and at least one wrong candidate. If the challenge embeds target constants, generate those constants from the intended solution instead of hand-copying them, then run the checker end-to-end; stale or mismatched constants make the exercise invalid.

## Projectization guidance

When the user asks to "push the project forward" after a CTF drill, do not keep solving by default. Convert the lesson into workflow assets:

- update Obsidian methodology notes with the durable pattern;
- add or update repo handoff docs/backlog for offline/local tooling;
- route contract-like tooling through Claude/Cowork direction review before Codex implementation;
- keep raw challenge artifacts under ignored local paths unless explicitly promoted.

A useful safe next slice is an offline CTF artifact + review-decision skeleton: prepare local challenge folders, generate solve-note/checklist templates, and classify solver output as `hint`, `candidate`, `verified`, or `needs_second_review` without doing network fetches by default. Keep confidence separate from status, use conservative second-review triggers, and test overwrite refusal/deterministic output/ignored target-scope override fields.

## References

- `references/2026-05-18-picoctf-workflow-validation.md` — session notes covering WASM embedded-NUL trap, JavaScript column-shifted PNG/QR reconstruction, Java bit-swap inversion, and Clouds/Nimbus differential cryptanalysis.
- `references/2026-05-18-ctf-to-platform-tooling.md` — escalation criteria, output-side review checklist, and P2.17-style offline tooling backlog for turning CTF lessons into platform workflow components.
- `references/offline-ctf-review-decision-skeleton.md` — reusable skeleton for local CTF artifact preparation and conservative solver-output classification.
