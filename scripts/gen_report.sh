#!/usr/bin/env bash
# Generate an offline draft pentest report from a completed recon scan directory.
# This script does not touch targets, send network traffic, or read loot/.

set -uo pipefail

if [[ -t 1 ]] && [[ "${NO_COLOR:-0}" != "1" ]]; then
    G=$'\033[0;32m'; Y=$'\033[1;33m'; R=$'\033[0;31m'; B=$'\033[0;34m'; RST=$'\033[0m'
else
    G=""; Y=""; R=""; B=""; RST=""
fi

HACKLAB="${HACKLAB:-$HOME/projects/cybersec}"
REPORT_ROOT="${REPORT_ROOT:-$HACKLAB/reports/generated}"
SCAN_DIR=""
OUT_DIR=""
REPORT_TITLE="Penetration Test Report"
FORMAT="md"
MAX_FINDINGS=50
MAX_EVIDENCE_LINES=20

info() { echo "${B}[INFO]${RST} $*"; }
ok() { echo "${G}[OK]${RST} $*"; }
warn() { echo "${Y}[WARN]${RST} $*" >&2; }
err() { echo "${R}[ERR]${RST} $*" >&2; }

show_help() {
    cat <<'EOF'
Usage:
  gen_report.sh [options] <scan_dir>

Purpose:
  Build an offline draft report from a completed scans/<target>_<timestamp>/ directory.
  Scanner output remains triage only; findings must be manually verified before delivery.

Options:
  -o, --out-dir <dir>      Output directory. Default: $HACKLAB/reports/generated/<scan_name>
  --title <title>          Report title. Default: Penetration Test Report
  --format <mode>          md, docx, both, or auto. Default: md
  --max-findings <n>       Maximum nuclei findings to summarize. Default: 50
  -h, --help               Show this help

Outputs:
  report.md                Always generated
  report.docx              Generated only when explicitly requested and pandoc is available
  report_manifest.json     Structured provenance and artifact summary

Safety:
  This script performs no scanning, exploitation, scheduling, webhook posting, or network IO.
  It refuses missing scan directories and does not read loot/.
EOF
}

need_value() {
    local opt="$1"
    local val="${2:-}"
    if [[ -z "$val" || "$val" == -* ]]; then
        err "$opt requires a value"
        exit 2
    fi
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            -o|--out-dir)
                need_value "$1" "${2:-}"
                OUT_DIR="$2"
                shift 2
                ;;
            --title)
                need_value "$1" "${2:-}"
                REPORT_TITLE="$2"
                shift 2
                ;;
            --format)
                need_value "$1" "${2:-}"
                FORMAT="$2"
                shift 2
                ;;
            --max-findings)
                need_value "$1" "${2:-}"
                MAX_FINDINGS="$2"
                shift 2
                ;;
            -*)
                err "Unknown option: $1"
                exit 2
                ;;
            *)
                if [[ -n "$SCAN_DIR" ]]; then
                    err "Only one scan_dir may be provided"
                    exit 2
                fi
                SCAN_DIR="$1"
                shift
                ;;
        esac
    done

    case "$FORMAT" in
        auto|md|docx|both) ;;
        *)
            err "--format must be one of: auto, md, docx, both"
            exit 2
            ;;
    esac
    if ! [[ "$MAX_FINDINGS" =~ ^[0-9]+$ ]] || [[ "$MAX_FINDINGS" -lt 1 ]]; then
        err "--max-findings must be a positive integer"
        exit 2
    fi
}

count_lines() {
    local file="$1"
    [[ -f "$file" ]] || { echo 0; return; }
    wc -l < "$file" | tr -d ' '
}

json_escape() {
    local s="$1"
    s=${s//\\/\\\\}
    s=${s//\"/\\\"}
    s=${s//$'\n'/\\n}
    s=${s//$'\r'/\\r}
    s=${s//$'\t'/\\t}
    printf '%s' "$s"
}

redact_url_secrets() {
    sed -E \
        -e 's/([?&](api[_-]?key|access[_-]?token|auth|code|key|password|passwd|secret|session|sid|token)=)[^&#[:space:]"'"'"'<>`]+/\1[REDACTED]/Ig' \
        -e 's#(https?://[^?[:space:]"'"'"'<>`]+)\?[^[:space:]"'"'"'<>`]+#\1?[REDACTED_QUERY]#Ig'
}

redact_stream() {
    sed -E \
        -e 's/([Aa]uthorization:[[:space:]]*)[^[:space:]]+/\1[REDACTED]/g' \
        -e 's/([Cc]ookie:[[:space:]]*).*/\1[REDACTED]/g' \
        -e 's/([Ss]et-[Cc]ookie:[[:space:]]*).*/\1[REDACTED]/g' \
        -e 's/((api[_-]?key|token|secret|password|passwd)[[:space:]]*[=:][[:space:]]*)[^[:space:]]+/\1[REDACTED]/Ig' \
        | redact_url_secrets
}

safe_table_cell() {
    redact_stream | tr '\r\n' '  ' | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/|/\\|/g; s/`/'"'"'/g'
}

safe_inline() {
    safe_table_cell | sed 's/[*_#[\]]/\\&/g'
}

heading_id() {
    printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-//; s/-$//'
}

scan_name() {
    basename "$SCAN_DIR"
}

target_from_scan_name() {
    local name
    name="$(scan_name)"
    if [[ "$name" =~ ^(.+)_[0-9]{8}_[0-9]{6}$ ]]; then
        echo "${BASH_REMATCH[1]}"
    else
        echo "$name"
    fi
}

severity_counts() {
    local nuclei="$SCAN_DIR/nuclei.jsonl"
    for sev in critical high medium low info unknown; do
        local count=0
        if [[ -s "$nuclei" ]] && command -v jq >/dev/null 2>&1; then
            if [[ "$sev" == "unknown" ]]; then
                count=$(jq -r '(.info.severity // "unknown")' "$nuclei" 2>/dev/null | grep -Ecv '^(critical|high|medium|low|info)$' || true)
            else
                count=$(jq -r '(.info.severity // "unknown")' "$nuclei" 2>/dev/null | grep -Ec "^$sev$" || true)
            fi
        fi
        printf '%s:%s\n' "$sev" "$count"
    done
}

write_asset_inventory() {
    local report="$1"
    {
        echo "## Asset Inventory"
        echo
        echo "### Live Hosts"
        echo
        if [[ -s "$SCAN_DIR/live_hosts.txt" ]]; then
            echo "| Host |"
            echo "|---|"
            sed '/^[[:space:]]*$/d' "$SCAN_DIR/live_hosts.txt" | head -100 | while IFS= read -r host; do
                printf '| `%s` |\n' "$(printf '%s' "$host" | safe_table_cell)"
            done
        else
            echo "No live host file was present in the scan directory."
        fi
        echo

        echo "### Open Ports"
        echo
        if [[ -s "$SCAN_DIR/ports.txt" ]]; then
            echo "| Host | Port |"
            echo "|---|---:|"
            head -200 "$SCAN_DIR/ports.txt" | while IFS=: read -r host port rest; do
                [[ -z "${host:-}" || -z "${port:-}" ]] && continue
                printf '| `%s` | `%s` |\n' "$(printf '%s' "$host" | safe_table_cell)" "$(printf '%s' "$port" | safe_table_cell)"
            done
        else
            echo "No port inventory was present in the scan directory."
        fi
        echo

        echo "### Web Technologies"
        echo
        if [[ -s "$SCAN_DIR/web/httpx.json" ]] && command -v jq >/dev/null 2>&1; then
            echo "| URL | Status | Title | Technology |"
            echo "|---|---:|---|---|"
            jq -r '[.url, (.status_code // "-"), (.title // "-"), ((.tech // []) | join(", "))] | @tsv' \
                "$SCAN_DIR/web/httpx.json" 2>/dev/null | head -100 | while IFS=$'\t' read -r url status title tech; do
                printf '| `%s` | %s | %s | %s |\n' \
                    "$(printf '%s' "$url" | safe_table_cell)" \
                    "$(printf '%s' "$status" | safe_table_cell)" \
                    "$(printf '%s' "$title" | safe_table_cell)" \
                    "$(printf '%s' "$tech" | safe_table_cell)"
            done
        elif [[ -s "$SCAN_DIR/web/live_urls.txt" ]]; then
            echo "| URL |"
            echo "|---|"
            head -100 "$SCAN_DIR/web/live_urls.txt" | while IFS= read -r url; do
                printf '| `%s` |\n' "$(printf '%s' "$url" | safe_table_cell)"
            done
        else
            echo "No web probe output was present in the scan directory."
        fi
        echo
    } >> "$report"
}

write_findings() {
    local report="$1"
    local nuclei="$SCAN_DIR/nuclei.jsonl"
    {
        echo "## Findings"
        echo
        echo "Scanner output in this section is triage only. Each item needs manual verification, impact analysis, remediation owner review, and retest evidence before it becomes a confirmed report finding."
        echo
    } >> "$report"

    if [[ ! -s "$nuclei" ]]; then
        {
            echo "No nuclei findings were present in the scan directory."
            echo
        } >> "$report"
        return
    fi

    if ! command -v jq >/dev/null 2>&1; then
        {
            echo "nuclei.jsonl exists, but jq is not available. Review the raw file manually:"
            echo
            echo "- \`$nuclei\`"
            echo
        } >> "$report"
        return
    fi

    jq -c '.' "$nuclei" 2>/dev/null | head -"$MAX_FINDINGS" | nl -ba | while IFS=$'\t' read -r idx json; do
        local severity template_id name host matcher reference cwe cvss_slug
        severity=$(printf '%s' "$json" | jq -r '.info.severity // "unknown"' 2>/dev/null)
        template_id=$(printf '%s' "$json" | jq -r '."template-id" // "unknown-template"' 2>/dev/null)
        name=$(printf '%s' "$json" | jq -r '.info.name // ."template-id" // "Unnamed scanner hit"' 2>/dev/null)
        host=$(printf '%s' "$json" | jq -r '.host // .matched // .url // "unknown asset"' 2>/dev/null)
        matcher=$(printf '%s' "$json" | jq -r '."matcher-name" // "-"' 2>/dev/null)
        reference=$(printf '%s' "$json" | jq -r '(.info.reference // []) | if type == "array" then join(", ") else tostring end' 2>/dev/null)
        cwe=$(printf '%s' "$json" | jq -r '(.info.classification.cwe-id // []) | if type == "array" then join(", ") else tostring end' 2>/dev/null)
        cvss_slug=$(heading_id "$template_id")

        {
            echo "### F-$idx: $(printf '%s' "$name" | safe_inline)"
            echo
            echo "- **Status:** Unverified scanner triage"
            echo "- **Scanner severity:** $(printf '%s' "$severity" | safe_inline)"
            echo "- **CVSS estimate:** Not assigned until manual verification"
            echo "- **Affected asset:** \`$(printf '%s' "$host" | safe_inline)\`"
            echo "- **Template:** \`$(printf '%s' "$template_id" | safe_inline)\`"
            echo "- **Matcher:** $(printf '%s' "$matcher" | safe_inline)"
            echo "- **Confidence:** Pending manual validation"
            echo
            echo "#### Evidence Excerpt"
            echo
            echo '```json'
            printf '%s\n' "$json" | jq '{template_id: ."template-id", matcher: ."matcher-name", host, matched, extracted_results, info: {name: .info.name, severity: .info.severity, description: .info.description}}' 2>/dev/null | redact_stream
            echo '```'
            echo
            echo "#### Remediation"
            echo
            echo "Review the affected service and vendor guidance for the verified weakness. Apply the least disruptive fix, then retest the specific endpoint or service."
            echo
            echo "#### Retest Steps"
            echo
            echo "1. Reproduce the condition manually on the authorized target."
            echo "2. Confirm impact without collecting secrets or sensitive data."
            echo "3. Apply the fix or mitigation."
            echo "4. Re-run the exact validation path and attach evidence showing the condition is resolved."
            echo
            echo "#### References"
            [[ -n "$cwe" && "$cwe" != "null" ]] && echo "- CWE: $(printf '%s' "$cwe" | safe_inline)"
            [[ -n "$reference" && "$reference" != "null" ]] && echo "- Scanner references: $(printf '%s' "$reference" | safe_inline)"
            [[ -z "$reference" || "$reference" == "null" ]] && echo "- Scanner template: \`$(printf '%s' "$template_id" | safe_inline)\`"
            echo "<a id=\"$cvss_slug\"></a>"
            echo
        } >> "$report"
    done
}

write_nmap_excerpt() {
    local report="$1"
    {
        echo "## Service Fingerprinting Evidence"
        echo
        if [[ -d "$SCAN_DIR/nmap" ]]; then
            local found=0
            while IFS= read -r file; do
                found=1
                echo "### $(basename "$file")"
                echo
                echo '```'
                grep -E '^[0-9]+/tcp[[:space:]]+open|^Service Info:|^Host is up|^Nmap scan report' "$file" 2>/dev/null \
                    | head -"$MAX_EVIDENCE_LINES" \
                    | redact_stream
                echo '```'
                echo
            done < <(find "$SCAN_DIR/nmap" -type f -name '*.nmap' 2>/dev/null | sort | head -20)
            [[ "$found" -eq 0 ]] && echo "No .nmap text files were present."
        else
            echo "No nmap directory was present."
        fi
        echo
    } >> "$report"
}

write_appendix() {
    local report="$1"
    {
        echo "## Appendix: Local Artifact References"
        echo
        echo "Raw scanner files are referenced rather than embedded to avoid accidental disclosure of sensitive data. Review and redact before sharing outside the lab or client-approved channel."
        echo
        echo "| Artifact | Present | Notes |"
        echo "|---|---:|---|"
        for path in \
            "summary.md" \
            "live_hosts.txt" \
            "ports.txt" \
            "web/httpx.json" \
            "web/live_urls.txt" \
            "nuclei.jsonl" \
            "nuclei_findings.md"; do
            if [[ -e "$SCAN_DIR/$path" ]]; then
                printf '| `%s` | yes | `%s` |\n' "$path" "$SCAN_DIR/$path"
            else
                printf '| `%s` | no | - |\n' "$path"
            fi
        done
        echo
        echo "### Screenshots Placeholder"
        echo
        echo "Attach manually captured screenshots only after confirming they contain no secrets, personal data, or unrelated client information."
        echo
    } >> "$report"
}

write_manifest() {
    local manifest="$1"
    local report_md="$2"
    local report_docx="$3"
    local generated_at target
    generated_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    target="$(target_from_scan_name)"
    {
        echo "{"
        printf '  "generated_at": "%s",\n' "$(json_escape "$generated_at")"
        printf '  "generator": "scripts/gen_report.sh",\n'
        printf '  "scan_dir": "%s",\n' "$(json_escape "$SCAN_DIR")"
        printf '  "target_guess": "%s",\n' "$(json_escape "$target")"
        printf '  "report_markdown": "%s",\n' "$(json_escape "$report_md")"
        if [[ -n "$report_docx" && -f "$report_docx" ]]; then
            printf '  "report_docx": "%s",\n' "$(json_escape "$report_docx")"
        else
            printf '  "report_docx": null,\n'
        fi
        printf '  "counts": {\n'
        printf '    "live_hosts": %s,\n' "$(count_lines "$SCAN_DIR/live_hosts.txt")"
        printf '    "ports": %s,\n' "$(count_lines "$SCAN_DIR/ports.txt")"
        printf '    "nuclei_findings": %s\n' "$(count_lines "$SCAN_DIR/nuclei.jsonl")"
        printf '  },\n'
        printf '  "tools": {\n'
        if command -v jq >/dev/null 2>&1; then
            printf '    "jq": "%s",\n' "$(json_escape "$(jq --version 2>/dev/null)")"
        else
            printf '    "jq": null,\n'
        fi
        if command -v pandoc >/dev/null 2>&1; then
            printf '    "pandoc": "%s"\n' "$(json_escape "$(pandoc --version 2>/dev/null | head -1)")"
        else
            printf '    "pandoc": null\n'
        fi
        printf '  }\n'
        echo "}"
    } > "$manifest"
}

generate_report() {
    local report="$1"
    local target generated_at host_count port_count finding_count
    target="$(target_from_scan_name)"
    generated_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    host_count="$(count_lines "$SCAN_DIR/live_hosts.txt")"
    port_count="$(count_lines "$SCAN_DIR/ports.txt")"
    finding_count="$(count_lines "$SCAN_DIR/nuclei.jsonl")"

    {
        echo "# $(printf '%s' "$REPORT_TITLE" | safe_inline)"
        echo
        echo "- **Target:** \`$(printf '%s' "$target" | safe_inline)\`"
        echo "- **Scan directory:** \`$SCAN_DIR\`"
        echo "- **Generated:** $generated_at"
        echo "- **Report status:** Draft, pending manual verification"
        echo "- **Allowed use:** Authorized lab, owned asset, explicit client scope, CTF/training, or bug bounty scope only"
        echo
        echo "## Executive Summary"
        echo
        echo "This draft summarizes artifacts from an existing local scan directory. It does not prove exploitability by itself. Scanner hits are presented as triage leads and must be manually verified before delivery."
        echo
        echo "| Metric | Count |"
        echo "|---|---:|"
        echo "| Live hosts | $host_count |"
        echo "| Open port records | $port_count |"
        echo "| Nuclei triage items | $finding_count |"
        echo
        echo "### Severity Histogram"
        echo
        echo "| Severity | Count |"
        echo "|---|---:|"
        severity_counts | while IFS=: read -r sev count; do
            printf '| %s | %s |\n' "$sev" "$count"
        done
        echo
        echo "## Methodology And Tooling"
        echo
        echo "| Phase | Source Artifact | Notes |"
        echo "|---|---|---|"
        echo "| Scope and target intake | scan directory name and local artifacts | Confirm authorization before treating any result as reportable. |"
        echo "| Host discovery | \`live_hosts.txt\` | Existing recon output only; this generator does not probe targets. |"
        echo "| Port inventory | \`ports.txt\` and \`nmap/\` | Service details require manual review. |"
        echo "| Web probing | \`web/httpx.json\`, \`web/live_urls.txt\` | Titles and technologies are informational. |"
        echo "| Vulnerability triage | \`nuclei.jsonl\` | Scanner hits are not confirmed findings. |"
        echo "| Report generation | \`scripts/gen_report.sh\` | Offline transformation into Markdown/DOCX. |"
        echo
    } > "$report"

    write_asset_inventory "$report"
    write_findings "$report"
    write_nmap_excerpt "$report"
    write_appendix "$report"
}

convert_docx() {
    local report_md="$1"
    local report_docx="$2"
    if ! command -v pandoc >/dev/null 2>&1; then
        if [[ "$FORMAT" == "docx" || "$FORMAT" == "both" ]]; then
            err "pandoc is required for --format $FORMAT but was not found"
            return 1
        fi
        warn "pandoc not found; generated Markdown only"
        return 0
    fi
    pandoc -- "$report_md" -o "$report_docx"
}

main() {
    parse_args "$@"

    if [[ -z "$SCAN_DIR" ]]; then
        err "Missing scan_dir"
        show_help
        exit 2
    fi
    if [[ ! -d "$SCAN_DIR" ]]; then
        err "Scan directory not found: $SCAN_DIR"
        exit 1
    fi
    if find "$SCAN_DIR" -type l -print -quit 2>/dev/null | grep -q .; then
        err "Refusing scan directory containing symlinks; copy artifacts into a plain directory first"
        exit 1
    fi
    SCAN_DIR="$(cd -P "$SCAN_DIR" && pwd -P)"
    local loot_canon=""
    if [[ -d "$HACKLAB/loot" ]]; then
        loot_canon="$(cd -P "$HACKLAB/loot" && pwd -P)"
    fi
    case "$SCAN_DIR" in
        *"/loot"|*"/loot/"*|*"\\loot"|*"\\loot\\"*)
            err "Refusing to read loot paths"
            exit 1
            ;;
    esac
    if [[ -n "$loot_canon" ]]; then
        case "$SCAN_DIR" in
            "$loot_canon"|"$loot_canon"/*)
                err "Refusing to read loot paths"
                exit 1
                ;;
        esac
    fi

    if [[ -z "$OUT_DIR" ]]; then
        OUT_DIR="$REPORT_ROOT/$(scan_name)"
    fi
    mkdir -p -- "$OUT_DIR"

    local report_md report_docx manifest
    report_md="$OUT_DIR/report.md"
    report_docx="$OUT_DIR/report.docx"
    manifest="$OUT_DIR/report_manifest.json"

    info "Reading scan artifacts from: $SCAN_DIR"
    info "Writing report artifacts to: $OUT_DIR"

    generate_report "$report_md"

    local docx_status=""
    case "$FORMAT" in
        auto|both|docx)
            if convert_docx "$report_md" "$report_docx"; then
                [[ -f "$report_docx" ]] && docx_status="$report_docx"
            else
                exit 1
            fi
            ;;
        md)
            ;;
    esac

    write_manifest "$manifest" "$report_md" "$docx_status"

    ok "Markdown report: $report_md"
    [[ -n "$docx_status" ]] && ok "DOCX report: $docx_status"
    ok "Manifest: $manifest"
    warn "Manual verification is required before any finding is reported as confirmed."
}

main "$@"
