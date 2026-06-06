#!/usr/bin/env bash
# headers_audit.sh — Score security headers across a list of hosts.
#
# Checks per host:
#   - Strict-Transport-Security (HSTS)
#   - Content-Security-Policy (CSP) — presence + key flags
#   - X-Content-Type-Options (XCTO)
#   - X-Frame-Options / CSP frame-ancestors
#   - Referrer-Policy
#   - Permissions-Policy
#   - Cross-Origin-Opener-Policy / Embedder-Policy
#   - Cookie attributes on Set-Cookie (Secure / HttpOnly / SameSite)
#   - Server / X-Powered-By disclosure
#
# Output: scored Markdown table + per-host detail.
#
# Required: curl, jq, awk

set -uo pipefail

LEGAL='
================ LEGAL NOTICE ================
This tool fetches HTTP response headers from each target URL.
Equivalent to a `curl -I`. Run only on your own / authorised hosts.
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

OUT="${OUT:-./headers_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"
URLS="$OUT/urls.txt"
SCORES="$OUT/scores.csv"
DETAIL="$OUT/detail.md"
REPORT="$OUT/report.md"

if [[ -n "$URLLIST" ]]; then cp "$URLLIST" "$URLS"; else echo "$TARGET" > "$URLS"; fi
NURL=$(wc -l < "$URLS")

echo "host,score,hsts,csp,xcto,xfo,refpol,permspol,coop,coep,setcookie_ok" > "$SCORES"
> "$DETAIL"

audit_one() {
  local url="$1"
  local h
  h=$(curl -sk -I --max-time 10 -L "$url" 2>/dev/null | tr -d '\r')

  has_header() { echo "$h" | grep -qiE "^${1}:"; }
  get_header() { echo "$h" | grep -iE "^${1}:" | head -1 | cut -d: -f2- | xargs; }

  local hsts csp xcto xfo refpol permspol coop coep setck score
  score=0

  has_header "Strict-Transport-Security" && { hsts="✅ $(get_header Strict-Transport-Security)"; score=$((score+1)); } || hsts="❌"
  has_header "Content-Security-Policy"   && { csp="✅"; score=$((score+1)); } || csp="❌"
  has_header "X-Content-Type-Options"    && { xcto="✅"; score=$((score+1)); } || xcto="❌"
  if has_header "X-Frame-Options" || echo "$h" | grep -qiE "frame-ancestors"; then
    xfo="✅"; score=$((score+1)); else xfo="❌"; fi
  has_header "Referrer-Policy"           && { refpol="✅ $(get_header Referrer-Policy)"; score=$((score+1)); } || refpol="❌"
  has_header "Permissions-Policy"        && { permspol="✅"; score=$((score+1)); } || permspol="❌"
  has_header "Cross-Origin-Opener-Policy"   && { coop="✅"; score=$((score+1)); } || coop="❌"
  has_header "Cross-Origin-Embedder-Policy" && { coep="✅"; score=$((score+1)); } || coep="❌"

  # cookies
  local cookies
  cookies=$(echo "$h" | grep -iE "^set-cookie:" || true)
  if [[ -n "$cookies" ]]; then
    if echo "$cookies" | grep -qiE "Secure" && echo "$cookies" | grep -qiE "HttpOnly" && echo "$cookies" | grep -qiE "SameSite"; then
      setck="✅"
      score=$((score+1))
    else
      setck="⚠️"
    fi
  else
    setck="(no Set-Cookie)"
  fi

  # disclosure
  local server xpowered
  server=$(get_header Server)
  xpowered=$(get_header X-Powered-By)

  echo "${url},${score},\"${hsts}\",${csp},${xcto},${xfo},\"${refpol}\",${permspol},${coop},${coep},${setck}" >> "$SCORES"

  {
    echo "### $url"
    echo
    echo "**Score**: ${score}/9"
    echo
    echo "| Header | Status |"
    echo "|--------|--------|"
    echo "| Strict-Transport-Security | $hsts |"
    echo "| Content-Security-Policy | $csp |"
    echo "| X-Content-Type-Options | $xcto |"
    echo "| X-Frame-Options / frame-ancestors | $xfo |"
    echo "| Referrer-Policy | $refpol |"
    echo "| Permissions-Policy | $permspol |"
    echo "| Cross-Origin-Opener-Policy | $coop |"
    echo "| Cross-Origin-Embedder-Policy | $coep |"
    echo "| Set-Cookie attrs (Secure+HttpOnly+SameSite) | $setck |"
    [[ -n "$server" ]]   && echo "| Server (disclosure) | \`$server\` |"
    [[ -n "$xpowered" ]] && echo "| X-Powered-By (disclosure) | \`$xpowered\` |"
    echo
  } >> "$DETAIL"
}

i=0
echo "[*] Auditing $NURL hosts ..."
while read -r u; do
  i=$((i+1))
  printf '\r    %d/%d' "$i" "$NURL"
  audit_one "$u"
done < "$URLS"
echo

# ---- Summary report --------------------------------------------------
{
  echo "# Security Headers Audit"
  echo
  echo "_Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_"
  echo
  echo "## Score summary (lower = worse)"
  echo
  echo "| Host | Score / 9 |"
  echo "|------|-----------|"
  awk -F, 'NR>1 {gsub(/"/,"",$1); printf "| %s | %s/9 |\n", $1, $2}' "$SCORES" \
    | sort -t/ -k1 -nk1
  echo
  echo "## Per-host detail"
  echo
  cat "$DETAIL"
  echo
  echo "## Severity / impact reference"
  echo
  echo "Most missing-header findings are **Low / Informational** in modern bug bounty programs unless chained:"
  echo "- Missing CSP enables more impactful XSS — bring an XSS chain for severity."
  echo "- Missing X-Frame-Options enables clickjacking — bring a sensitive action click PoC."
  echo "- Missing HSTS enables downgrade — only meaningful with on-path attacker."
  echo "- Cookies without Secure / HttpOnly / SameSite enable session theft chains."
  echo
  echo "Don't submit a 'security headers missing' report standalone unless the program explicitly accepts them."
  echo
  echo "---"
  echo
  echo "_CSV data: \`$SCORES\` (open in spreadsheet for sorting)._"
} > "$REPORT"

echo
echo "[+] Done."
echo "    Report: $REPORT"
echo "    CSV   : $SCORES"
