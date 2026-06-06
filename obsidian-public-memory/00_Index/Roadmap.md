> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Roadmap

## Cybersec Lab 長期方向

- 建立可擴充、可更新、系統化的授權 bug bounty / pentest / 防禦自動化平台；自動化是長期目標的核心，不只是輔助：preview/recon context → 選 module bundle 或 bounded script combination → gated execution → review → modularize → evidence/report-readiness。
- 嚴格 scope / program policy gate
- 模組化 vulnerability checks / scripts，讓成功的 local-lab 檢查可在未來授權範圍內被 policy-gated invocation 重用
- 掃描結果只作 triage，需經人工/agent review 才能進入 confirmed findings
- Hermes 協調，Codex 實作，Claude/Cowork 獨立審查

## 近期階段

- Phase 1: program scope / rules / policy decision runtime integration
- Phase 2: module manifest / runner architecture
- Phase 3: structured findings / evidence / report pipeline
- Phase 4A: controlled local-lab calibration before real bug-bounty activation
- Phase 4B: OWASP Top 10 modular lab-check library and lab-to-review/report-readiness workflow
- Phase 4C: one-program authorized bug-bounty private-beta planning only after explicit scope/rules/approval gates
