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
verification: 2026-09-27 L3 實跑 16 端點 200＋5 端點 404（見 §驗證方式）＋源碼 grep＋4 外部來源（含 TWSE 操作辦法 115.01.09）。四個已驗證否定：①無借券費參數（1669 key 中 borrow/fee/sbl 各 0）②SBL 個股欄位存在但無工具可達（115 工具 0 命中、路由全 404、只落 data/state/sbl/）③`sharpe_short` 非可實現報酬 ④放空可行性 0 命中。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-sk39-short-cost）
l3_endpoints_probed:
  - "200：/api/parameters、/api/field-contract、/api/dashboard/data-channels、/api/parameters/audit-log、/api/strategies、/api/capital-flow/daily（2026-09-27T19:30:41+08:00 起，同批 19:31:04 止）"
  - "200：/api/stock/chips?symbol=2330、/api/backtest/signals、/api/backtest/status、/api/dashboard/risk、/api/dashboard/risk-exposure、/api/dashboard/tax-snapshot、/api/dashboard/retail-sentiment、/api/dashboard/sessions (11:30:41Z)、/api/dashboard/sessions/session-20260927-daily (11:30:42Z)（2026-09-27T19:30:41+08:00 起，同批 19:31:04 止）"
  - "404：/api/stock/sbl?symbol=2330、/api/dashboard/sbl、/api/sbl/summary、/api/sbl/daily、/api/dashboard/sessions/latest（皆 11:30:47Z）（2026-09-27T19:30:41+08:00 起，同批 19:31:04 止）"
external_fetched: [TWSE sbl/qa.html、TWSE shl/trade/16.html、law.fsc.gov.tw GL001673 — 皆 200]
related: [skills/SK-19-cost-tax-adjustment.md, skills/SK-16-long-short-decile.md, skills/SK-37-liquidity-spread-screening.md]
---

## 一句話定位

散戶做空成本 **atlas 只算得到一半**：稅與手續費在 atlas，**借券費完全不在**；`sharpe_short` 無借券成本與可行性約束，不是可到手報酬。

## 論文版概念

放空報酬 = 賣出價 − 買回價 − 五塊成本：**①借券費**（按日計；SK-19 的 `total_cost` **不含**）**②證交稅**（0.3%；當沖 0.15%）**③手續費**（雙邊 ≤0.1425%）**④價差／流動性**（中小型股單邊 1–3%；SK-37）**⑤可行性**（借不到券是「做不了」，不是「貴」）。

**不對稱**：空頭腿多一筆**不確定、可能暴增**的借券費，外加「做不了」。

## atlas 對位

| 成本塊 | 能否量化 | 證據（2026-09-27） |
|---|---|---|
| 賣出證交稅 | ✅ 0.3%／❌ 當沖 0.15% | `tax.transaction_tax_rate` 0.003；1669 key **無**當沖稅率鍵，0.15% 只能用 SK-19 的 2026-08-22 官方驗證 |
| 手續費＋滑價 | ⚠️ 僅混合值 | `baseline.avg_trading_cost` 0.00654、`transaction_cost_bps` 14.25、`round_trip_pct` 0.00585；`internal/tax/taiwan_tax.go` `RoundTripCost` **不區分買／賣** |
| **借券費** | ❌ 否定 1 | 1669 key 中 `borrow`/`fee`/`sbl` 皆 0；源碼 `borrow_fee|borrow_rate|lending_fee` 0 命中 |
| 個股借券／融券餘額 | ❌ 否定 2 | field contract 有 `sbl_*` 4 欄，但 115 個 MCP 工具 0 個觸及、候選路由全 404；資料有抓（`data/state/sbl/` 144 檔、最新 2232 列）**只落檔不外送** |
| `sharpe_short` | ❌ 否定 3 | `backtest_signals` 回 `active_signals／var_95/99／sharpe_short／sharpe_long／drawdown_pct`，**無 borrow 成本欄**；今日均 0／null |
| 可行性（限額／券源） | ❌ 否定 4 | `平盤|uptick|short_sale_restriction|no_short` 0 命中；`strategy_ranker` 對 `short|side` 0 命中；96 筆 outcome ＋ 78 筆 `top_strategies` 的 `side` **全空** |

### 平盤下不得放空（外部規則）

- **TWSE 借券問答集**（2026-09-27 抓）：**102-09-23** 起融資融券標的之融券／借券賣出不受「不低於前一日收盤價」限制；**惟前一日跌停者，當日不得平盤下融券及借券賣出**；ETF／避險不受限。
- **FSC 函釋** `金管證投字第1040039488號`（104-09-18）：上市（櫃）股票及 TDR 自 **104-09-21** 起不受該限制。兩份**不代為整合**。
- **對 bottom-decile**：卡住低分位標的 = ①非融資融券標的 ②券源／額度 ③前一日跌停 ⇒ 當日禁平盤下放空。回測 D1 都空得到，現實有一批「空的池」。

### 外部成本數字（2026-09-27）

**散戶融券成本（來源：`concepts/tw-short-cost-sources.md`）**：**融券手續費**＝券商以融資買進證券供融券賣出時收取（**辦法未定費率**）；**融券費**＝以借入券／自有券供融券賣出時收取，**年利率 ≤16%、須議定**（辦法 **115.01.09＝2026-01-09**）；短差標借／議借／標購費用**由融券人負擔**（第 52 條）。「0.08%」原文 0 命中 ⇒ 實務慣例。

**SBL 借券（法人；散戶不可得）**：定價 3.5%／競價議借 ≤16%／服務費 1.6%／手續費 0.4%；總量管制 25%／10%／30%；短差標借上限＝開盤基準 ×7%、議借 ×10%（融券人分攤）；限法人／基金。**出處見來源頁。**

## 散戶解讀

1. **自己扣借券費**：atlas 淨報酬只扣 turnover 成本；散戶做空再加**融券手續費（券商訂）＋融券費（≤16% 年利率、須議定）**×持有天數——**3.5% 是法人費率，非散戶低標**。
2. **先問能不能空**：是融資融券標的？券源夠？前一日跌停？
3. **不要信只做空的 Sharpe**：無借券成本、無可行性約束（今日值 0）。
4. **借券費是時間成本**：按日累計（收盤價 × 數量 × 費率），抱越久越貴 ⇒ 空頭策略要設時間上限。
5. **短差最貴**：融資餘額低於融券餘額會啟動標借、費用由融券人分攤（低分位股最常見）⇒ 要空就挑流動性好的（分位用 SK-37 自算）。

## 驗證方式

- **200**：`parameters`（1669 key；`borrow`/`fee`/`sbl` 各 0）、`field-contract`（2262 欄；`sbl_*` 4 欄）、`dashboard/data-channels`（42，含 `twse_sbl`）、`stock/chips`（只回三大法人）、`backtest/signals`（`sharpe_short` 0、`active_signals` null）、`dashboard/sessions`（90 筆）、`sessions/session-20260927-daily`（96 outcome、`side` 全空）、`parameters/audit-log`（`{"changes":null}`）。
- **404**：`stock/sbl`、`dashboard/sbl`、`sbl/summary`、`sbl/daily`、`sessions/latest`（11:30:47Z，`route not found`）。
- 其餘 200（`risk`／`risk-exposure`／`tax-snapshot`／`retail-sentiment`／`strategies`／`backtest/status`／`capital-flow/daily`）與逐列 UTC 見 frontmatter `l3_endpoints_probed`。
- 重現：`curl -H "X-API-Key: $ATLAS_API_KEY" …/api/parameters` → `borrow|fee|sbl` 應 0 命中；`/api/field-contract` 確認 `sbl_*` 欄位名存在（≠ 值可得）。

## 不能主張什麼

- **不能說「台股可自由平盤下放空」或「一律禁止」**：102 放寬與 104 FSC 函未整合，不代判個股。
- **不能說「散戶借券費 = 3.5%」**：3.5% 是借券系統（限法人／基金）的定價費率；散戶走融券 ⇒ 成本＝券商訂定的**融券手續費** ＋ 議定的**融券費（年利率 ≤16%）**，短差費用另由融券人負擔（`concepts/tw-short-cost-sources.md`）。
- **不能說「atlas 算得出含借券費的淨報酬」**：無參數／欄位／工具（否定 1–3）。
- **不能把市場級 `short_balance` 當個股放空量**，也不當 `sharpe_short` 為可實現報酬。

## 未消化

（原第 1 項「散戶實際融券成本未取得一級來源」已於 2026-09-27 解，移出本段 ↓）

> **2026-09-27 已解（移出 §未消化）**：已取得**現行有效一級來源**＝《證券商辦理有價證券買賣融資融券業務操作辦法》**版本 115.01.09（2026-01-09）**（TWSE 法規查詢站，本機同日實抓 200、183 KB）。散戶成本結構 = **融券手續費**（辦法未定費率，由券商訂定）＋ **融券費**（**年利率 ≤16%，須議定**）＋ **短差標借／議借／標購費用由融券人負擔**（第 52 條）。另核實：「0.08%（萬分之八）」在辦法原文 **0 命中** ⇒ 屬券商實務慣例；「舊版 20%」在該頁條文中**查無**作為費率上限者 ⇒ 不引用。逐條引文見 `concepts/tw-short-cost-sources.md`。
- [ ] `data/state/sbl/` 個股資料無 route／無工具 ⇒ 需 atlas 端接線（atlas-go #2093，產品決策未定）。
- [ ] 標借費的**發生頻率**未量測（哪些標的常短差、實際分攤多少），需歷史回放。
- [ ] atlas 是否建 borrow-cost 參數（atlas-go #2094）；`parameters/audit-log` 回 `{"changes":null}` ⇒ 無法核對稅率變更史。
