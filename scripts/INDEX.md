> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Script Index

This index explains what each script is for, what it needs, what it creates, and the safe-use expectation. Use it before asking an agent to edit or run a script.

## Python Workflows

| Script | Purpose | Expected Output | Notes |
| --- | --- | --- | --- |
| `recon_automation.py` | Authorized target reconnaissance using external tools such as DNS, whois, subdomain discovery, and port/service enumeration. | JSON and Markdown recon summary. | Should be run only against labs or explicitly authorized targets. Add scope validation before expanding use. |
| `vuln_scan_integration.py` | Combine scanner output from tools such as nuclei, nikto, and whatweb into normalized findings. | JSON and Markdown vulnerability scan summary. | Scanner output must be manually verified before becoming a finding. |
| `passive_target_search.py` | Generate passive search URLs/queries and a first-bounty target triage template for a company/domain. | JSON or Markdown query pack; no network requests. | Use before Kali browser triage; outputs searches only and stops at gate terms rather than touching live targets. |
| `ingest_disclosed_reports.py` | Normalize offline public disclosed-report text into sanitized candidate-only records. | `disclosed_report_batch/0.1` JSON. | File-input only; no URL fetching/login; fails closed on login/CAPTCHA/private pages and redacts emails/secrets/OTP-like values. |
| `score_disclosed_report_patterns.py` | Score reusable primitive/class/surface/proof patterns from sanitized disclosed-report records. | `disclosed_report_patterns/0.1` JSON. | Candidate-pattern intelligence only; no live target contact or finding/report promotion. |

## Kali SSH Helpers

| Script | Purpose | Safe-Use Notes |
| --- | --- | --- |
| `kali-install-key.ps1` | Install the project public SSH key into Kali using one password-based SSH login. | Use only for your Kali VM. Does not store the Kali password. |
| `kali-check-tools.ps1` | Check common Kali/pentest tool availability over SSH. | Inventory only; does not scan targets. |
| `kali-run.ps1` | Run a command on Kali over SSH from Windows/Hermes/Codex. | Use only against labs, owned assets, or authorized scope. Prefer commands that write output under `~/codex-output`. |
| `kali-browser-ops.ps1` | Operate the Kali/noVNC browser workbench from Windows: status, open URL, browser reset, screenshot, click, type, hotkey, downloads metadata, and Chromium CDP tab metadata/visible text. | Browser-control helper only; do not type secrets/OTP/tokens/phone values; live target URLs still require scope and policy gates. |
| `kali-passive-browse.ps1` | End-to-end passive browser helper: start Kali if needed, ensure temporary NAT route, start noVNC tunnel, open a URL, extract sanitized visible text/gate flags, optionally close NAT after (`-CloseNatAfter`). | Passive/public browsing only; stops at gate flags for OTP/CAPTCHA/login-secret/phone/payment/KYC/scarce-claim/live-test decisions. |
| `kali-pull.ps1` | Pull Kali output files back into `<artifact-output-dir>/`. | Review outputs before moving them into formal notes or reports. |

## Shell Helpers

| Script | Purpose | Safe-Use Notes |
| --- | --- | --- |
| `gen_report.sh` | Generate an offline Markdown draft report from an existing `scans/<target>_<timestamp>/` directory. | Does not touch targets or send network traffic. Scanner hits remain triage until manually verified; DOCX output requires explicit format request plus local `pandoc`. |
| `subdomain_recon.sh` | Subdomain discovery and HTTP probing. | Use only within authorized domains and rate limits. |
| `subdomain_takeover.sh` | Identify possible dangling DNS or takeover indicators. | Treat as triage only; do not claim or modify third-party services without program rules and approval. |
| `xss_finder.sh` | Check reflected input behavior and XSS indicators. | Use minimal, non-destructive probes. Verify manually. |
| `sqli_triage.sh` | Triage possible SQL injection behavior. | Avoid heavy or destructive testing. Use lab targets unless explicit permission exists. |
| `ssrf_finder.sh` | Triage possible SSRF behavior using controlled callbacks. | Use only with approved callback infrastructure and authorization. |
| `lfi_finder.sh` | Triage possible file inclusion or path traversal behavior. | Do not access sensitive data beyond minimal proof. |
| `open_redirect.sh` | Detect open redirect behavior. | Verify impact and avoid abusive redirect destinations. |
| `cors_audit.sh` | Review CORS header behavior. | Confirm exploitability before reporting. |
| `jwt_inspect.sh` | Inspect JWT structure and weak configuration indicators. | Do not crack or attack real tokens without explicit authorization. Never store secrets. |
| `headers_audit.sh` | Review security headers and cookie flags. | Good candidate for defensive baseline checks. |
| `kali_audit.sh` | Inventory and audit a Kali environment. | Local defensive use. Avoid uploading sensitive local inventory. |
| `setup_kali.sh` | Install or configure Kali tooling. | Review before running because it may change the local environment. |

## Improvement Backlog

- Add a shared `--scope scope.json` option to scripts that touch targets.
- Add `--dry-run` to show planned commands without running them.
- Standardize output directories, filenames, timestamps, and tool version capture.
- Add parser tests using saved sample outputs instead of live scans.
- Add a dependency check command that reports missing tools cleanly.
