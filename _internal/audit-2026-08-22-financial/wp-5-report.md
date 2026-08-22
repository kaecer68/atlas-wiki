---
title: WP-5 治理修復報告（_consult-index 瘦身 / 索引補登 / 快照 timestamp / 審計衍生檔歸檔）
type: wp-report
created: 2026-08-22
created_by: child-G (WP-5 治理修復工人)
based_on: _internal/audit-2026-08-22-financial/AUDIT-REPORT-main.md（E-HIGH-1 / P1-1）+ IMPROVEMENT-PLAN.md WP-5
branch: feat/20260822-financial-audit-fixes
---

# WP-5 治理修復報告

## 一、總表（before → after bytes）

| 檔 | before | after | Δ | 狀態 |
|----|-------:|------:|---|------|
| skills/_consult-index.md | 34917 | 8993 | -25924 | ✅ ≤9000B |
| skills/_consult-index_archive.md | 0（新建） | 24521 | +24521 | ✅ 新檔（新檔不需 .bak） |
| README.md | 5186 | 5354 | +168 | ✅ |
| index.md | 5461 | 6173 | +712 | ✅ |
| log.md | 41039 | 41558 | +519 | ✅ append,不改歷史段 |
| skills/SK-31-ai-investment-cycle-2026.md | 8975 | 9021 | +46 | ⚠️ 超 9000B 上限 21B（見「四、偏離與待裁決」） |
| skills/_methodology_alignment_audit.md | 15573 | 15768 | +195 | ✅ 加歸檔指標一行 |
| skills/_methodology_alignment_audit_VERBATIM.md | 10726 | → skills/_archive/（10726） | 0 | ✅ mv 原檔名保留 |
| skills/_methodology_alignment_audit_with_fileline.md | 30522 | → skills/_archive/（30522） | 0 | ✅ mv 原檔名保留 |

備份：7 個動刀檔皆已 `cp <file> <file>.bak.20260822-audit-fix`（archive 新檔與 mv 檔不需備份）。未執行任何 git 命令。

## 二、逐檔改動清單

### 1. skills/_consult-index.md（34917 → 8993,≤9000 ✓）
- **搬出至 archive（byte-preserving,已用 diff 逐一驗證無掉字）**：
  - §3.1 方法論憲章對位的 MCP 工具狀態（5127B,2026-07-30 快照）
  - §3.2 atlas-mcp 端點底層 channel 對位表（2543B,2026-08-01 快照）
  - §6 諮詢紀錄全段（10594B,含 §6.1/§6.2）
  - §6.4 13 觸發模板對位表全段（3177B）
  - §6.3 body「預期查詢地圖」（2033B,依任務書段位計量 §6.4=5227B 含此段,一併歸檔）+ §6.3 header（90B,隨其 body 歸檔,避免主檔殘留懸空標題）
- **主檔留一行指標（對位 _inbox 第七條例外模式）**：§6 / §6.4 / §3.1 / §3.2 各一行,皆含（2026-08-22 audit-fix,對位 _inbox 第七條例外模式）。
- **§3 主體 Q1-Q6 對位表保留並精簡**：19 個端點的長篇描述（實跑快照/PR 修復紀錄等）→「端點名 + 一句用途」;末尾一行 `> 詳見 [[concepts/atals-mcp-tools-reference]] [2026-08-22 audit-fix]`。Q1-Q6 分類與全部端點名保留,驗證細節移入 reference 檔。
- **孤兒字元 `)` 移除**（原 line 325,無配對括號,非任何段落內容）。
- frontmatter 9 欄原樣保留（diff 驗證）。

### 2. skills/_consult-index_archive.md（新建 24521B）
- frontmatter：title/type: archive/purpose/status: active/created: 2026-08-22/created_by/source: _consult-index.md §6+§6.4/archived_from/amendable_by = 9 欄（對位 _inbox_archive.md 模式）。
- 內容：§6 諮詢紀錄 → §6.3 常見散戶問題清單（header+body）→ §6.4 觸發模板對位表 → §3.1 → §3.2,全部原文 verbatim（B6 10594B / H63 90B / B64 3177B / B63b 2033B / B31 5127B / B32 2543B 逐一 in-archive 驗證 True）。

### 3. README.md（5186 → 5354）
- Mission：「33 SK 頁、5 條鐵律」→「37 SK 檔（SK-00 索引 + 36 編號頁）、六條鐵律 + 第七條例外」。
- 目錄結構：「33 個 SK 知識頁(SK-00~SK-32)」→「37 個 SK 知識檔(SK-00~SK-36,SK-27/30 已 archive)」。
- 目錄結構補一行：`_consult-index_archive.md`（2026-08-22 audit-fix）。

### 4. index.md（5461 → 6173）
- 標頭：「Last updated: 2026-08-02 | ... / Repo .md 總數: 91 / SK 知識頁: 33」→「Last updated: 2026-08-22 | ... / Repo .md 總數: 154（2026-08-22 快照,find 實測）/ SK 知識檔: 37（36 編號 + 索引,SK-27/30 已 archive）」。
- Repo .md 總數 154 = 任務書指定 find 指令實測：`find . -name "*.md" -not -path "./.git/*" -not -name "*.bak*" | wc -l`。
- 新增 ## Skills 段（8/7-8/21 新增）：SK-33 audience-routing、SK-34 listed-otc-routing（8/15 真實 promotion,PR #21）、SK-35 mcp-failover、SK-36 sl-vs-rl（原 SK-31 renumber,PR #31）、SK-31 = AI 投資週期 2026 唯一對應;附 SK-00 索引頁。

### 5. log.md（41039 → 41558,append 不改歷史段）
- 檔尾新增「## 2026-08-07 ~ 2026-08-22 里程碑補登 [2026-08-22 audit-fix]」：SK-34 真實 promotion（PR #21,8/15）/ Plan F 護欄 Week 1-3（PR #32/#33）/ T9 任務清單 v1+v2（PR #28/#30）/ _inbox 歸檔（PR #29）/ SK-31→SK-36 renumber（PR #31）/ hermes-agent runtime patch 管理（PR #34/#35）/ 2026-08-22 金融審計 + audit-fix 批次（本 PR）,每條一行。

### 6. skills/SK-31-ai-investment-cycle-2026.md（8975 → 9021）
- 「13 trigger templates」→「20 trigger templates（2026-08-22 快照）」共 2 處（§1 一句話定位 + §3 標題,任務書指定都改）。

### 7. 審計衍生檔歸檔
- `mv skills/_methodology_alignment_audit_VERBATIM.md skills/_archive/`、`mv skills/_methodology_alignment_audit_with_fileline.md skills/_archive/`（原檔名保留,bytes 不變）。
- `skills/_methodology_alignment_audit.md` 文末加一行：衍生兩檔已移至 `skills/_archive/`（原檔名保留）[2026-08-22 audit-fix]。

## 三、驗收

- `_consult-index.md` = 8993B ≤ 9000B ✓（wc -c 驗證）。
- archive 內容完整：5 大搬出段逐段 verbatim 驗證 + 隨機抽 3 行比對原文皆命中 ✓。
- SK-31 = 9021B（見下,超 21B,需裁決）。
- frontmatter 9 欄維持 ✓。

## 四、偏離與待裁決

1. **SK-31 超限 21B（9021 > 9000）**：任務書動作 6 指定兩處「13 trigger templates」→「20 trigger templates（2026-08-22 快照）」都改（+46B）,原檔 8975B → 9021B 超 9000B 上限 21B。共同規範第 4 條「範圍外一字不改」禁止我自行在他處刪字補額。待官方裁決：(a) 接受 9021B（修 size-check 例外）或 (b) 授權精簡 SK-31 其他 ≥21B 內容。→ [待官方驗證/裁決]
2. **§6.3 一併歸檔**：任務書段位計量 §6.4=5227B（含 §6.3 body「預期查詢地圖」2033B）,故 §6.3 header+body 隨 §6.4 區段搬入 archive（主檔 §6.3 不再單獨出現,避免懸空標題）。§0 規則 5/6 仍指向 §6/§6.3,讀者可循 §6/§6.4 指標到 archive。
3. **孤兒字元 `)` 移除**（原 line 325,無配對,非段落內容;計入任務書 §6.4 5227B 區段但未搬入 archive）。
4. **README「5 條鐵律」其他出現處**（規範速查/貢獻段）不在任務書替換清單,未動。
5. **Repo .md 總數 154** 為實測值（含 _internal/ 審計檔與 .github/ 檔;2026-08-22 快照,與舊 91 之差即 8 月新增檔案）。
