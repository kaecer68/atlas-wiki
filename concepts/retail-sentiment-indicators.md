---
title: 散戶情緒指標：因果鏈第六層反向指標補課
created: 2026-08-22
updated: 2026-08-22
type: concept
tags: [framework, signal, contrarian, L6]
sources:
  - docs/ATLAS_METHODOLOGY.md v1.0 §二 第六層 + §四 散戶
  - concepts/taiwan-stock-market-structure.md（維持率現制：整戶 130% 追繳、追繳未補即處分,2022-04-01 起）
  - concepts/taiwan-chip-flow-analysis.md（當沖分級、集保分級）
  - concepts/taiwan-money-flow-seven-institutional-buckets.md（分點警示、門檻紀律）
confidence: medium
contested: false
contradictions: []
---

# 散戶情緒指標（因果鏈第六層）

> **一句話**：本頁是憲章因果鏈第六層「散戶情緒與籌碼」的補課頁——散戶情緒是**反向指標**，憲章原文：「融資高點 ≈ 市場頭部；融資斷頭潮 ≈ 市場底部。」2026-08-22 審計時 Google Trends 0 命中, 此頁補上 [2026-08-22 audit-fix]。

> 層級命名對齊憲章 §二中文層名；英數 L1-L5 保留給 atlas strategy_techniques 策略分層 [2026-08-22 iter2]

## 一、五個指標總表

| 指標 | 意義 | 公布節奏 | 判讀邏輯 |
|------|---------------|---------|---------|
| 融資餘額 + 維持率 | 槓桿 + 壓力水位 | 每日盤後（證交所） | 反向：高點≈頭部, 斷頭潮≈底部 |
| 當沖佔比 | 投機熱度 | 每日盤後 | 過熱 = 短線風險升高 |
| 散戶買賣超 + 集保分級 | 實際行為 + 籌碼結構 | 每日盤後 / 集保按月 [節奏需驗證] | 大戶增+散戶增 = 末期警訊 |
| Google Trends | 關注熱度（反向） | 即時/週更新 [資料管道待驗證] | 極端關注 ≈ 擁擠 |
| 券商分點進出 | 進出結構 | 每日盤後彙整 [管道需驗證] | 分點 ≠ 法人身份 |

### 1.1 融資餘額與融資維持率

- **意義**：融資餘額 = 散戶借錢買股金額（[[concepts/taiwan-chip-flow-analysis|籌碼面]] §5.1）；維持率 = 散戶壓力水位（憲章因果鏈第六層）。
- **現制門檻**：整戶擔保維持率低於 130% 通知追繳,限期未補足即處分擔保品（2022-04-01 起整戶新制；市場口語的 120% 斷頭線屬舊制簡化說法 [待證交所驗證]）（[[concepts/taiwan-stock-market-structure|市場結構]] §5.2）[2026-08-22 audit-fix]；憲章「轉折下壓」訊號用 150%——非追繳線, 勿混用。
- **判讀**：3 個月趨勢 + 分佈百分位；急速下降（斷頭潮）≈ 底部（憲章）。atlas 對位：`margin-balance-extreme` / `margin-trend-reversal`（[[concepts/taiwan-chip-flow-analysis|籌碼面]] §9.1）、[[templates/trigger-margin-350b]]。

### 1.2 當沖佔比

- **定義**：當沖買進成交值 ÷ 總成交值（[[concepts/taiwan-chip-flow-analysis|籌碼面]] §5.3）。
- **分級**（[[concepts/taiwan-chip-flow-analysis|籌碼面]] §5.3）：<30% 正常 / 30–50% 熱絡 / 50–70% 過熱 / >70% 嚴重過熱；憲章高原期條件 >35%。

### 1.3 散戶買賣超與集保戶數分級

- **散戶買賣超**：非官方直發、推算值 [需驗證]——散戶屬「行為代理層」（[[concepts/taiwan-money-flow-seven-institutional-buckets|七大資金勢力]]）；atlas `macro_get_capital_flow_latest` / `capital_flow_daily` 有散戶維度。
- **集保分級**：20 張以下散戶 / 400 張以上大戶——研究慣例, 非官方定義（[[concepts/taiwan-chip-flow-analysis|籌碼面]] §6.2）；按月發布 [節奏需驗證]。
- **判讀**：大戶增 + 散戶增 + 股價漲 = 籌碼流向散戶 → 末期警訊；散戶減 + 股價跌 = 籌碼集中 → 底部（[[concepts/taiwan-chip-flow-analysis|籌碼面]] §6.2）。

### 1.4 Google Trends

- **意義**：散戶關注熱度（反向指標, 憲章因果鏈第六層）。
- **現況**：本庫原 0 命中 [2026-08-22 audit-fix], 此頁補上；資料管道待建立 [資料管道待驗證]。既有研究註記：延遲高、PTT/Dcard 爬蟲有法律風險（raw/articles/atlas-trading-signals-audit-hints-v0.1.md）。
- **判讀**：熱度百分位極端高 ≈ 擁擠（頭部警訊候選）；極端低 ≈ 無人問津（機會區）。

### 1.5 券商分點進出

- **意義**：散戶進出結構（憲章因果鏈第六層原文）。
- **警示**：分點不是法人身份——同機構可分散多帳戶、券商可代客交易, 「前十大分點集中度 > 50% = 主力進場」不能當規則（[[concepts/taiwan-money-flow-seven-institutional-buckets|七大資金勢力]] §3）。
- **用法**：只當個股籌碼集中度線索, 與法人/集保交叉後才下結論。

## 二、反向指標使用規則

1. **只對「極端」動作, 中間區間無資訊**：極端 = 指標自身歷史分佈的百分位（如前/後 10%）, 不是絕對值。
2. **不用固定門檻**（[[concepts/taiwan-money-flow-seven-institutional-buckets|七大資金勢力]] §3）——「單日 50 億不是跨市場穩定門檻」；融資 5000 億、當沖 50% 只當參考刻度, 訊號看百分位 + 3 個月趨勢。
3. **反向訊號對位七時期**：融資高點 ≈ 頭部（高原/盤整警訊）；斷頭潮 ≈ 底部（轉折下壓/黑天鵝末端）。「資金對抗」布局點 = 低迷期末端：外資賣壓衰竭 + 公股買超 + 融資大減（憲章 §三 C）。七時期為真值, RISK_ON/OFF/NEUTRAL 只是向下相容層。
4. **多指標共振才動作**：融資暴增 + 當沖過熱 = 頭部警訊（憲章 §五）；單一指標到極端只列觀察。

## 三、與七大資金勢力 3+2+2 的關係

- 七維錢潮雷達 3+2+2（憲章）：共識 3 官方 → 行為 2 代理 → 訊號 2 領先（細項見 [[concepts/taiwan-chip-flow-analysis|籌碼面]] §2）。
- **散戶屬行為代理層**：本頁五指標都是代理/推算, 非官方直發。
- **不可加權平均**：代理層不得與官方層同層計票或加權平均（憲章 3+2+2 分層）；散戶票只作反證——外資買超但融資暴增 = 分配/接盤風險（[[concepts/taiwan-money-flow-seven-institutional-buckets|七大資金勢力]] §4C）。
- 對位 [[concepts/funding-forces-taxonomy-e05-pending-approval|E05]]：行為層與官方層同層計票屬待簽核爭議, 簽核前不得混入官方共識。

## 四、散戶解讀與驗證

**最常踩的坑**：

1. 把每日融資增減當方向——融資是反向指標, 極端才有效。
2. 用絕對金額門檻（「融資 > 5000 億 = 危險」）——水位漂移, 要用分佈百分位。
3. 把「某分點大買」當主力——分點不是法人身份。
4. 忽略當沖結構——過熱時盤中訊號與收盤方向脫節。

**驗證**：`macro_get_capital_flow_latest`、`capital_flow_daily`（散戶行為層）、`macro_get_snapshot_latest`（retail_margin_balance）[2026-08-22 audit-fix 對位 [[concepts/atals-mcp-tools-reference|MCP 參考]]]；融資原始數值以證交所為準 [通識]。

**未消化**：

- [ ] Google Trends 管道與延遲 [待驗證]
- [ ] 散戶買賣超推算方法 [待驗證]
- [ ] 集保戶股權分散表公布節奏 [待驗證]
- [ ] 五指標百分位極端與後續報酬回測 [待驗證]

## 參見

- [[concepts/taiwan-stock-market-structure]]（維持率現制：整戶 130% 追繳、未補即處分）
- [[concepts/taiwan-money-flow-seven-institutional-buckets]]（分點警示、門檻紀律）
- [[concepts/taiwan-export-orders-semiconductor-cycle]]（因果鏈第二層基本面層）
