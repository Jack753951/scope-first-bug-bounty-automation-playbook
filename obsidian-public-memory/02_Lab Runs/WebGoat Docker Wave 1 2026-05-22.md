> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# WebGoat Docker Wave 1 2026-05-22

Status: completed / Docker-backed target baseline
Repo handoff: `<user-home>`
Artifacts: `<user-home>`
Bundle: `<user-home>`

## Routing

- `<lab-vm>` <lab-ip>: Docker target host
- `<lab-vm>` <lab-ip>: tester
- NAT briefly opened on victim for image/deploy check, then closed.

## Docker state

```text
webgoat-lab webgoat/webgoat:latest <lab-ip>:8080->8080, <lab-ip>:9090->9090
juice-shop-lab bkimminich/juice-shop <lab-ip>:3000->3000
```

NAT closure verified:

```text
victim: internet=closed
aggressive: internet=closed
```

## Baseline evidence

```text
/WebGoat -> 302
/WebGoat/login -> 200 title=Login Page
/WebGoat/registration -> 200 title=Login Page
/WebGoat/actuator -> 200
/WebWolf/login -> 200 title=WebWolf
nmap 8080/9090 -> Apache Tomcat
browser DOM markers captured for WebGoat and WebWolf
```

## Next

Authenticated WebGoat registration/login, then one lesson proof per run with pre/post health and bounded evidence.
