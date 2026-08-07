---
title: SK-35 atlas-mcp 失敗時 4 級 fallback 鏈(2026-08-07 D4 v1.0)
type: skill-inbound
source: concepts/atlas-mcp-failover-policy.md(2026-08-07 v1.0)
ingested_at: 2026-08-07
status: active
tier: T2
confidence: high
atlas_go_relevance: high
mcp_tools_used: [system_get_circuit_breaker, system_get_health, system_get_data_pipeline]
verification: 對位 concepts/atlas-mcp-failover-policy.md §4 4 級鏈 + hermes `data-source-decision` §3 三層架構;L3 Step 1 用 `system_get_circuit_breaker` 確認熔斷狀態(已實跑,atlas-go 端);Step 2 用 `system_get_health` 確認系統層級
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §三(對外發布規範)
related:
  - concepts/atlas-mcp-failover-policy.md(政策本體)
  - summaries/_division_of_labor_skills_vs_agent.md(分工)
  - skills/SK-33-audience-routing.md(audience 切換)
  - skills/SK-34-listed-otc-routing.md(範圍分流)
  - ~/.hermes/skills/data-source-decision/SKILL.md(三層架構)
---

<!-- methodology_alignment_tip: 三 audience + 4 級 fallback + 來源標籤強制;對位 SK-00 §1 三條 pipeline 之外的元能力 -->

## 一句話定位

atlas-mcp 不在 atlas 範圍(上市/上櫃之外)或端點失敗時,**走 4 級 fallback 鏈**,任何引用強制附來源標籤 `[來源: atlas-mcp <tool_name> @ <ISO 8601>]` 或 `[來源: <站名> @ <URL> @ <ISO 8601>]`。

## 4 級 fallback 鏈(對位 failover-policy.md §4)

### Level 1:atlas-mcp(範圍內)
- **觸發**:用戶問上市/上櫃標的(2330/6488 等)
- **動作**:調 `stock_get_fundamentals` / `stock_get_quote` / `stock_get_technical` / `stock_get_chips` / `industry_sector_lookup`
- **標籤**:`[來源: atlas-mcp stock_get_fundamentals @ 2026-08-07T02:10+08:00]`
- **失敗訊號**:atlas 回 5xx / circuit_breaker / not_available → 走 L2

### Level 2-A:TPEx 公開網站(興櫃/上櫃但 atlas 失敗)
- **觸發**:atlas 失敗 + 用戶問興櫃 / 上櫃
- **動作**:curl TPEx 公開報價 API 或網頁爬取
- **標籤**:`[來源: TPEx 興櫃 https://www.tpex.org.tw/... @ 2026-08-07T...]`
- **風險**:15 分鐘延遲,atlas owner 不負責資料品質

### Level 2-B:Yahoo Finance / Investing.com(海外 / 一般)
- **觸發**:用戶問美股 / 港股 / 大陸股 / ETF 期權 / 加密貨幣
- **動作**:curl 公開端點
- **標籤**:`[來源: Yahoo Finance https://query1.finance.yahoo.com/... @ 2026-08-07T...]`
- **風險**:rate limit(公開 API 可能被擋),備援 = 公開網站 / 政府開放資料

### Level 3:不知道(誠實標示)
- **觸發**:用戶問未知標的,或在 L1+L2 都失敗
- **動作**:**不假裝,不猜測** → 標 `[來源: 不知道]` + 引導用戶補代碼 / 補來源
- **對位 SK-33**:user 看到的是「抱歉,沒有這標的資料,請提供代碼」;admin 看到的是「L1 失敗 5xx,L2-A 失敗 timeout,L2-B rate limit 429,L3 觸發,audit 全記錄」

## atlas 對位

| 場景 | 觸發 | 路徑 | 標籤格式 |
|---|---|---|---|
| 用戶問 2330 | 上市 | L1 atlas-mcp | `[來源: atlas-mcp <tool> @ <ISO>]` |
| 用戶問 6488 | 上櫃 | L1 atlas-mcp(Fugle→TWSE fallback 已 v6.43 修) | `[來源: atlas-mcp <tool> @ <ISO>]` |
| atlas 失敗 503 | 系統熔斷 | L2-A TPEx / L2-B Yahoo | `[來源: <站名> @ <URL> @ <ISO>]` |
| 用戶問 NVDA | 海外 | L2-B Yahoo | `[來源: Yahoo Finance @ <URL> @ <ISO>]` |
| 用戶問 興櫃 XYZ | 範圍外 | L2-A TPEx 興櫃 | `[來源: TPEx 興櫃 @ <URL> @ <ISO>]` |
| 用戶問 比特幣 | 非股票 | L2-B Investing.com | `[來源: Investing.com @ <URL> @ <ISO>]` |
| 用戶問 未知標的 | 沒有資料 | L3 不知道 | `[來源: 不知道]` |

## 散戶解讀(對位 SK-33)

- **散戶**:`[來源: 不知道]` → 看到「抱歉沒有資料,請提供代碼」,**不看到 error code**
- **開發者**:`[來源: atlas-mcp stock_get_quote 503 @ ...]` → 看到完整端點錯誤
- **管理者**:`[來源: L1→L2-A→L2-B→L3 全鏈 audit @ ...]` → 看到所有 fallback 嘗試

## 驗證方式

### L3 端點實跑(2026-08-07)
- [ ] `system_get_circuit_breaker` → 200,確認 atlas-go 熔斷狀態(已實跑)
- [ ] `system_get_health` → 200,確認系統健康(已實跑)
- [ ] `system_get_data_pipeline` → 200,確認資料管線狀態(已實跑)
- [ ] curl Yahoo Finance NVDA → 200,確認 L2-B 可用
- [ ] curl TPEx 興櫃 任一標的 → 200,確認 L2-A 可用

### 來源標籤驗證
- [ ] 每個回答必含 `[來源: ...@ ISO 8601]`
- [ ] 失敗訊息對 audience 分級(散戶 vs 管理者)

## 未消化 / 待補

- [ ] Yahoo Finance / TPEx rate limit 實測
- [ ] 加密貨幣可靠公開源選定
- [ ] 對位 `agent://` 跨 session 標籤一致性(若用戶跨 session 引用同一標籤,需可追溯)
- [ ] 對位 SK-34 上市/上櫃分流優先序(哪個先走?)
- [ ] 對位 SOUL §3.7.3 第 6 條邊界(改 hermes runtime 設定不外推,本檔已對位)

amendable_by: kaecer