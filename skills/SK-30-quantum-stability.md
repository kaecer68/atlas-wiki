---
title: SK-30 量子模型訓練穩定性分析
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-30
ingested_at: 2026-08-01
status: archive
tier: T3
confidence: low
atlas_go_relevance: low
mcp_tools_used: []
verification: 論文已明示量子模型不優於經典(SK-27 警告),本頁只記錄「梯度方差」「barren plateau」「參數敏感度」概念,**無 atlas-mcp 對位,標 [ARCHIVED — 學術展示無對位]**。
---

## 一句話定位
SK-30 配套 SK-27——診斷量子網路的訓練穩定性(梯度消失、barren plateau)。**因 SK-27 本身已標 archive,本頁同步 archive,避免後續維護負擔**。

## 論文版概念
- 輸入:quantum_model、training_log、n_qubits
- 動作:
  1. 提取梯度方差
  2. 檢查方差是否隨量子比特數指數衰減(barren plateau)
  3. 算參數微小擾動的輸出敏感度
- 輸出:`{gradient_variance, barren_plateau_detected, parameter_sensitivity}`

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| 量子模擬 | **無對位** |
| 梯度計算 | 完全 client 端 |

**沒有對位的部分**:**全部**。

## 散戶解讀
- 純學術展示。**散戶不該碰量子模型**(理由同 SK-27)。
- 若用戶問「量子 AI 選股穩定嗎?」 → 反問「為什麼你要用一個論文已承認不優於經典的東西?」

## 驗證方式
無 L3 端點。本頁 archive。

## 未消化 / 待補
- [ ] 與 SK-27 同等處理:等學術界有「量子勝過經典」的可重現研究再重啟。


---

## 歸檔聲明(2026-08-07 對位 SK-00 §1)

- **歸檔時間**:2026-08-07
- **歸檔理由**:配套 SK-27(已 archive);atlas 無量子模擬端點,無對位 L3 驗證
- **對位 SK-00 §1**:`archive` 標 + 一句話定位「學術展示無對位」一致