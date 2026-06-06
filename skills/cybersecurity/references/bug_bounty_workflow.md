> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Bug Bounty Workflow Reference

Read when the user asks about <bug-bounty-platform> / Bugcrowd / Intigriti / YesWeHack / Synack programs, "should I report this," report writing for bounties, AI tool use in bounties, or how to start hunting.

> **Bug bounty ≠ pentest.** A bounty report is read by a triager who sees 50+ submissions a day. It must stand on its own with no prior context. A pentest report assumes an engaged client engineering team. Optimise for the format you're actually in.

## Table of contents
1. The bounty hunter's mindset (and why most beginners fail)
2. Reading a program scope
3. 2026 platform-specific AI / automation policies — KEY SECTION
4. Recon strategy that doesn't get you banned
5. Allowed vs forbidden tools
6. Where AI use is actually OK (and where it isn't)
7. Report writing for bounties — differs from pentest reports
8. Common rejection reasons
9. Operational hygiene
10. Beginner-friendly programs
11. When to submit, when to drop

---

## 1. The bounty hunter's mindset

The depressing math:
- ~80% of submissions are duplicates, out-of-scope, or informational.
- Triagers across most platforms are now **drowning in AI-generated noise** — multiple high-profile programs (curl, Nextcloud, Node.js) have shut down or paused their bounties in late 2025 / early 2026 because of "AI slop".
- Successful hunters specialise. The general-purpose "I run a scanner against everything" approach worked in 2018; it gets you banned in 2026.

**What works:**
1. Pick a narrow class (SSRF, OAuth, GraphQL, SAML, JWT, Web Cache, Prototype Pollution, …) and master it across many programs.
2. Read every public report on that class — <bug-bounty-platform> Hacktivity, GitHub advisories, blog write-ups.
3. Build small, targeted, manual-augmented automation, not generalised AI-driven scanners.
4. Aim for fewer, higher-quality reports.

---

## 2. Reading a program scope

Before testing, extract these specifically. Quote them in your notes.

| Field | What to find | Why it matters |
|-------|--------------|----------------|
| In-scope assets | Domain wildcards, mobile apps, APIs, IP ranges | Touch only these |
| Out-of-scope assets | Often subdomains owned but excluded (status pages, marketing CMSs) | Auto-reject if violated |
| In-scope vuln types | Often a published list aligned with OWASP | Anything else = informational |
| Out-of-scope vuln types | Common: missing security headers, CSP without exploit, self-XSS, clickjacking on non-sensitive pages | Don't waste your or the triager's time |
| Severity / payout matrix | Bug class × bounty amount | Influences whether it's worth chasing |
| Test account requirements | Some programs *require* you use program-supplied accounts | Using your own = potential rejection |
| PII handling | "Stop at proof of access; do not enumerate user data" | Common rule; violating = ban |
| Disclosure terms | Embargo length, blog post permission | Affects your career story |
| Rate limit policy | "X requests per second", "no automated scanning" | See §3 |

If anything is ambiguous, ask the program staff via the platform **before** testing. Asking is free; getting banned is not.

---

## 3. 2026 platform-specific AI / automation policies (CRITICAL)

These are time-sensitive. Always re-verify on the platform's policy page before relying on this section.

### <bug-bounty-platform> (as of Q1 2026)
- **AI Research Safe Harbor** (introduced Jan 2026) — opt-in, separate from existing Gold Standard Safe Harbor, covers good-faith testing of AI systems.
- <bug-bounty-platform> does **not** train models on researcher submissions or customer data.
- After widespread "AI slop" incidents (curl publicly shut down its program citing AI-generated reports; Node.js suspended bounty releases), <bug-bounty-platform> emphasises **human validation** before submission.
- AI vuln-report volume reportedly up **210%** year-over-year — triage capacity didn't scale with it.

**Practical implication**: Submitting unverified AI-driven findings on <bug-bounty-platform> in 2026 will tank your reputation. They allow AI assistance, but you own every word in the submission.

### Bugcrowd (as of March 2026)
- Coined the term **"sloptimism"** — speculative or AI-generated reports submitted with minimal validation.
- **Permanent ban** for accounts identified as "submission farming".
- **30-day suspensions** for accounts submitting automated / AI-generated activity without sufficient pre-submission validation.
- Submission policies, rate controls, and detection mechanisms have been tightened.

**Practical implication**: Bugcrowd is the strictest of the big three on AI volume. One bad batch can lose you the account.

### Intigriti
- Automated tools allowed, but **rate-limited to 2–10 requests/sec depending on program**.
- Some programs disallow automated testing entirely — read each program's specific scope.
- Aggressive scanning is treated as a service-degradation incident.

**Practical implication**: Tune your tools per-program. Don't use a global "go-fast" config across all programs.

### YesWeHack
- Generally aligns with Intigriti-style: per-program rate rules, automation allowed within bounds. Always read the program brief.

### Synack Red Team
- Invite-only / vetted. Internal tooling and rules differ; if you're in, follow their internal docs.

### Public VDPs (Vulnerability Disclosure Programs)
- No bounty, but more relaxed scope. Good place to learn report writing without bounty pressure.

---

## 4. Recon strategy that doesn't get you banned

### Tier scans by intrusion level

```
Tier 0 — Pure passive (NO traffic to target)
├─ crt.sh, archive.org, GitHub dorks, Shodan/Censys (read-only),
   public NVD/CVE lookups, JS file analysis from production HTML

Tier 1 — Low-rate active enumeration
├─ DNS queries (subfinder, dnsx with default rates)
├─ HTTP probing one request per host (httpx)
├─ Burp Suite manual browsing — same speed as a real user

Tier 2 — Targeted active probing
├─ ffuf with -rate 5 (5 req/s)
├─ nuclei with -rl 10 (10 req/s) on specific templates only,
   not the full template library
├─ Manual injection testing in Burp Repeater

Tier 3 — Scanner runs (only if scope allows + program permits + rate-limited)
├─ Full nuclei runs, automated parameter discovery, fuzzing campaigns
└─ Throttle to per-program max RPS; pause on first sign of throttling
```

Most beginners run a global Tier-3 scan from minute one. That's how you get banned and never find the bug because the WAF is blocking you.

### Sustainable recon checklist

1. **Read the program brief twice**, including the changelog if available.
2. Save scope to a local file. When you're 5 hours deep, you'll forget what was excluded.
3. Start at Tier 0 — find the JavaScript files, secrets in repos, archived endpoints.
4. Tier 1 only after you've exhausted passive sources.
5. Use the program's test account if provided.
6. Check the platform's "trending" page — recently-changed scope often = fresh bug surface.

---

## 5. Allowed vs forbidden tools

### Generally allowed (with caveats)
- **Burp Suite Community / Pro / Caido** — manual proxy + targeted Repeater / Intruder.
- **nuclei** with rate-limit + specific templates only.
- **ffuf** with rate-limit.
- **sqlmap** *only after manual confirmation* of an injection point — never as a first probe.
- **Custom scripts** for narrow tasks (a one-off param discovery, JS endpoint extraction).
- **subfinder / amass / dnsx** for passive enumeration.
- **Shodan / Censys / FOFA** for passive lookups.

### Generally forbidden without explicit permission
- Mass scanners hitting at uncontrolled rate (Acunetix, Burp Active Scanner on `*.target.com` without scoping).
- AI agents that fan out across the surface (think: "let an LLM browse and click everything").
- Brute-force at scale (auth, password reset, IDORs across all IDs).
- Headless full-site crawlers without rate limits.
- Vuln scanners ran against assets you haven't confirmed are in scope.

### Always forbidden
- **Denial of Service** of any kind, including protocol-level (Slowloris, large-payload).
- Accessing other users' data beyond the minimum needed to demonstrate impact.
- Exfiltrating data — read one record to prove access; don't dump the table.
- Public disclosure before the program's embargo or before you have permission.
- Social engineering of staff unless explicitly in scope (almost never is).
- Physical attacks.
- Testing third-party services that happen to be on the target's domain (CDN, SaaS).

---

## 6. Where AI use is actually OK (and where it isn't)

Use AI for **work that doesn't reach the program**. Skip AI for **anything that becomes the submission**.

### OK
- Recon notes organisation, deduplication, summarisation.
- Drafting your written reports — then **edit every sentence**.
- Source code review on disclosed JS / open-source repos.
- CVE research / explaining a class of bug to yourself.
- Generating a wordlist for a specific tech stack.
- Writing one-off recon scripts.
- Triaging your own findings before submission ("does this actually have impact?").

### Borderline (only with manual verification)
- AI-suggested payloads in Burp Repeater — fine if you verify each one yourself.
- AI-generated nuclei templates — fine if you read and tune before running.

### Not OK
- AI agent autonomously crawling the target and "finding bugs."
- LLM-generated reports submitted without manual reproduction.
- Pasting the program scope into a generic LLM and asking "what's vulnerable?" — produces hallucinated findings.
- Any workflow where the AI decides what gets submitted.

**The litmus test**: if a triager asked "did you personally confirm every step in this report?" — and you can't say "yes" with a straight face — don't submit it.

---

## 7. Report writing for bounties (≠ pentest reports)

A bounty report is read in 5 minutes by a triager weighing it against 49 others. Optimise for that.

### Title
- Scannable. Mentions the bug class + asset + impact in 12–15 words.
- **Bad**: "Vulnerability in profile page"
- **Good**: "Stored XSS in profile bio field on app.example.com leads to account takeover via cookie theft"

### Severity
- Use the program's published rating system. Don't argue you deserve Critical when their matrix says High.
- Provide CVSS 3.1 vector + score. Vector justifies the score.

### Reproduction steps
- Numbered. Every step copy-pasteable. Every header. Every payload exact.
- Include: starting URL, login state, exact HTTP requests (use Burp's "Copy as curl"), and the response that proves impact.
- One screenshot per logical step. Don't dump 30 screenshots.

### Impact
- Concrete and quantified. Avoid "could allow attackers to..." weasel-words.
- **Bad**: "An attacker could potentially access user data."
- **Good**: "A logged-in attacker can read any other user's email, phone, address, and password reset token by changing the `userId` parameter (verified for user IDs 1042 and 1043; 4.2M users in scope)."

### PoC
- Screenshots > video. Triagers can't fast-forward screenshots.
- If video is necessary, ≤ 60 seconds, no commentary, time-stamped to relevant moments.

### Don't escalate beyond proving the bug
- One IDOR confirmation = enough. Don't dump the database.
- One read of admin email = enough. Don't read 100.
- One token theft proof-of-concept = enough. Don't pivot to other accounts unless asked.

### Don't submit similar low-value bugs in bulk
- Found 30 reflected XSS in 30 marketing pages? That's likely 1 report explaining the systemic gap, not 30 individual ones (and many programs explicitly de-duplicate this way).

### Suggest a fix
- Brief, not preachy. "Use parameterised queries" is a sentence, not a paragraph.

### Reference template

```markdown
## Title
[Class] in [Asset] leads to [Impact]

## Severity
Critical / High / Medium / Low — CVSS 3.1: 9.8 (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)

## Affected Asset
https://app.example.com/api/v1/users/{id}

## Summary
[One paragraph, plain English, what's wrong and what an attacker can do.]

## Steps to Reproduce
1. Log in as user A: alice@example.com / Test123!
2. Navigate to /profile.
3. Send the following request:
   ```http
   GET /api/v1/users/1043 HTTP/1.1
   Host: app.example.com
   Cookie: session=...
   ```
4. Observe response — full record of user 1043 returned.

## Impact
[Quantified business impact.]

## Proof of Concept
[Screenshots / minimal video.]

## Suggested Fix
Add server-side authorization on /api/v1/users/{id} requiring requested ID == authenticated user's ID, or that authenticated user has admin role. Verify via the same request after fix expects 403.

## References
- OWASP A01:2021 (Broken Access Control)
- CWE-639 (Authorization Bypass Through User-Controlled Key)
```

---

## 8. Common rejection reasons

| Rejection | Why it happens | How to avoid |
|-----------|----------------|--------------|
| Out-of-scope | Tested an asset not in the program | Re-read scope; quote it in your report |
| Duplicate | Someone else already reported it | Check Hacktivity for known issues; submit early |
| Informational | Missing headers, theoretical CSP, self-XSS | Don't submit unless explicitly in scope and exploitable |
| No impact / theoretical | "Could lead to..." but no PoC | Demonstrate concrete impact |
| Low quality / AI slop | Hallucinated reproduction, no real PoC | Don't ship without manual verification |
| Scope-excluded class | Program excludes this vuln class | Read the brief |
| Insufficient PoC | Vague reproduction steps | Be exact, copy-pasteable |
| Won't fix | Accepted risk by program | Out of your control; don't argue |

---

## 9. Operational hygiene

- **Separate testing browser profile** (Firefox container or dedicated Chrome profile per program). No bookmarks, no logged-in personal accounts.
- **VPN** that isn't on common blacklists (Mullvad, IVPN, ProtonVPN are usually fine; avoid free).
- **Don't reuse test accounts across programs** — credential collision = scope confusion.
- **Save evidence at the time of finding**, not retro. Use Burp's session save, take screenshots immediately.
- **Rate-limit yourself manually** — when in doubt, slower than the spec.
- **Local notes per-program** in your `lab_notes_template.md` format.
- **Keep an evidence directory per submission** — screenshots, raw HTTP exchanges, PoC scripts. Triagers may ask for more.

---

## 10. Beginner-friendly programs

| Type | Why good for beginners |
|------|----------------------|
| **VDP (no bounty)** | Lower competition, friendlier triagers, learn report writing without pressure |
| **Public bounty on legacy products** | Wider attack surface, fewer top hunters bothering |
| **GitHub Security Lab** | Source-code-driven, tutorials available, CodeQL focus |
| **Niche industry programs** (healthcare devices, gov, ICS, OT) | Specialised competition is thinner |
| **Time-bounded competitions / pwn2own** | Forced focus on a narrow target, fast feedback |

Stay away as a beginner from:
- Top-tier consumer programs (Google, Apple, Meta) — high-skill saturation, you'll mostly find dups.
- Web3 / crypto bounties — code review skills required, mistakes can be expensive.

---

## 11. When to submit, when to drop

Submit when ALL of these are true:
1. The bug class is in scope.
2. The asset is in scope.
3. You have a clean, replayable PoC.
4. You can articulate concrete impact in one paragraph.
5. You're confident it's not a duplicate (search Hacktivity / public CVEs).
6. The severity per the program's matrix is at or above your time-cost threshold.

Drop when:
- It's "interesting" but exploitation requires unrealistic preconditions.
- You've spent more time writing the report than you'd be paid for.
- The program is known for low-paying / hostile triage and an alternative target is available.
- You're not sure it's reproducible — file it as a learning note, don't submit.

---

## What to refuse helping with

- "Help me write a generic LLM agent that submits bugs to <bug-bounty-platform> automatically." — that gets the user banned. Suggest manual augmentation instead.
- "Generate 50 reports from this scanner output." — pure AI slop pattern. Refuse and explain.
- "I think this is a bug but I haven't tested it; can you write the report anyway?" — no. Verification is the user's job; the report follows.
- Asking which programs to "abuse" with automation. Reframe to "where to learn safely."
