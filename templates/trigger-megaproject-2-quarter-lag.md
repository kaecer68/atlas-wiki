# atlas-mcp Trigger Template #14 — trigger-megaproject-2-quarter-lag

**對位**:B 階段 kaecer 拍板「+ 第 14 template」+ T3-A248 v6.46 governance
**對位文獻**:UNCTAD WIR 2026 figure III.1 + Stanford HAI 2026 Chapter 4 + HKS M-RCBG WP No.213 (2026/05)
**對位 ATLAS_METHODOLOGY.md** v1.0 §二 因果傳導鏈 第 1 層(美股科技估值)→ 第 2 層(台灣出口與半導體景氣)
**對位 narrative**:`ai_supercycle_model`(hit_rate 0.625 / weight 0.1639 / 3 models 中最大)
**立此日期**:2026-08-04
**立此原因**:kaecer 2026-08-04 B+C 拍板,SK-31 落 SK-31,本模板為該週期對位的「訂單時序」執行端

---

## §1 觸發條件(對位「AI 宣布 → 設備下單 6~18 月,設備交貨 → 試產/量產 +12~24 月」鏈)

**Compare: gt** — 顯式聲明(對位 kaecer 7/30 結構性誠實 3 條規則 C)

| 期間 | 條件 | 端點 | 觸發層 |
|------|------|------|--------|
| **T-30 ~ T+30 天(單月)** | `stock_get_quote` 2330 月營收 YoY > +5% | `/api/stock/fundamentals?symbol=2330` 或回算自 quote | **單月 layer** |
| **T-90 ~ T+90 天(季度)** | 設備鏈(月營收)連 3 月 YoY > +30% | `/api/stock/fundamentals?symbol={3680|3533|5434}` | **季度 layer** |
| **T-180 ~ T+180 天(半年)** | 投信買超連 5 日 > +20 億 | `/api/stock/chips` 或 `capital_flow_summary` | **半年 layer** |

## §2 為什麼是 6-18 月 + 12-24 月的 lag

UNCTAD WIR 2026 figure III.1 顯示半導體 greenfield 5 年 CAGR +54%(2020→2025)。綜合:
- HKS Carvalho §3.3 「TSMC foundry model + ITRI patient capital」「AZ 一廠到量產 lead time 4-6 年」
- HAI 2026 §2.3 「TSMC 2025 announced $100B」(佔 US-TW 跨境 greenfield 約 1/3)
- 對位台股:**2026 Q3 ~ Q4 起,設備鏈(家登/崇越/旭東)首次可見訂單能見度;2027 全年 ~ 2028 Q1 月營收跳升**

**半年層的設計**:觸發 hit 後,對位「設備下單後 6 個月開始交貨」這個產業常識,**半年後再對位 monthly + quarterly 條件交叉驗證**,符合 trigger-monitor v6.22 的「1 小時去重」與「5 分鐘併發」規範。

## §3 觸發後執行(對位 SK-31 §4 散戶解讀)

1. **Telegram 通知 kaecer**(對位 SOUL §4.1 三方管理 + 觸發監控 v6.22)
2. **同步讀取 `narrative_get_chains` AI_capex_surge 即時 score**:
   - 若 score > 0.7 + 本 trigger = **雙因素共振** = 高信心訊號
   - 若 score < 0.4 + 本 trigger = **事件層與週期層分歧** = 警示(對位結構性誠實「不編造觸發」)
3. **寫入 `~/workspace/atlas-notes/04-daily/2026-08-XX-weekly-log.md`** 當週日誌(對位 `_method.md` §「重啟後 30 秒回神」)
4. **落 `_consult-index.md` §6 第 N 筆對話紀錄** — 觸發成功 + 結構性誠實標

## §4 結構性誠實護欄(kaecer 7/30 拍板三條規則 A/B/C + T3-A14 v8 + v6.22)

- **A**:單日可觸發(用 quote 計算,非 range query)
- **B**:觸發失敗 = 不觸發,**禁止編造**(對位 T3-A14 v8「結構性誠實三十七次」)
- **C**:`compare: gt` 顯式聲明(對位 trigger-monitor v6.22 fix)
- **額外護欄**:
  - **1 小時去重**:同一 trigger 不重複通知
  - **5 分鐘併發**:多 trigger 合併 1 條摘要
  - **失敗率 > 50%** → atlas 端故障通知(對位 v6.22)
  - **trigger ≥ 2 個獨立 atlas-mcp 端點 = 雙因素驗證**(本模板用 chips + chips,原則上不算雙因素,需下一版拉 `narrative_get_chains` 補強)

## §5 atlas-mcp-trigger-monitor.py 修改(給開發 / atlas agent)

### A. line 30-144 TEMPLATES 加 1 條

```python
"megaproject-2-quarter-lag": {
    "name": "Megaproject 半年報週期 + 設備鏈 lag 觸發",
    "file": "trigger-megaproject-2-quarter-lag.md",
    "condition": "設備鏈(3680/3533/5434)月營收連 3 月 YoY > +30% + 投信買超連 5 日 > +20 億",
    "http_path": "/api/stock/fundamentals",
    "field": "monthly_revenue_yoy_pct",
    "metric": "value",
    "threshold": 30.0,
    "compare": "gt",
    "extra_check": None,
    "is_custom_calc": False,  # 設備鏈月營收是 fundamental 直接暴露欄位
},
```

### B. Run 流程

- 預設 5 分鐘 cron(對位 `cron 9a9aa3` 既有規範)
- 觸發失敗 fallback:延後 1 個 cycle,不發假通知

### C. 測試 checklist

- [ ] 本地手動:`curl "http://127.0.0.1:18080/api/stock/fundamentals?symbol=3680"` 確認 200 + `monthly_revenue_yoy_pct` 欄位存在
- [ ] 加模板後跑:`python3 atlas-mcp-trigger-monitor.py` 確認 14 模板全綠
- [ ] 結構性誠實測試:手動 mock 月營收 YoY +35% → 觸發 → 對位 narrative score < 0.4 → 標「事件層與週期層分歧」
- [ ] **禁用場景**:模擬連 3 月 YoY < +30% → 不能觸發,**不要改邏輯繞過**

### D. 上線 + 治理留痕

- 不需動 atlas backend(只改 atlas-wiki/_scripts/template-impl)
- kaecer 拍板啟用後 → 落 `_consult-index.md` §6.4 對位表(從 13 模板升 14 模板)
- T3-A249 governance evidence 寫明 14 模板真實觸發 + 命中紀錄

## §6 與 SK-31 對位(對位表)

| SK-31 § | 本模板 § | 連接 |
|---------|---------|------|
| §1 一句話定位 | §3 觸發後執行 | 「週期性外部報告成為 atlas ground truth 校正點」的執行端 |
| §2 論文版第 7 點 | §2 為什麼是 lag | 「2026 Q3~Q4 設備鏈首次訂單 → 2027~2028 月營收跳升」的鏈 |
| §3 對位 atlas | §1 觸發條件 | hit_rate 0.625 / weight 0.1639 narrative model 校對 |
| §4 散戶解讀 | §3 觸發後執行 | 給散戶的可操作訊號 |
| §5 驗證 | §5 atlas-mcp-trigger-monitor.py 修改 | 驗證機制 |

## §7 對位 SKILL 與憲章

| 對位項 | 內容 |
|--------|------|
| ATLAS_METHODOLOGY 7 層因果鏈 | Layer 1(美股科技估值:NVDA capex)→ Layer 2(台灣出口:設備鏈月營收)→ Layer 3(半導體 leader) 三層正交對位 |
| Q1 個股 + Q3 產業 | Q3 產業輪動為主(半導體設備鏈是產業層) |
| 策略 archetype 對位 | **跟隨聰明錢**(押 AI 供應鏈的聰明錢流入);E5a 策略類別 = Aggressive。archetype 三分類正本 = 跟隨聰明錢／事件套利／資金對抗(AGENTS.md §12)[2026-08-22 audit-fix] |
| 七時期 | 黑天鵝時期(`black_swan`)+ 黑天鵝 + 7 時期對位 → trigger 不主動推(保守者存活原則) |
| 三態向下相容 | RISK_ON 時期 trigger 信號加強,RISK_OFF 減弱,NEUTRAL 中性 |
| 散戶語言 | 「設備鏈月營收連 3 月 YoY > 30% = 半導體接單已啟動」 |
| 結構性誠實 | 觸發失敗時標明,不用 fallback 假資料 |

## §8 為什麼這模板值得加(對位散戶價值 + 對位「精準預測」)

- **現有 13 模板**沒有一條對位「設備鏈 lag 6 個月至 2 年的鏈」 — 全是 5 分鐘或單日可觸發的即時訊號,無週期性 lead time
- **kaecer 2026-08-04 講的「精準預測的 atlas 才是有用」**:本模板對位半年/季度/月 三層 lead time,**讓 atlas 不只看當下股價,而是看 6-18 月後的設備接單結構性訊號**
- **2027 年 4 月驗收日**(對位 SK-31 §4 第 3 點 + cycle_label=2026H2 + decay_until=2027Q1-WIR-revision):UNCTAD 2027 WIR + HAI 2027 AI Index 4 月同步 release,**屆時本模板是否真實觸發 + 觸發後 hit_rate 變化將是「精準預測」這條標準的 ground truth 量化指標**

## §9 不該做的事

- ❌ 不要把 lag 改成日頻(週期性是核心,降頻就失去意義)
- ❌ 不要把 `monthly_revenue_yoy_pct` 改成日頻 quote(last → short-term noise 淹沒結構性訊號)
- ❌ 不要為單一 symbol 改獨立閾值(違反 atlas-mcp-trigger-monitor v6.22 統一 signature)
- ❌ 不要繞過 narrative_get_chains 驗證(雙因素共振是高信心訊號的來源)
- ❌ 不要把模板寫成「觸發就加碼」(對位 mission「保守者存活」原則,Aggressive 配置仍需時點 + 配置規則)


## §10 已知未對位 endpoint 限制 — v0.3 補封(T3-A253)

對位 T3-A252 ad-hoc verification + T3-A253 v0.3 設計 pivot:

**v0.1 / v0.2 (T3-A248 commit eeb20aa 已落,但 dormant)**:
- 設計依賴 `monthly_revenue_yoy_pct` 欄位
- 真實 atlas-mcp `/api/stock/fundamentals` 不暴露此欄位(只有 `DividendYield / PB / PE / PS / Sector` 5 欄)
- 真實跑結果:`failed reason=monthly_revenue_yoy_threshold_not_met`(結構性誠實,未編造)
- dormant 原因 = 設計 vs endpoint 暴露面不匹配

**v0.3 (本版,T3-A253 補封)**:
- pivot 改用 `stock_get_chips` 單日當點 + `capital_flow_summary` 整體 z-score
- 真實 data 範例(2026-08-03):2330 `domestic_fund_net: 387.45`(投信當日買超 387 張)
- 設備鏈 3 檔(3680/3533/5434)同方案,aggregate 投信 `domestic_fund_net > +X 合計` + `capital_flow_summary` 投信 z_score > 1.0 同步 → 觸發

**解封條件**:
- 真實 trigger 預期 2026 Q3 ~ 2027 Q1 AI 設備鏈採購旺季,與 T3-A248 SK-31 §2.7 的「訂單跳升點」鏈對位
- 之後若 atlas-go 補 monthly_revenue_yoy_pct 欄位 → 仍可回歸 v0.1/v0.2 月營收鏈(獨立 v0.4 設計)

**為什麼 v0.3 不用 foreign_investor_net + dealer_net**:
- v0.3 設計對位 mission「跟隨聰明錢」原則(對位 SOUL §3.5 + 哲學「由上而下,由外而內」)
- 投信 = 國內聰明錢,**最直接**反映台股內部對 AI 半導體的 allocation
- 外資 + 自營 = 已被既有 trigger(外 12 已觸發,自營非 monthly cadence 訊號)

**trigger-monitor.py 對位**:
- § A.elif is_fundamentals_revenue_yoy:分支擴增(不破壞 v6.22 `field+metric+threshold` signature)
- § A.擴 `is_chips_aggregate` 分支:多 symbol 單日 aggregate(新分支)
- main() /14 維持

**真實觸發預期**(2026-08-04 today):
- 對位 z_score:1.678 + 設備鏈 3680 投信買超確認 → 設備鏈若當日同步,可能觸發
- 不觸發也屬結構性誠實「未達觸發條件」(對位 §4)

對位回鏈對位 v0.3 對位 SK-31 對位 #14 對位 T3-A248 對位 kaecer B+C 對位「精準預測」核心。
