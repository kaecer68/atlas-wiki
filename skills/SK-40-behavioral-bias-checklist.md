---
title: SK-40 行為偏誤反制：下單前檢查表（atlas 對位版）
description: "問「我一直賠錢是不是心態問題／下單前該檢查什麼／為什麼追高就被套」時載入。"
type: skill-inbound
source: "atlas-notes（皆 2026-07-20、T2）：retail-investor-trading-loss-barber-2009、eight-joys-bahi-retail-behavior-protocol、position-decision-card(v0.1)、forrest-gump-investing-fact-vs-story；外部文獻：Barber-Lee-Liu-Odean (2009) RFS 22(2):609-632、周行一《一生金錢無虞平衡理財法》(天下文化 2023)、闕又上《阿甘投資法》(天下文化 2020)"
ingested_at: 2026-09-30
status: active
tier: T2
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [universe_get_sessions]
verification: 2026-09-30 L3 實跑 3 端點 200（/api/dashboard/retail-sentiment、/api/dashboard/risk、/api/dashboard/sessions，08:58:04+08:00 起）＋ 4 份 atlas-notes T2 來源 ＋ Barber 2009 台灣普查數字逐項核對（3.8pp 與 27/32/34/7 拆解）
last_verified: 2026-09-30
l3_run_at: 2026-09-30
l3_run_by: prime-agent（atlas-wiki G3 行為偏誤頁）
l3_endpoints_probed:
  - "200：/api/dashboard/retail-sentiment、/api/dashboard/risk、/api/dashboard/sessions（2026-09-30T08:58:04+08:00 起，同批 08:58:05 止）"
sources:
  - "Barber, Lee, Liu, Odean (2009), Just How Much Do Individual Investors Lose by Trading?, Review of Financial Studies 22(2):609-632（樣本 1995-1999 台灣 TWSE 全體投資人普查）"
  - "URL: http://faculty.haas.berkeley.edu/odean/papers/taiwan%20performance/just%20how%20much%20do%20investors%20lose.pdf"
  - 周行一《一生金錢無虞平衡理財法》，天下文化 2023（八喜／BAHI 行為紀律協議）
  - 闕又上《阿甘投資法》，天下文化 2020（含第三方績效反證；來源分級待補）
  - atlas-notes 對位檔（2026-07-20）：retail-investor-trading-loss-barber-2009／eight-joys-bahi-retail-behavior-protocol／position-decision-card／forrest-gump-investing-fact-vs-story
related: [skills/SK-19-cost-tax-adjustment.md, skills/SK-16-long-short-decile.md, skills/SK-37-liquidity-spread-screening.md]
---

## 一句話定位

散戶賠錢的第一大來源不是選錯股，是**下單方式**：Barber-Lee-Liu-Odean (2009) 用 1995-1999 台灣全體投資人普查資料估計，散戶每年因交易損失 **3.8 個百分點**，其中 **66%（手續費 32%＋交易稅 34%）是週轉率成本**、27% 是追價交易損失、7% 是擇時錯誤。反制不靠預測，靠**行為規則＋下單前檢查表**。

## 論文版概念

**證據（台灣普查，來源等級最高）**

| 指標 | 數字 |
|---|---|
| 散戶每年交易損失 | 3.8 個百分點 |
| 損失拆解 | 手續費 32%／交易稅 34%／追價交易損失 27%／擇時 7% |
| 機構同期（扣費稅後） | ＋1.5 個百分點 |
| 1995-1999 散戶佔台股成交額 | 89.5% |
| 損失佔台灣 GDP／個人總所得 | 2.2%／2.8% |

原文關鍵句：「virtually all of the individual trading losses can be traced to their aggressive orders; passive orders placed by individuals are profitable at short horizons」——**虧損幾乎全部來自積極單（追價／市價單），被動限價單短期是賺的**。

**六類偏誤與其證據**

1. **過度交易（高週轉）**：費稅 66% 直接吃掉報酬，與預測能力無關。
2. **追漲殺跌（積極單）**：論文把「幾乎所有個別投資人虧損」歸因於積極單。
3. **處分效應（賣賺抱賠）**：「等回本」是它最常見的延長型。
4. **凹單／攤平**：同屬處分效應的行為延伸（不希望實現虧損）。
5. **錨定**：以自身成本價當參考點，而不是當日環境。
6. **故事取代事實**：對位檔 forrest-gump-investing-fact-vs-story 收錄第三方績效反證（含 10 年 4.83% 與 22 年淨值倒退）。

**限制（必須一起講）**：樣本為 1995-1999（當時散戶佔成交 89.5%，現約 50-60%；費稅結構亦改），且只測到 1 年持有期 ⇒ **3.8% 這個具體數字可能縮小，但「追價／高週轉 → 虧損」的結構性關係應仍成立**。

**反制協議（八喜／BAHI，周行一 2023）**：規（紀律）／等（等待）／分（分散）／被（被動）／長（長期）／複（複利）／調（再平衡）／平（平衡）。

## atlas 對位

| 檢查點 | 對應偏誤 | atlas 查什麼 | 端點或工具 |
|---|---|---|---|
| 這筆會花多少成本 | 過度交易 | 手續費與證交稅試算 | `/api/dashboard/tax-snapshot`（對位 SK-19） |
| 今天環境支持這個動作嗎 | 錨定、追價 | 當日風險閘門與 regime | `/api/dashboard/risk`、`/api/dashboard/sessions` |
| 我是不是被群眾情緒推著走 | 羊群、追漲殺跌 | 散戶情緒分數與融資變化 | `/api/dashboard/retail-sentiment` |
| 流動性夠不夠（滑價） | 追價 | 流動性分位與買賣價差 | 對位 SK-37 |

## 散戶解讀

- 要買就用**限價單**掛，**不要用市價單追漲停**（論文：被動單短期是賺的）。
- **不要每天下單**：週轉率減半，那一塊 66% 的費稅成本就減半。
- 「等回本」不是策略，是處分效應。
- **下面 5 欄填不出具體答案，就不要下單**。

**下單前檢查表（5 欄）**

1. 我為什麼現在買／賣？（不能寫「感覺會漲」「朋友說會賺」）
2. 我能承受的最大虧損是多少？（寫具體金額）
3. 環境支持這個動作嗎？（引用當日 regime 與風險狀態）
4. 我預計持有多久？（天／週／月，不接受「不知道」）
5. 什麼情況我承認錯了？（具體價位或條件，不接受「看情況」）

## 驗證方式

- **L3（2026-09-30 實跑）**：`/api/dashboard/retail-sentiment`、`/api/dashboard/risk`、`/api/dashboard/sessions` 皆回 **200**（08:58:04-08:58:05 +08:00，HTTP probe 帶 `X-API-Key`）。
- **來源**：Barber et al. (2009) RFS 22(2)（1995-1999 台灣普查）；周行一（2023）；闕又上（2020）；atlas-notes 對位 4 檔（2026-07-20）。
- 本頁每個數字都可回溯至上列來源；拆解比例與 3.8pp 取自論文 abstract 與對位檔。

## 不能主張什麼

- 不能說「避開偏誤就會賺錢」：本頁解的是「為什麼賠」（floor 層），不提供進場時機與選股 alpha。
- 不能把 3.8% 當成**現行**台灣數字（樣本 1995-1999）。
- 不能取代個股研究與部位控管（部位大小屬另一缺口，見 §未消化）。

## 未消化

- [ ] 2026 年台灣散戶交易成本損失的**重算**（Barber 樣本已 27 年、散戶佔比由 89.5% 降至約 50-60%）——目前 atlas 無對應研究。
- [ ] 八喜（BAHI）為書籍框架（T2），**非同儕審查**，缺學術對位。
- [ ] 對位檔中的第三方績效反證（10 年 4.83%、22 年淨值倒退）尚未建立來源分級。
- [ ] 部位大小（G1）尚未成頁：檢查表第 2 欄的「具體金額」目前無 atlas-wiki 頁可對位。
