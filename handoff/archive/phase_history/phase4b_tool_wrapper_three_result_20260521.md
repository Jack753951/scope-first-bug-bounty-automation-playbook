> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B three mature-tool wrapper module run result

Status: completed / local-lab mature-tool wrappers / candidate-only
Date: 2026-05-21
Final run id: `phase4b_tool_wrapper_three_20260521T085200Z`
Target: `http://<lab-ip>:3000/`
Attacker: Kali VM `<lab-ip>`
Victim: disposable local lab `<lab-ip>`

## Purpose

After operator clarification, this wave intentionally did **not** category-ban broad scanners/fuzzers/tooling against the authorized disposable local靶機. It promoted three mature tools into reusable gated modules:

1. `lab_ffuf_sensitive_path_discovery`
2. `lab_nikto_server_misconfig`
3. `lab_nmap_http_fingerprint`

All output remains candidate-only and needs manual review. No public target, credentials, callback/OAST, loot retention, or report submission was used.

## Tool availability / NAT

Checked from Kali attacker VM:

```text
ffuf=/usr/bin/ffuf
nikto=/usr/bin/nikto
nmap=/usr/bin/nmap
sslyze=/usr/bin/sslyze
wfuzz=/usr/bin/wfuzz
gobuster=/usr/bin/gobuster
```

No NAT/download was needed in this wave because the selected tools were already installed. Attacker route still showed host-only lab route only:

```text
<lab-ip>/24 dev eth0 ...
```

## Safety gates

- local lab target only;
- generated runners require `--lab-approved`;
- public targets fail closed;
- pre/post health recorded;
- bounded tool timeouts;
- no real credentials;
- no callbacks/OAST;
- no raw response body retention by custom code;
- scanner/tool output parsed as `candidate-only`;
- no confirmed/reportable/submission language.

## TDD / implementation

RED test added first:

```text
scripts/test_owasp_tool_wrapper_modules.py
```

Then implemented:

```text
scripts/lab_modules/tool_wrapper_common.py
scripts/lab_modules/lab_ffuf_sensitive_path_discovery.py
scripts/lab_modules/lab_nikto_server_misconfig.py
scripts/lab_modules/lab_nmap_http_fingerprint.py
```

Generated runners:

```text
setting/local/lab_ffuf_sensitive_path_discovery_run.sh
setting/local/lab_nikto_server_misconfig_run.sh
setting/local/lab_nmap_http_fingerprint_run.sh
```

## Final artifacts

```text
<artifact-output-dir>/phase4b_tool_wrapper_three_20260521T085200Z/lab_ffuf_sensitive_path_discovery/
<artifact-output-dir>/phase4b_tool_wrapper_three_20260521T085200Z/lab_nikto_server_misconfig/
<artifact-output-dir>/phase4b_tool_wrapper_three_20260521T085200Z/lab_nmap_http_fingerprint/
```

Each module produced:

```text
observations.jsonl
possible_vulnerabilities.md
health.txt
summary.txt
artifact_manifest.txt
```

Tool-specific raw outputs were kept as local lab artifacts only.

## Results

### lab_ffuf_sensitive_path_discovery

Health:

```text
pre_health=200
post_health=200
```

Possible manual-review candidates:

```text
/rest/admin/application-configuration
/metrics
/api-docs
/ftp
/robots.txt
```

Suppressed likely SPA/default fallback controls:

```text
/admin
/administration
/backup
/server-status
/debug
/.git/HEAD
/swagger.json
```

### lab_nikto_server_misconfig

Health:

```text
pre_health=200
post_health=200
```

Possible manual-review candidates:

```text
Access-Control-Allow-Origin: *
Uncommon x-recruiting header pointing to /#/jobs
robots.txt should be manually viewed
Missing permissions-policy
Missing content-security-policy
Missing strict-transport-security
Missing referrer-policy
```

Note: an earlier pre-final Nikto run briefly left the app health check at `000`; the victim VM was restored from snapshot and the final run was rerun with shorter Nikto max time plus a cooldown. Final run health passed.

### lab_nmap_http_fingerprint

Health:

```text
pre_health=200
post_health=200
```

Possible manual-review candidates:

```text
None from this run.
```

Control:

```text
:3000 open service fingerprint observed
```

## Validation

```text
python scripts/test_owasp_tool_wrapper_modules.py
python -m py_compile scripts/lab_modules/tool_wrapper_common.py scripts/lab_modules/lab_ffuf_sensitive_path_discovery.py scripts/lab_modules/lab_nikto_server_misconfig.py scripts/lab_modules/lab_nmap_http_fingerprint.py
bash -n setting/local/lab_ffuf_sensitive_path_discovery_run.sh
bash -n setting/local/lab_nikto_server_misconfig_run.sh
bash -n setting/local/lab_nmap_http_fingerprint_run.sh
```

Focused tests passed:

```text
Ran 3 tests
OK
```

## Next recommended step

Add offline importer/candidate-review bridge for mature tool wrapper observations, with false-positive suppression metadata preserved. In particular, carry forward ffuf SPA/default fallback suppression and Nikto informational-versus-plugin-id separation.
