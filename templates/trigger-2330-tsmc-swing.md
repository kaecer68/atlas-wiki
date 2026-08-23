# 2330 台積電報價觸發模板(單日版)

> [2026-08-22 快照:21] templates/*.md 實數 21 檔（本檔「現有 N 模板/第 N 模板」為撰寫當下歷史計數，快照統一，數字不一屬歷史演進）

**觸發條件(單日)**:2330 台積電盤中漲跌幅 > +3.0% 或 < -3.0%(單日劇烈波動)
**對位**:ATLAS_METHODOLOGY.md §二 Layer 3(半導體 leader 急動)
**對位 strategy**:tsmc-price-shock-trigger(事件型,無固定 L1-L5)
**對位端點**:`/api/stock/quote?symbol=2330`(對位 `mcp__atlas_mcp__stock_get_quote`)
**新增日期**:2026-08-03
**新增原因**:PR #1445 修復 stock_get_quote + parameters_get 雙失敗後,`/api/stock/quote` 從 503 → 200(已實測驗收),開啟個股報價觸發模板的可能性

---

## Step 1:信號捕捉(對位真實 2026-08-03)

- **2330 last=2370**(對位當下)
- **計算當日漲跌幅** = `(last - 昨收) / 昨收 * 100`
  - 需要「昨收」資料(quote 不含,需從 `stock_get_technical` 或 `backtest_signals` 拿)
  - 或用 quote 內 `last vs open` 計算盤中振幅:`(high - low) / open * 100`(替代方案)

### 觸發邏輯(pseudocode)

```python
quote = atlas_get("/api/stock/quote?symbol=2330")
last = quote["last"]
open_ = quote["open"]
high = quote["high"]
low = quote["low"]

# 兩個觸發條件二選一
intraday_swing = (high - low) / open_ * 100
if intraday_swing > 3.0:
    triggered = True  # 盤中振幅 > 3%
# 或:
change_pct_estimate = (last - open_) / open_ * 100  # 簡化版,不取昨收
if abs(change_pct_estimate) > 3.0:
    triggered = True
```

## Step 2:自動跑端點(觸發後)

- `mcp__atlas_mcp__stock_get_fundamentals(symbol="2330")`(PE/PB/股利率)
- `mcp__atlas_mcp__industry_sector_lookup(symbol="2330")`(半導體同業 12 支)
- `mcp__atlas_mcp__capital_flow_summary`(半導體 80% inflow 確認)
- `mcp__atlas_mcp__risk_get_correlation_matrix`(半導體 ↔ 散熱 0.96)
- `mcp__atlas_mcp__macro_get_snapshot_latest`(TSMC 月營收 YoY + NVDA/T SM ADR)

## Step 3:建議

- 觸發成功(2330 急漲 +3%):
  - 確認 AI 鏈動能(NVDA +2% 觸發模板 #1 是否同步)
  - 半導體同業全篩(看是否同漲)
  - **加碼半導體 5%**(對位 Q3 產業輪動)
- 觸發成功(2330 急跌 -3%):
  - 確認宏觀(USD_TWD 32+,VIX 30+,SOX 跌)
  - **減碼半導體 10%**(風險控管)
- 觸發失敗:觀望

## Step 4:落 §6 + Telegram

- 落 `_consult-index.md` §6 第 N 筆對話紀錄(觸發成功)
- Telegram 通知 + 摘要 5 端點實跑結果
- 結構性誠實標(若 2330 觸發失敗但 NVDA 觸發,標「2330 未同步 = 半導體個股訊號分歧」)

---

## 實作 checklist(給開發 / atlas agent 用)

### A. 修 atlas-mcp-trigger-monitor.py(line 30-144 新增 1 條 TEMPLATES 條目)

```python
"2330-tsmc-swing": {
    "name": "2330 台積電急漲/急跌觸發",
    "file": "trigger-2330-tsmc-swing.md",
    "condition": "2330 盤中振幅 > 3% 或 (last-open)/open > +3%",
    "http_path": "/api/stock/quote",
    "field": "2330",  # symbol 不是 field,需自訂解析
    "metric": "intraday_swing_pct",  # 計算欄位
    "threshold": 3.0,
    "compare": "gt",
    "extra_check": None,
    "is_custom_calc": True,  # 標記為自訂計算欄位
},
```

註:**當前 trigger-monitor.py 的 field 邏輯是「data[field][metric]」**,不支援 symbol-based 報價。需小改 `run_triggers()` 函式,加 `is_custom_calc` 分支處理。

### B. 修 run_triggers()(line 222-261)

當 `is_custom_calc=True` 時:
- 對 `/api/stock/quote` 端點,query string 加 `?symbol={field}`
- 從回傳 JSON 取 `high/low/open/last` 計算振幅 / change_pct

### C. 測試

- [ ] 本地手動觸發:`curl "http://127.0.0.1:18080/api/stock/quote?symbol=2330"` 確認回 200(對位 PR #1445 驗收)
- [ ] trigger-monitor.py 加 2330 模板後跑:`python3 atlas-mcp-trigger-monitor.py` 確認不破壞現有 12 模板
- [ ] 結構性誠實測試:手動把 2330 報價模擬成 +3.5% → 觸發成功

### D. 上線

- 不需動 atlas backend(只在 atlas-wiki/_scripts 加模板,atlas-mcp-trigger-monitor.py 改)
- kaecer 拍板啟用後 → 落 `_consult-index.md` §6.4 對位表(從 12 模板升 13 模板)
- 不需動 PR #1445 / PR #1445 已合 main,直接吃新功能

---

## 對位 SKILL 與憲章

| 對位項 | 內容 |
|--------|------|
| ATLAS_METHODOLOGY 7 層因果鏈 | Layer 3(半導體 leader 急動)+ Layer 5(事件觸發)正交 |
| Q1 個股 + Q3 產業 | 跨 Q1(個股訊號)+ Q3(產業輪動)雙對位 |
| 散戶語言 | 「2330 急漲/急跌 = 半導體訊號,確認要不要加碼」 |
| 結構性誠實 | 觸發失敗時標明,不用 fallback 假資料 |

---

## 為什麼這模板值得加(對位散戶價值)

- **現有 12 模板全吃 macro 層**(NVDA/USD_TWD/DXY/融資/外資/SOX/台海/中國需求/關稅/ETF/央行/散戶融資)
- **沒有任何模板打個股層** = 2330 急漲/急跌時,現有訊號沒人通知
- 2330 = 台股權值 30% + 半導體 leader + AI 鏈火車頭 = **個股最 critical 訊號源**
- 觸發 → 即時通知 → 散戶可決定是否加碼/減碼半導體 = 直接對位 mission「找漏洞」

---

## 不該做的事

- ❌ 不要把模板改成「每分鐘報 2330」(會被當報價 API,失去觸發語意)
- ❌ 不要加太多個股(2330 + 2454 + 2303 為主,加太多變 wash sale / 噪音)
- ❌ 不要繞過 atlas backend 改 quote 邏輯(PR #1445 已修,直接用)
- ❌ 不要用「quote.high vs open 漲幅」假裝昨收變化(昨收是真實資料,不是 quote 內的字段)
- ❌ 不要把模板寫成「Q1 個股通用」(單一 symbol,單一閾值,簡單可維護)