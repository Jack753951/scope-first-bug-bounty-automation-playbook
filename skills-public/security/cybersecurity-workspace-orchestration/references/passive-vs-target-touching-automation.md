> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Passive vs target-touching automation modes

Use this reference when the operator asks whether the workspace will automatically use websites, query IP/MAC data, capture traffic, or run network analysis.

## Default stance

The platform may automate passive research and local/offline analysis, but it must not automatically perform target-touching network activity against live/public targets.

Treat these as different modes:

1. Passive research
   - Allowed by default when relevant: public documentation, vendor advisories, CVE/GHSA/NVD/CISA KEV, package registries, public HackerOne metadata, API docs, OUI/vendor lookup pages, ASN/whois/reverse-DNS lookups, and public PoC reading.
   - Do not log in to target apps, call target APIs, or mutate target state under this mode.

2. Offline/local evidence analysis
   - Allowed when the operator provides files or the data is already local: pcap, Zeek/Suricata output, web/server/auth logs, redacted requests/responses, IP/domain lists, MAC/OUI values, VM interface data.
   - Redact or avoid storing secrets: cookies, bearer tokens, passwords, OTPs, private keys, verification links, phone numbers, and non-owned data.

3. Local/lab network analysis
   - Allowed when explicitly framed as user-owned lab, disposable VM, CTF, or靶機 work.
   - IP/MAC/ARP/interface checks and packet capture are fine inside the declared lab boundary, with temporary NAT/downloads only when approved and verified closed afterward when required by project policy.

4. Authorized live target
   - Requires exact scope, program/client rules, `config/scope.txt`/program scope alignment, and explicit operator approval for the specific action.
   - Do not auto-run scans, fuzzers, DAST, nmap/masscan/nuclei, callback/OAST/tunnels, target API calls, invite/team/role mutations, workflow activation, OAuth/channel/mailbox connections, traffic capture/MITM, or report submission.

## IP / MAC / traffic decision rule

- This machine / VM / owned lab subnet: safe to inspect when useful.
- User-provided artifacts: safe to analyze offline, redact before preserving.
- Public IP/domain in live bounty or unknown ownership: passive lookup only unless scope and operator approval authorize active probes.
- MAC/OUI lookups are generally passive; discovering MACs on a network is target-touching unless it is the local/owned lab.
- Traffic capture is local/lab-only unless separately authorized; do not initiate MITM or capture live target sessions by default.

## Operator-facing short modes

Offer these concise mode labels when clarifying intent:

```text
passive research only
local/lab network analysis
analyze provided pcap/logs only
authorized live target: <scope> / <allowed actions> / <blocked actions>
```

## Pitfall

Do not answer "yes, it will use needed sites/tools automatically" without separating passive websites from target-touching actions. The operator is often asking about capability, but the safe answer must state what is automatic, what requires approval, and what remains blocked by default.