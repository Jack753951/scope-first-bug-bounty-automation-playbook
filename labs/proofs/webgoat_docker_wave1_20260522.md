> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat Docker Wave 1

Status: completed / Docker-backed local target deployed and baseline-tested
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> VirtualBox -> victim Docker host `<victim-vm>` -> testing from `<attacker-vm>`

## Target and routing

Docker host:

```text
<victim-vm> <lab-ip>
Docker version 28.5.2+dfsg4
Docker Compose version 2.40.3-3
```

Tester:

```text
<attacker-vm> <lab-ip>
```

Deployed containers:

```text
juice-shop-lab bkimminich/juice-shop <lab-ip>:3000->3000/tcp
webgoat-lab webgoat/webgoat:latest <lab-ip>:8080->8080/tcp, <lab-ip>:9090->9090/tcp
```

## NAT policy

NAT was opened briefly on `<victim-vm>` to confirm/pull/use Docker images. Existing image `webgoat/webgoat:latest` was already present, so no long pull was required.

NAT was closed after deployment:

```text
<victim-vm> nic2=null cableconnected2=off
<victim-vm> route: 172.17.0.0/16 docker0 + <lab-ip>/24 eth0 only
<victim-vm> internet=closed
<attacker-vm> internet=closed
```

## Runner and artifacts

Runner:

`<private-workspace>/scripts/labs/webgoat_docker_wave1.sh`

Artifacts:

`<private-workspace>/<artifact-output-dir>/webgoat_docker_wave1_20260522T031708Z/`

## Results

HTTP reachability:

```text
WebGoat /WebGoat -> 302
WebGoat /WebGoat/login -> 200 title="Login Page"
WebGoat /WebGoat/registration -> 200 title="Login Page"
WebGoat /WebGoat/actuator -> 200
WebGoat /WebGoat/swagger-ui.html -> 302
WebWolf /WebWolf -> 302
WebWolf /WebWolf/login -> 200 title="WebWolf"
```

Nmap bounded service fingerprint on known ports only:

```text
8080/tcp open http Apache Tomcat
9090/tcp open http Apache Tomcat
```

Browser DOM proof from Kali Chromium:

```text
WebGoat markers: Login,WebGoat
WebWolf markers: WebWolf
```

## Classification

This is a target-readiness / valuable baseline bundle, not yet a vulnerability proof. It confirms a recoverable Docker-backed OWASP training target is reachable from the attacker VM after NAT is closed.

## Next safe slices

- WebGoat registration/login with throwaway lab user.
- Enumerate lesson endpoints after authenticated session.
- Run one bounded WebGoat lesson proof at a time, saving request/response/evidence and post-health.
- Keep WebGoat on victim-lab; run all probes from aggressive-lab.
