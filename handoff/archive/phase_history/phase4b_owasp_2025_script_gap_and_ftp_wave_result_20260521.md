> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B OWASP 2025 script gap inventory and /ftp/ bounded wave result

Status: active result / local-lab fast lane
Date: 2026-05-21
Route/tool: Hermes local tools + Kali bridge (`scripts/kali-run.ps1`, `scripts/kali-pull.ps1`)
Visible runtime model: gpt-5.5 via Hermes/OpenAI Codex route; exact lower-level deployment details not exposed

## Operator intent

Collect scripts against OWASP Top 10 2025 classes, test them on the intentionally vulnerable lab target, reduce over-heavy review where the target is the local靶機, and modularize successful script combinations.

## Lab boundary used

Target class: local intentionally vulnerable lab / private host-only VM.

Concrete target used for this wave:

```text
http://<lab-ip>:3000/
```

This run did not touch public or real bug-bounty targets. It did not run broad scanners, brute force, OAST/callbacks, credentialed flows, exploit chains, recursive crawlers, file downloads, or report submission.

## OWASP Top 10 2025 script gap inventory

| OWASP 2025 class | Current scripts/modules | Gap / treatment |
|---|---|---|
| A01 Broken Access Control | `route_auth_matrix`, `idor_manual_checklist` planning; no fast-lane runner | manual/checklist first; no credentialed/auth bypass automation in this wave |
| A02 Security Misconfiguration | `phase4b_get_only_metadata_probe.py`, `ftp_filename_content_class_verifier.py`, `lab_directory_listing_triage` bundle | selected for lowest-risk bounded lab wave around `/ftp/` |
| A03 Software Supply Chain Failures | lockfile/dependency metadata planning only | checklist/offline only; no registry/API downloads in fast lane |
| A04 Cryptographic Failures | headers/cookie/TLS metadata aliases | passive metadata only; no secret/key collection |
| A05 Injection | `wave2_benign_params.py`; original `open_redirect.sh`, `xss_finder.sh`, `sqli_triage.sh` gated | inert canary adapter exists; SQLi/LFI style payload automation remains deferred |
| A06 Insecure Design | checklist/threat-model artifacts | no target-touching automation selected |
| A07 Authentication Failures | manual auth checklist/JWT offline inspection | no brute force, no credential stuffing, no credentialed flows |
| A08 Software or Data Integrity Failures | lockfile/integrity metadata planning | offline/checklist only |
| A09 Security Logging and Alerting Failures | checklist/evidence questions | no noisy event generation in this wave |
| A10 Mishandling of Exceptional Conditions | error-page/status metadata planning | no fuzz/crash/DoS/error storming |

Selected bounded wave: A02:2025 Security Misconfiguration / directory listing metadata, because it is already indicated by previous `/ftp/` preview context and can be tested with three fixed GET requests and no file-content retrieval.

## Implemented reusable adapter

New module:

```text
scripts/lab_modules/ftp_filename_content_class_verifier.py
```

Focused tests:

```text
scripts/test_ftp_filename_content_class_verifier.py
```

Generated runnable script:

```text
setting/local/ftp_filename_content_class_verifier_run.sh
```

Bundle promoted/updated:

```text
modules/bundles/lab_directory_listing_triage.md
scripts/SCRIPT_INVENTORY.md
```

Adapter behavior:

- plan-only by default;
- `--lab-approved` required before writing executable script;
- private/local-lab target allowlist;
- fixed `/ftp/` path only;
- pre/post health checks;
- one bounded GET of `/ftp/`;
- parse anchor filenames locally;
- classify filename/content classes;
- remove temporary raw body;
- output candidate-only JSONL;
- no listed-file downloads, recursion, scanner, payload, callback, credential, or promotion vocabulary.

## Lab run result

Remote output directory:

```text
/home/kali/codex-output/phase4b_ftp_filename_20260521T064526Z
```

Pulled local artifact directory:

```text
<artifact-output-dir>/phase4b_ftp_filename_20260521T064526Z/
```

Summary:

```text
observations=1
GET /ftp/ -> 200 entries=11 title='listing directory /ftp/'
```

Health:

```text
pre_health=200
post_health=200
requests_sent=1
```

Filename classes observed:

```text
quarantine [unknown_or_other]
acquisitions.md [text_or_markdown]
announcement_encrypted.md [text_or_markdown]
coupons_2013.md.bak [backup_or_temporary_candidate]
eastere.gg [unknown_or_other]
encrypt.pyc [unknown_or_other]
incident-support.kdbx [password_database_candidate]
legal.md [text_or_markdown]
package-lock.json.bak [backup_or_temporary_candidate]
package.json.bak [backup_or_temporary_candidate]
suspicious_errors.yml [unknown_or_other]
```

Interpretation: this is a candidate/observation-only lab result. It is useful for triage and report rehearsal after manual review, but it is not confirmed evidence and not report-ready.

## Validation commands

```text
python scripts/test_ftp_filename_content_class_verifier.py
bash -n setting/local/ftp_filename_content_class_verifier_run.sh
Kali bridge run via scripts/kali-run.ps1
Kali artifact pull via scripts/kali-pull.ps1 with MSYS2_ARG_CONV_EXCL='*'
```

Observed validation:

```text
5 tests OK
bash -n OK
pre/post health 200
observations.jsonl produced
```

## Modularization decision

The successful script combination is now retained as:

1. bounded runner/adapter: `scripts/lab_modules/ftp_filename_content_class_verifier.py`;
2. operator-facing bundle: `modules/bundles/lab_directory_listing_triage.md`;
3. script inventory entry: `scripts/SCRIPT_INVENTORY.md`;
4. generated runnable helper: `setting/local/ftp_filename_content_class_verifier_run.sh`;
5. pulled lab artifact fixture/result: `<artifact-output-dir>/phase4b_ftp_filename_20260521T064526Z/`.

Bridge/importer deferral: candidate-review fixture generation is intentionally deferred. The output has filename classes only and needs a separate small bridge/importer slice before any finding fixture or report-readiness workflow consumes it.
