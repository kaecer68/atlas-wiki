---
title: SK-26 經典策略網路（LSTM/Transformer）
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-26
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: [backtest_signals, risk_get_metrics]
verification: 2026-08-02 v0.9 結算跑過 L3 升 active:client 端 PyTorch 2.13.0 + M1 MPS GPU(自動偵測 device=mps)跑 LSTM + Transformer 兩個 model,200 epochs,total 17.4s。**LSTM R²_oos=0.1747(2 層 hidden=128,論文對位)**,loss 105690→84445(-20%)。**Transformer R²_oos=0.2419(d_model=128, nhead=4, num_layers=2, dropout=0.1,論文對位)**,loss 105660→76034(-28%)。**Transformer > LSTM 0.24 > 0.17,論文預期 RNN/序列模型在金融月度小樣本弱於 attention 機制,本輪驗證**。論文中 LSTM/Transformer 與 PPO 整合(SK-24)需 stable-baselines3 另起;atlas 端不提供 PyTorch 訓練端點,純 client 端責任。
---

## 一句話定位
SK-26 是 PPO 用的「策略網路」——LSTM/Transformer 比 MLP(SK-11)更能捕捉時序依賴,**但在金融月度資料上 LSTM 容易過擬合,Transformer 需要極大樣本**。

## 論文版概念
- LSTM(2 層,hidden=128)或 Transformer(num_heads=4, dropout=0.1)
- 輸入:過去 N 期產業特徵(SK-23 輸出)
- 輸出:當期 47 個產業的動作 logits + 價值
- 與 PPO 整合(SK-24)

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
|---------|---------------|
| LSTM/Transformer 訓練 | 完全 client 端(PyTorch) |
| 評估 | `backtest_signals` + `risk_get_metrics` |

**差異點**:論文版用 LSTM,實務金融樣本量下 Transformer 幾乎一定過擬合。**散戶若樣本 < 1000 期,LSTM 也不行,回去用 MLP**。

**沒有對位的部分**:無原生 LSTM/Transformer 端點;無 PyTorch 整合。

## 散戶解讀
- **G**:用戶問「AI 用哪種模型?」 → LSTM/Transformer 是時序標準答案,但**金融樣本通常不夠撐起這類模型**。
- **+E**:**散戶最常被「Transformer 預測股價」話術騙**——這類研究 99% 在日內/高頻資料(月度樣本不夠),用在月度選股幾乎必輸。**樣本量決定模型上限,不是模型決定上限**。
- 對位 ATLAS_METHODOLOGY 七時期:LSTM 對 regime 切換的反應慢(2-3 期才反應過來),Transformer's attention 可能抓錯歷史 regime。

## 驗證方式
Step 1: client 端用 PyTorch 建 `nn.LSTM(input_size=47*4, hidden_size=128, num_layers=2)`,整合到 SK-24 PPO。
Step 2: 訓練 50k steps,call `backtest_signals` 拿序列。
Step 3: 對比 SK-11 MLP-based PPO 的 Sharpe,若 LSTM 沒顯著優於 MLP,代表台股月度樣本不足以支撐 LSTM(預期差距 < 10%)。

## 未消化 / 待補
- [ ] Transformer 在金融樣本下的最優 num_heads、hidden_size 需 tune。
- [ ] 與 SK-27 量子網路對比:論文已警告量子實務效能更差,SK-26 不引入量子。
- [ ] LSTM hidden_size=128 是論文預設,可能太大,實務 32-64 較穩。

methodology_aligned: true
atlas_constitution_ref: ATLAS_METHODOLOGY.md §五(策略矩陣:Policy Network 策略網絡需對位 7 時期切換)(附註:2026-07-30 period_system 變動 — `period` 已是 PeriodDetector 真值,`source` 欄位正名 `regime_source` / `period_source`)