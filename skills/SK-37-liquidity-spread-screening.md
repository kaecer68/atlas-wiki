---
title: SK-37 流動性分位與買賣價差篩選
type: skill-inbound
source: Fin-Skills.md §SK-21 未消化缺口（流動性分位 / bid-ask spread）＋ atlas LiquidityScore / Amihud ILLIQ 對位
ingested_at: 2026-09-27
status: active
tier: T3
confidence: medium
atlas_go_relevance: high
mcp_tools_used: [stock_get_quote, stock_get_technical, stock_get_chips, stock_get_volume_divergence, data_get_field_contract, data_get_channels, universe_get_session_detail]
verification: 2026-09-27 L3 實跑 9 端點、全部附 http_code 與 UTC timestamp（§驗證方式）;兩個「已驗證的否定」——無 per-symbol 流動性端點、無真實 bid-ask spread（`SpreadEstimate` 代理存在但 provider 無 caller）;替代路徑（client 端用 quote volume 自算分位）同日實跑 14 檔
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR feat/20260927-sk37-liquidity-and-attribution）
l3_endpoints_probed:
  - "/api/stock/quote?symbol=2330 → 200"
  - "/api/stock/chips?symbol=2330 → 200"
  - "/api/stock/technical?symbol=2330&days=10 → 200"
  - "/api/stock/volume_divergence?symbol=2330&window=30 → 200"
  - "/api/field-contract → 200"
  - "/api/dashboard/data-channels → 200"
  - "/api/parameters → 200"
  - "/api/dashboard/sessions/session-20260927-daily → 200"
numbering_note: 編號 SK-37 曾於 2026-08-22 因品質整頁撤回到 `skills/_archive/2026-08-22-sk37-revert/`（主題 = fin-skill decision index）。本頁主題不同（流動性/價差），非復活該檔內容；舊檔續留 _archive。
related:
  - skills/SK-21-penny-stock-exclusion.md（缺口來源頁；本 PR 同步更正其工具建議）
  - skills/SK-20-size-group-robustness.md（robustness pipeline 前一步）
  - concepts/atlas-risk-management-framework.md（1–3% 價差論述）
---

## 一句話定位

下單前先問「這檔我吃得下嗎」:**看成交金額分位,不要只看股價**。中價但量極低的股票,散戶一張單就會吃掉 1–3% 價差。atlas 目前**不給** per-symbol 流動性分數,只給原料（報價成交量）,分位要 client 端自己算。

## 論文版概念

- **Amihud ILLIQ（非流動性）**:`|報酬| / 成交金額`。atlas 有實作 `CalculateLiquidityScore`（`internal/portfolio/factor_engine_liquidity.go`）。
- **bid-ask spread**:最直接的可交易成本。取不到真實報價時,文獻用 `(High−Low)/Last` 當代理;atlas 的 `calculateSpreadEstimate` 再加 `1/sqrt(Volume/avgVolume)` 修正（`internal/marketdata/microstructure_provider.go`）。
- **流動性分位篩選**:先排除流動性最低 10–20% 的標的,再跑策略。與 SK-21 的「股價門檻」互補——股價會漏掉「中價但量極低」的隱性仙股。

| 論文概念 | 標準做法 | 本頁立場 |
|---|---|---|
| 流動性度量 | 成交金額（週轉額）優先 | 股數與金額**都要算**,排名會分岔 |
| 價差 | 真實 bid/ask | atlas 取不到 ⇒ 只能用代理,且必須標示 |
| 篩選 | 分位門檻 | atlas 內部有定額門檻,但**不對外查詢** |

## atlas 對位

| 用戶問題 | atlas 路徑 | 現況（2026-09-27 實跑） |
|---|---|---|
| 這檔成交量多少? | `stock_get_quote.volume` / `stock_get_technical.volume` | ✅ 2330 回 12989000 / 14557662（股） |
| 這檔籌碼? | `stock_get_chips` | ⚠️ 只回三大法人淨額,**沒有 volume**（SK-21 原本建議的對位工具選錯） |
| 這檔真實買賣價差? | — | ❌ **已驗證的否定**:atlas 無此資料 |
| 這檔流動性分數? | — | ❌ **已驗證的否定**:無 per-symbol 端點 |
| atlas 內部有流動性篩選嗎? | `parameters_get` | ✅ 有定額門檻,但只能讀參數,不能查個股 |

**已驗證的否定 1（無真實價差）**:`internal/marketdata/microstructure_provider.go` 定義 `MicrostructureSnapshot{LiquidityScore, SpreadEstimate, TradeabilityScore}`,但 `NewMicrostructureProvider` 全 repo **只有自身檔案的定義處**、沒有任何 caller（2026-09-27 源碼 grep,排除 `_test`）⇒ 是斷線程式碼,任何端點都拿不到。`/api/field-contract` 確實有欄位名 `spread_estimate`,但**欄位名存在 ≠ 值可得**。

**已驗證的否定 2（無 per-symbol 流動性）**:`/api/field-contract` 有 `liquidity` 系列 10 欄、`/api/parameters` 有 `liquidity` 前綴 20 key（含 `factor_weight.base_weights.liquidity`）,但**沒有任何端點回傳個股流動性分數**。唯一例外是 `universe_get_session_detail` 的 `factor_scores.liquidity`——該 session 96 列**全為 0**,且同層 `momentum`/`value`/`quality`/`agent`/`institutional_sentiment` 亦全 0 ⇒ 該欄位退化,不可用。

**atlas 其實有流動性下限（可讀參數,不可查個股）**:`baseline.min_tradable_volume`=1000000（股）、`smart_universe.min_daily_amount_twd`=5000000（元）、`smart_universe.volume_floor_twd`=10000000（元）、`smart_universe.price_minimum`=10（元）[2026-09-27 實跑 `parameters_get`,共 1669 key]。

**替代路徑（本 PR 實跑 14 檔示範,2026-09-27）**:client 端逐檔 call `stock_get_quote` 取 `volume` 與 `last`,自算 `turnover = volume × last` 再排名。結果**股數分位與金額分位會分岔**:3008 股數分位 7%（最低）但金額分位 64%;1301 股數分位 93%（次高）但金額分位 36%。⇒ 只看「張數」會同時誤判高價股與低價股。

## 散戶解讀

- 問「這檔安全嗎」:先看成交**金額**,不要只看股價。股價 50 元但日成交金額 800 萬的股票,風險遠高於股價 500 元、日成交 80 億的股票。
- 台股 1 張 = 1000 股。`stock_get_quote.volume` 回的是**股數**,除以 1000 才是張數;`stock_get_technical.volume` 同單位。
- 中價股（20–100 元）若日成交量低,散戶單筆就可能吃掉 1–3% 價差——來回一趟就吃掉大半停利空間。
- atlas 的內部下限（`min_tradable_volume`=1000000 股、`min_daily_amount_twd`=5000000 元、`price_minimum`=10 元）是**模擬器自己的**門檻,不代表你的券商或你的單子安全。
- 不要問 atlas「這檔流動性幾分」——目前答不出來（已驗證的否定）。要分位就 client 端自算;要真實價差就必須外部來源並標明。

## 驗證方式

### L3 端點實跑（2026-09-27,本 PR;每列附 http_code 與 UTC timestamp）

| # | 端點（GET） | http_code | UTC timestamp |
|---|---|---|---|
| 1 | `/api/stock/quote?symbol=2330` | 200 | 2026-09-27T08:56:23Z |
| 2 | `/api/stock/chips?symbol=2330` | 200 | 2026-09-27T08:56:24Z |
| 3 | `/api/stock/technical?symbol=2330&days=10` | 200 | 2026-09-27T08:56:24Z |
| 4 | `/api/stock/volume_divergence?symbol=2330&window=30` | 200 | 2026-09-27T08:56:24Z |
| 5 | `/api/field-contract` | 200 | 2026-09-27T08:56:23Z |
| 6 | `/api/dashboard/data-channels` | 200 | 2026-09-27T08:56:23Z |
| 7 | `/api/parameters` | 200 | 2026-09-27T08:56:24Z |
| 8 | `/api/dashboard/sessions/session-20260927-daily` | 200 | 2026-09-27T08:56:46Z |
| 9 | `/api/dashboard/sessions/latest` | **404** | 2026-09-27T08:56:42Z |

- 第 9 列是**路徑陷阱**:工具 `universe_get_session_detail` 的 canary 對照值寫 `/api/dashboard/sessions/latest`,今日 404（`{"error":"session not found"}`）。真實路徑 = `/api/dashboard/sessions/{session_id}`,id 從 `universe_get_sessions` 取。
- 第 1–4 列同日對 14 檔各跑一次（2330/2317/2454/2412/1301/6505/2881/2603/6488/8069/2313/2308/3008/1476）,全部 200。
- 第 5 列回 2262 欄:`liquidity` 10 欄、`spread_estimate` 在、`market_cap` 0 命中。
- 第 6 列回 42 個 channel（含 `tw_vol`、`twse_sbl`、`twse_margin`）。
- 第 7 列回 1669 key。
- 斷線證據（源碼 grep,2026-09-27）:`NewMicrostructureProvider` 命中數 = 1（只有定義處）。

### 可重現步驟

Step 1: `curl -s "http://127.0.0.1:18080/api/stock/quote?symbol=2330"` → 取 `volume` 與 `last`。
Step 2: 對 universe 逐檔重複 Step 1,算 `turnover=volume*last`,排名取分位（本頁用 14 檔示範方法,非全量）。
Step 3: `curl -s http://127.0.0.1:18080/api/parameters` → 篩 `volume_floor|min_tradable_volume|min_daily_amount`,讀 atlas 內部下限。
Step 4: 真實 bid/ask 一律標「atlas 無此資料」,**不得**把 `(High−Low)/Last` 當真實價差對外報數。

## 未消化 / 待補

- [ ] 真實 bid/ask 仍無 atlas 來源;需外部（券商 API / 交易所揭示）並標替代來源。
- [ ] `MicrostructureProvider` 接線後可取代 client 端代理;目前 0 caller,是否接線由 atlas 端決定（追蹤）。
- [ ] 分位門檻（排除最低幾 %）本頁未校準:只給方法,未回測;需與 SK-21 的 P20=19.70 元一起定。
- [ ] 14 檔僅為方法示範,非 universe 全量分位;全量需 client 端逐檔呼叫（成本 = N 次請求）。
