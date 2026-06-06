> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Firewall Baseline

Use this as a starting checklist for defensive firewall design. Adapt it to the host, network, and business purpose.

## Principles

- Default deny inbound.
- Allow only required services.
- Restrict admin access to trusted IPs or VPN.
- Log denied traffic at a useful rate.
- Separate public, internal, management, and lab networks.
- Review egress rules for servers that should not initiate arbitrary outbound traffic.

## Host Firewall Checklist

- Inventory listening services.
- Confirm each exposed port has an owner and purpose.
- Restrict SSH / RDP / WinRM to management networks.
- Rate-limit or protect authentication endpoints.
- Block unused IPv6 exposure if IPv6 is not intentionally configured.
- Keep emergency access documented but controlled.

## Web Server Baseline

- Public: 80 / 443 only unless a service explicitly needs more.
- Redirect HTTP to HTTPS.
- Keep admin panels behind VPN, SSO, IP allowlist, or private network.
- Separate staging and production.
- Keep upload paths from executing code.

## Review Questions

- What breaks if this port is closed?
- Who owns this service?
- Is the service patched and monitored?
- Can access be limited by source?
- Is outbound access needed?
- What log proves the rule is working?
