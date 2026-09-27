---
title: "2026 AI 投資週期對位台股"
type: cycle-page
source: external-report-triangulation
ingested_at: 2026-08-04
last_updated: 2026-09-27
status: active
tier: T1
maturity: stable
confidence: high
atlas_go_relevance: high
mcp_tools_used: [macro_get_stress_index_current, narrative_get_chains, narrative_get_models, stock_get_quote, stock_get_fundamentals, template_detector_status]
verification: "T3-A248 快照(2026-08-04)：chains score 0.7343、ai_supercycle_model hit_rate 0.625／weight 0.1639、stress_index 4.22。**2026-09-27 L3 重跑**：stress_index **19.844**、chains **4 條**(AI_capex_surge 0.7695)、hit_rate **0.4111**／weight **0.03696**(已非最大)、templates **29 筆**、detector scan 2 筆(無編號);6 條缺口仍 2✅+1⚠️+3⛔,不假結案。見 §驗證方式。"
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-l3-backfill-b6）
l3_endpoints_probed:
  - "/api/narrative/stress-index/current → 200（19.844 / low） (2026-09-27T20:33:19+08:00)"
  - "/api/narrative/chains → 200（4 條,最高 0.7695） (2026-09-27T20:33:19+08:00)"
  - "/api/narrative/models → 200（AI weight 0.03696 已非最大） (2026-09-27T20:33:19+08:00)"
  - "/api/narrative/templates → 200（29 筆,無 template_number） (2026-09-27T20:33:19+08:00)"
  - "/api/detector/scan/status → 200（2 筆 theme 級） (2026-09-27T20:33:19+08:00)"
  - "/api/detector/registry/list → 200（29 themes） (2026-09-27T20:33:19+08:00)"
  - "/api/parameters → 200（cowos_utilization_threshold 78） (2026-09-27T20:34:20+08:00)"
sources:
  - UNCTAD WIR 2026 / Stanford HAI 2026 AI Index / HKS M-RCBG WP No.213 / HBS+HBP 2026 / atlas-notes 12-ext-research/2026-un-harvard-ai-investment/README.md
owner: kaecer
amendable_by: kaecer
cycle_label: 2026H2
decay_until: 2027Q1-WIR-revision
---

## 一句話定位

把 5 份 2026 權威機構的全球 AI 投資數字,**用 atlas trigger detectors + 3 narrative models + trigger templates 對位台股設備鏈**,讓週期性外部報告成為 `ai_supercycle_model`／`narrative_get_chains` 的 ground truth 校正點,而非歸檔的一次性事實層。

## 論文版概念（外部報告對位）

**4 條基線**:①半導體 greenfield CAGR **+54%/年** ②AI 投資 CAGR **+47%/年**(UNCTAD WIR 2026 ch.III)③2025 corporate AI 投資 **$581.7B**、private $344.7B(HAI ch.4)④TSMC 宣布 **$100B**(UNCTAD ch.I)。

**3 條結構性偏離**:⑤80% AI private 投資流向美國,但**半導體採購 70–90% 落台灣**(HKS §3.3)⑥「三限制」(能源/勞動/治理,HKS Singapore delay 4–6 年)缺雙向賽局 trigger ⑦**2027~2028 訂單跳升點**:宣布→下單 6~18 月、量產 +12~+24 月。

## atlas 對位

| atlas 既有機制 | 今日實測(2026-09-27) | 缺口 |
|----------|---------|----------|
| `AI_capex_surge` detector | registry 29 themes 之一;chains score **0.7695** | 缺「報告 cadence 重置」 |
| `ai_supercycle_model` | hit_rate **0.4111**／weight **0.03696**(replay 評估) | **已非最大權重**(hawkish_fed 0.04556) |
| atlas-wiki `templates/` #14/#15/#16 | 三檔實存;templates 端點回 **29 筆** | `template_number` 不在端點面 |
| `narrative.cowos_utilization_threshold` | **78**(heuristic,last_calibrated 2026-06-09);`engine.structural_trend` 版 75.05 | **EMIB/CoPoS 0 命中** |

**對位缺口**:缺 CoWoS/CoPoS trigger;設備股歸「其他電子」/「電機機械」無明確對應;圖卡訊號需自追蹤(未涵蓋 Layer 5)。

## 6 層因果鏈框架(圖層 T2 × 週期報告雙重驗證)

> **圖層 T2** = 2026-08 的 10 張半導體敘事新聞圖卡(顧奎國/溫建勛/阮惠慈),非學術/官方數據。**當 trigger 用,當 ground truth 須獨立驗證**。

| 層 | 對位 atlas | 圖層實例 |
|---|---|---|
| Layer 1 週期 | `ai_supercycle_model` | greenfield +54%/年 |
| Layer 2 時序 | `narrative_get_chains` | 宣布 → 下單 6~18 月 |
| Layer 3 技術 | **參數層有(CoWoS 使用率)、roadmap 層無** | CoWoS→EMIB→CoPoS |
| Layer 4 個股 | `stock_get_quote/chips` | 3131/6187/6640/6831 |
| Layer 5 漲停 | `narrative_get_chains` | +60~131% 回撤 |
| Layer 6 風險 | `risk_get_metrics` | Singapore 4–6 年 delay |

**4 條前提**:①T2 = 次級解盤 ②6 缺口逐個勾選才升 active ③圖卡 2026-08 收盤,**2027-02 框架本體需重寫** ④與 §atlas 對位 不重疊。

**6 條驗證缺口(2026-08-06 T3-A275.1)**:①設備月營收 REST ✅ ②2408 外資 chips ✅ +9183 ③TSMC AZ PDF ⛔ 撤 ④CoPoS 2028 ⛔ 撤 ⑤反彈型態 chains ✅ 4 chains(2026-09-27 複驗仍 4)⑥7/31 漲停 ⛔ 撤 ⇒ **2 ✅ + 1 ⚠️ + 3 ⛔(未變)**。

## 散戶解讀

1. **立刻可看**:`narrative_get_chains` 看 score 排名;前 3 條若全偏多 AI 供應鏈 = 偏多可不追,波動 > 30%/24h = 警戒(今日最高 0.7695)。
2. **月頻**:投信買超連 5 日 + 設備鏈月營收 YoY > 30%(家登 3680 last **542**)⇒ 結構性訂單 signal。
3. **季頻**:UNCTAD/HAI 4 月、BIS 6 月、IMF WEO 4/10 月 = 報告週期 anchor,下次驗收 2027 年 4 月。
4. **不可做**:用「CAPE 高檔」當「不看 AI 週期」的理由——前者是防禦層、後者是找信息差,兩層不互相取代。

## 驗證方式

**格式 ✅** / **對位 ATLAS_METHODOLOGY.md ✅**(七時期+三態+RiskLevel+七維+策略三分類) / **外部報告 cadence**:atlas 端**無** `external_report_calendar`(`git grep` 0 命中)⇒ 週期 anchor 只能 client 端維護。

### L3 端點實跑（2026-09-27,本 PR）

| 端點／命令 | http_code | 實測結果 | timestamp |
|---|---|---|---|
| `/api/narrative/stress-index/current` | 200 | `score`=**19.844**(2026-08-04 為 4.22)、`regime`=low、8 components | 2026-09-27T20:33:19+08:00 |
| `/api/narrative/chains` | 200 | **4** 條(2026-08-04 為 5):AI_capex_surge **0.7695**＞earnings_surprise 0.6＞inflation_spike 0.4276＞JPY_carry_unwind 0.4247 | 2026-09-27T20:33:19+08:00 |
| `/api/narrative/models` | 200 | `ai_supercycle_model` hit_rate **0.4111**／weight **0.03696**／sample 90;**最大權重 `hawkish_fed_model` 0.04556** | 2026-09-27T20:33:19+08:00 |
| `/api/narrative/templates` | 200 | **29** 筆,無 `template_number` 欄;「AI 資本支出激增」`historical_hit_rate`=**0.81**／`handwritten_prior` | 2026-09-27T20:33:19+08:00 |
| `/api/detector/registry/list`＋`scan/status` | 200／200 | registry **29 themes**(全 enabled,與 templates 1:1);scan status **2 筆**,theme 皆 `conflict_deescalation` | 2026-09-27T20:33:19+08:00 |
| `/api/parameters` | 200 | `narrative.cowos_utilization_threshold.value`=**78**(heuristic);`engine.structural_trend.…`=75.05 | 2026-09-27T20:34:20+08:00 |
| `/api/stock/quote` 2330/3680/3131/6187/6640/6831＋fundamentals 2330 | 全 200 | last=2475／**542**／2410／1195／1010／497.5;PE 30.19／PB 9.57 逐字未變 ⇒ 靜態快照 | 2026-09-27T20:33:19+08:00 |
| 源碼 grep `cowos\|emib\|copos`、`template_number` | — | CoWoS 在 config/參數/提示檔有(預設門檻 85);**EMIB/CoPoS 0 命中**;`template_number` 於 atlas-go 0 命中(僅 atlas-wiki 檔頭 2/22 檔有值) | 2026-09-27T20:36+08:00 |

**更正（2026-09-27）**

1. **快照全面位移**(時點 2026-09-27T20:33:19+08:00):stress_index 4.22 → **19.844**;chains 5 → **4**;AI_capex_surge 0.7343 → **0.7695**。
2. **「3 models 中 weight 最大」不成立**:AI weight **0.03696** < `hawkish_fed_model` **0.04556**;hit_rate 0.625 → **0.4111**。
3. **兩種 hit_rate 不可混用**:template 0.81=`handwritten_prior`(人工先驗)、model 0.4111=回放評估。
4. **「21 trigger templates」stale**:端點今日 **29 筆**(與 registry 1:1);atlas-wiki `templates/` 22 檔。
5. **Layer 3 只對一半**:CoWoS 參數層有(78),EMIB/CoPoS 路徑層 0 命中。
6. **2330 fundamentals 靜態**(PE/PB 逐字未變),3680 last 427 → **542**。

## 未消化 / 待補

- [ ] 建 `external_report_calendar`(2027Q1 WIR＋2027Q2 HAI)做年度稽核 cron(atlas 端 0 路由,需 client 端維護)
- [ ] HKS Carvalho §3.3 patient capital 模型 → 入 `atlas-notes/02-knowledge/`(資料卡,非 quota)
- [ ] 散戶解讀段原引之 CAPE 數值缺端點與 timestamp(鐵律五),已改定性;回填須附 snapshot + 時間
- [ ] 6 層因果鏈 6 條驗證缺口尚未全勾(2 ✅ + 1 ⚠️ + 3 ⛔)→ 未達升 active 條件(2026-09-27 複驗未變,**不假結案**)

> **2026-09-27 已解(移出本段)**:①`template_detector_status` 能否識別 #14/#15 → **不能**(scan status 是 theme 級歷史;`template_number` 在 atlas-go 0 命中)②第 16 模板已落 `templates/trigger-renewable-energy-divergence.md`,L3 實測**未觸發**(gap_rev +41.86pp 成立、gap_rs +3.27pp 不成立)。

## 反向鏈接

- `_consult-index.md` §Q1 T3-A248 / `12-ext-research/2026-un-harvard-ai-investment/README.md` / `docs/ATLAS_METHODOLOGY.md` v1.1 §一 §二
- 圖層 T2 來源:telegram session `20260711_190603_a8ec0010` msg 15622 + T3-A275 實查(2026-08-05)
- **真實股號**(fact_d72e14ee):3131 / 6187 / 6640 / 6831
