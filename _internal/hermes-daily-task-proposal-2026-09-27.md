# hermes 每日任務設定變更提案（2026-09-27，**待 kaecer 拍板**）

> 依據：2026-09-27 唯讀審計 `/tmp/aw-audit/hermes-tasks.md`（35 KB，逐條附證據）＋ 同日 48+ PR 的實證。
> **本檔只是提案與可貼用的 diff；尚未套用任何變更。** 任何 cron／prompt 修改都屬生產變更。

## 0. 為什麼要改（一句話）

**現行 cron 是「體積機器」，不是「品質機器」。** 實證：
- `atlas-wiki` git：**8/27–9/26 零 commit**，9/27 一天 42 commit ⇒ 真正提升品質的是**互動 PR session**，cron 一個字都沒寫進 wiki。
- `atlas-notes-pulse`（`5f4ebd3bc322`，每 30 分）：27 天 **1,270 次 / 8.16 億 prompt tokens**，產 1,188 份 market-pulse；最近 202 條中 101 條含「持平」、63 條明寫「未修改 atlas-wiki」；抽樣 macro 表 **24/24 列 Δ=0**。
- `atlas-skill-inbound`（`5ffe485d18c4`，02:30）：主任務**已飽和**（我實跑同一條 grep ⇒ **40/40 頁 6 段齊全、0 缺口**）；次任務來源 `~/workspace/Fin-Skills` **不存在** ⇒ 兩個任務都死。
- `knowledge-harvest-cycle`（`a794ca7881ca`）：**W=0 連續 6 週期**（每次仍產 20–40 KB 報告）。
- **14 個 job 中 0 個是「品質／精煉」任務**；8 個 cron 的 verification **全是格式 gate**（wc -c／條數／md5 自比），沒有一個是「宣稱 vs atlas backend 實測」。
- 副作用：`atlas-notes` 7.1 GB，其中 **6.7 GB 是 `.bak*` 副本**（源於 prompt 的「append 前整檔備份」SOP）。

## 1. 優先序（建議照序套用，可分批）

| # | Job（id／profile） | 現況 | 建議變更 | 風險 |
|---|---|---|---|---|
| **P1** | `5f4ebd3bc322` cio `*/30` | 每 30 分寫 1 份 market-pulse（多數 Δ=0） | **沉默為預設**：只在**實質變更**（任一 macro 序列 Δ≠0、或觸發門檻跨越）才寫檔；**每日最多 1 份合併檔**；刪除 LLM 自述 md5 | 低（少寫檔，不影響下游） |
| **P2** | `5ffe485d18c4` cio `02:30` | 主任務＝補 SK 六段（已 100%）、次任務＝Fin-Skills（來源不存在） | 改為 **evidence gap filling**：讀 `skills/_inbox.md`＋`[待驗]`＋`l3_run_at` 過舊頁，**每日最多關 1 項且必須真跑端點**；無缺口 → `[SILENT]`；**移除 Fin-Skills 次任務** | 中（改變產出型態；需觀察 1 週） |
| **P3** | 新增 job（建議 cio，週一次） | 目前**沒有**任何品質／精煉任務 | 新增 **atlas-wiki refinement pass**：每次最多 **3 個 refinement diff**（表達／結構／檢索性），走 PR ＋ `make ci-gate`（9 道）＋ wiki-critic；**不得新增頁面** | 低（有 gate 擋） |
| **P4** | `a794ca7881ca` cio `0 1 */3 * *` | W=0 仍每 3 天產報告 | 加**斷路器**：連續 W=0 ≥3 → `[ESCALATE]` 並暫停；把「refine 既有頁」列為一等結果 | 低 |
| P5 | `d9c20cfc295a`(06:00)、`90244488110a`(06:30) | 產研究報告，落到 notes | 換輸出契約：1 頁變更表 ＋ **每天最多 1 個 patch proposal**（收回「直接改 SK／AGENTS.md」的無界寫入權） | 中 |
| P6 | `6be1e9d33749`(週六 lint 解讀) | 解讀清單落 bot-chat | 清單必須落 `_inbox.md`（含根因＋期限），避免 dead drop | 低 |
| P7 | `d13f2b439274`(06:45 自驗收提醒) | 自述 schedule 對位錯誤 25 天、鏡子檔 §2/§3 失同步 | 修 schedule 文字、移除寫死清單、給 `_self-audit.md` §3 同步權 | 低 |

## 2. 共通護欄（建議寫進每個 prompt 的開頭）

1. **沉默＝成功**：沒有實質變更就 `[SILENT]`，不要為了產出而產出。
2. **每日體積預算**：單一 job 每日寫入 ≤1 份新檔／≤1 個 § 修補。
3. **證據優先**：任何數字要附來源或實測（`http_code` ＋ `+08:00` 時戳）。
4. **對準缺口**：動工前先讀 `~/.agents/skills/atlas-wiki-quality/SKILL.md`（缺口 G1–G7 ＋ 品質標準 S1–S8 ＋ 禁用主張）。
5. **不得自我指涉 KPI**：禁止以「滿足檢查器」為目標（第九條①）。

## 3. 套用方式（拍板後才執行；每步皆可回滾）

```bash
# 1) 先備份
cp ~/.hermes/profiles/cio/cron/jobs.json ~/.hermes/backups/$(date +%Y%m%dT%H%M)-cron-before-task-rework.json
# 2) 用 hermes 自己的 CLI 改 prompt（不要手改 JSON）
hermes -p cio --accept-hooks cron edit <job_id> --prompt "$(cat /tmp/new_prompt_<job>.txt)"
# 3) 驗證：JSON 可解析、job 數不變、只改 prompt 欄位
python3 -c "import json,os;d=json.load(open(os.path.expanduser('~/.hermes/profiles/cio/cron/jobs.json')));print(len(d['jobs']))"
```

## 4. 驗收（套用後 1 週觀察）

- `atlas-wiki` 出現**由 cron 產生**的 refinement PR（P3），且每個都過 9 道 gate。
- pulse 的每日寫檔數由 41–48 降到 ≤1；`[SILENT]` 成為常態。
- skill-inbound 不再產「0/3 段」空轉報告；有缺口時能在同日關閉 1 項並附實測。
- harvest 的 W=0 連續 ≥3 時出現 `[ESCALATE]`。

## 5. 不在本提案內（需另外拍板）

- **branch protection `required_status_checks`**（CI 紅目前不擋 merge）。
- **備份 SOP 改 hash-chain ＋ 保留政策**（會刪既有 `.bak`，屬資料處置）。
- **lint 工具後續**：`wiki-friday-lint.py` 的 `TYPE_DIRS`／索引歸屬／只當目標檔案已於 2026-09-27 修好；再修其他檢查（如 `TYPE_DIRS` 擴及 `skills/_*.md`）會一次浮出歷史問題，需搭配修復排程。
