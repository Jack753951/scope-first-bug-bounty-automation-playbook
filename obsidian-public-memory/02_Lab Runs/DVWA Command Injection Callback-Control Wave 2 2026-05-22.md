> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# DVWA Command Injection Callback-Control Wave 2 2026-05-22

Status: completed / verified command execution + marker + Docker-bridge callback
Repo handoff: `<user-home>`
Source inventory: `<user-home>`
Artifacts: `<user-home>`

## Result

Verified:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data
DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T054954Z
```

Verified callback record:

```json
{"ts":"2026-05-22T05:50:03+00:00","remote":"172.17.0.5","query":"marker=DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T054954Z","ua":""}
```

## Caveat

Callback is Docker-bridge local lab callback, not true attacker-VM high-port callback. Aggressive-lab inbound remains blocked except SSH.

## Source inventory summary

Requested source families represented: 5/6.

- OWASP/vulnerable labs: active, 14 verified bundles.
- CISA KEV: ingested/mapped.
- NVD/CVE: ingested/briefed, some unverified due egress limits.
- Exploit-DB: 25 references acquired.
- GitHub: 6 repos acquired, 1 retryable failure.
- HTB: 0 concrete runs yet.
