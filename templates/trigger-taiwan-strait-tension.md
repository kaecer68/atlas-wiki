# 台海緊張 觸發模板(單日版)

**觸發條件(單日)**:GeoIntensity ≥ 40（v1.1 §3 對位 — 4 級制升溫(2)及以上 / 觸發轉折下壓候選）
**對位**:ATLAS_METHODOLOGY.md §二 Layer 5(地緣政治) + §3 判別聚合規則（v1.1，2026-08-25 補）
**對位 strategy**:taiwan-strait-tension(L5, hit_rate 0.55)

> **v1.1 對位說明**:v1.0 時期用「geopolitical 元件值 > 4」（台灣壓力指數 scale=1.0、weight=0.13 元件），屬污染刻度；v1.1 起改為 GeoIntensity 0-100（4 級制：平靜 0-25 / 升溫 26-50 / 高張 51-75 / 危機 76-100），由 TaiwanRSSGeopoliticalProvider 直接產出。判定：≥ 40 為升溫(2)級觸發轉折下壓候選；≥ 60 為高張(3)級觸發黑天鵝候選；≥ 76 為危機(4)級（v1.1 §3 判別聚合規則表）。

## Step 1:信號捕捉(對位真實 2026-08-03 → v1.1 重對位)
- **geopolitical 5.07**（舊刻度）對位 v1.1 GeoIntensity 估算：原 taiwan_stress_index 的 geopolitical 元件經 scale=1.0、weight=0.13 計算，5.07 屬「低度升溫」；v1.1 重對位為 GeoIntensity 4 級制估算需經 component→GeoIntensity 換算（具體換算公式待 §3 對位延伸派工）。
- **對位端點**:`mcp__atlas_mcp__macro_get_stress_index_current`(geopolitical 元件;原 taiwan_stress_index 已改名);v1.1 對位 GeoIntensity 輸出端點待 §3 對位延伸派工後確認。

## Step 2:自動跑端點
- mcp__atlas_mcp__capital_flow_summary(外資期貨 -82515 偏空)
- mcp__atlas_mcp__mcp_quickstart(stress score -7.66 low)[2026-08-22 驗證:stress score 為連續值隨日變動,-7.66 為 2026-08-03 快照;實跑 macro_get_stress_index_current 2026-08-23=7.71(low),與 log.md 歷史 29.92(low)/32.55/34.74(alert) 同指標同尺度]

## Step 3:建議
- 觸發成功(GeoIntensity ≥ 40) → **加碼內需/高股息/黃金/防禦性資產 5%**(對位 §3 轉折下壓候選)
- 觸發失敗(GeoIntensity < 40) → 觀望

## Step 4:落 §6 + Telegram
