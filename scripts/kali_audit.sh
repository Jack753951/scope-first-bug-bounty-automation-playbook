#!/usr/bin/env bash
# kali_audit.sh — Inventory aggressive offensive tools on your Kali, AND
# look for suspicious scripts/persistence that shouldn't be there.
#
# Usage:
#   chmod +x kali_audit.sh
#   ./kali_audit.sh                       # writes ~/kali_audit_<date>.md
#   ./kali_audit.sh -o /tmp/report.md     # custom output
#
# Run on YOUR OWN Kali only. Read-only — does not modify the system.

set -u

OUTFILE="$HOME/kali_audit_$(date +%Y%m%d_%H%M%S).md"
while getopts "o:" opt; do
  case $opt in
    o) OUTFILE="$OPTARG" ;;
  esac
done

# helpers ---------------------------------------------------------------
H() { echo -e "\n## $*\n" >> "$OUTFILE"; }
H3() { echo -e "\n### $*\n" >> "$OUTFILE"; }
P() { echo -e "$*" >> "$OUTFILE"; }
CODE() { echo -e "\n\`\`\`\n$*\n\`\`\`\n" >> "$OUTFILE"; }

have() { command -v "$1" >/dev/null 2>&1; }

# probe tools by category, report whether each is installed
probe_list() {
  local cat="$1"; shift
  H3 "$cat"
  P "| Tool | Installed | Path |"
  P "|------|-----------|------|"
  for t in "$@"; do
    if have "$t"; then
      P "| \`$t\` | ✅ | $(command -v "$t") |"
    else
      P "| \`$t\` | — | — |"
    fi
  done
}

# header ----------------------------------------------------------------
{
  echo "# Kali Audit Report"
  echo
  echo "_Host: $(hostname) — User: $USER — Date: $(date -u '+%Y-%m-%dT%H:%M:%SZ')_"
  echo "_Kernel: $(uname -r)_  _Distro: $(lsb_release -d 2>/dev/null | cut -f2 || echo Kali)_"
  echo
  echo "> Read-only audit. Section A = inventory of installed offensive tools."
  echo "> Section B = integrity scan for suspicious scripts / persistence."
} > "$OUTFILE"

# ======================================================================
# SECTION A — Inventory
# ======================================================================
H "A. Inventory of offensive capabilities"

H3 "A.1 Installed Kali metapackages"
KALI_META=$(dpkg -l 2>/dev/null | awk '/^ii/ && /kali-tools-/ {print $2}' | sort)
if [ -z "$KALI_META" ]; then
  P "_(no kali-tools-* metapackages installed)_"
else
  CODE "$KALI_META"
fi

probe_list "A.2 Information gathering / recon" \
  nmap masscan rustscan amass subfinder dnsx httpx theharvester recon-ng spiderfoot sublist3r whatweb wafw00f

probe_list "A.3 Vulnerability scanners" \
  nikto nuclei wpscan joomscan sqlmap commix xsser wapiti vega nessus openvas

probe_list "A.4 Exploitation frameworks (HIGH IMPACT)" \
  msfconsole msfvenom searchsploit beef-xss setoolkit empire crackmapexec netexec impacket-psexec

probe_list "A.5 Password attacks" \
  hydra medusa ncrack hashcat john crowbar patator cewl crunch hashid hash-identifier

probe_list "A.6 Wireless attacks (HIGH IMPACT)" \
  aircrack-ng airmon-ng airodump-ng aireplay-ng reaver bully wifite kismet mdk4 fern-wifi-cracker

probe_list "A.7 Network attacks / MITM" \
  ettercap bettercap responder mitmproxy mitm6 yersinia macof arpspoof dnsspoof

probe_list "A.8 Denial of Service (VERY HIGH IMPACT — illegal against unauthorized targets)" \
  hping3 t50 slowhttptest siege thc-ssl-dos torshammer goldeneye hyenae

probe_list "A.9 Sniffing / spoofing" \
  wireshark tshark tcpdump scapy driftnet dsniff

probe_list "A.10 Reverse engineering" \
  gdb radare2 ghidra ida cutter binwalk strings objdump nasm

probe_list "A.11 Post-exploitation / persistence" \
  empire pupy chisel ligolo socat proxychains4 sshuttle koadic

probe_list "A.12 Active Directory" \
  bloodhound-python neo4j impacket-secretsdump impacket-getuserspns impacket-getnpusers responder

probe_list "A.13 Forensics" \
  volatility3 vol3 autopsy plaso log2timeline foremost binwalk testdisk

# ======================================================================
# SECTION B — Integrity / Unexpected scripts
# ======================================================================
H "B. Integrity check — unexpected scripts and persistence"

H3 "B.1 Recently modified executables (last 14 days, top 30)"
RECENT=$(find /usr/local/bin /usr/local/sbin /opt /home /tmp /var/tmp /dev/shm /root \
  -type f \( -perm -u+x -o -name "*.sh" -o -name "*.py" -o -name "*.pl" -o -name "*.rb" \) \
  -mtime -14 2>/dev/null | head -30)
if [ -z "$RECENT" ]; then
  P "_(none in the past 14 days)_"
else
  CODE "$RECENT"
fi

H3 "B.2 Scripts in suspicious locations (/tmp, /var/tmp, /dev/shm)"
SUS=$(find /tmp /var/tmp /dev/shm -type f \( -name "*.sh" -o -name "*.py" -o -name "*.pl" -o -perm -u+x \) 2>/dev/null | head -50)
if [ -z "$SUS" ]; then
  P "_(none — clean)_"
else
  P "**Found scripts in temp directories. Investigate:**"
  CODE "$SUS"
fi

H3 "B.3 SUID binaries (filtered to non-package items)"
ALL_SUID=$(find / -perm -4000 -type f 2>/dev/null)
P "**Total SUID files**: $(echo \"$ALL_SUID\" | wc -l)"
P
P "Items NOT owned by an installed package (the suspicious ones):"
ORPHAN_SUID=$(while IFS= read -r f; do
  dpkg -S "$f" >/dev/null 2>&1 || echo "$f"
done <<<"$ALL_SUID")
if [ -z "$ORPHAN_SUID" ]; then
  P "_(none — every SUID belongs to a package)_"
else
  CODE "$ORPHAN_SUID"
fi

H3 "B.4 World-writable executables (a classic backdoor signature)"
WW=$(find / -type f -perm -o+w -perm -u+x 2>/dev/null | grep -vE '^/proc|^/sys|^/dev' | head -50)
if [ -z "$WW" ]; then
  P "_(none — clean)_"
else
  CODE "$WW"
fi

H3 "B.5 Cron / scheduled tasks"
P "**System crontab**:"
CODE "$(cat /etc/crontab 2>/dev/null)"
P "**/etc/cron.d/**:"
CODE "$(ls -la /etc/cron.d/ 2>/dev/null)"
P "**Per-user crontabs**:"
USERCRON=$(for u in $(cut -f1 -d: /etc/passwd); do
  c=$(crontab -u "$u" -l 2>/dev/null)
  [ -n "$c" ] && echo "[$u]"; echo "$c"
done)
CODE "$USERCRON"

H3 "B.6 Systemd services with suspicious ExecStart"
SVCS=$(systemctl list-unit-files --type=service --state=enabled 2>/dev/null | tail -n +2 | head -n -2 | awk '{print $1}')
ODD=""
while IFS= read -r svc; do
  exec=$(systemctl cat "$svc" 2>/dev/null | grep -E '^ExecStart' | head -1)
  case "$exec" in
    *"/tmp/"*|*"/var/tmp/"*|*"/dev/shm/"*|*"curl "*|*"wget "*|*"bash -i"*|*"nc "*)
      ODD+="$svc → $exec"$'\n' ;;
  esac
done <<<"$SVCS"
if [ -z "$ODD" ]; then
  P "_(no enabled service has ExecStart pointing at temp dirs or shell-pipe patterns)_"
else
  CODE "$ODD"
fi

H3 "B.7 Listening services"
CODE "$(ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null)"

H3 "B.8 Recent shell history (last 50 lines, root + your user)"
P "**Root \`.bash_history\`**:"
CODE "$(tail -n 50 /root/.bash_history 2>/dev/null || echo '(no permission or empty)')"
P "**Your \`.bash_history\`**:"
CODE "$(tail -n 50 "$HOME/.bash_history" 2>/dev/null)"
P "**Zsh history (if present)**:"
CODE "$(tail -n 50 "$HOME/.zsh_history" 2>/dev/null)"

H3 "B.9 Last logins"
CODE "$(last -n 20 2>/dev/null)"

H3 "B.10 Strange network connections (currently established)"
CODE "$(ss -tn state established 2>/dev/null | head -30)"

H3 "B.11 Loaded kernel modules — check for unusual ones"
P "**Unsigned modules** (potential rootkit signal):"
UNSIGNED=$(awk '!/SIG/' /proc/modules 2>/dev/null | head -20)
CODE "$UNSIGNED"

H3 "B.12 Files with no owner (orphaned UID/GID)"
ORPH=$(find / -nouser -o -nogroup 2>/dev/null | grep -vE '^/proc|^/sys|^/run' | head -30)
if [ -z "$ORPH" ]; then
  P "_(none)_"
else
  CODE "$ORPH"
fi

# ======================================================================
# SUMMARY
# ======================================================================
H "Summary checklist"
P "- [ ] Section A.4 / A.6 / A.8 list tools you don't recognise → review"
P "- [ ] Section B.2 / B.3 (orphan SUID) / B.4 (world-writable) anything → INVESTIGATE NOW"
P "- [ ] Section B.5–B.6 cron / systemd: anything you didn't add → INVESTIGATE"
P "- [ ] Section B.8 history shows commands you didn't run → INVESTIGATE"
P "- [ ] Section B.10 connections to unknown IPs → check what process"
P
P "If anything in section B looks suspicious, do NOT clean up immediately."
P "Capture evidence first (\`cp\` the file with hash, snapshot the VM if possible),"
P "then follow the IR playbook in \`hacking/skills/cybersecurity/assets/ir_playbook_template.md\`."
P
P "_Report file: $OUTFILE_"

echo "[+] Audit complete. Report: $OUTFILE"
echo "    Open with: less $OUTFILE   (or any markdown viewer)"
