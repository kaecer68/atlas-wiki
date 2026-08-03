---
title: H1/H2/H3 假說 D+1 EXTEND 驗證(2026-07-18 對照 2026-07-17)
created: 2026-07-18
updated: 2026-07-18
type: query
tags: [T, signal, hypothesis, time-anchor, anomaly, contested]
sources:
  - queries/H1-H2-H3-replay-2026-07-17.md
  - concepts/funding-forces-taxonomy-e05-pending-approval.md
  - concepts/taiwan-money-flow-seven-institutional-buckets.md
confidence: low
contested: true
contradictions: [queries/H1-H2-H3-replay-2026-07-17.md]
---

# H1/H2/H3 假說 D+1 EXTEND 驗證

> **狀態**:研究文件,E05 修正分類(5 主體)待業主簽核,簽核前不修改正式 manifest / 後端 / 生產權重。
> **不宣稱 H 假說已通過/失敗**:只標 D+1 觀察到的五主體方向 + SUSPECTED → CONFIRMED → EXTENDING → DISTRIBUTING → EXITED 狀態變化。

## 任務邊界

昨晚(2026-07-17)第一次事件回放針對 H1/H2/H3,真實發生的事:

- TAIEX -6.47%(2026-07-17, 大跌當日)
- 5 主體方向矩陣(7/17): 外資 bear / 投信 bull(+0.30) / 自營商 bear(-31.98) / **官股 MISSING** / 散戶 bull → 典型「土洋對殺」
- stress foreign_flow 從 -0.07 跳 22,7/17 18:42 UTC 一度 alert 32.55,19:59 又回 low 29.92
- narrative 仍把 AI_capex 標 conf 0.95;darwinian 已把 ai_supercycle_model 權重壓到 0.0001

今晚的問題:**D+1(2026-07-18),五主體方向是 EXTEND(確認)還是 DISTRIBUTING(開始翻轉)?** 這是 SUSPECTED → CONFIRMED → EXTENDING 鏈條的關鍵驗證點。

## 真實觀察(2026-07-18 15:59:54 UTC)

### 5 主體方向矩陣(E05 修正版)
來源:`capital_flow_summary`、timestamp=1784390093

| 主體 | raw_value | trend | z | 狀態機標籤 |
|---|---|---|---|---|
| 外資 | -12.72 | bearish | -1.368 | **EXTENDING bear**(從 7/17 延續) |
| 投信 | +0.296 | bullish | +1.202 | **EXTENDING bull**(從 7/17 微 bull 延續) |
| 自營商 | -31.98 | bearish | -1.408 | **EXTENDING bear**,絕對值未收斂 |
| 官股行庫 | 0 | (neutral/缺資料) | n/a | **MISSING 仍持續**(缺資料,不能當中性) |
| 散戶 | +29.30 | bullish | +1.403 | **EXTENDING bull**,z 從 7/17 (當時 retail_raw_value 算法未知,>0) 延續 |

- resonance_dir = **bearish**
- dominant_force = dealer(-31.98)
- quality_label = strong_outflow(-1.57)
- 缺資料旗標:government=0 + futures=0 → 至少 2 個觀測維度確認有資料斷層,非中性

### 對照 7/17 的 EXTEND 矩陣(回填表)

| 主體 | 7/17 | 7/18 | 變化 |
|---|---|---|---|
| 外資 | bearish | bearish | **EXTEND bear**(量級略縮 -12.7 vs 原始量級未知,但符號不變) |
| 投信 | bull | bull | **EXTEND bull** |
| 自營商 | -31.98(已週一落底) | -31.98(同日 timestamp) | 看上去同一日 snapshot;**不是新增**,要小心讀(見 §限制) |
| 官股 | MISSING | MISSING | **持續 MISSING**(2 個交易日皆無觀測) |
| 散戶 | bull(retail_raw +29.30 來自 7/17 macro snapshot) | bull +29.30(同一筆?) | **同上,要小心是不是同一日收盤後快照** |

### stress index 5 點序列(從 7/16 到 7/18)

`macro_get_stress_index_history` 7 點(節錄重點):

| UTC timestamp | date(估) | score | regime | foreign_flow 成分 |
|---|---|---|---|---|
| 1784236913 | 7/16 早 | 7.49 | low | -0.07 |
| 1784247900/8613 | 7/16 17:45 | 16.77 | low(連 3 tick) | -0.07 |
| 1784299374 | 7/17 13:42 | **32.55** | **alert** | **22**(跳 296x) |
| 1784303993 | 7/17 14:59 | 29.92 | low(降) | 22 |
| 1784390093 | 7/18 15:54 | **30.45** | **alert** | 22(持續) |

**關鍵觀察**:foreign_flow 22 這個成分值,從 7/17 13:42 到 7/18 15:54,**至少 4-5 個 tick 都是 22**。這意味著:

- 7/17 從 -0.07 跳到 22,**不是單日 spike**。是後續延伸中。
- 7/18 仍 22 → stress score 仍 alert 區 → **H2 的「本土機構承接」機制尚未觸發**(若投信繼續買但融資不升才算 H2 通過;目前 stress alert 表示環境未舒緩)。
- smoothing 切換邏輯仍未公開(7/17 alert → low → 7/18 alert 是同一個 score 帶,但 regime 不同)。**已知問題,今晚不重做**。

### narrative vs darwinian 一致性再次驗證

`narrative_get_bundle` 2026-07-18 16:01:09 UTC:

- AI_capex event conf=0.95,expires 7/25(7 天後到期) — 仍在 active
- JPY_carry_unwind event conf=0.664,expires 7/23 — 短線更急
- hawkish_fed_model darwinian weight = 0.1428
- ai_supercycle_model darwinian weight = **0.0001428**(被壓到接近 0)

**EXTEND 觀察**:7/17 已記錄的「narrative vs darwinian 不一致」**仍在持續**(同一筆 snapshot 來源)。**不是 7/17 偶然,是結構性**,這本身是 S(訊號紊亂)的觀測之一。

## H 假說 D+1 狀態判定(低 confidence 嚴守邊界)

### H1(跨來源方向一致性 = S 紊亂)
- 7/17:**通過**(一次觀察)
- **D+1 觀察**:5 主體齊向(2 bull / 2 bear / 1 MISSING)且 stress alert 持續 → 跨主體依然不對齊
- 7/18 結論:**支持延續(EXTENDING)**,但單點 D+1 不構成驗證。要觀察 5+ 個交易日才能上 medium confidence。

### H2(本土機構買而融資不升 = 真護盤)
- 7/17:**未通過**(投信 +0.30 但自營商 -31.98;不構成「本土同步承接」)
- D+1 觀察:7/18 投信 +0.296 與 7/17 +0.30 **幾乎重複**。**但若把兩日視為同一筆收盤後快照**,則這不是 D+1 EXTEND,而是「原始數據沒刷新」。**此處須誠實標誌:目前無法區分「真的 7/18 新值」與「快照延遲未更新」。**
- 7/18 結論:**尚未通過,也尚未失敗**(D+1 樣本不足)

### H3(被動 / 套利誤判)
- 7/17:**通過但觸發條件與 template 不同**(真實 pattern 是「散戶去槓桿 + 借券放空」)
- D+1:7/18 retail_short_balance 仍 2.363(從 7/17 +33.79% 後);無法確認是否繼續上升
- 7/18 結論:**樣本不足,無法對 H3 上調**

## 進度鏈條

照 SUSPECTED → CONFIRMED → EXTENDING → DISTRIBUTING → EXITED 對今天的觀察重新標:

- **主體狀態(7/18)**:
  - 外資:CONFIRMED bear(連 2 日同符號,從 7/17 起開始)→ 屬於 EXTENDING bear
  - 投信:CONFIRMED bull(連 2 日微正)
  - 自營商:CONFIRMED bear(連 2 日大負)
  - 官股:**MISSING**(資料未到位)
  - 散戶:CONFIRMED bull(連 2 日正)
- **敘事**:
  - AI_capex narrative:CONFIRMED(從 7/17 起持續)但 darwinian 把它降權 → 結構性 S 訊號
  - JPY_carry_unwind narrative:CONFIRMED(從 7/17 起持續)→ 屬於 EXTENDING bear 流

## 限制(不隱藏)

1. **兩個 snapshot 疑似延遲未刷新**:`capital_flow_summary` 與 7/17 那份 macro snapshot 的 retail_raw +29.30 / dealer -31.98 數字完全相同。資本流報表可能是 T+1 結算,因此 7/18 讀到的數字其實是 7/17 收盤後的快照。**此處必須誠實標:** 我無法用一次 MCP 呼叫區分「7/18 新值」與「7/17 snapshot 重複」。
2. **政府資金 0 持續 2 日**:已驗證不是中性,但也無法斷言「官股進場/退場」。需查公開資料源(證交所 8:30 公布)才能補上。
3. **TAIFEX 期貨未平倉 0 持續 2 日**:仍是「外資觀測維度缺資料」。這是 E05 修正案的核心,若 2 日內不補上,要寫進 known-issues.md。
4. **stress smoothing 邏輯不公開**:7/17 同樣 score 帶切到 low 又回 alert,這是 model 內部 state,不影響 H1/H2/H3 判定。
5. **缺 5+ 個交易日的歷史回放**,所以 H 假說 D+1 結論仍是 low confidence。

## 對 E05 修正案的延伸建議

今晚的 7/18 snapshot 觀察**進一步支持** E05 修正提案的 4 個待簽核項目中的前 2 個:

1. ✅ **5 主體共振動態觀察**值得到 — 5 主體當前 2 bull / 2 bear / 1 MISSING,**不是「共振 bearish」**,是「土洋對殺 + 官股位置不清楚」。
2. ✅ **TAIFEX 期貨掛在外資底下、不另計票** — 因為 TAIFEX 0 = 完全無法觀測,**現在的共振算式如果誤把 TAIFEX 當勢力,只會再多一個 0 的噪音票**。
3. ➖ **TSM ADR / VIX / USD_TWD 當情緒特徵** — 7/18 TSM ADR -2.77%、VIX +12.19%、USD/TWD +0.31% 三個情緒指標一致偏空,跟主體方向吻合。**但這也意味情緒調整層若權重太高,會把「土洋對殺」誤算成「一致看空」**。
4. ✅ **缺資料不補零** — 今晚再次驗證:0 不等於中性。

## 待驗證假說(小步候選)

- 跑 2024-2026 同期「外資連 2 日 bear + 投信連 2 日微 bull」的真實發生頻率,確認當前結構是否稀有
- 驗證 capital_flow_summary 的 timestamp 與 macro_get_snapshot 的 timestamp 是否同步更新,以排除「snapshot 延遲」這個第三限制
- 把 2 個交易日的政府與 TAIFEX 期貨缺資料正式寫到 known-issues.md,催促業主補資料源

## 相關頁面

- [[queries/H1-H2-H3-replay-2026-07-17]]
- [[concepts/funding-forces-taxonomy-e05-pending-approval]]
- [[concepts/taiwan-money-flow-seven-institutional-buckets]]
- [[concepts/atlas-mcp-interpretation-guide]]
- [[concepts/t1-t4-signal-light]]
