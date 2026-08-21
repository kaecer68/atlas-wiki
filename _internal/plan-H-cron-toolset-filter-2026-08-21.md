# Plan H — Cron Toolset 過濾（2026-08-21）

## §1 現況問題

- hermes 4 個 cron job（atlas-skill-inbound / trigger-monitor / session-self-check 等）
- 每個 cron 都用 **全量 24 個 tools**（59,112 B 每次 cron 都帶）
- cron 任務性質單一（特定查詢 / 特定寫入），大部分 tool 用不到

## §2 4 個 Cron Job 分析

| Cron | 排程 | 真實所需 tools | 全量 vs 需求 |
|------|------|--------------|------------|
| atlas-skill-inbound | 每日 04:00 | file, memory, web, session_search | 4 / 24 |
| trigger-monitor | 監聽 | delegation, memory, session_search | 3 / 24 |
| session-self-check | 排程 | session_search, memory, file | 3 / 24 |
| schedule-health-audit | 每日 | session_search, terminal | 2 / 24 |

**節省估算**: 每 cron 平均 -70% tool schemas

## §3 落地 SOP

### Week 3 Day 5（Plan H 落地）

1. **每個 cron job 改 config.yaml 加 `enabled_toolsets`**：
   ```yaml
   cron:
     atlas-skill-inbound:
       schedule: "0 2 * * *"
       enabled_toolsets: [content-toolset]
     trigger-monitor:
       schedule: "*/5 * * * *"
       enabled_toolsets: [governance-toolset, reporting-toolset]
   ```

2. **驗證**：
   - cron log 顯示 tool schemas size 下降
   - 任務成功率不變

## §4 風險與回退

- cron toolset 配置錯誤 → cron 失敗
- **回退**: 每個 cron 加 `fallback_toolset: general-toolset`

## §5 對位 Plan B

Plan B 的 toolset 定義直接用於本計畫，無需重複定義。

