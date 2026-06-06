> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Defensive Architecture & Hardening Reference

Read when the user asks about firewalls, WAFs, IDS/IPS, fail2ban, IPsec/IKEv2, network segmentation, or detection rules.

## Table of contents
1. Network firewalls (nftables / iptables / pf)
2. Web Application Firewalls (SafeLine, ModSecurity, managed WAFs)
3. Intrusion Prevention / Detection (Fail2Ban, CrowdSec, Suricata, Snort, Zeek)
4. Encrypted tunnels (WireGuard, IPsec/IKEv2, Cisco IPsec)
5. Endpoint hardening checklists (Linux, Windows, Web)
6. Detection-as-code (Sigma, YARA, MITRE D3FEND)
7. Defence-in-depth blueprint (small business example)

---

## 1. Network firewalls

### Linux: nftables (modern) and iptables (legacy)

```bash
# Minimal hardened nftables ruleset for a public-facing host
sudo tee /etc/nftables.conf <<'EOF'
flush ruleset
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    ct state established,related accept
    iif "lo" accept
    ct state invalid drop
    ip protocol icmp icmp type { echo-request, destination-unreachable, time-exceeded } accept
    tcp dport 22 accept   # SSH
    tcp dport { 80, 443 } accept
  }
  chain forward { type filter hook forward priority 0; policy drop; }
  chain output  { type filter hook output  priority 0; policy accept; }
}
EOF
sudo systemctl enable --now nftables
```

**Hardening principles**: default-drop, allow only necessary ports, log dropped packets sparingly (use rate limit), separate management plane onto a non-default SSH port behind a bastion or VPN.

### pf (BSD / macOS)
Used on OpenBSD, pfSense, OPNsense — same default-drop philosophy.

---

## 2. Web Application Firewalls (WAF)

### SafeLine (open-source, self-hosted, modern UI)
```bash
bash -c "$(curl -fsSLk https://waf.chaitin.com/release/latest/setup.sh)"
# Then visit https://<host>:9443
```
Strengths: easy install, semantic detection, good dashboard, bot protection. Place in <program-name> of the application and route 80/443 through it.

### ModSecurity + Nginx + OWASP CRS (battle-tested)
```bash
sudo apt install libmodsecurity3 modsecurity-crs nginx-module-modsecurity
# In nginx.conf:  load_module modules/ngx_http_modsecurity_module.so;
# In server block: modsecurity on; modsecurity_rules_file /etc/nginx/modsec/main.conf;
```
Strengths: proven, rule library covers OWASP Top 10. Weakness: high false positive rate without tuning — start in `DetectionOnly`, tune for 2 weeks, then enforce.

### Cloudflare / AWS WAF (managed)
Use when you don't run the edge. Configure custom rules for application-specific routes; rely on managed rule sets for OWASP Top 10.

**Rule of thumb**: WAF is a compensating control. Patch the underlying SQL injection in the app; don't rely on the WAF as the only line of defence.

---

## 3. Intrusion Prevention / Detection

### Fail2Ban — auth log monitoring + dynamic ban
```bash
sudo apt install fail2ban
sudo tee /etc/fail2ban/jail.local <<'EOF'
[DEFAULT]
bantime  = 1h
findtime = 10m
maxretry = 5
backend  = systemd

[sshd]
enabled  = true

[nginx-http-auth]
enabled = true
filter  = nginx-http-auth
logpath = /var/log/nginx/error.log
EOF
sudo systemctl restart fail2ban
sudo fail2ban-client status sshd
```

### CrowdSec — community-driven, behaviour-based
Modern alternative to fail2ban with a shared block-list. Decouples detection (parsers + scenarios) from remediation (bouncers).

### Suricata — IDS/IPS, DPI
```bash
sudo apt install suricata suricata-update
sudo suricata-update              # pull ET Open ruleset
sudo suricata -c /etc/suricata/suricata.yaml -i eth0
# Inline (IPS) mode requires nfqueue: -q 0
```

### Snort 3 — alternative to Suricata
Same role; pick one and stick with it. Suricata is more parallelism-friendly.

### Zeek (formerly Bro) — protocol-aware analyzer
Not a blocker; produces structured logs (conn.log, http.log, dns.log) ideal for SIEM ingestion and threat hunting.

---

## 4. Encrypted tunnels

### WireGuard (modern, recommended)
```bash
# Server
wg genkey | tee server.key | wg pubkey > server.pub
ip link add wg0 type wireguard
ip addr add 10.10.0.1/24 dev wg0
wg set wg0 listen-port 51820 private-key /etc/wg/server.key
ip link set wg0 up

# /etc/wireguard/wg0.conf — server side
[Interface]
Address    = 10.10.0.1/24
ListenPort = 51820
PrivateKey = <server-key>

[Peer]
PublicKey  = <peer-pub>
AllowedIPs = 10.10.0.2/32
```

### IPsec / IKEv2 (strongSwan)
Use IKEv2 + AES-GCM-256 + SHA384 + ECP384. Avoid L2TP/IPsec (legacy, weaker key exchange) and PPTP (broken).

```conf
# /etc/swanctl/conf.d/site.conf  (strongSwan vici)
connections {
  site-to-site {
    version = 2
    proposals = aes256gcm16-prfsha384-ecp384
    local_addrs  = 203.0.113.5
    remote_addrs = 198.51.100.7
    children {
      net {
        local_ts  = 10.0.1.0/24
        remote_ts = 10.0.2.0/24
        esp_proposals = aes256gcm16-ecp384
      }
    }
  }
}
```

### Cisco IPsec (legacy enterprise)
Configure on ASA / Cisco IOS via crypto map; on client side use built-in OS dialler. Acceptable when interop with old gear is required, but prefer IKEv2 over the older "Cisco IPsec / XAUTH" mode.

**Verdict**: WireGuard for new builds, IKEv2 strongSwan for site-to-site enterprise, OpenVPN only when the platform forces it.

---

## 5. Endpoint hardening checklists

### Linux server baseline
- Disable root SSH login, password SSH; use ed25519 keys.
- `unattended-upgrades` for automatic security patches.
- `auditd` rules from neo23x0/auditd: monitor execve, sudo, password files.
- `apparmor` or `selinux` enforcing.
- Sysctl: `net.ipv4.tcp_syncookies=1`, `kernel.kptr_restrict=2`, `kernel.dmesg_restrict=1`.
- Time sync via `chrony` or `systemd-timesyncd`.

### Windows server baseline
- LAPS for local admin password rotation.
- Sysmon with neo23x0/sysmon-config.
- `AppLocker` or `WDAC` execution control.
- Defender ASR rules enabled.
- Disable SMBv1; enforce SMB signing.
- Disable LLMNR + NBT-NS at the policy level (kills Responder attacks).

### Web app (regardless of stack)
- HSTS preload, CSP with nonces, `SameSite=Lax` minimum on cookies, `HttpOnly` + `Secure`.
- Security.txt at `/.well-known/security.txt`.
- Rate limit auth endpoints; add CAPTCHA after N failures.
- Output encoding by default; allow-list HTML only where needed (DOMPurify).

---

## 6. Detection-as-code

### Sigma rules — generic detection format, compiles to your SIEM

```yaml
title: Suspicious PowerShell Encoded Command
id: 5fbd39c8-3a89-46e4-9e5f-1c87b4fb8b9f
status: stable
description: Detects encoded PowerShell launches often used by malware
logsource: { product: windows, category: process_creation }
detection:
  selection:
    Image|endswith: '\powershell.exe'
    CommandLine|contains: '-EncodedCommand'
  condition: selection
level: high
```

Tooling: `sigma` CLI converts to Splunk SPL, Elastic EQL, Kusto, etc.

### YARA rules — pattern matching for files / memory

```yara
rule SuspiciousReverseShellPython {
  strings:
    $a = "import socket"
    $b = "subprocess.call"
    $c = /connect\(\(["'][\d.]+["']\s*,/
  condition:
    all of them
}
```

Tooling: `yara` CLI, `yara-python`, integration with Volatility (`yarascan` plugin).

### MITRE D3FEND — defensive counterpart to ATT&CK
Maps each ATT&CK technique to defensive countermeasures. Useful when you have a finding mapped to T1059.001 and need to articulate the defence.

---

## 7. Defence-in-depth blueprint (small business, single VM)

```
Internet
   │
   ├─ Cloudflare DNS + WAF (managed rules)
   │
   ▼
[Edge nginx + SafeLine (or ModSecurity)]   port 443 → ┐
   │                                                   │
   ├─ HSTS, CSP, rate-limit, sane TLS                  │
   │                                                   │
   ▼                                                   │
Application (in container)                             │
   │                                                   │
   ├─ Read-only FS where possible                      │
   ├─ Drop capabilities, no-new-privileges             │
   │                                                   │
   ▼                                                   │
Backend services on private subnet ◄───────────────────┘
   │
   ├─ Database with TLS, separate user per service
   ├─ Backups encrypted, off-host, tested monthly
   ▼
Logging → systemd-journal + Sysmon/auditd → Loki / Splunk
   │
   └─ Sigma rules → alert to Slack / PagerDuty
```

Layered controls so that defeating any one doesn't compromise the system.
