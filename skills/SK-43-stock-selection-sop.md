---
title: SK-43 端到端選股 SOP：九步 fail-stop 漏斗（atlas 對位版）
description: "問「我該怎麼從頭選一檔股票／選股流程是什麼」時載入。"
type: skill-inbound
source: "內部：atlas-wiki 既有 SK 頁（SK-16／SK-19／SK-21／SK-37／SK-40／SK-41／SK-42）＋atlas-notes 對位檔（hypothesis-registry、task-tracker、taiwan-usa-cape-2026q2-elevated-warning）；外部依據散見各對位頁（Barber 2009 見 SK-40、Kelly/Thorp/Moreira & Muir 見 SK-41、AQR/NBER 見 SK-42）"
ingested_at: 2026-09-30
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [universe_get_sessions, stock_get_chips, narrative_get_events, parameters_get, report_get_tax_snapshot]
verification: 2026-09-30 L3 實跑 8 端點 200（/api/dashboard/risk、/api/dashboard/sessions、/api/narrative/events、/api/parameters、/api/stock/quote?symbol=2330、/api/stock/chips?symbol=2330、/api/dashboard/tax-snapshot、/api/backtest/signals，12:33:36+08:00 起）＋內部對位 7 頁逐頁確認存在（`ls skills/SK-*.md`）
last_verified: 2026-09-30
l3_run_at: 2026-09-30
l3_run_by: prime-agent（atlas-wiki G6 選股 SOP 頁）
l3_endpoints_probed:
  - "200：/api/dashboard/risk、/api/dashboard/sessions、/api/narrative/events、/api/parameters（2026-09-30T12:33:36+08:00 起，同批 12:33:36 止）"
  - "200：/api/stock/quote?symbol=2330、/api/stock/chips?symbol=2330、/api/dashboard/tax-snapshot、/api/backtest/signals（2026-09-30T12:33:36+08:00 起，同批 12:33:36 止）"
sources:
  - "內部（T3）：atlas-wiki skills/SK-16、SK-19、SK-21、SK-37、SK-40、SK-41、SK-42（本頁為其流程串接）"
  - "外部依據（各對位頁已載明，本頁不重複引用數字）：Barber-Lee-Liu-Odean (2009) RFS 22(2)（SK-40）；Kelly (1956)／Thorp (2007)／Moreira & Muir (2017)（SK-41）；AQR Time Series Momentum／NBER w20439／w22208（SK-42）"
  - "實務慣例（本頁門檻為流程設計，非外部統計）：各步 fail-stop 判準由 atlas 現有端點可得欄位推得"
related: [skills/SK-16-long-short-decile.md, skills/SK-19-cost-tax-adjustment.md, skills/SK-21-delisting-robustness.md, skills/SK-37-liquidity-spread-screening.md, skills/SK-40-behavioral-bias-checklist.md, skills/SK-41-position-sizing-drawdown.md, skills/SK-42-exit-discipline.md]
---

## 一句話定位

選股不是「找一檔會漲的」，而是**九步關卡依序過、任何一步失敗就停**（fail-stop 漏斗）：先排除「不該做的」，剩下的才輪到「會不會漲」。

## 論文版概念

**為什麼是漏斗，不是評分制**：散戶的錯誤成本**不對稱**——一次凹單可吃掉多次小賺（對位 SK-40：Barber 2009 的損失結構裡，66% 來自手續費與交易稅、27% 來自追價交易）。因此流程設計成**先擋掉不可做的**，而不是把所有條件加權打分（加權會讓「很心動但不該做」的案子過關）。

**九步（每一步都要有可機械檢查的失敗判準）**

| # | 步驟 | atlas 查什麼 | 失敗判準（任一成立 ⇒ 停） | 對位頁 |
|---|---|---|---|---|
| 1 | 環境 | `/api/dashboard/risk`（`gate_mode`）、`/api/dashboard/sessions` | `gate_mode` 非 NORMAL 或系統降級 | SK-42 |
| 2 | 事件 | `/api/narrative/events` | 無對應事件，或事件已過期（`expires` 早於今日） | SK-42 |
| 3 | 資金與部位 | `/api/parameters`（門檻）、自填可承受虧損 | 算不出部位上限（缺停損距離或可承受虧損） | SK-41 |
| 4 | 標的與流動性 | `/api/stock/quote?symbol=` | 流動性／買賣價差不合格 | SK-37 |
| 5 | 籌碼驗證 | `/api/stock/chips?symbol=` | 外資／投信方向與事件方向不一致 | — |
| 6 | 成本 | `/api/dashboard/tax-snapshot` | 期望值扣掉費稅後 ≤ 0 | SK-19 |
| 7 | 出場規則先寫 | 自填三項（停損價／持有期／事件到期日） | 三項缺一 | SK-42 |
| 8 | 下單前檢查表 | 5 欄（理由／可承受虧損／環境／持有期／認錯條件） | 任一欄寫不出具體答案 | SK-40 |
| 9 | 事後檢討 | 交易日誌 | 未留紀錄（下次不得重複同一套邏輯） | G7 失敗模式 |

**順序不可顛倒**：先環境（1）再事件（2），因為環境不支持時任何事件都不該做；資金（3）必須在選標的（4）之前，否則會用「標的很好」回頭放大部位。

## atlas 對位

| 端點 | 取什麼 | 用在哪一步 |
|---|---|---|
| `/api/dashboard/risk` | `gate_mode`、風險快照 | 1（環境） |
| `/api/dashboard/sessions` | session 清單與 regime | 1（環境） |
| `/api/narrative/events` | 事件 id／主題／到期 | 2（事件） |
| `/api/parameters` | 可查參數與門檻 | 3（資金） |
| `/api/stock/quote?symbol=` | 最新價／當日高低 | 4（流動性） |
| `/api/stock/chips?symbol=` | 外資／投信／自營買賣超 | 5（籌碼） |
| `/api/dashboard/tax-snapshot` | 稅後損益口徑 | 6（成本） |
| `/api/backtest/signals` | 現行訊號狀態 | 6–8（輔助核對） |

## 散戶解讀

- 一句話：**先問「這筆能不能做」，再問「這檔會不會漲」。**
- 九步中任何一步卡住就是「不做」——**不做是流程的正常輸出，不是失敗**。
- 順序不能顛倒（先環境、再事件、再資金、最後才是標的）。
- 每筆都要留日誌，否則第 9 步無法檢討、同一個錯會一直犯。

## 驗證方式

- **L3（2026-09-30 實跑）**：9 步所用 8 個端點皆 **200**（12:33:36+08:00 起，帶 `X-API-Key`）。
- **內部對位**：SK-16／SK-19／SK-21／SK-37／SK-40／SK-41／SK-42 逐頁確認存在（`ls skills/SK-*.md`）。
- **來源分級**：本頁為流程設計（T3）；外部量化依據在各對位頁載明，本頁**不重複引用數字**以免雙重來源失準。

## 不能主張什麼

- 不保證流程能選到上漲標的：它只負責**排除不該做的**。
- 不以評分加權取代 fail-stop（散戶錯誤成本不對稱）。
- 各步門檻目前是流程設計**尚未以台股資料校準**（見 §未消化）。
- 第 5 步一致性檢查缺可操作定義（需先完成 G5 個股事件劇本）。

## 未消化

- [ ] 各步量化門檻（價差上限、期望值下限、部位上限係數）尚未回測校準。
- [ ] 第 5 步「籌碼與事件一致性」缺可操作定義（依賴 G5 個股事件劇本）。
- [ ] 與 SK-16（多空十分位）在「標的池」階段的關係未定（建池 vs 排序）。
- [ ] 全流程未做端到端回測；第 9 步日誌格式未定義。
