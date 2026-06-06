#!/usr/bin/env bash
# cors_audit.sh — Audit CORS configuration across a list of URLs.
#
# Tests:
#   1) Reflected origin            — Origin: https://evil.com
#   2) Null origin                 — Origin: null
#   3) Wildcard subdomain bypass   — Origin: https://target.com.evil.com
#   4) Pre-domain bypass           — Origin: https://eviltarget.com
#   5) Wildcard with credentials   — flagged when ACAO=* + ACAC=true
#
# Each test inspects:
#   - Access-Control-Allow-Origin (ACAO)
#   - Access-Control-Allow-Credentials (ACAC)
#
# Required: curl, jq

set -uo pipefail

LEGAL='
================ LEGAL NOTICE ================
This tool sends HTTP requests with crafted Origin headers. Use only on:
  (a) your own systems,
  (b) authorised targets,
  (c) self-hosted lab apps.
==============================================
'

TARGET=""; URLLIST=""; OUT=""; YES=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -l|--list) URLLIST="$2"; shift 2 ;;
    -o|--out)  OUT="$2"; shift 2 ;;
    --yes)     YES=1; shift ;;
    -h|--help) sed -n '2,18p' "$0"; exit 0 ;;
    *)         TARGET="$1"; shift ;;
  esac
done

[[ -z "$TARGET" && -z "$URLLIST" ]] && { echo "Usage: $0 <target-url> | -l urls.txt"; exit 2; }
echo "$LEGAL"
[[ $YES -ne 1 ]] && { read -rp "Proceed? (yes/N) " a; [[ "$a" != yes ]] && exit 1; }

OUT="${OUT:-./cors_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"
URLS="$OUT/urls.txt"
HITS="$OUT/hits.txt"
REPORT="$OUT/report.md"

if [[ -n "$URLLIST" ]]; then cp "$URLLIST" "$URLS"; else echo "$TARGET" > "$URLS"; fi
NURL=$(wc -l < "$URLS")

> "$HITS"

# Run a CORS test, capture relevant headers
test_cors() {
  local url="$1" origin="$2" label="$3"
  local headers
  headers=$(curl -sk -I --max-time 10 -H "Origin: ${origin}" "$url" 2>/dev/null)
  local acao acac
  acao=$(echo "$headers" | grep -i '^access-control-allow-origin:' | tr -d '\r' | head -1 | cut -d: -f2- | xargs)
  acac=$(echo "$headers" | grep -i '^access-control-allow-credentials:' | tr -d '\r' | head -1 | cut -d: -f2- | xargs)

  [[ -z "$acao" ]] && return 0   # no CORS at all on this endpoint

  # Hit conditions
  local issue=""
  if [[ "$acao" == "*" && "$acac" == "true" ]]; then
    issue="WILDCARD+CREDS (HIGH)"
  elif [[ "$acao" == "$origin" ]]; then
    issue="REFLECTS_ORIGIN ($label)"
  elif [[ "$acao" == "null" && "$origin" == "null" ]]; then
    issue="NULL_ORIGIN_ALLOWED"
  fi

  if [[ -n "$issue" ]]; then
    local sev="LOW"
    [[ "$acac" == "true" ]] && sev="HIGH (creds allowed)"
    echo "$sev | $issue | origin=$origin | acao=$acao | acac=$acac | $url" >> "$HITS"
    echo "  [HIT-$sev] $issue  $url"
  fi
}

i=0
total=$NURL
echo "[*] Testing $total URLs ..."
while read -r u; do
  i=$((i+1))
  printf '\r    %d/%d  ' "$i" "$total"
  # Derive a plausible "evil" origin from target host
  host=$(echo "$u" | sed -E 's#https?://([^/]+).*#\1#')
  test_cors "$u" "https://evil.com"                              "external"
  test_cors "$u" "null"                                          "null"
  test_cors "$u" "https://${host}.evil.com"                      "subdomain-of-evil"
  test_cors "$u" "https://evil${host}"                           "pre-domain"
  test_cors "$u" "http://${host}"                                "scheme-downgrade"
done < "$URLS"
echo

NHIT=$(wc -l < "$HITS" 2>/dev/null || echo 0)
echo "    -> $NHIT CORS misconfig hits"

{
  echo "# CORS Audit Report"
  echo
  echo "_Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_"
  echo
  echo "## Summary"
  echo
  echo "| Metric | Count |"
  echo "|--------|-------|"
  echo "| URLs tested | $NURL |"
  echo "| Misconfig hits | $NHIT |"
  echo
  echo "## Hits"
  if [[ -s "$HITS" ]]; then
    echo '```'
    cat "$HITS"
    echo '```'
  else
    echo "_(no CORS misconfig — clean)_"
  fi
  echo
  echo "## Severity guide"
  echo
  echo "- **HIGH**: \`Access-Control-Allow-Origin\` reflects attacker origin AND \`Access-Control-Allow-Credentials: true\` → attacker can read authenticated responses cross-origin → account takeover surface."
  echo "- **MEDIUM**: ACAO reflects origin without credentials → still bad if endpoint returns sensitive non-cookie data."
  echo "- **LOW / Informational**: \`Access-Control-Allow-Origin: *\` without credentials on public endpoints — usually intended."
  echo
  echo "## Validation"
  echo
  echo "Build a one-page PoC that fetches the endpoint cross-origin from your domain and shows the response. Without that, programs typically reject reports as theoretical."
  echo
  echo "---"
} > "$REPORT"

echo
echo "[+] Done."
echo "    Report: $REPORT"
