---
template_id: trigger-equipment-capex-external-report-cycle
template_number: 15
type: cron-cadence-trigger(週期型)
cycle_type: annual-semi-annual
---

# atlas-mcp Trigger Template #15 — trigger-equipment-capex-external-report-cycle

> [2026-08-22 快照:21] templates/*.md 實數 21 檔（本檔「現有 N 模板/第 N 模板」為撰寫當下歷史計數，快照統一，數字不一屬歷史演進）

**對位**:B 階段 kaecer 拍板「+ 第 15 template」+ T3-A248 v6.46 governance + SK-31 §6 對位
**對位文獻**:UNCTAD WIR(5/21 announcement + 7/7 release)+ Stanford HAI AI Index(4 月 release)+ HKS M-RCBG WP(5 月 release)
**對位 ATLAS_METHODOLOGY.md** v1.0 §一 投資哲學(由上而下,由外而內)
**對位 narrative**:1 份外部報告發布 = 1 次 narrative hit_rate 重置事件,本模板將其結構化為週期 trigger
**立此日期**:2026-08-04
**立此原因**:kaecer 「B+C」拍板 + SK-31 §6「對位外部報告 cadence」待辦 = C 階段「第六條鐵律」後配套執行端

---

## §1 設計差異(對位既有 14 templates)

| 既 templates | 本 template |
|-------------|-------------|
| 即時觸發(5 分鐘 cron)+ 結構性誠實「單日可達」 | **週期觸發**(annual/semi-annual)+ 結構性誠實「**週期啟動有錨**」 |
| quote + fundamentals + chips 為主 | **`external_report_calendar` + `stock_get_quote 2330/3680` 為主** |
| 命中 = 立即通知 | 命中 = **對位 1 份外部報告 + 重置 hit_rate 觀察窗口** |

**核心價值**:**把「外部報告 release 週期」變成結構化 cron 事件**,讓 atlas 不再「讀完歸檔」,而是「**每當 UNCTAD/HAI/HKS release 新報告時,自動對位 narrative hit_rate 基線**」。這是 SK-31 §6 第 2 條待辦的執行端。

## §2 觸發條件(週期型,不是即時)

**錨點 anchor**(對位既報告 release calendar):

| 錨點 | 來源 | 預期時點 | 對位 atlas 行為 |
|------|------|---------|---------------|
| **annual-spring-WIR** | UNCTAD World Investment Report | 每年 4-7 月(annual) | 讀 `~/workspace/atlas-notes/12-ext-research/{年度}-un-investment/`,落 SK-31 §2 基線重置 |
| **annual-spring-HAI** | Stanford HAI AI Index Report | 每年 4 月(annual) | 同上 + 對位 HAI 第 4 章(經濟) |
| **annual-spring-BIS** | BIS Annual Economic Report | 每年 6 月(annual) | 對位「AI investment race」章節 |
| **semi-annual-WEO** | IMF World Economic Outlook | 4 月 + 10 月 | 對位全球外需,主要驗 macro snapshot |
| **irregular-HKS** | HKS M-RCBG Working Paper | irregular(本研究納入) | 對位 policy framework |

## §3 觸發流程(對位 C 階段第六條鐵律)

### Stage 1:外部報告 announce 檢測

- cron job 每 24 小時跑 1 次 `web_search` 對位上述 5 個錨點
- 一旦命中(例:「UNCTAD WIR 2027 announce」)→ Stage 2

### Stage 2:報告內容讀取 + 對位

- 讀 report key 投資數字 + 對位現有 narrative model 的 hit_rate 基線
- 例:WIR 2027 announce → 讀「半導體 5 年 CAGR +X%」「AI 5 年 CAGR +Y%」「TSMC announced $Z 億」+ 與上一版對比
- 計算 delta:`Δ = (新數字 - 舊數字) / 舊數字`
- 若 delta > ±20% 任意關鍵數字 → **觸發 SK-31 §6 第 2 條「對位外部報告 cadence」對位觀察 30 天**

### Stage 3:散戶解讀(對位 SK-31 §4)

- 寫入 `~/workspace/atlas-notes/04-daily/{日期}-ext-report-cycle.md` 當週日誌
- Telegram 通知 kaecer(SOUL §4.1)
- **落 `_consult-index.md` §6 「external report cycle log」第 N 筆**

## §4 結構性誠實護欄

- ⚠️ **週期型 trigger 與即時 trigger 完全不同**:**命中可能失敗但不是錯**(例:2026 年 4 月 HAI 真的出來,但內容是去年同向,delta < 20%,所以「不觸發」是正確行為)
- **絕對禁止的兩件事**:
  - ❌ 不要把「報告有沒有出來」當觸發(只是「報告有」≠ 「信號強」)
  - ❌ 不要把「內容摘要」包裝成觸發(對位 SOUL §6 紅線「不補造數據」)
- **必跑的驗證鏈**:
  - Stage 1:`web_search` 命中 → 比對 5 個錨點 keyword
  - Stage 2:讀實際 PDF/HTML → 數字對位 → delta 計算
  - Stage 3:三段全跑通才「觸發」(任一失敗 = 結構性誠實標「未達觸發條件」)

## §5 atlas-mcp-trigger-monitor.py 修改

```python
"equipment-capex-external-report-cycle": {
    "name": "外部權威報告週期觸發(annual/semi-annual)",
    "file": "trigger-equipment-capex-external-report-cycle.md",
    "condition": "5 錨點任一命中 + 數字對位 + delta > ±20% 對任意關鍵投資數字",
    "http_path": "N/A",  # 週期型,不走 atlas HTTP,走 web_search cron
    "field": "external_report_anchor",
    "metric": "delta_pct",
    "threshold": 20.0,
    "compare": "gt",
    "cycle_type": "annual-semi-annual",
    "extra_check": None,
    "is_custom_calc": True,
},
```

**重要差異**:本模板**不走 atlas HTTP**(沒有 api/.../external-report);走 `web_search` + `web_extract` 純文字工作。這是 14 templates 唯一一條「無 HTTP 端點」的設計,**需在 `run_triggers()` 加 `cycle_type: cron-cadence` 分支判斷**。

## §6 對位 SK-31(對位表)

| SK-31 § | 本模板 § | 連接 |
|---------|---------|------|
| §1 一句話定位 | §3 Stage 2 | 「週期性外部報告成為 atlas ground truth 校正點」的週期性端 |
| §2 論文版第 1-4 點 | §1 設計差異 + §2 錨點 | 4 條基線數字 + 3 條結構性偏離都來自這 4 個錨點 |
| §4 散戶解讀第 3 點 | §2 錨點 | 「季頻對位」執行端 |
| §5 驗證 | §5 atlas-mcp-trigger-monitor.py | 結構性誠實護欄 |
| §6 未消化第 2 條 | §3 Stage 3 | 「external_report_calendar」待辦 → 本模板落 |

## §7 對位 SKILL 與憲章

| 對位項 | 內容 |
|--------|------|
| ATLAS_METHODOLOGY §一 投資哲學 | 「由上而下,由外而內」對位「外部報告 macro → atlas narrative → 台股個股」 |
| 七時期 | 對位 high-period 區間 trigger 偏多,black_swan 區間 trigger 暫停 |
| 三態 | RISK_ON 對位 hit_rate 上調;RISK_OFF 下調;NEUTRAL 中性 |
| 散戶語言 | 「聯合國 / Stanford HAI 等機構發布新版 AI 投資報告 → atlas 自動對位台股,給出修訂訊號」 |

## §8 為什麼這模板值得加

- **現有 14 templates 全是「即時」訊號** = 不解決「半年/年週期基線重置」
- **kaecer 2026-08-04「B+C 才是正確的」**:B 階段落 trigger 但若無 C 規範綁,半年後沒人重讀 WIR → 觸發仍可能漏觸
- **本模板是 C 階段的「執行端」**:第六條鐵律規範「外部報告週期稽核」需有 trigger 撐;**沒 trigger,規範是死的**
- **2027 年 4 月驗收**:第一個 WIR + HAI 雙 release 週期 → 此模板是否真實自動運作 = B+C 拍板的 ground truth

## §9 不該做的事

- ❌ 不要把週期型 trigger 與即時 trigger 共用同一 cron(節奏差異會互相干擾)
- ❌ 不要把 5 錨點縮成 1 個(UNCTAD 與 HAI 是兩個不同口徑,縮了會失去交叉驗證)
- ❌ 不要把 trigger 寫成「讀完報告就賣出」(對位結構性誠實 §5)
- ❌ 不要繞過 governance-log 留痕(週期型 trigger 必須有 T3 evidence)
- ❌ 不要 mock(本模板絕對禁止 mock 觸發:即使沒命中也誠實標「未達觸發條件」)

參見:[[concepts/taiwan-export-orders-semiconductor-cycle]]（L2 台灣出口/半導體景氣——本模板外部報告數字的台灣端月頻驗證）[2026-08-22 audit-fix 接線]
