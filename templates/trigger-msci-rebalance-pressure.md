# MSCI 季度再平衡壓力觸發模板(對位 2026 韓股崩盤被動再平衡教訓)

> [2026-08-22 快照:21] templates/*.md 實數 21 檔（本檔「現有 N 模板/第 N 模板」為撰寫當下歷史計數，快照統一，數字不一屬歷史演進）

**觸發條件**:MSCI 季度再平衡(2/5/8/11 月檢討)[2026-08-22 audit-fix]檢討月月底生效日尾盤,MSCI Taiwan 指數權重單季上調 > +2pp 或單季上調至 > 30%,觸發「被動 ETF 必須增持台股」結構買盤訊號(對位再平衡 + 反向警示)

**反向觸發(本模板主場景)**:MSCI Korea / Taiwan 任一權重單季下調 > 1.5pp,觸發「被動 ETF 必須減持」→ **生效日尾盤被動賣壓** = 直接對位 2026/6 韓股崩盤真因;權重上調時被動 ETF 為**增持(買壓)**而非減持 [2026-08-22 audit-fix](本模板雙向)

**對位**:ATLAS_METHODOLOGY.md §二 Layer 1(全球資金配置)+ Layer 4(產業鏈結構)
**對位 strategy**:msci-rebalance-pressure(事件型,對位 2026/6 MSCI 新興市場權重 TSMC + 24.8% 觸發 ETF 增持)
**對位端點**:
- `/api/macro/snapshot/latest` — `msci_taiwan_weight_pct` / `msci_korea_weight_pct` / `msci_rebalance_date` 欄位
- `/api/event/calendar` — MSCI 季度再平衡公告日(2/5/8/11 月)[2026-08-22 audit-fix]
- 需新增 `msci_rebalance_analyzer` 服務計算「權重變動 vs 觸發」(**atlas 端未暴露 = web fallback MSCI 官網**)

**新增日期**:2026-08-09 | **序號**:第 17 模板
**新增原因**:v6.58 研究發現**韓股 2026 崩盤真因之一 = Samsung/SK Hynix 權重下調 → 被動 ETF 被迫減持 → 結構性賣壓**(權重上升時被動 ETF 是增持/買壓,不是減持)[2026-08-22 audit-fix](對位 v6.58 §3.1 「MSCI 季度再平衡」觸發鏈)。MSCI Taiwan 4/30/2026 已達 24.8%(全 EM 最大權重),若再升,觸發條件成熟

---

## 觸發設計(雙向 OR 邏輯,但反向訊號需更高警戒)

| 條件 | 觸發門檻 | 邏輯 |
|------|---------|------|
| **正向**:MSCI Taiwan 權重單季上調 | > +2pp | 被動 ETF 大量增持台股 = 結構性買盤訊號(對位 2026/4 台股權重 24.8% 觸發) |
| **正向**:MSCI Taiwan 權重單季絕對值 | > 30% | 警戒:單一國家權重過高 = 風險集中(對位 v6.58 §6.1 TSMC 集中度) |
| **反向**:MSCI Korea 權重單季下調 | > -1.5pp | **直接對位韓股崩盤** — 被動 ETF 大量減持韓股 = 結構性賣壓訊號 |
| **反向**:MSCI Taiwan 權重單季下調 | > -1.5pp | 警戒:台股被外資主動拋售訊號(極端尾部風險) |

---

## Step 1:信號捕捉(對位 2026-08-09 嘗試)

**實測結果**:
- `mcp__atlas_mcp__system_get_health` → **unreachable 4 次**
- `mcp__atlas_mcp__mcp_quickstart` → **unreachable 4 次**
- `mcp__atlas_mcp__stock_get_quote symbol=2330` → 仍 unreachable
- **atlas-mcp 端至 2026-08-09 仍未恢復,動態驗證全部跳過**

**已知業界資料(2026/8/9)**:
- MSCI Taiwan 2026/4/30 = 24.8%(EM 最大權重,對位 MSCI 官網)
- MSCI Korea 2026/4/30 同步上升至接近 27%(IT 類達 37%)
- MSCI 季度再平衡:2/5/8/11 月檢討,檢討月月底生效;2026/8 檢討 → **8 月底生效**(非 11 月),生效日尾盤為關鍵監測期 [2026-08-22 audit-fix]

---

## Step 2:自動跑端點(觸發後 — atlas 端恢復時跑)

- `mcp__atlas_mcp__macro_get_snapshot_latest` — 取 `msci_*_weight_pct` 欄位(若 atlas 端未暴露,走 MSCI 官網 web fallback)
- `mcp__atlas_mcp__event_calendar` — MSCI 公告日
- `mcp__atlas_mcp__risk_get_metrics` — 對位台股波動率是否同步上升
- `mcp__atlas_mcp__capital_flow_summary` — 外資 ETF 流向驗證

---

## Step 3:建議(私人平台散戶 — exit timing 優先)

**正向觸發(MSCI Taiwan 權重上調)**:
- **這是買盤訊號**,但對位 v6.58 §6.2 **「過度集中 = 風險」**:
  - 散戶持有台股 → 重新評估**是否過度集中**(若 TSMC + 半導體 > 70% 持股 = 警戒)
  - 散戶想加碼 → **勿在權重突破 30% 後追高**(歷史均值約 15-20%,突破上限後容易觸發反向再平衡)
  - 注意:**正向觸發不是「無腦加碼」訊號,是「該分散就分散」訊號**

**反向觸發(MSCI Korea / Taiwan 權重下調)**:
- **這是韓股崩盤真因**:
  - 散戶持有台股半導體 → **立即評估是否減碼 30%**(對位 v6.58 §3.1 韓股 SK Hynix 從 -52% 教訓)
  - 散戶持有韓股 → 觸發即**主動退出**,**不要等崩盤結束**(被動 ETF 賣壓是結構性,不是暫時性)
  - 散戶持有槓桿 ETF → **優先減碼**(對位 v6.58 §1.3 散戶槓桿 ETF 從 -75% 教訓)

**觸發失敗**:觀望(結構性誠實)

**結構性誠實**:
- atlas 端 401/503/timeout = 標 fail 不觸發
- MSCI 公告但權重變動 < 1pp = **未觸發(結構性訊號不足)**
- 雙向觸發同時(台股上 + 韓股下)= **標「結構性輪動訊號,可能是東亞半導體敘事降溫前兆」**

---

## Step 4:落 §6 + Telegram

- 落 `_consult-index.md` §6 第 N+1 筆紀錄
- Telegram 通知 + 摘要權重變動數據
- 結構性誠實標(若只觸發正向未觸發反向 = 「買盤訊號但無賣壓」)

---

## 實作 checklist(給開發 / atlas agent 用)

### A. 修 atlas-mcp-trigger-monitor.py(line 175 後新增 TEMPLATES 條目)

```python
# 第 17 模板(2026-08-09 新增,對位 v6.58 韓股 MSCI 再平衡真因)
"msci-rebalance-pressure": {
    "name": "MSCI 季度再平衡壓力觸發",
    "file": "trigger-msci-rebalance-pressure.md",
    "condition": "MSCI Taiwan 權重單季 > +2pp 或 > 30% 絕對值 / MSCI Korea 下調 > 1.5pp",
    "http_path": "/api/macro/snapshot/latest",
    "field": "msci_taiwan_weight_change",
    "metric": "value",
    "threshold": 2.0,
    "compare": "gt",
    "extra_check": {
        "msci_korea_weight_change": "value<-1.5",  # 反向訊號
    },
    "is_dual_direction": True,  # v0.4 新分支:支援雙向觸發
},
```

### B. 注意

1. **atlas 端 `msci_*` 欄位未必暴露**,需先 `mcp__atlas_mcp__data_get_field_contract` 驗證(對位 v2.0 CLI 假設 pitfall)
2. 若無欄位 → 走 web fallback(MSCI 官網 `https://www.msci.com/our-solutions/indexes/msci-emerging-markets-index`)→ 模板升級為 `is_web_fallback` 模式
3. `is_dual_direction` flag 為 monitor.py v0.4 擴充(目前不存在),需開發 agent 支援

### C. 測試(atlas 端恢復後跑)

- [ ] `curl "/api/macro/snapshot/latest"` 確認含 `msci_taiwan_weight_change` + `msci_korea_weight_change`
- [ ] 結構性誠實測試:注入 MSCI Taiwan +3pp + MSCI Korea -2pp → 正向 + 反向雙觸發
- [ ] 反驗證:只台股 +2pp,韓股 -0.5pp → 只正向觸發(雙向邏輯驗證)

### D. 上線

- 不需動 atlas backend(只在 atlas-wiki/_scripts + templates 加)
- kaecer 拍板啟用後 → 落 `_consult-index.md` §6.4 對位表(從 15 模板升 16)
- 對位 v6.16 CI:`trigger-existence` job 加 msci-rebalance-pressure

---

## 對位 SKILL 與憲章

| 對位項 | 內容 |
|--------|------|
| ATLAS_METHODOLOGY 7 層因果鏈 | Layer 1(全球資金配置)+ Layer 4(產業鏈結構) |
| Q5 宏觀(全球資金配置) | 跨 Q5 + Q3 雙對位 |
| 散戶語言(私人平台/exit timing) | 「權重過高=集中風險,權重下調=賣壓訊號,該賣沒賣的現在評估減碼」 |
| 結構性誠實 | 雙向 OR 但反向需更高警戒;atlas 端失敗 = 標 fail 不觸發 |

---

## 為什麼這模板值得加

- **現有 16 模板全吃 macro/個股/chips/HBM 週期**,**沒涵蓋 MSCI 被動再平衡壓力** = 對位韓股崩盤最關鍵的結構性賣壓源
- **MSCI Taiwan 4/30/2026 = 24.8% 已是 EM 最大權重**(對位 MSCI Markets in Motion),若再升,觸發條件成熟
- **反向觸發 = 直接對位 2026 韓股崩盤真因**(Samsung/SK Hynix 權重下調 → ETF 被迫減持 → 結構性賣壓;權重上調 → 增持買壓)[2026-08-22 audit-fix]

---

## 不該做的事

- ❌ 不要把雙向 OR 改單向(會失韓股崩盤真因預警)
- ❌ 不要用 LLM 推估 MSCI 權重(必須 web fallback 或 atlas 端欄位)
- ❌ 不要把正向觸發寫成「無腦買入」(對位 v6.58 §6.2 集中度風險)
- ❌ 不要跳過開發 agent 改 monitor.py(`is_dual_direction` flag 需正式擴充)
- ❌ 不要在反向觸發時自動執行減碼(本模板是通知,不是自動交易)