---
title: SK-41 部位大小與資金管理：回撤反推法（atlas 對位版）
description: "問「這筆該買多少／資金怎麼分配／我最多能賠多少」時載入。"
type: skill-inbound
source: "內部：atlas-wiki concepts/atlas-risk-management-framework §8.1（5-10%／20-30% 上限、原文無來源）、atlas-notes position-decision-card(v0.1)、drawdown-playbook-v0.1、cape-aware-dynamic-allocation-v6；外部（2026-09-30 直接抓取、HTTP 200 驗證）：Kelly (1956) BSTJ 35(4)、Thorp (2007) Kelly Criterion in Blackjack/Sports Betting/Stock Market、Moreira & Muir (2017) NBER w22208"
ingested_at: 2026-09-30
status: active
tier: T2
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [macro_get_snapshot_latest, data_get_channels]
verification: 2026-09-30 L3 實跑 4 端點 200（/api/parameters、/api/dashboard/risk、/api/dashboard/sessions、/api/dashboard/tax-snapshot，12:05:48-12:05:50+08:00）＋3 份外部來源同（2026-09-30 抓取 200）＋內部 §8.1 上限標為「無來源的內部慣例」
last_verified: 2026-09-30
l3_run_at: 2026-09-30
l3_run_by: prime-agent（atlas-wiki G1 部位大小頁）
l3_endpoints_probed:
  - "200：/api/parameters、/api/dashboard/risk、/api/dashboard/sessions、/api/dashboard/tax-snapshot（2026-09-30T12:05:48+08:00 起，同批 12:05:50 止）"
sources:
  - "Kelly, J. L. (1956), A New Interpretation of Information Rate, Bell System Technical Journal 35(4):917-926（URL: https://www.princeton.edu/~wbialek/rome/refs/kelly_56.pdf ，抓取 200／2026-09-30）"
  - "Thorp, E. O. (2007), The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market（URL: http://www.edwardothorp.com/wp-content/uploads/2016/11/TheKellyCriterionAndTheStockMarket.pdf ，抓取 200／2026-09-30）"
  - "Moreira, A. & Muir, T. (2017), Volatility-Managed Portfolios, NBER Working Paper w22208（URL: https://www.nber.org/papers/w22208 ，抓取 200／2026-09-30）"
  - "內部（T3，無外部來源，標為實務慣例）：atlas-wiki concepts/atlas-risk-management-framework §8.1 的 5-10%／20-30% 上限（**待查**，2026-09-30）；atlas-notes position-decision-card v0.1（2026-07-11）"
related: [skills/SK-19-cost-tax-adjustment.md, skills/SK-16-long-short-decile.md, skills/SK-37-liquidity-spread-screening.md, skills/SK-40-behavioral-bias-checklist.md]
---

## 一句話定位

部位大小由「**可投入資金 × 可承受回撤**」反推，不是由「看好程度」決定：散戶最常見的致命錯誤，是用「我有多看好」當成買多少的依據。本頁給三種可算的方法（回撤反推、分數凱利、波動率目標）與 atlas 可查的輸入。

## 論文版概念

**四種方法（由簡到繁）**

1. **回撤反推法（本頁主推，散戶可直接算）**
   - 令 `L` = 這筆最多可承受虧損（**金額**）、`d` = 停損距離（%）
   - **部位上限 = L ÷ d**
   - 例：可承受虧損 30,000 元、停損 10% ⇒ 部位上限 **300,000 元**
   - 再用組合層檢查：單一部位 ≤ 總資金 20%、持股 ≥ 5 檔、現金 ≥ 10%
2. **分數凱利（fractional Kelly）**：Kelly (1956) 給最大化長期成長率的比例 `f* = edge / odds`；實務因參數估計誤差會**過度下注**，Thorp (2007) 主張用 **1/4 – 1/2 凱利**。本頁**不給單一「最佳比例」**。
3. **波動率目標（volatility targeting）**：以目標波動度反推部位，部位與波動度成反比（Moreira & Muir 2017）。
4. **上限規則**：atlas 內部 `concepts/atlas-risk-management-framework` §8.1 寫 5-10%／20-30% 上限——**原文無來源**，本頁僅當「內部慣例」引用，不當外部事實（見 §未消化）。

**最小可下單位（台股結構現實）**：台股 1 張 = 1,000 股；資金不足一張時可交易零股，但撮合方式與流動性不同 ⇒ 直接影響可實現部位與滑價（對位 SK-37）。零股撮合細節**待驗證**（見 §未消化）。

## atlas 對位

| 目的 | atlas 查什麼 | 端點或工具 |
|---|---|---|
| 當日風險狀態（決定是否縮部位） | 風險閘門與 regime | `/api/dashboard/risk`、`/api/dashboard/sessions` |
| 可用參數與門檻 | 參數表 | `/api/parameters` |
| 把費稅算進期望值 | 稅後損益快照 | `/api/dashboard/tax-snapshot`（對位 SK-19） |
| 滑價與流動性 | 分位與買賣價差 | 對位 SK-37 |
| 下單前檢查表 | 5 欄檢查 | 對位 SK-40 |

## 散戶解讀

1. 先寫「**我最多能賠多少錢**」（金額），不是「我想賺多少」。
2. 用公式算上限：**部位上限 = 可承受虧損 ÷ 停損距離**。
3. 三個檢查：單一部位 ≤ 總資金 20%？持股 ≥ 5 檔？現金 ≥ 10%？
4. 停損距離寫不出來 ⇒ **不能下單**（SK-40 檢查表第 5 欄）。
5. 小資金：若「1 張」就超過上限，**改用零股或直接不做**，不要為了湊一張而放大部位。

## 驗證方式

- **L3（2026-09-30 實跑）**：`/api/parameters`、`/api/dashboard/risk`、`/api/dashboard/sessions`、`/api/dashboard/tax-snapshot` 皆 **200**（12:05:48-12:05:50 +08:00，帶 `X-API-Key`）。
- **外部來源（2026-09-30 直接抓取，HTTP 200）**：Kelly (1956) BSTJ 35(4):917-926；Thorp (2007) Kelly Criterion 論文；Moreira & Muir (2017) NBER w22208。
- **內部來源（T3）**：`concepts/atlas-risk-management-framework` §8.1（**無來源**）、atlas-notes `position-decision-card`(v0.1, 2026-07-11)、`drawdown-playbook-v0.1`。
- **來源分級**：同儕審查期刊／NBER 工作論文 = T2；書籍與內部慣例 = T3；**未標來源的內部數字不得當事實引用**。

## 不能主張什麼

- 不回答「該買哪一檔」；本頁只處理「買多少」。
- 不給單一「最佳部位比例」數字：凱利在參數有誤差時會過度下注。
- 5-10%／20-30% 上限目前**無外部來源**，只能當內部慣例，不能當業界標準引用。
- 不保證任何回撤推導能避免虧損（它只控制單筆風險，不控制策略期望值）。

## 未消化

- [ ] 台股零股撮合規則（撮合頻率、手續費、最小單位）**待官方 URL 驗證**：嘗試的 TWSE 頁面皆 404。
- [ ] `atlas-risk-management-framework` §8.1 的 5-10%／20-30% 上限**缺來源**，需補來源或改寫。
- [ ] 凱利比例在台股實際報酬分布下的適用性未實測（缺本地回測）。
- [ ] 波動率目標法需要 atlas 波動度端點對位（目前未確認可用端點）。
