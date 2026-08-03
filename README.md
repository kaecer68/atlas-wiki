# Atlas Wiki — 散戶 AI 實戰金融工程知識引擎

[![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)](https://github.com/kaecer68/atlas-wiki/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI: validate-wiki](https://img.shields.io/badge/CI-validate--wiki-brightgreen.svg)](.github/workflows/validate-wiki.yml)
[![Public](https://img.shields.io/badge/visibility-public-lightgrey.svg)](https://github.com/kaecer68/atlas-wiki)

> **Mission**:散戶 AI 實戰金融工程。找信息差、找漏洞、找大型機構不會幹的落差。悶聲賺錢。

 ## Mission

atlas-wiki = 提煉成品知識層。`atlas-notes`(原料庫)→ atlas-wiki(知識引擎)流水線的輸出端。33 SK 頁、5 條鐵律、CI 自動驗證一條龍。

## 目錄結構

```
atlas-wiki/
├── README.md              # 本檔
├── AGENTS.md              # 專案 context(操作必讀)
├── SCHEMA.md              # 知識結構 schema
├── index.md / log.md      # 知識索引 / 演進日誌
├── skills/                # 33 個 SK 知識頁(SK-00~SK-32)
│   ├── _method.md         # 寫入規範(5 條鐵律 + 格式)
│   ├── _consult-index.md  # 跨頁查詢索引
│   ├── _inbox.md          # 跨 SK 待辦
│   ├── _index-finskills.md
│   ├── _methodology_alignment_audit.md  # 對位憲章審計
│   └── _scripts/          # 驗證工具(Python)
│       ├── validate-timestamp-rule.py   # 第 5 條鐵律 enforcement
│       └── audit-atlas-endpoints.py     # atlas-mcp 端點 audit
├── templates/
│   └── audit-report.md    # 審計報告模板
├── concepts/              # 台股市場概念 / 領域模型
├── entities/              # L1 宏觀實體研究
├── queries/               # 研究盤查記錄
├── comparisons/           # 框架比較
├── summaries/             # 階段總結
└── .github/workflows/
    └── validate-wiki.yml  # CI(四項檢查 + Telegram 通知)
```

## 規範速查(詳見 `skills/_method.md`)

- 單頁大小 ≤ 9,000 bytes(2026-07-30 kaecer 拍板 bump 自 6000)
- frontmatter 核心欄位:title / type / source / ingested_at / status / tier / confidence / atlas_go_relevance / mcp_tools_used / verification
- 5 條鐵律:① 不搬運,翻譯 ② 不瞎寫 ③ 不裝完成 ④ 不違背憲章 ⑤ 快照值必附 timestamp
- 每日 quota:D1 示範 1 頁 → D2+ 每日 3 頁上限(2026-07-29 降標)

## Repo 邊界(不進 git)

| 項目 | 理由 |
|------|------|
| `*.bak*` 備份檔 | 第 5 條 SOP 備份,不入 git(由 .gitignore 排除) |
| `skills/_self-audit.md` | 審計日誌,跨 session 累積,屬 atlas-notes governance-log 一類 |
| `atlas-notes/` 原料庫 | 獨立治理,不在此 repo |

## CI

push / PR 到 `main` 觸發 `validate-wiki`：

1. **validate-timestamp-rule** — 第 5 條鐵律(快照值必附 timestamp)
2. **audit-atlas-endpoints** — 掃描 atlas-mcp 109 端點(對位 `kaecer68/atlas-go`)
3. **size-check** — 每頁 ≤ 9,000 bytes
4. **frontmatter-check** — frontmatter 核心欄位齊全

 任一失敗 → **Telegram 通知**。需在 GitHub repo Settings → Secrets and variables 設定：

 - `TELEGRAM_BOT_TOKEN`(來源 `~/.hermes/.env`)
 - `TELEGRAM_CHAT_ID`(可選,預設 `8387647295`)

## 版本

[v1.0.0](https://github.com/kaecer68/atlas-wiki/releases/tag/v1.0.0)(2026-08-03)— 首發版。33 SK 頁 + 9 索引 + CI validate-wiki(4 檢查 + Telegram 通知)+ audit 模板。

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

## 貢獻

以 PR 形式提交至 `main` 分支。CI 會自動跑 4 項檢查;需遵守 `skills/_method.md` 5 條鐵律(尤其第 5 條:快照值必附 timestamp)。貢獻前請閱讀:

1. `AGENTS.md`(專案 context)
2. `skills/_method.md`(寫入規範)
3. `skills/_index-finskills.md`(來源映射)

## 相關連結

- 上游:`atlas-notes/`(原料庫,未公開)
- 對位:`kaecer68/atlas-go`(atlas-mcp 端點來源)
- 憲章:`~/workspace/atlas/docs/ATLAS_METHODOLOGY.md` v1.0
