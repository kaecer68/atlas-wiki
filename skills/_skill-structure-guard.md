---
title: SK 結構守衛與反補丁機制（配套文件）
type: guard-doc
status: active
created: 2026-09-18
created_by: kaecer 2026-09-18 拍板（反補丁機制 M1-M6）
used_by: skills/_method.md 第九條 / Makefile ci-gate / validate-wiki.yml
amendable_by: kaecer
---

# SK 結構守衛與反補丁機制

> 本檔是 `_method.md` 第九條的**配套細節**（第九條先前版本把細節內嵌，使 `_method.md` 超出自身 9000 bytes 上限——依本 repo「規範本體瘦身、細節移附錄」既有模式拆出）。

## 為什麼（2026-09-06 事故根因）

| 缺口 | 具體 |
|---|---|
| 標準無機器可讀 SSOT | 6 段標準名只存在於散文與 cron 的臨時 grep → 檢查器只能檢查「有沒有標題」 |
| 補丁比正解省力 | 檢查失敗時「加別名空殼段」比「正名重構」容易 → cron 選擇補丁（SK-22 +923／SK-31 +956 bytes） |
| 無髒檔偵測 | 補丁躺在工作區 **12 天**未經審查 → 兩頁撞 9000 bytes 上限卻沒人處理 |

## 機制組成

| # | 元件 | 位置 | 行為 |
|---|---|---|---|
| M1 | **標準 SSOT** | `skills/_scripts/skill-page-schema.json` | 6 段標準名＋段序＋補充段上限＋frontmatter 必要欄＋**禁用標記**；所有守衛與 cron 一律讀它 |
| M2 | **結構守衛** | `skills/_scripts/check-skill-structure.py`（`make check-skill-structure`、`ci-gate`、CI job） | 硬規則：段名正規化比對（去吃 `§N`／`[INTERNAL]`／括號）、**段序**、**重複標準段**、缺段、禁用標記；warn：未消化含已結項、補充段過多、超 size |
| M2′ | **最小重構處方** | 同上（失敗時的輸出） | 直接印 rename／刪重複段／重排／歸屬指示，讓**正解比補丁省力** |
| M6 | **骨架產生器** | `skills/_scripts/new-skill-page.py` | 輸出合規骨架（段名段序取自 schema），手寫段名不再是必要風險 |
| M5 | **未提交偵測** | `skills/_scripts/check-stale-worktree.py`（`make check-stale`） | `skills/` 未提交內容 > `--hours`（預設 48）告警 |
| M4 | **歸屬判斷強制化** | `.github/pull_request_template.md` | 「內容歸屬判斷」必填區塊（引用 `_manifest_coverage_routing.md §3.2`） |
| M7 | **量測** | `skills/_scripts/structure-health-metrics.py`（`make structure-metrics`） | 指標：結構守衛通過率、補丁標記數（目標 0）、未消化已結項數、髒檔時長 |

## 禁用標記（schema 為準）

別名補丁段（`alias →`）、cron 補強段（`補強備註`）、壓縮補丁標籤（`（壓縮版）`）、非標準段名前綴（`## [INTERNAL]`）、
行號指路（`L` + ≥2 位數字；`L1-L3` 為備援層級術語，**不在此列**——2026-09-18 實測修正的假陽性）。

## 用法

```bash
make check-skill-structure          # 結構自查（失敗附最小重構處方）
make check-skill-pages              # size ≤ 9000 + frontmatter
make check-stale                    # skills/ 未提交內容偵測（session 開頭建議跑）
python3 skills/_scripts/new-skill-page.py --id SK-37 --title "..."   # 產生合規骨架
```

## 與其他規範的關係

- `_method.md` 第九條＝**規則**（禁空殼補丁／歸屬判斷／最小重構／收尾義務）
- 本檔＝**機械配套**（SSOT、守衛、處方、產生器、偵測、PR 模板、量測）
- `_manifest_coverage_routing.md §3.2`＝**歸屬判準表**（哪一層寫什麼、不寫什麼）

## CI 觸發條件（2026-09-18 實測）

`validate-wiki.yml` 只在 **`push → main`** 與 **`pull_request → main`** 觸發——stacked PR（base 指向功能分支）**不會**跑 CI；把 base 改成 main 也**不會**重跑（`edited` 不在預設事件內），需再推一次 commit。

## M7 結構健康度基線（2026-09-18，納入結算）

`make structure-metrics` 輸出可直接貼進結算的 Markdown 區塊（`--json` 供程式消費）。基線（37 頁）：結構硬違規 **0**、禁用標記 **0**、超 size **0**、frontmatter 缺欄 **0**、未提交 **0 檔 >48h**；唯一非零＝**未消化含已結項 16 項（跨 7 頁）** → 判定 **DRIFT**（warn 級；依第九條於下次動到該頁時收斂）。

## strict 已開啟（2026-09-18）

16 項「未消化含已結項」結清後，schema 將 `unconsumed_must_be_open` 由 warn 升為 **hard**：
新增 `[x]` 於「未消化」= 硬違規（附最小重構處方）。驗證方式：臨時注入假項 → 守衛立即擋下；移除後全綠。
同批清理內容：13 項過程紀錄刪除、2 項誤標完成的真未結問題改回 `[ ]`、4 項耐久事實折入各頁 `驗證方式`。
