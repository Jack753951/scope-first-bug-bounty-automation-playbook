> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# webgoat_docker_target_baseline

Status: valuable-candidate / target-readiness / Docker-backed local lab
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> victim Docker host `<victim-vm>` -> testing from `<attacker-vm>`
Artifacts: `<artifact-output-dir>/webgoat_docker_wave1_20260522T031708Z/`
Runner: `scripts/labs/webgoat_docker_wave1.sh`

## Target

```text
Host: <lab-ip>
WebGoat: http://<lab-ip>:8080/WebGoat
WebWolf: http://<lab-ip>:9090/WebWolf
Container: webgoat-lab webgoat/webgoat:latest
```

## Evidence

HTTP:

```text
/WebGoat -> 302
/WebGoat/login -> 200 title=Login Page
/WebGoat/registration -> 200 title=Login Page
/WebGoat/actuator -> 200
/WebWolf -> 302
/WebWolf/login -> 200 title=WebWolf
```

Nmap, known ports only:

```text
8080/tcp open http Apache Tomcat
9090/tcp open http Apache Tomcat
```

Browser proof:

```text
WebGoat DOM markers: Login,WebGoat
WebWolf DOM markers: WebWolf
```

## Classification

Valuable target-readiness baseline. This is not a vulnerability proof by itself. It proves Docker-backed WebGoat/WebWolf is available on the isolated host-only lab network after NAT closure.

## Safety boundaries

- Local authorized lab only.
- NAT closed after deployment.
- Bounded nmap only on known ports 8080/9090.
- No credential attacks.
- No destructive lessons executed.
- No public targets.

## Next steps

Convert this baseline into one verified WebGoat lesson proof at a time, starting with registration/login and a single lesson with explicit pre/post health checks.
