---
title: WP-2 報告 — trigger 模板修復（6 失效/矛盾 + 1 分類錯植 + 1 憲章用語）
worker: prime-agent 子代理（WP-2 trigger 修復工）
date: 2026-08-22
scope: templates/ 白名單 8 檔
method: 逐檔精準替換（edit skill 原則）；改動前 cp <file>.bak.20260822-audit-fix；frontmatter key 與整體結構不動；每個修改處標 [2026-08-22 audit-fix]；只用任務書事實正本，未自行發明數字
result: 7 檔修改完成（bytes 見下）；T7 經實證為審計誤植，白名單檔無錯植內容，未改動（見 §T7）
---

# WP-2 報告 — trigger 模板修復

## 總表（before → after bytes）

| 檔 | before | after | Δ | 狀態 |
|----|--------|-------|---|------|
| templates/trigger-foreign-3day-inflow.md | 749 | 1077 | +328 | ✅ 已修（T1） |
| templates/trigger-etf-rebalance.md | 771 | 1170 | +399 | ✅ 已修（T2） |
| templates/trigger-retail-margin-decrease.md | 806 | 1334 | +528 | ✅ 已修（T3） |
| templates/trigger-msci-rebalance-pressure.md | 7650 | 8062 | +412 | ✅ 已修（T4） |
| templates/trigger-sox-foreignflow.md | 746 | 1025 | +279 | ✅ 已修（T5） |
| templates/trigger-tariff-shock.md | 785 | 1352 | +567 | ✅ 已修（T6） |
| templates/trigger-2330-tsmc-swing.md | 5409 | 5409 | 0 | ⚠️ 未改動（T7 誤植實證，見下） |
| templates/trigger-megaproject-2-quarter-lag.md | 9682 | 9823 | +141 | ✅ 已修（T8） |

備份：7 個修改檔皆已 `cp <file> <file>.bak.20260822-audit-fix`（T7 未動刀故無備份）。
相容性：此 8 檔為純 markdown，無 YAML frontmatter；`skills/_scripts/atlas-mcp-trigger-monitor.py` 用自有 TEMPLATES dict（不解析 .md 內文），結構未動，相容性不受影響。Step 1-4 標題 / §1-§10 標題全數保留。

## T1 trigger-foreign-3day-inflow.md（檔名/策略名 3day vs 單日條件矛盾）

- 標題：`(單日版)` → `(3日版)`。
- 觸發條件：`foreign_investor_net > +20 億台幣` → `外資現貨連續 3 日累計買超 > +100 億台幣`（對位 concepts/taiwan-chip-flow-analysis.md「單日 100 億以上為大動作」口徑；已實證該檔 §3.1/§4.1 有此口徑）。
- hit_rate 0.37 保留，加註「舊單日 +20 億條件快照 [2026-08-22 audit-fix]」。
- Step 1 2026-08-03 快照（+21.83 億）標為舊快照、未達新門檻，舊「✅(觸發 > 20)」判定刪除。

## T2 trigger-etf-rebalance.md（恆真條件「成交量 > 0」）

- 標題：`(單日版)` → `(事件日曆型)`。
- 觸發條件：刪除「市場成交量 > 0」恆真條件 → `ETF 成份股調整公告日觸發 → 生效日前 5 個交易日佈局`。
- `etf_net_subscription 0(API 未提供即時)` → `[PENDING — ETF 申購資料 API 未提供]`。
- Step 3 建議改事件驅動表述（公告 → 生效日前 5 個交易日佈局）。
- 新增說明段：本模板為**事件日曆型,非資料觸發型**，無 ETF 申購 API 下無法以資料驗證。
- 舊 2026-08-03 快照保留標舊快照。

## T3 trigger-retail-margin-decrease.md（標題「融資大減」vs 條件「融資 > 5000 億高水位」方向相反 + margin-350b 複製品）

- 標題：`(單日版)` → `(衰竭訊號版)`。
- 觸發條件改為：`融資餘額較近 60 日高點減少 > 15%,且近 5 日不再大減`（對位 ATLAS_METHODOLOGY.md §三 低迷期指標；已實證憲章原文「融資餘額 | 較高點減少 > 15%，且近 5 日不再大減」）。
- Step 3 建議反轉為衰竭訊號表述（低迷末端布局參考），刪除「融資 > 5000 億 → 減倉 30%」過熱方向建議。
- 說明段寫清與 trigger-margin-350b 差異：350b = 過熱警訊（多頭末端）；本檔 = 衰竭訊號（低迷末端布局參考）。
- Step 1 舊高水位快照標舊快照（未做 60 日高點減幅判定）。

## T4 trigger-msci-rebalance-pressure.md（反向機制自相矛盾 + 漏 5 月 + 8 月生效日錯）

- 月份：`公告日(2/8/11 月)` → `(2/5/8/11 月)`（2 處：對位端點 + 觸發條件）。
- 生效日：`公告後 5 個交易日內` → `檢討月月底生效日尾盤`；Step 1「2026/8 公告 = 11月生效」→ `2026/8 檢討 → 8 月底生效(非 11 月)`。
- 機制修正（3 處）：權重**下調** > 1.5pp → 被動 ETF 被迫**減持** → 生效日尾盤被動賣壓；權重**上調** → **增持(買壓)** 非減持。原「Samsung/SK Hynix 權重飆升 → 被動 ETF 被迫減持」自相矛盾鏈已改為「權重下調 → 被迫減持」。
- 反向觸發標為本模板主場景（下調賣壓）。

## T5 trigger-sox-foreignflow.md（SOX > 0% 擲硬幣級門檻）

- 觸發條件：`SOX change > 0%(收紅) + 當日外資買超` → `SOX 單日 > +1.5% 且站回 50 日線 + 當日外資買超 > 50 億`（對位憲章 §五 Layer 2「SOX 在 50 日線下不做多」；已實證）。
- hit_rate 0.33 保留，加註「舊 SOX > 0% 條件快照 [2026-08-22 audit-fix]」。
- Step 1 舊快照（SOX +0.07% / 外資 +21.83 億）標舊快照、未達新門檻。

## T6 trigger-tariff-shock.md（名為關稅但條件無關稅變數）

- 新增主條件：`narrative detector tariff_shock 觸發(關稅新聞事件)`。
- USD_TWD > 32 + 出口電子指數 > 0 降格為「確認條件」。
- Step 1 舊快照標確認條件成立、tariff_shock 主條件需以 narrative detector 驗證。
- 說明段：原條件不含任何關稅變數、名實不符，2026-08-22 修正為事件主條件 + 經濟變數確認條件。

## T7 trigger-2330-tsmc-swing.md（審計 M21 誤植 — 本檔未動）

**實證結論**：任務書所述錯植內容「2329 + 2363 + 2379 矽晶圓 / 封測 / 光罩」**不存在於白名單檔** templates/trigger-2330-tsmc-swing.md（全文 grep：2329/2363/2379 均 0 命中；檔內唯一 4 碼數字為 1445/2026/2303/2330/2370/2454；mtime 2026-08-04，非本次審計期間改動）。

**實際位置**（皆在白名單外，依規範「範圍外一字不改」未動）：
- `entities/l1-t2-petrodollar-hormuz.md` §8.1：「**2329 + 2363 + 2379 矽晶圓 / 封測 / 光罩**:次級衝擊,觀望」— 含原句。
- `raw/papers/atlas-original-paper-v0.1-L1T-multi.md` §8.1：同句（原文出處）。
- 審計 child-B M21 把該句誤植掛在 templates/trigger-2330-tsmc-swing.md 名下，應為盤查歸檔錯誤。

**建議後續**（需主 agent 擴大白名單或另行派工後才能落地）：在上述兩檔將該句改為任務書正本對應：
「矽晶圓：6488 環球晶、3532 台勝科；封測：2329 華泰、3711 日月光投控；光罩：2338 台灣光罩；IC 設計：2379 瑞昱、2363 矽統（若保留需標 IC 設計）」

## T8 trigger-megaproject-2-quarter-lag.md §7（E5a 策略類別誤當憲章 archetype）

- `| 策略三分類 | 對位 Aggressive(押 AI 供應鏈),不用於 Defensive / Tactical |` → `| 策略 archetype 對位 | **跟隨聰明錢**(押 AI 供應鏈的聰明錢流入);E5a 策略類別 = Aggressive。archetype 三分類正本 = 跟隨聰明錢／事件套利／資金對抗(AGENTS.md §12) |`。
- §9「Aggressive 配置仍需時點 + 配置規則」為 E5a 類別合法引用，未動。

## 未動範圍備註（後續待辦，非本次白名單）

- `skills/_scripts/atlas-mcp-trigger-monitor.py` TEMPLATES dict 內條件仍為舊值（foreign-3day threshold 20、sox threshold 0、etf-rebalance market_volume > 0、retail-margin-decrease > 5000 億等）— 與本次模板修正不一致，建議主 agent 另派工同步（該檔不在白名單）。
- 所有 2026-08-03 / 2026-08-09 舊快照均標「舊快照」保留，未刪（歷史對位軌跡）。
