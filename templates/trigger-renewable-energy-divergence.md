---
description: 綠能雙臂（電網 × 發電）月營收 YoY 差距 >15pp 且相對強弱差距 >5pp、同月同向成立時載入本模板。
template_id: trigger-renewable-energy-divergence
template_number: 16
type: dual-arm-divergence-trigger(月頻營收 × 日頻相對強弱 雙確認)
cadence: monthly(月營收 YoY) + daily(close/sma20);兩臂分歧需**同向且同月**成立才觸發
detector_theme: null
detector_note: atlas 端**不存在**再生能源 detector;嚴禁臆造 detector id(見 §3)
atlas_mcp_tools: [stock_get_monthly_revenue, stock_get_technical, stock_get_quote, stock_get_chips, macro_get_snapshot_latest, detector_registry_list, industry_sector_list, narrative_get_chains]
arms:
  grid_power: ["1513", "1519", "1503", "1514"]
  renewable_gen: ["3576", "6477", "9958", "6244", "3691"]
thresholds:
  arm_gap_revenue_yoy_pp: 15.0
  arm_gap_relstrength_pp: 5.0
l3_run_at: 2026-09-27
l3_run_by: hermes-agent (branch feat/20260927-template-16-renewable)
l3_result: 未觸發(雙條件未同時成立)— 非失敗,見 §4 結構性誠實
l3_endpoints_probed:
  - /api/detector/registry/list → 200 (2026-09-27 19:29:51)
  - /api/detector/scan/status?limit=200 → 200 (2026-09-27 19:29:51)
  - /api/industry/sectors → 200 (2026-09-27 19:29:51)
  - /api/dashboard/industry-classification → 200 (2026-09-27 19:29:51)
  - /api/stock/monthly_revenue?symbol=1513 → 200 (2026-09-27 19:29:51)
  - /api/stock/monthly_revenue?symbol=3576 → 200 (2026-09-27 19:29:51)
  - /api/stock/technical?symbol=1513&days=30 → 200 (2026-09-27 19:29:51)
  - /api/stock/technical?symbol=6244&days=30 → 200 (2026-09-27 19:29:51)
---

# atlas-mcp Trigger Template #16 — trigger-renewable-energy-divergence

> 快照紀律(第五條鐵律):本檔所有數字皆附來源與時間戳,取自 **2026-09-27 19:27–19:30** 對 `http://127.0.0.1:18080` 的真實 GET(帶 `X-API-Key`)。

**對位**:B 階段 kaecer 拍板「+ 第 16 template」+ SK-31 §未消化最後一條(第 16 template 待產)
**對位文獻**:UNCTAD WIR 2026 Chapter I/III(figure III.1)+ Stanford HAI 2026 AI Index Chapter 4
**對位檔案**:`~/workspace/atlas-notes/12-ext-research/2026-un-harvard-ai-investment/README.md` §2.1(數字表)
**對位 ATLAS_METHODOLOGY.md** §二 因果傳導鏈 第 1 層(全球資本配置)→ 第 2 層(台灣產業營收)
**立此日期**:2026-09-27

---

## §1 觸發條件(雙臂分歧,雙條件同向才觸發)

**Compare: gt(絕對值)** — 顯式聲明;方向由兩臂誰強決定,不預設多空。

| # | 條件 | 門檻 | 端點 | 資料源 | 頻率 |
|---|------|------|------|--------|------|
| C1 | `gap_rev = mean(YoY[綠能發電臂]) − mean(YoY[電網/重電臂])` | **≥ +15.0 pp 或 ≤ −15.0 pp** | `/api/stock/monthly_revenue` | finmind 月營收 | 月頻(每月 10 日後) |
| C2 | `gap_rs = mean(close/sma20−1[綠能發電臂]) − mean(同值[電網/重電臂])` | **≥ +5.0 pp 或 ≤ −5.0 pp** | `/api/stock/technical?days=30` | 日線收盤 | 日頻(收盤後) |

**觸發規則**:C1 與 C2 **同向**且同一個月內同時成立 → 觸發。任一不成立 → **不觸發**(結構性誠實,不補造)。

- `grid_power`(電網/重電 — AI 用電受益端):1513 中興電、1519 華城、1503 士電、1514 亞力
- `renewable_gen`(再生能源發電 — 資本排擠端):3576 元晶、6477 安集、9958 世紀鋼(離岸風電鋼構)、6244 茂迪、3691 碩禾

## §2 閾值依據(每個數字都可回溯)

| 門檻 | 依據 | 實測值(2026-09-27) |
|------|------|--------------------|
| C1 = **15.0 pp** | = 1.55 × 「電網/重電臂組內 YoY 標準差」9.68 pp(2026-08 月營收,4 檔實測)。設計意圖:兩臂差距須**超過自身組內雜訊**才視為結構性 | `gap_rev = +41.86 pp` → **C1 成立** |
| C2 = **5.0 pp** | = 2.71 × 「電網/重電臂組內相對強弱標準差」1.84 pp(2026-09-24 收盤 4 檔實測)。意圖:日頻臂差距須 **> 2.7σ** | `gap_rs = +3.27 pp` → **C2 不成立** |

**實測原始值(2026-08 月營收 YoY,`/api/stock/monthly_revenue`)**:
電網/重電 1513 **+3.83**、1519 **−8.32**、1503 **+15.10**、1514 **+6.51** → mean **+4.28**、σ **9.68**;
綠能發電 3576 **+72.75**、6477 **−26.89**、9958 **+91.16**、6244 **+27.12**、3691 **+66.54** → mean **+46.14**、σ **47.03**;
對照(半導體/NVIDIA 鏈)2330 **+44.69**、3680 **+71.69**、5434 **+42.61**、3533 **+18.60** → mean **+44.40**。

**實測相對強弱(2026-09-24 收盤,`/api/stock/technical?days=30`)**:
1513 +0.47pp(166 / sma20 165.23)、1519 −3.20pp(699 / 722.1)、1503 −2.63pp(196 / 201.3)、1514 +0.01pp(102 / 101.99) → mean **−1.34**、σ **1.84**;
3576 +6.54pp(18.25 / 17.13)、6477 −2.13pp(34 / 34.74)、9958 +1.40pp(92.2 / 90.93) → mean **+1.93**、σ **4.36**。

**先驗錨點(半年才更新一次,非 cron 掃描項)**:UNCTAD WIR 2026 — 開發中經濟體 renewable energy greenfield **$109B(2024)→ $55B(2025)= −50%**,同年半導體 greenfield 新案 **+35% YoY**(5 年 CAGR **+54%/年**);全球 telco(以資料中心為主)投資**首次超越**再生能源(來源:`2026-un-harvard-ai-investment/README.md` §2.1)。

## §3 對位 atlas 端:detector 不存在(誠實標,不臆造 id)

**2026-09-27 實測結論:atlas 端沒有任何再生能源 detector,也沒有再生能源 sector 桶。**

| 檢查 | 端點 | http_code | 實測結果 |
|------|------|-----------|----------|
| detector 註冊表 | `/api/detector/registry/list` | 200 | **29 個 theme**(`AI_capex_surge` 在內),**無** renewable/solar/wind/energy-transition |
| detector 掃描史 | `/api/detector/scan/status?limit=200` | 200 | 近期掃描無能源類 theme |
| sector 桶 | `/api/industry/sectors` | 200 | **38 桶**;最接近者為 `energy`「油電燃氣」= 6505、9933,**不是**再生能源 |
| sector 反查 | `/api/industry/sector-lookup?symbol=9958 / 3576 / 1513` | 200 | 三者皆 `found:false`;僅 9933 `found:true` → 油電燃氣 |
| 產業權重表 | `/api/dashboard/industry-classification` | 200 | `energy`「能源電力」權重 **0.05**、`semiconductor` **0.30**、`ai_supply_chain` **0.10**。**8:1 的結構性傾斜 already 寫在 atlas 自己的權重表裡** |
| narrative chains | `/api/narrative/chains` | 200 | 4 條 chain(AI_capex_surge 0.7695 最高),**無**能源/綠能 chain |
| narrative templates | `/api/narrative/templates` | 200 | **29 個模板**,**無**再生能源模板 |
| 總經欄位 | `/api/macro/snapshot/latest` | 200 | 有 `oil`(CL=F 92.41,−2.33%)、`copper`、`silver`;**無**任何再生能源/發電欄位 |

**⇒ 本模板不綁任何 detector id**(不編 `renewable_energy_divergence` 這種不存在的 theme)。分歧計算由 **atlas-wiki 端 cron 腳本自算**,只消費上面**已存在**的讀取端點。

**若要 atlas 端原生支援,需要的工作(未做,僅列出)**:
1. 新增 detector theme `renewable_energy_divergence`(KB pipeline),輸入需 macro 端新增綠能/發電資料源。
2. `/api/industry/sectors` 增 bucket `renewable_energy`(現行 38 桶無此桶);`/api/dashboard/industry-classification` 之 `energy` 增子節點(再生能源發電 / 電網重電)。
3. macro snapshot 增欄位(例:台灣再生能源裝置容量、台電電網標案金額、離岸風電併網量)。
**在上述 1–3 落地前,本模板維持「wiki 端自算」形態,狀態 = draft(見 §5)。**

## §4 觸發後執行(散戶解讀,對位 SK-31 §4)

1. 寫入 `~/workspace/atlas-notes/04-daily/{日期}-renewable-divergence.md`,記 `gap_rev`、`gap_rs`、兩臂逐檔原始值 + 抓取時間。
2. Telegram 通知(對位 SOUL §4.1;週末與空白行不計入長度,見 AGENTS.md §5 硬規則 4)。
3. 交叉確認(不通過就不發「高信心」字眼):`/api/narrative/chains` 的 `AI_capex_surge` score、`/api/capital-flow/summary` 的 `dominant_force`。
4. 落 `_consult-index.md` 對位紀錄(觸發成功或**未達觸發條件**都留痕)。

**散戶一句話**:「全球綠能外資腰斬,但台股綠能族群營收仍年增 46% —— 這條線在追『外資撤、台灣本地需求撐』的落差;兩臂差距收斂或反轉時,才是換股時點。」

## §5 結構性誠實護欄與失敗模式

- **本模板今日實測 = 未觸發**:C1 成立(+41.86 ≥ 15.0)但 C2 不成立(+3.27 < 5.0)。**未觸發是正確行為,不是故障**(對位 T3-A14 v8 結構性誠實)。
- **狀態 = draft(未啟用)**:門檻僅有 1 個交易日的 baseline,**未經 60 交易日校準**,故不得寫 `status: active`;`trigger-monitor.py` 亦不納入 TEMPLATES 字典(避免每 5 分鐘被誤掃;對位 #15 的 `cycle_type: cron-cadence` 同款處理)。
- **失敗模式(必須標示,不得掩蓋)**:
  1. **覆蓋率缺口**:`6244 茂迪`、`3691 碩禾` 在 `/api/stock/technical` 回 `NOT_COVERED`(`quote_covered:true`,2026-09-27 實測)。⇒ **C2 只用 3 檔**(3576/6477/9958),C1 用 5 檔,兩臂樣本不同,必須在輸出中標明。
  2. **臂內離散極大**:綠能發電臂 σ = 47.03 pp(vs 電網臂 9.68 pp)。單檔財報事件即可推動整個臂 ⇒ 必讀逐檔值,不可只看均值。
  3. **月頻延遲**:月營收每月 10 日後才更新(實測 1513 為 2026-08 資料)⇒ C1 有最長 40 天陳舊期。
  4. **不交易個股**:本模板只輸出「分歧訊號」,不含下單;`atlas 端 sector 桶缺失` 意味無法用 `industry_sector_lookup` 驗證成分股,需人工維護臂名單。
  5. **反轉即失效**:兩臂方向反轉(電網領先綠能)時,同一組門檻成立但**解讀相反** ⇒ 通知必附方向欄位。
- **禁止**:❌ mock 觸發 ❌ 用單臂訊號冒充雙臂確認 ❌ 把「未覆蓋」寫成「持平」 ❌ 繞過 governance-log 留痕。

## §6 對位 SK-31 與憲章

| SK-31 § | 本模板 § | 連接 |
|---------|---------|------|
| §atlas 對位表「未存在:trigger-renewable-energy-divergence ❌ 缺」 | 全檔 | 該列由「缺」改「已落(第 16 模板)」 |
| §未消化「第 16 template(待產)」 | 全檔 | 該條已解,移出 §未消化 |
| §2 論文版第 5 點(地理路徑偏離) | §2 先驗錨點 | 全球 FDI 與台灣營收的落差 |
| §4 散戶解讀 | §4 觸發後執行 | 可操作訊號 |
| §5 驗證 | §3 端點實測表 | 結構性誠實 |

| 對位項 | 內容 |
|--------|------|
| ATLAS_METHODOLOGY §二 | 第 1 層(全球資本配置)→ 第 2 層(台灣產業營收) |
| 七時期 / 三態 | RISK_ON 兩臂分歧訊號加權;RISK_OFF 只留風險提示,不推加碼 |
| 策略 archetype 正本(AGENTS.md §12) | **跟隨聰明錢**;E5a 策略類別 = Tactical(事件/落差套利) |
| 散戶語言 | 「外資撤綠能、台灣本地需求撐綠能」的落差 |

## §7 為什麼這模板值得加

- 本檔加入前實測 `ls templates/trigger-*.md | wc -l` = **20**;`git grep -l '相對強弱\|相對強度\|兩臂\|價差' templates/` = **0 命中**,即沒有一條是「兩個產業臂互相比較」的分歧型 — 全是單一資產/單一事件的門檻型。分歧型才是「找信息差」的直接對位。
- 補上 SK-31 §未消化最後一條待辦,且**不是**靠新增 detector 假裝完成(§3 已證 atlas 端無此能力)。
- 2027-04 驗收日(對位 SK-31 `cycle_label=2026H2`、`decay_until=2027Q1-WIR-revision`)WIR + HAI 換版時,可回看本模板的 `gap_rev` 序列是否領先報告數字。

## §8 不該做的事

- ❌ 不要為本模板編一個 atlas detector id。
- ❌ 不要把兩臂門檻做成 OR(必須 AND + 同向,否則單臂雜訊即觸發)。
- ❌ 不要把未覆蓋檔(6244/3691)當 0 代入均值。
- ❌ 不要在未完成 60 交易日校準前把狀態改成 `active`。
- ❌ 不要繞過 `_consult-index.md` 留痕。

參見:[[SK-31-ai-investment-cycle-2026]](本模板的母頁)、[[templates/trigger-equipment-capex-external-report-cycle]](#15,週期型)、[[templates/trigger-megaproject-2-quarter-lag]](#14,設備鏈 lag)
