> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Protocols — Deep Reference

Read when a specific protocol comes up. Scan the table of contents first.

## Table of contents
1. TCP/IP basics (handshake, RST, sequence)
2. TLS 1.2 / 1.3
3. HTTP/1.1, HTTP/2, HTTP/3 (key differences for security)
4. DNS (records, DoH/DoT, zone transfer, rebinding)
5. SMB / CIFS
6. Kerberos
7. NTLM
8. LDAP
9. SSH
10. RDP
11. SMTP / DKIM / SPF / DMARC
12. SNMP
13. WebSocket / gRPC
14. OAuth 2.0 / OIDC / SAML / JWT

---

## 1. TCP/IP

- 3-way handshake: SYN → SYN/ACK → ACK. Port-scan techniques (SYN scan, FIN/Xmas/Null scan) abuse partial handshakes.
- RST sent on closed port → distinguishes closed vs filtered (filtered = no response).
- Sequence numbers should be unpredictable (<specific-cve-id> ARP/TCP issues exist on weak stacks).
- IPv6 first: many security tools default IPv4; attackers prefer IPv6 because monitoring is often weaker.

## 2. TLS

- **TLS 1.2 vs 1.3**: 1.3 removed insecure ciphers (RC4, 3DES, CBC-mode), made forward secrecy mandatory, simplified handshake (1-RTT or 0-RTT with caveats).
- **Forward secrecy** — ECDHE ciphers; an attacker capturing today's traffic + future server key doesn't decrypt anything.
- **0-RTT** in TLS 1.3 — fast resumption, BUT replay-able. Don't allow 0-RTT for non-idempotent requests.
- **Certificate validation**: hostname verification + chain to trust anchor + revocation (OCSP / CRL). Pinning beyond that adds risk if rotation isn't planned.
- **Common attacks**: BEAST (TLS 1.0 CBC), POODLE (SSL 3.0), Lucky13 (CBC timing), Heartbleed (OpenSSL bug, not protocol), CRIME / BREACH (compression). All resolved by using TLS 1.2 + AEAD or TLS 1.3.
- **Audit**: `nmap --script ssl-enum-ciphers -p 443 host`, `testssl.sh host`.

## 3. HTTP

### HTTP/1.1
- **Request smuggling** (CL.TE, TE.CL, TE.TE, H2.CL): <program-name>-end and back-end disagree on request boundaries. Mitigation: enforce one parser; reject ambiguous Content-Length / Transfer-Encoding combinations.
- **Caching attacks**: cache poisoning (unkeyed input ends up in shared cache), cache deception (`/profile.css` served with /profile data).
- **Header injection (CRLF)**: user input contains `\r\n` → injected headers / response splitting.

### HTTP/2
- Binary, multiplexed. Issues: HTTP/2 Rapid Reset (<specific-cve-id>), HPACK compression bombs.
- Smuggling between H2 frontend and H1 backend is its own class.

### HTTP/3 (QUIC over UDP)
- Inherits TLS 1.3 always. Newer surface — fewer mature scanners.
- AMP DoS via 0-RTT and connection migration; check vendor advisories regularly.

### Security headers checklist
- `Strict-Transport-Security` with `max-age=63072000; includeSubDomains; preload`
- `Content-Security-Policy` (use nonces, no `unsafe-inline`)
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- `Cross-Origin-Opener-Policy: same-origin`
- `Cross-Origin-Embedder-Policy: require-corp`

## 4. DNS

- Record types: A, AAAA, CNAME, MX, TXT, NS, SOA, SRV.
- **Zone transfer (AXFR)**: leaks every record. Should never be allowed from arbitrary IPs.
- **DNS rebinding**: TTL manipulation to make a hostname resolve internally after first request. Mitigation: validate Host header, refuse private IPs in answers for public hostnames.
- **DoH / DoT**: encrypted DNS. Defenders need to allow the right resolver and block public DoH from clients.
- **DNSSEC**: signs records. Reduces cache poisoning risk; doesn't add confidentiality.

## 5. SMB / CIFS

- Versions: SMB1 (broken — disable everywhere), SMB2 (default since Vista), SMB3 (encryption + signing).
- **SMB signing**: defeats relay attacks. Should be required on all DCs.
- **Null sessions** (anonymous bind): leak user lists; should be disabled.
- Tools: `smbclient`, `smbmap`, `nxc smb`, `enum4linux-ng`.
- Common bugs: EternalBlue (MS17-010), SMBGhost (<specific-cve-id>).

## 6. Kerberos

- TGT (issued by KDC for the user) → TGS (issued for a specific service) → service ticket presented to service.
- **Pre-authentication**: user encrypts timestamp with their hash; KDC verifies. Disabling pre-auth → ASREPRoast.
- **Service Principal Name (SPN)**: any account with SPN can be Kerberoasted (TGS encrypted with the service account's hash → offline cracking).
- **Encryption types**: AES256/AES128 preferred; RC4 (NTLM-derived) is the legacy weakness used in Kerberoasting.
- **Skew**: Kerberos requires clock sync (default 5 min); time misalignment breaks auth.
- **Ticket attacks**:
  - Golden — KRBTGT hash → forge any TGT.
  - Silver — service account hash → forge ticket for that service.
  - Diamond / Sapphire — modifications of legitimate tickets.

## 7. NTLM

- Challenge-response: server sends challenge, client encrypts with NT hash, server validates.
- **NetNTLMv2** is what you crack from Responder captures.
- **Pass-the-Hash**: NTLM hash is functionally equivalent to the password for NTLM auth.
- Mitigations: Protected Users group, disable NTLM where possible, enforce signing on SMB/LDAP, channel binding tokens for HTTP Negotiate.

## 8. LDAP

- Bind operations: anonymous, simple (cleartext over plain LDAP), SASL (Kerberos / NTLM).
- **LDAP injection**: same idea as SQL injection but in LDAP filters: `*)(uid=*))(|(uid=*` style.
- Use LDAPS (port 636) or STARTTLS on 389; never plain bind for credentials.
- Tools: `ldapsearch`, `windapsearch`, BloodHound's LDAP collection.

## 9. SSH

- Always v2; v1 is broken.
- Use ed25519 keys (or RSA-4096); disable password auth.
- `AllowUsers`, `Match Group`, `ForceCommand` for least privilege.
- Forwarding flags: `-L` local, `-R` remote, `-D` SOCKS dynamic — see `command_library.md` § Pivoting.
- Audit: `ssh-audit host`.

## 10. RDP

- TLS-based since Windows 7. Network Level Authentication (NLA) requires authentication before session — should be required.
- BlueKeep (<specific-cve-id>) — pre-auth RCE on legacy RDP. Patched, but legacy systems still bite.
- Restricted Admin mode + Remote Credential Guard prevent credential theft from RDP host.

## 11. Email auth (SPF / DKIM / DMARC)

- **SPF**: TXT record listing IPs allowed to send mail for the domain. Limited (10 DNS lookup cap).
- **DKIM**: signs message with domain key; recipient verifies via DNS-published public key.
- **DMARC**: alignment policy — does the visible `From:` align with SPF/DKIM-verified domains? Action policy: `none` / `quarantine` / `reject`.
- **DMARC enforcement (`p=reject`)** is the single most effective anti-spoofing control.
- Reporting: aggregate (`rua=`) + forensic (`ruf=`) reports tell you who's spoofing your domain.

## 12. SNMP

- v1 / v2c: community string is plaintext; "public" / "private" are common defaults — easy wins on internal pentests.
- v3: per-user auth + encryption — required.
- Information disclosure: SNMP walks routinely leak interfaces, MAC tables, ARP, software versions.
- Tools: `snmpwalk`, `onesixtyone`, `snmp-check`.

## 13. WebSocket / gRPC

- WebSocket inherits the page's CSP and CORS — don't trust CSRF protection of HTTP forms to apply.
- **CSWSH** (Cross-Site WebSocket Hijacking): no Origin enforcement → attacker page can open auth'd WebSocket.
- gRPC over HTTP/2; tooling-wise, treat the Protobuf endpoint like any other API for auth/authz testing. `grpcurl` is your friend.

## 14. OAuth / OIDC / SAML / JWT

- **OAuth 2.0**: authorization framework. Common pitfalls: open redirect on `redirect_uri`, missing `state` (CSRF), accepting `response_type=token` (implicit flow — deprecated, prefer Authorization Code with PKCE).
- **OIDC**: authentication layer on top of OAuth. ID token (JWT) signed by issuer.
- **SAML**: XML-based SSO. Vulnerable to XML signature wrapping if poorly implemented; always validate signed assertions strictly.
- **JWT**:
  - `alg=none` accepted → forge tokens.
  - `kid` header SQLi or path traversal → load attacker key.
  - `jwk` header attacker-supplied → forge tokens.
  - Weak HMAC secret → brute-force.
  - Confused-deputy: HS256 vs RS256 algorithm confusion.
- **Best practice**: short-lived access tokens, refresh-token rotation, PKCE on public clients, store `state` and `nonce` server-side.

---

## Cross-protocol observations

- **Auth protocol downgrades** are a recurring class — TLS, SMB, Kerberos all have history. Disable legacy versions explicitly.
- **Protocol confusion**: tools that speak both HTTP and HTTPS on the same port; servers that interpret a malformed first byte as a different protocol → ALPACA, smuggling, etc.
- **Session fixation / pinning**: always rotate session IDs after authentication state changes (login, privilege escalation, MFA elevation).
