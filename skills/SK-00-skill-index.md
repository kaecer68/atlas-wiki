---
title: SK-00 技能索引指南
description: "要查「有哪些 SK 頁、某主題屬哪一頁、pipeline 順序」時載入。"
type: skill-inbound
source: ~/workspace/Fin-Skills/Fin-Skills.md §SK-00
ingested_at: 2026-08-01
status: active
tier: T3
confidence: high
atlas_go_relevance: high
mcp_tools_used: []
verification: 本檔是純索引頁,驗證方式 = `ls ~/workspace/atlas-wiki/skills/SK-*.md | wc -l`; **2026-09-27 實測 = 40**(39 編號 + SK-00 索引;SK-27/30 已 archive)。歷史值:同日稍早 = 39(新增 SK-39 前)、37(新增 SK-37/38 前);2026-08-21 = 36(原 35 + SK-36 新編號)。
l3_run_at: 2026-09-27
l3_run_by: prime-agent（PR docs/20260927-sk00-l3-and-coverage-gate）
l3_endpoints_probed:
  - "N/A（純索引頁，無 atlas HTTP 端點；本頁的可驗證宣稱就是索引一致性）"
  - "`ls skills/SK-*.md | wc -l` → 40；`python3 skills/_scripts/audit-file-index-sync.py` → 8 類 sync 通過、0 未索引（2026-09-27T20:58:03+08:00）"
  - "`python3 skills/_scripts/check-skill-index-sync.py`（R1+R3+R4）→ 通過（同上時間）"
---

## 一句話定位
SK-00 在 atlas 是「所有 SK 頁的目錄 + pipeline 組裝藍圖」——給散戶一句話看完整套體系怎麼用,不需逐頁翻。

## SK 全表（40 檔;2026-09-27 `ls skills/SK-*.md | wc -l` 實測）

> 2026-09-27 補:本節補列 17 檔原本未被本索引引用的 SK 頁（audit-file-index-sync.py 實測）。名稱取自各頁 frontmatter `title`。

- **SK-00** 技能索引指南（本檔）
- **SK-01~09 因子與建模**:SK-01 建構多元預測因子庫｜SK-02 特徵擴充:股票-總經交互作用｜SK-03 時間序列滾動切割｜SK-04 Huber 損失異常值處理｜SK-05 OLS 基準線性模型｜SK-06 彈性網正則化模型｜SK-07 廣義線性模型(樣條非線性)｜SK-08 主成分迴歸(PCR)｜SK-09 偏最小平方法(PLS)
- **SK-10~19 模型與評估**:SK-10 隨機森林模型｜SK-11 多層神經網路(1~5 層)｜SK-12 樣本外評估(R²/夏普/累積報酬)｜SK-13 排列重要性｜SK-14 部分相依圖(邊際效應)｜SK-15 雙特徵交互作用分析｜SK-16 多空十分位數投資組合｜SK-17 加權方式(等權/價值加權)｜SK-18 因子模型風險調整 Alpha｜SK-19 交易成本與稅務調整
- **SK-20~29 穩健性與強化學習**:SK-20 規模分組穩健性檢驗｜SK-21 排除仙股穩健性檢驗｜SK-22 消去法(排除特定因子集)｜SK-23 產業輪動環境建構｜SK-24 PPO 強化學習訓練框架｜SK-25 獎勵函數設計與評估｜SK-26 經典策略網路(LSTM/Transformer)｜SK-27 量子增強策略網路(已 archive)｜SK-28 獎勵-績效錯配診斷｜SK-29 滾動窗口回測模擬
- **SK-30~36 治理・判斷・備援**:SK-30 量子模型訓練穩定性分析(已 archive)｜SK-31 2026 AI 投資週期對位台股｜SK-32 獎勵函數敏感性分析｜SK-33 三 audience 表達口徑切換｜SK-34 上市/上櫃分流判斷與備援｜SK-35 atlas-mcp 失敗時 4 級 fallback 鏈｜SK-36 監督學習 vs. 強化學習策略比較
- **SK-37~38 流動性・歸因(2026-09-27 新增)**:SK-37 流動性分位與買賣價差篩選｜SK-38 PnL 歸因工作流(描述性歸因 vs 消去法)
- **SK-39 放空成本模型(2026-09-27 新增)**:借券費/標借費/平盤下規則的外部制度面＋atlas 端四個已驗證的否定(無借券費參數、SBL 欄位不可達、`sharpe_short` 非可實現報酬、可行性 0 對位)

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
| **40 個 SK 索引(2026-09-27 實測)** | 本檔 + `skills/SK-*.md`(40 頁,含本索引頁;SK-27/30 已 archive) |
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
Step 1: `ls ~/workspace/atlas-wiki/skills/SK-*.md | wc -l` 應回 **40**(2026-09-27 實測;39 編號 + SK-00 索引,SK-27/30 已 archive)。
Step 2: 對 `universe_get_sessions` 抽一份 supervised session,看其 strategy_id 對應哪些 SK。
Step 3: 對 `experiment_history` 抽一份,看其 pipeline metadata 是否含 SK pipeline 標籤。

## 相關入口

- `_consult-index.md` — 工具路由（Q→atlas-mcp 端點）
- `_knowledge-router.md` — 知識路由（Q→concepts/entities 知識頁→SK,角色 GT/INT/NAR/DOC,2026-08-22 案 A 建立）
- `_method.md` — 寫入規範（六條鐵律）
- `_inbox.md` — 跨 SK 待辦總表

## 未消化 / 待補
- [ ] 論文 pipeline 順序(supervised / reinforcement)是否真為「最佳實務」,需在台股資料上重跑驗證。
- [ ] 跨 SK 依賴圖(visualization)未實作,目前只有文字 pipeline 順序。

## SK-31 衝突已解決(2026-08-21, 方案 b: renumber sl-vs-rl → SK-36)

- **現狀**:`SK-31-ai-investment-cycle-2026.md` 保留為 SK-31 唯一對應(AI 投資週期);原 `SK-31-sl-vs-rl.md` 重新編號為 `SK-36-sl-vs-rl.md`(2026-08-21 kaecer 拍板方案 b, kimi-for-coding 審查 8 步執行)
- **原因**:兩個 SK-31 編號主題不同(AI 投資週期 vs SL/RL 策略比較),不互補,合併方案 a 不可行;保留雙頁方案 c 治標不治本
- **執行**:`git mv SK-31-sl-vs-rl.md → SK-36-sl-vs-rl.md` + 修 frontmatter `renumbered_from: SK-31` + 修 5 個引用 (SK-32, _methodology_alignment_audit, _index-finskills, SK-00, T9 v2)
- **驗證**:2026-08-21 當日 36 個 SK-* 檔案(原 35 + SK-36 新編號);**2026-09-27 實測 40**(以 `ls skills/SK-*.md | wc -l` 為準);`grep -R 'SK-31' --include='*.md' skills/ | grep -v 'SK-31-ai-investment-cycle-2026.md' | grep -v '§SK-31'` 應只出現於 _index-finskills.md 與 _methodology_alignment_audit.md 的 deprecate 註記
- [x] 規範已同步(2026-08-01 v0.9 結算):SKILL.md size 6000→9000 bytes(4 處)、quota 5→3 頁(8 處);_method.md 已對齊 9,000 bytes 與 3 頁上限
