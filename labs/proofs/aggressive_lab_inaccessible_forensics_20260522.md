> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# AGGRESSIVE LAB 不可存取盤點 — 2026-05-22

## 結論

VirtualBox 目前把 `<attacker-vm>` 舊註冊項顯示為 `<inaccessible>`，不是因為 `.vbox` 或 VDI 檔案整體消失，而是 VM 設定的快照/差分磁碟鏈不一致。

VirtualBox 服務日誌明確原因：

```text
Hard disk '<user-home>\VirtualBox VMs\<attacker-vm>\Snapshots/{059a396f-8be9-4c71-a82b-67e32709a46f}.vdi'
with UUID {059a396f-8be9-4c71-a82b-67e32709a46f} cannot be directly attached ...
because it has 1 differencing child hard disks
```

所以狀態是：目前 VM 硬體設定直接掛了 `{059a396f...}.vdi`，但 MediaRegistry 裡它底下還有一個 child differencing disk `{c1605561...}.vdi`。VirtualBox 不允許直接掛載還有 child 的 parent differencing disk，因此 MachineWrap 進入 limited functionality / E_ACCESSDENIED。

## 觀察證據

### VirtualBox registry

`<user-home>\.VirtualBox\VirtualBox.xml` 仍註冊：

```text
<MachineEntry uuid="{5764e0cc-bee0-404b-a8f6-3bd808744326}" src="<user-home>\VirtualBox VMs\<attacker-vm>\<attacker-vm>.vbox"/>
```

`VBoxManage list vms` 顯示：

```text
"kali-linux-2026.1-virtualbox-amd64" {e0b26239-4e20-4e3d-bff0-e44798844d54}
"<victim-vm>" {49df0cc7-776e-4307-a062-40297bfa13c1}
"<inaccessible>" {5764e0cc-bee0-404b-a8f6-3bd808744326}
```

### 舊 AGGRESSIVE LAB 檔案存在

```text
<user-home>\VirtualBox VMs\<attacker-vm>\<attacker-vm>.vbox exists=True size=26879
<user-home>\VirtualBox VMs\<attacker-vm>\<attacker-vm>.vdi exists=True size=16486760448
Snapshots/{48963f95...}.vdi exists=True
Snapshots/{db2a5979...}.vdi exists=True
Snapshots/{059a396f...}.vdi exists=True
Snapshots/{c1605561...}.vdi exists=True
Snapshots/2026-05-18T06-03-49-205441800Z.sav exists=True
```

### `.vbox` 內部不一致點

`<attacker-vm>.vbox`：

```text
Machine currentSnapshot="{d240230c-146e-430b-b81c-ae713ac26f38}" aborted="true"
MediaRegistry chain: ... {059a396f...}.vdi -> child {c1605561...}.vdi
Current hardware attached image: {059a396f-8be9-4c71-a82b-67e32709a46f}
```

這代表它可能在 live snapshot / aborted shutdown 期間被中斷，留下「current hardware 指向 parent、但 parent 已有 child」的非法狀態。

### 最後 VM log 線索

`Logs/VBox.log` 顯示最後接近線索：

```text
Console: Machine state changed to 'LiveSnapshotting'
Saving state of VM, reason 'Snapshot'
Changing the VM state from 'RUNNING' to 'RUNNING_LS'
...
Changing the VM state from 'RUNNING_LS' to 'SUSPENDING_EXT_LS'
Console: Machine state changed to 'OnlineSnapshotting'
```

此後 `.vbox` 記錄 `aborted="true"`。這支持「線上快照/儲存狀態途中中斷」的判斷。

## 可用替代 VM 狀態

目前沒有 running VM。

### `kali-linux-2026.1-virtualbox-amd64`

```text
VMState="poweroff"
ostype="Debian (64-bit)"
memory=2048
cpus=2
nic1="hostonly" cableconnected1="on"
nic2="null" cableconnected2="off"
CurrentSnapshotName="security-runtime-20260518-140349"
last guest IP evidence: eth0 <lab-ip>, eth1 10.0.3.15
```

可作為 attacker / aggressive-lab 替代基底，但要先明確決定是否改名或 clone 成新的 `<attacker-vm>`。

### `<victim-vm>`

```text
VMState="poweroff"
ostype="Debian (64-bit)"
memory=4096
cpus=4
nic1="hostonly" cableconnected1="on"
nic2="null" cableconnected2="off"
CurrentSnapshotName="pre-aggressive-current-running-recovery-20260521-093252"
last guest IP evidence: eth0 <lab-ip>, docker0 172.17.0.1
```

可作為 vulnerable app / victim host 替代；上一輪 Juice Shop 目標 IP 也是 `<lab-ip>:3000`。

## 建議處置

不要直接手改 `.vbox` 作為第一選項。建議順序：

1. 先保持舊 `<inaccessible>` 註冊項不動，避免破壞可復原檔案。
2. 以 `kali-linux-2026.1-virtualbox-amd64` clone 或 rename 出新的 attacker VM，例如 `<attacker-vm>`。
3. 把新 attacker VM 設為 host-only first；需要 apt/Docker pull 時才短暫開 NAT，完成後關閉/驗證。
4. 只有在需要救舊 VM 狀態時，才做離線備份後再嘗試 VirtualBox GUI/CLI snapshot repair（例如從可用 snapshot clone 出新 VM，而不是直接編輯 registry）。

## 未執行的動作

我沒有啟動、修復、刪除、unregister、discard snapshot 或修改任何 VM。只做讀取、列舉、日誌檢查，以及停止一個先前卡住的 `VBoxManage list vms` 查詢行程。
