# AI capex 指引下修觸發模板(對位 2026 韓股 HBM 預期降溫真因)

> [2026-08-22 快照:21] templates/*.md 實數 21 檔（本檔「現有 N 模板/第 N 模板」為撰寫當下歷史計數，快照統一，數字不一屬歷史演進）

**觸發條件**:任一雲端商(NVDA/GOOGL/META/MSFT)capex 季報 YoY 指引從當季 > 30% 下修至下一季 < 20%,觸發「AI 基礎設施支出敘事降溫」結構訊號

**反向觸發**:四家雲端商 capex 季報 YoY **同步上調 > 50%** = AI 敘事強化 = 半導體買盤訊號

**對位**:ATLAS_METHODOLOGY.md §二 Layer 1(全球資金配置)+ Layer 4(產業鏈)
**對位 strategy**:ai-capex-guidance-cut(事件型,對位 2026/7 HBM 預期降溫 → SK Hynix -52% 教訓)
**對位端點**:
- `/api/macro/snapshot/latest` — `nvda_capex_guidance_yoy` / `googl_capex_guidance_yoy` / `meta_capex_guidance_yoy` / `msft_capex_guidance_yoy` 欄位
- web fallback:公司 IR / SEC 10-Q filing(每季 45 天內公告)
- 需新增 `capex_change_tracker` 服務計算「季報 vs 指引變動」(**atlas 端未必暴露 = web fallback**)

**新增日期**:2026-08-09 | **序號**:第 18 模板
**新增原因**:v6.58 研究 §3.1 觸發鏈明文列「HBM 預期降溫 → 兩大權重股估值重估」是韓股 2026 崩盤核心觸發之一。**沒有任何模板監測雲端商 capex 指引變動** = 觸發鏈上游訊號源完全失明

---

## 觸發設計(雙向 OR,但反向訊號較低警戒)

| 條件 | 觸發門檻 | 邏輯 |
|------|---------|------|
| **觸發向**:任一雲端商 capex 季報 YoY 指引下修至 < 20% | 從 > 30% → < 20% | AI capex 降溫訊號,觸發半導體估值重估(對位 2026/7 HBM 預期降溫) |
| **反向**:四家雲端商 capex 季報 YoY 同步 > 50% | 四家同步 > 50% | AI capex 強化,半導體買盤訊號(但**不等於無腦加碼**,需配合 TSMC 月營收) |

---

## Step 1:信號捕捉(對位 2026-08-09 嘗試)

**實測結果**:
- `mcp__atlas_mcp__system_get_health` → **unreachable 4 次**
- atlas 端 `capex_*` 欄位 **未驗證是否存在**(需等 atlas 端恢復後跑 `data_get_field_contract`)
- **動態驗證全部跳過**

**已知業界資料(2026/8/9)**:
- NVDA 2026/Q2(公布於 2026/5/28):資料中心 revenue YoY +154%,capex 指引未變
- Microsoft / Google / Meta 2026/Q2 capex 指引持續強勁(YoY +60~+80%)
- **Q4 2026 指引(2026/10~11 公布)= 真正的降溫觸發窗口**,需密切監測

---

## Step 2:自動跑端點(觸發後)

- `mcp__atlas_mcp__macro_get_snapshot_latest` — 取 `*_capex_guidance_yoy` 欄位
- `mcp__atlas_mcp__event_calendar` — 雲端商財報公告日(7/8/10/11 月密集)
- web fallback:公司 IR / SEC EDGAR 10-Q
- `mcp__atlas_mcp__risk_get_correlation_matrix` — 半導體 ↔ AI capex 相關性

---

## Step 3:建議(私人平台散戶 — exit timing 優先)

**觸發向(下修至 < 20%)**:
- **這是韓股崩盤真因前兆**:
  - 散戶持有半導體個股 → **立即評估減碼 30-50%**(對位 SK Hynix -52% 教訓)
  - 散戶持有半導體 ETF → 重新評估槓桿倍率
  - 該賣沒賣的散戶 → **這是最後一根稻草訊號,不是恐慌訊號**
- **不該做**:恐慌殺低 / 砍光 / 借錢加碼

**反向(四家同步 > 50%)**:
- **AI 敘事強化**,但**不等於無腦加碼**:
  - 散戶想加碼 → 確認 TSMC 月營收是否同步強勁(雙確認)
  - 散戶想減碼 → 不需要因為反向觸發而重新進場
  - **注意**:2026 上半年已大幅上漲,**反向觸發是「持有不賣」訊號,不是「現在進場」訊號**

**觸發失敗**:觀望

**結構性誠實**:
- 觸發向但只有 1 家下修 / 3 家仍強 = **未觸發(非結構性訊號)**,標「僅 NVDA 下修,結構未變」
- atlas 端 401/503 = 標 fail 不觸發
- 反向觸發需 4 家同步,3 家不達 = 標 fail

---

## Step 4:落 §6 + Telegram

- 落 `_consult-index.md` §6 第 N+2 筆紀錄
- Telegram 通知 + 摘要 4 家雲端商 capex 變動
- 結構性誠實標(若僅 1 家下修 = 「非結構性」)

---

## 實作 checklist(給開發 / atlas agent 用)

### A. 修 atlas-mcp-trigger-monitor.py(line 175 後新增 TEMPLATES 條目)

```python
# 第 18 模板(2026-08-09 新增,對位 v6.58 韓股 HBM 預期降溫真因)
"ai-capex-guidance-cut": {
    "name": "AI capex 指引下修觸發",
    "file": "trigger-ai-capex-guidance-cut.md",
    "condition": "任一雲端商(NVDA/GOOGL/META/MSFT)capex YoY 指引從 > 30% 下修至 < 20%",
    "http_path": "/api/macro/snapshot/latest",
    "field": "ai_capex_guidance_yoy_min",  # 取四家中最低值
    "metric": "value",
    "threshold": 20.0,
    "compare": "lt",
    "extra_check": {
        "ai_capex_guidance_yoy_previous": "value>30",  # 上一季 > 30%
    },
    "is_capex_downgrade": True,  # v0.4 新分支:capex 指引下修偵測
    "tracked_symbols": ["NVDA", "GOOGL", "META", "MSFT"],
},
```

### B. 注意

1. **atlas 端 `*_capex_guidance_yoy` 欄位未必暴露**,需先 `data_get_field_contract` 驗證
2. 若無欄位 → 走 web fallback(公司 IR / SEC EDGAR)→ 模板升級為 `is_web_fallback` 模式
3. **訊號有時間延遲**:財報公告後 capex 指引生效,監測需在公告後 5 天內跑

### C. 測試(atlas 端恢復後跑)

- [ ] `curl "/api/macro/snapshot/latest"` 確認含 `ai_capex_guidance_yoy_*` 欄位
- [ ] 結構性誠實測試:注入 NVDA capex 指引從 +35% → +18% → 觸發
- [ ] 反驗證:NVDA -5pp 下修但仍 > 20% = 未觸發(下修幅度不足)

### D. 上線

- 不需動 atlas backend(只在 atlas-wiki/_scripts + templates 加)
- kaecer 拍板啟用後 → 落 `_consult-index.md` §6.4 對位表

---

## 對位 SKILL 與憲章

| 對位項 | 內容 |
|--------|------|
| ATLAS_METHODOLOGY 7 層因果鏈 | Layer 1(全球資金配置)+ Layer 4(產業鏈結構) |
| Q5 宏觀 | 跨 Q5 + Q3 雙對位 |
| 散戶語言(私人平台/exit timing) | 「雲端商降 capex = AI 敘事降溫,半導體個股訊號反轉,該賣沒賣的現在評估減碼」 |
| 結構性誠實 | 4 家同步才反向觸發;1 家下修 = 未觸發(非結構);atlas 失敗 = 標 fail |

---

## 為什麼這模板值得加

- **現有 16 模板全吃 macro/個股/chips/HBM 週期/MSCI 再平衡**,**沒涵蓋 AI capex 結構性指引變動** = 觸發鏈上游訊號源完全失明
- **這是韓股 2026/7 崩盤的核心觸發鏈起點**(HBM 預期降溫 → 兩大權重股估值重估)
- **台股 TSMC 與 NVDA / Google / Apple 高度連動**,AI capex 變動 = **台股結構性風險預警源**

---

## 不該做的事

- ❌ 不要 1 家下修就觸發(會假警報)
- ❌ 不要用 LLM 推估 capex 數字(必須 atlas 端欄位或 web fallback)
- ❌ 不要把反向觸發寫成「無腦加碼」(2026 H1 已大漲,反向是持有不賣)
- ❌ 不要跳過開發 agent 改 monitor.py(`is_capex_downgrade` flag 需正式擴充)