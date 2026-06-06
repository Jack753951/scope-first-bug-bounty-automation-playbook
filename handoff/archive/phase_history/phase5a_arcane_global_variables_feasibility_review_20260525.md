> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 5A Arcane <specific-ghsa-id> Feasibility Review

Status: source/install feasibility reviewed / no target touched
Date: 2026-05-25
Source: Hermes source-only review of GitHub Advisory API, `getarcaneapp/arcane` tag `v1.19.1`, patched tag `v1.19.2`, and repository install examples
Repo truth: `handoff/phase5a_arcane_global_variables_bootstrap_plan_20260523.md`, `targets/catalog/arcane_ghsa_jpjh_jm2p_39hh.md`, this file

## Reviewer identity

- Reviewer route/tool: Hermes terminal/source review
- Visible runtime model: gpt-5.5 via OpenAI-Codex provider in current Hermes session
- Provider / CLI version if visible: provider visible as `openai-codex`; exact deployment details not exposed
- Review focus: source/install feasibility, safety boundary, next-step routing
- Limitation: no Arcane instance was launched; no live target or local target was touched; GHCR tag existence was checked via registry manifests only

## Scope and boundary

This review is intentionally source-only and metadata-only.

Performed:

```text
GitHub Advisory metadata read
repository metadata/tag read
shallow source checkout of public tag v1.19.1 under /tmp/hermes_arcane_review
patched v1.19.2 source snippet comparison
GHCR manifest tag existence check
static source/install-path inspection
```

Not performed:

```text
no public/live target testing
no local Arcane target launch
no Docker daemon/socket mounting
no exploit/proof request
no account creation
no scanning
no callback/OAST/tunnel
no report submission
```

## Advisory and version facts checked

GitHub Advisory API for `<specific-ghsa-id>` reports:

```text
summary: Arcane: Missing admin authorization on global variables endpoint
severity: high
published_at: 2026-05-23T00:16:56Z
package: github.com/getarcaneapp/arcane/backend
vulnerable range: <= 1.19.1
first patched version: 1.19.2
```

Repository metadata checked:

```text
repository: getarcaneapp/arcane
default branch: main
license: BSD-3-Clause
tag v1.19.1 commit: 02829b270b7975df32c8d5f787db7345dc6c27ac
tag v1.19.2 commit: dd81632ae3c8dd455aad898802f0179970e53ede
```

GHCR manifest check:

```text
ghcr.io/getarcaneapp/arcane:v1.19.1 exists, digest sha256:8f03cb1b7a877aa90d398ca07ad47a01732e73e3aefc731bc004b7187485883a
ghcr.io/getarcaneapp/arcane:v1.19.2 exists, digest sha256:247fc5b3e79e04262d128a3468cac62837cd1e0aefe472e044691f9ba049070a
plain tags 1.19.1 and 1.19.2 returned 404; use v-prefixed tags
```

Interpretation: vulnerable and patched container tags appear pin-able by version with `v` prefix. This supports a later disposable local bootstrap, but does not by itself prove runtime behavior.

## Vulnerable endpoint/source finding

At tag `v1.19.1`, the endpoint is registered in `backend/api/handlers/templates.go`:

```text
OperationID: updateGlobalVariables
Method: PUT
Path: /environments/{id}/templates/variables
Security: BearerAuth or ApiKeyAuth
Handler: h.UpdateGlobalVariables
```

The handler at `backend/api/handlers/templates.go:884-905` checks that `templateService` exists, proxies remote environments when `EnvironmentID != "0"`, and then calls:

```text
h.templateService.UpdateGlobalVariables(ctx, input.Body.Variables)
```

No `checkAdminInternal(ctx)` appears before the write in `v1.19.1`.

The admin helper exists at `backend/api/handlers/helpers.go:15-20`:

```text
checkAdminInternal(ctx) -> 403 "admin access required" if IsAdminFromContext(ctx) is false
```

The auth middleware exposes role status through `IsAdminFromContext(ctx)`, but role enforcement is handler-level.

Patched comparison:

```text
v1.19.2 UpdateGlobalVariables adds:
if err := checkAdminInternal(ctx); err != nil {
    return nil, err
}
```

Interpretation: the source diff strongly supports the advisory's stated vulnerability shape. A later local proof can focus on role boundary/config-write marker, not RCE.

## Write target and impact boundary

`backend/internal/services/template_service.go:1107-1148` writes supplied variables into the global variables file path returned by `getGlobalVariablesPath(ctx)`. The generated file content is headed:

```text
# Global Environment Variables
# These variables are available to all projects
```

The safe local proof primitive remains:

```text
authenticated non-admin writes one lab-owned marker variable through PUT /api/environments/0/templates/variables
```

Do not prove or claim command execution by default. The next proof, if authorized later, should stop at authorization-boundary + global configuration marker write/readback unless the operator separately authorizes a stronger disposable-lab deployment proof.

## Install/bootstrap feasibility

Arcane provides Docker examples and environment docs:

```text
.env.example PORT=3552
.env.example DATABASE_URL defaults to SQLite under data/arcane.db
.env.example DOCKER_HOST default: unix:///var/run/docker.sock
.env.example DOCKER_HOST proxy example: tcp://docker-socket-proxy:2375
docker/examples/compose.basic.yaml exposes 3552 and mounts /var/run/docker.sock
docker/examples/compose.proxy.yaml runs tecnativa/docker-socket-proxy and sets DOCKER_HOST=tcp://docker-socket-proxy:2375
```

Default admin bootstrap exists in source:

```text
username: arcane
password: arcane-admin
role: admin
RequiresPasswordChange: true
```

The user-management API can create a throwaway member/non-admin only after admin auth:

```text
POST /api/users
handler calls checkAdminInternal(ctx)
default role if none supplied: user
```

Login endpoint exists:

```text
POST /api/auth/login
```

Feasibility judgment:

```text
feasible-but-high-risk-docker-posture
```

Why feasible:

- versioned vulnerable and patched images appear available with v-prefixed tags;
- SQLite default reduces database setup complexity;
- default admin bootstrap exists for first login in empty DB;
- admin-only user creation path exists for creating a throwaway non-admin;
- target endpoint, login path, and role-check contrast are identifiable from source;
- Docker socket proxy path exists and can be adapted for a disposable daemon/proxy.

Why high risk:

- Arcane is a Docker management UI;
- official basic compose mounts `/var/run/docker.sock` directly;
- even the proxy example usually fronts a Docker daemon and includes POST plus container/image/network permissions;
- using any host/user Docker socket would violate the lab boundary.

## Required safe architecture for next slice

A later bootstrap script must use only a disposable Docker surface, for example:

```text
<victim-vm> host-only network
  arcane:v1.19.1 container
  isolated docker-socket-proxy or Docker-in-Docker endpoint
  disposable docker daemon/state only
  dedicated arcane-data volume
  no host/user Docker socket
  no real projects/secrets
```

The compose must not contain this unsafe bind:

```text
/var/run/docker.sock:/var/run/docker.sock
```

Unless `/var/run/docker.sock` belongs to a disposable nested daemon created only for this lab, not the VM/host's real Docker daemon. If that distinction is ambiguous, stop.

## Minimum next proof plan, if operator approves local bootstrap later

Target classification:

```text
verified_role_separation_config_write_lab_only
```

Minimum HTTP evidence:

```text
pre-health GET /api/health -> 200
admin login with default bootstrap admin or reset throwaway admin -> token/session works
admin creates throwaway member user via POST /api/users -> 200/expected success
member login -> token/session works
GET /api/auth/me for member -> role user/non-admin observed
unauth PUT /api/environments/0/templates/variables -> 401/403
admin baseline PUT marker variable -> 200 or documented admin success
member PUT marker variable -> 200 unexpected vulnerable positive on v1.19.1
GET /api/environments/0/templates/variables -> marker visible with minimal response excerpt
member separate admin-only control, such as POST /api/users or another admin handler -> 403
post-health GET /api/health -> 200
cleanup removes Arcane container, disposable daemon/proxy, data volume, and test network
```

Safe marker shape:

```text
HERMES_ARCANE_ROLE_SEPARATION_MARKER_<UTC timestamp>
```

Only write marker variables such as:

```text
HERMES_ARCANE_MARKER=HERMES_ARCANE_ROLE_SEPARATION_MARKER_<timestamp>
```

Do not write registry/image/database/secret variables in the first proof.

## Stop conditions

Stop before running anything if:

```text
only the host/user Docker socket is available
v1.19.1 image cannot be pinned by digest or tag
container cannot be kept host-only/local-only
disposable Docker daemon/proxy posture is unclear
admin/member setup requires real accounts or real project data
proof requires real secrets, real compose projects, deployment, RCE, callback, or external network
```

Stop during bootstrap/proof if:

```text
Arcane attempts to manage non-disposable host containers/images/volumes
unexpected sensitive data appears in responses/logs
request leaves host-only lab unexpectedly
cleanup fails
vulnerable endpoint behavior diverges and would require guessing or stronger payloads
```

## Recommendation

Proceed next with a bootstrap-script draft only if the script is written as fail-closed and precheck-first:

```text
scripts/labs/arcane_global_variables_authz_wave1.sh
```

Required script modes:

```text
--precheck-only: verify route, image tag/digest, no host socket bind, planned disposable daemon/proxy, no trigger
--setup-only: launch disposable target and create users, no vulnerable member PUT yet
--run-proof: require explicit local-lab confirmation before the member marker write
--cleanup-only: remove target/proxy/volumes/network
```

Do not run the bootstrap/proof until the disposable Docker daemon/socket posture is confirmed. Since the operator said a legal scope package will be provided next session, keep live-target work blocked until that package exists; this Arcane lane remains local-bootstrap only unless separately scoped.
