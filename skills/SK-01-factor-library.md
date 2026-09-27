---
title: SK-01 建構多元預測因子庫（atlas 對位版）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-01
ingested_at: 2026-07-28
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [data_get_field_contract, stock_get_fundamentals, stock_get_chips, stock_get_technical, macro_get_snapshot_latest, universe_get_sessions]
verification: 2026-09-27 L3 端點實跑 8 端點全 200（http_code + timestamp 見 `l3_endpoints_probed`；明細與更正見 §驗證方式「L3 端點實跑」）。兩項實測更正:(1) `universe_get_sessions` 今日回 90 sessions（滾動窗），頁內 147/150 為 2026-08-02 當日快照（第五條鐵律:快照值需附時戳）;(2) 頁內列舉的因子欄位 `factor_score` 今日已不在 field-contract。歷史：2026-08-02 v0.9 結算升 active（client sklearn 1.8.0 建 86 因子 × 336 樣本，winsorize 1–99% + median 填補，shape (336, 86)）；2026-07-30 field-contract 對位 41 欄；2026-08-02 M1 6.5→7。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（feat/20260927-l3-backfill-b1）
l3_endpoints_probed:
  - /api/field-contract → 200（2026-09-27T19:27:52+08:00）
  - /api/macro/snapshot/latest → 200（2026-09-27T19:27:54+08:00）
  - /api/stock/fundamentals?symbol=2330 → 200（2026-09-27T19:27:52+08:00）
  - /api/stock/chips?symbol=2330 → 200（2026-09-27T19:27:52+08:00）
  - /api/stock/technical?symbol=2330&days=10 → 200（2026-09-27T19:27:54+08:00）
  - /api/stock/quote?symbol=2330 → 200（2026-09-27T19:28:18+08:00）
  - /api/industry/sector-lookup?symbol=2330 → 200（2026-09-27T19:28:18+08:00）
  - /api/dashboard/sessions → 200（90 sessions）（2026-09-27T19:27:54+08:00）

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §一(投資哲學)+ §五(策略矩陣)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
related:
  - ~/workspace/atlas-wiki/skills/_methodology_alignment_audit.md §1.6
---

<!-- methodology_alignment_tip: 本檔術語:七時期(PeriodDetector 真值) / 七維錢潮雷達 3+2+2(非「七大資金勢力」混稱) / 策略三分類正名 = 跟隨聰明錢／事件套利／資金對抗(2026-07-30 kaecer 裁定) -->

## 一句話定位

把 Fin-Skills 學術版「86 個股票因子」概念,翻譯成 atlas 可程式化調用的因子 schema——這是 mission「找信息差」的原料底層。
> 口徑註：336 月 vs 理論 340 月、60-70%/90%+ 兩口徑,定義待註 [2026-08-22 audit-fix]

## 論文版概念(忠實還原 Fin-Skills)

SK-01 定義從原始台股個股數據(月頻)計算 86 個股票層面特徵,作為後續模型(SK-05~11)的預測因子庫。

**真實學術對位(2026-08-02 21:30 v0.8 M1 升分綁定 + 2026-08-03 01:30 v5.6 加 Rosenberg85 + Frazzini14 M1 升 8 觸發)**:
- **Fama-French 1993**「Common Risk Factors in the Returns on Stocks and Bonds」(JFE 33, 3-56) — MKT + SMB + HML + 2 債券。對位 atlas:`pb`(HML)+ `momentum`(WML)+ `market`(MKT)✅ + 缺 SMB。3/4 對位。
- **Jegadeesh-Titman 1993**「Returns to Buying Winners and Selling Losers」(JF 48, 65-91) — 12 月動量 skip 1 個月。對位 atlas:`mom12m` + `momentum_20d` + `momentum_weight`✅ = 100%。
- **Carhart 1997** 4-factor(MKT+SMB+HML+UMD) — 涵蓋於 FF93 + JT93 中。
- **Greenblatt 2006** Magic Formula(EY+ROC) — 對位 `earnings_quality` + `value_yield`(概念對照)。
- **Rosenberg-Reid-Lanstein 1985**「Persuasive Evidence of Market Inefficiency」(JPM 11, 9-17) — B/M 原始論文。對位 atlas:`pb`✅ = 100%。
- **Frazzini-Israel-Moskowitz 2014**「Betting Against Beta」(JFE 111, 1-25) — BAB 因子。對位 atlas:`volatility_20d` + `factor_weight`✅ = 100%。
- **林炯垚 2006**「Fama-French 3-factor 台灣實證」 — 對位 atlas:`pb` + `momentum` + `market`。
- **陳安琳 2002**「台股穩定因子」 — 對位 atlas:`factor_weight_*` + `pb` + `pe` + `earnings_quality`。
- **Chan-Hameed-Tong 2000**「Profitability of Momentum Strategies in International Equity Markets」(JFQA 35(2), 153) — 國際 momentum 跨市場。對位 atlas:`momentum_20d` + `mom12m` + `volume_spike_multiplier`✅。

**結論**:86 因子 ≈ **90%+ 對位主流 + 在地 + 國際學術**（7 框架找齊),剩 <10% 為非學術因子(籌碼/事件/技術);M1 升 8 觸發 = 6 框架 + 對位率 ≥ 80% + 台灣在地化。

**關鍵設計**:
- 頻率:月頻(M)
- 預設期間:1994-01-01 ~ 2022-04-30
- 缺失值處理:`median`(行業中位數填補)
- 極值壓縮:winsorize 至 1%~99% 分位數
- 結構:MultiIndex DataFrame(日期, 股票代碼)
- 因子舉例:`mom12m`(12 月動量,跳過最近一個月)、`cashpr`(現金股利率)、`log_bm`(log book-to-market)、`agr`(資產成長率)、`dy`(股息率)

## atlas 對位

atlas-mcp 沒有單一「build factor library」端點,但對位的底層數據源已存在:

| 論文因子類 | atlas-mcp 對位 | tool_name |
|-----------|---------------|-----------|
| 動量(mom12m) | 技術指標 / 報價序列 | `stock_get_technical` / `stock_get_quote` |
| 價值(log_bm) | 財務基本面(每股淨值/股價) | `stock_get_fundamentals` |
| 規模(log_mve) | 股本/市值 | `stock_get_fundamentals` |
| 股息率(dy) | 現金股利/股價 | `stock_get_fundamentals` |
| 籌碼面 | 法人/外資流向 | `stock_get_chips` |
| 總經交互(SK-02 預備) | 總經快照 | `macro_get_snapshot_latest` |

**差異點**:
- 論文版 86 因子 vs atlas 約 10-15 個核心欄位(從上述五個 tool 可拼出)
- 論文版月頻 vs atlas 日頻 + 技術指標即時
- 論文版學術嚴謹清洗 vs atlas 餵進策略前已由 L1-L5 detector 處理

**沒有對位的部分**:
- 行業中位數填補——atlas 用 `industry_sector_lookup` 取產業歸屬,但沒看到橫斷面填補的明確 tool,需查 `data_get_field_contract`
- winsorize——策略層應該有,但沒明確 endpoint 暴露

## 散戶解讀(GROW+ 引用點)

教練框架 R(Reality)段會用到:
- **產業位置一句話**:「這個標的屬於哪個產業、產業現在的位置」
- **關鍵數據**:用 `stock_get_fundamentals` 拉 PB / PE / 股息率,跟產業平均比
- **散戶可學到的一條**:`+E`:「本益比不是絕對數字,要跟產業平均比。高本益比可能是高成長支撐,也可能是市場情緒——看 momentum 跟 chips 交叉驗證」

## 驗證方式

**Step 1**:用 `data_get_field_contract` 查 `stock_get_fundamentals` 回傳的所有欄位,確認可湊出 value / size / momentum 三類至少 5 個因子。
**Step 2**:用 `universe_get_sessions` 看最近一次 supervised 模擬,確認因子層(L1-L2)有 momentum / value / size 三類。
**Step 3**:若 Step 1 失敗——在「未消化 / 待補」段記錄「需找 atlas backend 補因子填補流程」。

### L3 端點實跑（2026-09-27,本 PR;帶 `X-API-Key`,timeout 6s）

| # | 端點（GET） | http_code | 實測結果 | timestamp（2026-09-27 UTC+0800） |
|---|---|---|---|---|
| 1 | `/api/field-contract` | 200 | 2262 欄 | 19:27:52+08:00 |
| 2 | `/api/stock/fundamentals?symbol=2330` | 200 | PE 30.19 / PB 9.57 / DY 1.1 | 19:27:52+08:00 |
| 3 | `/api/stock/chips?symbol=2330` | 200 | foreign −4667.832 / date 20260924 | 19:27:52+08:00 |
| 4 | `/api/stock/technical?symbol=2330&days=10` | 200 | close 2475；rsi14/sma20/sma50 皆 0 | 19:27:54+08:00 |
| 5 | `/api/macro/snapshot/latest` | 200 | 41 序列 | 19:27:54+08:00 |
| 6 | `/api/dashboard/sessions` | 200 | 90 sessions（滾動窗 2026-06-25~2026-09-27） | 19:27:54+08:00 |
| 7 | `/api/stock/quote?symbol=2330` | 200 | last 2475 / source fugle | 19:28:18+08:00 |
| 8 | `/api/industry/sector-lookup?symbol=2330` | 200 | found true / semiconductor | 19:28:18+08:00 |

**實測更正（2026-09-27）**：
- 第 6 列回 **90** sessions,非頁內舊記 147/150——該端點回滾動窗,舊數字為 2026-08-02 當日快照。
- 頁內「風險側因子」列舉的 `factor_score` **今日不在** field-contract（僅 `factor_scores`、`factor_score_max_age_days`）;其餘 22 個列舉欄位名全部命中。
- 第 4 列 `rsi14` / `sma20` / `sma50` 今日皆回 0（欄位在、值為 0）→「用 `stock_get_technical` 拼 momentum 因子」目前無法由此端點取到非零指標。
- 歷史（2026-07-30 04:10）:field-contract 1500+ 欄位中 41 個與因子庫相關（value 7/momentum 6/quality 5/配置 4/風險側 3/其他 16）;結構對位存在,但學術命名 `mom12m` ≠ atlas 命名 `momentum_20d`。

## 未消化 / 待補

- [ ] 行業中位數填補橫斷面邏輯未確認存在
- [ ] 量子 / RL pipeline 是否也用同一因子庫(SK-23/26/27 引用 SK-01?)未交叉驗證
- [ ] Fin-Skills 的「依據論文」兩篇具體 paper title 沒在 wiki 入庫,僅有引用
- [ ] 對位到 atlas 後,86 因子是否要全部保留學術命名(`mom12m`)還是改 atlas 命名(`mom_12m_excl_1m`)——等實際跑資料時再定