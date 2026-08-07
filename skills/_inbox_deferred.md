---
title: atlas-wiki 內部約定登記處 — audience / 跨邊界決議(v6.52 撤銷外推改內部化)
type: deferred-registry
status: active
created: 2026-08-07
created_by: hermes-agent
trigger: "manifest _manifest_coverage_routing.md v1.0 §3.3 Day 3 + kaecer 2026-08-07 第 3 輪拍板"
amendable_by: kaecer
related:
  - skills/_manifest_coverage_routing.md §2 題 3 + §3.3 Day 3
  - skills/_inbox.md §待辦總表(inline 條目因 size 上限已分散至此檔)
  - SOUL §3.7.3 第 6 條(規範本體邊界)+ §3.7.4(agent 自主範圍)
  - AGENTS.md §11 內容歸檔規範
---

# 內部約定登記處 — atlas-wiki audience / 跨邊界決議(v6.52 撤銷外推)

> **為何獨立成檔**:主檔 `_inbox.md` 現 11301 bytes,超過 _method §3 size 9,000 上限,
> 無法在主檔內 append 新段。本檔作為「**內部約定 / 跨邊界提案**」的專屬登記處,
> 主檔只留 1 行 cross-ref,所有條目細節走這裡。
> 
> **對位**:SOUL §3.7.3 第 6 條邊界(_method.md / SKILL.md 規範本體修改 → 走 task-governance)
> + SOUL §3.7.4(agent 自扛範圍)——
> **2026-08-07 v6.52 撤銷外推**:kaecer 拍板「我們自己把事做完,不外推」,本檔**不再以「跨邊界移交給 hermes owner」為主軸**,而是「**atlas-wiki 內部約定**」(agent 從 session context 讀 audience,預設 `user`)的登記處。若未來 hermes runtime 提供 `HERMES_AUDIENCE` env,升級為「env 優先,session context fallback」雙層架構。
> 
> **v6.52 範圍重定義**:
> - ✅ **可做**(atlas-wiki 範圍):SK-33 / financial-advisor-coach §X / 來源標籤格式 / 三 audience 表達紀律
> - ⚠️ **需走 task-governance**(規範本體擴張):_method §3 size 上限例外 / SOUL §0.1 例外 5 種 / 憲法本體
> - ❌ **不再外推**(已撤):「動 hermes runtime 全域設定」(原屬 owner 範圍,改為內部約定)

---

## 內部約定總表(2026-08-07 v6.52 起,取代「跨邊界移交」表)

| 提案 ID | 內容 | 來源 | 影響 | 落地範圍 | 狀態 |
|---|---|---|---|---|---|
| ENV-CR-2026-08-07 | atlas-wiki **內部約定**(取代原 hermes runtime env 提案):agent 從 session context 推導 audience,預設 `user`;**未來 hermes runtime 升級時**,若提供 `HERMES_AUDIENCE` env,改為「env 優先,session context fallback」雙層架構 | manifest v1.0 §2 題 3 + §3.3 Day 3 + **2026-08-07 v6.52 kaecer「我們自己把事做完,不外推」拍板** | atlas-wiki / atlas-notes agent **自扛** audience 識別 | SK-33 frontmatter 已修(v6.52);financial-advisor-coach §X 待寫;不依賴 hermes runtime env | 部分落地(SK-33 ✅;§X 待寫) |

---

## ENV-CR-2026-08-07:HERMES_AUDIENCE → atlas-wiki 內部約定(v6.52 撤銷外推改內部化)

### 用途
讓 agent 對散戶預設不外漏 error code + 給開發者看完整 audit 細節 + 給 admin 看 metrics trend。

### kaecer 第二輪訊息原始理由
「投資人用戶會非常害怕看到任何信息出錯或有任何問題提醒的警告」 → user 觀點不可外漏原生日誌
「系統管理者就特別需要知道有沒有什麼地方信息不對」 → admin 觀點必須看到完整 audit 細節

### v6.52 內部化決策(取代原 owner 提案)
- **原方案**:HERMES_AUDIENCE env → hermes daemon 啟動時讀取 → 跨邊界移交 Nous Research
- **新方案**:atlas-wiki agent **自扛** audience 識別 — agent 從 session context(使用者 channel / task type / time-of-day)推導,預設 `user`;若未來 hermes runtime 升級提供 env,改雙層架構(env 優先,session context fallback)
- **決策理由**:kaecer 2026-08-07「我們自己把事做完,不外推」+「quota 不含直接指令」拍板

### 配套 skill 落地(已部分完成,§X 待寫)
1. ✅ **SK-33-audience-routing.md**(Day 1 quota)— 三 audience 各自的輸入 / 輸出 / 引用規範,frontmatter v6.52 已修語意
2. ⏳ **financial-advisor-coach §X** — 對 `user` audience 的 atlas-mcp 降級口徑(error 改「目前這項的公開資料源不在我的服務範圍」、來源必標 `[來源: ...]`);**v6.52 改為 atlas-wiki 自扛,不走 task-governance**(對位 kaecer 「quota 不含直接指令」)
3. ⏳ **`_scripts/handle-atlas-failures.py` #7**「Source Unreachable」分支(走 task-governance)— 對應 §CR-2 落地

### 風險點(已緩解)
- ~~env 未上線前 agent 全走 user 口徑 → developer / admin 視角在過渡期受限制~~ → **v6.52 解**:agent 自扛 session context 推導,過渡期不再受限
- 預期 ~~hermes owner 回覆期 ≤ 14 天~~ → **v6.52 解**:已撤銷 owner 回覆依賴
- 配套 SK-33 + financial-advisor-coach §X 應**先**寫完,避免「caller 還沒讀」的索引空窗 → 仍維持

### 移交後狀態更新規則(v6.52 修)
1. ~~收到 hermes owner 回覆後...~~ → **撤銷**(已無 owner 移交)
2. §X 寫完後,於本表「狀態」欄更新為「全部落地」
3. atlas-wiki 內 agent 自扛的補強(SK-33 已修、§X 待寫)不阻塞,可平行推進
4. ~~每 14 天 owner 未回應 → append 「逾期 T3 evidence」~~ → **撤銷**(已無 owner 依賴)

---

## 變更記錄

- **v1.0 / 2026-08-07**:首次建立(kaecer 2026-08-07 第 3 輪拍板:HERMES_AUDIENCE 提案移交)
  - 觸發:manifest §3.3 Day 3 + 主檔 `_inbox.md` 已 11301 bytes 超 size 上限
  - 來源:kaecer 第 2 輪反饋「給提示詞」+ manifest v1.0 §2 題 3 + §3.3
  - 目的:把跨邊界提案獨立登錄,主檔不超 size 上限,移交鏈可追蹤
  - 不變動:主檔 `_inbox.md`、manifest v1.0 本體、SOUL/AGENTS.md 規範本體

- **v1.1 / 2026-08-07 v6.52**:撤銷外推,改內部化(對位 kaecer「我們自己把事做完,不外推」拍板)
  - 觸發:kaecer 第 5 輪訊息「owner 就是我」+ 「原本推給別人的,做完後再研究突破」拍板
  - 變更:title 改「內部約定登記處」;總表「跨邊界移交」→「內部約定」;ENV-CR-2026-08-07 從「env 提案等 owner」改「agent 自扛 session context 推導」;移除 hermes owner 回覆鏈 / 14 天逾期警報 / GitHub issue 提交流程
  - 不變動:主檔 `_inbox.md` §擱置區 cross-ref、manifest v1.0 §2 題 3 + §3.3(語意由 manifest §3.1 CR-3 (a) 同步修)
