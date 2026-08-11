# 對沖基金集中持倉爆倉連鎖觸發模板(對位 2021 Archegos 教訓)

**觸發條件**:任一個股(尤其 ADR/中概股/半導體鏈)在 1 個交易日內下跌 > 20%,且跨市場 ADR/H 股同步下跌 > 15%,觸發「對沖基金集中持倉爆倉 + prime broker 連鎖拋售」訊號(對位 2021/3 Archegos 案例)

**對位**:ATLAS_METHODOLOGY.md §二 Layer 5(事件觸發)+ Layer 4(產業鏈結構)
**對位 strategy**:hedge-fund-unwind(事件型,對位 2021/3/26 Archegos 爆倉導致 ViacomCBS/Discovery 1 日跌 27%)
**對位端點**:
- `/api/stock/quote` — 個股 1 日跌幅(對位 monitor.py `is_custom_calc` 模式)
- `/api/stock/chips` — 法人 / 主力流向(對位爆倉會造成異常賣超)
- `/api/macro/snapshot/latest` — 個股 ADR 報價(若 atlas 端有暴露)
- web fallback:Bloomberg / Reuters 即時新聞(爆倉通常伴隨媒體報導)

**新增日期**:2026-08-09 | **序號**:第 19 模板
**新增原因**:v6.58 §5.3 識別出 2021 Archegos 案例**為國際資本透過衍生品隱藏集中持倉的真實示範**,**台灣曾因 ADR 被波及**(TSMC ADR / MediaTek)。**現有 16 模板全沒涵蓋此訊號** = 跨市場連鎖風險預警源完全失明

---

## 觸發設計(個股層 + 跨市場雙確認)

| 條件 | 觸發門檻 | 邏輯 |
|------|---------|------|
| **個股層**:個股 1 日跌幅 | < -20% | 異常跌幅,需懷疑集中持倉爆倉(對位 ViacomCBS 2021/3/26 -27%) |
| **跨市場層**:ADR / H 股同步跌幅 | < -15% | 跨市場聯動確認(對位 Archegos 同時持有 ViacomCBS + Discovery) |
| **結構性**:法人 / 主力異常賣超 | 1 日 > 5 日均量 3x | prime broker 連鎖拋售訊號 |

---

## Step 1:信號捕捉(對位 2026-08-09 嘗試)

**實測結果**:
- atlas-mcp 仍 unreachable,動態驗證全部跳過
- **無真實個股數據,觸發邏輯需等 atlas 端恢復後跑**

**已知 2021 Archegos 真實數據**(供模板設計驗證用):
- ViacomCBS 2021/3/22 開始跌,3/26 -27%
- Discovery 同時跌 27%
- 5 日內 prime broker(Credit Suisse / Nomura / Goldman / Morgan Stanley)拋售 $30B+
- **台股未直接受波及,但 TSMC ADR 1 日內曾跌 4-5%**

---

## Step 2:自動跑端點(觸發後)

- `mcp__atlas_mcp__stock_get_quote(symbol=*)` — 多個股跌幅
- `mcp__atlas_mcp__stock_get_chips(symbol=*)` — 法人 / 主力流向
- `mcp__atlas_mcp__stock_get_technical(symbol=*)` — RSI / 成交量比對 5 日均量
- `mcp__atlas_mcp__risk_get_correlation_matrix` — 跨市場相關性(ADR ↔ 本地股)

---

## Step 3:建議(私人平台散戶 — exit timing 優先)

**觸發成功**:
- **這是結構性跨市場爆倉訊號**:
  - 散戶持有同產業個股 → **立即重新評估**,尤其是槓桿型或高估值個股(對位 v6.58 §1.3 槓桿 ETF -75~80% 教訓)
  - 散戶持有相關 ADR → **主動評估是否減碼**(不要等爆倉結束才動作)
  - **不該做**:恐慌殺低(等第二天開盤再判斷) / 借錢加碼(槓桿是爆倉主因)
- **保留觀察**:爆倉通常 1-3 日內結束,結構性壓力會逐步釋放

**觸發失敗**:觀望(結構性誠實)

**結構性誠實**:
- 只有個股跌但 ADR 同步性弱 = **未觸發(非跨市場爆倉)**,標「個股事件,非集中持倉爆倉」
- atlas 端 401/503 = 標 fail 不觸發
- 個股跌但成交量未爆量 = **未觸發**(可能只是單日波動)

---

## Step 4:落 §6 + Telegram

- 落 `_consult-index.md` §6 第 N+3 筆紀錄
- Telegram 通知 + 摘要個股 + ADR 跌幅
- 結構性誠實標(若個股跌但 ADR 同步性弱 = 「個股事件,非集中持倉」)

---

## 實作 checklist(給開發 / atlas agent 用)

### A. 修 atlas-mcp-trigger-monitor.py(line 175 後新增 TEMPLATES 條目)

```python
# 第 19 模板(2026-08-09 新增,對位 2021 Archegos 教訓)
"hedge-fund-unwind": {
    "name": "對沖基金爆倉連鎖觸發",
    "file": "trigger-hedge-fund-unwind.md",
    "condition": "個股 1 日跌幅 > -20% + 跨市場 ADR 同步 > -15% + 成交量 > 5 日均量 3x",
    "http_path": "/api/stock/quote",
    "symbols": ["*"],  # 萬用監測所有個股(成本高,需 watchlist 過濾)
    "metric": "intraday_change_pct",
    "threshold": -20.0,
    "compare": "lt",
    "is_custom_calc": True,
    "extra_check": {
        "adr_change_pct": "value<-15",  # ADR 同步
        "volume_vs_avg": "value>3",  # 成交量比
    },
    "is_archegos_pattern": True,  # v0.4 新分支:Archegos 型爆倉偵測
},
```

### B. 注意

1. `is_archegos_pattern` 為 monitor.py v0.4 擴充,需開發 agent 支援
2. **萬用監測所有個股成本高**,需配合 watchlist(對位 v6.33 PR #1443 trade 模板)
3. ADR 報價 atlas 端未必暴露,走 web fallback(Bloomberg / Reuters)

### C. 測試(atlas 端恢復後跑)

- [ ] `curl "/api/stock/quote?symbol=2330"` 確認含 intraday_change_pct 計算欄位
- [ ] 結構性誠實測試:注入某個股 -25% + ADR -18% + 成交量 4x → 觸發
- [ ] 反驗證:個股 -22% 但 ADR 同步 -5% = 未觸發(跨市場性不足)

### D. 上線

- 不需動 atlas backend(只在 atlas-wiki/_scripts + templates 加)
- kaecer 拍板啟用後 → 落 `_consult-index.md` §6.4 對位表

---

## 對位 SKILL 與憲章

| 對位項 | 內容 |
|--------|------|
| ATLAS_METHODOLOGY 7 層因果鏈 | Layer 4(產業鏈)+ Layer 5(事件觸發)正交 |
| Q1 個股 + Q5 宏觀 | 跨 Q1 + Q5 雙對位 |
| 散戶語言(私人平台/exit timing) | 「跨市場個股爆量跌 = 對沖基金爆倉訊號,同產業個股立即評估減碼」 |
| 結構性誠實 | 個股 + ADR + 成交量 三項確認;個股單跌 = 未觸發;atlas 失敗 = 標 fail |

---

## 為什麼這模板值得加

- **現有 16 模板全吃 macro/個股/chips/HBM/MSCI/capex**,**沒涵蓋跨市場對沖基金爆倉連鎖** = v6.58 §5.3 真實案例教訓訊號源失明
- **台股 TSMC ADR / 半導體鏈曾因 Archegos 受波及**,預警機制 = 結構性風險管控
- **2021 Archegos 案例**為國際資本透過衍生品隱藏集中持倉的真實示範,需主動監測

---

## 不該做的事

- ❌ 不要單一個股跌就觸發(會假警報過多)
- ❌ 不要萬用監測所有個股(成本過高)
- ❌ 不要把此模板寫成「恐慌賣出」(爆倉通常 1-3 日結束)
- ❌ 不要跳過開發 agent 改 monitor.py(`is_archegos_pattern` flag 需正式擴充)
- ❌ 不要忽略 web fallback 訊號(Bloomberg/Reuters 報導通常 1 小時內出來)