#!/usr/bin/env bash
# subdomain_takeover.sh — find dangling subdomains pointing to unclaimed
#                        services (S3, GitHub Pages, Heroku, etc.)
#
# Pipeline:
#   1) subfinder + amass passive → all subdomains we know about
#   2) dnsx                       → which resolve, with CNAME info
#   3) match CNAME against known takeover signatures
#   4) httpx                      → fetch each candidate's response body
#   5) match body against fingerprint strings (e.g. "NoSuchBucket")
#   6) nuclei takeover templates  → cross-validation
#
# Usage:
#   ./subdomain_takeover.sh example.com
#   ./subdomain_takeover.sh example.com -o /tmp/takeover --yes
#
# Required: subfinder, dnsx, httpx (-toolkit, not python), nuclei, jq, curl
# Optional: amass (richer passive recon)
# Install on Kali:
#   sudo apt install subfinder dnsx-toolkit httpx-toolkit nuclei amass jq -y

set -uo pipefail

LEGAL_NOTICE='
================ LEGAL NOTICE ================
This tool issues HTTP and DNS queries against the target.
Use only on:
  (a) domains you own,
  (b) targets under written authorization, or
  (c) bug bounty programs where the scope explicitly allows.
==============================================
'

YES=0
OUTBASE=""
DOMAIN=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--out) OUTBASE="$2"; shift 2 ;;
    --yes)    YES=1; shift ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) DOMAIN="$1"; shift ;;
  esac
done

[[ -z "$DOMAIN" ]] && { echo "Usage: $0 <domain> [-o OUTDIR] [--yes]"; exit 2; }

# legality gate
echo "$LEGAL_NOTICE"
if [[ $YES -ne 1 ]]; then
  read -rp "Proceed? (yes/N) " a
  [[ "$a" != "yes" ]] && { echo "Aborted."; exit 1; }
fi

OUT="${OUTBASE:-./takeover_${DOMAIN}_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"
REPORT="$OUT/report.md"

have(){ command -v "$1" >/dev/null 2>&1; }

# Known takeover fingerprints (CNAME pattern → body marker)
# Sources: EdOverflow/can-i-take-over-xyz + nuclei takeover templates
declare -A SIGNATURE=(
  ["s3.amazonaws.com"]="NoSuchBucket"
  ["github.io"]="There isn't a GitHub Pages site here"
  ["herokuapp.com"]="No such app"
  ["herokussl.com"]="No such app"
  ["wordpress.com"]="Do you want to register"
  ["pantheonsite.io"]="The gods are wise, but do not know of the site"
  ["cloudfront.net"]="Bad request: ERROR: The request could not be satisfied"
  ["azurewebsites.net"]="404 Web Site not found"
  ["cloudapp.net"]="Sorry, this page cannot be found"
  ["ghost.io"]="The thing you were looking for is no longer here"
  ["readme.io"]="Project doesnt exist"
  ["surge.sh"]="project not found"
  ["unbouncepages.com"]="The requested URL was not found on this server"
  ["myshopify.com"]="Sorry, this shop is currently unavailable"
  ["bitbucket.io"]="Repository not found"
  ["fastly.net"]="Fastly error: unknown domain"
  ["tumblr.com"]="Whatever you were looking for doesn't currently exist"
  ["zendesk.com"]="Help Center Closed"
  ["statuspage.io"]="Statuspage doesn't allow"
  ["hosted-status.com"]="404"
)

# ---- 1. Subdomain enumeration -----------------------------------------
echo "[*] Enumerating subdomains for $DOMAIN ..."
{
  if have subfinder; then subfinder -d "$DOMAIN" -silent; fi
  if have amass; then amass enum -passive -d "$DOMAIN" 2>/dev/null; fi
  echo "$DOMAIN"
} | sort -u > "$OUT/subdomains.txt"
NSUB=$(wc -l < "$OUT/subdomains.txt")
echo "    -> $NSUB unique subdomains"

# ---- 2. DNS resolution + CNAME extraction -----------------------------
echo "[*] Resolving + collecting CNAMEs ..."
if have dnsx; then
  dnsx -l "$OUT/subdomains.txt" -cname -resp -silent -o "$OUT/dnsx.txt" 2>/dev/null
else
  # fallback: dig
  while read -r s; do
    cn=$(dig +short CNAME "$s" 2>/dev/null | head -1)
    [[ -n "$cn" ]] && echo "$s [CNAME] $cn"
  done < "$OUT/subdomains.txt" > "$OUT/dnsx.txt"
fi

# ---- 3. CNAME signature matching --------------------------------------
echo "[*] Matching against takeover signatures ..."
> "$OUT/candidates.txt"
while IFS= read -r line; do
  for sig in "${!SIGNATURE[@]}"; do
    if echo "$line" | grep -qiF "$sig"; then
      sub=$(echo "$line" | awk '{print $1}')
      cname=$(echo "$line" | grep -oE '[A-Za-z0-9._-]+' | tail -1)
      echo "$sub | $cname | $sig | ${SIGNATURE[$sig]}" >> "$OUT/candidates.txt"
      break
    fi
  done
done < "$OUT/dnsx.txt"
NCAND=$(wc -l < "$OUT/candidates.txt")
echo "    -> $NCAND candidates with suspicious CNAMEs"

# ---- 4. HTTP body fingerprint verification ----------------------------
echo "[*] Verifying with HTTP body fingerprints ..."
> "$OUT/confirmed.txt"
while IFS='|' read -r sub cname sig marker; do
  sub=$(echo "$sub" | xargs)
  marker=$(echo "$marker" | xargs)
  # follow redirects, 10s timeout, curl quietly
  body=$(curl -sk -L --max-time 10 "http://$sub" 2>/dev/null; curl -sk -L --max-time 10 "https://$sub" 2>/dev/null)
  if echo "$body" | grep -qF "$marker"; then
    echo "$sub | $cname | CONFIRMED ($marker)" >> "$OUT/confirmed.txt"
  fi
done < "$OUT/candidates.txt"
NCONF=$(wc -l < "$OUT/confirmed.txt")
echo "    -> $NCONF confirmed via HTTP body"

# ---- 5. Cross-check with nuclei ---------------------------------------
NUCLEI_OUT="$OUT/nuclei_takeovers.jsonl"
if have nuclei; then
  echo "[*] Nuclei takeover templates ..."
  nuclei -l "$OUT/subdomains.txt" -t http/takeovers/ -jsonl -o "$NUCLEI_OUT" -silent -disable-update-check 2>/dev/null || true
fi

# ---- 6. Markdown report -----------------------------------------------
{
  echo "# Subdomain Takeover Report — $DOMAIN"
  echo
  echo "_Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_"
  echo
  echo "## Summary"
  echo
  echo "| Metric | Count |"
  echo "|--------|-------|"
  echo "| Total subdomains discovered | $NSUB |"
  echo "| With CNAME matching takeover signature | $NCAND |"
  echo "| Confirmed via HTTP body | $NCONF |"
  echo
  echo "## Confirmed takeovers (highest priority)"
  echo
  if [[ -s "$OUT/confirmed.txt" ]]; then
    echo '```'
    cat "$OUT/confirmed.txt"
    echo '```'
    echo
    echo "**Validation steps**:"
    echo "1. Confirm the subdomain still resolves to the dangling service."
    echo "2. Try registering the resource (S3 bucket, Heroku app, etc.) to demonstrate impact."
    echo "3. **Do not** actually take over a third-party domain in a bug bounty — taking the bucket and serving content can be considered exceeding scope."
    echo "4. Report immediately to program / vendor."
  else
    echo "_(none confirmed)_"
  fi
  echo
  echo "## Candidate (signature matched but not body-verified)"
  echo
  echo '```'
  cat "$OUT/candidates.txt" 2>/dev/null
  echo '```'
  echo
  if [[ -s "$NUCLEI_OUT" ]]; then
    echo "## Nuclei findings"
    echo
    echo '```'
    jq -r '"\(.template-id)\t\(.host)\t\(.matched-at)"' < "$NUCLEI_OUT" 2>/dev/null
    echo '```'
  fi
  echo
  echo "---"
  echo
  echo "_Run only on authorized targets. See bug bounty rules — many programs require validation without serving content from the takeover._"
} > "$REPORT"

echo
echo "[+] Done."
echo "    Report: $REPORT"
echo "    Confirmed takeovers: $NCONF"
echo "    Candidates: $NCAND"
