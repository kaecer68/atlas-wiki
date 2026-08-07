---
title: SK-00 技能索引指南
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-00
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: []
verification: 本檔是純索引頁,驗證方式 = `ls ~/workspace/atlas-wiki/skills/SK-*.md | wc -l` 應回 35(33 編號含 SK-27/30 archive + SK-31 二擇一衝突待 §未消化 + SK-00 索引);實際 grep 2026-08-07 = 35 個檔案。
---

## 一句話定位
SK-00 在 atlas 是「所有 SK 頁的目錄 + pipeline 組裝藍圖」——給散戶一句話看完整套體系怎麼用,不需逐頁翻。

## 論文版概念（忠實還原來源）
- **功能**:編號 + 名稱 + 功能 + 依賴關係 + 典型應用 pipeline
- **預期輸出 JSON**:skills 陣列(34 條)+ pipelines(三條主軸:supervised / reinforcement / robustness)
  - **SK-33 audience-routing 例外**:不在三條 pipeline 內——它是 SK-00 同層的元能力(meta-skill),跨所有 pipeline 提供 audience 切換
- **三條主軸 pipeline**(論文原版):
  - **supervised_learning**:`SK-01 → SK-03 → SK-09 → SK-16 → SK-18`(建因子→切時序→PLS→十分位→Alpha)
  - **reinforcement_learning**:`SK-23 → SK-03 → SK-24 → SK-26 → SK-29 → SK-18 → SK-28`(產業環境→切時序→PPO→LSTM→回測→Alpha→獎勵診斷)
  - **robustness**:`SK-20 → SK-21`(規模分組→排除仙股);**SK-22 部分對位(PR #1443,commit 383a48b8,2026-08-02)**——實驗級 metric delta 可用(`experiment_diff` 回 acceptance_metric/baseline_value/candidate_value;**2026-08-07 證偽 eval_metrics — 18/18 experiment 皆無此欄**),by-factor 排除式邊際貢獻仍對位失敗;atlas-mission pipeline 內**實驗級可落地,by-factor 路徑不列入**

## atlas 對位
| 論文概念 | atlas-mcp 對位 |
| 33 個 SK 索引 | 本檔 + `~/workspace/atlas-wiki/skills/SK-*.md`(已 33 頁) |
| 33 個 SK 索引(2026-08-07 +SK-33 → 34) | 本檔 + `~/workspace/atlas-wiki/skills/SK-*.md`(已 34 頁;SK-33 audience-routing 是元能力頁) |
| 三條 pipeline | 對位 atlas `universe_get_sessions`(SL/RL session 結構) |
| 跨 SK 依賴 | `experiment_history`(audit trail) |

**差異點**:論文版是靜態 JSON 索引,atlas 版是動態 wiki 頁面+ atlas 端 session log 交叉對位。**散戶實務:先看本檔選 pipeline,再去翻個別 SK 頁的「驗證方式」段照跑**。

**沒有對位的部分**:無原生「skill index」端點;無「跨 SK 依賴圖」端點。

## 散戶解讀（GROW+ 引用點）
- **G 段**:用戶問「我該從哪個 SK 開始?」 → 看 pipeline:
  - 監督學習用戶:走 `SK-01→SK-03→SK-09→SK-16`
  - 強化學習用戶:走 `SK-23→SK-24→SK-25`
  - 任何策略要穩健:必跑 `SK-20→SK-21`;**SK-22 兩層分開**(2026-08-02 PR #1443):**實驗級 metric delta 可用**(用 `experiment_diff` 拿 prompt mutation 帶來的 baseline vs candidate 數值),**by-factor 排除式邊際貢獻仍對位失敗**,僅作 Fin-Skill 概念對照
- **R 段**:對位 atlas → 「`universe_get_sessions` 取一份 supervised session,看用了哪些 SK;`experiment_history` 對應 SK pipeline」。
- **+E 段**:警示「**不要跳 SK-03 直接做 SK-16**——沒切時序直接跑多空十分位,90% 是 overfit」。Pipeline 順序是學術驗證後的捷徑,**散戶自創順序 9 成踩雷**。
- 對位 ATLAS_METHODOLOGY 七時期:三條 pipeline 在不同 regime 的可靠度不同——SL pipeline 在 RISK_ON 穩定,RL pipeline 在 regime 切換時更有適應力,robustness pipeline 是任何 regime 的必要驗證。

## 驗證方式
Step 1: `ls ~/workspace/atlas-wiki/skills/SK-*.md | wc -l` 應回 34(33 主體 SK 含 SK-33 + SK-00 索引)。
Step 2: 對 `universe_get_sessions` 抽一份 supervised session,看其 strategy_id 對應哪些 SK。
Step 3: 對 `experiment_history` 抽一份,看其 pipeline metadata 是否含 SK pipeline 標籤。

## 未消化 / 待補
- [ ] 論文 pipeline 順序(supervised / reinforcement)是否真為「最佳實務」,需在台股資料上重跑驗證。
- [x] **archive 標一致性驗證(2026-08-02)**:grep SK-00/27/30 三檔 archive 標,**三者一致**——SK-00 §未消化寫「SK-27/SK-30 已標 [ARCHIVED — 學術展示無對位]」,SK-27 frontmatter 自標 archive + §散戶解讀「主動 archive」,SK-30 frontmatter 自標 archive + §驗證方式「無 L3 端點。本頁 archive」。無引用錯誤。
- [x] **SK-22 pipeline 標翻轉(2026-08-02 PR #1443)**:§論文 pipeline robustness 段由「對位失敗」改為「兩層分開——實驗級可用,by-factor 仍失敗」;§散戶解讀 G 段同步。`_consult-index.md` §2 Q2 + §3.1 SK-22 段 + §6.2 紀錄三處同步;`SK-22-ablation-analysis.md` 全文重寫;`SK-13-permutation-importance.md` §atlas 對位「因子刪除後效果」行同步。
- [ ] 跨 SK 依賴圖(visualization)未實作,目前只有文字 pipeline 順序。

## SK-31 衝突待解(2026-08-07)

- **現況**:`SK-31-ai-investment-cycle-2026.md` 與 `SK-31-sl-vs-rl.md` 同編號,35 個檔案 ≠ 33 主體
- **原因**:Fin-Skills 原版 SK-31 應為單一頁(待查 Fin-Skills.md §SK-31)
- **解法**:重命名 `SK-31-sl-vs-rl.md` → `SK-XX-sl-vs-rl.md`(XX = 下一未佔編號),待你拍板
- [x] 規範已同步(2026-08-01 v0.9 結算):SKILL.md size 6000→9000 bytes(4 處)、quota 5→3 頁(8 處);_method.md 已對齊 9,000 bytes 與 3 頁上限
