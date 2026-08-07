---
title: atlas-mcp 失效時 fail-over 政策 — 來源標籤 + 網路替代源清單
created: 2026-08-07
updated: 2026-08-07
type: concept
tags: [framework, fallback, source-attribution, methodology]
sources:
  - atlas-mcp:concepts/atals-mcp-tools-reference.md §5 三層訂閱制
  - data-source-decision ~hermes/skills/data-source-decision §1-§2 三層架構 + 端點對位
  - concepts/atlas-mcp-interpretation-guide.md §Rule 3 Proxy question
confidence: high
contested: false
contradictions: []
amendable_by: kaecer
---

# atlas-mcp fail-over 政策(2026-08-07 v1.0)

> **一句話**:atlas-mcp 不在 atlas 範圍或端點失敗時,**走 4 級 fallback 鏈**,任何引用強
> 制附來源標籤 `[來源: atlas-mcp <tool_name> @ <ISO 8601>]` 或 `[來源: <站名> @ <URL> @ <ISO 8601>]`。

## 為什麼需要 fail-over

atlas 系統**只服務台灣上市公司(TWSE)**,不涵蓋上櫃(TPEx)、興櫃(ESM)、非 TWSE 標的。
但 `atlas-outbound` 對象(散戶 / OpenClaw / hermes 對話)**沒範圍邊界**——遇到超出 atlas
範圍的 symbol 時,必須能給「有限度的服務」而不是「資料庫錯誤」這種嚇退用戶的訊息。

## 4 級 fallback 鏈(from 強至弱)

| 級 | 來源 | 何時觸發 | 標籤格式 |
|---|---|---|---|
| **L1 本地 cache** | atlas-go 預計算結果(`stock_get_fundamentals`、`stock_get_technical`) | 已在 L1 命中 | `[來源: atlas-mcp <tool> @ <ts>]` |
| **L2 atlas 端點 + HybridProvider fallback** | Fugle → TWSE OpenAPI(`stock_get_quote` 主源) | 仍在 atlas channel 範圍 | `[來源: atlas-mcp <tool> @ <ts>,channel=<fugle\|twse>]` |
| **L3 atlas 邊界外 + Web fallback** | 5 個網路替代源(見下) | symbol 不在 atlas universe(上櫃/興櫃/海外) | `[來源: <站名> @ <URL> @ <ISO 8601>]` |
| **L4 源不可達** | 全失敗 | L1+L2+L3 都失敗 | `[源不可達:<失敗原因>]`,**不裝懂、不推估** |

## L3 Web fallback 5 個替代源(對位:在台灣可達、無 API key、有限度公開)

| 站名 | 覆蓋 | URL 範本 | 限制 |
|---|---|---|---|
| **TWSE 公開網頁** | TWSE 集中市場報價 + 基本面 | `https://mis.twse.com.tw/stock/fibest.jsp?stock=<4碼>` | 盤中 5 分鐘 refresh;非 TWSE 不適用 |
| **TPEx 公開網頁** | 上櫃市場報價 + 基本面 | `https://www.tpex.org.tw/web/stock/after_trading/index.php?l=zh-tw` | 需從清單頁取 symbol,單檔 URL 不固定 |
| **Goodinfo** | TWSE+TPEx 整合(技術面 + 法人 + 融資融券) | `https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=<4碼>` | 非同步 JavaScript 渲染,純 HTML 難抓 |
| **公司 IR 頁** | 上櫃/興櫃/海外標的官方資料 | 各上市公司投資人專區 | 需逐家搜尋;無統一 URL pattern |
| **公開財經新聞** | 事件驅動資訊(股價異動、合併、現增) | yahoo finance / 經濟日報 / 工商時報 | 點頭條為主,**不可作為報價源** |

## 散戶表達紀律(對位 financial-advisor-coach 散戶對話框架)

| 情境 | 禁止表達 | 推薦表達 |
|---|---|---|
| L1 / L2 命中 | (不用特別標) | 直接說結論 + 數字 |
| L3 Web fallback | 「公開財經資料顯示」(來源已知) | 「依公開財經資料顯示,<TS> 的資料是:<事實><來源戳>` |
| L4 源不可達 | 「API 故障」「資料庫錯誤」「我不會查」 | 「目前這項的公開資料源不在我的服務範圍,您可參考:<替代查詢建議>` |

**禁止的句型**(對位 SOUL §5 紅線):
- ❌ `看起來報價 API 故障了` → 這是 LLM 推測的事實
- ❌ `這支股票目前沒有報價` → 把「我查不到」寫成「股票沒報價」
- ❌ `根據我的知識` → 來源不明 = 不驗證就不寫

## 對位 atlas-mcp 端點覆蓋表

| 端點類別 | L1 是否命中 | L2 是否能 fallback | L3 Web fallback 適用 |
|---|---|---|---|
| `stock_get_quote` | 部分(本地 cache) | ✅ Fugle→TWSE | ✅ Goodinfo / TWSE 公開網頁 |
| `stock_get_fundamentals` | ✅(本地 JSON) | n/a | ✅ 公司 IR + 公開新聞 |
| `stock_get_chips` | ✅(T86 backfill) | n/a | ✅ TPEx 公開頁(僅上櫃有) |
| `stock_get_technical` | ✅(本地計算) | n/a | ❌(網路無歷史 SMA/RSI) |
| `industry_sector_lookup`(TPEx/興櫃) | ❌ | ❌ | ⚠️(需人工標註,不在 5 站範圍) |
| `risk_get_*`(全域) | ✅(本地) | n/a | ❌(整體風險非單股) |
| `macro_get_*` | ✅(5min cache) | n/a | ✅ 公開新聞事件 |

## 驗證方式(2026-08-07 v1.0 L1 結構通過,L3 待實跑)

```
Step 1: 跑 5 個替代源 URL 各 1 次,確認 200 + 內容可解析
        → 寫到 _atlas-endpoint-cards/ 對應 YAML card
Step 2: 寫 ad-hoc Python verify(atlas-failover-policy.py),結構 5 TEST:
        (a) 5 站 URL 200
        (b) 來源標籤生成格式正確(regex 驗證)
        (c) L4 不可達 → 不返回任何「推估」字串
        (d) L1/L2/L3 各級可達性實測
        (e) 生產標籤格式樣本 5 條
Step 3: 跑 _scripts/validate-timestamp-rule.py 驗證本文時間戳合規(對位 §5 鐵律)
Step 4: 確認 wiki _consult-index.md §3 atlas-mcp 端點字典 cross-ref 到本檔
```

## 未消化 / 待補

- [ ] **HERMES_AUDIENCE env 上線前,L4 對 user audience 的 fallback 策略未定**(已落 `_inbox_deferred.md` §ENV-CR-2026-08-07 等 hermes owner)
- [ ] Goodinfo 與公司 IR 頁 scraper 是否要在 atlas-go 端實作,屬 atlas 端任務,**非本檔可修**
- [ ] 5 個替代源首頁 priority 順序,在 fallback chain 真實跑過後才能定(目前按可達性排,非按資料完整度)
- [ ] 海外標的(美股 ADR / 港股)fallback 源未列——等 atlas-skill-inbound 之 Fin-Skills 2026-08-08+ 有相關頁再加
- [ ] TPEx 公開頁的單檔 URL 不固定,需寫爬清單頁 → 解析 symbol → 拿資料的兩階段 fetcher,但 L3 觸發率低(< TWSE 的 10%)先不做

## 相關入口(對位同源原則)

- [[concepts/atlas-mcp-interpretation-guide]] — Rule 3 proxy question + 6 anti-patterns(已含失敗時「明說不可信,不膨風」紀律)
- [[concepts/atals-mcp-tools-reference]] §5 三層訂閱制 + tier 對 audience 路由
- [[concepts/taiwan-stock-market-structure]] §2.2 / §2.3 TPEx / 興櫃市場定義
- [[skills/_manifest_coverage_routing]] §3.1 CR-2 + §2 題 2 兩段制來源標籤規範
- [[skills/_scripts/handle-atlas-failures.py]] — 升級時加 #7「Source Unreachable → Web fallback」分支(走 task-governance)
