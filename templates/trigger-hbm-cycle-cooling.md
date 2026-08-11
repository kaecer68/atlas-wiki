# HBM/AI 半導體敘事降溫觸發模板(對位 2026 韓股崩盤教訓)

**觸發條件(三項 AND)**:SK Hynix(000660)月跌幅 < -10% + HBM 報價連 2 月跌 < -5% + 雲端商(NVDA/GOOGL/META/MSFT)任一 capex 季報 YoY 指引下修至 < +20%
**對位**:ATLAS_METHODOLOGY.md §二 Layer 4(產業鏈)+ Layer 5(事件觸發)
**對位端點**:`/api/stock/chips?symbol=660`(SK Hynix chips)+ `/api/macro/snapshot/latest`(HBM 報價 + capex)
**新增日期**:2026-08-09 | **序號**:第 16 模板(對位 v6.21 monitor.py 第 13/14/15 之後)
**新增原因**:v6.58 研究發現**現有 14 模板全沒覆蓋 HBM 半導體週期訊號**;韓股崩盤主因之一就是 SK Hynix 從 6 月峰值跌 -52%,台股 TSMC 與其連動 0.95 = 結構性風險預警源

---

## 觸發設計(三項 AND 非 OR)

| 條件 | 門檻 | 來源 | 為何 AND |
|------|------|------|---------|
| SK Hynix 月跌幅 | < -10% | `/api/stock/chips?symbol=660` 取 `month_change_pct` | HBM 報價跌但 capex 仍強 = 短週期調整;capex 下修但 HBM 穩 = 公司策略;**三者同步 = 結構性 AI 敘事逆轉** |
| HBM 報價連 2 月跌 | < -5% | DRAMeXchange / TrendForce | 同上 |
| 雲端商 capex 指引下修 | 任一 YoY < +20% | 公司 IR / 10-Q SEC filing | 同上 |

---

## Step 1:信號捕捉(對位 2026-08-09 嘗試)

**實測結果**:`mcp__atlas_mcp__stock_get_quote symbol=660` → **MCP server unreachable 3 次**(對位 v6.45 atlas 端已知限制)。**本 session 無法跑真實觸發驗證,動態驗證待 atlas 端恢復後跑。**

**已知業界資料(2026/8/9)**:
- SK Hynix 自 6/22 高點跌 -52%(Emerald Book 2026-08-04,本研究 v6.58 §1.1)
- HBM3 12Hi 報價 2026/Q3 估約 $200(對位結構性 AI capex 降溫市場共識,待驗證)
- NVDA/GOOGL/META 2026/Q2 capex 仍強,**Q4 指引待觀察**

---

## Step 2:自動跑端點(觸發後)

- `mcp__atlas_mcp__stock_get_chips(symbol="660")` — SK Hynix 法人 chips
- `mcp__atlas_mcp__stock_get_quote(symbol="660")` — SK Hynix 報價
- `mcp__atlas_mcp__risk_get_correlation_matrix` — 半導體 ↔ 記憶體(對位 TSMC vs SK Hynix 0.95)
- `mcp__atlas_mcp__macro_get_snapshot_latest` — 取 `hbm_price_change_2m` + `cloud_capex_yoy`(若 atlas 端未暴露欄位,走 web fallback DRAMeXchange + 公司 IR)

---

## Step 3:建議(私人平台散戶 — exit timing 優先)

**觸發成功**:
- **立即動作**:持有半導體(2330/2454/2303/3711) → 重新評估減碼 30-50%;槓桿型 ETF(00690/006201 等) → 重新評估槓桿倍率;**該賣沒賣的散戶 — 此訊號是最後一根稻草,不是恐慌訊號**(對位你拍板的散戶痛點)
- **保留觀察**:NVDA/AMD 仍強 + TSMC 月營收仍強 = 半導體基本面未逆轉,**僅敘事降溫,非全面撤退**
- **不該做**:恐慌殺低(等第二天開盤)/ 砍光半導體(基本面回溫會反彈)/ 借錢加碼(槓桿是韓股崩盤主因)

**觸發失敗**:觀望 = 未觸發就是沒訊號(結構性誠實)

**結構性誠實**:
- 只有 SK Hynix 跌但 TSMC + NVDA 穩 = 韓股個股訊號,**未與台股同步**,標「**未觸發(僅韓股訊號)**」
- atlas 端 401/503/timeout = **標 fail 不觸發**

---

## Step 4:落 §6 + Telegram

- 落 `_consult-index.md` §6 第 N 筆對話紀錄(觸發成功 + 觸發失敗都記)
- Telegram 摘要 5 端點實跑結果
- 結構性誠實標(若 SK Hynix 觸發但 TSMC 未同步 = 訊號僅韓股,降溫未擴散)

---

## 實作 checklist(給開發 / atlas agent 用)

### A. 修 atlas-mcp-trigger-monitor.py(line 175 後新增 TEMPLATES 條目)

```python
# 第 16 模板(2026-08-09 新增,對位 v6.58 研究 + 韓股崩盤教訓)
"hbm-cycle-cooling": {
    "name": "HBM/AI 半導體敘事降溫觸發",
    "file": "trigger-hbm-cycle-cooling.md",
    "condition": "SK Hynix 月跌幅 < -10% + HBM 報價 連 2 月跌 > 5% + 雲端商 capex 季報下修",
    "http_path": "/api/stock/chips",
    "symbols": ["660"],
    "metric": "month_change_pct",
    "threshold": -10.0,
    "compare": "lt",
    "aggregate_mode": "sum",
    "is_chips_aggregate": True,
    "extra_check": {
        "hbm_price_change_2m": "value<-5",
        "cloud_capex_guidance": "value<20",
    },
},
```

### B. 注意

1. `is_chips_aggregate` 模式目前只支援 sum aggregate,不支援 AND 多條件 — 需 monitor.py 擴增 `extra_check` 邏輯(對位 v6.46)
2. HBM 報價與雲端商 capex **atlas 端未必有對位欄位**,需先 `mcp__atlas_mcp__data_get_field_contract` 驗證(對位 v2.0 CLI 假設 pitfall)
3. 若 atlas 端無欄位 → 走 web fallback → 模板升級為 is_web_fallback 模式

### C. 測試(待 atlas 端恢復後跑)

- [ ] `curl "/api/stock/chips?symbol=660"` 確認回 200 + 含 month_change_pct
- [ ] `curl "/api/macro/snapshot/latest"` 確認含 `hbm_price_change_2m` + `cloud_capex_guidance`
- [ ] trigger-monitor.py 加新模板後跑:確認不破壞現有 14 模板
- [ ] 結構性誠實測試:注入 SK Hynix 月跌 -15% + HBM 跌 -7% + capex 下修 → 觸發
- [ ] 反驗證:只 SK Hynix 跌,其他 2 條件不達 → **未觸發**(AND 邏輯驗證)

### D. 上線

- 不需動 atlas backend(只在 atlas-wiki/_scripts + templates 加)
- kaecer 拍板啟用後 → 落 `_consult-index.md` §6.4 對位表(從 14 模板升 15)
- 對位 v6.16 CI:`trigger-existence` job 加 hbm-cycle-cooling + `endpoint-validation` 加 `/api/stock/chips?symbol=660`

---

## 對位 SKILL 與憲章

| 對位項 | 內容 |
|--------|------|
| ATLAS_METHODOLOGY 7 層因果鏈 | Layer 4(產業鏈)+ Layer 5(事件觸發)正交 |
| Q3 產業(半導體集中度) | 跨 Q3:半導體訊號反轉直接影響 2330/2454 |
| 散戶語言(私人平台/exit timing) | 「AI 敘事降溫 = 半導體個股訊號反轉,該賣沒賣的現在評估減碼」 |
| 結構性誠實 | 三項 AND 才觸發;單項達標 = 未觸發;atlas 端失敗 = 標 fail 不觸發 |

---

## 為什麼這模板值得加

- **現有 14 模板全吃 macro 層 + 個股報價 + chips aggregate**,**沒涵蓋 HBM 半導體週期 + AI capex 結構性逆轉** = 對位韓股崩盤核心觸發鏈(SK Hynix 跌 -52%)
- **台股 vs 韓股 = 同型結構(TSMC vs SK Hynix = 半導體雙 leader)**,連動 0.95
- 觸發 → 即時通知 → 散戶(私人平台)可決定是否減碼 = 對位 mission「找漏洞」+「exit timing 痛點」

---

## 不該做的事

- ❌ 不要把 AND 改 OR(假警報過多失信任)
- ❌ 不要只監測 SK Hynix 不監測 TSMC/NVDA(個股 ≠ 結構)
- ❌ 不要繞過 atlas backend 改 quote(對位 SK-22 v3.3 PR #1443 已合)
- ❌ 不要把 HBM 報價寫成「猜的」(沒 DRAMeXchange 就標 fail)
- ❌ 不要用 web fallback 數據假裝 atlas 端有(誠實標 web_fallback)
- ❌ 不要在觸發時自動執行減碼(本模板是**通知 + 散戶自行判斷**,不是自動交易)