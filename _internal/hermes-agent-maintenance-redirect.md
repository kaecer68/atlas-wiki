# hermes-agent 維護專案 — 已遷移

> **2026-08-22**：hermes-agent fork（Plan F/Plan B runtime）的安裝/維護/升級工作
> 已從 atlas-wiki 遷移至獨立專案，避免跨專案維護混淆（kaecer 指示）。

## 新位置

**專案**：https://github.com/kaecer68/hermes-agent-maintenance（private）

**本機路徑**：`~/workspace/hermes-agent-maintenance/`

## 內容

- `0001-feat-runtime-Plan-F-Plan-B-runtime-toolset-SOP.patch` — 主力 patch
- `install.sh` / `sync-hermes-agent.sh` / `check-conflicts.sh` — 工具 scripts
- `INSTALL.md` / `UPGRADE.md` / `MAINTENANCE.md` — SOP 文件
- `payload/` — Plan F 5 檔案最終版
- `.github/workflows/hermes-agent-sync.yml` — 每週一自動同步 CI

## 本檔（atlas-wiki）保留原因

atlas-wiki 專注於知識引擎本身；此 redirect 檔僅為歷史指引，避免舊路徑迷航。
