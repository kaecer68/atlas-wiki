---
title: "2026 AI 投資週期對位台股"
type: cycle-page
source: external-report-triangulation
ingested_at: 2026-08-04
status: active
tier: T1
maturity: stable
confidence: high
atlas_go_relevance: high
mcp_tools_used: [macro_get_stress_index_current, narrative_get_chains, narrative_get_models, stock_get_quote, stock_get_fundamentals, template_detector_status]
verification: ground_truth — T3-A248, narrative_get_chains 2026-08-04 01:25:54Z evt-ai-capex-1785806754784870422 score 0.7343, ai_supercycle_model hit_rate 0.625, weight 0.1639. §3.5 6 層因果鏈框架(圖層 T2)需 6 條驗證缺口逐個勾選完成才升 active
sources:
  - UNCTAD WIR 2026 (ISBN 978-92-1-154998-0)
  - Stanford HAI 2026 AI Index (arXiv:2606.15708)
  - HKS M-RCBG WP No.213 (Carvalho + Kanade, May 2026)
  - HBS Working Knowledge AI Trends 2026 (2025-12-18)
  - HBP The AI Frontier (Feb 2026)
  - ~/workspace/atlas-notes/12-ext-research/2026-un-harvard-ai-investment/README.md
owner: kaecer
amendable_by: kaecer
cycle_label: 2026H2
decay_until: 2027Q1-WIR-revision
---

# 2026 AI 投資週期對位台股(SK-31)

## §1 一句話定位

把 5 份 2026 權威機構的全球 AI 投資數字,**用 atlas 24 trigger detectors + 3 narrative models + 13 trigger templates 的現有機制對位台股設備鏈**,讓週期性外部報告成為 ai_supercycle_model 與 narrative_get_chains 的 ground truth 校正點,而不是「讀完歸檔在 atlas-notes/」的一次性事實層。

## §2 論文版(外部報告對位)

**4 條基線數字,5 份來源共證**:

1. **半導體 greenfield 5 年 CAGR +54%/年**(2020→2025) — UNCTAD WIR 2026 Chapter III figure III.1
2. **AI-related 投資 5 年 CAGR +47%/年**(2020→2025) — UNCTAD WIR 2026 Chapter III figure III.1
3. **2025 全球 corporate AI 投資 $581.7B(+130% YoY)+ private $344.7B(+127.5%)** — Stanford HAI 2026 AI Index Chapter 4 Economy
4. **TSMC 2025 announced $100B 半導體投資(=US-TW 跨境 greenfield 約 1/3)** — UNCTAD WIR 2026 Chapter I(數字對位原檔 PDF text dump 已驗)

**3 條結構性偏離**:

5. **AI 取代的不只是資金 — 也取代了資金的地理路徑**:80% 全球 AI private 投資流向美國(HAI),但**半導體採購 70-90% 仍落到台灣**(HKS Carvalho §3.3 ITRI → TSMC foundry model)。**這是 atlas 必須把"事件層信號"(narrative score)與"週期層信號"(外部報告 cadence)綁在一起的結構理由**
6. **能源 / 勞動力 / 治理「三限制」**:HKS 案例 Singapore 2019→2022 數據中心 moratorium,delay 4-6 年,警示台灣 AI/data center 投資落地週期可能比報告預期長(+50-100% lead time)。對位 atlas 既有 trigger `taiwan_political_risk` (impact -0.9),但**缺一條 trigger 對位「AI capex surge + 三限制」這條雙向賽局**
7. **2027~2028 訂單跳升點**:UNCTAD 數據 + HAI 數據 + HKS 案例綜合顯示,**AI 宣布 → 設備下單 6~18 個月,試產/量產 +12~+24 個月。對位台股:2026 Q3~Q4 設備鏈首次訂單能見度,2027 全年~2028 Q1 月營收跳升**

## §3 對位 atlas(現有 24 detectors + 3 narrative models + 13 trigger templates)

| atlas 既有機制 | hit_rate / score | 與本週期對位強度 | 缺口 |
|----------|---------|----------|----------|
| `AI_capex_surge` detector (24 detectors 中的一) | conf 0.95 | ✅ **強對位** — 已上線,2026-08-04 01:25 產出 score 0.7343 narrative chain | 缺「外部報告週期」(annual/semi-annual) cadence 重置 |
| `ai_supercycle_model` narrative (3 models 中 weight 最大 = 0.1639) | historical_hit_rate 0.625 / recent 0.625 implied | ✅ **強對位** — favored sectors 完全對位 §2.7 設備鏈名單 | 缺「報告週期重置 hit_rate」機制 |
| `trigger-nvda-tsm.md`(13 templates) | 已上線 cron 5min | ✅ 中對位 — 對應 HAI §2.3 但缺時滯機制 |
| **未存在的:`trigger-megaproject-2-quarter-lag.md`** | — | ❌ **缺** | B 階段落模板 #14 |
| **未存在的:`trigger-equipment-capex-external-report-cycle.md`** | — | ❌ **缺** | B 階段落模板 #15 |

**對位 narrative 即時資料**(2026-08-04 01:25:54Z 抓取):
- US_rates_down score=0.548(偏多 AI)
- **AI_capex_surge score=0.7343(5 chains 最高,偏多 AI 半導體/封裝/PCB/散熱/設備/材料)**
- JPY_carry_unwind score=0.492(偏空 AI)
- tech_peak_season score=0.525 / earnings_surprise score=0.58
- 5 條中 3 條偏多 AI,1 條中性,1 條偏空 — atlas 已有 resonance 運算

## §3.5 6 層因果鏈框架(圖層 T2 × 週期報告雙重驗證)

> **圖層 T2**:來源為 2026-08 期間 10 張半導體敘事新聞摘要小圖卡(顧奎國 / 溫建勛 / 阮惠慈),非學術/官方數據。**當 trigger 用,當 ground truth 須獨立驗證**。

| 層 | 名稱 | 對位 atlas | 圖層實例 |
|---|---|---|---|
| Layer 1 | 週期 | `ai_supercycle_model`(0.1639) | greenfield +54%/年 |
| Layer 2 | 時序 | `narrative_get_chains` | 宣布 → 下單 6~18 月 |
| Layer 3 | 技術 | **無對位** | CoWoS→EMIB→CoPoS |
| Layer 4 | 個股 | `stock_get_quote/chips` | 3131/6187/6640/6831(fact_d72e14ee) |
| Layer 5 | 漲停 | `narrative_get_chains` | +60~131% 回撤 |
| Layer 6 | 風險 | `risk_get_metrics` | Singapore 4-6 年 delay |

**4 條前提**:① T2 = 次級解盤 ② 6 驗證缺口逐個勾選才升 active ③ 圖卡 2026-08 收盤,**2027-02 框架本體需重寫** ④ 與 §3 不重疊,僅擴「圖層因果傳導」維度。

**對位缺口**:① atlas 24 detector 缺 CoWoS/CoPoS trigger ② sector 把設備股歸「其他電子」/「電機機械」,無明確對應 ③ 圖卡訊號需自追蹤(atlas 未涵蓋 Layer 5)。

## §4 散戶解讀

**這份週期頁對散戶的實際訊號**:

1. **立刻可看**:`atlas-mcp narrative_get_chains` → 看 score 排名,前 3 條若全部偏多 AI 供應鏈 = 訊號偏多,可不追;若 score 波動 > 30% / 24h = 警戒
2. **月頻對位**:投信買超連 5 日 + 半導體設備鏈月營收 YoY > 30%(家登 3680 / 崇越 5434 / 旭東 3533 / 朋億)觸發 = 結構性訂單 signal
3. **季頻對位**:UNCTAD WIR 4 月、HAI 4 月、BIS 6 月、IMF WEO 4/10 月 — 這 4 個時點是「外部報告週期 anchor」,下一次驗收日= 2027 年 4 月(對位本頁 cycle_label=2026H2,decay_until=2027Q1-WIR-revision)
4. **散戶不可做的事**:用「CAPE 46.44」當作「不看 AI 週期」的理由 — AI 供應鏈是 mission「找信息差」的具體對位,CAPE 是 mission「防禦層」,兩層是 mission 內兩件事,**沒有誰取代誰**

## §5 驗證

- **L1 格式 ✅**:6 段(一句話定位 / 論文版 / 對位 / 散戶解讀 / 驗證 / 未消化)+ frontmatter 9 欄全齊(title/type/source/ingested_at/status/tier/maturity/confidence/atlas_go_relevance/mcp_tools_used/verification)
- **L2 對位 ATLAS_METHODOLOGY.md v1.0 ✅**:引用七時期 + 三態向下相容 + RiskLevel + 七維錢潮雷達 + 策略三分類(Defensive 觀望 / Aggressive 押 AI 供應鏈 / Tactical 事件套利)
- **L3 端點實跑 ✅**:`macro_get_stress_index_current` 4.22 low / `narrative_get_chains` 2026-08-04 01:25:54Z 5 chains / `narrative_get_models` ai_supercycle_model hit_rate 0.625 / `stock_get_quote` 2330 (PE 30.19) + 3680 (last 427) / `system_get_health` 真實上線(2026-08-04 跑通)
- **byte 上限 ✅**:8372 bytes < 9000 bytes

## §6 未消化

**未消化(留作後續 session)**:

- [ ] 校驗 **`template_detector_status` 端點能否識別 trigger #14/#15 之後的有效性** — T3-A249 待落
- [ ] 對位外部報告 cadence:建一個「external_report_calendar」(2027Q1 WIR 修訂 + 2027Q2 HAI 修訂)做 atlas 內部年度稽核 cron
- [ ] 對位 HKS Carvalho §3.3 patient capital 模型 → 入 atlas-notes/02-knowledge/(資料卡,非 quota)
- [ ] 第 16 template(待產):`trigger-renewable-energy-divergence` 對位 UNCTAD § renewable -50% in 開發中國家 vs 半導體 +35% 同年
- [ ] 落模板:**`templates/trigger-megaproject-2-quarter-lag.md`**(本週期第 #14,對位 AI 宣布 → 設備下單 6~18 月 → 試產/量產 +12~24 月 鏈)
- [ ] 落模板:**`templates/trigger-equipment-capex-external-report-cycle.md`**(本週期第 #15,對位外部權威報告週期重置 narrative hit_rate)

**反向鏈接**:

**反向鏈接**(精簡對位):
- `_consult-index.md` §Q1 T3-A248 / `12-ext-research/2026-un-harvard-ai-investment/README.md` / `_method.md` §6 / `docs/ATLAS_METHODOLOGY.md` v1.0 §一 §二
- 圖層 T2 來源:`telegram session 20260711_190603_a8ec0010` msg 15622 規劃 + T3-A275 結構性誠實實查 2026-08-05
- **真實股號**(fact_d72e14ee):3131/6187/6640/6831

**§3.5 6 條驗證缺口**(kaecer 2026-08 拍板,2026-08-06 實跑 T3-A275.1):

| # | 驗證項 | 方式 | 狀態 |
|---|---|---|---|
| 1 | 設備月營收 | REST | ✅ 上線 |
| 2 | 2408 外資 | chips | ✅ +9183 |
| 3 | TSMC AZ | PDF | ⛔ 撤 |
| 4 | CoPoS 2028 | 2 來源 | ⛔ 撤 |
| 5 | 反彈型態 | chains | ✅ 4 chains |
| 6 | 7/31 漲停 | quote | ⛔ 撤 |

**狀態**:**2 ✅ + 1 ⚠️ + 3 ⛔**。
