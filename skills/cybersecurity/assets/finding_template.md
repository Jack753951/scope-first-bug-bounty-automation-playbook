> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Finding Template — single vulnerability block

Copy this block once per finding in §4 Detailed Findings.

---

## F-XX — [Concise Title — verb + asset, e.g. "SQL Injection in /login"]

| | | | |
|---|---|---|---|
| **Severity** | _Critical / High / Medium / Low / Info_ | **CVSS 3.1 Score** | _0.0–10.0_ |
| **CVE / CWE** | _CVE-YYYY-XXXX / CWE-XXX_ | **OWASP** | _e.g. A03:2021-Injection_ |
| **CVSS Vector** | _AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H_ | | |

### Description
[1–2 paragraphs. Plain explanation of the flaw. Avoid pasting raw scanner output. Identify the affected component, version, and the unsafe behaviour.]

### Affected Assets
- `https://target.example/path`
- `hostname.internal:port`

### Impact
[Concrete business impact across CIA. Quantify when you can: "An unauthenticated attacker can read all user records (~120k accounts) and modify any user's profile." Avoid generic phrases like "could allow attackers to gain access".]

### Proof of Concept

**Pre-conditions**: [What state must hold — e.g. "Anonymous access to /login"].

**Step 1 — Request:**
```http
POST /login HTTP/1.1
Host: target.example
Content-Type: application/x-www-form-urlencoded

username=admin' OR '1'='1&password=x
```

**Step 2 — Response:**
```http
HTTP/1.1 302 Found
Location: /admin/dashboard
Set-Cookie: session=...; HttpOnly
```

[Add screenshots or extra steps as needed. Each step should be replayable by the developer.]

### Remediation

**Short-term (within 48 hours):**
- [WAF rule blocking the pattern, feature flag disabling the endpoint, etc.]

**Long-term (root-cause fix):**
- [Parameterised queries / prepared statements; authorization layer; library upgrade.]

**Verification (how the client can confirm the fix):**
- [Replay PoC and confirm the response is no longer exploitable; specify the expected response.]

### References
- OWASP: https://owasp.org/Top10/A03_2021-Injection/
- CWE: https://cwe.mitre.org/data/definitions/89.html
- Vendor advisory / CVE: [URL]
- Related blog post / writeup: [URL]
