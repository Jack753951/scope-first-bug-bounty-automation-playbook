> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Phase 1 Proposal — Program Scope Intake & Validation

Author:   Cowork (Claude, strategy/spec pass)
Date:     2026-05-15
Status:   Proposal / Spec only — no code changes in this document
Inputs:   `.hermes.md`, `HERMES_WORKFLOW.md`, `handoff/sustained_review_loop.md`,
          `handoff/cowork_phase0_1_review.md`, `handoff/codex_review.md`,
          `recon.sh`, `config/scope.txt`, `config/recon.conf`
Authority: Phase 0 + Phase 0.1 closed (`cowork_phase0_1_review.md` verdict ACCEPT)

---

## 1. Executive Summary

Phase 0 established a default-deny `safe_target` runtime guard on `recon.sh` that
validates every host/URL against operator-controlled `config/scope.txt` before
any probe, scan, or notification stage consumes it. Phase 0.1 closed validation
evidence gaps. Phase 1 layers **program-specific** authorization on top of the
global whitelist so the same script can support bug bounty / client engagements
where each program publishes its own narrower asset list and rules-of-engagement
(allowed techniques, rate caps, testing windows, automation permission).

This proposal defines:

- A `programs/<program-slug>/scope.json` schema with required and optional fields.
- A precedence model: a target/technique is only permitted if **both** the global
  scope file **and** the active program scope/rules allow it. Either source can
  veto. Out-of-scope entries within a program always win over in-scope entries.
- A new `--program <slug>` CLI flag plus `RECON_ACTIVE_PROGRAM` env knob. When
  absent, `recon.sh` behaves exactly as Phase 0 (backward compatible). When
  present, program-scope validation runs before any safe-target check passes.
- A technique gate keyed by stage tags (`subdomain_enumeration`, `port_scan`,
  `directory_bruteforce`, `vulnerability_scan_active`, …) so that even an in-scope
  host is denied if the program forbids the stage's technique.
- A rate/window enforcement layer that **tightens** (never loosens) the config
  defaults from `config/recon.conf` and refuses execution outside declared
  testing windows.
- Audit event vocabulary extensions (`PROGRAM_LOAD_OK`, `PROGRAM_LOAD_FAIL`,
  `PROGRAM_TECHNIQUE_DENIED`, `PROGRAM_OUT_OF_SCOPE`, `PROGRAM_WINDOW_DENIED`,
  `PROGRAM_AUTOMATION_DENIED`).
- A safe dry-run test matrix Codex must pass before Phase 1 acceptance.

Design principles (binding):

- **Extensible architecture.** Phase 1 should lay foundations for future modular vulnerability checks/plugins, not hard-code every future check into `recon.sh`. Program rules, technique tags, target types, rate/window gates, and audit events should be reusable by later module manifests and finding schemas. See `handoff/extensible_architecture_direction.md`.
- **Default deny.** Missing, unreadable, malformed, expired, or
  `automation_permitted: false` program scope causes refusal — never silent
  fallback to "global only."
- **Intersection, not union.** Program scope can only narrow the global scope.
  It cannot authorize anything `config/scope.txt` does not already allow.
- **Operator-controlled.** `config/scope.txt` remains operator-only. Program
  files are operator-curated artifacts checked into the repo; they are *data*,
  never executable.
- **Phase 0 invariants preserved.** `safe_target` stays the single authoritative
  gate; this proposal extends it, never replaces it.
- **Triage-only output.** Phase 1 does not introduce any new scanner feature,
  payload class, or finding-elevation rule.

---

## 2. Proposed Schema — `programs/<program-slug>/scope.json`

### 2.1 Layout on disk

```
programs/
├── _schema/
│   └── scope.schema.json        # JSON Schema (draft 2020-12) for validation
├── _examples/
│   ├── public-bounty.example.json
│   ├── client-engagement.example.json
│   └── ctf-platform.example.json
├── acme-corp/
│   ├── scope.json               # program scope + rules
│   ├── README.md                # human notes, program URL, retest contact
│   └── authorization.txt        # immutable copy of program rules / signed
│                                  client letter (operator places here)
└── widgetco/
    └── scope.json
```

Codex will create `programs/_schema/scope.schema.json` and the
`programs/_examples/` directory only. Per-program directories are
**operator-created**; Codex never auto-creates a program slug from CLI input.

### 2.2 Required top-level fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `schema_version` | string (semver) | yes | exact match required for current parser; mismatch = default-deny |
| `program` | object | yes | metadata block (§2.3) |
| `scope` | object | yes | asset rules (§2.4) |
| `techniques` | object | yes | technique rules (§2.5) |
| `rate_limits` | object | yes | concurrency/RPS caps (§2.6) |
| `testing_windows` | object | yes | when automation may run (§2.7); use `{ "always": true }` only for lab/CTF |
| `expiration` | object | yes | `valid_from` / `valid_until` ISO-8601 UTC |

Absence of any required field at parse time = `PROGRAM_LOAD_FAIL` with reason,
non-zero exit, no scan stages executed.

### 2.3 `program` block

```json
{
  "slug": "acme-corp",
  "name": "Acme Corporation Public Bounty",
  "platform": "<bug-bounty-platform>",
  "url": "https://<bug-bounty-platform>.com/acme",
  "authorization_reference": "Public bounty accepted by operator 2026-05-15; rules archived in authorization.txt",
  "policy_version": "2026-05-01",
  "policy_acknowledged_at": "2026-05-15T10:00:00Z",
  "operator_contact": "researcher@example",
  "program_contact": "security@acme.example"
}
```

- `slug` MUST match the directory name and the `--program` flag value exactly,
  ASCII `[a-z0-9-]+`, ≤64 chars. Mismatch = default-deny.
- `authorization_reference` is free text but required and surfaced in audit
  rows so reviewers can trace why automation ran. A pointer to
  `programs/<slug>/authorization.txt` is the recommended pattern.
- `policy_acknowledged_at` must be ≤ `expiration.valid_until` and not in the
  future. Drift > 24h is a warning, not an error.

### 2.4 `scope` block

```json
{
  "in_scope": [
    { "type": "domain",     "value": "acme.example.com",            "include_apex": true,  "notes": "primary site" },
    { "type": "wildcard",   "value": "*.acme.example.com",          "include_apex": false, "notes": "subdomains only" },
    { "type": "cidr",       "value": "203.0.113.0/24",              "notes": "owned netblock" },
    { "type": "ip",         "value": "198.51.100.42",               "notes": "edge host" },
    { "type": "url_prefix", "value": "https://acme.example.com/api/", "notes": "API surface only" }
  ],
  "out_of_scope": [
    { "type": "domain",     "value": "internal.acme.example.com",         "reason": "explicitly excluded by program rules" },
    { "type": "wildcard",   "value": "*.staging.acme.example.com",        "reason": "staging environment" },
    { "type": "url_prefix", "value": "https://acme.example.com/admin/",   "reason": "admin panel out of scope" }
  ],
  "idn_handling": "punycode_only"
}
```

Entry types (`type` enum is closed; unknown type = default-deny):

| `type` | `value` shape | Match semantics |
|---|---|---|
| `domain` | exact ASCII FQDN; `valid_domain` regex from `recon.sh:296` | exact-equal host match. `include_apex` is implicit `true` for this type and may be omitted; it is a no-op (host literally equals value). |
| `wildcard` | `*.<ASCII FQDN>` | `host == base` (apex) only if `include_apex: true` (default `true` for backward compatibility with `config/scope.txt:8`'s existing rule); otherwise only `host == *.<base>` matches. |
| `cidr` | IPv4 CIDR; `valid_cidr` from `recon.sh:283` | numeric containment via `ip_in_cidr`. |
| `ip` | IPv4 dotted-quad | exact-equal IP match. |
| `url_prefix` | `https?://<host>[:port]/<path-prefix>` | host must independently match an in-scope entry; path must start with `<path-prefix>`. Bare hosts probed at `/` do **not** auto-pass URL-prefix gates — see §3.4. |

`idn_handling` (enum):

- `"punycode_only"` (default, recommended) — values must be ASCII/punycode.
  Raw Unicode inputs at scan time are rejected exactly like Phase 0 does today.
- `"reject_idn"` — explicit, identical effect to `punycode_only` for Phase 1.
- `"allow_idn"` — **NOT IMPLEMENTED** in Phase 1; presence = default-deny with
  reason `idn_handling=allow_idn not supported in this release`.

### 2.5 `techniques` block

```json
{
  "allowed": [
    "subdomain_enumeration",
    "http_probe",
    "port_scan",
    "service_fingerprint",
    "vulnerability_scan_passive"
  ],
  "forbidden": [
    "directory_bruteforce",
    "vulnerability_scan_active",
    "dos",
    "intrusive_fuzz",
    "credential_brute_force",
    "social_engineering",
    "physical",
    "malware",
    "callback_payloads"
  ],
  "automation_permitted": true,
  "automation_notes": "automated triage scanning permitted within rate_limits; manual confirmation required before reporting"
}
```

Technique tag vocabulary (closed enum; any tag outside this list = default-deny):

| Tag | Maps to `recon.sh` function(s) | Stage gate point |
|---|---|---|
| `subdomain_enumeration` | `enum_subdomains` | start of `enum_subdomains` |
| `http_probe` | `find_live_hosts`, `web_probe` | start of each |
| `port_scan` | `port_scan` | start of `port_scan` |
| `service_fingerprint` | `service_fingerprint` | start of `service_fingerprint` |
| `directory_bruteforce` | `dir_bruteforce` | start of `dir_bruteforce` |
| `vulnerability_scan_passive` | `vuln_scan` with `INTENSITY in {quick,normal}` | start of `vuln_scan` if passive-only intensity selected |
| `vulnerability_scan_active`  | `vuln_scan` with `INTENSITY in {aggressive,full}` | start of `vuln_scan` if active intensity selected |
| `dos` | — | always forbidden in Phase 1; presence in `allowed` = default-deny |
| `intrusive_fuzz` | nuclei tags `dos,intrusive,fuzz` | refuse `--full` intensity if not allowed |
| `credential_brute_force` | — | always forbidden in Phase 1 |
| `social_engineering` | — | always forbidden in Phase 1 |
| `physical` | — | always forbidden in Phase 1 |
| `malware` | — | always forbidden in Phase 1 |
| `callback_payloads` | — | always forbidden in Phase 1 |

Hard rules (cannot be overridden by program file):

- A technique that appears in **both** `allowed` and `forbidden` = default-deny
  with reason `technique listed as both allowed and forbidden`.
- Phase 1 forbidden categories (`dos`, `credential_brute_force`,
  `social_engineering`, `physical`, `malware`, `callback_payloads`) MUST NOT
  appear in `allowed`. If they do, refuse to load the file.
- `automation_permitted: false` causes refusal of all non-dry-run runs. A
  `--dry-run` invocation is still permitted because no network egress occurs.
- An empty `allowed` list = default-deny (no techniques permitted = nothing to do).

### 2.6 `rate_limits` block

```json
{
  "max_concurrency": 5,
  "max_requests_per_second": 10,
  "request_delay_ms": 100,
  "nuclei_rate_limit": 50,
  "nuclei_concurrency": 10,
  "naabu_rate": 500,
  "httpx_threads": 20,
  "subfinder_threads": 10
}
```

All fields optional; each present field **caps** the corresponding value from
`config/recon.conf` (program may tighten, never loosen). When both program and
config define a value, the **minimum** wins.

`max_requests_per_second` and `request_delay_ms` are advisory metadata for
Phase 1 (no third-party tool consumes a unified RPS knob); they are surfaced
in `summary.md` and audit rows so operators can verify external-tool flags
match the declared cap. Phase 2 may add an outbound rate proxy.

### 2.7 `testing_windows` block

```json
{
  "timezone": "UTC",
  "always": false,
  "allowed": [
    { "days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "start": "00:00", "end": "23:59" }
  ],
  "blackouts": [
    { "from": "2026-12-23T00:00:00Z", "to": "2026-12-27T00:00:00Z", "reason": "vendor holiday freeze" }
  ]
}
```

- `always: true` skips window checks; permitted only when `program.platform` is
  one of `lab`, `ctf`, or `self-hosted`. For `<bug-bounty-platform>`, `bugcrowd`,
  `intigriti`, `client`, or any other platform value, `always: true` =
  default-deny.
- `timezone` is required when `always` is `false`; IANA name (`UTC`,
  `America/Los_Angeles`, `Asia/Taipei`, …). Operator-curated; `recon.sh` uses
  `date -u` and string compare in UTC, converting via `TZ=` for window
  evaluation.
- If wall-clock at start time falls in a `blackouts` window, refuse with
  `PROGRAM_WINDOW_DENIED`. Audit row records the matched blackout reason.

### 2.8 `expiration` block

```json
{
  "valid_from": "2026-05-15T00:00:00Z",
  "valid_until": "2026-11-15T00:00:00Z"
}
```

- Both required, ISO-8601 UTC.
- `valid_from > now` = default-deny with reason `program scope not yet active`.
- `valid_until < now` = default-deny with reason `program scope expired`.
- `valid_until - valid_from > 365 days` = warning logged but allowed (long
  engagement windows are common; flag for operator awareness).

### 2.9 Worked example — minimal lab program

```json
{
  "schema_version": "1.0",
  "program": {
    "slug": "home-lab",
    "name": "Local Lab",
    "platform": "lab",
    "url": "file:///home/operator/lab",
    "authorization_reference": "operator-owned local lab; see authorization.txt",
    "policy_version": "2026-05-15",
    "policy_acknowledged_at": "2026-05-15T00:00:00Z"
  },
  "scope": {
    "in_scope": [
      { "type": "cidr", "value": "10.0.0.0/8", "notes": "lab subnet" },
      { "type": "domain", "value": "localhost" }
    ],
    "out_of_scope": [],
    "idn_handling": "punycode_only"
  },
  "techniques": {
    "allowed": [
      "subdomain_enumeration", "http_probe", "port_scan",
      "service_fingerprint", "directory_bruteforce",
      "vulnerability_scan_passive", "vulnerability_scan_active"
    ],
    "forbidden": ["dos", "credential_brute_force", "social_engineering",
                  "physical", "malware", "callback_payloads", "intrusive_fuzz"],
    "automation_permitted": true,
    "automation_notes": "full lab automation"
  },
  "rate_limits": {
    "max_concurrency": 5,
    "nuclei_rate_limit": 150,
    "naabu_rate": 1000
  },
  "testing_windows": { "always": true },
  "expiration": {
    "valid_from": "2026-05-15T00:00:00Z",
    "valid_until": "2027-05-15T00:00:00Z"
  }
}
```

---

## 3. Scope Semantics

### 3.1 Precedence model

For a candidate (host, URL, IP) `T` arriving at `safe_target` with active
program `P`:

```
permit(T, P) ⇔
    parse_target(T) succeeds                                  (Phase 0)
  ∧ T matches some entry in config/scope.txt                  (Phase 0, global)
  ∧ T matches some entry in P.scope.in_scope                  (Phase 1, program)
  ∧ T does NOT match any entry in P.scope.out_of_scope        (Phase 1, exclusion)
  ∧ now ∈ P.testing_windows.allowed ∧ now ∉ P.blackouts       (Phase 1, window)
  ∧ now ∈ [P.expiration.valid_from, P.expiration.valid_until] (Phase 1, validity)
  ∧ P.techniques.automation_permitted = true OR DRY_RUN=true  (Phase 1, automation)
```

If any clause is false → `safe_target` fails → stage refuses to consume `T` →
audit row records the **first failing reason** (not all of them — short-circuit
on first failure to avoid information leakage into out-of-scope deltas).

Apex/wildcard interaction with global scope:

- The Phase 0.1 review confirmed `config/scope.txt:8` already documents
  `*.example.com` matches both `example.com` and `*.example.com`. Phase 1
  **preserves** this for global scope (no change to `scope_match` in `recon.sh`).
- For program scope, the `wildcard` entry's `include_apex` defaults to `true`
  to match operator intuition built around the global rule; operators wanting
  subdomain-only program scope explicitly set `include_apex: false`.

### 3.2 CIDR / IP

- CIDR entries use existing `ip_in_cidr`. IPv6 remains unsupported (existing
  Phase 0 limitation; URL parser already rejects `[::1]`-style literals).
  Calling this out as a Phase 1 non-goal in §8.
- IP entries are exact-match only. A `203.0.113.42` IP entry does not satisfy
  a `203.0.113.0/24` program scope unless the CIDR is also listed; conversely,
  a host whose resolved IP falls in the CIDR is accepted on the CIDR rule.
- DNS resolution at scope-match time is **not** performed. Targets are matched
  by the literal string the user (or expansion stage) supplied. This preserves
  Phase 0 semantics and avoids opening a DNS amplification channel during
  validation.

### 3.3 URL path handling

- A `url_prefix` entry like `https://acme.example.com/api/` matches any URL
  whose normalized form (scheme, host, optional port, path) starts with that
  exact prefix. Path is compared case-sensitively after host lowercasing.
- A bare host or domain target (no URL form) does NOT auto-satisfy a
  `url_prefix` entry. Rationale: prevents `acme.example.com` (bare) from
  passing scope when only `https://acme.example.com/api/` is in scope and the
  program excludes everything else.
- Conversely, a URL target `https://acme.example.com/api/v1/foo` is accepted
  if either (a) `acme.example.com` matches an in-scope `domain` / `wildcard` /
  `ip` / `cidr` entry **and** no `out_of_scope` URL prefix matches, OR
  (b) some `url_prefix` entry is a prefix of the target.
- Query strings and fragments are stripped before prefix comparison
  (matches existing `parse_target` URL normalization at `recon.sh:357`).

### 3.4 IDN / punycode

- `valid_domain` in `recon.sh:296` is ASCII-only; Phase 0.1 evidence confirmed
  raw `bücher.example` is rejected. Phase 1 preserves this and adds an explicit
  `idn_handling` declaration on the program file so operators **state their
  intent** rather than relying on implicit behavior.
- Operators converting IDN to punycode externally (`idn2`, browser address bar,
  online tooling) record both forms in `authorization.txt` and place the
  punycode form in `scope.json`. The README under `programs/<slug>/` should
  call this out.

### 3.5 Out-of-scope precedence

- `out_of_scope` is evaluated **after** `in_scope` and **always wins**.
- An out-of-scope `wildcard` entry like `*.staging.acme.example.com` excludes
  the entire subtree even if a broader `*.acme.example.com` in-scope wildcard
  would otherwise admit it.
- An out-of-scope `url_prefix` entry excludes only URL targets matching that
  prefix; bare-host probes of the same host remain permitted if the host is
  otherwise in scope. This mirrors typical bug bounty rules ("the site is in
  scope but /admin is not").
- Audit reason when out-of-scope wins: `program out_of_scope match: <entry>
  (reason: <entry.reason>)`.

---

## 4. Technique / Rate-Limit Rules

### 4.1 Technique gate placement

The gate fires at the **start of each pipeline stage function** in `recon.sh`,
not per-target. Rationale: stages map 1:1 to techniques; per-target evaluation
would multiply audit rows without changing the deny decision.

Codex implements `program_technique_allowed <technique-tag>` returning 0/1, with
audit row on deny:

```
<ts> | user=<u> | target=<resolved-target-or-stage> | event=PROGRAM_TECHNIQUE_DENIED
   | intensity=<i> | dry_run=<bool>
   | reason=technique=<tag> not in program.allowed (program=<slug>)
```

Hook points (function entry, before any tool invocation):

| Function | Technique tag checked |
|---|---|
| `enum_subdomains` (recon.sh:530) | `subdomain_enumeration` |
| `find_live_hosts` (recon.sh:572) | `http_probe` |
| `port_scan` (recon.sh:613) | `port_scan` |
| `service_fingerprint` (recon.sh:645) | `service_fingerprint` |
| `web_probe` (recon.sh:681) | `http_probe` |
| `dir_bruteforce` (recon.sh:717) | `directory_bruteforce` |
| `vuln_scan` (recon.sh:754) | `vulnerability_scan_passive` if `INTENSITY ∈ {quick,normal}`, else `vulnerability_scan_active`; additionally `intrusive_fuzz` required when `INTENSITY=full` |

If a technique is denied, the stage:

1. Logs a single `PROGRAM_TECHNIQUE_DENIED` audit row.
2. Writes a clear note to `RUN_LOG` and to `summary.md`'s "Skipped Stages"
   section (new section, see §5.4).
3. Returns 0 (continue pipeline; later stages may still be allowed). It is
   NOT a fatal error — bug bounty programs commonly allow port scanning but
   forbid directory bruteforcing, and the pipeline should run as far as is
   authorized.

Exception: if `automation_permitted: false` and `DRY_RUN=false`, the pipeline
refuses to run **at all** with a single top-level `PROGRAM_AUTOMATION_DENIED`
event. No per-stage iteration.

### 4.2 Forbidden categories (always)

Independent of any program declaration, Phase 1 hard-codes a refusal list at
the gate. Even if a malformed program file claims `"allowed": ["dos"]`, the
loader rejects the file with `PROGRAM_LOAD_FAIL` before the gate is reached.
This is belt-and-suspenders defense in depth.

### 4.3 Rate-limit application

At load time, build the **effective config** by taking elementwise minimum of
program `rate_limits` and `config/recon.conf` defaults. Persist the effective
config to `<outdir>/effective_config.json` for audit traceability.

Example:

```
config/recon.conf:        NAABU_RATE=1000, NUCLEI_RATE_LIMIT=150, NUCLEI_CONCURRENCY=25
programs/acme/scope.json: naabu_rate=500, nuclei_rate_limit=50, nuclei_concurrency=10
effective_config.json:    NAABU_RATE=500,  NUCLEI_RATE_LIMIT=50,  NUCLEI_CONCURRENCY=10
```

CLI `--rate <n>` continues to override `NAABU_RATE` but is **also capped** by
the program's `naabu_rate`. If `--rate 2000` is passed and program caps at 500,
the effective value is 500 and a warning is logged.

### 4.4 Testing window check

Window evaluation runs once at pipeline start (after `validate_runtime_flags`,
before `safe_target` of the initial target). If `now` is outside `allowed` or
inside a `blackouts` entry → `PROGRAM_WINDOW_DENIED`, exit 1, no stages run.

Re-evaluation mid-run is **not** performed in Phase 1 (avoid races and partial
runs). Long engagements should set wide `allowed` windows.

---

## 5. `recon.sh` Integration Plan

### 5.1 New CLI surface

```
--program <slug>            Activate program scope at programs/<slug>/scope.json
                             Also accepts $RECON_ACTIVE_PROGRAM env var as default.

--list-programs             Read-only: enumerate programs/ directory and print
                             slug, name, validity status, automation flag.
                             Exits 0 without running any pipeline.

--program-file <path>       Override default programs/<slug>/scope.json path.
                             Slug must still match program.slug field inside.
```

Mutual exclusions enforced in `parse_args`:

- `--program` + `--skip-scope-check` → exit 2 with
  `--skip-scope-check is refused when a program scope is active`. Rationale:
  the operator who provided the program file is explicitly opting into stricter
  controls; bypass tokens would defeat the audit purpose.
- `--program <slug>` with `programs/<slug>/scope.json` missing → exit 1 with
  `PROGRAM_LOAD_FAIL` and reason.

Backward compatibility: when `--program` is absent and `RECON_ACTIVE_PROGRAM`
is unset, `recon.sh` behaves exactly as Phase 0.

### 5.2 Validation order in `recon.sh`

```
parse_args
validate_config             # existing
validate_runtime_flags      # existing + new --program/--skip-scope-check exclusion
load_program                # new: only if --program / $RECON_ACTIVE_PROGRAM set
  ├── resolve path (programs/<slug>/scope.json or --program-file value)
  ├── jq syntax-check the JSON
  ├── jsonschema validate against programs/_schema/scope.schema.json
  ├── semantic checks (slug match, expiration, forbidden-in-allowed, etc.)
  ├── compute effective rate limits (min with recon.conf)
  ├── window check (current time within allowed, not in blackout)
  ├── automation_permitted check (refuse if false and not --dry-run)
  ├── record sha256 of scope.json into audit log + outdir/effective_config.json
  └── on any failure: PROGRAM_LOAD_FAIL, exit 1, no scans

# Per-target / per-stage from here:
safe_target                 # existing, extended to call program_scope_match
  ├── parse_target          # unchanged
  ├── validate_scope_file (config/scope.txt)  # unchanged
  ├── scope_match against config/scope.txt    # unchanged
  └── if PROGRAM_ACTIVE:
        program_scope_match against scope.json    # NEW
        out_of_scope_match against scope.json     # NEW (wins over in_scope)

# At each pipeline stage entry:
program_technique_allowed <tag>   # NEW; on deny: PROGRAM_TECHNIQUE_DENIED, skip stage
```

`safe_target` returns success only if both global and program checks pass.
Audit row distinguishes the failure source so reviewers can tell whether
`config/scope.txt` or `programs/<slug>/scope.json` rejected.

### 5.3 Combining global + program scope

The two files are AND-combined per §3.1. Concrete sequence inside the
extended `safe_target`:

```
1. parse_target(t)            -> SAFE_TARGET_VALUE, SAFE_TARGET_HOST
2. if --skip-scope-check accepted: short-circuit OVERRIDE_DRY_RUN as today
   (note: not reachable when --program is active per §5.1 exclusion)
3. validate_scope_file(config/scope.txt) -> as today
4. scope_match(host, config/scope.txt) -> on FAIL: SAFE_TARGET_REJECTED reason="not in global scope"
5. if PROGRAM_ACTIVE:
   a. program_scope_match(host_or_url, scope.json.in_scope)
      -> on FAIL: SAFE_TARGET_REJECTED reason="not in program in_scope (program=<slug>)"
   b. program_out_of_scope_match(host_or_url, scope.json.out_of_scope)
      -> on TRUE: SAFE_TARGET_REJECTED reason="program out_of_scope match: <entry> (reason: <r>)"
6. SAFE_TARGET_OK reason="in scope (global + program=<slug>)"
```

### 5.4 Audit events

Existing events preserved:

- `SAFE_TARGET_OK`, `SAFE_TARGET_FAIL`, `SAFE_TARGET_REJECTED`,
  `SAFE_TARGET_OVERRIDE_DRY_RUN`.

New events:

| Event | When emitted | Reason field example |
|---|---|---|
| `PROGRAM_LOAD_OK` | after successful `load_program` | `program=acme-corp, sha256=<hex>, valid_until=2026-11-15T00:00:00Z, automation=true` |
| `PROGRAM_LOAD_FAIL` | parse/schema/semantic failure | `program=acme-corp, reason=schema_version mismatch (got 1.1, expected 1.0)` |
| `PROGRAM_AUTOMATION_DENIED` | `automation_permitted=false` and not dry-run | `program=acme-corp, dry_run=false` |
| `PROGRAM_WINDOW_DENIED` | now outside allowed or inside blackout | `program=acme-corp, now=2026-12-25T03:00:00Z, blackout=vendor holiday freeze` |
| `PROGRAM_TECHNIQUE_DENIED` | stage entry technique not in `allowed` | `program=acme-corp, technique=directory_bruteforce, stage=dir_bruteforce` |
| `PROGRAM_OUT_OF_SCOPE` | already covered by `SAFE_TARGET_REJECTED`; alias for searchability | `program=acme-corp, matched=*.staging.acme.example.com (reason: staging out of scope)` |

The audit log line format stays compatible with Phase 0 (`audit_log`
function at `recon.sh:249`) — only the `event=` value and `reason=` text change.

### 5.5 `summary.md` additions

Append two new sections when `PROGRAM_ACTIVE`:

```markdown
## Program Scope

- Program: acme-corp (Acme Corporation Public Bounty)
- Platform: <bug-bounty-platform>
- Authorization: Public bounty accepted by operator 2026-05-15
- Scope file sha256: 3a7f... (programs/acme-corp/scope.json)
- Valid: 2026-05-15 → 2026-11-15
- Automation permitted: true
- Effective rate limits: naabu_rate=500, nuclei_rate_limit=50, ...

## Skipped Stages

- dir_bruteforce: technique `directory_bruteforce` not in program.allowed
- vuln_scan (active): intensity `aggressive` requires `vulnerability_scan_active`, not allowed
```

This is operator-facing documentation; it makes deny decisions visible without
forcing the reviewer to grep audit logs.

---

## 6. Safe Dry-Run Test Matrix

Codex must execute the following matrix in **isolated temp lab roots** (same
pattern Phase 0.1 used, see `cowork_phase0_1_review.md` §"HACKLAB isolation
worked"). No network egress, no modification of production
`config/scope.txt` or production `logs/audit.log`. All cases use
`./recon.sh --dry-run --scope <temp-scope> --program-file <temp-program> -o <temp-out> ...`
with synthetic targets.

| # | Case | Inputs | Expected outcome | Audit row to confirm |
|---|---|---|---|---|
| 1 | Happy path: target in both global and program scope | global: `*.acme.example.com`; program in_scope: `*.acme.example.com`; target `api.acme.example.com` | exit 0; pipeline runs allowed stages | `PROGRAM_LOAD_OK`, `SAFE_TARGET_OK reason=in scope (global + program=acme)` |
| 2 | In global, not in program | global: `*.acme.example.com`; program in_scope: only `acme.example.com`; target `evil.acme.example.com` | safe_target FAIL | `SAFE_TARGET_REJECTED reason=not in program in_scope` |
| 3 | In program, not in global | global: `corp.example`; program in_scope: `acme.example.com`; target `acme.example.com` | safe_target FAIL | `SAFE_TARGET_REJECTED reason=not in global scope` |
| 4 | Out-of-scope wins over in-scope wildcard | program in_scope: `*.acme.example.com`; out_of_scope: `internal.acme.example.com`; target `internal.acme.example.com` | safe_target FAIL | `SAFE_TARGET_REJECTED reason=program out_of_scope match: internal.acme.example.com` |
| 5 | URL prefix in scope, bare host out | program in_scope: `url_prefix=https://acme.example.com/api/`; target `acme.example.com` (bare host) | safe_target FAIL | `SAFE_TARGET_REJECTED reason=not in program in_scope` |
| 6 | URL prefix in scope, matching URL passes | same as #5; target `https://acme.example.com/api/v1/foo` | safe_target PASS | `SAFE_TARGET_OK` |
| 7 | Wildcard `include_apex: false` rejects apex | program wildcard: `*.acme.example.com` with `include_apex: false`; target `acme.example.com` | safe_target FAIL | `SAFE_TARGET_REJECTED reason=not in program in_scope` |
| 8 | Wildcard `include_apex: true` (default) admits apex | same wildcard, `include_apex: true`; target `acme.example.com` | safe_target PASS | `SAFE_TARGET_OK` |
| 9 | CIDR positive match | program in_scope: `cidr=203.0.113.0/24`; target `203.0.113.42` | safe_target PASS | `SAFE_TARGET_OK` |
| 10 | CIDR negative | same CIDR; target `198.51.100.42` | safe_target FAIL | `SAFE_TARGET_REJECTED` |
| 11 | Punycode allowed | program in_scope: `xn--bcher-kva.example`; target same | safe_target PASS | `SAFE_TARGET_OK` |
| 12 | Raw Unicode rejected | program in_scope: `xn--bcher-kva.example`; target `bücher.example` | safe_target FAIL at parse_target | `SAFE_TARGET_FAIL reason=target is not a supported IP, CIDR, domain, or HTTP(S) URL` |
| 13 | `idn_handling: allow_idn` rejected at load | scope.json declares allow_idn | `PROGRAM_LOAD_FAIL`, exit 1 | `PROGRAM_LOAD_FAIL reason=idn_handling=allow_idn not supported` |
| 14 | Forbidden technique in allowed list | scope.json has `allowed: ["dos"]` | `PROGRAM_LOAD_FAIL`, exit 1 | `PROGRAM_LOAD_FAIL reason=forbidden technique dos cannot appear in allowed` |
| 15 | Technique gate skips stage cleanly | program allows `port_scan` only; full pipeline run on lab CIDR | exit 0; only port_scan executes; other stages logged as skipped | one `PROGRAM_TECHNIQUE_DENIED` per skipped stage; summary.md "Skipped Stages" section populated |
| 16 | `automation_permitted: false` + `--dry-run` | program flag false; --dry-run on | exit 0; runs in dry-run with warning | `PROGRAM_LOAD_OK`, all stages dry-run only |
| 17 | `automation_permitted: false` without `--dry-run` | program flag false; no --dry-run | exit 1 immediately | `PROGRAM_AUTOMATION_DENIED` |
| 18 | Expired program | `valid_until` in the past | exit 1 at load | `PROGRAM_LOAD_FAIL reason=program scope expired` |
| 19 | Not-yet-valid program | `valid_from` in the future | exit 1 at load | `PROGRAM_LOAD_FAIL reason=program scope not yet active` |
| 20 | Outside testing window | window Mon-Fri 09:00-17:00 UTC; sim now=Sat | exit 1 at window check | `PROGRAM_WINDOW_DENIED` |
| 21 | Blackout window | now inside a declared blackout | exit 1 at window check | `PROGRAM_WINDOW_DENIED reason=blackout=<reason>` |
| 22 | Rate limit narrowing | recon.conf NAABU_RATE=1000, program naabu_rate=500, CLI --rate 2000 | effective=500; warning logged | `PROGRAM_LOAD_OK` row records effective rates |
| 23 | Schema version mismatch | scope.json schema_version=1.1; parser supports 1.0 | exit 1 at load | `PROGRAM_LOAD_FAIL reason=schema_version mismatch` |
| 24 | Missing required field | scope.json missing `expiration` | exit 1 at load | `PROGRAM_LOAD_FAIL reason=required field missing: expiration` |
| 25 | Malformed JSON | scope.json with trailing comma | exit 1 at load | `PROGRAM_LOAD_FAIL reason=JSON parse error: <line>` |
| 26 | Slug mismatch | dir `acme-corp`, file says `slug: "widgetco"` | exit 1 at load | `PROGRAM_LOAD_FAIL reason=program.slug "widgetco" != --program value "acme-corp"` |
| 27 | `--list-programs` smoke | one valid, one expired, one malformed under programs/ | exit 0; tabular output marks each | no SAFE_TARGET events |
| 28 | `--program` + `--skip-scope-check` mutual exclusion | both flags passed | exit 2 at parse_args | no audit row needed; stderr message |
| 29 | No `--program` flag (backward compat) | Phase 0 invocation with config/scope.txt only | identical to Phase 0 behavior | no `PROGRAM_*` events |
| 30 | Scanme dry-run with program | global scope includes scanme; program in_scope `scanme.nmap.org`; allowed techniques full | exit 0; same 5 audit rows as Phase 0.1 evidence + `PROGRAM_LOAD_OK` | matches `cowork_phase0_1_review.md` row #6 plus program event |

Each case must produce a temp directory under `.tmp_phase1_validation_<ts>/`
with `lab/config/scope.txt`, `lab/programs/<slug>/scope.json`, and
`lab/logs/audit.log`. Codex archives audit rows into
`handoff/phase1_validation_evidence.md` (analogous to
`handoff/phase0_1_validation_evidence.md`) before cleaning up.

---

## 7. Migration & Backward Compatibility

### 7.1 Phase 0 workflows that must keep working unchanged

- `./recon.sh <target>` with `config/scope.txt` only.
- `./recon.sh --dry-run --domain example.com -o /tmp/out` (Phase 0.1 evidence
  row #6 must still pass under Phase 1 code).
- `--skip-scope-check` + `SCOPE_OVERRIDE_TOKEN` + `SCOPE_OVERRIDE_CONFIRM`
  forced-dry-run path stays available **only when** `--program` is not set.
- `REQUIRE_SCOPE_CHECK=false` rejection stays a hard error.
- `bin/hermes review` continues to pass without `programs/` existing.

### 7.2 Mechanism

- All Phase 1 logic is gated on `PROGRAM_ACTIVE` being set after `load_program`.
- `load_program` runs only when `--program`, `--program-file`, or
  `$RECON_ACTIVE_PROGRAM` is present.
- `programs/` directory's mere existence is **not** a trigger.

### 7.3 Operator migration path

1. Operator creates `programs/<slug>/` with `scope.json` and
   `authorization.txt`.
2. Operator runs `./recon.sh --program <slug> --dry-run --domain <target>` to
   smoke-test schema and intersection.
3. Once acceptable, operator runs without `--dry-run` (and within window).
4. Existing global `config/scope.txt` entries don't need to change — programs
   carve narrower slices out of the global allow-list.

### 7.4 Behavior under partial operator readiness

- `programs/` directory present but empty: Phase 0 behavior. No change.
- `programs/<slug>/` directory present but `scope.json` missing or empty:
  `--program <slug>` → `PROGRAM_LOAD_FAIL`. Operator without `--program` flag
  is unaffected.
- `programs/<slug>/scope.json` valid but `authorization.txt` missing: warning
  logged, run proceeds. `authorization.txt` is a paper-trail expectation, not
  a code-enforced gate (operator discipline issue).

---

## 8. Risks and Non-Goals

### 8.1 Risks

1. **Schema validator dependency.** Robust schema enforcement wants
   `jsonschema` (Python) or `ajv` (Node). Phase 0.1 evidence shows `python3`
   and `python` are both available via `bin/hermes`'s fallback. Codex should
   prefer `python3 -m jsonschema` and degrade to a hand-written `jq`-based
   validator only if Python is unavailable at runtime. The handwritten
   fallback covers required-fields + enum + type checks; the JSON Schema file
   remains canonical.
2. **Time-zone arithmetic in bash.** Window checks use `TZ=<zone> date` which
   is fine on Linux/Kali but inconsistent on Git Bash for Windows. Codex must
   include a Git-Bash compatibility test in the validation matrix and document
   the supported timezone set or fall back to UTC-only windows on Windows.
3. **Out-of-scope wildcards interacting with global wildcards.** A global
   wildcard `*.example.com` plus a program out-of-scope `*.example.com` would
   reject everything. This is correct but might surprise operators; surface
   the intersection result in `summary.md` so dry-run output makes the
   restriction obvious.
4. **DNS-vs-literal mismatch.** A program lists `acme.example.com` and an
   in-scope CIDR `203.0.113.0/24`. If `acme.example.com` resolves into that
   CIDR, the literal-match approach treats the domain and IPs as distinct.
   Operator must list both forms if they want IP probing of the resolved host.
   Phase 2 may add opt-in resolve-and-revalidate; explicitly out of scope for
   Phase 1.
5. **Slug spoofing via `--program-file`.** A malicious or careless symlink
   could point `--program-file ./programs/acme/scope.json` at a different
   file with `slug: "acme"`. Mitigation: log resolved real-path and sha256 in
   `PROGRAM_LOAD_OK`. Slug match against the CLI value is verified, but the
   directory location is not authoritative; operator review of audit rows is
   the second layer.
6. **Concurrent runs reading the same program file.** If a program file is
   edited mid-run, in-flight stages keep the old effective config (file loaded
   once at start). Document this; do not hot-reload.
7. **Audit log size growth.** Per-stage `PROGRAM_TECHNIQUE_DENIED` rows are
   cheap (one per stage, not per target) so impact is minimal. No rotation
   change needed.

### 8.2 Non-goals for Phase 1

- IPv6 scope entries (existing Phase 0 limitation).
- Cryptographic signing of `scope.json` (out of scope; operator-curated repo
  files are trusted at the filesystem layer).
- Programmatic ingestion of <bug-bounty-platform>/Bugcrowd APIs to auto-build `scope.json`
  (operator writes the file by hand; auto-import is a Phase 3 idea).
- Runtime DNS resolution and re-validation.
- Per-target rate limiting via outbound proxy (advisory metadata only).
- Mid-run hot reload of program scope.
- Allowing `idn_handling: allow_idn`.
- Multi-program union runs (`--program a,b`). Operators that need two programs
  invoke `recon.sh` twice with different `--program` flags and separate output
  directories.
- New scanner stages, payload classes, or finding-elevation logic.

---

## 9. Codex Implementation Tasks (Small Reviewable Chunks)

Each task is small enough for an independent `handoff/codex_task_phase1_<n>.md`
and a corresponding `handoff/codex_review.md` update.

### Task P1-1 — Repo scaffolding

- Create `programs/` with `_schema/` and `_examples/` subdirectories.
- Add `programs/_schema/scope.schema.json` (JSON Schema draft 2020-12) covering
  the field set in §2.
- Add three `programs/_examples/*.example.json` files: `public-bounty`,
  `client-engagement`, `ctf-platform`.
- Add `programs/README.md` explaining the directory contract.
- Update `.gitignore` if needed (no — these files are operator-curated and
  belong in git).
- No `recon.sh` changes yet.
- Acceptance: `python3 -m jsonschema -i programs/_examples/public-bounty.example.json programs/_schema/scope.schema.json` exits 0 for each example; one deliberately-broken sample under `programs/_examples/invalid/` fails schema validation as documented in the README.

### Task P1-2 — Loader skeleton (no enforcement yet)

- Add `load_program <slug>` function to `recon.sh` that performs:
  syntax check (`jq -e . <file>`), schema check (`python3 -m jsonschema` with
  jq fallback), slug match, expiration, window, automation_permitted,
  forbidden-in-allowed.
- Add `--program`, `--program-file`, `--list-programs`, `$RECON_ACTIVE_PROGRAM`
  parsing.
- Add `PROGRAM_LOAD_OK` / `PROGRAM_LOAD_FAIL` / `PROGRAM_AUTOMATION_DENIED` /
  `PROGRAM_WINDOW_DENIED` audit events.
- `--program <slug>` activates the loader and exits with a clear "loader OK,
  enforcement not yet wired" warning so this chunk is testable in isolation.
- Acceptance: matrix rows 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27 pass
  (these exercise loader correctness without per-target enforcement).

### Task P1-3 — Program scope match (in-scope + out-of-scope)

- Add `program_scope_match <host_or_url>` and
  `program_out_of_scope_match <host_or_url>` helpers in `recon.sh`.
- Extend `safe_target` (recon.sh:431) to invoke both when `PROGRAM_ACTIVE`.
- Preserve all Phase 0 deny reasons; add the new ones from §3.5.
- No technique gate yet.
- Acceptance: matrix rows 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 28, 29, 30
  pass.

### Task P1-4 — Technique gate

- Add `program_technique_allowed <tag>` helper.
- Hook the per-stage entry points listed in §4.1.
- Wire `PROGRAM_TECHNIQUE_DENIED` audit + `summary.md` "Skipped Stages"
  section.
- Acceptance: matrix row 15 passes; row 30 still passes with full technique
  set; rows 13 and 14 reject malformed files at load (already covered by
  P1-2 but re-verified).

### Task P1-5 — Effective rate-limit computation

- At successful `load_program`, write `<outdir>/effective_config.json`
  computing minimums between recon.conf and program `rate_limits`.
- Override `NAABU_RATE`, `NUCLEI_RATE_LIMIT`, `NUCLEI_CONCURRENCY`,
  `HTTPX_THREADS`, `SUBFINDER_THREADS`, `MAX_PARALLEL_HOSTS` from effective
  values.
- Cap CLI `--rate` against program cap and warn on clamp.
- Surface effective rates in `summary.md`.
- Acceptance: matrix row 22 passes; rate visible in audit and summary.

### Task P1-6 — Documentation

- Update `.hermes.md` Security Gate section to point at Phase 1 as live, not
  future.
- Update `HERMES_WORKFLOW.md` row for "Change scope enforcement ... program
  scope parsing" with Phase 1 expectations.
- Update `config/scope.txt` header comment to reference `programs/<slug>/
  scope.json` as the program-specific layer.
- Add `programs/README.md` operator quickstart (created in P1-1; expand here).
- Append a Phase 1 entry to `handoff/accepted_changes.md` only after the
  Cowork independent review (next bullet) signs off.

### Task P1-7 — Independent review preparation

- Generate `handoff/phase1_validation_evidence.md` analogous to Phase 0.1:
  one row per matrix case, with the on-disk temp-lab path and a short audit
  excerpt for each.
- Clean up temp lab directories at the end (the Phase 0.1 review flagged this
  as housekeeping — do it from the start in Phase 1).
- Hand off to Cowork (Claude) for independent review →
  `handoff/cowork_phase1_review.md`.

Sequencing: P1-1 → P1-2 → P1-3 → P1-4 → P1-5 → P1-6 → P1-7. Tasks
P1-3 and P1-4 are coupled but split for review-size discipline; they may be
reviewed as one chunk if the operator prefers.

---

## 10. Acceptance Criteria

Phase 1 is closeable when **all** of the following hold:

### 10.1 Code & safety invariants

1. `bash -n recon.sh` exits 0.
2. `bin/hermes review` exits 0 with `programs/` populated by examples.
3. `config/scope.txt` is unchanged.
4. `REQUIRE_SCOPE_CHECK=false` still rejected as hard error.
5. `--skip-scope-check` without override still rejected; with override still
   forces dry-run; when combined with `--program`, exits 2.
6. Without `--program` / `$RECON_ACTIVE_PROGRAM`, recon.sh behavior is
   byte-for-byte equivalent to Phase 0 for the Phase 0.1 dry-run smoke matrix
   (especially row #6: scanme dry-run produces exactly the same five audit
   row types).
7. `safe_target` remains the single authoritative gate; no scanner stage
   bypasses it (no new `command -v <tool> && <tool>` paths added without
   prior `filter_safe_targets` step).
8. Scanner output framed in `summary.md` as triage-only (unchanged language).

### 10.2 Functional requirements

9. All 30 rows in the §6 test matrix produce the expected outcome and audit
   row, captured in `handoff/phase1_validation_evidence.md`.
10. JSON Schema validation rejects every deliberately-broken example under
    `programs/_examples/invalid/`.
11. `--list-programs` enumerates programs without running any stage and
    correctly labels expired / malformed / valid states.
12. Audit log distinguishes global-scope rejections from program-scope
    rejections in the `reason=` field.
13. `summary.md` shows the active program, scope file sha256, validity
    window, effective rate caps, and any skipped stages.

### 10.3 Default-deny behavior

14. Missing `programs/<slug>/scope.json` for an active `--program` flag →
    exit 1, no scans.
15. Malformed JSON, schema-invalid, schema-version-mismatched, expired,
    not-yet-valid, slug-mismatched, blackout-active, window-outside,
    automation-denied (without dry-run), forbidden-in-allowed,
    `allow_idn`-declared → all default-deny with `PROGRAM_LOAD_FAIL`/
    `PROGRAM_AUTOMATION_DENIED`/`PROGRAM_WINDOW_DENIED` and exit 1.
16. Hand-curated test where program file has `automation_permitted: true`
    but `allowed: []` → loader rejects (empty allowed list).

### 10.4 Workflow & review

17. `handoff/codex_review.md` documents files changed, validation results,
    and any open risks.
18. `handoff/accepted_changes.md` has a Phase 1 entry, appended only after
    Cowork independent review (next item) accepts.
19. Independent Cowork review at `handoff/cowork_phase1_review.md` issues a
    verdict (ACCEPT / ROUTE-BACK / REJECT) cross-checking at least the
    safety-critical matrix rows (1, 3, 4, 13, 14, 15, 17, 23, 24, 28) against
    the actual on-disk artifacts the Codex run produced.
20. `.agent.lock` is clear at the end of the Phase 1 sequence.

When 1–20 hold, Phase 1 is complete and the workflow can move to Phase 2
candidates (DNS resolution scope checks, outbound rate proxy,
platform-API-driven program ingestion).

---

## Appendix A — Suggested JSON Schema sketch (informative)

The full schema lives in `programs/_schema/scope.schema.json` and is Codex's
P1-1 deliverable; this sketch is for reviewer orientation only.

```jsonc
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Recon Program Scope",
  "type": "object",
  "required": ["schema_version", "program", "scope", "techniques",
               "rate_limits", "testing_windows", "expiration"],
  "additionalProperties": false,
  "properties": {
    "schema_version": { "type": "string", "const": "1.0" },
    "program": {
      "type": "object",
      "required": ["slug", "name", "platform", "url",
                   "authorization_reference", "policy_version",
                   "policy_acknowledged_at"],
      "additionalProperties": false,
      "properties": {
        "slug":    { "type": "string", "pattern": "^[a-z0-9-]{1,64}$" },
        "name":    { "type": "string", "minLength": 1, "maxLength": 200 },
        "platform":{ "type": "string",
                     "enum": ["<bug-bounty-platform>","bugcrowd","intigriti","yeswehack",
                              "client","lab","ctf","self-hosted","other"] },
        "url":     { "type": "string", "format": "uri" },
        "authorization_reference": { "type": "string", "minLength": 1 },
        "policy_version":          { "type": "string", "minLength": 1 },
        "policy_acknowledged_at":  { "type": "string", "format": "date-time" },
        "operator_contact":        { "type": "string" },
        "program_contact":         { "type": "string" }
      }
    },
    "scope": {
      "type": "object",
      "required": ["in_scope", "out_of_scope", "idn_handling"],
      "additionalProperties": false,
      "properties": {
        "in_scope": {
          "type": "array",
          "minItems": 1,
          "items": { "$ref": "#/$defs/scope_entry" }
        },
        "out_of_scope": {
          "type": "array",
          "items": { "$ref": "#/$defs/scope_entry" }
        },
        "idn_handling": {
          "type": "string",
          "enum": ["punycode_only", "reject_idn", "allow_idn"]
        }
      }
    },
    "techniques": {
      "type": "object",
      "required": ["allowed", "forbidden", "automation_permitted"],
      "additionalProperties": false,
      "properties": {
        "allowed":   { "type": "array", "items": { "$ref": "#/$defs/technique" } },
        "forbidden": { "type": "array", "items": { "$ref": "#/$defs/technique" } },
        "automation_permitted": { "type": "boolean" },
        "automation_notes":     { "type": "string" }
      }
    },
    "rate_limits": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "max_concurrency":         { "type": "integer", "minimum": 1 },
        "max_requests_per_second": { "type": "integer", "minimum": 1 },
        "request_delay_ms":        { "type": "integer", "minimum": 0 },
        "nuclei_rate_limit":       { "type": "integer", "minimum": 1 },
        "nuclei_concurrency":      { "type": "integer", "minimum": 1 },
        "naabu_rate":              { "type": "integer", "minimum": 1 },
        "httpx_threads":           { "type": "integer", "minimum": 1 },
        "subfinder_threads":       { "type": "integer", "minimum": 1 }
      }
    },
    "testing_windows": {
      "type": "object",
      "oneOf": [
        { "required": ["always"], "properties": { "always": { "const": true } } },
        { "required": ["timezone", "allowed"],
          "properties": {
            "always":   { "const": false },
            "timezone": { "type": "string", "minLength": 1 },
            "allowed":  { "type": "array", "minItems": 1,
                          "items": { "$ref": "#/$defs/window" } },
            "blackouts":{ "type": "array",
                          "items": { "$ref": "#/$defs/blackout" } }
          }
        }
      ]
    },
    "expiration": {
      "type": "object",
      "required": ["valid_from", "valid_until"],
      "additionalProperties": false,
      "properties": {
        "valid_from":  { "type": "string", "format": "date-time" },
        "valid_until": { "type": "string", "format": "date-time" }
      }
    }
  },
  "$defs": {
    "scope_entry": {
      "type": "object",
      "required": ["type", "value"],
      "properties": {
        "type":  { "enum": ["domain","wildcard","cidr","ip","url_prefix"] },
        "value": { "type": "string", "minLength": 1 },
        "include_apex": { "type": "boolean" },
        "notes":  { "type": "string" },
        "reason": { "type": "string" }
      }
    },
    "technique": {
      "enum": [
        "subdomain_enumeration","http_probe","port_scan","service_fingerprint",
        "directory_bruteforce","vulnerability_scan_passive",
        "vulnerability_scan_active","dos","intrusive_fuzz",
        "credential_brute_force","social_engineering","physical","malware",
        "callback_payloads"
      ]
    },
    "window": {
      "type": "object",
      "required": ["days","start","end"],
      "properties": {
        "days":  { "type": "array",
                   "items": { "enum": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] },
                   "minItems": 1 },
        "start": { "type": "string", "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$" },
        "end":   { "type": "string", "pattern": "^([01]\\d|2[0-3]):[0-5]\\d$" }
      }
    },
    "blackout": {
      "type": "object",
      "required": ["from","to","reason"],
      "properties": {
        "from":   { "type": "string", "format": "date-time" },
        "to":     { "type": "string", "format": "date-time" },
        "reason": { "type": "string", "minLength": 1 }
      }
    }
  }
}
```

The schema is informative here; the canonical version Codex commits in P1-1
may add type-specific value patterns (e.g., a `oneOf` over `value` keyed on
`type`) for tighter validation. Hand-written value validation in `recon.sh`
remains the runtime authority regardless of the schema's reach.

---

## Appendix B — Cross-reference to Phase 0.1 review

This proposal addresses the open Phase 1 design questions called out in
`cowork_phase0_1_review.md`:

- §"Safety Review", point 5 (apex-vs-wildcard policy choice): resolved as
  preserve-by-default with explicit `include_apex` opt-out per entry — §2.4,
  §3.1.
- §"Route Back to Codex", item 1 (reword wildcard recommendation): the
  current proposal treats Phase 1 as a *preserve-with-opt-out* decision,
  matching the existing rule in `config/scope.txt:8`. Codex P1-6 documentation
  task should update `handoff/phase0_1_validation_evidence.md` if not yet
  done.
- §"Documentation Issues", item 5 (temp lab cleanup): Codex P1-7 makes
  cleanup mandatory from the start.

---

End of proposal. Ready for operator approval and routing to Codex as
P1-1 through P1-7.
