# Atlas Wiki — 散戶 AI 實戰金融工程知識引擎

[![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)](https://github.com/kaecer68/atlas-wiki/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI: validate-wiki](https://img.shields.io/badge/CI-validate--wiki-brightgreen.svg)](.github/workflows/validate-wiki.yml)
[![Public](https://img.shields.io/badge/visibility-public-lightgrey.svg)](https://github.com/kaecer68/atlas-wiki)

> **Mission**:散戶 AI 實戰金融工程。找信息差、找漏洞、找大型機構不會幹的落差。悶聲賺錢。

 ## Mission

atlas-wiki = 提煉成品知識層。`atlas-notes`(原料庫)→ atlas-wiki(知識引擎)流水線的輸出端。37 SK 檔（SK-00 索引 + 36 編號頁）、六條鐵律 + 第七條例外、CI 自動驗證一條龍。

## 目錄結構

```
atlas-wiki/
├── README.md              # 本檔
├── AGENTS.md              # 專案 context(操作必讀)
├── SCHEMA.md              # 知識結構 schema
├── index.md / log.md      # 知識索引 / 演進日誌
├── skills/                # 39 個 SK 知識檔(SK-00~SK-38;SK-27/30 已 archive)
│   ├── _method.md         # 寫入規範(六條鐵律 + 格式)
│   ├── _consult-index.md  # 跨頁查詢索引
│   ├── _consult-index_archive.md  # 諮詢索引歷史段歸檔(2026-08-22 audit-fix)
│   ├── _inbox.md          # 跨 SK 待辦
│   ├── _index-finskills.md
│   ├── _methodology_alignment_audit.md  # 對位憲章審計
│   └── _scripts/          # 驗證工具 14 檔(Python;逐一用途見 §CI 表)
├── templates/
│   ├── audit-report.md    # 審計報告模板
│   └── trigger-*.md       # 21 檔觸發模板(2026-09-27 實測,§12)
├── concepts/              # 台股市場概念 / 領域模型
├── entities/              # L1 宏觀實體研究
├── summaries/             # 階段總結(分工藍圖)＋ HTTP path drift 記錄
├── _internal/            # 內部設計/維運紀錄(索引見其 README.md)
├── _archive/             # append-only 歷史(月切日誌 log-YYYY-MM.md)
└── .github/workflows/
    └── validate-wiki.yml  # CI(9 jobs:8 驗證 + Telegram 通知;2026-09-27 實測)
```

## 規範速查(詳見 `skills/_method.md`)

- 單頁大小 **依類別**(2026-09-27 kaecer 拍板,取代「所有 .md ≤ 9,000」):SK 頁/入口檔 ≤ 9,000、`concepts/**`+`entities/**` ≤ 30,000、`docs/**` ≤ 12,000、append-only(log/_self-audit/_inbox/_archive)無硬上限但需分流歸檔、`_internal/**` 無硬上限但結案即瘦身(表見 `_method.md` 六條鐵律 6)
- frontmatter 核心欄位:title / type / source / ingested_at / status / tier / confidence / atlas_go_relevance / mcp_tools_used / verification
- 六條鐵律(2026-09-27 校正:原記 5 條;正本 `_method.md` §六條鐵律):① 不搬運,翻譯 ② 不瞎寫 ③ 不裝完成 ④ 不違背憲章 ⑤ 派工備份 ⑥ size **依類別**(SK 頁 9,000 / 參考 `concepts`+`entities` 30,000 / `docs` 12,000 / append-only＋`_internal` 無硬上限)
- 另見 `_method.md` §第五條鐵律(快照值必附 timestamp)+ §第六條鐵律(外部權威報告週期稽核)
- 每日 quota:D1 示範 1 頁 → D2+ 每日 3 頁上限(2026-07-29 降標)

## Repo 邊界(不進 git)

| 項目 | 理由 |
|------|------|
| `*.bak*` 備份檔 | 第 5 條 SOP 備份,不入 git(由 .gitignore 排除) |
| `skills/_self-audit.md` | 審計日誌,跨 session 累積,屬 atlas-notes governance-log 一類 |
| `atlas-notes/` 原料庫 | 獨立治理,不在此 repo |

## CI

push / PR 到 `main` 觸發 `validate-wiki`（2026-09-27 實測 9 個 job:8 個驗證 + 1 個失敗通知）：

1. **validate-timestamp-rule** — 第 5 條鐵律(快照值必附 timestamp)
2. **audit-atlas-endpoints** — 掃描 atlas-mcp 端點(2026-09-27 實測 **115** 端點;舊記 109。對位 `kaecer68/atlas-go`)
3. **skill-structure-check** — SK 頁段名/段序/禁用標記(SSOT `skill-page-schema.json`)
4. **size-check** — SK 頁 ≤ 9,000 bytes（`_inbox.md` > 12,000 僅警告;類別表見 `_method.md` 六條鐵律 6）
5. **frontmatter-check** — frontmatter 核心 10 欄齊全
6. **audit-file-index-sync** — SK/concepts/entities/triggers/scripts 索引同步
7. **trigger-template-existence** — 12 核心觸發模板存在 + 結構關鍵字
8. **trigger-endpoint-validation** — 12 核心觸發模板對位 atlas 端點
9. **notify-telegram** — 任一 job 失敗才跑（`if: failure()`）

### 本地驗證腳本（`skills/_scripts/`;2026-09-27 實測 14 檔 `*.py`）

| 腳本 | 用途(取自該檔 docstring) |
|------|--------------------------|
| `validate-timestamp-rule.py` | 第 5 條鐵律 enforcement(快照值 timestamp) |
| `audit-atlas-endpoints.py` | atlas-mcp 端點 audit + 抓 Description |
| `check-skill-pages.py` | 一次跑 SK 頁 size + frontmatter |
| `check-skill-structure.py` | SK 頁結構守衛(反補丁 M2/M2′) |
| `check-stale-worktree.py` | skills/ 未提交內容偵測(反補丁 M5) |
| `check-retrieval-integrity.py` | 檢索性完整性 S5(載入條件/索引/入口可達性;warn) |
| `check-skill-index-sync.py` | 強制 skills 建立/修改時索引同步更新 |
| `new-skill-page.py` | SK 頁骨架產生器(反補丁 M6) |
| `structure-health-metrics.py` | 結構健康度量測(M7;含指標 8 = L3 覆蓋率＋watch list,非門檻) |
| `audit-file-index-sync.py` | 驗證 wiki 內落檔是否被索引引用 |
| `atlas-mcp-trigger-monitor.py` | 觸發模板自動信號捕捉(每 5 分鐘) |
| `handle-atlas-failures.py` | atlas-mcp 端點失敗降級處理 |
| `atlas-failures-telegram-report.py` | 每日 atlas 端點健康檢查 + Telegram |
| `cron-health-monitor.py` | cron job 健康監控 |
| `_A977_ground_truth.py` | A977 ground truth 檢查(importlib 雙副本 + curl) |

 任一失敗 → **Telegram 通知**。需在 GitHub repo Settings → Secrets and variables 設定：

 - `TELEGRAM_BOT_TOKEN`(來源 `~/.hermes/.env`)
 - `TELEGRAM_CHAT_ID`(可選,預設 `8387647295`)

## 版本

[v1.0.0](https://github.com/kaecer68/atlas-wiki/releases/tag/v1.0.0)(2026-08-03)— 首發版。33 SK 頁 + 9 索引 + CI validate-wiki(首發當時 4 檢查 + Telegram 通知)+ audit 模板。

版本紀律遵循 semver:
- **MAJOR**:憲章對位/鐵律變更(對位憲章 §1)
- **MINOR**:新增 SK 頁或索引章節
- **PATCH**:錯字修正、連結修補、frontmatter 補欄

## 許可證

[MIT License](LICENSE)— Copyright (c) 2026 Kaecer Chan。

可自由使用、修改、散布、商業利用,僅需保留著作權聲明。

> **聲明**:本 wiki 內容僅為學術與教學用途,不構成任何投資建議。投資有風險,決策責任自負。詳見 `skills/_method.md` 與憲章 `~/workspace/atlas/docs/ATLAS_METHODOLOGY.md`。

## 12 觸發模板自動化(2026-08-03 v6.18)

atlas-wiki v6.18 含 **12 觸發模板** 落 `templates/` = 自動信號捕捉系統(對位 ATLAS 憲章 7 層因果鏈 + 12 strategy):
- trigger-nvda-tsm / trigger-usd-twd-32 / trigger-dxy-us10y-weak / trigger-margin-350b
- trigger-foreign-3day-inflow / trigger-sox-foreignflow / trigger-taiwan-strait-tension
- trigger-china-slowdown / trigger-tariff-shock / trigger-etf-rebalance
- trigger-cb-fx-intervention / trigger-retail-margin-decrease

跑 `atlas-mcp-trigger-monitor.py` 每 5 分鐘觸發 1 次 + 自動 §6 紀錄 + Telegram 通知。

**現況(2026-09-27 實測)**:`ls templates/trigger-*.md | wc -l` = **21**(templates/ 共 22 檔,含 `audit-report.md`)。v6.18 之後新增 9 檔(名稱取自各檔 H1):

- `trigger-2330-tsmc-swing` — 2330 台積電報價觸發(盤中振幅逾 ±3%)
- `trigger-ai-capex-guidance-cut` — AI capex 指引下修(對位 2026 韓股 HBM 降溫)
- `trigger-cb-emergency-intervention` — 央行緊急干預匯市(1997 IMF + 2022 BOK)
- `trigger-equipment-capex-external-report-cycle` — 設備 capex 外部報告週期(年/半年)
- `trigger-hbm-cycle-cooling` — HBM/AI 敘事降溫(對位 2026 韓股崩盤)
- `trigger-hedge-fund-unwind` — 對沖基金集中持倉爆倉(對位 2021 Archegos)
- `trigger-megaproject-2-quarter-lag` — 巨型專案 2 季落後(訂單時序)
- `trigger-msci-rebalance-pressure` — MSCI 季度再平衡壓力(被動 ETF 增減持)
- `trigger-renewable-energy-divergence` — 綠能發電 vs 電網/重電雙臂分歧(第 16 模板,月頻+日頻雙確認)

## 貢獻

以 PR 形式提交至 `main` 分支。CI 會自動跑 8 項驗證(共 9 jobs);需遵守 `skills/_method.md` 六條鐵律(尤其快照值必附 timestamp,見該檔 §第五條鐵律)。貢獻前請閱讀:

1. `AGENTS.md`(專案 context)
2. `skills/_method.md`(寫入規範)
3. `skills/_index-finskills.md`(來源映射)

## 相關連結

- 上游:`atlas-notes/`(原料庫,未公開)
- 對位:`kaecer68/atlas-go`(atlas-mcp 端點來源)
- 憲章:`~/workspace/atlas/docs/ATLAS_METHODOLOGY.md` v1.0
