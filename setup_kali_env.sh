#!/usr/bin/env bash
# =============================================================================
#  setup_kali_env.sh
#  Cybersecurity 專案環境一鍵設定腳本 (Kali Linux VM)
#  目標:
#    1. 偵測 VM 類型 (VirtualBox / VMware)
#    2. 驗證共享資料夾掛載
#    3. 將使用者加入 vboxsf 群組 (若為 VirtualBox)
#    4. 建立固定 symlink ~/projects/cybersec
#    5. 寫入 $HACKLAB 環境變數至 shell rc
#    6. 檢查常用滲透測試工具是否齊備, 缺的列出安裝指令
#
#  用法:
#    chmod +x setup_kali_env.sh
#    ./setup_kali_env.sh
# =============================================================================

set -u  # 未定義變數視為錯誤 (不用 -e, 我們要全程跑完並收集報告)

# ---------- 顏色輸出 ----------
RED=$'\033[0;31m'; GRN=$'\033[0;32m'; YEL=$'\033[1;33m'
BLU=$'\033[0;34m'; CYN=$'\033[0;36m'; BLD=$'\033[1m'; RST=$'\033[0m'

ok()    { echo "${GRN}[OK]${RST}    $*"; }
info()  { echo "${BLU}[INFO]${RST}  $*"; }
warn()  { echo "${YEL}[WARN]${RST}  $*"; }
fail()  { echo "${RED}[FAIL]${RST}  $*"; }
title() { echo; echo "${BLD}${CYN}=== $* ===${RST}"; }

MISSING_TOOLS=()
ACTIONS_TAKEN=()
USER_NAME="${SUDO_USER:-$USER}"
USER_HOME="$(getent passwd "$USER_NAME" | cut -d: -f6)"

# =============================================================================
# 1. 偵測 VM 類型
# =============================================================================
title "1. 偵測虛擬機類型"

VM_TYPE="unknown"
if command -v systemd-detect-virt &>/dev/null; then
    VIRT=$(systemd-detect-virt 2>/dev/null || echo "none")
    info "systemd-detect-virt: $VIRT"
    case "$VIRT" in
        oracle)  VM_TYPE="virtualbox" ;;
        vmware)  VM_TYPE="vmware" ;;
        kvm|qemu) VM_TYPE="kvm" ;;
    esac
fi

# 用掛載狀況再次確認
if mount | grep -q 'type vboxsf'; then
    VM_TYPE="virtualbox"
elif mount | grep -qE 'vmhgfs|fuse.vmhgfs-fuse'; then
    VM_TYPE="vmware"
fi

case "$VM_TYPE" in
    virtualbox) ok "偵測到 VirtualBox" ;;
    vmware)     ok "偵測到 VMware" ;;
    kvm)        warn "偵測到 KVM/QEMU — 共享資料夾通常用 virtiofs / 9p, 此腳本主要針對 VBox/VMware" ;;
    *)          warn "無法判斷 VM 類型, 仍會嘗試後續步驟" ;;
esac

# =============================================================================
# 2. 尋找共享資料夾掛載點
# =============================================================================
title "2. 偵測 hacking 共享資料夾掛載點"

CANDIDATES=(
    "/mnt/hacking"
    "/media/sf_hacking"
    "/media/sf_Hacking"
    "/mnt/hgfs/hacking"
    "$HOME/hacking"
)

SHARE_PATH=""
for p in "${CANDIDATES[@]}"; do
    if [[ -d "$p" ]] && [[ -n "$(ls -A "$p" 2>/dev/null)" ]]; then
        SHARE_PATH="$p"
        break
    fi
done

# 還沒找到? 從 mount 表撈
if [[ -z "$SHARE_PATH" ]]; then
    SHARE_PATH=$(mount | grep -Ei 'vboxsf|vmhgfs' | awk '{print $3}' | head -n1)
fi

if [[ -n "$SHARE_PATH" ]]; then
    ok "共享資料夾位於: $SHARE_PATH"
else
    fail "找不到已掛載的共享資料夾"
    warn "請確認:"
    warn "  VirtualBox: VM 設定 → 共用資料夾 → 加入 hacking 並勾 [自動掛載][永久存在]"
    warn "  VMware:     VM Settings → Options → Shared Folders → Always enabled"
    SHARE_PATH=""
fi

# =============================================================================
# 3. (僅 VBox) 加入 vboxsf 群組
# =============================================================================
if [[ "$VM_TYPE" == "virtualbox" ]]; then
    title "3. 確認 vboxsf 群組成員資格"
    if id -nG "$USER_NAME" | tr ' ' '\n' | grep -qx "vboxsf"; then
        ok "$USER_NAME 已在 vboxsf 群組"
    else
        warn "$USER_NAME 不在 vboxsf 群組, 正在加入 (需要 sudo)"
        if sudo usermod -aG vboxsf "$USER_NAME"; then
            ok "已加入 vboxsf 群組 — ${YEL}需登出再登入才會生效${RST}"
            ACTIONS_TAKEN+=("加入 vboxsf 群組 (重新登入後生效)")
        else
            fail "加入 vboxsf 群組失敗"
        fi
    fi
fi

# =============================================================================
# 4. 建立固定 symlink ~/projects/cybersec
# =============================================================================
title "4. 建立固定路徑 symlink"

PROJ_DIR="$USER_HOME/projects"
LINK_PATH="$PROJ_DIR/cybersec"

mkdir -p "$PROJ_DIR"

if [[ -z "$SHARE_PATH" ]]; then
    warn "因共享資料夾未掛載, 跳過 symlink 建立"
elif [[ -L "$LINK_PATH" ]]; then
    CUR_TARGET=$(readlink "$LINK_PATH")
    if [[ "$CUR_TARGET" == "$SHARE_PATH" ]]; then
        ok "Symlink 已存在且正確: $LINK_PATH -> $SHARE_PATH"
    else
        warn "Symlink 指向錯誤 ($CUR_TARGET), 修正中"
        rm "$LINK_PATH" && ln -s "$SHARE_PATH" "$LINK_PATH"
        ok "已更新 symlink: $LINK_PATH -> $SHARE_PATH"
        ACTIONS_TAKEN+=("修正 symlink 目標")
    fi
elif [[ -e "$LINK_PATH" ]]; then
    fail "$LINK_PATH 已存在且非 symlink, 請手動處理"
else
    ln -s "$SHARE_PATH" "$LINK_PATH"
    ok "建立 symlink: $LINK_PATH -> $SHARE_PATH"
    ACTIONS_TAKEN+=("建立 symlink $LINK_PATH")
fi

# =============================================================================
# 5. 寫入 HACKLAB 環境變數
# =============================================================================
title "5. 設定 \$HACKLAB 環境變數"

ENV_LINE="export HACKLAB=\"$LINK_PATH\""
ENV_LINE2="export PATH=\"\$HACKLAB/bin:\$PATH\""

for rc in "$USER_HOME/.zshrc" "$USER_HOME/.bashrc"; do
    [[ -f "$rc" ]] || continue
    if grep -q "export HACKLAB=" "$rc"; then
        # 已存在 — 確認指向正確
        if grep -q "export HACKLAB=\"$LINK_PATH\"" "$rc"; then
            ok "$rc 已含正確 HACKLAB"
        else
            sed -i "s|export HACKLAB=.*|$ENV_LINE|" "$rc"
            ok "$rc 已更新 HACKLAB 路徑"
            ACTIONS_TAKEN+=("更新 $rc HACKLAB")
        fi
    else
        {
            echo ""
            echo "# --- cybersec project (added by setup_kali_env.sh) ---"
            echo "$ENV_LINE"
            echo "$ENV_LINE2"
        } >> "$rc"
        ok "已寫入 $rc"
        ACTIONS_TAKEN+=("寫入 HACKLAB 至 $rc")
    fi
done

# =============================================================================
# 6. 檢查常用滲透測試工具
# =============================================================================
title "6. 檢查滲透測試工具庫"

# (工具名, 套件名) — 工具名若 = 套件名則第二欄留空
declare -A TOOLS=(
    # 偵察 / 掃描
    [nmap]="nmap"
    [masscan]="masscan"
    [rustscan]="rustscan"
    [whois]="whois"
    [dig]="dnsutils"
    [whatweb]="whatweb"
    [wafw00f]="wafw00f"
    # Web
    [nikto]="nikto"
    [gobuster]="gobuster"
    [ffuf]="ffuf"
    [feroxbuster]="feroxbuster"
    [sqlmap]="sqlmap"
    [wpscan]="wpscan"
    # Exploitation
    [msfconsole]="metasploit-framework"
    [searchsploit]="exploitdb"
    # 密碼
    [hydra]="hydra"
    [john]="john"
    [hashcat]="hashcat"
    [crackmapexec]="crackmapexec"
    # 網路 / 嗅探
    [tcpdump]="tcpdump"
    [tshark]="tshark"
    [wireshark]="wireshark"
    [responder]="responder"
    # 無線
    [aircrack-ng]="aircrack-ng"
    # AD / Win
    [impacket-secretsdump]="impacket-scripts"
    [evil-winrm]="evil-winrm"
    [bloodhound]="bloodhound"
    # 後滲透
    [chisel]="chisel"
    [proxychains]="proxychains4"
    # 雜項
    [git]="git"
    [python3]="python3"
    [pip3]="python3-pip"
    [go]="golang"
    [jq]="jq"
    [curl]="curl"
)

PRESENT=0
TOTAL=0
for cmd in "${!TOOLS[@]}"; do
    ((TOTAL++))
    if command -v "$cmd" &>/dev/null; then
        ((PRESENT++))
    else
        MISSING_TOOLS+=("${TOOLS[$cmd]:-$cmd}")
    fi
done

info "工具齊備度: ${BLD}$PRESENT / $TOTAL${RST}"

if (( ${#MISSING_TOOLS[@]} > 0 )); then
    # 去重
    UNIQ=$(printf "%s\n" "${MISSING_TOOLS[@]}" | sort -u | tr '\n' ' ')
    warn "缺少套件: $UNIQ"
    echo
    echo "${YEL}建議安裝指令:${RST}"
    echo "  sudo apt update && sudo apt install -y $UNIQ"
else
    ok "所有常用工具皆已就緒"
fi

# =============================================================================
# 7. 建立專案資料夾骨架 (在共享資料夾內)
# =============================================================================
if [[ -n "$SHARE_PATH" ]] && [[ -w "$SHARE_PATH" ]]; then
    title "7. 建立專案資料夾骨架"
    SUBDIRS=(
        "recon"        # 偵察結果
        "scans"        # nmap / nikto / 掃描輸出
        "exploits"     # PoC, 利用腳本
        "loot"         # 取得的資料 (帳密, hash, 檔案)
        "reports"      # 測試報告 (md / pdf / docx)
        "scripts"      # 自動化腳本
        "wordlists"    # 自訂字典
        "tools"        # 自編 / 第三方工具
        "logs"         # 操作紀錄
        "notes"        # 筆記
        "cves"         # CVE 追蹤與 PoC
    )
    for d in "${SUBDIRS[@]}"; do
        if [[ ! -d "$SHARE_PATH/$d" ]]; then
            mkdir -p "$SHARE_PATH/$d"
            ok "建立 $SHARE_PATH/$d"
        fi
    done
    # 預設 .gitignore (避免把 loot 推上 git)
    if [[ ! -f "$SHARE_PATH/.gitignore" ]]; then
        cat > "$SHARE_PATH/.gitignore" <<'EOF'
loot/
logs/
*.pcap
*.cap
*.kdbx
*.key
*.pem
creds*
EOF
        ok "建立預設 .gitignore"
    fi
fi

# =============================================================================
# 總結
# =============================================================================
title "完成總結"
echo "${BLD}共享資料夾:${RST}  ${SHARE_PATH:-未掛載}"
echo "${BLD}固定 symlink:${RST} $LINK_PATH"
echo "${BLD}HACKLAB:${RST}     $LINK_PATH"
echo

if (( ${#ACTIONS_TAKEN[@]} > 0 )); then
    echo "${BLD}本次執行的變更:${RST}"
    for a in "${ACTIONS_TAKEN[@]}"; do echo "  • $a"; done
    echo
fi

echo "${BLD}${YEL}接下來:${RST}"
echo "  1. 執行 ${CYN}source ~/.zshrc${RST} (或 ~/.bashrc) 載入 \$HACKLAB"
echo "  2. 若剛被加入 vboxsf 群組, 請 ${CYN}登出再登入${RST} 才能讀寫共享資料夾"
echo "  3. 測試: ${CYN}cd \$HACKLAB && ls${RST}"
if (( ${#MISSING_TOOLS[@]} > 0 )); then
    UNIQ=$(printf "%s\n" "${MISSING_TOOLS[@]}" | sort -u | tr '\n' ' ')
    echo "  4. 安裝缺少工具: ${CYN}sudo apt install -y $UNIQ${RST}"
fi
echo
ok "Setup 完成"
