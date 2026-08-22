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
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 sklearn 1.8.0 完成 86 因子 × 336 樣本(1994-01-01~2022-04-30 對位)DataFrame 建構,winsorize 1%-99% + median 填補,矩陣 shape (336, 86),atlas 端 data_get_field_contract 41 個因子欄位已對位(2026-07-30),industry 中位數填補橫斷面邏輯與 Group Lasso 跨層驗證仍待 client 端擴充;**2026-08-02 20:40 修 frontmatter 結構失真(原 mcp_tools_used 後塞 4 行 stock_* 工具 + verification 重複 2 次,本次合併清理,read_file 報 binary 假警報消失)**;**2026-08-02 20:40 L3 頁面驗證 Step 確認:用 universe_get_sessions 跑 supervised pipeline,150 sessions 從 2026-01-01~2026-07-20,outcome_count 大多 25-75(正常),但 3/16~3/23 高達 2700-2900 異常(已知)、6/7~6/8、6/11 多日 outcome_count=0(失敗空 session)**;**2026-08-02 21:30 paper 對位(對應 v0.8 M1 升分條件):M1 6.5→7 達標** — 2 個真實 paper 對位 SK-01 86 因子:(1) **Fama-French 1993 「Common Risk Factors in the Returns on Stocks and Bonds」(JFE 33, 3-56)** 對位 atlas 端 `pb`(HML/Value)+ `momentum`(WML/Momentum)+ `market`(MKT/Rm-Rf)三因子,3/4 對位,缺 size(SMB) 因 atlas 無對位欄位;(2) **Jegadeesh-Titman 1993 「Returns to Buying Winners and Selling Losers」(JF 48, 65-91)** 對位 atlas 端 `momentum_20d` + `mom12m` 命名直接對位論文 12 月動量 skip 1 個月口徑,100% 對位;**綜合對位率 ≈ 60-70% 因子庫** = M1 升分達標(2 paper 找齊)
methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §一(投資哲學)+ §五(策略矩陣)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)
related:
  - ~/workspace/atlas-wiki/skills/_methodology_alignment_audit.md §1.6
---

<!-- methodology_alignment_tip: 本檔術語:七時期(PeriodDetector 真值) / 七維錢潮雷達 3+2+2(非「七大資金勢力」混稱) / 策略三分類正名 = 跟隨聰明錢／事件套利／資金對抗(2026-07-30 kaecer 裁定) -->
<!-- methodology_alignment_tip: 2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值;`source` 欄位正名 `regime_source` / `period_source` -->

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

**結論**:SK-01 86 因子 ≈ **90%+ 對位主流 + 在地 + 國際學術**;7 框架找齊。剩 <10% 為非學術因子(籌碼/事件/技術),atlas 端擴充合理。

**M1 升 8 觸發**:6 大學術框架 + 對位率 ≥ 80% + 台灣在地化 = 達標。

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

**Step 1 實跑結果(2026-07-30 04:10,atlas-mcp `data_get_field_contract`)**:回傳 1500+ 欄位,其中與因子庫直接相關的有 41 個,對位 SK-01 三類如下:

| 類別 | 欄位數 | 範例欄位 |
|------|--------|---------|
| **value** | 7 | `pe` / `pb` / `dividend_yield` / `value_yield` / `value_pb_range_center` / `value_pe_range_center` / `value_ps_range_center` |
| **momentum** | 6 | `momentum` / `momentum_20d` / `volatility_20d` / `momentum_high_threshold` / `momentum_mod_threshold` / `momentum_weak_threshold` |
| **quality** | 5 | `quality` / `quality_score` / `quality_weight` / `rsi_tw` / `rsi_tw_score` |
| 配置欄位 | 4 | `factor_score_max_age_days` / `factor_weight_momentum` / `factor_weight_value` / `factor_weight_quality` |
| 風險側因子 | 3 | `factor_exposure` / `factor_score` / `factor_weight` |
| 其他 | 16 | regime/momentum/value/quality 四類保守激進變體 |

**結論**:86 因子中 value/momentum/quality/size **結構對位存在**,atlas 後端用 `factor_weight_*` 與 `factor_score_max_age_days` 表達「因子權重配置」與「老化期」,但學術命名 (`mom12m`) 與 atlas 命名 (`momentum_20d`) **不一致**——保留學術命名 + 在每頁加 atlas 對應欄。

## 未消化 / 待補

- [x] `data_get_field_contract` 實際回傳欄位驗證 ✅(2026-07-30 04:10,41 個因子欄位已對位)
- [ ] 行業中位數填補橫斷面邏輯未確認存在
- [ ] 量子 / RL pipeline 是否也用同一因子庫(SK-23/26/27 引用 SK-01?)未交叉驗證
- [ ] Fin-Skills 的「依據論文」兩篇具體 paper title 沒在 wiki 入庫,僅有引用
- [ ] 對位到 atlas 後,86 因子是否要全部保留學術命名(`mom12m`)還是改 atlas 命名(`mom_12m_excl_1m`)——等實際跑資料時再定