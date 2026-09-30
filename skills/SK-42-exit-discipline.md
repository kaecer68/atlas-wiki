---
title: SK-42 出場紀律：事件／技術／時間＋風控四類規則（atlas 對位版）
description: "問「什麼時候該賣／停損怎麼設／要不要續抱」時載入。"
type: skill-inbound
source: "外部（2026-09-30 直接抓取、HTTP 200 驗證）：Moskowitz-Ooi-Pedersen, Time Series Momentum（AQR 轉載 JFE 2012）、Daniel & Moskowitz, Momentum Crashes（NBER w20439）、Moreira & Muir (2017) Volatility-Managed Portfolios（NBER w22208）；內部：atlas-notes drawdown-playbook-v0.1、position-decision-card(v0.1)、對位頁 SK-16／SK-19／SK-21／SK-40"
ingested_at: 2026-09-30
status: active
tier: T2
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [narrative_get_events, macro_get_snapshot_latest, stock_get_chips, universe_get_sessions]
verification: 2026-09-30 L3 實跑 7 端點 200（/api/dashboard/risk、/api/dashboard/sessions、/api/parameters、/api/stock/quote?symbol=2330、/api/stock/chips?symbol=2330、/api/narrative/events、/api/backtest/signals，12:14:41-12:16+08:00）＋3 份外部來源（同日抓取 200）；SSRN 之停損有效性文獻 403 無法驗證 ⇒ 標待查、不引用
last_verified: 2026-09-30
l3_run_at: 2026-09-30
l3_run_by: prime-agent（atlas-wiki G2 出場紀律頁）
l3_endpoints_probed:
  - "200：/api/dashboard/risk、/api/dashboard/sessions、/api/parameters（2026-09-30T12:14:41+08:00 起，同批 12:14:43 止）"
  - "200：/api/stock/quote?symbol=2330、/api/stock/chips?symbol=2330、/api/narrative/events、/api/backtest/signals（2026-09-30T12:14:41+08:00 起，同批 12:16 止）"
sources:
  - "Moskowitz, Ooi, Pedersen (2012), Time Series Momentum, Journal of Financial Economics（AQR 轉載頁 URL: https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum ，抓取 200／2026-09-30）"
  - "Daniel & Moskowitz, Momentum Crashes, NBER Working Paper w20439（URL: https://www.nber.org/papers/w20439 ，抓取 200／2026-09-30）"
  - "Moreira & Muir (2017), Volatility-Managed Portfolios, NBER Working Paper w22208（URL: https://www.nber.org/papers/w22208 ，抓取 200／2026-09-30）"
  - "內部（T3）：atlas-notes drawdown-playbook-v0.1、position-decision-card v0.1；atlas-wiki SK-16／SK-19／SK-21／SK-40。停損有效性的學術反證文獻（Kaminski & Lo 類）**待查**（SSRN 403，2026-09-30）"
related: [skills/SK-16-long-short-decile.md, skills/SK-19-cost-tax-adjustment.md, skills/SK-21-delisting-robustness.md, skills/SK-40-behavioral-bias-checklist.md]
---

## 一句話定位

出場必須**事前寫死**（規則、價位、期限），不能等「感覺不對」才賣——因為行為研究指出人會不願實現虧損（對位 SK-40 的處分效應）。本頁把出場拆成四類可對位 atlas 資料的規則：**事件型／技術型／時間型／風控型**。

## 論文版概念

**學理基礎（三篇，皆為外部可查來源）**

1. **趨勢與時間序列動能**：Moskowitz、Ooi、Pedersen（JFE 2012）證明「時間序列動能」在多資產上長期存在 ⇒ 出場（趨勢反轉）可用**規則化訊號**處理，不必依賴預測。
2. **動能崩潰（Momentum Crashes）**：Daniel & Moskowitz（NBER w20439）指出動能策略在市場反轉期會出現**極端回撤** ⇒ **出場與風控規則在崩潰期最重要**。
3. **波動管理**：Moreira & Muir（2017）顯示高波動時降低曝險可改善風險調整後報酬 ⇒ 這是「風控型出場（縮部位而非全出）」的學理基礎。

**反證（必須一起講）**：停損不是萬靈丹——在均值回歸／高雜訊市場，機械停損可能**降低期望報酬**。另一支（Kaminski & Lo 類）文獻本次**無法驗證**（SSRN 403）⇒ 標待查，不作為本頁結論。

**四類出場規則（都可事前寫死）**

| 類型 | 觸發條件 | atlas 對位資料 |
|---|---|---|
| **事件型** | 事件到期（`expires`）或事件反轉（主題由多轉空） | `/api/narrative/events`（事件 id／theme／expires） |
| **技術型** | 跌破事前寫定的停損價；或籌碼反轉（外資由買轉賣） | `/api/stock/quote?symbol=`、`/api/stock/chips?symbol=` |
| **時間型** | 持有期到（例：事件窗口結束、季報公布後）即強制檢視 | `/api/dashboard/sessions`（交易日曆）；對位 SK-16 |
| **風控型** | `gate_mode` 非 NORMAL／系統降級 ⇒ 縮部位（非全出） | `/api/dashboard/risk`、`/api/dashboard/sessions` |

**成本提醒**：每次出場都要付證交稅與手續費（對位 SK-19、`/api/dashboard/tax-snapshot`）⇒ 過度進出本身會吃掉報酬（對位 SK-40 的 66% 費稅結構）。

## atlas 對位

| 目的 | 查什麼 | 端點 |
|---|---|---|
| 事件窗口（事件型出場） | 事件 id／主題／到期日 | `/api/narrative/events` |
| 停損價與當日價格 | 最新價、當日高低 | `/api/stock/quote?symbol=` |
| 籌碼反轉（技術型） | 外資／投信／自營買賣超 | `/api/stock/chips?symbol=` |
| 風險閘門（風控型） | gate_mode、風險快照 | `/api/dashboard/risk` |
| 交易日曆（時間型） | session 清單與 regime | `/api/dashboard/sessions` |
| 參數與門檻 | 可查參數表 | `/api/parameters` |

## 散戶解讀

1. **下單前就寫好**三個數字：停損價、最長持有期、事件到期日（＝SK-40 檢查表第 5 欄）。
2. 到價就出，不改規則；要改規則是**下一筆**的事。
3. 事件到期（`expires`）當天**必須檢視**，不能自動續抱。
4. 系統風險升高（gate_mode 非 NORMAL）時**降部位**，不是硬抱。
5. 不要用「攤平」取代停損：那是處分效應的另一種形式（SK-40）。

## 驗證方式

- **L3（2026-09-30 實跑）**：`/api/dashboard/risk`、`/api/dashboard/sessions`、`/api/parameters`、`/api/stock/quote?symbol=2330`、`/api/stock/chips?symbol=2330`、`/api/narrative/events`、`/api/backtest/signals` 皆 **200**（12:14:41-12:16 +08:00，帶 `X-API-Key`）。
- **外部來源（2026-09-30 抓取 200）**：AQR 轉載之 Time Series Momentum；NBER w20439 Momentum Crashes；NBER w22208 Volatility-Managed Portfolios。
- **來源分級**：期刊／NBER 工作論文 = T2；內部規則與對位檔 = T3；**無法驗證者標待查**（SSRN 403 之停損文獻）。

## 不能主張什麼

- 不主張停損能提高期望報酬：反證存在，且本頁未在台股資料上實測。
- 不提供「最佳停損百分比」：它取決於策略與波動，本頁只給規則化流程。
- 不保證事件型出場能避開事件損失（事件結果不預測）。
- 不引用未驗證的 SSRN 文獻作為結論支撐。

## 未消化

- [ ] 停損有效性的學術反證（Kaminski & Lo 類）**待查**：SSRN 403，需另找可驗證來源（NBER／期刊開放版本）。
- [ ] 四類出場規則**未在台股資料回測**（缺 atlas 端可用的停損回測）。
- [ ] 與 SK-16（十分位重平衡）／SK-21（排除仙股穩健性）的對位細節待補。
- [ ] 處分效應原始文獻（Barber et al. 2007）目前僅經 atlas-notes 轉引，**缺直接來源**。
