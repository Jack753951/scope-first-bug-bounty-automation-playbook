#!/usr/bin/env bash
# xss_finder.sh — find reflected XSS candidates and validate context.
#
# Pipeline:
#   1) URL collection (gau / user list)
#   2) keep URLs with parameters
#   3) kxss — fast reflection check (which params reflect special chars)
#   4) dalfox  — context-aware payload generation + blind verification
#   5) generate per-finding curl PoC
#
# Usage:
#   ./xss_finder.sh https://target.lab
#   ./xss_finder.sh -l urls.txt -o /tmp/xss
#   ./xss_finder.sh https://target.lab --yes
#
# Required: curl
# Recommended: gau, kxss, dalfox, qsreplace
# Install (Kali):
#   sudo apt install dalfox
#   go install github.com/lc/gau/v2/cmd/gau@latest
#   go install github.com/Emoe/kxss@latest
#   go install github.com/tomnomnom/qsreplace@latest

set -uo pipefail

LEGAL='
================ LEGAL NOTICE ================
This tool injects XSS probe strings into target URLs. Run only on:
  (a) systems you own,
  (b) authorised targets,
  (c) lab apps (Juice Shop, WebGoat, DVWA, XSS-game).
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

OUT="${OUT:-./xss_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"
URLS="$OUT/urls.txt"
PARAMS="$OUT/params.txt"
KX="$OUT/kxss.txt"
DX="$OUT/dalfox.json"
REPORT="$OUT/report.md"

have(){ command -v "$1" >/dev/null 2>&1; }

# ---- 1. URL collection ------------------------------------------------
if [[ -n "$URLLIST" ]]; then
  cp "$URLLIST" "$URLS"
elif have gau; then
  echo "[*] gau on $TARGET ..."
  echo "$TARGET" | gau --threads 5 2>/dev/null | sort -u > "$URLS"
else
  echo "$TARGET" > "$URLS"
fi
NURL=$(wc -l < "$URLS")
echo "    -> $NURL URLs"

# ---- 2. Filter to URLs with parameters --------------------------------
grep -E '\?[a-zA-Z0-9_]+=.+' "$URLS" | sort -u > "$PARAMS"
NPARAM=$(wc -l < "$PARAMS")
echo "    -> $NPARAM URLs with query parameters"

# ---- 3. kxss reflection check -----------------------------------------
NREFL=0
if have kxss; then
  echo "[*] kxss reflection check ..."
  cat "$PARAMS" | kxss > "$KX" 2>/dev/null || true
  NREFL=$(grep -c "" "$KX" 2>/dev/null || echo 0)
  echo "    -> $NREFL reflection candidates"
else
  echo "    !! kxss not installed — skipping reflection pre-filter"
  cp "$PARAMS" "$KX"
  NREFL=$NPARAM
fi

# ---- 4. dalfox deep scan ----------------------------------------------
NCONF=0
if have dalfox && [[ -s "$KX" ]]; then
  echo "[*] dalfox deep scan (this can take a while) ..."
  # Extract just the URL portion in case kxss output has prefix
  awk '{ for(i=1;i<=NF;i++) if($i~/^https?:\/\//) {print $i; break} }' "$KX" \
    | sort -u > "$OUT/dalfox_input.txt"
  dalfox file "$OUT/dalfox_input.txt" -o "$DX" --format json --silence \
    --skip-bav --no-color --user-agent "Mozilla/5.0 xss-finder" 2>/dev/null || true
  NCONF=$(jq -s 'length' "$DX" 2>/dev/null || echo 0)
  echo "    -> $NCONF dalfox findings"
fi

# ---- 5. Manual probe — minimal reflection check -----------------------
# If neither kxss nor dalfox are available, do a minimal canary test
if ! have kxss && ! have dalfox; then
  echo "[*] Manual fallback: canary reflection probe ..."
  > "$OUT/manual_reflect.txt"
  CANARY="xss$(date +%s)canary"
  while read -r u; do
    prefix="${u%=*}="
    body=$(curl -sk --max-time 8 "${prefix}${CANARY}" 2>/dev/null)
    if echo "$body" | grep -qF "$CANARY"; then
      ctx="unknown"
      echo "$body" | grep -oE ".{0,20}${CANARY}.{0,20}" | head -1 > "$OUT/_ctx.tmp"
      echo "$u | reflects" >> "$OUT/manual_reflect.txt"
    fi
  done < "$PARAMS"
  NCONF=$(wc -l < "$OUT/manual_reflect.txt" 2>/dev/null || echo 0)
fi

# ---- 6. Report --------------------------------------------------------
{
  echo "# XSS Auto-Finder Report"
  echo
  echo "_Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_"
  echo
  echo "## Summary"
  echo
  echo "| Metric | Count |"
  echo "|--------|-------|"
  echo "| URLs collected | $NURL |"
  echo "| URLs with parameters | $NPARAM |"
  echo "| kxss reflections | $NREFL |"
  echo "| dalfox findings | $NCONF |"
  echo
  echo "## Findings (dalfox)"
  if [[ -s "$DX" ]]; then
    echo
    echo '| Severity | Type | URL | Param | Payload |'
    echo '|----------|------|-----|-------|---------|'
    jq -r '.[] | "| \(.severity // "?") | \(.type // "?") | \(.url) | \(.param // "?") | `\(.evidence // .payload // "?")` |"' \
      "$DX" 2>/dev/null
  else
    echo
    echo "_(none)_"
  fi
  echo
  echo "## Reflection candidates (kxss)"
  echo
  echo '```'
  cat "$KX" 2>/dev/null | head -50
  echo '```'
  echo
  echo "## Recommended next steps"
  echo
  echo "1. **Open each finding in Burp Repeater** — figure out the injection context (HTML body, attribute, JS, URL, CSS)."
  echo "2. Tailor a payload to the actual context. Generic dalfox payloads often miss because of CSP / WAF / encoding."
  echo "3. If reflected but not exploitable today, note WHY (CSP nonce, context escape, encoding)."
  echo "4. For confirmed XSS, capture: the request, the reflected response, the executing PoC HTML, and impact (cookie steal? CSRF chain? account takeover?)."
  echo
  echo "---"
  echo
  echo "_Reflection ≠ exploitable XSS. Always validate context manually._"
} > "$REPORT"

echo
echo "[+] Done."
echo "    Report: $REPORT"
