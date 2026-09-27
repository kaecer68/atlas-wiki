# `_internal/_l3-backfill-recipe.md` — SK 頁 L3 端點實跑回填做法（v1,2026-09-27）

> **用途**:把「`status: active` 但從未跑過 L3」的 SK 頁,逐頁補上**可稽核的端點實測證據**。
> **背景**:2026-09-27 `make structure-metrics` 新增指標 8「L3 覆蓋率」,當時為 **3/37**（僅 SK-34/37/38),watch list 34 頁。本檔是逐頁補完的標準程序。
> **關係**:`skills/_method.md` 定義 L3 的**語意**（端點實跑證據）;本檔定義**操作**（怎麼跑、怎麼寫、跑失敗怎麼記）。

## 0. 前置（3 個常數,每次照抄）

| 項目 | 值 | 說明 |
|------|----|------|
| Base URL | `http://127.0.0.1:18080` | atlas-go HTTP（read-only GET） |
| Auth | `X-API-Key: <ATLAS_API_KEY>` | 讀 `~/.hermes/.env`;**不帶 key 回 401,會把 404 藏起來** |
| Timeout | `timeout=6` | 端點多為本地快取,今日實測 1–1700 ms |

時間戳一律用 **ISO-8601 帶 `+08:00`**（UTC+0800）,寫成 `2026-09-27T19:27:54+08:00`。只寫 `19:27` 或只寫日期都不合格（第五條鐵律:快照值需附時戳）。

## 1. 找出「這頁聲稱用了什麼」

依序讀 3 個地方,**三處都要看,常有不一致**:

1. frontmatter `mcp_tools_used:` — 工具白名單（例:SK-04 = `[backtest_signals, risk_get_metrics]`）。
2. frontmatter `verification:` — 歷史結算內文,常藏「當時實測到什麼數字」（例:SK-03「147 sessions」、SK-04「session_count=147」）。
3. 內文 §驗證方式 — 可重現步驟（Step 1/2/3）,這才是**要驗的 claim**。

同時記下:內文其他段落提到的工具也算（例:SK-01 正文引用 `stock_get_quote`、`industry_sector_lookup`,即使不在 `mcp_tools_used`）。

## 2. 工具 → HTTP 端點對映（SSOT）

**正本**:`~/workspace/atlas/cmd/atlas-mcp/server/tools_canary_test.go` 的 `canaryRoutes`（tool 名 → upstream path,含 canary 參數）。這是唯一權威對映,不要憑記憶猜路徑。

常用列（2026-09-27 核對）:

| MCP tool | upstream path |
|---|---|
| `stock_get_quote` | `/api/stock/quote?symbol=2330` |
| `stock_get_fundamentals` | `/api/stock/fundamentals?symbol=2330` |
| `stock_get_technical` | `/api/stock/technical?symbol=2330&days=10` |
| `stock_get_chips` | `/api/stock/chips?symbol=2330` |
| `industry_sector_lookup` | `/api/industry/sector-lookup?symbol=2330` |
| `data_get_field_contract` | `/api/field-contract` |
| `macro_get_snapshot_latest` | `/api/macro/snapshot/latest` |
| `macro_get_snapshot_history` | `/api/macro/snapshot/timeline` |
| `universe_get_sessions` | `/api/dashboard/sessions` |
| `universe_get_session_detail` | `/api/dashboard/sessions/{session_id}`（**canary 值 `.../latest` 是錯的,見下**） |
| `risk_get_metrics` | `/api/dashboard/risk` |
| `backtest_status` / `backtest_signals` | `/api/backtest/status` / `/api/backtest/signals` |
| `parameters_get` | `/api/parameters` |
| `event_calendar` | `/api/events/calendar` |
| — (IS/OOS 唯一出口) | `/api/dashboard/agent-observatory`（**只有這裡有 `is_sharpe`/`oos_sharpe`/`is_oos_ratio`/`overfit_warning`**;`/api/dashboard/risk` 沒有） |
| — (訊號層歸屬判斷) | `/api/strategies/layers`（L1–L5,2026-09-27 實測 12 筆） |
| — (detector 歸屬判斷) | `/api/detector/registry/list`（2026-09-27 實測 **29** themes,非文件寫的 24） |

**CLI 模型白名單（2026-09-27 實測,batch #2 補）**:`cmd/backtest-pipeline` 的 `-model` 只接受 `ols/pcr/pls/elasticnet/glm/rf`（`newModel()` 白名單,`xgboost` 會報錯）。**每個都能當模型層 L3 代理**,不只 `ols`。

### 三個必知陷阱

1. **`universe_get_session_detail` 的 canary 值 `/api/dashboard/sessions/latest` 回 404**（`{"error":"session not found","session_id":"latest"}`;SK-37 與本批同日各驗一次）。真實路徑是 `/api/dashboard/sessions/{session_id}`,id 從 `/api/dashboard/sessions` 取（如 `session-20260927-daily` → 200）。
2. **canary 沒有 ≠ 端點不存在**。`/api/backtest/snapshots` 不在 `canaryRoutes`、也沒有 MCP tool（`grep` `cmd/atlas-mcp` 0 命中）,但 **HTTP 200 可用**。反向亦然:有些工具沒有 HTTP 端點（見第 3 節）。
3. **本地快取端點會回 0 不代表壞掉**。`/api/stock/technical?symbol=2330&days=10` 今日 200 但 `rsi14/sma20/sma50` 皆 0;`/api/dashboard/risk` 今日 200 但 `sharpe_short/long`、`var_95` 皆 0。**記錄觀測值,不要推論成「壞」**。

**沒有 HTTP 端點時**（近例:`audit_state`、`mcp_roots_read_file` 為 local-only）:在 frontmatter 明寫「源碼級代理（無 HTTP 端點）」,改用最近的**可驗證代理**並註明其性質:
- CLI 實跑:`cd ~/workspace/atlas && go run ./cmd/backtest-pipeline -synthetic -model ols`（本批 SK-05 用,exit 0、`R²_OOS +0.9993`）。
- 源碼閱讀 + `grep`（例:SK-03 由 `internal/backtest/rolling_split.go` 與 `cmd/backtest-pipeline` 旗標證明三軸存在;SK-04 由 `internal/ml/elasticnet.go` 的 `UseHuber`/`Xi` 證明 Huber 實作存在但 0 呼叫者）。
- 完全不確定 → 標「unverifiable」,**不准編數字**（鐵律 2）。

## 3. 實跑（複製即可）

```python
import os, json, time, datetime, requests
env = dict(l.split('=',1) for l in open(os.path.expanduser('~/.hermes/.env')).read().splitlines()
           if l and not l.startswith('#') and '=' in l)
HDR = {'X-API-Key': env['ATLAS_API_KEY'].strip().strip('"')}
BASE = 'http://127.0.0.1:18080'
def probe(path):
    ts = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    try:
        r = requests.get(BASE+path, headers=HDR, timeout=6)
        code, body = r.status_code, r.text
    except Exception as e:
        code, body = 'ERR', repr(e)
    return code, body, ts.strftime('%Y-%m-%dT%H:%M:%S+08:00')
```

`ERR`（timeout / connection refused）也要照實寫進表格 —— 那正是 L3 要留下的證據。順手記錄**回傳規模**（欄數/序列數/筆數）,它是跨日比對的錨點。

## 4. 什麼算合格的 L3（四條全中才算）

1. frontmatter 同時有 `l3_run_at`（`YYYY-MM-DD`）、`l3_run_by`（人或 PR/branch）、`l3_endpoints_probed`（**今天真的跑過**的清單）。
   - 只寫 `l3_endpoints_probed` 而沒有今日實跑 = **不裝完成**,不可把 `status` 留 active 又宣稱 L3。
2. `l3_endpoints_probed` 每列 = `路徑 → http_code（UTC+0800 timestamp）`;非 200（404/401/500）照寫。
3. §驗證方式 有一段 `### L3 端點實跑（YYYY-MM-DD,本 PR）` 表格,欄位 = 端點 / http_code / 實測結果 / timestamp。
4. `verification:` 更新為**今日量到什麼**,並保留歷史結算（標明其日期為快照）。

## 5. 怎麼改頁面（含 9,000 B 上限）

> **batch #2 實證**:已有 audit-fix 口徑註 ＋ 再加 9 列證據表的頁**一定撞 9,000 B 上限**（SK-09 就是）。做法:先在同頁壓縮重複敘述（verification 段的歷史、散戶解讀的重述、對位段的冗語），**保留證據表**,再寫入 L3 區塊;壓完要 `wc -c` 確認。

- 插入位置:`verification:` 行之後、`methodology_aligned:` 之前（與 SK-34/37/38 一致）;§驗證方式 只**新增** `###` 小節（不算 canonical section,不觸發段序檢查）。
- **9,000 B 硬上限**:加 L3 區塊前先看頁面大小;接近上限就先壓縮重複敘述（同一事實只留一份）,不要為了塞證據刪掉未消化項。
  - 本批實例:SK-01 原本 8,989 B,已近上限 → 先把「逐字重複的 M1 計分敘述」「重複的 period_system tip 註解」壓掉,才放得下 L3 表（收在 8,979 B）。
- 「未消化」規則（schema `unconsumed_must_be_open`）:**已解項要移出**該段,把結論寫進 §驗證方式／`verification:`,不要就地打勾。已解但需留痕時,在清單下方以非 checkbox 一行記錄「已解（YYYY-MM-DD）…」。
  - 本批實例:SK-02「atlas 是否支援日頻 macro」→ `macro_get_snapshot_history` 實跑 200、30 天日頻 → 移出,結論寫進 §驗證方式;SK-03「是否可自訂 step_years」→ 源碼+旗標證明存在 → 移出,並原位更正 §atlas 對位 的錯誤敘述。

## 6. 當 claim 被實測推翻（這是 L3 的主要產出,不是意外）

1. **不刪歷史,只加更正**:在 §驗證方式 寫「**更正（YYYY-MM-DD）**」,指明原句錯在哪、今日量到什麼。
2. 快照型數字（session 數、序列數、PE/PB 等）一律在頁內補上**取樣時點**,避免下一個 session 誤用。
   - 本批實例:`universe_get_sessions` 從 147/150 → 今日 **90**（端點回滾動窗,不是壞掉）;`risk_get_metrics.session_count` 147 → **210**;`macro_get_snapshot_latest` 12/31 → **41** 條序列;2330 `PE 30.19/PB 9.57` 與 2026-07-30 逐字相同,但同日 `quote.last` 已由 2395→2475 → **fundamentals 是靜態快照**。
3. 若更正改變了對位結論（例:能力其實存在,只是不在 MCP/HTTP 面）,同步改 §atlas 對位 的對應句,並註日期。

## 7. 驗收（每次批次結束）

```bash
make ci-gate                                   # 7/7 green（commit 後才跑,gate 讀 git diff HEAD）
python3 skills/_scripts/audit-file-index-sync.py   # 0 unindexed
make structure-metrics                          # 前後對照 L3 覆蓋率與 watch list
```

`make structure-metrics` 的前後數字（`L3 覆蓋率 N/37`、watch list 大小）要原文貼進 PR body 與回報 —— 這是這項工作的唯一成效指標。

## 8. 批量與額度

- **一批 5 頁**是實測可用的大小:本批 5 頁共 7 個 HTTP 端點群 + 2 次 CLI/源碼代理,端到端約 20 分鐘（含改頁與驗收）,單頁平均 4 分鐘。
- 端點呼叫本身極便宜（本地、毫秒級）,**成本在改頁與壓 9,000 B**,所以批量的瓶頸是編輯,不是 probe。
- 進行中:`_self-audit.md` 記錄上一輪結算,`make structure-metrics` 給目前覆蓋率 → 下一批直接從 watch list 取 5 頁（建議按頁號順序,方便 P0 優先）。
- **紅線**:探測 repo 時只在 repo 內用 `git grep` 或 `grep -rn --include='*.md' . | head`;`~/.hermes` 有 50 GB,遞迴 grep 會拖垮 session（2026-09-27 已發生 3 次）。

## 9. 本批（batch #1,2026-09-27）實跑成果

| 頁 | 端點 | 今日結果 | 主要更正 |
|---|---|---|---|
| SK-01 | 8 | 全 200 | sessions 147→90;`factor_score` 欄位已移除;technical 指標全 0 |
| SK-02 | 5 | 全 200 | macro 序列 12→41;日頻 macro **待補項已解**;fundamentals 為靜態快照 |
| SK-03 | 8 + 源碼 | 7×200、`/sessions/latest` 404 | 三軸實作存在（不在 MCP/HTTP）;risk sharpe 皆 0 |
| SK-04 | 4 + 源碼 | 全 200 | 「Huber 加權 atlas 沒有」不成立（`internal/ml` 有,0 呼叫者）;signals 今日 null |
| SK-05 | 5 + CLI | 全 200;CLI exit 0 | atlas 原生 OLS `R²_OOS +0.9993`;4 端點皆無 R²_oos 欄位 |

覆蓋率:3/37 → 8/37（數字以 PR body 的 before/after 為準）。

## 9b. 本批（batch #2,2026-09-27,PR #92）實跑成果

| 頁 | 今日結果 | 主要更正 |
|---|---|---|
| SK-06 elastic-net | CLI `-model elasticnet` R²_OOS +0.6406 WARN（vs OLS +0.9992） | 「alpha 由 CV 自動選」在 CLI 路徑**不成立**（`AlphaAuto:false`,Alpha 固定 1.0） |
| SK-07 glm-spline | CLI `-model glm` +0.9992 | 「atlas 無 ML 訓練端點、100% client 端」**不成立**:原生 `internal/ml/spline.go`（truncated-power,degree 3,gaussian/poisson/gamma）在跑 |
| SK-08 pcr | CLI `-model pcr` +0.9993 | 原生 SVD PCR 存在（`internal/ml/pcr.go`,NComponents 預設 4）;L1–L5（12）與 detector（29）**與 PCA 訊號無重疊** |
| SK-09 pls | CLI `-model pls` +0.9993 | 原生 NIPALS PLS1 存在;**IS/OOS 只在 `/api/dashboard/agent-observatory`**,`risk_get_metrics` 完全沒有 R²/Sharpe |
| SK-10 random-forest | CLI `-model rf` +0.9914 | 原生 RF 預設 `NTrees=100 / MaxDepth=10`（與頁面「500 棵淺樹 depth=2」相反）;**無 `feature_importances_`**,重要性只能走 `PermutationImportance` |

覆蓋率:11/38 → **16/38（42.1%）**,watch list 27 → 22 頁。下一批建議序:SK-11、SK-12、SK-13、SK-14、SK-15。

## 10. 已知未解（下一批可接手）

- `universe_get_session_detail` 仍不回 train/valid/test 三段日期（SK-03 §未消化）。
- `/api/backtest/signals` 今日 `active_signals: null`,報酬序列無處可取;`/api/backtest/snapshots` 是替代,但只有 20 筆日快照、且無 MCP tool。
- `/api/dashboard/risk` **沒有 Sharpe 欄位**（2026-09-27 更正:payload keys 只有 `degraded/gate_mode/risk_snapshot/session_count/source/var_gate`;`risk_snapshot` = `var_95/var_99/cvar_95`（皆 0,且 `insufficient_data=1` ⇒ 0 是「資料不足」不是「零風險」）、`max_drawdown_pct`、`data_points`）。**以 Sharpe 為驗證步驟的頁一律改走 `/api/dashboard/agent-observatory`**;`var_95=0` 不可當零風險引用。（先前版本誤記「sharpe_short/long 皆 0」,已於 PR #89 更正）
- **🚧 CLI 真實資料路徑今日不可用（batch #2 新發現,影響所有要「真實 OOS R²」的頁）**:`internal/backtest/rolling_split.go:72` **硬編 `stopYear := 2020`**,而 repo 的 replay 檔 `data/replay/merged.csv` 覆蓋 **2024-07-01 → 2026-08-24**（22,956 列）⇒ 真實資料一律回 `no windows produced`;把 `-first-train-end` 移進迴圈則回 `has empty training data`。**結論:目前只能用 `-synthetic` 做「模型層」L3,不可當市場結論**;要解需 1994–2022 月頻 replay 檔,或把 `stopYear` 改成旗標（atlas-go 側,需拍板）。
- `/api/experiment/history` 今日回 `{"history":[]}`、`/api/experiment/diff` 未知 id → 404 ⇒ **實驗 diff 目前不能當證據路徑**。
- `cmd/atlas-mcp/server/tools_template_detector.go:19` 的 tool 描述仍寫「All **24** template trigger detectors」,而 live registry 回 **29** ⇒ 引用數目時**以 registry 為準**,勿抄文件字串（atlas-go 側待修）。
