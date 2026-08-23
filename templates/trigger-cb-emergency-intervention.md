# 央行緊急干預匯市觸發模板(對位 1997 IMF + 2022 BOK 干預教訓)

> [2026-08-22 快照:21] templates/*.md 實數 21 檔（本檔「現有 N 模板/第 N 模板」為撰寫當下歷史計數，快照統一，數字不一屬歷史演進）

**觸發條件**:任一亞洲主要央行(BOK 台灣央行 / BOK 韓國央行 / PBOC 中國人行 / BOJ 日本央行)單日匯市操作 > 50 億美元,或央行公開聲明「採取措施穩定匯市」,觸發「央行緊急干預」結構訊號

**反向觸發**:亞洲匯市波動率回落至月內均值 - 1σ,觸發「干預結束 / 市場回穩」訊號

**對位**:ATLAS_METHODOLOGY.md §二 Layer 1(全球資金配置)+ Layer 7(政策風險)
**對位 strategy**:cb-emergency-intervention(事件型,對位 1997 IMF 韓國 584 億美元紓困 + 2022 BOK 韓元干預)
**對位端點**:
- `/api/macro/snapshot/latest` — `cb_fx_intervention_amount` / `cb_intervention_date` 欄位
- `/api/event/calendar` — 央行公開聲明日
- web fallback:央行官網新聞稿 / Reuters / Bloomberg

**新增日期**:2026-08-09 | **序號**:第 20 模板
**新增原因**:v6.58 §5.1 1997 IMF 案例 + §6.1 「央行獨立性」都是關鍵結構性因素。**現有 11 模板(trigger-cb-fx-intervention)**只涵蓋台灣央行接近防線 32.5 的「預警」,**未涵蓋實際干預發生後的「結構訊號」**。**這兩個模板必須並行**(預警 vs 實際)

---

## 觸發設計(正向觸發 + 反向觀察)

| 條件 | 觸發門檻 | 邏輯 |
|------|---------|------|
| **正向**:任一亞洲央行單日匯市操作 | > 50 億 USD | 央行緊急干預訊號(對位 1997 IMF 韓國 584 億美元) |
| **正向**:央行公開聲明「採取措施穩定匯市」 | 出現關鍵字 | 政策風險升級 |
| **反向**:亞洲匯市波動率回落 | 月內均值 - 1σ | 干預結束訊號 |

---

## Step 1:信號捕捉(對位 2026-08-09 嘗試)

**實測結果**:
- atlas-mcp 仍 unreachable,動態驗證全部跳過

**已知央行干預案例(供設計驗證)**:
- 2022/9-10 BOK 韓元干預:累計約 400 億美元(2026 BOK 7/28 累計)
- 1997/12 IMF 對韓國 584 億美元紓困(歷史最大單一國家)
- 2026/8 月初 TWD/USD 接近央行防線 32.5(已有 trigger-cb-fx-intervention 模板覆蓋)
- **2026/8 月初若 BOK/CBC 真正出手干預**,本模板應觸發

---

## Step 2:自動跑端點(觸發後)

- `mcp__atlas_mcp__macro_get_snapshot_latest` — 取 `cb_fx_intervention_amount` / `cb_intervention_date`
- `mcp__atlas_mcp__event_calendar` — 央行聲明日
- `mcp__atlas_mcp__risk_get_metrics` — 匯率波動率(VXO / VXY)
- web fallback:央行官網新聞稿

---

## Step 3:建議(私人平台散戶 — exit timing 優先)

**觸發成功(央行干預)**:
- **這是結構性恐慌訊號**:
  - 散戶持有新興市場資產 → **重新評估整體配置**(央行干預 = 市場失序)
  - 散戶持有單一新興市場(如台股)→ 央行干預不一定直接影響台股,**但區域風險升級**
  - 該賣沒賣的散戶 → **若觸發且自己持股高度集中**,主動減碼 20-30%
- **不該做**:看到干預就恐慌殺低(干預是「穩定」訊號,不是「崩盤」訊號)

**反向觸發(干預結束)**:
- 市場回穩,觀望
- 但**不代表結構性風險消失**,需配合其他觸發模板判斷

**觸發失敗**:觀望

**結構性誠實**:
- 央行聲明但無實際操作 = **未觸發(口頭干預,非實際干預)**
- 央行操作 < 20 億 USD = **未觸發(規模不足)**
- atlas 端 401/503 = 標 fail 不觸發

---

## Step 4:落 §6 + Telegram

- 落 `_consult-index.md` §6 第 N+4 筆紀錄
- Telegram 通知 + 摘要央行操作金額
- 結構性誠實標(若口頭干預但無實際操作 = 「口頭穩定訊號」)

---

## 實作 checklist(給開發 / atlas agent 用)

### A. 修 atlas-mcp-trigger-monitor.py(line 175 後新增 TEMPLATES 條目)

```python
# 第 20 模板(2026-08-09 新增,對位 1997 IMF + 2022 BOK 干預教訓)
"cb-emergency-intervention": {
    "name": "央行緊急干預匯市觸發",
    "file": "trigger-cb-emergency-intervention.md",
    "condition": "任一亞洲央行(BOK/CBC/PBOC/BOJ)單日匯市操作 > 50 億 USD",
    "http_path": "/api/macro/snapshot/latest",
    "field": "cb_fx_intervention_amount_max",  # 取四家央行最大操作金額
    "metric": "value",
    "threshold": 50.0,
    "compare": "gt",
    "extra_check": {
        "cb_official_statement": "value contains '採取措施' or 'stabilize'",
    },
    "tracked_symbols": ["BOK", "CBC", "PBOC", "BOJ"],
    "is_cb_intervention": True,  # v0.4 新分支:央行干預偵測
},
```

### B. 注意

1. **atlas 端 `cb_fx_intervention_amount` 欄位未必暴露**,需先 `data_get_field_contract` 驗證
2. 若無欄位 → 走 web fallback(央行官網 + Reuters)→ 模板升級為 `is_web_fallback` 模式
3. 央行操作有「官方版 + 估算版」差異,需 5 個工作日後才能確認實際規模
4. **與 trigger-cb-fx-intervention 並行**:本模板覆蓋「實際干預」,原模板覆蓋「接近防線預警」

### C. 測試(atlas 端恢復後跑)

- [ ] `curl "/api/macro/snapshot/latest"` 確認含 `cb_fx_intervention_amount` 欄位
- [ ] 結構性誠實測試:注入 BOK 60 億 USD 干預 → 觸發
- [ ] 反驗證:BOK 聲明但無操作 = 未觸發(口頭干預)

### D. 上線

- 不需動 atlas backend(只在 atlas-wiki/_scripts + templates 加)
- kaecer 拍板啟用後 → 落 `_consult-index.md` §6.4 對位表(從 16 升 17)

---

## 對位 SKILL 與憲章

| 對位項 | 內容 |
|--------|------|
| ATLAS_METHODOLOGY 7 層因果鏈 | Layer 1(全球資金)+ Layer 7(政策風險)正交 |
| Q5 宏觀 + Q6 政策 | 跨 Q5 + Q6 雙對位 |
| 散戶語言(私人平台/exit timing) | 「央行真的出手干預 = 結構性恐慌訊號,持有高度集中者主動評估減碼」 |
| 結構性誠實 | 操作 > 50 億才觸發;口頭干預 = 未觸發;atlas 失敗 = 標 fail |

---

## 為什麼這模板值得加

- **現有 11 模板(trigger-cb-fx-intervention)只涵蓋「接近防線預警」**,**未涵蓋「實際干預發生」**
- **1997 IMF 584 億美元干預是史上最大新興市場央行操作**,觸發即結構性恐慌
- **2026/8 月初新台幣貶值 + 韓元貶值 = 央行干預風險升級**

---

## 不該做的事

- ❌ 不要看到央行聲明就觸發(口頭干預 ≠ 實際干預)
- ❌ 不要小於 50 億 USD 就觸發(日常操作)
- ❌ 不要把央行干預寫成「恐慌賣出」(干預是穩定訊號)
- ❌ 不要跳過開發 agent 改 monitor.py(`is_cb_intervention` flag 需正式擴充)
- ❌ 不要忽略「干預後 1 個月」的市場反應(歷史顯示干預後通常有 1-3 月反彈期)