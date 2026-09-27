---
title: SK-39 放空成本模型（atlas 對位版）
type: skill-inbound
source: SK-19 §未消化（融券/借券費）＋ SK-16 §未消化（融券限額/流動性折扣）；外部面 = TWSE 借券問答集、TWSE 宅在家學習網、FSC 函釋（皆 2026-09-27）
ingested_at: 2026-09-27
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [parameters_get, data_get_channels, data_get_field_contract, stock_get_chips, backtest_signals, universe_get_sessions, report_get_tax_snapshot]
verification: 2026-09-27 L3 實跑 16 端點 200＋4 端點 404（code 與 timestamp 見 §驗證方式）＋源碼 grep＋3 外部來源。四個已驗證的否定：①無借券費參數（1669 key 中 borrow/fee/sbl 各 0）②SBL 個股欄位存在但無工具/路由可達（115 工具 0 命中、候選路由全 404、資料只落 data/state/sbl/）③`sharpe_short` 非可實現報酬（無 borrow 成本欄、今日值 0）④放空可行性 0 命中。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-sk39-short-cost）
l3_endpoints_probed:
  - 200：/api/parameters、/api/field-contract、/api/dashboard/data-channels、/api/parameters/audit-log、/api/strategies、/api/capital-flow/daily
  - 200：/api/stock/chips?symbol=2330、/api/backtest/signals、/api/backtest/status、/api/dashboard/risk、/api/dashboard/risk-exposure、/api/dashboard/tax-snapshot、/api/dashboard/retail-sentiment、/api/dashboard/sessions (11:30:41Z)、/api/dashboard/sessions/session-20260927-daily (11:30:42Z)
  - 404：/api/stock/sbl?symbol=2330、/api/dashboard/sbl、/api/sbl/summary、/api/sbl/daily、/api/dashboard/sessions/latest（皆 11:30:47Z）
external_fetched: [TWSE sbl/qa.html、TWSE shl/trade/16.html、law.fsc.gov.tw GL001673 — 皆 200]
related: [skills/SK-19-cost-tax-adjustment.md, skills/SK-16-long-short-decile.md, skills/SK-37-liquidity-spread-screening.md]
---

## 一句話定位

散戶做空成本 **atlas 只算得到一半**：稅與手續費在 atlas，**借券費完全不在**；`sharpe_short` 是「無借券成本、無借券可行性」的數字，不是你可到手的報酬。

## 論文版概念

放空報酬 = 賣出價 − 買回價 − 五塊成本：**①借券費**（按日計：年率 × 天數 × 部位；SK-19 的 `total_cost = turnover × (avg_trading_cost + tax_rate)` **不含**）**②賣出證交稅**（0.3%；當沖 0.15%，見 SK-19）**③手續費**（雙邊，上限 0.1425%）**④價差／流動性**（中小型股單邊 1–3%；SK-37：atlas 無真實 bid/ask）**⑤可行性**（借不到券不是「貴」，是「做不了」）。

**不對稱**：空頭腿多一筆**不確定、可能暴增**的借券費，外加「做不了」。

## atlas 對位

| 成本塊 | 能否量化 | 證據（2026-09-27） |
|---|---|---|
| 賣出證交稅 | ✅ 0.3%／❌ 當沖 0.15% | `tax.transaction_tax_rate` 0.003（tax snapshot 每檔同值）；1669 key **無**當沖稅率鍵，0.15% 只能用 SK-19 的 2026-08-22 官方驗證 |
| 手續費＋滑價 | ⚠️ 僅混合值 | `baseline.avg_trading_cost` 0.00654、`transaction_cost_bps` 14.25、`stockpicker.costs.round_trip_pct` 0.00585 等；源碼 `internal/tax/taiwan_tax.go`：`RoundTripCost = turnover × (AvgTradingCost + TaxRate)`，**不區分買／賣** |
| **借券費** | ❌ 否定 1 | 1669 key 中 `borrow` 0、`fee` 0、`sbl` 0；源碼 `borrow_fee｜borrow_rate｜lending_fee` 0 命中 |
| 個股借券／融券餘額 | ❌ 否定 2 | field contract 有 `sbl_short_balance` 等 4 欄，但 115 個 MCP 工具 **0 個**觸及、4 條候選路由全 404；資料有抓（`data/state/sbl/` 144 檔、最新 `20260924_sbl.json` 2232 列）——**只落檔，不外送**；市場級 `short_balance`（`retail-sentiment` 2.02008）非個股、非成本 |
| `sharpe_short` | ❌ 否定 3 | `backtest_signals` 只回 `active_signals／var_95/99／sharpe_short／sharpe_long／drawdown_pct`，**無 borrow 成本欄**；今日 `sharpe_short` 0、`active_signals` null |
| 可行性（限額／券源） | ❌ 否定 4 | `平盤｜uptick｜short_sale_restriction｜no_short` 0 命中；`internal/strategy_ranker` 對 `short｜side` 0 命中；session 96 筆 outcome＋sessions 清單 78 筆 `top_strategies` 的 `side` **全空字串** |

### 平盤下不得放空（外部規則；atlas 0 命中）

- **TWSE 借券問答集**（2026-09-27 抓取）：自 **102-09-23** 起「得為融資融券交易之有價證券」的融券／借券賣出不受「不得低於前一營業日收盤價」限制；**但前一營業日收盤價為跌停者，當日不得於平盤以下融券及借券賣出**；ETF 與避險不受限。
- **FSC 函釋** `金管證投字第1040039488號`（民國 104-09-18）：**上市（櫃）股票及 TDR** 自 **104-09-21** 起不受該價格限制。兩份適用範圍本頁**不代為整合**。
- **對 bottom-decile 的意義**：卡住低分位標的的是 ①不是融資融券標的 ⇒ 不能融券 ②券源／額度 ③前一日跌停 ⇒ 當日禁平盤下放空。回測裡 D1 都空得到，現實裡有一批「空的池」是空的。

### 外部成本數字（2026-09-27）

- **借券費**：定價交易固定**年利率 3.5%**；競價／議借最高**年利率 16%**（升降單位 0.1%）；借貸服務費 **1.6%**、券商手續費 **0.4%**（皆按借券費用計）；期間 6 個月、可續借 2 次。
- **總量管制**：放空總額（借券＋融券）≤ 股份 **25%**、借券賣出 ≤ **10%**、每日盤中委託 ≤ 前 30 日均量 **30%**。
- **短差時標借費由融券人分攤**：最高標借單價 = 開盤競價基準 × **7%**（官方範例每股 0.03943 元）、議借上限 × **10%**；融券另有手續費／融券費，融券利息是券商**付給**投資人。
- 借券系統參加人限「國內外法人或基金」⇒ **散戶走融券（券商／證金公司）**，3.5%／16% ≠ 散戶實際券源成本。

## 散戶解讀

1. **自己扣借券費**：atlas 淨報酬只扣 turnover 成本；做空再加一層，**3.5% 年率當低標、16% 當天花板**，乘預計持有天數。
2. **先問能不能空再看划不划算**：是融資融券標的嗎？券源夠嗎？前一日跌停了嗎？
3. **不要信只做空的 Sharpe**：無借券成本、無可行性約束，今日（2026-09-27 snapshot）為 0。
4. **借券費是時間成本**：按日累計（收盤價 × 數量 × 費率），抱越久越貴——空頭策略要有時間上限。
5. **短差最貴**：融資餘額低於融券餘額會啟動標借、費用由融券人分攤（低分位股最常見）；要空就挑流動性好的（分位用 SK-37 自算）。

## 驗證方式

- **200**：`/api/parameters`（1669 key；`borrow`/`fee`/`sbl` 各 0）、`/api/field-contract`（2262 欄；`sbl_*` 4 欄）、`data-channels`（42 channel，含 `twse_sbl` enabled）、`stock/chips`（只回三大法人淨額）、`backtest/signals`（`sharpe_short` 0、`active_signals` null）、`sessions`（90 筆 2026-06-27～2026-09-27）、`session-20260927-daily`（96 outcome、`side` 全空、無 borrow/cost/fee 欄）、`parameters/audit-log`（`{"changes":null}`）。
- **404**：`/api/stock/sbl?symbol=2330`、`/api/dashboard/sbl`、`/api/sbl/summary`、`/api/sbl/daily`、`sessions/latest`（11:30:47Z、`route not found`）。
- 其餘 200（`risk`／`risk-exposure`／`tax-snapshot`／`retail-sentiment`／`strategies`／`backtest/status`／`capital-flow/daily`）與逐列 UTC 見 frontmatter `l3_endpoints_probed`。
- 重現：`curl -H "X-API-Key: $ATLAS_API_KEY" http://127.0.0.1:18080/api/parameters` → `borrow|fee|sbl` 應 0 命中；`/api/field-contract` 確認 `sbl_*` 欄位名存在（≠ 值可得）。

## 本頁不能主張什麼

- **不能說「台股可自由平盤下放空」或「一律禁止」**：2013 放寬與 2015 FSC 函適用範圍未整合，不代為判定個股。
- **不能說「散戶借券費 = 3.5%」**：3.5% 是借券系統公告費率；融券手續費率本頁**未取得**一級來源。
- **不能說「atlas 算得出含借券費的淨報酬」**：無參數、無欄位、無工具（否定 1–3）。
- **不能把市場級 `short_balance` 當個股放空量**，也不能把 `sharpe_short` 當可實現報酬。

## 未消化

- [ ] 散戶實際融券成本（融券手續費率、保證金成數、券源費率）未取得現行有效一級來源——本次查到的「融資融券額度／融券保證金成數」令已標「廢」「不再援用」，故不引用其數字。
- [ ] `data/state/sbl/` 的個股借券資料無 route、無工具 ⇒ 要變成可用訊號需 atlas 端接線（產品決策未定）。
- [ ] 標借費的**發生頻率**未量測（哪些標的常短差、實際分攤多少），需歷史回放。
- [ ] atlas 是否建 borrow-cost 參數，以及 `parameters_get_audit_log` 回 `{"changes":null}`（無法核對 `tax.transaction_tax_rate` 變更史）＝兩項待產品決策。
