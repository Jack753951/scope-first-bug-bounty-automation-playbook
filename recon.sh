#!/usr/bin/env bash
# =============================================================================
# recon.sh - Authorized reconnaissance pipeline
#
# Safety contract:
# - Scanner output is triage only, never a confirmed finding.
# - Every host or URL is checked through safe_target before any stage consumes it.
# - Missing, malformed, ambiguous, or out-of-scope targets are refused by default.
# - --skip-scope-check is retained for CLI compatibility only. It requires a
#   matching per-session token and forces dry-run mode so no network egress occurs.
# =============================================================================

set -uo pipefail
shopt -s nocasematch

if [[ -t 1 ]] && [[ "${NO_COLOR:-0}" != "1" ]]; then
    R=$'\033[0;31m'; G=$'\033[0;32m'; Y=$'\033[1;33m'
    B=$'\033[0;34m'; C=$'\033[0;36m'
    BLD=$'\033[1m'; DIM=$'\033[2m'; RST=$'\033[0m'
else
    R=""; G=""; Y=""; B=""; C=""; BLD=""; DIM=""; RST=""
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HACKLAB="${HACKLAB:-$HOME/projects/cybersec}"
CONFIG_FILE="$HACKLAB/config/recon.conf"
SCOPE_FILE="$HACKLAB/config/scope.txt"
AUDIT_LOG_FILE="$HACKLAB/logs/audit.log"

DEFAULT_INTENSITY="normal"
RECON_PROFILE="live-low-speed"
NAABU_TOP_PORTS_QUICK=100
NAABU_TOP_PORTS_NORMAL=1000
NAABU_RATE=50
NAABU_TIMEOUT=1000
NMAP_SCRIPTS="default,vuln,banner"
NMAP_TIMING="-T4"
NMAP_HOST_TIMEOUT="10m"
SUBFINDER_TIMEOUT=30
SUBFINDER_THREADS=20
USE_CRT_SH=true
HTTPX_THREADS=5
HTTPX_TIMEOUT=10
HTTPX_PROBES="-title -tech-detect -status-code -content-length -web-server -ip -cname"
FEROX_WORDLIST="/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt"
FEROX_WORDLIST_FALLBACK="/usr/share/wordlists/dirb/common.txt"
FEROX_THREADS=2
FEROX_DEPTH=2
FEROX_EXTENSIONS="php,html,txt,bak,old,zip,js,json,xml,conf"
FEROX_STATUS_CODES="200,204,301,302,307,401,403,500"
NUCLEI_SEVERITY_NORMAL="info,low,medium"
NUCLEI_SEVERITY_AGGRESSIVE="info,low,medium,high,critical"
NUCLEI_RATE_LIMIT=10
NUCLEI_CONCURRENCY=3
NUCLEI_TIMEOUT=10
NUCLEI_EXCLUDE_TAGS="dos,intrusive,fuzz"
NUCLEI_EXCLUDE_TAGS_FULL=""
DEFAULT_PROXY=""
BURP_PROXY="http://127.0.0.1:8080"
SLACK_WEBHOOK=""
GENERIC_WEBHOOK=""
NOTIFY_ON_FINDING_SEVERITY="high,critical"
MAX_PARALLEL_HOSTS=5
LIVE_MAX_REQUESTS_PER_HOST_PER_RUN=50
LIVE_MAX_STATE_CHANGES_PER_RUN=5
LIVE_MAX_CHAIN_STEPS=3
LIVE_REQUIRE_TECHNIQUE_ALLOW=true
LIVE_ALLOW_FULL_PROFILE=false
REQUIRE_SCOPE_CHECK=true
AUDIT_LOG=true

if [[ -f "$CONFIG_FILE" ]]; then
    # shellcheck source=/dev/null
    source "$CONFIG_FILE"
fi

TARGET=""
TARGETS_FILE=""
DOMAIN_MODE=false
INTENSITY="$DEFAULT_INTENSITY"
PROXY=""
USE_BURP=false
RATE_OVERRIDE=""
SLACK_OVERRIDE=""
WEBHOOK_OVERRIDE=""
SKIP_SCOPE_CHECK=false
OUTPUT_DIR_OVERRIDE=""
VERBOSE=false
DRY_RUN=false
PROGRAM_SLUG=""
PROGRAM_SCOPE_FILE=""
POLICY_MODE=""
ALLOW_CIDR=false

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RUN_LOG=""
SAFE_TARGET_VALUE=""
SAFE_TARGET_HOST=""
SAFE_TARGET_REASON=""
SCOPE_FILE_VALIDATED=""
POLICY_ARTIFACT_DIR=""
POLICY_VERDICT=""
POLICY_AUDIT_EVENT=""
POLICY_ARTIFACT=""
POLICY_DENY_REASON_CODES=""
POLICY_MESSAGE=""
POLICY_PROGRAM_SHA256=""
POLICY_GLOBAL_SHA256=""
POLICY_DECIDED_AT_UTC=""
POLICY_ERROR_COUNT=0
# Exit code 3 is reserved for program-policy boundary/config errors.
POLICY_BOUNDARY_ERROR_EXIT=3

_log() {
    local level="$1"; shift
    local color="$1"; shift
    local msg="$*"
    local line="[$(date +%H:%M:%S)] [${level}] ${msg}"
    echo "${color}${line}${RST}"
    [[ -n "$RUN_LOG" ]] && echo "$line" >> "$RUN_LOG"
}

info()  { _log "INFO" "$B" "$@"; }
ok()    { _log "OK" "$G" "$@"; }
warn()  { _log "WARN" "$Y" "$@"; }
err()   { _log "ERR" "$R" "$@"; }
dbg()   { $VERBOSE && _log "DBG" "$DIM" "$@"; return 0; }
title() { echo; echo "${BLD}${C}== $* ==${RST}"; [[ -n "$RUN_LOG" ]] && echo "== $* ==" >> "$RUN_LOG"; }

policy_note_boundary_error() {
    POLICY_ERROR_COUNT=$((POLICY_ERROR_COUNT + 1))
}

policy_is_boundary_error() {
    [[ "$POLICY_VERDICT" == "error" ]] && return 0
    case ",${POLICY_DENY_REASON_CODES}," in
        *,VALIDATOR_DENY,*|*,ARTIFACT_VALIDATION_FAILED,*|*,INVALID_POLICY_TIMEOUT,*) return 0 ;;
    esac
    return 1
}

show_help() {
    cat <<EOF
${BLD}recon.sh${RST} - authorized reconnaissance pipeline

Usage:
  $0 [OPTIONS] <target>
  $0 [OPTIONS] -f <targets-file>

Target options:
  -d, --domain              Expand subdomains for an authorized domain.
  -f, --file <file>         Read targets from a local file.

Intensity:
  --quick                   Top 100 ports, nuclei info/low only.
  --normal                  Default: top 1000 ports, info/low/medium.
  --aggressive              All ports, info through critical.
  --full                    Includes intrusive/fuzz nuclei tags; use only when authorized.

Network options:
  --proxy <url>             SOCKS/HTTP proxy, e.g. socks5://127.0.0.1:9050.
  --burp                    Proxy web tooling through http://127.0.0.1:8080.
  --rate <n>                naabu rate override. Default: $NAABU_RATE.

Notifications:
  --slack <webhook>         Slack incoming webhook URL.
  --webhook <url>           Generic JSON POST webhook URL.

Safety:
  --scope <file>            Authorization scope file. Default: $SCOPE_FILE.
  --skip-scope-check        Compatibility only. Requires matching
                             SCOPE_OVERRIDE_TOKEN and SCOPE_OVERRIDE_CONFIRM and
                             always forces --dry-run.
  --dry-run                 Print commands and create local bookkeeping only.
  --program <slug>          Activate program scope file lookup at
                             \$HACKLAB/programs/<slug>/scope.json.
  --policy-mode <mode>      Required with --program: dry-run, planned, or live.
  --allow-cidr              Accepted for future program CIDR policy handling.

Output:
  -o, --output <dir>        Output directory. Default: \$HACKLAB/scans/<target>_<ts>.
  -v, --verbose             Verbose logging.
  -h, --help                Show this help.
EOF
}

trim() {
    local s="$*"
    s="${s#"${s%%[![:space:]]*}"}"
    s="${s%"${s##*[![:space:]]}"}"
    printf '%s' "$s"
}

check_tool() {
    local tool="$1"
    if ! command -v "$tool" &>/dev/null; then
        warn "$tool not found; related stage will be skipped"
        return 1
    fi
    return 0
}

require_arg() {
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
            -h|--help)          show_help; exit 0 ;;
            -d|--domain)        DOMAIN_MODE=true; shift ;;
            -f|--file)          require_arg "$1" "${2:-}"; TARGETS_FILE="$2"; shift 2 ;;
            --quick)            INTENSITY="quick"; shift ;;
            --normal)           INTENSITY="normal"; shift ;;
            --aggressive)       INTENSITY="aggressive"; shift ;;
            --full)             INTENSITY="full"; shift ;;
            --proxy)            require_arg "$1" "${2:-}"; PROXY="$2"; shift 2 ;;
            --burp)             USE_BURP=true; shift ;;
            --rate)             require_arg "$1" "${2:-}"; RATE_OVERRIDE="$2"; shift 2 ;;
            --slack)            require_arg "$1" "${2:-}"; SLACK_OVERRIDE="$2"; shift 2 ;;
            --webhook)          require_arg "$1" "${2:-}"; WEBHOOK_OVERRIDE="$2"; shift 2 ;;
            --scope)            require_arg "$1" "${2:-}"; SCOPE_FILE="$2"; shift 2 ;;
            --skip-scope-check) SKIP_SCOPE_CHECK=true; shift ;;
            --dry-run)          DRY_RUN=true; shift ;;
            --program)          require_arg "$1" "${2:-}"; PROGRAM_SLUG="$2"; shift 2 ;;
            --policy-mode)      require_arg "$1" "${2:-}"; POLICY_MODE="$2"; shift 2 ;;
            --allow-cidr)       ALLOW_CIDR=true; shift ;;
            -o|--output)        require_arg "$1" "${2:-}"; OUTPUT_DIR_OVERRIDE="$2"; shift 2 ;;
            -v|--verbose)       VERBOSE=true; shift ;;
            -*)                 err "Unknown option: $1"; exit 2 ;;
            *)
                if [[ -z "$TARGET" ]]; then
                    TARGET="$1"
                else
                    err "Unexpected extra target: $1"
                    exit 2
                fi
                shift
                ;;
        esac
    done

    [[ -n "$SLACK_OVERRIDE" ]] && SLACK_WEBHOOK="$SLACK_OVERRIDE"
    [[ -n "$WEBHOOK_OVERRIDE" ]] && GENERIC_WEBHOOK="$WEBHOOK_OVERRIDE"
    [[ -n "$RATE_OVERRIDE" ]] && NAABU_RATE="$RATE_OVERRIDE"

    if $USE_BURP; then
        PROXY="$BURP_PROXY"
        warn "Burp mode enabled; web tooling will use $BURP_PROXY"
    fi

    if [[ -z "$TARGET" && -z "$TARGETS_FILE" ]]; then
        err "Provide a target or -f <targets-file>"
        echo
        show_help
        exit 2
    fi
}

resolve_existing_path() {
    local path="$1"
    if command -v realpath &>/dev/null; then
        realpath "$path"
    elif command -v readlink &>/dev/null; then
        readlink -f "$path"
    else
        return 1
    fi
}

validate_program_flags() {
    local programs_dir program_file programs_real program_real rel slug_lower

    if [[ -z "$PROGRAM_SLUG" ]]; then
        [[ -z "$POLICY_MODE" ]] || { err "--policy-mode requires --program"; exit 2; }
        return 0
    fi

    slug_lower="${PROGRAM_SLUG,,}"
    if [[ -z "$PROGRAM_SLUG" || ! "$PROGRAM_SLUG" =~ ^[a-z0-9][a-z0-9_-]{0,62}$ ]] || [ "$PROGRAM_SLUG" != "$slug_lower" ]; then
        err "--program requires a lowercase slug matching ^[a-z0-9][a-z0-9_-]{0,62}$"
        exit 2
    fi
    if [[ "$PROGRAM_SLUG" == "_examples" || "$PROGRAM_SLUG" == "_schema" ]]; then
        err "--program cannot use reserved program directory: $PROGRAM_SLUG"
        exit 2
    fi
    if [[ "$PROGRAM_SLUG" == *"/"* || "$PROGRAM_SLUG" == *"\\"* || "$PROGRAM_SLUG" == *".."* || "$PROGRAM_SLUG" =~ [[:space:][:cntrl:]] || "$PROGRAM_SLUG" == .* || "$PROGRAM_SLUG" == -* ]]; then
        err "--program must be a slug, not a path-like value"
        exit 2
    fi
    if $SKIP_SCOPE_CHECK; then
        err "--program is incompatible with --skip-scope-check"
        exit 2
    fi
    if [[ -z "$POLICY_MODE" ]]; then
        err "--program requires --policy-mode {dry-run|planned|live}"
        exit 2
    fi
    if [ "$POLICY_MODE" != "${POLICY_MODE,,}" ]; then
        err "--policy-mode must be lowercase: dry-run, planned, or live"
        exit 2
    fi
    case "$POLICY_MODE" in
        dry-run|planned|live) ;;
        *) err "--policy-mode must be one of: dry-run, planned, live"; exit 2 ;;
    esac
    if [[ "$POLICY_MODE" == "dry-run" ]] && ! $DRY_RUN; then
        err "--policy-mode dry-run requires --dry-run; use --policy-mode planned or --policy-mode live for execution"
        exit 2
    fi

    programs_dir="$HACKLAB/programs"
    program_file="$programs_dir/$PROGRAM_SLUG/scope.json"

    [[ -d "$programs_dir" ]] || { err "--program scope directory missing: $programs_dir"; exit 1; }
    [[ -e "$program_file" ]] || { err "--program scope file missing: $program_file"; exit 1; }
    [[ -f "$program_file" ]] || { err "--program scope path is not a regular file: $program_file"; exit 1; }
    [[ -r "$program_file" ]] || { err "--program scope file is not readable: $program_file"; exit 1; }

    programs_real="$(resolve_existing_path "$programs_dir")" || { err "cannot resolve programs directory: $programs_dir"; exit 1; }
    program_real="$(resolve_existing_path "$program_file")" || { err "cannot resolve program scope file: $program_file"; exit 1; }
    case "$program_real" in
        "$programs_real"/*) ;;
        *) err "--program scope file resolves outside $programs_dir"; exit 1 ;;
    esac

    rel="${program_real#"$programs_real"/}"
    if [ "$rel" != "$PROGRAM_SLUG/scope.json" ]; then
        err "--program scope file must resolve exactly to programs/$PROGRAM_SLUG/scope.json"
        exit 1
    fi
    case "$rel" in
        _examples/*|_schema/*)
            err "--program scope file cannot resolve under programs/_examples or programs/_schema"
            exit 1
            ;;
    esac

    PROGRAM_SCOPE_FILE="$program_real"

}

validate_config() {
    if [[ "$REQUIRE_SCOPE_CHECK" == "false" ]]; then
        err "REQUIRE_SCOPE_CHECK=false is refused. Scope checks are mandatory."
        exit 1
    fi
    if [[ "$REQUIRE_SCOPE_CHECK" != "true" ]]; then
        err "REQUIRE_SCOPE_CHECK must be exactly true; got '$REQUIRE_SCOPE_CHECK'"
        exit 1
    fi
    case "$RECON_PROFILE" in
        live-low-speed|lab-aggressive) ;;
        *) err "RECON_PROFILE must be live-low-speed or lab-aggressive; got '$RECON_PROFILE'"; exit 1 ;;
    esac
    if [[ "$RECON_PROFILE" == "live-low-speed" && "$INTENSITY" == "full" && "$LIVE_ALLOW_FULL_PROFILE" != "true" ]]; then
        err "--full is refused under RECON_PROFILE=live-low-speed unless LIVE_ALLOW_FULL_PROFILE=true and program scope allows the technique"
        exit 1
    fi
}

validate_runtime_flags() {
    validate_program_flags

    if $SKIP_SCOPE_CHECK; then
        if [[ -z "${SCOPE_OVERRIDE_TOKEN:-}" || -z "${SCOPE_OVERRIDE_CONFIRM:-}" ]]; then
            err "--skip-scope-check requires SCOPE_OVERRIDE_TOKEN and SCOPE_OVERRIDE_CONFIRM"
            exit 1
        fi
        if [[ "$SCOPE_OVERRIDE_TOKEN" != "$SCOPE_OVERRIDE_CONFIRM" ]]; then
            err "--skip-scope-check override token mismatch"
            exit 1
        fi
        DRY_RUN=true
        warn "--skip-scope-check accepted only for dry-run; network stages will not execute"
    fi
}

audit_log() {
    local target="$1" event="$2" reason="${3:-}"
    $AUDIT_LOG || return 0
    mkdir -p "$(dirname "$AUDIT_LOG_FILE")"
    printf '%s | user=%s | target=%s | event=%s | intensity=%s | dry_run=%s | reason=%s\n' \
        "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        "${USER:-${USERNAME:-unknown}}" "$target" "$event" "$INTENSITY" "$DRY_RUN" "$reason" \
        >> "$AUDIT_LOG_FILE"
}

detect_target_type() {
    local t="$1"
    if [[ "$t" =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}/[0-9]{1,2}$ ]]; then
        echo "cidr"
    elif [[ "$t" =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]]; then
        echo "ip"
    elif [[ "$t" == "localhost" ]]; then
        echo "local"
    elif [[ "$t" =~ ^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)+$ ]]; then
        echo "domain"
    else
        echo "unknown"
    fi
}

valid_ipv4() {
    local ip="$1" IFS=. a b c d
    [[ "$ip" =~ ^[0-9]{1,3}(\.[0-9]{1,3}){3}$ ]] || return 1
    read -r a b c d <<< "$ip"
    for octet in "$a" "$b" "$c" "$d"; do
        [[ "$octet" =~ ^[0-9]+$ ]] || return 1
        (( 10#$octet >= 0 && 10#$octet <= 255 )) || return 1
    done
    return 0
}

valid_cidr() {
    local cidr="$1" ip bits
    [[ "$cidr" == */* ]] || return 1
    ip="${cidr%/*}"
    bits="${cidr#*/}"
    valid_ipv4 "$ip" || return 1
    [[ "$bits" =~ ^[0-9]+$ ]] || return 1
    (( bits >= 0 && bits <= 32 )) || return 1
}

valid_domain() {
    local host="$1"
    [[ ${#host} -le 253 ]] || return 1
    [[ "$host" =~ ^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)+$ ]] || return 1
}

valid_scope_entry() {
    local entry="$1"
    if [[ "$entry" == \*.* ]]; then
        valid_domain "${entry#*.}"
    else
        case "$(detect_target_type "$entry")" in
            ip) valid_ipv4 "$entry" ;;
            cidr) valid_cidr "$entry" ;;
            local) [[ "$entry" == "localhost" ]] ;;
            domain) valid_domain "$entry" ;;
            *) return 1 ;;
        esac
    fi
}

ip_to_dec() {
    local IFS=. a b c d
    read -r a b c d <<< "$1"
    valid_ipv4 "$1" || return 1
    echo $(( (10#$a << 24) + (10#$b << 16) + (10#$c << 8) + 10#$d ))
}

ip_in_cidr() {
    local ip="$1" cidr="$2" ip_dec cidr_ip cidr_bits cidr_dec mask
    valid_ipv4 "$ip" || return 1
    valid_cidr "$cidr" || return 1
    ip_dec=$(ip_to_dec "$ip") || return 1
    cidr_ip="${cidr%/*}"
    cidr_bits="${cidr#*/}"
    cidr_dec=$(ip_to_dec "$cidr_ip") || return 1
    mask=$(( 0xFFFFFFFF << (32 - cidr_bits) & 0xFFFFFFFF ))
    [[ $((ip_dec & mask)) -eq $((cidr_dec & mask)) ]]
}

parse_target() {
    local raw="$1" mode="${2:-auto}" t scheme rest host port type
    SAFE_TARGET_VALUE=""
    SAFE_TARGET_HOST=""
    SAFE_TARGET_REASON=""

    t="$(trim "$raw")"
    [[ -n "$t" ]] || { SAFE_TARGET_REASON="empty target"; return 1; }
    [[ "$t" != -* ]] || { SAFE_TARGET_REASON="target starts with '-'"; return 1; }
    [[ ! "$t" =~ [[:space:][:cntrl:]] ]] || { SAFE_TARGET_REASON="target contains whitespace/control characters"; return 1; }
    [[ ! "$t" =~ [\;\|\&\`\<\>\$\\] ]] || { SAFE_TARGET_REASON="target contains shell metacharacters"; return 1; }

    if [[ "$t" =~ ^https?:// ]]; then
        [[ "$mode" != "host" ]] || { SAFE_TARGET_REASON="URL not allowed in host-only context"; return 1; }
        scheme="${t%%://*}"
        rest="${t#*://}"
        rest="${rest%%/*}"
        rest="${rest%%\?*}"
        rest="${rest%%#*}"
        [[ "$rest" != *"@"* ]] || { SAFE_TARGET_REASON="URL userinfo is not allowed"; return 1; }
        if [[ "$rest" == \[*\]* ]]; then
            SAFE_TARGET_REASON="IPv6 literals are not supported by this guard"
            return 1
        fi
        host="${rest%%:*}"
        port=""
        if [[ "$rest" == *:* ]]; then
            port="${rest##*:}"
            [[ "$port" =~ ^[0-9]+$ ]] && (( port >= 1 && port <= 65535 )) || {
                SAFE_TARGET_REASON="URL port is malformed"
                return 1
            }
        fi
        host="${host,,}"
        type="$(detect_target_type "$host")"
        [[ "$type" == "ip" || "$type" == "domain" || "$type" == "local" ]] || { SAFE_TARGET_REASON="URL host is malformed"; return 1; }
        [[ "$type" != "ip" ]] || valid_ipv4 "$host" || { SAFE_TARGET_REASON="URL host IP is malformed"; return 1; }
        [[ "$type" != "domain" ]] || valid_domain "$host" || { SAFE_TARGET_REASON="URL host domain is malformed"; return 1; }
        [[ "$type" != "local" || "$host" == "localhost" ]] || { SAFE_TARGET_REASON="URL local host is malformed"; return 1; }
        SAFE_TARGET_HOST="$host"
        SAFE_TARGET_VALUE="${scheme}://${host}${port:+:$port}"
        return 0
    fi

    [[ "$mode" != "url" ]] || { SAFE_TARGET_REASON="expected URL"; return 1; }
    host="${t,,}"
    type="$(detect_target_type "$host")"
    case "$type" in
        ip) valid_ipv4 "$host" || { SAFE_TARGET_REASON="IP is malformed"; return 1; } ;;
        cidr) valid_cidr "$host" || { SAFE_TARGET_REASON="CIDR is malformed"; return 1; } ;;
        local) [[ "$host" == "localhost" ]] || { SAFE_TARGET_REASON="local host is malformed"; return 1; } ;;
        domain) valid_domain "$host" || { SAFE_TARGET_REASON="domain is malformed"; return 1; } ;;
        *) SAFE_TARGET_REASON="target is not a supported IP, CIDR, domain, or HTTP(S) URL"; return 1 ;;
    esac
    SAFE_TARGET_HOST="$host"
    SAFE_TARGET_VALUE="$host"
    return 0
}

validate_scope_file() {
    local scope_file="$1" line entry count=0 line_no=0
    [[ -f "$scope_file" ]] || { SAFE_TARGET_REASON="scope file missing: $scope_file"; return 1; }
    [[ -r "$scope_file" ]] || { SAFE_TARGET_REASON="scope file unreadable: $scope_file"; return 1; }

    while IFS= read -r line || [[ -n "$line" ]]; do
        line_no=$((line_no + 1))
        entry="${line%%#*}"
        entry="$(trim "$entry")"
        [[ -z "$entry" ]] && continue
        entry="${entry,,}"
        if ! valid_scope_entry "$entry"; then
            SAFE_TARGET_REASON="unparseable scope entry at ${scope_file}:${line_no}: $entry"
            return 1
        fi
        count=$((count + 1))
    done < "$scope_file"

    (( count > 0 )) || { SAFE_TARGET_REASON="scope file has no usable entries: $scope_file"; return 1; }
    return 0
}

scope_match() {
    local host="$1" scope_file="$2" line entry base
    while IFS= read -r line || [[ -n "$line" ]]; do
        entry="${line%%#*}"
        entry="$(trim "$entry")"
        [[ -z "$entry" ]] && continue
        entry="${entry,,}"

        [[ "$host" == "$entry" ]] && return 0

        if [[ "$entry" == \*.* ]]; then
            base="${entry#*.}"
            [[ "$host" == "$base" || "$host" == *".$base" ]] && return 0
        elif [[ "$entry" == */* ]]; then
            ip_in_cidr "$host" "$entry" && return 0
        fi
    done < "$scope_file"
    return 1
}

safe_target() {
    local candidate="$1" context="${2:-target}" mode="${3:-auto}"
    if ! parse_target "$candidate" "$mode"; then
        warn "safe_target FAIL context=$context target=$candidate reason=$SAFE_TARGET_REASON"
        audit_log "$candidate" "SAFE_TARGET_FAIL" "$context: $SAFE_TARGET_REASON"
        return 1
    fi

    if $SKIP_SCOPE_CHECK; then
        SAFE_TARGET_REASON="scope override token accepted; dry-run only"
        warn "safe_target PASS context=$context target=$SAFE_TARGET_VALUE reason=$SAFE_TARGET_REASON"
        audit_log "$SAFE_TARGET_VALUE" "SAFE_TARGET_OVERRIDE_DRY_RUN" "$context: $SAFE_TARGET_REASON"
        return 0
    fi

    if [[ "$SCOPE_FILE_VALIDATED" != "$SCOPE_FILE" ]]; then
        if ! validate_scope_file "$SCOPE_FILE"; then
            err "safe_target FAIL context=$context target=$SAFE_TARGET_VALUE reason=$SAFE_TARGET_REASON"
            audit_log "$SAFE_TARGET_VALUE" "SAFE_TARGET_FAIL" "$context: $SAFE_TARGET_REASON"
            return 1
        fi
        SCOPE_FILE_VALIDATED="$SCOPE_FILE"
    fi

    if scope_match "$SAFE_TARGET_HOST" "$SCOPE_FILE"; then
        SAFE_TARGET_REASON="in scope"
        ok "safe_target PASS context=$context target=$SAFE_TARGET_VALUE reason=$SAFE_TARGET_REASON"
        audit_log "$SAFE_TARGET_VALUE" "SAFE_TARGET_OK" "$context: $SAFE_TARGET_REASON"
        return 0
    fi

    SAFE_TARGET_REASON="not in scope"
    err "safe_target FAIL context=$context target=$SAFE_TARGET_VALUE reason=$SAFE_TARGET_REASON"
    audit_log "$SAFE_TARGET_VALUE" "SAFE_TARGET_REJECTED" "$context: $SAFE_TARGET_REASON"
    return 1
}


shell_unquote_policy_value() {
    local value="$1"
    if [[ "$value" == "''" ]]; then
        printf ''
    elif [[ "$value" == "'"*"'" && "$value" == *"'" ]]; then
        value="${value:1:${#value}-2}"
        value="${value//"'\\''"/"'"}"
        printf '%s' "$value"
    else
        printf '%s' "$value"
    fi
}

select_policy_python() {
    local candidate
    for candidate in python3 python; do
        if command -v "$candidate" &>/dev/null && env -u PYTHONIOENCODING -u PYTHONUTF8 "$candidate" -I --version &>/dev/null; then
            printf '%s' "$candidate"
            return 0
        fi
    done
    err "program policy mode requires runnable python3 or python"
    return 1
}


normalize_policy_timeout() {
    local raw="${PROGRAM_POLICY_TIMEOUT_SECS:-15}"
    if [[ ! "$raw" =~ ^[1-9][0-9]?$ ]]; then
        return 1
    fi
    if (( 10#$raw > 60 )); then
        return 1
    fi
    printf '%d' "$((10#$raw))"
}

policy_validate_artifact() {
    local py="$1" artifact="$2" artifact_dir="$3" target="$4" stage="$5" technique="$6" mode="$7" audit_event="$8" program_hash="$9" global_hash="${10}" decided_at="${11}" program_file="${12}" global_scope_file="${13}"
    env -u PYTHONIOENCODING -u PYTHONUTF8 "$py" -I - "$artifact" "$artifact_dir" "$target" "$stage" "$technique" "$mode" "$audit_event" "$program_hash" "$global_hash" "$decided_at" "$program_file" "$global_scope_file" <<'PY'
import hashlib
import json
import os
import re
import sys
from pathlib import Path

artifact_arg, dir_arg, target, stage, technique, mode, audit_event, program_hash, global_hash, decided_at, program_file_arg, global_scope_arg = sys.argv[1:13]
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

try:
    artifact = Path(artifact_arg).resolve(strict=True)
    artifact_dir = Path(dir_arg).resolve(strict=True)
    program_file = Path(program_file_arg).resolve(strict=True)
    global_scope_file = Path(global_scope_arg).resolve(strict=True)
except Exception as exc:
    print(f"path resolution failed: {exc}")
    raise SystemExit(1)

try:
    common = os.path.commonpath([str(artifact), str(artifact_dir)])
except ValueError as exc:
    print(f"artifact path is on a different drive/tree: {exc}")
    raise SystemExit(1)
if common != str(artifact_dir):
    print(f"artifact outside policy directory: {artifact}")
    raise SystemExit(1)
try:
    with artifact.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
except Exception as exc:
    print(f"artifact JSON parse failed: {exc}")
    raise SystemExit(1)
errors = []
try:
    actual_program_hash = hashlib.sha256(program_file.read_bytes()).hexdigest()
    actual_global_hash = hashlib.sha256(global_scope_file.read_bytes()).hexdigest()
except Exception as exc:
    errors.append(f"policy source hash calculation failed: {exc}")
    actual_program_hash = ""
    actual_global_hash = ""
if audit_event != "PROGRAM_POLICY_ALLOW":
    errors.append("boundary output audit_event mismatch")
if not HASH_RE.fullmatch(program_hash):
    errors.append("boundary output program hash invalid")
elif program_hash != actual_program_hash:
    errors.append("boundary output program hash source mismatch")
if not HASH_RE.fullmatch(global_hash):
    errors.append("boundary output global hash invalid")
elif global_hash != actual_global_hash:
    errors.append("boundary output global hash source mismatch")
if not UTC_RE.fullmatch(decided_at):
    errors.append("boundary output decided_at invalid")
if data.get("schema_version") != "policy_boundary/1.0":
    errors.append("schema_version mismatch")
boundary = data.get("boundary")
if not isinstance(boundary, dict) or boundary.get("status") != "allow":
    errors.append("boundary.status mismatch")
else:
    if boundary.get("audit_event") != "PROGRAM_POLICY_ALLOW":
        errors.append("boundary.audit_event mismatch")
    if boundary.get("audit_event") != audit_event:
        errors.append("boundary.audit_event output mismatch")
request = data.get("request")
if not isinstance(request, dict):
    errors.append("request object missing")
else:
    expected = {
        "target": target,
        "stage": stage,
        "technique": technique,
        "mode": mode,
    }
    for key, expected_value in expected.items():
        if request.get(key) != expected_value:
            errors.append(f"request.{key} mismatch")
decision = data.get("decision")
if not isinstance(decision, dict):
    errors.append("decision object missing")
else:
    expected_decision = {
        "verdict": "allow",
        "target": target,
        "technique": technique,
        "mode": mode,
        "audit_event": audit_event,
        "program_file_sha256": program_hash,
        "global_scope_sha256": global_hash,
        "decided_at_utc": decided_at,
    }
    for key, expected_value in expected_decision.items():
        if decision.get(key) != expected_value:
            errors.append(f"decision.{key} mismatch")
    if decision.get("audit_event") != "PROGRAM_POLICY_ALLOW":
        errors.append("decision.audit_event allow mismatch")
if errors:
    print("; ".join(errors))
    raise SystemExit(1)
PY
}

policy_decide() {
    local stage="$1" technique="$2" target="$3" mode="${4:-$POLICY_MODE}"
    local boundary_script py timeout status_file line key value validation_message force_policy_args=()

    POLICY_VERDICT="error"
    POLICY_AUDIT_EVENT="PROGRAM_POLICY_BOUNDARY_ERROR"
    POLICY_ARTIFACT=""
    POLICY_DENY_REASON_CODES=""
    POLICY_MESSAGE="policy boundary did not run"
    POLICY_PROGRAM_SHA256=""
    POLICY_GLOBAL_SHA256=""
    POLICY_DECIDED_AT_UTC=""

    [[ -n "$PROGRAM_SLUG" ]] || return 0
    [[ -n "$POLICY_ARTIFACT_DIR" ]] || { POLICY_MESSAGE="policy artifact directory is not initialized"; audit_log "$target" "$POLICY_AUDIT_EVENT" "$stage: $POLICY_MESSAGE"; policy_note_boundary_error; return 1; }
    boundary_script="$SCRIPT_DIR/scripts/program_policy_boundary.py"
    if [[ ! -f "$boundary_script" ]]; then
        POLICY_MESSAGE="policy boundary script missing: $boundary_script"
        audit_log "$target" "$POLICY_AUDIT_EVENT" "$stage: $POLICY_MESSAGE"
        policy_note_boundary_error
        return 1
    fi
    py="$(select_policy_python)" || { POLICY_MESSAGE="policy python unavailable"; audit_log "$target" "$POLICY_AUDIT_EVENT" "$stage: $POLICY_MESSAGE"; policy_note_boundary_error; return 1; }
    if ! timeout="$(normalize_policy_timeout)"; then
        POLICY_MESSAGE="invalid program policy timeout: ${PROGRAM_POLICY_TIMEOUT_SECS:-15} (must be integer 1..60)"
        audit_log "$target" "$POLICY_AUDIT_EVENT" "$stage: $POLICY_MESSAGE"
        warn "policy DENY stage=$stage target=$target technique=$technique status=error codes=INVALID_POLICY_TIMEOUT message=$POLICY_MESSAGE"
        policy_note_boundary_error
        return 1
    fi
    if [[ "$(detect_target_type "$target")" == "cidr" && "$ALLOW_CIDR" != "true" ]]; then
        force_policy_args=(--force-deny-code "CIDR_REQUIRES_ALLOW_CIDR" --force-deny-message "CIDR targets require --allow-cidr in program policy mode")
    fi
    status_file="$(mktemp "${POLICY_ARTIFACT_DIR}/.policy_status.XXXXXX")" || return 1

    if ! env -u PYTHONIOENCODING -u PYTHONUTF8 "$py" -I "$boundary_script" \
        --stage "$stage" \
        --program "$PROGRAM_SCOPE_FILE" \
        --global-scope "$SCOPE_FILE" \
        --target "$target" \
        --technique "$technique" \
        --mode "$mode" \
        --artifact-dir "$POLICY_ARTIFACT_DIR" \
        --timeout-seconds "$timeout" \
        "${force_policy_args[@]}" > "$status_file" 2>>"$RUN_LOG"; then
        :
    fi

    while IFS= read -r line || [[ -n "$line" ]]; do
        line="${line%$'\r'}"
        [[ -z "$line" ]] && continue
        key="${line%%=*}"
        value="${line#*=}"
        value="$(shell_unquote_policy_value "$value")" || continue
        case "$key" in
            POLICY_BOUNDARY_STATUS) POLICY_BOUNDARY_STATUS="$value" ;;
            POLICY_BOUNDARY_AUDIT_EVENT) POLICY_BOUNDARY_AUDIT_EVENT="$value" ;;
            POLICY_BOUNDARY_ARTIFACT) POLICY_BOUNDARY_ARTIFACT="$value" ;;
            POLICY_BOUNDARY_DENY_REASON_CODES) POLICY_BOUNDARY_DENY_REASON_CODES="$value" ;;
            POLICY_BOUNDARY_MESSAGE) POLICY_BOUNDARY_MESSAGE="$value" ;;
            POLICY_BOUNDARY_PROGRAM_HASH) POLICY_BOUNDARY_PROGRAM_HASH="$value" ;;
            POLICY_BOUNDARY_GLOBAL_HASH) POLICY_BOUNDARY_GLOBAL_HASH="$value" ;;
            POLICY_BOUNDARY_DECIDED_AT_UTC) POLICY_BOUNDARY_DECIDED_AT_UTC="$value" ;;
        esac
    done < "$status_file"
    rm -f "$status_file"

    POLICY_VERDICT="${POLICY_BOUNDARY_STATUS:-error}"
    POLICY_AUDIT_EVENT="${POLICY_BOUNDARY_AUDIT_EVENT:-PROGRAM_POLICY_BOUNDARY_ERROR}"
    POLICY_ARTIFACT="${POLICY_BOUNDARY_ARTIFACT:-}"
    POLICY_ARTIFACT="${POLICY_ARTIFACT//\\//}"
    POLICY_DENY_REASON_CODES="${POLICY_BOUNDARY_DENY_REASON_CODES:-}"
    POLICY_MESSAGE="${POLICY_BOUNDARY_MESSAGE:-policy boundary status missing}"
    POLICY_PROGRAM_SHA256="${POLICY_BOUNDARY_PROGRAM_HASH:-}"
    POLICY_GLOBAL_SHA256="${POLICY_BOUNDARY_GLOBAL_HASH:-}"
    POLICY_DECIDED_AT_UTC="${POLICY_BOUNDARY_DECIDED_AT_UTC:-}"
    unset POLICY_BOUNDARY_STATUS POLICY_BOUNDARY_AUDIT_EVENT POLICY_BOUNDARY_ARTIFACT POLICY_BOUNDARY_DENY_REASON_CODES POLICY_BOUNDARY_MESSAGE POLICY_BOUNDARY_PROGRAM_HASH POLICY_BOUNDARY_GLOBAL_HASH POLICY_BOUNDARY_DECIDED_AT_UTC

    if [[ "$POLICY_VERDICT" == "allow" && -f "$POLICY_ARTIFACT" ]]; then
        if validation_message="$(policy_validate_artifact "$py" "$POLICY_ARTIFACT" "$POLICY_ARTIFACT_DIR" "$target" "$stage" "$technique" "$mode" "$POLICY_AUDIT_EVENT" "$POLICY_PROGRAM_SHA256" "$POLICY_GLOBAL_SHA256" "$POLICY_DECIDED_AT_UTC" "$PROGRAM_SCOPE_FILE" "$SCOPE_FILE" 2>>"$RUN_LOG")"; then
            audit_log "$target" "$POLICY_AUDIT_EVENT" "$stage: technique=$technique mode=$mode artifact=$POLICY_ARTIFACT program_sha256=${POLICY_PROGRAM_SHA256:-unknown} global_sha256=${POLICY_GLOBAL_SHA256:-unknown} decided_at=${POLICY_DECIDED_AT_UTC:-unknown}"
            ok "policy PASS stage=$stage target=$target technique=$technique artifact=$POLICY_ARTIFACT"
            return 0
        fi
        POLICY_VERDICT="error"
        POLICY_AUDIT_EVENT="PROGRAM_POLICY_BOUNDARY_ERROR"
        POLICY_DENY_REASON_CODES="ARTIFACT_VALIDATION_FAILED"
        POLICY_MESSAGE="policy artifact validation failed: ${validation_message:-unknown validation error}"
    fi

    [[ -n "$POLICY_ARTIFACT" && -f "$POLICY_ARTIFACT" ]] || POLICY_MESSAGE="$POLICY_MESSAGE; missing policy artifact"
    audit_log "$target" "$POLICY_AUDIT_EVENT" "$stage: technique=$technique mode=$mode status=${POLICY_VERDICT:-error} codes=${POLICY_DENY_REASON_CODES:-none} message=$POLICY_MESSAGE artifact=${POLICY_ARTIFACT:-none} program_sha256=${POLICY_PROGRAM_SHA256:-unknown} global_sha256=${POLICY_GLOBAL_SHA256:-unknown} decided_at=${POLICY_DECIDED_AT_UTC:-unknown}"
    warn "policy DENY stage=$stage target=$target technique=$technique status=${POLICY_VERDICT:-error} codes=${POLICY_DENY_REASON_CODES:-none} message=$POLICY_MESSAGE"
    policy_is_boundary_error && policy_note_boundary_error
    return 1
}

filter_safe_and_policy_targets() {
    local input="$1" output="$2" safe_dropped="$3" policy_dropped="$4" context="$5" mode="${6:-auto}" technique="$7"
    local line candidate kept=0 safe_drop_count=0 policy_drop_count=0 normalized
    : > "$output"
    : > "$safe_dropped"
    : > "$policy_dropped"

    if [[ ! -f "$input" ]]; then
        warn "safe/policy filter input missing for $context: $input"
        return 1
    fi

    while IFS= read -r line || [[ -n "$line" ]]; do
        candidate="${line%%#*}"
        candidate="$(trim "$candidate")"
        [[ -z "$candidate" ]] && continue
        if ! safe_target "$candidate" "$context" "$mode"; then
            printf '%s\t%s\n' "$candidate" "$SAFE_TARGET_REASON" >> "$safe_dropped"
            safe_drop_count=$((safe_drop_count + 1))
            continue
        fi
        normalized="$SAFE_TARGET_VALUE"
        if [[ -n "$PROGRAM_SLUG" ]] && ! policy_decide "$context" "$technique" "$normalized" "$POLICY_MODE"; then
            printf '%s\t%s\t%s\n' "$normalized" "${POLICY_DENY_REASON_CODES:-POLICY_DENY}" "$POLICY_MESSAGE" >> "$policy_dropped"
            policy_drop_count=$((policy_drop_count + 1))
            continue
        fi
        echo "$normalized" >> "$output"
        kept=$((kept + 1))
    done < "$input"

    sort -u -o "$output" "$output"
    sort -u -o "$safe_dropped" "$safe_dropped"
    sort -u -o "$policy_dropped" "$policy_dropped"
    kept=$(wc -l < "$output" 2>/dev/null || echo 0)
    safe_drop_count=$(wc -l < "$safe_dropped" 2>/dev/null || echo 0)
    policy_drop_count=$(wc -l < "$policy_dropped" 2>/dev/null || echo 0)
    info "safe/policy filter context=$context kept=$kept safe_dropped=$safe_drop_count policy_dropped=$policy_drop_count output=$output"
    return 0
}

filter_safe_targets() {
    local input="$1" output="$2" dropped="$3" context="$4" mode="${5:-auto}"
    local line candidate kept=0 dropped_count=0
    : > "$output"
    : > "$dropped"

    if [[ ! -f "$input" ]]; then
        warn "safe filter input missing for $context: $input"
        return 1
    fi

    while IFS= read -r line || [[ -n "$line" ]]; do
        candidate="${line%%#*}"
        candidate="$(trim "$candidate")"
        [[ -z "$candidate" ]] && continue
        if safe_target "$candidate" "$context" "$mode"; then
            echo "$SAFE_TARGET_VALUE" >> "$output"
            kept=$((kept + 1))
        else
            printf '%s\t%s\n' "$candidate" "$SAFE_TARGET_REASON" >> "$dropped"
            dropped_count=$((dropped_count + 1))
        fi
    done < "$input"

    sort -u -o "$output" "$output"
    sort -u -o "$dropped" "$dropped"
    kept=$(wc -l < "$output" 2>/dev/null || echo 0)
    dropped_count=$(wc -l < "$dropped" 2>/dev/null || echo 0)
    info "safe filter context=$context kept=$kept dropped=$dropped_count output=$output dropped_file=$dropped"
    return 0
}

filter_safe_ports() {
    local input="$1" output="$2" dropped="$3" context="$4"
    local line host port kept=0 dropped_count=0
    : > "$output"
    : > "$dropped"
    [[ -f "$input" ]] || { warn "ports input missing for $context: $input"; return 1; }

    while IFS=: read -r host port _rest || [[ -n "${host:-}" ]]; do
        host="$(trim "${host:-}")"
        port="$(trim "${port:-}")"
        if [[ -z "$host" || -z "$port" || -n "${_rest:-}" || ! "$port" =~ ^[0-9]+$ || "$port" -lt 1 || "$port" -gt 65535 ]]; then
            printf '%s:%s\tmalformed host:port\n' "$host" "$port" >> "$dropped"
            dropped_count=$((dropped_count + 1))
            continue
        fi
        if safe_target "$host" "$context" "host"; then
            printf '%s:%s\n' "$SAFE_TARGET_VALUE" "$port" >> "$output"
            kept=$((kept + 1))
        else
            printf '%s:%s\t%s\n' "$host" "$port" "$SAFE_TARGET_REASON" >> "$dropped"
            dropped_count=$((dropped_count + 1))
        fi
    done < "$input"

    sort -u -o "$output" "$output"
    sort -u -o "$dropped" "$dropped"
    info "safe ports context=$context kept=$kept dropped=$dropped_count output=$output dropped_file=$dropped"
    return 0
}

enum_subdomains() {
    local domain="$1" outdir="$2"
    title "Subdomain enumeration: $domain"
    local raw_file="$outdir/subdomains_raw.txt"
    local sub_file="$outdir/subdomains.txt"
    local dropped_file="$outdir/subdomains_dropped.txt"
    : > "$raw_file"

    if [[ -n "$PROGRAM_SLUG" ]] && ! policy_decide "enum_subdomains" "subdomain_enumeration" "$domain" "$POLICY_MODE"; then
        warn "program policy denied subdomain enumeration for $domain; falling back to apex-only path"
        echo "$domain" > "$raw_file"
        filter_safe_and_policy_targets "$raw_file" "$sub_file" "$dropped_file" "$outdir/subdomains_policy_dropped.txt" "domain_expansion" "host" "http_probe"
        ok "subdomains kept=$(wc -l < "$sub_file" 2>/dev/null || echo 0) dropped=$(wc -l < "$dropped_file" 2>/dev/null || echo 0) file=$sub_file"
        return
    fi

    if check_tool subfinder; then
        info "subfinder enumeration queued"
        if $DRY_RUN; then
            echo "DRY: subfinder -d $domain -t $SUBFINDER_THREADS -timeout $SUBFINDER_TIMEOUT -silent -o $outdir/.subfinder.tmp"
        else
            subfinder -d "$domain" -t "$SUBFINDER_THREADS" -timeout "$SUBFINDER_TIMEOUT" \
                -silent -o "$outdir/.subfinder.tmp" 2>>"$RUN_LOG" || true
            [[ -f "$outdir/.subfinder.tmp" ]] && cat "$outdir/.subfinder.tmp" >> "$raw_file"
        fi
    fi

    if $USE_CRT_SH && check_tool curl && check_tool jq; then
        info "crt.sh enumeration queued"
        if $DRY_RUN; then
            echo "DRY: curl -s https://crt.sh/?q=%25.$domain&output=json | jq ..."
        else
            curl -s "https://crt.sh/?q=%25.$domain&output=json" 2>/dev/null \
                | jq -r '.[].name_value' 2>/dev/null \
                | tr ',' '\n' | sed 's/\*\.//' \
                | grep -Ei "\.$domain\$|^$domain\$" \
                | sort -u >> "$raw_file" || true
        fi
    fi

    echo "$domain" >> "$raw_file"
    sort -u -o "$raw_file" "$raw_file"
    if [[ -n "$PROGRAM_SLUG" ]]; then
        filter_safe_and_policy_targets "$raw_file" "$sub_file" "$dropped_file" "$outdir/subdomains_policy_dropped.txt" "domain_expansion" "host" "subdomain_enumeration"
    else
        filter_safe_targets "$raw_file" "$sub_file" "$dropped_file" "domain_expansion" "host"
    fi

    local kept dropped
    kept=$(wc -l < "$sub_file" 2>/dev/null || echo 0)
    dropped=$(wc -l < "$dropped_file" 2>/dev/null || echo 0)
    ok "subdomains kept=$kept dropped=$dropped file=$sub_file"
}

find_live_hosts() {
    local input="$1" outdir="$2"
    title "Live host probe"
    local safe_input="$outdir/.find_live_hosts.safe_input.txt"
    local safe_dropped="$outdir/.find_live_hosts.dropped.txt"
    local live_raw="$outdir/.live_hosts_raw.txt"
    local live="$outdir/live_hosts.txt"

    if [[ -n "$PROGRAM_SLUG" ]]; then
        filter_safe_and_policy_targets "$input" "$safe_input" "$safe_dropped" "$outdir/.find_live_hosts.policy_dropped.txt" "find_live_hosts.input" "host" "http_probe"
    else
        filter_safe_targets "$input" "$safe_input" "$safe_dropped" "find_live_hosts.input" "host"
    fi
    [[ -s "$safe_input" ]] || { warn "no safe hosts for live probe"; : > "$live"; return; }

    if check_tool httpx; then
        info "httpx probe queued"
        if $DRY_RUN; then
            echo "DRY: httpx -l $safe_input -silent -no-color -o $live_raw -threads $HTTPX_THREADS -timeout $HTTPX_TIMEOUT"
            cp "$safe_input" "$live_raw"
        else
            httpx -l "$safe_input" -silent -no-color -o "$outdir/.httpx_raw.txt" \
                -threads "$HTTPX_THREADS" -timeout "$HTTPX_TIMEOUT" 2>>"$RUN_LOG" || true
            awk -F[/:] '{print $4}' "$outdir/.httpx_raw.txt" 2>/dev/null | sort -u > "$live_raw" || true
        fi
    fi

    if [[ ! -s "$live_raw" ]]; then
        if $DRY_RUN; then
            cp "$safe_input" "$live_raw"
        else
            warn "httpx produced no live hosts; falling back to ICMP for safe hosts only"
            while IFS= read -r host; do
                [[ -z "$host" ]] && continue
                if ping -c1 -W1 "$host" &>/dev/null; then
                    echo "$host" >> "$live_raw"
                fi
            done < "$safe_input"
        fi
    fi

    if [[ -n "$PROGRAM_SLUG" ]]; then
        filter_safe_and_policy_targets "$live_raw" "$live" "$outdir/live_hosts_dropped.txt" "$outdir/live_hosts_policy_dropped.txt" "find_live_hosts.output" "host" "http_probe"
    else
        filter_safe_targets "$live_raw" "$live" "$outdir/live_hosts_dropped.txt" "find_live_hosts.output" "host"
    fi
    ok "live hosts $(wc -l < "$live" 2>/dev/null || echo 0) file=$live"
}

port_scan() {
    local hosts_file="$1" outdir="$2"
    title "Port scan (naabu)"
    local safe_hosts="$outdir/.port_scan.safe_hosts.txt"
    local ports_file="$outdir/ports.txt"
    if [[ -n "$PROGRAM_SLUG" ]]; then
        filter_safe_and_policy_targets "$hosts_file" "$safe_hosts" "$outdir/.port_scan.dropped.txt" "$outdir/.port_scan.policy_dropped.txt" "port_scan.input" "host" "port_scan"
    else
        filter_safe_targets "$hosts_file" "$safe_hosts" "$outdir/.port_scan.dropped.txt" "port_scan.input" "host"
    fi
    [[ -s "$safe_hosts" ]] || { warn "no safe hosts for port scan"; : > "$ports_file"; return; }

    check_tool naabu || { warn "skipping port scan"; : > "$ports_file"; return; }

    local top_ports_arg
    case "$INTENSITY" in
        quick) top_ports_arg="-top-ports $NAABU_TOP_PORTS_QUICK" ;;
        aggressive|full) top_ports_arg="-p -" ;;
        *) top_ports_arg="-top-ports $NAABU_TOP_PORTS_NORMAL" ;;
    esac

    info "intensity=$INTENSITY rate=$NAABU_RATE"
    if $DRY_RUN; then
        echo "DRY: naabu -list $safe_hosts $top_ports_arg -rate $NAABU_RATE -o $ports_file"
        : > "$ports_file"
    else
        # shellcheck disable=SC2086
        naabu -list "$safe_hosts" $top_ports_arg \
            -rate "$NAABU_RATE" -timeout "$NAABU_TIMEOUT" \
            -silent -no-color -o "$outdir/.ports_raw.txt" 2>>"$RUN_LOG" || true
        filter_safe_ports "$outdir/.ports_raw.txt" "$ports_file" "$outdir/ports_dropped.txt" "port_scan.output"
    fi

    ok "ports $(wc -l < "$ports_file" 2>/dev/null || echo 0) file=$ports_file"
}

service_fingerprint() {
    local ports_file="$1" outdir="$2"
    title "Service fingerprint (nmap)"
    local nmap_dir="$outdir/nmap"
    local safe_ports="$outdir/.service_fingerprint.safe_ports.txt"
    mkdir -p "$nmap_dir"

    filter_safe_ports "$ports_file" "$safe_ports" "$outdir/.service_fingerprint.dropped.txt" "service_fingerprint.input"
    [[ -s "$safe_ports" ]] || { warn "no safe ports for nmap"; return; }
    check_tool nmap || { warn "skipping nmap"; return; }

    declare -A HOST_PORTS=()
    local host port
    while IFS=: read -r host port; do
        [[ -z "$host" || -z "$port" ]] && continue
        HOST_PORTS["$host"]+="$port,"
    done < "$safe_ports"

    for host in "${!HOST_PORTS[@]}"; do
        safe_target "$host" "service_fingerprint.host" "host" || continue
        if [[ -n "$PROGRAM_SLUG" ]] && ! policy_decide "service_fingerprint.host" "service_fingerprint" "$SAFE_TARGET_VALUE" "$POLICY_MODE"; then
            printf '%s\t%s\t%s\n' "$SAFE_TARGET_VALUE" "${POLICY_DENY_REASON_CODES:-POLICY_DENY}" "$POLICY_MESSAGE" >> "$outdir/.service_fingerprint.policy_dropped.txt"
            continue
        fi
        local ports="${HOST_PORTS[$host]%,}"
        local safe_host="${SAFE_TARGET_VALUE//\//_}"
        local nmap_base="$nmap_dir/$safe_host"
        info "nmap -> $host ports=$ports"
        if $DRY_RUN; then
            echo "DRY: nmap -sV -sC -p $ports $NMAP_TIMING --script=$NMAP_SCRIPTS --host-timeout=$NMAP_HOST_TIMEOUT -oA $nmap_base $host"
        else
            # shellcheck disable=SC2086
            nmap -sV -sC -p "$ports" $NMAP_TIMING \
                --script="$NMAP_SCRIPTS" \
                --host-timeout="$NMAP_HOST_TIMEOUT" \
                -oA "$nmap_base" "$host" >>"$RUN_LOG" 2>&1 || true
        fi
    done
}

web_probe() {
    local ports_file="$1" outdir="$2"
    title "Web probe (httpx)"
    local web_dir="$outdir/web"
    local safe_ports="$outdir/.web_probe.safe_ports.txt"
    local urls_file="$web_dir/urls.txt"
    local safe_urls="$web_dir/safe_urls.txt"
    mkdir -p "$web_dir"

    filter_safe_ports "$ports_file" "$safe_ports" "$outdir/.web_probe.dropped_ports.txt" "web_probe.input"
    [[ -s "$safe_ports" ]] || { warn "no safe ports for web probe"; : > "$web_dir/live_urls.txt"; return; }

    awk -F: '{print "http://"$1":"$2"\nhttps://"$1":"$2}' "$safe_ports" > "$urls_file"
    if [[ -n "$PROGRAM_SLUG" ]]; then
        filter_safe_and_policy_targets "$urls_file" "$safe_urls" "$web_dir/urls_dropped.txt" "$web_dir/urls_policy_dropped.txt" "web_probe.urls" "url" "http_probe"
    else
        filter_safe_targets "$urls_file" "$safe_urls" "$web_dir/urls_dropped.txt" "web_probe.urls" "url"
    fi
    [[ -s "$safe_urls" ]] || { warn "no safe URLs for web probe"; : > "$web_dir/live_urls.txt"; return; }

    check_tool httpx || { warn "skipping httpx"; return; }

    local proxy_arg=""
    [[ -n "$PROXY" ]] && proxy_arg="-proxy $PROXY"

    if $DRY_RUN; then
        echo "DRY: httpx -l $safe_urls $HTTPX_PROBES $proxy_arg -json -o $web_dir/httpx.json"
        cp "$safe_urls" "$web_dir/live_urls.txt"
    else
        # shellcheck disable=SC2086
        httpx -l "$safe_urls" $HTTPX_PROBES $proxy_arg \
            -threads "$HTTPX_THREADS" -timeout "$HTTPX_TIMEOUT" \
            -silent -no-color -json -o "$web_dir/httpx.json" 2>>"$RUN_LOG" || true
        jq -r '.url' "$web_dir/httpx.json" 2>/dev/null | sort -u > "$web_dir/.live_urls_raw.txt" || true
        filter_safe_targets "$web_dir/.live_urls_raw.txt" "$web_dir/live_urls.txt" "$web_dir/live_urls_dropped.txt" "web_probe.output" "url"
    fi

    ok "web URLs $(wc -l < "$web_dir/live_urls.txt" 2>/dev/null || echo 0) dir=$web_dir"
}

dir_bruteforce() {
    local web_dir="$1"
    title "Directory brute force (feroxbuster)"
    local live_urls="$web_dir/live_urls.txt"
    local safe_urls="$web_dir/.dir_bruteforce.safe_urls.txt"
    if [[ -n "$PROGRAM_SLUG" ]]; then
        filter_safe_and_policy_targets "$live_urls" "$safe_urls" "$web_dir/.dir_bruteforce.dropped.txt" "$web_dir/.dir_bruteforce.policy_dropped.txt" "dir_bruteforce.input" "url" "directory_bruteforce"
    else
        filter_safe_targets "$live_urls" "$safe_urls" "$web_dir/.dir_bruteforce.dropped.txt" "dir_bruteforce.input" "url"
    fi
    [[ -s "$safe_urls" ]] || { warn "no safe web URLs for feroxbuster"; return; }

    check_tool feroxbuster || { warn "skipping feroxbuster"; return; }

    local wordlist="$FEROX_WORDLIST"
    [[ -f "$wordlist" ]] || wordlist="$FEROX_WORDLIST_FALLBACK"
    [[ -f "$wordlist" ]] || { warn "wordlist missing; skipping feroxbuster"; return; }

    local proxy_arg=""
    [[ -n "$PROXY" ]] && proxy_arg="--proxy $PROXY"

    local url safe_name outfile
    while IFS= read -r url; do
        [[ -z "$url" ]] && continue
        safe_target "$url" "dir_bruteforce.url" "url" || continue
        if [[ -n "$PROGRAM_SLUG" ]] && ! policy_decide "dir_bruteforce.url" "directory_bruteforce" "$SAFE_TARGET_VALUE" "$POLICY_MODE"; then
            printf '%s\t%s\t%s\n' "$SAFE_TARGET_VALUE" "${POLICY_DENY_REASON_CODES:-POLICY_DENY}" "$POLICY_MESSAGE" >> "$web_dir/.dir_bruteforce.url_policy_dropped.txt"
            continue
        fi
        safe_name=$(echo "$SAFE_TARGET_VALUE" | sed 's|https\?://||; s|[:/]|_|g')
        outfile="$web_dir/ferox_${safe_name}.txt"
        info "ferox -> $SAFE_TARGET_VALUE"
        if $DRY_RUN; then
            echo "DRY: feroxbuster -u $SAFE_TARGET_VALUE -w $wordlist -d $FEROX_DEPTH -t $FEROX_THREADS -x $FEROX_EXTENSIONS -s $FEROX_STATUS_CODES $proxy_arg -o $outfile"
        else
            # shellcheck disable=SC2086
            feroxbuster -u "$SAFE_TARGET_VALUE" -w "$wordlist" \
                -d "$FEROX_DEPTH" -t "$FEROX_THREADS" \
                -x "$FEROX_EXTENSIONS" -s "$FEROX_STATUS_CODES" \
                --no-state --silent $proxy_arg \
                -o "$outfile" 2>>"$RUN_LOG" || true
        fi
    done < "$safe_urls"
}

vuln_scan() {
    local web_dir="$1" outdir="$2"
    title "Vulnerability scan (nuclei)"
    local live_urls="$web_dir/live_urls.txt"
    local safe_urls="$web_dir/.vuln_scan.safe_urls.txt"
    local vuln_technique="vulnerability_scan_passive"
    case "$INTENSITY" in
        aggressive|full) vuln_technique="vulnerability_scan_active" ;;
    esac
    if [[ -n "$PROGRAM_SLUG" ]]; then
        filter_safe_and_policy_targets "$live_urls" "$safe_urls" "$web_dir/.vuln_scan.dropped.txt" "$web_dir/.vuln_scan.policy_dropped.txt" "vuln_scan.input" "url" "$vuln_technique"
    else
        filter_safe_targets "$live_urls" "$safe_urls" "$web_dir/.vuln_scan.dropped.txt" "vuln_scan.input" "url"
    fi
    [[ -s "$safe_urls" ]] || { warn "no safe URLs for nuclei"; return; }

    check_tool nuclei || { warn "skipping nuclei"; return; }

    local severity exclude_tags=""
    case "$INTENSITY" in
        quick) severity="info,low" ;;
        aggressive) severity="$NUCLEI_SEVERITY_AGGRESSIVE"; exclude_tags="$NUCLEI_EXCLUDE_TAGS" ;;
        full) severity="$NUCLEI_SEVERITY_AGGRESSIVE"; exclude_tags="$NUCLEI_EXCLUDE_TAGS_FULL" ;;
        *) severity="$NUCLEI_SEVERITY_NORMAL"; exclude_tags="$NUCLEI_EXCLUDE_TAGS" ;;
    esac

    local exclude_arg=""
    [[ -n "$exclude_tags" ]] && exclude_arg="-exclude-tags $exclude_tags"
    local proxy_arg=""
    [[ -n "$PROXY" ]] && proxy_arg="-proxy $PROXY"

    local nuclei_out="$outdir/nuclei.jsonl"
    info "intensity=$INTENSITY severity=$severity"
    if $DRY_RUN; then
        echo "DRY: nuclei -l $safe_urls -severity $severity $exclude_arg $proxy_arg -rl $NUCLEI_RATE_LIMIT -c $NUCLEI_CONCURRENCY -jsonl -o $nuclei_out"
        : > "$nuclei_out"
    else
        # shellcheck disable=SC2086
        nuclei -l "$safe_urls" \
            -severity "$severity" $exclude_arg $proxy_arg \
            -rl "$NUCLEI_RATE_LIMIT" -c "$NUCLEI_CONCURRENCY" \
            -timeout "$NUCLEI_TIMEOUT" \
            -silent -no-color -jsonl -o "$nuclei_out" 2>>"$RUN_LOG" || true
    fi

    local cnt=0
    [[ -f "$nuclei_out" ]] && cnt=$(wc -l < "$nuclei_out")
    ok "nuclei triage findings=$cnt file=$nuclei_out"

    if [[ -s "$nuclei_out" ]] && command -v jq &>/dev/null; then
        local findings_md="$outdir/nuclei_findings.md"
        {
            echo "# Nuclei Findings"
            echo
            echo "| Severity | Template | Host | Matcher |"
            echo "|---|---|---|---|"
            jq -r '"| " + (."info"."severity"|ascii_upcase) + " | " + ."template-id" + " | " + ."host" + " | " + ((."matcher-name" // "-")) + " |"' \
                "$nuclei_out" 2>/dev/null | sort
        } > "$findings_md"
    fi
}

generate_summary() {
    local target="$1" outdir="$2"
    title "Generate summary.md"
    local summary="$outdir/summary.md"

    local sub_count=0 dropped_sub_count=0 live_count=0 port_count=0 finding_count=0
    [[ -f "$outdir/subdomains.txt" ]] && sub_count=$(wc -l < "$outdir/subdomains.txt")
    [[ -f "$outdir/subdomains_dropped.txt" ]] && dropped_sub_count=$(wc -l < "$outdir/subdomains_dropped.txt")
    [[ -f "$outdir/live_hosts.txt" ]] && live_count=$(wc -l < "$outdir/live_hosts.txt")
    [[ -f "$outdir/ports.txt" ]] && port_count=$(wc -l < "$outdir/ports.txt")
    [[ -f "$outdir/nuclei.jsonl" ]] && finding_count=$(wc -l < "$outdir/nuclei.jsonl")

    {
        echo "# Recon Summary - $target"
        echo
        echo "- Generated: $(date '+%Y-%m-%d %H:%M:%S %Z')"
        echo "- Operator: ${USER:-${USERNAME:-unknown}}@$(hostname)"
        echo "- Intensity: $INTENSITY"
        echo "- Dry run: $DRY_RUN"
        echo "- Proxy: ${PROXY:-none}"
        echo "- Scope file: \`$SCOPE_FILE\`"
        if [[ -n "$PROGRAM_SLUG" ]]; then
            echo "- Program scope: \`$PROGRAM_SCOPE_FILE\`"
            echo "- Policy mode: $POLICY_MODE"
            echo "- Policy artifacts: \`${POLICY_ARTIFACT_DIR:-$outdir/evidence/policy}\`"
        fi
        echo "- Output directory: \`$outdir\`"
        echo
        echo "## Counts"
        echo
        echo "| Item | Count |"
        echo "|---|---:|"
        $DOMAIN_MODE && echo "| Safe subdomains | $sub_count |"
        $DOMAIN_MODE && echo "| Dropped subdomains | $dropped_sub_count |"
        echo "| Live hosts | $live_count |"
        echo "| Open ports | $port_count |"
        echo "| Nuclei triage findings | $finding_count |"
        echo
        echo "## Safety Notes"
        echo
        echo "- All scanner output is triage-only."
        echo "- Hosts and URLs are filtered through \`safe_target\` before stage consumption."
        echo "- Dropped domain-expansion hosts are recorded in \`subdomains_dropped.txt\` when present."
        [[ -n "$PROGRAM_SLUG" ]] && echo "- Program policy decisions are fail-closed and recorded under \`evidence/policy/\`."
        echo "- Manual verification, impact analysis, remediation, and retest evidence are required before reporting."

        if [[ -s "$outdir/ports.txt" ]]; then
            echo
            echo "## Ports (first 30)"
            echo '```'
            head -30 "$outdir/ports.txt"
            echo '```'
        fi
    } > "$summary"

    ok "summary file=$summary"
    cat "$summary"
}

send_notifications() {
    local target="$1" outdir="$2"
    local nuclei_out="$outdir/nuclei.jsonl"

    [[ -z "$SLACK_WEBHOOK" && -z "$GENERIC_WEBHOOK" ]] && return 0
    [[ ! -s "$nuclei_out" ]] && { dbg "no findings; no notification"; return 0; }
    $DRY_RUN && { warn "dry-run: notifications suppressed"; return 0; }

    local notify_count=0
    if command -v jq &>/dev/null; then
        notify_count=$(jq -r --arg sevs "$NOTIFY_ON_FINDING_SEVERITY" \
            'select(.info.severity as $s | ($sevs | split(",")) | index($s)) | .' \
            "$nuclei_out" 2>/dev/null | grep -c '"template-id"' || echo 0)
    fi

    [[ "$notify_count" -eq 0 ]] && { dbg "no findings at notification severity"; return 0; }

    local msg="Recon triage alert for authorized target $target: ${notify_count} candidate finding(s). Report: $outdir/summary.md"

    if [[ -n "$SLACK_WEBHOOK" ]]; then
        info "sending Slack notification"
        curl -s -X POST -H 'Content-Type: application/json' \
            --data "$(jq -n --arg t "$msg" '{text: $t}')" \
            "$SLACK_WEBHOOK" >/dev/null && ok "Slack notification sent"
    fi
    if [[ -n "$GENERIC_WEBHOOK" ]]; then
        info "sending generic webhook notification"
        curl -s -X POST -H 'Content-Type: application/json' \
            --data "$(jq -n --arg t "$target" --arg c "$notify_count" \
                --arg p "$outdir/summary.md" \
                '{target:$t, findings:$c|tonumber, report:$p}')" \
            "$GENERIC_WEBHOOK" >/dev/null && ok "webhook notification sent"
    fi
}

run_pipeline() {
    local target="$1"
    local policy_error_count_before="$POLICY_ERROR_COUNT"

    safe_target "$target" "initial_target" "auto" || return 1
    local normalized_target="$SAFE_TARGET_VALUE"
    local safe_name="${normalized_target//\//_}"
    safe_name="${safe_name//:/_}"

    local outdir
    if [[ -n "$OUTPUT_DIR_OVERRIDE" ]]; then
        outdir="$OUTPUT_DIR_OVERRIDE"
    else
        outdir="${SCANS_DIR:-$HACKLAB/scans}/${safe_name}_${TIMESTAMP}"
    fi
    mkdir -p "$outdir"
    if [[ -n "$PROGRAM_SLUG" ]]; then
        POLICY_ARTIFACT_DIR="$outdir/evidence/policy"
        mkdir -p "$POLICY_ARTIFACT_DIR"
    fi
    RUN_LOG="${LOGS_DIR:-$HACKLAB/logs}/recon_${safe_name}_${TIMESTAMP}.log"
    mkdir -p "$(dirname "$RUN_LOG")"
    : > "$RUN_LOG"

    info "output dir: $outdir"
    info "run log: $RUN_LOG"

    local input_hosts="$outdir/.input_hosts.txt"
    local ttype
    ttype=$(detect_target_type "$normalized_target")
    info "target type: $ttype"

    if $DOMAIN_MODE && [[ "$ttype" == "domain" ]]; then
        enum_subdomains "$normalized_target" "$outdir"
        cp "$outdir/subdomains.txt" "$input_hosts"
    else
        echo "$normalized_target" > "$input_hosts"
    fi

    find_live_hosts "$input_hosts" "$outdir"
    port_scan "$outdir/live_hosts.txt" "$outdir"
    service_fingerprint "$outdir/ports.txt" "$outdir"
    web_probe "$outdir/ports.txt" "$outdir"
    dir_bruteforce "$outdir/web"
    vuln_scan "$outdir/web" "$outdir"
    generate_summary "$normalized_target" "$outdir"
    send_notifications "$normalized_target" "$outdir"

    ok "pipeline complete target=$normalized_target output=$outdir"
    if (( POLICY_ERROR_COUNT > policy_error_count_before )); then
        return "$POLICY_BOUNDARY_ERROR_EXIT"
    fi
    return 0
}

parse_args "$@"
validate_config
validate_runtime_flags

title "Recon start"
info "intensity=$INTENSITY domain_mode=$DOMAIN_MODE proxy=${PROXY:-none}"
$DRY_RUN && warn "DRY-RUN enabled: commands are printed; network stages do not execute"

for t in subfinder httpx naabu nmap feroxbuster nuclei jq curl; do
    if command -v "$t" &>/dev/null; then
        dbg "tool available: $t"
    else
        warn "tool missing: $t"
    fi
done

mkdir -p "${SCANS_DIR:-$HACKLAB/scans}" "${LOGS_DIR:-$HACKLAB/logs}" "$HACKLAB/config"

record_pipeline_status() {
    local status="$1"
    if [[ "$status" -eq "$POLICY_BOUNDARY_ERROR_EXIT" ]]; then
        EXIT_CODE="$POLICY_BOUNDARY_ERROR_EXIT"
    elif [[ "$status" -ne 0 && "$EXIT_CODE" -eq 0 ]]; then
        EXIT_CODE=1
    fi
}

EXIT_CODE=0
if [[ -n "$TARGETS_FILE" ]]; then
    [[ -f "$TARGETS_FILE" ]] || { err "targets file missing: $TARGETS_FILE"; exit 1; }
    info "processing targets file with max_parallel=$MAX_PARALLEL_HOSTS"
    pids=()
    while IFS= read -r line || [[ -n "$line" ]]; do
        line="${line%%#*}"
        line="$(trim "$line")"
        [[ -z "$line" ]] && continue
        run_pipeline "$line" &
        pids+=($!)
        if (( ${#pids[@]} >= MAX_PARALLEL_HOSTS )); then
            wait "${pids[0]}"
            record_pipeline_status "$?"
            pids=("${pids[@]:1}")
        fi
    done < "$TARGETS_FILE"
    for pid in "${pids[@]}"; do
        wait "$pid"
        record_pipeline_status "$?"
    done
else
    run_pipeline "$TARGET"
    record_pipeline_status "$?"
fi

title "Recon done"
echo "${G}Output root: ${SCANS_DIR:-$HACKLAB/scans}${RST}"
echo "${G}Audit log: $AUDIT_LOG_FILE${RST}"
exit "$EXIT_CODE"
