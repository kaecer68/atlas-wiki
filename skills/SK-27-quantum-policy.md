---
title: SK-27 量子增強策略網路（QNN/QRWKV/QASA）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-27
ingested_at: 2026-08-01
status: draft
tier: T3
confidence: low
atlas_go_relevance: low
mcp_tools_used: []
verification: 論文已明示量子模型在真實投資績效低於經典模型,本頁只記錄概念對位,**無 atlas-mcp 對位,標 [ARCHIVED — 學術展示無對位]**。
---

## 一句話定位
SK-27 是論文的「實驗性附錄」——用變分量子電路(VQC)做策略網路,論文**已明示**實務績效低於經典網路,僅作研究用途。**散戶不該用,本頁主動 archive**。

## 論文版概念
- 三種量子網路:QNN、QRWKV、QASA
- 輸入經線性投影到 n_qubits=4 維 → 角度編碼 → 參數化量子電路(CNOT 糾纏)→ 測量期望值 → 經典後接層
- 與 SK-24 PPO 整合

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| 量子網路 | **無對位**(atlas 完全沒量子模擬端點) |
| 評估 | 即使能跑,論文已警告不優於經典 |

**差異點**:atlas 端 0 對位;**論文本身已承認「量子模型在真實投資績效上低於經典模型,建議僅作研究用途」**——本頁主動標記 archive,避免後續浪費工時。

**沒有對位的部分**:**全部**。

## 散戶解讀
- **G**:用戶問「量子計算選股?」 → 論文已說不優於經典,**現實中沒有任何量子選股勝過 LSTM 的證據**。
- **+E**:**「量子選股」是話術的經典樣本**——任何宣稱量子 AI 選股勝過 Fama-French 的,99.9% 是過擬合或包裝。散戶**直接拒絕**。
- 對位 ATLAS_METHODOLOGY 七時期:量子網路在 regime 切換時行為不可預測,加上論文已承認不優,**對位毫無意義**。

## 驗證方式
無 L3 端點可驗。本頁主動 archive,**不建議 atlas 端做對位開發**。

## 未消化 / 待補
- [ ] 量子硬體進展(IBM Condor 等)若未來 NISQ 實用,可能改寫結論,但 2026-08-01 當下無對位必要。
- [ ] 若學術界有新論文「量子 RL 勝過經典」,再回頭重啟本頁,否則維持 archive。
