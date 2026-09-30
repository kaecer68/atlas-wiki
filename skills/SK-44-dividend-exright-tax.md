---
title: SK-44 除權息與股利稅務：atlas 對位與待補清單
description: "問「除息會扣多少／股利要繳多少稅／二代健保怎麼算」時載入。"
type: skill-inbound
source: "內部（T3，已驗證）：atlas `/api/parameters` 的 `tax.dividend_tax_rate`／`tax.nhi_surcharge_rate`／`tax.transaction_tax_rate` 與 `dividend_season` 敘事鉤子（2026-09-30 實跑）；`skills/SK-19-cost-tax-adjustment.md`（稅務事實本體，本頁不重複數字）；外部：除權息價格實務之官方來源**待查**（TWSE／MOPS 子頁以 URL 猜測皆回 404 頁；本 session 無 web search）"
ingested_at: 2026-09-30
status: active
tier: T3
confidence: medium
atlas_go_relevance: medium
mcp_tools_used: [parameters_get, report_get_tax_snapshot]
verification: 2026-09-30 L3 實跑 2 端點 200（/api/parameters、/api/dashboard/tax-snapshot，12:36:19+08:00 起）＋參數值逐鍵核對（tax.dividend_tax_rate=0.28、tax.nhi_surcharge_rate=0.0211、tax.transaction_tax_rate=0.003、narrative.event_ttl_multiplier.dividend_season=30、narrative_conviction.theme_hit_rates.dividend_season=0.65）
last_verified: 2026-09-30
l3_run_at: 2026-09-30
l3_run_by: prime-agent（atlas-wiki G4 除權息頁）
l3_endpoints_probed:
  - "200：/api/parameters、/api/dashboard/tax-snapshot（2026-09-30T12:36:19+08:00 起，同批 12:36:19 止）"
  - "參數快照：tax.dividend_tax_rate=0.28、tax.nhi_surcharge_rate=0.0211、tax.transaction_tax_rate=0.003（2026-09-30T12:36:19+08:00）"
sources:
  - "內部（T3，2026-09-30 實跑）：atlas `/api/parameters`（1669 keys）——`tax.dividend_tax_rate`=0.28、`tax.nhi_surcharge_rate`=0.0211、`tax.transaction_tax_rate`=0.003、`stockpicker.costs.round_trip_pct`=0.00585"
  - "內部（T3）：`skills/SK-19-cost-tax-adjustment.md` §散戶稅後淨報酬三塊（股利 28% 分離課稅或併入綜所稅 8.5% 抵減、每戶上限 8 萬元；單次股利 ≥2 萬元另扣補充保費 2.11%）——**本頁不重複該頁數字**"
  - "臺灣證券交易所 除權除息計算結果表 https://www.twse.com.tw/zh/announcement/ex-right/twt49u.html （抓取 200／2026-09-30）— 頁內明載『權值+息值 = 除權息前收盤價 - 除權息參考價』"
  - "臺灣證券交易所股份有限公司營業細則（法規分享知識庫）https://twse-regulation.twse.com.tw/m/LawContent.aspx?FID=FL007304 （抓取 200／2026-09-30）— 除權息參考價之制度依據"
  - "**待查（2026-09-30）**：各式除權息（含員工紅利、現金增資等混合情形）之完整計算、填息／貼息之統計定義、股利發放時程——尚未取得對應官方頁面" 
related: [skills/SK-19-cost-tax-adjustment.md, skills/SK-40-behavioral-bias-checklist.md]
---

## 一句話定位

除權息有**兩件事要分開算**：①**價格面**（除息後參考價往下調、填息或貼息）②**稅費面**（股利所得稅與二代健保）。atlas 目前**只對位了稅費面**（參數與 tax snapshot），價格面**沒有端點**、官方來源也待查。

## 論文版概念

**價格面（除權息的本體）**

- 除權息當日的交易**參考價**由證交所依公式計算；TWSE 除權除息計算結果表頁明載：**權值＋息值＝除權息前收盤價 − 除權息參考價**（來源見 §驗證方式，2026-09-30 抓取）。
- 之後是否「填息／填權」是**市場結果**，不是保證：參考價下調後回不回來，取決於後續買賣。
- 對散戶的意義：**除息不是額外獲利**——領到的股利與參考價下調大致互抵，真正的差別在**稅**與**時間**。
- 制度依據：證交所營業細則（法規分享知識庫，2026-09-30 抓取 200）。**本頁只寫來源可查的式子，其餘（各類除權息完整計算）仍屬未消化**。

**稅費面（atlas 已對位）**

| 項目 | atlas 參數鍵 | 值（2026-09-30 實跑） |
|---|---|---|
| 股利所得稅率 | `tax.dividend_tax_rate` | 0.28 |
| 二代健保補充保費 | `tax.nhi_surcharge_rate` | 0.0211 |
| 證交稅（賣方） | `tax.transaction_tax_rate` | 0.003 |
| 來回成本 | `stockpicker.costs.round_trip_pct` | 0.00585 |

**敘事層的股利季節鉤子**：`narrative.event_ttl_multiplier.dividend_season`=30（股利季事件存活期 ×30）、`narrative_conviction.theme_hit_rates.dividend_season`=0.65 ⇒ atlas 已把「股利季」當成一個敘事主題處理。

## atlas 對位

| 想知道 | 查什麼 | 端點 |
|---|---|---|
| 股利稅率、健保費率 | 參數表 | `/api/parameters`（`tax.*`） |
| 我的稅後損益 | 稅後快照（含 `total_tax_paid`） | `/api/dashboard/tax-snapshot` |
| 交易成本口徑 | 參數表 | `/api/parameters`（`baseline.*`／`stockpicker.costs.*`） |
| 股利季事件 | 事件清單（主題 `dividend_season`） | `/api/narrative/events` |

**注意**：atlas **只給單一 `tax.transaction_tax_rate`=0.003**，當沖（0.15%）與股票型 ETF（0.1%）的低稅率**沒有欄位** ⇒ 需在 client 端覆蓋（此點 SK-19 已載）。

## 散戶解讀

1. **除息不等於賺到**：價格會下調，別把除息當報酬。
2. **高股息策略必扣兩筆**：股利所得稅 + 二代健保補充保費（單次給付門檻見 SK-19）。
3. 想算稅後實拿，用 `/api/dashboard/tax-snapshot`（含 `total_tax_paid`）對位你的實際持倉。
4. 當沖或 ETF 部位，記得**自行覆蓋稅率**（atlas 只有 0.3% 單一值）。

## 驗證方式

- **L3（2026-09-30 實跑）**：`/api/parameters`、`/api/dashboard/tax-snapshot` 皆 **200**（12:36:19+08:00，帶 `X-API-Key`）；參數值逐鍵核對見 frontmatter。
- **來源分級**：atlas 參數與頁面（T3）；稅務事實本體引用 SK-19（不在本頁重複）；價格面公式引 **TWSE 除權除息計算結果表**與**證交所營業細則**（皆 2026-09-30 抓取 200，T2／官方）。

## 不能主張什麼

- 不提供除權息參考價的**計算公式**（缺可驗證官方來源）。
- 不主張「填息」可預測；也不主張高股息策略的稅後報酬。
- 不以本頁取代 SK-19：稅務細節以 SK-19 為準（避免兩頁各寫一份數字）。
- atlas 的 0.28／0.0211 是**參數快照值**，非法規原文；法規變動時需重新核對。

## 未消化

- [ ] 除權息**完整計算**（員工紅利／現金增資等混合情形）與**填息／貼息之統計定義**、股利發放時程——官方頁面待補（2026-09-30）。
- [ ] atlas 缺當沖（0.15%）與 ETF（0.1%）稅率欄位（SK-19 已記，本頁重申需 client 覆蓋）。
- [ ] `tax.dividend_tax_rate`=0.28 是否含 8.5% 抵減情境未區分（分離課稅 vs 併入綜所稅）。
- [ ] 股利季敘事鉤子（TTL×30、hit rate 0.65）**未在台股資料驗證**其預測力。
