# hermes gateway multiplex migration — 2026-09-27 已收斂至單一 default multiplexer

> **2026-09-27**：8 個 profile（call-center / cio / consultant / mis / qc / reporter / vip / default）
> 的 per-profile gateway 已收斂到單一 default multiplexer gateway（launchd supervised）。
>
> 變更摘要、驗證結果、24–72h 觀察項、rollback SOP 詳見 atlas-notes SSOT。

## 為何放 atlas-notes 而非本檔展開

- atlas-wiki 專注於「散戶 AI 實戰金融工程」知識引擎（AGENTS.md §0 mission）；
  本檔僅作 redirect，避免 ops 紀錄稀釋 wiki 內容純度。
- SSOT 在 atlas-notes/03-system-health/hermes-gateway-multiplex-migration-2026-09-27.md；
  rollback 依據 SSOT 的 manifest 路徑，非本檔。
- 對位 precedent：`_internal/hermes-agent-maintenance-redirect.md`（2026-08-22 遷移指引同型態）。

## 新位置

**本機路徑**：`~/workspace/atlas-notes/03-system-health/hermes-gateway-multiplex-migration-2026-09-27.md`

**SSOT runtime artifacts**：
- `~/.hermes/config.yaml`（`gateway.multiplex_profiles: true`）
- `~/.hermes/gateway_migration.json`（rollback manifest, version=1, migrated_at=2026-09-27T11:42:55+0800）

## 變更一句話

`hermes update` 觸發 `hermes gateway migrate --multiplex`，把 8 個 profile 的
獨立 launchd gateway 收成一個 multiplexed default gateway；新 PID 63056，
`hermes gateway list` 確認 8/8 profiles served。

## 本檔（atlas-wiki）保留原因

僅作跨專案索引（atlas-wiki ←→ atlas-notes 雙向對位），
避免未來 session 從 wiki 入口查 gateway 狀態時迷航。

**Last updated**: 2026-09-27 by oz agent（per kaecer request: "Add the migration record to atlas-wiki as a git-tracked reference."）