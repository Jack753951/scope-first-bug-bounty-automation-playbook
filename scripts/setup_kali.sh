#!/usr/bin/env bash
# setup_kali.sh — One-shot installer for everything our scripts need.
#
# Run on a fresh Kali (works on Kali 2024+ and 2026):
#   chmod +x setup_kali.sh
#   ./setup_kali.sh
#
# It will:
#   1) sudo apt update + install Kali-repo tools
#   2) install Go (if missing)
#   3) go install ProjectDiscovery + tomnomnom tools
#   4) extend PATH with ~/go/bin
#   5) update nuclei templates
#   6) gunzip rockyou.txt for jwt_inspect.sh
#   7) chmod +x all the *.sh scripts in this directory
#   8) print a status table of every tool

set -uo pipefail

# ---- Pre-flight ------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ $EUID -ne 0 ]]; then
  echo "[*] Re-running with sudo (apt + symlinks need root)..."
  exec sudo -E bash "$0" "$@"
fi

REAL_USER="${SUDO_USER:-$(whoami)}"
REAL_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)

echo "================================================="
echo "  setup_kali.sh   user=$REAL_USER   home=$REAL_HOME"
echo "================================================="

# ---- 1. Apt packages -------------------------------------------------
echo
echo "[1/8] Installing Kali-repo tools via apt ..."
apt update -qq
APT_PKGS=(
  # core
  curl wget git jq build-essential pkg-config
  # recon
  nmap masscan whois dnsutils
  subfinder amass
  # web
  nikto whatweb wfuzz dirb dirbuster ffuf gobuster
  sqlmap dalfox
  # http probing
  httpx-toolkit dnsx-toolkit
  # nuclei
  nuclei
  # screenshots
  gowitness
  # crypto / cracking
  hashcat john hash-identifier hashid
  # AD / network
  bloodhound impacket-scripts crackmapexec netexec responder
  # misc
  python3-pip golang-go seclists
)
DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends "${APT_PKGS[@]}" 2>&1 \
  | grep -vE "^(Reading|Building|Selecting|Preparing|Unpacking|Setting up|Processing) " \
  | tail -20

# ---- 2. Go ----------------------------------------------------------
echo
echo "[2/8] Verifying Go ..."
if ! command -v go >/dev/null 2>&1; then
  apt install -y golang-go
fi
go version

# ---- 3. Go-installed tools ------------------------------------------
echo
echo "[3/8] Installing Go-based tools (as $REAL_USER) ..."
GO_TOOLS=(
  "github.com/lc/gau/v2/cmd/gau@latest"
  "github.com/Emoe/kxss@latest"
  "github.com/tomnomnom/qsreplace@latest"
  "github.com/tomnomnom/anew@latest"
  "github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest"
  "github.com/projectdiscovery/katana/cmd/katana@latest"
  "github.com/projectdiscovery/notify/cmd/notify@latest"
)
for t in "${GO_TOOLS[@]}"; do
  echo "    -> $t"
  sudo -u "$REAL_USER" -H bash -lc "GOPATH=$REAL_HOME/go GOBIN=$REAL_HOME/go/bin go install -v $t" 2>&1 \
    | tail -3
done

# ---- 4. PATH for Go bin ----------------------------------------------
echo
echo "[4/8] Ensuring ~/go/bin is in PATH ..."
for rc in .bashrc .zshrc; do
  rcfile="$REAL_HOME/$rc"
  [[ ! -f "$rcfile" ]] && continue
  if ! grep -q 'go/bin' "$rcfile"; then
    echo 'export PATH="$PATH:$HOME/go/bin"' >> "$rcfile"
    echo "    added to $rcfile"
  else
    echo "    already in $rcfile"
  fi
done

# ---- 5. Nuclei templates --------------------------------------------
echo
echo "[5/8] Updating nuclei templates ..."
sudo -u "$REAL_USER" -H bash -lc "nuclei -update-templates -silent 2>&1 | tail -5" || true

# ---- 6. Wordlists ---------------------------------------------------
echo
echo "[6/8] Preparing wordlists ..."
if [[ -f /usr/share/wordlists/rockyou.txt.gz && ! -f /usr/share/wordlists/rockyou.txt ]]; then
  echo "    gunzip rockyou.txt.gz ..."
  gunzip -k /usr/share/wordlists/rockyou.txt.gz
fi
ls -lah /usr/share/wordlists/rockyou.txt 2>/dev/null || echo "    (rockyou not found — install seclists?)"

# ---- 7. Make our scripts executable ----------------------------------
echo
echo "[7/8] chmod +x on .sh scripts in $SCRIPT_DIR ..."
chmod +x "$SCRIPT_DIR"/*.sh 2>/dev/null
chown "$REAL_USER:$REAL_USER" "$SCRIPT_DIR"/*.sh 2>/dev/null
ls -1 "$SCRIPT_DIR"/*.sh

# ---- 8. Status table -------------------------------------------------
echo
echo "[8/8] Final tool check ..."
echo
echo "| Tool                | Status |"
echo "|---------------------|--------|"
TOOLS=(
  curl wget jq nmap masscan whois dig
  subfinder amass dnsx httpx
  nikto whatweb ffuf gobuster sqlmap dalfox nuclei
  gowitness hashcat john
  gau kxss qsreplace anew interactsh-client katana
  bloodhound-python crackmapexec nxc impacket-secretsdump
)
for t in "${TOOLS[@]}"; do
  if sudo -u "$REAL_USER" -H bash -lc "command -v $t" >/dev/null 2>&1; then
    printf '| %-19s |   ✅   |\n' "$t"
  else
    printf '| %-19s |   ❌   |\n' "$t"
  fi
done

echo
echo "================================================="
echo "  Setup done. Open a NEW shell (so PATH refreshes)"
echo "  then run e.g.:  ./subdomain_recon.sh example.com --yes"
echo "================================================="
