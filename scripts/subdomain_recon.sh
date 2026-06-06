#!/usr/bin/env bash
# subdomain_recon.sh — subdomain enumeration + alive check + tech fingerprint
#                      + screenshot. The "first pass" of any external recon.
#
# Pipeline:
#   1) subfinder + amass passive  → subdomains
#   2) dnsx                       → resolve, drop dead names
#   3) httpx                      → alive HTTP/S, title, status, tech detect
#   4) gowitness                  → screenshot every alive host
#   5) Markdown report with thumbnails inline
#
# Usage:
#   ./subdomain_recon.sh example.com
#   ./subdomain_recon.sh example.com -o /tmp/recon --yes
#
# Required: subfinder, dnsx-toolkit, httpx-toolkit, gowitness (optional), jq

set -uo pipefail

LEGAL='
================ LEGAL NOTICE ================
This tool issues DNS + HTTP probes against the target.
Use only on:
  (a) domains you own,
  (b) targets under written authorization, or
  (c) bug bounty programs where the scope explicitly allows.
==============================================
'

YES=0
OUT=""
DOMAIN=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--out) OUT="$2"; shift 2 ;;
    --yes)    YES=1; shift ;;
    -h|--help) sed -n '2,18p' "$0"; exit 0 ;;
    *) DOMAIN="$1"; shift ;;
  esac
done

[[ -z "$DOMAIN" ]] && { echo "Usage: $0 <domain> [-o OUTDIR] [--yes]"; exit 2; }
echo "$LEGAL"
[[ $YES -ne 1 ]] && { read -rp "Proceed? (yes/N) " a; [[ "$a" != yes ]] && exit 1; }

OUT="${OUT:-./recon_${DOMAIN}_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT/screenshots"
SUB="$OUT/subdomains.txt"
RES="$OUT/resolved.txt"
ALIVE="$OUT/alive.json"
REPORT="$OUT/report.md"

have(){ command -v "$1" >/dev/null 2>&1; }

# ---- 1. Subdomain enumeration (passive sources only) ------------------
echo "[*] Enumerating subdomains for $DOMAIN ..."
{
  if have subfinder; then subfinder -d "$DOMAIN" -silent; fi
  if have amass;     then amass enum -passive -d "$DOMAIN" 2>/dev/null; fi
  # crt.sh fallback (always works without tools)
  curl -s "https://crt.sh/?q=%25.${DOMAIN}&output=json" 2>/dev/null \
    | jq -r '.[].name_value' 2>/dev/null \
    | tr ',' '\n' | sed 's/^\*\.//' || true
  echo "$DOMAIN"
} | grep -E "\.${DOMAIN}$|^${DOMAIN}$" | sort -u > "$SUB"
NSUB=$(wc -l < "$SUB")
echo "    -> $NSUB unique subdomains"

# ---- 2. DNS resolution ------------------------------------------------
echo "[*] Resolving ..."
if have dnsx; then
  dnsx -l "$SUB" -silent -a -resp-only 2>/dev/null | sort -u > "$RES"
else
  while read -r s; do
    getent hosts "$s" >/dev/null 2>&1 && echo "$s"
  done < "$SUB" > "$RES"
fi
NRES=$(wc -l < "$RES")
echo "    -> $NRES resolve"

# ---- 3. Alive HTTP probing + tech fingerprint -------------------------
echo "[*] HTTP probing (httpx) ..."
if have httpx; then
  httpx -l "$RES" -silent -title -status-code -tech-detect -tls-grab \
    -follow-redirects -json -o "$ALIVE" 2>/dev/null
  NALIVE=$(grep -c "" "$ALIVE" 2>/dev/null || echo 0)
else
  echo "    !! httpx-toolkit not installed; falling back to curl"
  > "$ALIVE"
  while read -r h; do
    for scheme in https http; do
      code=$(curl -sk -o /dev/null -w "%{http_code}" --max-time 8 "${scheme}://${h}" 2>/dev/null)
      if [[ "$code" != 000 ]]; then
        title=$(curl -sk --max-time 8 "${scheme}://${h}" 2>/dev/null | grep -oE '<title>[^<]+' | head -1 | sed 's/<title>//')
        echo "{\"url\":\"${scheme}://${h}\",\"status_code\":${code},\"title\":\"${title}\"}" >> "$ALIVE"
        break
      fi
    done
  done < "$RES"
  NALIVE=$(grep -c "" "$ALIVE" 2>/dev/null || echo 0)
fi
echo "    -> $NALIVE alive"

# ---- 4. Screenshots ---------------------------------------------------
if have gowitness && [[ "$NALIVE" -gt 0 ]]; then
  echo "[*] Screenshotting alive hosts ..."
  jq -r '.url' "$ALIVE" 2>/dev/null > "$OUT/alive_urls.txt"
  ( cd "$OUT/screenshots" && \
    gowitness scan file -f "$OUT/alive_urls.txt" --threads 5 --timeout 15 2>/dev/null || true ) || true
fi

# ---- 5. Report --------------------------------------------------------
{
  echo "# Recon Report — $DOMAIN"
  echo
  echo "_Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_"
  echo
  echo "## Summary"
  echo
  echo "| Metric | Count |"
  echo "|--------|-------|"
  echo "| Subdomains discovered | $NSUB |"
  echo "| Resolving | $NRES |"
  echo "| Alive (HTTP/S) | $NALIVE |"
  echo
  echo "## Alive hosts"
  echo
  if [[ -s "$ALIVE" ]]; then
    echo '| URL | Status | Title | Tech |'
    echo '|-----|--------|-------|------|'
    jq -r '"| \(.url) | \(.status_code) | \(.title // "") | \((.tech // []) | join(", ")) |"' "$ALIVE" 2>/dev/null
  else
    echo "_(no alive hosts found)_"
  fi
  echo
  echo "## Findings worth investigating"
  echo
  echo "Heuristics — anything matching deserves a closer look:"
  echo
  echo "### Non-200 / unusual status codes"
  echo
  echo '```'
  jq -r 'select(.status_code != 200 and .status_code != 301 and .status_code != 302) | "\(.status_code)\t\(.url)"' "$ALIVE" 2>/dev/null | head -30
  echo '```'
  echo
  echo "### Admin / login / dev / staging / test panels"
  echo
  echo '```'
  jq -r '.url' "$ALIVE" 2>/dev/null \
    | grep -iE "admin|login|dev|stag|test|api|internal|portal|dashboard|phpmyadmin|cpanel|grafana|kibana|jenkins|jira|wiki|gitlab|sonar"
  echo '```'
  echo
  echo "### Old / outdated technologies (hand-pick from this list)"
  echo
  echo '```'
  jq -r '"\(.url)\t\((.tech // []) | join(","))"' "$ALIVE" 2>/dev/null \
    | grep -iE "wordpress|drupal|joomla|jboss|tomcat|struts|coldfusion|magento|shopify|laravel|django|rails|express|aspnet" | head -30
  echo '```'
  echo
  if [[ -d "$OUT/screenshots/screenshots" ]] || ls "$OUT/screenshots"/*.png 2>/dev/null >/dev/null; then
    echo "## Screenshots"
    echo
    echo "Open \`$OUT/screenshots/\` (gowitness writes \`gowitness.sqlite3\` + per-host pngs)."
    echo "If gowitness wrote a HTML report, open it directly: \`$OUT/screenshots/report/index.html\`."
  fi
  echo
  echo "## Suggested next steps"
  echo
  echo "1. For each interesting host, manually browse + look at JS for endpoints."
  echo "2. Run **subdomain_takeover.sh** on the same domain — dangling DNS often hides here."
  echo "3. For tech matches, check known CVEs (\`searchsploit <tech>\`)."
  echo "4. For login pages, test default creds + common username enumeration vectors."
  echo
  echo "---"
  echo
  echo "_Recon is the cheapest hour you'll ever spend. Most beginners skip ahead to scanning. Don't._"
} > "$REPORT"

echo
echo "[+] Done."
echo "    Report: $REPORT"
echo "    Alive : $NALIVE"
