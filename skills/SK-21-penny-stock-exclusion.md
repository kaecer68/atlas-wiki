---
title: SK-21 排除仙股穩健性檢驗
description: "問「這策略賺的錢是否都來自低價股」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-21
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [industry_sector_list, industry_sector_lookup, stock_get_quote, stock_get_fundamentals]
verification: 2026-08-01 v0.9 結算跑過 L3 升 active:industry_sector_list 38 個產業;industry_sector_lookup(2330)→半導體 12 成分股;stock_get_quote(2330 2026-08-01 23:42) last=2425/high 2425/low 2345;stock_get_fundamentals(2330) PE 30.19/PB 9.57/sector=semiconductor;**atlas 無「市值分組」端點**,台股 1 張=1000 股的最小交易單位需 client 端修補。[2026-09-27 更正:原寫「用 stock_get_fundamentals 算市值」不成立——該端點無市值欄位;且 lot 約束在 atlas 源碼有實作但 0 生產呼叫者,見 SK-17 §驗證方式。][2026-09-27 batch#4:6 端點全 200。`stock_get_quote`(2330) 今日 **last=2475／volume=12989000**（2026-08-01 快照 2425 已過期）;`stock_get_technical` 有 `volume` 14557662（date 2026-09-24）;**`stock_get_chips` 仍只回三大法人淨額、無 volume**（工具更正成立）;`industry_sector_list` 複驗 **38 產業**;`stock_get_fundamentals` 仍無市值。見 §驗證方式。]
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b4）
l3_endpoints_probed:
  - /api/stock/quote?symbol=2330 → 200 (2026-09-27T20:13:25+08:00)
  - /api/stock/technical?symbol=2330&days=10 → 200 (2026-09-27T20:13:25+08:00)
  - /api/stock/chips?symbol=2330 → 200 (2026-09-27T20:13:25+08:00)
  - /api/industry/sectors → 200 (2026-09-27T20:13:26+08:00)
  - /api/stock/fundamentals?symbol=2330 → 200 (2026-09-27T20:13:25+08:00)
  - /api/dashboard/risk → 200 (2026-09-27T20:13:25+08:00)
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:仙股排除需對位 7 時期,不同時期仙股風險溢價不同)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
---

> 口徑註：原「電子股 80% < 20 元／金融股 80% > 20 元」與「P20 10-15 元」為未實證推測（2026-08-22）;已由下條 TWSE 實測推翻。
> [2026-08-23 TWSE 實測] 上市+上櫃 2026-08-21 收盤全量 1954 檔（TWSE openapi + TPEX openapi,非抽樣）:電子股 904 檔 <20 元僅 12.6%（原 80% 斷言不成立,實為 87.4% ≥20）;金融股 38 檔 >20 元 71.1%（80% 未達）;全市場 P20=19.70 元（原預期 10-15 元區間偏低,實值近 20 元）[2026-08-23 實測:修正]

## 一句話定位
SK-21 在 atlas 是「策略會不會被仙股污染」的真值檢驗——剔除最低價 20% 股票重跑,若策略績效大幅衰退,代表 alpha 來自小股操縱/雜訊,實盤不可行。

## 論文版概念（忠實還原來源）
- **核心**:把每月股價最低 20% 股票剃掉,重新評估策略
- **輸入**:data(含股價/報酬/預測值)、`percentile_threshold=0.2`、strategy_func
- **動作**:
  1. 每月算股價第 20 百分位數
  2. 剔除股價 < 該分位數的股票
  3. 在篩選後樣本上重跑 strategy_func
  4. 輸出排除前後差異
- **為何重要**:**仙股流動性差、操縱成本低、報價雜訊大**,任何在仙股上有顯著 alpha 的策略,實盤執行成本會吃掉所有利潤
- **散戶盲點**:台股「飆股故事」多發生在 < 20 元仙股;散戶看到「策略年賺 100%」就買,其實是仙股拉動,實盤跟不上

## atlas 對位
| 論文概念 | atlas-mcp 對位 | tool_name |
|---------|---------------|-----------|
| 股價資料 | 報價序列 | `stock_get_quote` |
| 市值確認 | **無對位**:fundamentals 無 `market_cap`（2026-09-27 實測） | 缺 |
| 排除後回測 | backtest 序列 | `backtest_signals` |
| 效果對比 | risk metrics | `risk_get_metrics` |
| 排除名單規則 | 需 client 端實作 percentile filter | 缺(client) |

**差異點**:論文是純 Python 操作,atlas 沒有「價格百分位篩選」端點,需 client 端算每月第 20 百分位 + 過濾。

**沒有對位的部分**:
- 沒有「百分位篩選」endpoint
- 沒有「流動性指標」endpoint(流動性比股價更該看;**成交量取自 `stock_get_quote`／`stock_get_technical`,`stock_get_chips` 只回三大法人淨額** [2026-09-27 更正]）
- 沒有「操縱風險標記」endpoint

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「這策略 1 年賺 80%,要不要跟?」→ 反問「賺的錢從哪幾檔來?若多數 < 20 元,實盤你買不到足夠數量」。
- **R 段**:對位 atlas → 「`stock_get_quote` 拿現價 → client 端算每月第 20 百分位 → 排除後重跑 `backtest_signals` → `risk_get_metrics` 對比」。
- **+E 段**:警示「**排除仙股後若 Sharpe 從 2.0 掉到 0.3,這策略就別碰**;若 Sharpe 維持 1.5 以上,才是真 alpha」。對位 ATLAS_METHODOLOGY 七時期:仙股 alpha 在 RISK_ON 上升期特別亮眼(因為投機熱),在 RISK_OFF 黑天鵝期直接歸零——**散戶若只看到上升期就跑進去,實盤遇到一次黑天鵝就畢業**。
- 散戶實務:台股 1 張 = 1000 股,股價 < 10 元要 1 萬本金才買得到 1 張 ⇒ **「等權」在小資族的仙股上不可行**。

## 驗證方式
Step 1: 呼叫 `stock_get_quote` 取 universe 全股票現價,client 端算第 20 百分位閾值(2026-08-23 TWSE 全量實測:2026-08-21 收盤 P20=19.70 元;原預期 10-15 元偏低)。
Step 2: client 端用 `universe_get_sessions` 拿策略名單,排除股價低於閾值的股票。
Step 3: 對排除前/後各跑一次 `backtest_signals`,呼叫 `risk_get_metrics` 對比 Sharpe / 換手率 / max_drawdown。**2026-09-27 實測:`backtest_signals` 回 `active_signals:null`、sharpe 全 0 ⇒ 今日算不出,須等回測序列恢復。**

### L3 端點實跑（2026-09-27,本 PR;每列附 http_code 與 UTC+0800 時戳）

| 端點（GET 127.0.0.1:18080） | http_code | 今日實測結果 | timestamp |
|---|---|---|---|
| `/api/stock/quote?symbol=2330` | 200 | last=2475、open 2480／high 2490／low 2470、**volume 12989000**、as_of 2026-09-27T12:13:25Z | 2026-09-27T20:13:25+08:00 |
| `/api/stock/technical?symbol=2330&days=10` | 200 | **volume 14557662**（date 2026-09-24）;rsi14／sma20／sma50 皆 0（未算,非「無波動」） | 2026-09-27T20:13:25+08:00 |
| `/api/stock/chips?symbol=2330` | 200 | 只回 foreign_investor_net -4667.832／domestic_fund_net -1287.718／dealer_net 242.701;**無 volume 欄位** | 2026-09-27T20:13:25+08:00 |
| `/api/industry/sectors` | 200 | **38 產業**,與 2026-08-01 記載一致 | 2026-09-27T20:13:26+08:00 |
| `/api/stock/fundamentals?symbol=2330` | 200 | PE 30.19／PB 9.57／Sector semiconductor（**無市值**;與 2026-07-30 同值 ⇒ 靜態快照） | 2026-09-27T20:13:25+08:00 |
| `/api/dashboard/risk` | 200 | var_95=0、insufficient_data=1 ⇒ 排除後 Sharpe/VaR 今日**無值可對比**（0 是資料不足） | 2026-09-27T20:13:25+08:00 |

**今日結論（皆 2026-09-27 實跑）**
1. **工具歸屬確認（2026-09-27 更正成立）**:成交量在 `stock_get_quote`（volume 12989000）與 `stock_get_technical`（14557662）,**`stock_get_chips` 只有三大法人淨額** ⇒ 本頁「用 chips 取成交量」的舊寫法確實錯,已改。
2. **股價快照會過期**:2330 last 由 2026-08-01 的 2425 變今日 2475（+2.1%）;fundamentals 的 PE/PB 卻與 2026-07-30 逐字相同 ⇒ **quote 會動、fundamentals 不動**,引用時必須各自附時戳。

## 未消化 / 待補
- [ ] 排除比例 20% 與流動性代理的**門檻校準**仍未做:本頁只給方法（股價 P20 + 成交量代理）,未回測;需與 `skills/SK-37-liquidity-spread-screening.md` 的分位門檻一起定。
- [ ] 排除比例 20% 是論文預設,實務該看產業:(2026-08-23 TWSE 實測修正:電子股 <20 元僅 12.6%、金融股 >20 元 71.1%,原「電子 80% <20 / 金融 80% >20」不成立;電子股 87.4% ≥20 元)需分產業處理;atlas 端無產業×價格聯合篩選端點。

> **2026-09-27 batch#4 結案（移出本段）**:①「atlas 沒有流動性分位篩選」→ **已驗證的否定**（無分位端點）,替代法（client 端用 quote volume 自算）已落 `skills/SK-37-liquidity-spread-screening.md`,本頁複驗成交量確在 quote／technical;②「與 SK-20 差別」→ 兩頁軸不同（SK-20 要市值、SK-21 要股價）,同日實測顯示 SK-20 在 atlas **無市值資料**、SK-21 的股價軸可用 ⇒ 不重疊;SK-21 可實作、SK-20 不可。

- [ ] 「實盤流動性」需考量 bid-ask spread;**2026-09-27 精確化:atlas 無真實 spread,只有 OHLCV 代理 `SpreadEstimate`(`internal/marketdata/microstructure_provider.go`),該 provider 無 caller ⇒ 端點不可達(已驗證的否定,見 `skills/SK-37-liquidity-spread-screening.md`)**;需另尋外部 data source。
